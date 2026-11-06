import gzip
import hashlib
import json
import arm7_lane_sound_init_native_20261031 as fixture
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address!=fixture.ADDRESS or len(original)!=fixture.SIZE or original!=rebuilt:
        raise ValueError('Complete ordinary sound initialization must genuinely link every original byte')
    records=[]
    nested={}
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Original/source initializer returns, thread ABI or complete memory effects differ')
        records.append(native)
        for state in native['states']:
            for entry,count in state['actualNativeHelperReturns'].items():
                nested[entry]=nested.get(entry,0)+count*2
    own=set(range(address,address+fixture.CODE,4))
    if {pc for row in records for pc in row['visited']}!=own:
        raise ValueError('Initializer corpus did not visit every own instruction')
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],11),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Bounded initialization exhaustion gained return credit')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/'work/arm7-bulk-20261030/lane-sound-init108-final/supported-records.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=4*len(records),
        providerFreeOriginalAndCompiledReturns=4*len(records),syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=nested,separatelyScopedOriginalPrerequisiteReturns=4*len(records),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=False,
        independentCompleteMappedMemoryModel=True,independentSixPhysicalWordThreadCreationModel=True,
        independentExactStoreFootprintModel=False,allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=20000,timeoutMicroseconds=500000,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        providerReplacements=[],meaningfulReturnContract='Void initializer; incidental R0 is compared original/source without assigning an integer result',
        supportedContext='Actual kernel initialization and one actual scheduler-disable call precede the sound initializer; new sound thread is created/marked READY but never executed',
        originalSoundThreadExecutions=0,nonlocalContextTransfers=0,physicalAudioExecutionCredit=0,auxiliaryHelperDefinitionCredit=0,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,functionMatchedBytes=108,moduleAdopted=False,
        limitations=['Complete mapped memory is independently modeled using measured kernel creation/list/context models and the actual command-queue/PXI registration ABI; ordered accesses and stack bytes are original/source compared',
            'Real command initialization, queue initialization, PXI callback registration, IRQ helpers, thread create/clear/list insertion/wakeup and disabled rescheduler execute without providers',
            'The sound thread and both SaveContext/LoadContext entries are forbidden by the fixture; no sound loop, timer, BIOS, audio or enclosing game scene is executed',
            'Five explicit initial flag words and ten full-word priorities exercise first initialization and nonzero-flag no-op reentry; flags/priority contexts are synthetic and not asserted legitimate game states',
            'The static helper is inlined source logic with no extra native function credit; original helper bodies, BSS/stack data and whole-ROM scaffolding have zero new credit',
            'Scheduler-enabled/concurrent initialization, executing the newly created sound thread, malformed kernel/stack context and physical IPC behavior remain unqualified'])
