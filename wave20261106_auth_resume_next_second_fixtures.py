import hashlib
import json
import random
import re
import struct
import match_runtime as C
import unicorn as un
import unicorn.arm_const as ar
from project import ROOT,write_json
from wave20261106_auth_resume_next_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK as OWN_WORK


SP,STOP,INPUT,WORK,HOLD,GLOBAL=0x027e0000,0x04000000,0x03001000,0x03005000,0x03007000,0x021d18cc
HELPERS=[0x020946ec,0x02094818,0x02096050,0x02095864,0x02095cec]
PROVIDERS={0x02007a9c:'arm',0x0208a268:'thumb',0x02090554:'thumb',0x02099138:'thumb',0x02090580:'thumb'}


def helper_specs(image,inventory):
    result=[]
    for address in HELPERS:
        record=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x%08x'%address,line)),None)
        if record is None:raise ValueError('Exact configured pure helper boundary absent')
        size=int(re.search(r'size=(0x[0-9a-f]+)',record).group(1),0);result.append(dict(address=address,bytes=size,mode='thumb',canonicalInventoryRecord=record,targetSha256=hashlib.sha256(image[address-0x02000000:address-0x02000000+size]).hexdigest(),sourceCredit=0))
    return result


def vector(address,seed):
    rng=random.Random(0x20ac0000+seed);source=bytes(rng.randrange(256)for unused in range(96));work=bytearray(3352);hold=bytearray(36);work[3339]=0x10;args=[WORK,0,0,0];answer=None;provider=None;dns=None
    if address==0x02096050:args[0]=INPUT;answer=int.from_bytes(source[:4],'little')
    elif address==0x02096094:
        prefix=seed if seed<256 else 0xffffffff-(seed-256);args[0]=prefix;shift=(32-prefix)&0xffffffff;shift=shift-(1<<32)if shift&0x80000000 else shift;mask=(0xffffffff<<max(shift,0))&0xffffffff;answer=int.from_bytes(mask.to_bytes(4,'big'),'little')
    elif address==0x02095bd0:
        phase=[0,1,2,6,17,255,3,4,5][seed%9];args[1]=phase;answer=6 if phase in(3,4,5)else phase
    elif address==0x020960d0:
        kind=[0,1,2,3,4,5,6,255][seed%8];work[3341]=kind
        if kind<6:
            index=kind if kind<3 else kind-3;page=index*256;work[page+192]=0 if seed//8%3!=0 else 1;primary=bytes([8,8,seed,1])if seed//8%3==2 else bytes(4);secondary=bytes([1,1,1,seed]);work[page+200:page+204]=primary;work[page+204:page+208]=secondary
            if work[page+192]==0 and any(primary):provider=0x02090580;dns=[int.from_bytes(primary,'little'),int.from_bytes(secondary,'little')]
    elif address==0x02095aec:provider=0x02007a9c
    elif address==0x02095d50:provider=0x0208a268
    elif address==0x02095e9c:provider=0x02090554
    elif address==0x02095f34:provider=0x02099138
    else:raise ValueError('Unknown exact second caller')
    return dict(source=source,work=bytes(work),hold=bytes(hold),args=args,answer=answer,provider=provider,dns=dns)


def run(image,row,body,seed,specs):
    address=int(row['address'],0);case=vector(address,seed);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x02000000,0x400000);cpu.mem_write(0x02000000,image);cpu.mem_write(address,body);cpu.mem_map(0x03000000,0x10000);cpu.mem_write(INPUT,case['source']);cpu.mem_write(WORK,case['work']);cpu.mem_write(HOLD,case['hold']);cpu.mem_write(GLOBAL,struct.pack('<5I',0,0,0,HOLD,WORK));cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_map(STOP,0x1000)
    initial=[0x6b000000+i*0x101+seed for i in range(15)];initial[:4]=case['args'];initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for register,value in zip(C.REGISTERS,initial):cpu.reg_write(register,value)
    observed=None;pcs=[];active=[];calls=0;returns=0
    def code(machine,at,size,user):
        nonlocal observed,calls,returns
        regs=[machine.reg_read(r)for r in C.REGISTERS];thumb=bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)
        while active and at==active[-1]:active.pop();returns+=1
        if at==STOP:
            if active or regs[4:12]!=initial[4:12]or regs[13]!=SP:raise ValueError('Original caller/helper ABI return differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS:
            if at!=case['provider']or thumb!=(PROVIDERS[at]=='thumb')or active:raise ValueError('Original opaque provider path/mode differs from independent case')
            if address in(0x02095aec,0x02095e9c)and regs[4]!=WORK:raise ValueError('Actual caller work-pointer boundary differs')
            if address==0x02095f34 and(regs[4]!=HOLD or regs[5]!=WORK):raise ValueError('Actual holder/work boundary differs')
            if case['dns']is not None:
                if regs[0]!=regs[13]+4 or regs[1]!=regs[13]or [struct.unpack('<I',machine.mem_read(p,4))[0]for p in regs[:2]]!=case['dns']:raise ValueError('Actual resolver caller stack/value interface differs')
            observed=dict(kind='provider-stop',address=hex(at),providerInstructionsExecuted=0,resolverValues=case['dns']);machine.emu_stop();return
        if address<=at<address+len(body):
            if not thumb:raise ValueError('Actual caller left Thumb mode')
        else:
            helper=next((item for item in specs if item['address']<=at<item['address']+item['bytes']),None)
            if helper is None or not thumb:raise ValueError(('Execution escaped genuinely configured pure helper set',hex(at)))
            if at==helper['address']:calls+=1;active.append(regs[14]&~1)
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if WORK<=at and at+size<=WORK+3352:return
        raise ValueError('Unexpected actual caller/helper memory write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Actual source/native caller did not reach bounded endpoint')
    expected='provider-stop'if case['provider']else'return';guards=all(bytes(cpu.mem_read(at,len(value)))==value for at,value in [(INPUT,case['source']),(WORK,case['work']),(HOLD,case['hold'])]);passed=observed['kind']==expected and guards and calls==returns
    if case['answer']is not None:passed=passed and observed['value']==case['answer']
    if not passed:raise ValueError(('Actual caller disagrees with independent field/phase/network-order model',hex(address),seed,observed,case['answer'],guards,calls,returns))
    return dict(address=row['address'],seed=seed,observed=observed,topReturned=expected=='return',partialProviderStopped=bool(case['provider']),modelPassed=passed,actualOriginalHelperInvocations=calls,actualOriginalHelperReturns=returns,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,OWN_WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();specs=helper_specs(image,(ROOT/'config/arm9/symbols.txt').read_text());records=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x02000000:address-0x02000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes();count=260 if address==0x02096094 else 32 if address==0x02096050 else 24 if address==0x020960d0 else 9 if address==0x02095bd0 else 4
        for seed in range(count):
            left=run(image,row,native,seed,specs);right=run(image,row,compiled,seed,specs)
            if left!=right:raise ValueError('Complete original and freshly linked caller traces differ')
            records.append(left)
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest();result=dict(status='passed',traceSha256=trace,records=records,actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*sum(r['topReturned']for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped']for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),wholeCNegativeControlsRejected=0,limits='Pure byte-order32/netmask260 and bounded phase/DNS guard returns execute; positive DNS stops before actual resolver with checked stack words. Search/start/host-ID/netcheck callers stop BEFORE first opaque timer/WCM/socket/netcheck provider body. Qualified original RAM-only helper executions carry0source/extent/storage credit. No provider/device/network/timing/game/Windows execution; no claim of all-domain behavior for huge-loop netmask inputs.')
    write_json(LANE/'caller-fixtures.json',result);return result
