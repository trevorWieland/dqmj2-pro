import gzip
import sys
import json
from pathlib import Path
import match_runtime
import unicorn
import elftools
import match_arm7_lane_thread_init_20261031 as frozen_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
from arm7_lane_scheduler_probe_engine_v3_20261031 import setup,BASE,DATA,RETURN
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UcError
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

ADDRESS,SIZE=0x037FBE90,212
WORK=ROOT/'work/arm7-bulk-20261030/lane-scheduler-callback-model-v3'


def build():
    old=json.loads((ROOT/'nonmatching/arm7-bulk/20261031/lane-os-near212-v3/source-profile.json').read_text())['profile']
    for item in [dict(path=old['source'],sha256=old['sourceSha256']),*old['sourceDependencies'],dict(path=old['compiler'],sha256=old['compilerSha256'])]:
        candidate=(ROOT/item['path']).resolve()
        if not candidate.is_relative_to(ROOT) or sha256(candidate)!=item['sha256']:
            raise ValueError('Source-only scheduler draft input differs or escaped repository')
    directory=WORK/'fresh-source'
    directory.mkdir(parents=True,exist_ok=True)
    attempt,compiled=crossreuse_utility_c.compile_origin(old,ROOT/old['compiler'],old['compilerFlags'],directory)
    if compiled is None:
        raise ValueError(attempt)
    derived,unused,body=compiled
    with (ROOT/derived['probeObject']).open('rb') as stream:
        elf=ELFFile(stream)
        symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name==old['name'])
        section,offset=symbol['st_shndx'],symbol['st_value']
    entry=dict(old,object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
        relocations=[dict(row,format='SHT_RELA',explicitAddend=row['addend'],originalEncodedWord=body[row['offset']:row['offset']+4].hex()) for row in derived['relocations']])
    proof=linker.validate(entry,directory/'real-link')
    return entry,proof,(directory/'real-link/caller.bin').read_bytes()


def execute(body,seed,scenario,budget=20000,callback_mask=0,callback_probe=None):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    machine=setup(0x037FBF64,raw[0x3F64:0x3F64+240],seed,callback_probe if callback_mask else None)
    cpu=machine['cpu']
    cpu.mem_write(ADDRESS,body)
    cpu.mem_write(0x03807678,bytes(0x0380B4E4-0x03807678))
    calls=[(0x037FBF64,[]),(0x037FC558,[]),(0x037FC054,[DATA+0x1000,0x037FC290,0,DATA+0x6000,1024,0])]
    if scenario not in ('same-current','no-ready'):
        calls.append((0x037FC36C,[DATA+0x1000]))
    calls.append((0x037FC590,[]))
    prerequisites=[]
    for entry,args in calls:
        execution=machine['invoke'](entry,args,False)
        if not execution['actualReturn']:
            raise ValueError('Original roundtrip initialization/create/wakeup/scheduler prerequisite failed')
        prerequisites.append(dict(entry=hex(entry),arguments=args,actualReturn=True))
    if scenario in ('disabled','disabled-max'):
        cpu.mem_write(0x038076F4,(0xFFFFFFFF if scenario=='disabled-max' else 1).to_bytes(4,'little'))
    if scenario in ('irq-depth','irq-depth-max'):
        cpu.mem_write(0x03807716,(0xFFFF if scenario=='irq-depth-max' else 1).to_bytes(2,'little'))
    if scenario=='terminated-current':
        cpu.mem_write(0x038077C8+0x48,(2).to_bytes(4,'little'))
    if scenario=='no-ready':
        cpu.mem_write(0x038077C8+0x48,bytes(4))
    if callback_mask:
        if scenario!='roundtrip' or callback_probe is None:
            raise ValueError('Synthetic callback provider used outside its bounded scenario')
        cpu.mem_write(0x038076F0,(0x023C7000 if callback_mask&1 else 0).to_bytes(4,'little'))
        cpu.mem_write(0x03807720,(0x023C7000 if callback_mask&2 else 0).to_bytes(4,'little'))
        cpu.mem_write(0x023C7800,bytes(36))
    predicted={base:bytearray(cpu.mem_read(base,len(data))) for base,data in machine['regions'].items()}
    contexts=dict(serviceSp=0,pendingSave=None,pendingLoad=None,resumePc=None,normalSaveReturns=0,resumedSaveContinuations=0,loads=0,callbackEntries=0,callbackReturns=0,pendingCallback=None)
    def put_model(target,value,width=4):
        for base,data in predicted.items():
            if base<=target and target+width<=base+len(data):
                data[target-base:target-base+width]=(value&((1<<(8*width))-1)).to_bytes(width,'little')
                return
        raise ValueError('Independent scheduler context model write escaped bounded backing')
    def peek_model(target,width=4):
        for base,data in predicted.items():
            if base<=target and target+width<=base+len(data):
                return bytes(data[target-base:target-base+width])
        raise ValueError('Independent scheduler context model read escaped bounded backing')
    if scenario in ('irq-depth','irq-depth-max','irq-mode'):
        put_model(0x03807714,1,2)
    if scenario=='roundtrip':
        put_model(DATA+0x1048,0)
    events,visited,steps=[],set(),[0]
    def code(machine,pc,size,unused):
        steps[0]+=1
        if ADDRESS<=pc<ADDRESS+204:
            visited.add(pc)
        callback=contexts['pendingCallback']
        if callback and pc==callback['lr']:
            values=[machine.reg_read(register) for register in match_runtime.REGISTERS]
            if values[4:12]!=callback['saved'] or values[13]!=callback['sp'] or machine.reg_read(UC_ARM_REG_CPSR)&255!=callback['control']:
                raise ValueError('Compiled synthetic callback broke its two-pointer caller ABI')
            if bytes(machine.mem_read(0x023C7800,36))!=peek_model(0x023C7800,36):
                raise ValueError('Synthetic callback effects disagree with independent ordered pointer-log model')
            contexts['callbackReturns']+=1
            contexts['pendingCallback']=None
        if pc==0x023C7000:
            values=[machine.reg_read(register) for register in match_runtime.REGISTERS]
            index=contexts['callbackEntries']
            width=callback_mask.bit_count()
            expected=(0x038077C8,DATA+0x1000) if index<width else (DATA+0x1000,0x038077C8)
            if values[:2]!=list(expected) or index>=2*width or contexts['pendingCallback'] is not None:
                raise ValueError('Original caller did not supply the qualified two-pointer callback ordering')
            put_model(0x023C7800+4+8*index,expected[0])
            put_model(0x023C7800+8+8*index,expected[1])
            put_model(0x023C7800,index+1)
            contexts['callbackEntries']+=1
            contexts['pendingCallback']=dict(lr=values[14],saved=values[4:12],sp=values[13],control=machine.reg_read(UC_ARM_REG_CPSR)&255)
        load=contexts['pendingLoad']
        if load and pc==load['pc']:
            registers=[machine.reg_read(register) for register in match_runtime.REGISTERS]
            if registers!=load['registers'] or machine.reg_read(UC_ARM_REG_CPSR)!=load['cpsr']:
                raise ValueError('Actual context transfer disagrees with independent complete-register/CPSR restore model')
            contexts['serviceSp']=load['serviceSp']
            contexts['loads']+=1
            contexts['pendingLoad']=None
            if load['context']==0x038077C8:
                contexts['resumePc']=load['registers'][14]
        save=contexts['pendingSave']
        if save and pc==save['lr']:
            if bytes(machine.mem_read(save['context'],72))!=peek_model(save['context'],72) or machine.reg_read(match_runtime.REGISTERS[0])!=0:
                raise ValueError('Actual SaveContext memory/ordinary zero return differs from independent assembly ABI model')
            contexts['normalSaveReturns']+=1
            contexts['pendingSave']=None
        elif contexts['resumePc'] is not None and pc==contexts['resumePc']:
            if machine.reg_read(match_runtime.REGISTERS[0])!=1:
                raise ValueError('Resumed saved continuation did not return the saved1 discriminator')
            contexts['resumedSaveContinuations']+=1
            contexts['resumePc']=None
        if pc==0x037FC64C:
            values=[machine.reg_read(register) for register in match_runtime.REGISTERS]
            context=values[0]
            flags=machine.reg_read(UC_ARM_REG_CPSR)
            if context not in (0x038077C8,DATA+0x1000):
                raise ValueError('SaveContext escaped the two qualified thread records')
            saved=[flags,1,context+4,flags,*values[3:13],values[13],values[14],0x037FC680,contexts['serviceSp']]
            if len(saved)!=18:
                raise ValueError('Independent context record layout differs')
            for index,value in enumerate(saved):
                put_model(context+index*4,value)
            contexts['pendingSave']=dict(context=context,lr=values[14])
        if pc==0x037FC680:
            context=machine.reg_read(match_runtime.REGISTERS[0])
            expected=(DATA+0x1000,0x038077C8)[contexts['loads']] if contexts['loads']<2 else 0
            if context!=expected or bytes(machine.mem_read(context,72))!=peek_model(context,72):
                raise ValueError('Actual LoadContext target/current record differs from independently predicted state')
            values=[int.from_bytes(peek_model(context+index*4),'little') for index in range(18)]
            contexts['pendingLoad']=dict(context=context,pc=values[16]-4,registers=values[1:16],cpsr=values[0],serviceSp=values[17])
        if pc in (0x037FC64C,0x037FC680,0x037FC290,ADDRESS):
            events.append(dict(pc=hex(pc),r0=hex(machine.reg_read(match_runtime.REGISTERS[0])),
                sp=hex(machine.reg_read(match_runtime.REGISTERS[13])),lr=hex(machine.reg_read(match_runtime.REGISTERS[14])),
                current=hex(int.from_bytes(machine.mem_read(0x03807718,4),'little'))))
    cpu.hook_add(UC_HOOK_CODE,code)
    data_reads,data_writes=[],[]
    def memory_read(machine,access,target,size,value,unused):
        data_reads.append([target,size])
    def memory_write(machine,access,target,size,value,unused):
        data_writes.append([target,size,value&((1<<(8*size))-1)])
    cpu.hook_add(UC_HOOK_MEM_READ,memory_read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,memory_write)
    initial=[(seed*0x10305+0x12345678+index*0x1020304)&0xFFFFFFFF for index in range(15)]
    initial[13:]=[0x0380FB78,RETURN]
    mode=0x12 if scenario=='irq-mode' else 0x1F
    cpsr=mode|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
    cpu.reg_write(UC_ARM_REG_CPSR,0xD3)
    cpu.reg_write(match_runtime.REGISTERS[13],0)
    cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for register,value in zip(match_runtime.REGISTERS,initial):
        cpu.reg_write(register,value)
    fault=None
    try:
        cpu.emu_start(ADDRESS,RETURN,timeout=500000,count=budget)
    except (UcError,ValueError) as error:
        fault=str(error)
    actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
    result=dict(seed=seed,scenario=scenario,callbackMask=callback_mask,actualOuterReturn=actual,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),
        instructions=steps[0],events=events,visited=sorted(visited),originalPrerequisites=prerequisites)
    if not actual:
        return dict(result,postBoundaryStateExcluded=True,returnCredit=0)
    registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=cpsr&255:
        raise ValueError('Genuine original caller saved-register/SP/LR/control ABI did not survive')
    current=int.from_bytes(cpu.mem_read(0x03807718,4),'little')
    need=int.from_bytes(cpu.mem_read(0x03807714,2),'little')
    next_state=int.from_bytes(cpu.mem_read(DATA+0x1048,4),'little')
    if current!=0x038077C8 or need!=int(scenario in ('irq-depth','irq-depth-max','irq-mode')) or next_state!=int(scenario in ('disabled','disabled-max','irq-depth','irq-depth-max','irq-mode')):
        raise ValueError('Independent scheduler final current/deferred flag/sleep-state model differs')
    loads=[row for row in events if row['pc']=='0x37fc680']
    if scenario=='roundtrip':
        if [row['r0'] for row in loads]!=[hex(DATA+0x1000),'0x38077c8']:
            raise ValueError('Original two-way context loads were not independently observed')
    elif loads:
        raise ValueError('Early-return scheduler scenario unexpectedly switched context')
    count=2 if scenario=='roundtrip' else 0
    if contexts['normalSaveReturns']!=count or contexts['resumedSaveContinuations']!=count//2 or contexts['loads']!=count or any(contexts[key] is not None for key in ('pendingSave','pendingLoad','resumePc','pendingCallback')):
        raise ValueError('Ordinary save returns, resumed continuations and nonreturning load transfers were conflated')
    if contexts['callbackEntries']!=2*callback_mask.bit_count() or contexts['callbackReturns']!=contexts['callbackEntries']:
        raise ValueError('Synthetic callback contract entries/actual returns differ')
    execution_stacks=((0x0380F784,0x0380FB7C),(DATA+0x5C04,DATA+0x5FFC))
    for base,expected in predicted.items():
        actual=bytearray(cpu.mem_read(base,len(expected)))
        for first,last in execution_stacks:
            first,last=max(first,base),min(last,base+len(expected))
            if first<last:
                actual[first-base:last-base]=expected[first-base:last-base]
        if actual!=expected:
            differences=[hex(base+index) for index,(a,b) in enumerate(zip(actual,expected)) if a!=b]
            raise ValueError('Independent complete scheduler memory model outside declared execution stacks differs: '+repr(differences[:20]))
    return dict(result,orderedDataReads=data_reads,orderedDataWrites=data_writes,actualSyntheticCallbackReturns=contexts['callbackReturns'],independentSavedAndLoadedContextAbiModel=True,independentAllMemoryOutsideDeclaredExecutionStacks=True,
        declaredExecutionStackRanges=[[hex(first),hex(last)] for first,last in execution_stacks],
        ordinarySaveReturns=contexts['normalSaveReturns'],resumedSaveContinuations=contexts['resumedSaveContinuations'],
        registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
        memorySha256={hex(base):linker.digest(bytes(cpu.mem_read(base,len(data)))) for base,data in machine['regions'].items()},
        current=hex(current),deferredFlag=need,nextState=next_state,realContextTransfers=len(loads),
        suspendedSecondarySleepAndSchedulerFrames=int(scenario=='roundtrip'),originalLoadContextReturnCredit=0,
        actualOriginalCallerReturns=1,callerStackCanary=int.from_bytes(cpu.mem_read(0x0380FB7C,4),'little'))


def main():
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4' or elftools.__version__!='0.33':
        raise ValueError('Pinned scheduler draft runtime differs')
    if sha256(frozen_runtime.PIN_FILE)!=frozen_runtime.PIN_SHA:
        raise ValueError('Frozen scheduler draft runtime input list differs')
    runtime=json.loads(frozen_runtime.PIN_FILE.read_text())['files']
    for item in runtime:
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Scheduler draft runtime dependency differs')
    entry,proof,rebuilt=build()
    raw=(ROOT/entry['binary']).read_bytes()
    original=raw[ADDRESS-entry['base']:ADDRESS-entry['base']+SIZE]
    from build_arm7_lane_scheduler_callback_probe_v3_20261031 import build as build_probe
    callback_probe=build_probe()
    records=[]
    scenarios=[(scenario,0) for scenario in ('roundtrip','disabled','disabled-max','irq-depth','irq-depth-max','irq-mode','same-current','no-ready')]
    scenarios.extend(('roundtrip',mask) for mask in (1,2,3))
    for scenario,mask in scenarios:
        for seed in range(8):
            native=execute(original,seed,scenario,callback_mask=mask,callback_probe=callback_probe)
            source=execute(rebuilt,seed,scenario,callback_mask=mask,callback_probe=callback_probe)
            if not native['actualOuterReturn'] or native!=source:
                raise ValueError('Original/recompiled scheduler complete return/register/memory/context records differ')
            records.append(dict(native,actualOriginalAndCompiledOuterReturns=2))
    cap=execute(original,29,'roundtrip',budget=1)
    if cap['actualOuterReturn']:
        raise ValueError('Scheduler prologue cap received an actual-return credit')
    terminated=execute(original,29,'terminated-current',budget=1000)
    terminated_rebuilt=execute(rebuilt,29,'terminated-current',budget=1000)
    if terminated['actualOuterReturn'] or terminated!=terminated_rebuilt:
        raise ValueError('Unsupported terminated-current execution classification diverged or returned')
    data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    compressed=gzip.compress(data,compresslevel=9,mtime=0)
    product=WORK/'roundtrip-records.json.gz'
    product.write_bytes(compressed)
    report=ROOT/'evidence/attempts/arm7-lane-scheduler-callback-model-v3-20261031.json'
    write_json(report,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),entry=entry,realLink=proof,
        sourceCredit=0,wholeModuleCredit=0,providerReplacements=[dict(kind='compiled-synthetic-two-pointer-callback',originalCalleeCredit=0,sourceCredit=0)],
        syntheticCallbackProof=callback_probe[1],providerFreeOriginalAndCompiledOuterReturns=2*sum(not row['callbackMask'] for row in records),
        syntheticCallbackContractOriginalAndCompiledOuterReturns=2*sum(bool(row['callbackMask']) for row in records),
        actualSyntheticCallbackReturns=2*sum(row['actualSyntheticCallbackReturns'] for row in records),
        runtimeVersions=dict(python='3.13.5',unicorn=unicorn.__version__,pyelftools=elftools.__version__),
        frozenRuntimeSources=runtime,sourceOnlyProfile=dict(path='nonmatching/arm7-bulk/20261031/lane-os-near212-v3/source-profile.json',sha256=sha256(ROOT/'nonmatching/arm7-bulk/20261031/lane-os-near212-v3/source-profile.json')),freshScenarios=len(records),
        actualOriginalAndCompiledOuterReturns=2*len(records),genuineOriginalAndCompiledContextTransfers=2*sum(row['realContextTransfers'] for row in records),
        loadContextOrdinaryReturnCredit=0,actualCompleteSecondaryThreadReturns=0,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=len(compressed),
            rawSha256=linker.digest(data),rawBytes=len(data),records=len(records),gzipMtime=0),
        instructionAddressesReached=sorted({pc for row in records for pc in row['visited']}),cap=cap,
        unsupportedTerminatedCurrent=terminated,unsupportedTerminatedCurrentReturnCredit=0,
        additionalCurrentRuntimeSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in (
            'arm7_lane_scheduler_probe_engine_v3_20261031.py','build_arm7_lane_scheduler_callback_probe_v3_20261031.py',
            'nonmatching/arm7-bulk/20261031/lane-scheduler-callback-probe-v3/native_scheduler_probe_callback.c')],
        limitations=['Source is freshly compiled/genuinely linked, but this is a zero-credit functional draft, without final source/profile/negative controls',
            'Original init/create/disable/wakeup/enable and SaveContext/LoadContext execute unchanged; synthetic callback-provider cases are separate from provider-free cases and suspended secondary frames remain distinct',
            'Final current pointer/deferred flag/sleep state, two actual load targets and saved caller ABI are independently checked; all original/source CPU/memory records match',
            'Every saved context field, loaded register/CPSR/SVC-SP and all memory outside declared execution stacks is independently modeled; execution-stack bytes are original/source compared only, with no ordinary LoadContext return or completed secondary-thread credit',
            'Nonnull system/user callback branches use an explicitly compiled synthetic C two-pointer contract with0 original-callee credit; real game callbacks remain unqualified',
            'Trace is deterministic gzip output rebuilt from current source and original inputs, not a cached prerequisite']))
    print(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),actualOuterReturns=2*len(records),contextTransfers=128,sourceCredit=0))


if __name__=='__main__':
    main()
