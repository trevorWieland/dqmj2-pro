import hashlib
import json
import re
import struct
import match_runtime as C
import unicorn as un
import unicorn.arm_const as ar
from project import ROOT,write_json
from wave20261106_auth_core_next_third_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK as OWN_WORK


DESC=0x03009000
SP,STOP,WORK,HOLD,GLOBAL=0x027e0000,0x04000000,0x03005000,0x03007000,0x021d18cc
HELPERS=[0x020946ec,0x0209477c,0x020957f0]
PROVIDERS={0x02094a58:'thumb',0x02094ab0:'thumb',0x0208a268:'thumb'}


def helper_specs(image,inventory):
    result=[]
    for address in HELPERS:
        record=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x%08x'%address,line)),None)
        if record is None:raise ValueError('Actual original pure getter boundary absent')
        size=int(re.search(r'size=(0x[0-9a-f]+)',record).group(1),0);result.append(dict(address=address,bytes=size,mode='thumb',canonicalInventoryRecord=record,targetSha256=hashlib.sha256(image[address-0x02000000:address-0x02000000+size]).hexdigest(),sourceCredit=0))
    return result


def vector(address,seed):
    work=bytearray(3352);hold=bytearray(36);desc=bytearray(192);args=[DESC,0,0,0];hold[11]=0x55;provider=None;channel=[1,6,14,65535][seed%4];struct.pack_into('<H',desc,54,channel);phase=[0,1,2,3,3,3,3,4,5,6,17,255][seed%12];hold[9]=phase;work[3343]=[0,1,8][seed%3];work[3344]=9;work[3345]=[0,1,12,127,128,255][seed%6];struct.pack_into('<H',work,3350,[0,1,0x1555,0x8000][seed%4]);expected=bytearray(work);expectedHold=bytearray(hold)
    if address==0x020948d0:
        expectedHold[11]=1
        if phase==3:
            style=seed%4
            if style==0:struct.pack_into('<H',desc,10,0)
            elif style==1:struct.pack_into('<H',desc,10,4);desc[12]=0
            elif style==2:struct.pack_into('<H',desc,10,1);desc[12]=32;provider=0x02094a58
            else:struct.pack_into('<H',desc,10,32);desc[12:44]=b'X'*32;provider=0x02094a58
            if style<=2:
                old=struct.unpack_from('<H',expected,3350)[0];struct.pack_into('<H',expected,3350,old|(1<<(min(channel,13)-1)))
        elif phase==4:provider=0x02094ab0
        elif phase==5:provider=0x02094a58
    elif address==0x020956dc:provider=0x0208a268;args=[0,0,0,0]
    else:raise ValueError('Unknown qualified beacon/retry body')
    return dict(work=bytes(work),expectedWork=bytes(expected),hold=bytes(hold),expectedHold=bytes(expectedHold),desc=bytes(desc),args=args,answer=None,provider=provider,phase=phase)



def run(image,row,body,seed,specs):
    address=int(row['address'],0);case=vector(address,seed);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x02000000,0x400000);cpu.mem_write(0x02000000,image);cpu.mem_write(address,body);cpu.mem_map(0x03000000,0x10000);cpu.mem_write(WORK,case['work']);cpu.mem_write(HOLD,case['hold']);cpu.mem_write(DESC,case['desc']);cpu.mem_write(GLOBAL,struct.pack('<5I',0,0,0,HOLD,WORK));cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_map(STOP,0x1000);initial=[0x6d000000+i*0x101+seed for i in range(15)];initial[:4]=case['args'];initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for register,value in zip(C.REGISTERS,initial):cpu.reg_write(register,value)
    observed=None;pcs=[];active=[];calls=0;returns=0
    def code(machine,at,size,user):
        nonlocal observed,calls,returns
        regs=[machine.reg_read(r)for r in C.REGISTERS];thumb=bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)
        while active and at==active[-1]:active.pop();returns+=1
        if at==STOP:
            if active or regs[4:12]!=initial[4:12]or regs[13]!=SP:raise ValueError('Actual original caller/getter return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS:
            if active or at!=case['provider']or thumb!=(PROVIDERS[at]=='thumb'):raise ValueError('Actual original opaque provider/mode differs')
            if address==0x020956dc:
                if regs[5]!=WORK:raise ValueError('Actual retry work context differs before WCM provider')
            elif at==0x02094ab0:
                if regs[:2]!=[DESC,WORK]:raise ValueError('Actual different-list descriptor/work interface differs')
            elif at==0x02094a58:
                count=1 if case['phase']==5 else case['work'][3344];cursor=case['work'][3343] if case['phase']==5 else 0
                if regs[:3]!=[DESC,count,WORK+768+36*cursor]:raise ValueError('Actual search-list descriptor/count/page interface differs')
            observed=dict(kind='provider-stop',address=hex(at),providerInstructionsExecuted=0);machine.emu_stop();return
        if address<=at<address+len(body):
            if not thumb:raise ValueError('Actual caller left Thumb mode')
        else:
            helper=next((item for item in specs if item['address']<=at<item['address']+item['bytes']),None)
            if helper is None or not thumb:raise ValueError(('Execution escaped actual original pure getter set',hex(at)))
            if at==helper['address']:calls+=1;active.append(regs[14]&~1)
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if WORK<=at and at+size<=WORK+3352:return
        if HOLD<=at and at+size<=HOLD+36:return
        raise ValueError('Unexpected actual source/getter RAM mutation')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Original/source caller did not reach bounded endpoint')
    guards=bytes(cpu.mem_read(WORK,3352))==case['expectedWork']and bytes(cpu.mem_read(HOLD,36))==case['expectedHold']and bytes(cpu.mem_read(DESC,192))==case['desc'];expected='provider-stop'if case['provider']else'return';passed=observed['kind']==expected and guards and calls==returns
    if case['answer']is not None:passed=passed and observed['value']==case['answer']
    if not passed:raise ValueError(('Actual caller differs from independent mask/cursor/RAM model',hex(address),seed,observed,case['answer'],guards,calls,returns))
    return dict(address=row['address'],seed=seed,observed=observed,topReturned=expected=='return',partialProviderStopped=bool(case['provider']),modelPassed=passed,actualOriginalHelperInvocations=calls,actualOriginalHelperReturns=returns,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,OWN_WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();specs=helper_specs(image,(ROOT/'config/arm9/symbols.txt').read_text());records=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x02000000:address-0x02000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes();count=12 if address==0x020948d0 else 4
        for seed in range(count):
            left=run(image,row,native,seed,specs);right=run(image,row,compiled,seed,specs)
            if left!=right:raise ValueError('Complete original and fresh C caller traces differ')
            records.append(left)
    result=dict(status='passed',traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),records=records,actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*sum(r['topReturned']for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped']for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),wholeCNegativeControlsRejected=0,limits='Beacon12 vectors prove actual findAP byte11 mutation, inactive-phase returns, empty/zero-first-byte SSIDs, clamped positive-channel bit insertion through the actual pure canonical setter, and exact phase3/4/5 list-provider arguments. Retry stops BEFORE WCM_GetPhase. Pure original RAM getters/setter run with0source/extent/storage credit. No comparator/sort/add-list/WCM body execution; post-provider beacon/retry control,hardware/network/game/Windows behavior remains unexecuted.')
    write_json(LANE/'caller-fixtures.json',result);return result
