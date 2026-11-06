import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json
from wave20261106_dwc_auth_next_third_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_auth_next_third_build import build

THREAD,PARSE=0x20977cc,0x209798c
GLOBAL,CTRL,HTTP,STOP,SP=0x21d18f0,0x2171000,0x217c000,0x27e0000,0x2701000
PROVIDERS={0x2006890:'arm',0x209798c:'thumb',0x2097d94:'thumb',0x2007a9c:'arm',0x2098d0c:'thumb'}


def run(image,row,body,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);activity=seed%2;error=[0,2,3,7,8][(seed//2)%5];alloc=0x27e1000+(seed&1);free=0x27e2000+((seed>>1)&1);work=bytearray([0x61])*5108;struct.pack_into('<I',work,0x1314,HTTP);struct.pack_into('<II',work,0x120c,alloc,free);http=bytearray([0x63])*7188;struct.pack_into('<I',http,4128,error);struct.pack_into('<I',http,7076,activity);memory={GLOBAL:struct.pack('<III',0x11223344,0x22334455,CTRL),CTRL:bytes(work),HTTP:bytes(http)}
    for at,data in memory.items():cpu.mem_write(at,data)
    if a==THREAD:
        if activity:target=0x2006890;frame=[HTTP+6968]
        elif error==8:target=0x209798c;frame=[]
        elif error==7:target=0x2097d94;frame=[20]
        else:target=0x2007a9c;frame=[]
        args=[0x12345678]
    elif a==PARSE:target=0x2098d0c;frame=[HTTP,0];args=[]
    else:raise ValueError('Wrong Auth residual identity')
    initial=[0x64d00000+i*0x101+seed for i in range(15)];initial[:len(args)]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;interface=True;captured=True;pcs=[]
    def code(machine,at,size,user):
        nonlocal observed,interface,captured
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at in PROVIDERS and at!=a:
            if at!=target or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(PROVIDERS[at]=='thumb'):raise ValueError('Wrong original Auth provider/entry/mode')
            observed=dict(kind='provider',address=hex(at));interface=regs[:len(frame)]==frame
            if a==PARSE:captured=regs[4]==free and regs[5]==alloc
            machine.emu_stop();return
        if not a<=at<a+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Auth caller escaped original bounded body')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if a==THREAD and at==CTRL+0x1008 and size==4:return
        raise ValueError('Unexpected original/source caller RAM write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=20000)
    if observed is None:raise ValueError('Actual Auth caller did not reach bounded provider')
    expected_work=bytearray(work)
    if a==THREAD and not activity and error!=8:struct.pack_into('<I',expected_work,0x1008,20100)
    guards=all(bytes(cpu.mem_read(at,len(data)))==(bytes(expected_work) if at==CTRL else data) for at,data in memory.items())
    return dict(address=row['address'],seed=seed,vector=dict(activityWord=activity,httpError=error,alloc=hex(alloc),free=hex(free)),observed=observed,topReturned=False,partialProviderStopped=True,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,earlyCallbackCapturePassed=captured,modelPassed=observed==dict(kind='provider',address=hex(target)) and interface and guards and captured,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[];variants={THREAD:('result.returncode = 20100;','result.returncode = 20101;'),PARSE:('native_fn_02098d0c(http,0)','native_fn_02098d0c(http,1)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(20 if a==THREAD else 8):
            left=run(image,row,native,seed);right=run(image,row,compiled,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent actual Auth provider/state/capture model differs',left,right))
            records.append(left)
        folder=WORK/'wrong-c'/f'{a:08x}';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        before,after=variants[a];text=(ROOT/row['source']).read_text();changed=text.replace(before,after,1)
        if changed==text:raise ValueError('Meaningful whole-C Auth residual negative did not change')
        source=folder/'wrong.c';source.write_text(changed);bad,body=build(source,folder/'proof',negative=True);failed=sum(not run(image,row,body,seed)['modelPassed'] for seed in range(10))
        if failed<1:raise ValueError('Wrong whole C did not reject independent measured provider/state model')
        negative.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,after],realLink=bad['realLink']))
    limits=['28paired actual full caller entries56pre-provider stops;0complete caller returns,0callee/provider/helper instructions or synthetic returns. Thread checks active/inactive HTTP lifecycle and HTTP0/2/3/7/8 paths through actual join/parse/error/tick callsite,positive20100 result write and full RAM guards. Parser checks exact parse-provider frame and early alloc/free callback capture inR5/R4 for both ARM/Thumb pointer tags; callbacks remain unexecuted.','All post-provider HTTP parsing/account-recovery/retry/tick/division/sleep/locking/flash behavior is complete-byte genuine-link exact but unexecuted. Original API types/offsets/prototype presence are independently compiled; naming the HTTPthread+108 word as id/state remains unproven.','0network/device/I/O/timer/hardware/game/nativeWindows execution or external BSS/data storage/callee source credit. Native unsigned64 compiler helper260dc binds only its genuine canonical ARM entry; helper body not executed/reconstructed.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();result=dict(status='passed',records=records,nativeAndCompiledReturningCalls=0,nativeAndCompiledPartialStops=2*len(records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',result);return result
