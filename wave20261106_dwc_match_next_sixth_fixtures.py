import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json
from wave20261106_dwc_match_next_sixth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_next_sixth_build import build

GP,GT=0x209becc,0x209bf8c
GLOBAL,CTRL,STOP,SP=0x21d19e0,0x2171000,0x27e0000,0x2701000
PROVIDERS={0x209c610,0x209f130,0x209d03c}


def vector(address,seed):
    return dict(result=seed%(5 if address==GP else 8),state=(seed//5)%8,loginState=(seed//40)%4)


def model(address,v):
    result=v['result']
    if result==0 or address==GT and result in [2,5]:return dict(kind='return',value=0),None
    if address==GT:
        fatal,code={1:(9,-67001),3:(6,-67010),4:(6,-67030),6:(6,-67070),7:(6,-67080)}[result];return dict(kind='provider',address=hex(0x209c610)),[fatal,code&0xffffffff]
    fatal,sub={1:(9,-1),2:(9,-2),3:(6,-10),4:(6,-20)}[result];state=v['state'];base=-61000 if state in [1,2] else -81000 if state==5 else -71000 if state==4 else -91000;target=0x209c610 if state==1 or state==2 and v['loginState']<1 else 0x209f130 if state==5 else 0x209d03c
    return dict(kind='provider',address=hex(target)),[fatal,(base+sub)&0xffffffff]


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);context=bytearray([0x61])*160;struct.pack_into('<I',context,36,v['state']);struct.pack_into('<I',context,156,v['loginState']);memory={GLOBAL:struct.pack('<I',CTRL),CTRL:bytes(context)}
    for at,data in memory.items():cpu.mem_write(at,data)
    initial=[(0x64d00000+i*0x101+seed)&0xffffffff for i in range(15)];initial[0]=v['result'];initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    expected,frame=model(a,v);observed=None;interface=True;pcs=[]
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual error caller return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual error provider mode differs')
            observed=dict(kind='provider',address=hex(at));interface=frame is None or regs[:len(frame)]==frame;machine.emu_stop();return
        if not a<=at<a+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Error caller escaped genuine bounded body/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        raise ValueError('Unexpected SDK control write before error provider')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Error caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items())
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={GP:('if (result == GP_NO_ERROR) return GP_NO_ERROR;','if (result == GP_NO_ERROR) return GP_MEMORY_ERROR;'),GT:('result = GT2Success;','result = GT2NetworkError;')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(160):
            v=vector(a,seed);left=run(image,row,native,v,seed);right=run(image,row,compiled,v,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent error routing/model differs',left,right))
            records.append(left)
        directory=WORK/'wrong-c'/f'{a:08x}';directory.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
        before,after=variants[a];text=(ROOT/row['source']).read_text();changed=text.replace(before,after,1)
        if text==changed:raise ValueError('Meaningful whole-C error negative did not mutate')
        source=directory/'wrong.c';source.write_text(changed);bad,body=build(source,directory/'proof',negative=True);failed=sum(not run(image,row,body,vector(a,seed),seed)['modelPassed'] for seed in range(16))
        if not failed:raise ValueError('Wrong C did not reject independent error result/routing model')
        negative.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,after],realLink=bad['realLink']))
    coverage={row['address']:sorted({r['observed']['address'] for r in records if r['address']==row['address'] and r['partialProviderStopped']}) for row in rows}
    if coverage[hex(GP)]!=sorted(hex(x) for x in PROVIDERS) or coverage[hex(GT)]!=[hex(0x209c610)]:raise ValueError('Original error provider branch coverage incomplete')
    limits=['320 paired actual original/source caller entries: complete no-error/rejected/duplicate-address returns and original error routing/error codes, initialized core/login states, all three GP provider branches.0callee/provider instructions executed; no synthetic returns.','GP errors limited to0..4 and GT2 errors0..7. Remaining error enumerators/sentinels and uninitialized SDK control are untested and may have undefined source-level behavior. Provider error handling/recovery/callbacks, network/device/game/nativeWindows execution remain unproven.0storage extent/authorship credit.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,requiredProviderBranchCoverage=coverage,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
