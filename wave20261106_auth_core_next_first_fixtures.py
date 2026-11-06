import hashlib
import json
import re
import struct
import match_runtime as C
import unicorn as un
import unicorn.arm_const as ar
from project import ROOT,write_json
from wave20261106_auth_core_next_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK as OWN_WORK


SP,STOP,WORK,HOLD,GLOBAL=0x027e0000,0x04000000,0x03005000,0x03007000,0x021d18cc
HELPERS=[0x020946ec,0x0209477c]
PROVIDERS={0x02007a9c:'arm',0x0208a268:'thumb',0x020953e0:'thumb'}


def helper_specs(image,inventory):
    result=[]
    for address in HELPERS:
        record=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x%08x'%address,line)),None)
        if record is None:raise ValueError('Actual original pure getter boundary absent')
        size=int(re.search(r'size=(0x[0-9a-f]+)',record).group(1),0);result.append(dict(address=address,bytes=size,mode='thumb',canonicalInventoryRecord=record,targetSha256=hashlib.sha256(image[address-0x02000000:address-0x02000000+size]).hexdigest(),sourceCredit=0))
    return result


def vector(address,seed):
    work=bytearray(3352);hold=bytearray(36);hold[9]=[0,2,3,6][seed%4];args=[WORK,0,0,0];answer=None;provider=None
    if address==0x02095818:
        masks=[0,1,0x1000,0x1fff,0x1555,0xaaaa,0x8000];counts=[0,1,2,12,13,255,65535];mask=masks[seed//7];count=counts[seed%7];struct.pack_into('<H',work,3350,mask);args[0]=count;selected=[i for i in range(13)if mask&(1<<i)];answer=selected[count]if count<len(selected)else 0xffffffff
    elif address==0x02095864:
        args[0]=[0,1,2,3,4,5,6,17,255][seed%9]
        if args[0]in(3,4,5):provider=0x02007a9c
    elif address==0x02095778:provider=0x0208a268
    elif address in(0x02095910,0x02095954):provider=0x02007a9c
    elif address==0x020959d0:
        work[3339]=[0x03,0x1a,0xe5,0xff][seed%4];work[3349]=0x63;provider=0x020953e0
    else:raise ValueError('Unknown new complete source identity')
    expected=bytearray(work)
    if address==0x020959d0:expected[3339]=(expected[3339]&15)|((((expected[3339]>>4)+1)&15)<<4);expected[3349]=0
    return dict(work=bytes(work),expectedWork=bytes(expected),hold=bytes(hold),args=args,answer=answer,provider=provider)


def run(image,row,body,seed,specs):
    address=int(row['address'],0);case=vector(address,seed);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x02000000,0x400000);cpu.mem_write(0x02000000,image);cpu.mem_write(address,body);cpu.mem_map(0x03000000,0x10000);cpu.mem_write(WORK,case['work']);cpu.mem_write(HOLD,case['hold']);cpu.mem_write(GLOBAL,struct.pack('<5I',0,0,0,HOLD,WORK));cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_map(STOP,0x1000);initial=[0x6d000000+i*0x101+seed for i in range(15)];initial[:4]=case['args'];initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
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
            if address==0x020959d0 and regs[0]!=0:raise ValueError('Actual around-list mode argument differs')
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
        raise ValueError('Unexpected actual source/getter RAM mutation')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Original/source caller did not reach bounded endpoint')
    guards=bytes(cpu.mem_read(WORK,3352))==case['expectedWork']and bytes(cpu.mem_read(HOLD,36))==case['hold'];expected='provider-stop'if case['provider']else'return';passed=observed['kind']==expected and guards and calls==returns
    if case['answer']is not None:passed=passed and observed['value']==case['answer']
    if not passed:raise ValueError(('Actual caller differs from independent mask/cursor/RAM model',hex(address),seed,observed,case['answer'],guards,calls,returns))
    return dict(address=row['address'],seed=seed,observed=observed,topReturned=expected=='return',partialProviderStopped=bool(case['provider']),modelPassed=passed,actualOriginalHelperInvocations=calls,actualOriginalHelperReturns=returns,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,OWN_WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();specs=helper_specs(image,(ROOT/'config/arm9/symbols.txt').read_text());records=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x02000000:address-0x02000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes();count=49 if address==0x02095818 else 9 if address==0x02095864 else 4
        for seed in range(count):
            left=run(image,row,native,seed,specs);right=run(image,row,compiled,seed,specs)
            if left!=right:raise ValueError('Complete original and fresh C caller traces differ')
            records.append(left)
    result=dict(status='passed',traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),records=records,actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*sum(r['topReturned']for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped']for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),wholeCNegativeControlsRejected=0,limits='Stealth-channel49 mask/u16-index cases check full signed32-bit return including-1; restart guarded phases return. Actual pure RAM getters run with0source/extent/storage credit. Search/start/around/restart-active/list callers stop BEFORE actual WCM/clock/list provider bodies; last group proves pre-provider4-bit wrap/count reset and exact list-mode argument. No provider/hardware/network/game/Windows execution.')
    write_json(LANE/'caller-fixtures.json',result);return result
