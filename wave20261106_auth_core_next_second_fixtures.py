import hashlib
import json
import re
import match_runtime as C
import unicorn as un
import unicorn.arm_const as ar
from project import ROOT,write_json
from wave20261106_auth_core_next_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK as OWN_WORK


SP,STOP,WORK,WEP=0x027e0000,0x04000000,0x03005000,0x03008000
PROVIDERS={0x02094f58:'thumb',0x0208a268:'thumb',0x020961bc:'thumb',0x0209615c:'thumb'}


def helper_specs(image,inventory):
    address=0x02008e0c;record=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x02008e0c',line)),None)
    if record is None:raise ValueError('Actual pure byte-copy entry/mode missing')
    size=int(re.search(r'size=(0x[0-9a-f]+)',record).group(1),0);return [dict(address=address,bytes=size,mode='arm',canonicalInventoryRecord=record,targetSha256=hashlib.sha256(image[address-0x02000000:address-0x02000000+size]).hexdigest(),sourceCredit=0)]


def vector(address,seed):
    work=bytearray((i*13+seed*7)&255 for i in range(3352));work[3347]=[0,1,10][seed%3];wep=bytearray([0xcc])*82;wep[0]=seed%4;args=[WORK,0,0,0];provider=None;answer=None;expected=bytearray(wep)
    if address==0x02094d9c:provider=0x02094f58
    elif address==0x02094e68:provider=0x0208a268
    elif address==0x020950e4:
        kind=[0,1,2,3,4,5,6,7,8,9,10,0xffffffff][seed%12];args=[WORK,kind,WEP,0]
        if kind<=2:expected[0]=work[kind*256+230]&3;expected[2:18]=work[kind*256+128:kind*256+144]
        elif kind<=5:page=(kind-3)*256;expected[0]=1;expected[2:7]=work[page+209:page+214]
        elif kind in(6,7):expected[0]=2;provider=0x020961bc if kind==6 else 0x0209615c
        if provider is None:answer=int(expected[0]!=0)
    else:raise ValueError('Unknown grounded connection body')
    return dict(work=bytes(work),wep=bytes(wep),expectedWep=bytes(expected),args=args,provider=provider,answer=answer)


def run(image,row,body,seed,specs):
    address=int(row['address'],0);case=vector(address,seed);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x02000000,0x400000);cpu.mem_write(0x02000000,image);cpu.mem_write(address,body);cpu.mem_map(0x03000000,0x10000);cpu.mem_write(WORK,case['work']);cpu.mem_write(WEP,case['wep']);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_map(STOP,0x1000);initial=[0x6e000000+i*0x101+seed for i in range(15)];initial[:4]=case['args'];initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];active=None;calls=0;returns=0
    def code(machine,at,size,user):
        nonlocal observed,active,calls,returns
        regs=[machine.reg_read(r)for r in C.REGISTERS];thumb=bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)
        if active is not None and at==active:active=None;returns+=1
        if at==STOP:
            if active is not None or regs[4:12]!=initial[4:12]or regs[13]!=SP:raise ValueError('Actual original caller/copy return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS:
            if at!=case['provider']or not thumb or active is not None:raise ValueError('Actual imported provider path/mode differs')
            if address==0x02094d9c and(regs[0]!=WORK or regs[4]!=WORK+1136+case['work'][3347]*192):raise ValueError('Actual selected BSS/type-provider interface differs')
            if address==0x02094e68 and regs[5]!=WORK:raise ValueError('Actual connection work boundary differs')
            if address==0x020950e4 and regs[:2]!=[WORK+1136+case['work'][3347]*192+12,WEP+2]:raise ValueError('Actual imported key-wrapper SSID/output interface differs')
            observed=dict(kind='provider-stop',address=hex(at),providerInstructionsExecuted=0);machine.emu_stop();return
        if address<=at<address+len(body):
            if not thumb:raise ValueError('Actual caller left Thumb mode')
        else:
            helper=next((item for item in specs if item['address']<=at<item['address']+item['bytes']),None)
            if helper is None or thumb:raise ValueError(('Execution escaped actual canonical pure copy body',hex(at)))
            if at==helper['address']:calls+=1;active=regs[14]&~1
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if WEP<=at and at+size<=WEP+82:return
        raise ValueError(('Unexpected original caller/copy RAM mutation',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Actual caller did not reach bounded return/provider')
    expected='provider-stop'if case['provider']else'return';guards=bytes(cpu.mem_read(WORK,3352))==case['work']and bytes(cpu.mem_read(WEP,82))==case['expectedWep'];passed=observed['kind']==expected and guards and calls==returns
    if case['answer']is not None:passed=passed and observed['value']==case['answer']
    if not passed:raise ValueError(('Actual caller differs from independent page/key/guard model',hex(address),seed,observed,case['answer'],guards,calls,returns))
    return dict(address=row['address'],seed=seed,observed=observed,topReturned=expected=='return',partialProviderStopped=bool(case['provider']),modelPassed=passed,actualOriginalHelperInvocations=calls,actualOriginalHelperReturns=returns,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,OWN_WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();specs=helper_specs(image,(ROOT/'config/arm9/symbols.txt').read_text());records=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x02000000:address-0x02000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(24 if address==0x020950e4 else 4):
            left=run(image,row,native,seed,specs);right=run(image,row,compiled,seed,specs)
            if left!=right:raise ValueError('Original and freshly linked connection traces differ')
            records.append(left)
    result=dict(status='passed',traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),records=records,actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*sum(r['topReturned']for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped']for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),wholeCNegativeControlsRejected=0,limits='Key-selector24 cases cover all3 native256-byte pages,low2-bit mode,16/5-byte copies,opaque USB/shop wrapper pointer boundaries,8/9/out-of-range guards and preserved keyID/tail bytes. Original canonical pure copy executes0source/extent credit. Setup/state callers stop BEFORE actual type-selection/WCM bodies; key wrappers stop before body. No post-provider connection-flow,crypto-wrapper,hardware/network/game/Windows or imported storage execution/authorship credit.')
    write_json(LANE/'caller-fixtures.json',result);return result
