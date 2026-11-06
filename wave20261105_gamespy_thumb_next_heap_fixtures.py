import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_heap_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/heap'
WORK=ROOT/'work/w5gt/heap/fixtures'
TABLE,STOP,SP=0x21d2374,0x27e0000,0x2701000


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    table=struct.pack('<IIIII',0x11223344,0x55667788,v['callback'],0x12345678,v['callback']);cpu.mem_write(TABLE,table);initial=[(0x55990000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    initial[:2]=[v['size'],0xdeadbeef] if a==0x20a927c else [v['pointer'],v['size']]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    native=image[a-0x2000000:a-0x2000000+row['bytes']];expected=bytes.fromhex('8847' if a==0x20a927c else '9047')
    if native[6:8]!=expected:raise ValueError('Original callback BLX-register instruction differs')
    pcs=[];capture=None
    def code(machine,at,size,user):
        nonlocal capture
        if at==a+6:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32 or bytes(machine.mem_read(at,2))!=expected:raise ValueError('Scoped original callback instruction/mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];capture=dict(stoppedAtOriginalInstruction=hex(at),instruction=expected.hex(),mode='thumb',registers=regs[:4],callerSp=hex(regs[13]),callerLr=hex(regs[14]));machine.emu_stop();return
        if not a<=at<a+6 or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Callback staging escaped original caller prefix')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not SP-0x4000<=at or at+size>SP:raise ValueError('Callback staging wrote outside local stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100)
    if capture is None:raise ValueError('Original callback instruction not reached')
    regs=capture['registers'];correct=regs[0]==initial[0] and regs[1 if a==0x20a927c else 2]==v['callback'] and bytes(cpu.mem_read(TABLE,20))==table
    if a==0x20a928c:correct=correct and regs[1]==initial[1]
    return dict(address=row['address'],vector=v,seed=seed,scope='entry-before-original-BLX-register-instruction',callerReturned=False,callbackInstructionsExecuted=0,actualOriginalHelperInvocations=0,initialCallerExcludedFromHelperMetric=True,callbackTargetIdentityOrModeProven=False,modelPassed=bool(correct),capture=capture,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();stops=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();vectors=[dict(size=s,pointer=p,callback=c) for s in [0,1,0x7fffffff,0xffffffff] for p in [0,0x2178000] for c in [0x217a000,0x217a001]]
        for seed,v in enumerate(vectors):
            original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent callback-slot/argument staging differs',original,source))
            stops.append(original)
        old,new=('native_data_021d2374.malloc(size)','((MallocCB)native_data_021d2374.uninterpreted[1])(size)') if a==0x20a927c else ('native_data_021d2374.realloc(ptr,size)','((ReallocCB)native_data_021d2374.uninterpreted[0])(ptr,size)');folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole callback wrapper C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=16:raise ValueError('Wrong whole callback wrapper extent changed')
        failures=[]
        for seed in range(16):
            result=run(image,row,body,vectors[-1],seed)
            if result['modelPassed']:raise ValueError('Wrong whole callback slot accepted')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],boundaryModelRejections=len(failures),records=failures))
    limits=['Both ordinary C callback wrappers genuinely link over every16-byte original extent and unchanged original BSS literal relocation. Existing canonical2374 minimum20-byte field view has opaque leading8 bytes and typed callback slots8/16; complete external object storage extent/authorship is uncredited.','Actual original/source entry instructions stop BEFORE each original Thumb BLX-register instruction. Independent models check exact loaded slot word and incoming size/pointer registers for both pointer tags; callback destination identity/mode is deliberately unqualified and no callback instruction, helper body, allocation/reallocation outcome or caller return executes.','Two genuine same-extent whole wrong C units select different stored words and violate separate partial staging models. Dynamic callback/game/device/scenes and full native application execution remain unexecuted/uncredited; callback ABI types are comparative and qualified only to the measured wrapper interface.']
    trace=hashlib.sha256(json.dumps(stops,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=[],boundaryRecords=stops,nativeAndCompiledReturningCalls=0,actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=0,wrongC=[],boundaryWholeCNegativeControlsRejected=len(negative),boundaryWrongC=negative,actualNativeAndSourceEntryToCallbackInstructionStops=2*len(stops),boundaryCallerReturns=0,boundaryHelperInstructions=0,actualCallbackInstructionsExecuted=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
