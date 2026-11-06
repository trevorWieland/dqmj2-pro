import gzip
import json
import prove_arm7_lane_scheduler_callback_model_v3_20261031 as fixture
from build_arm7_lane_scheduler_callback_probe_v3_20261031 import build as build_probe
from project import ROOT,sha256

ADDRESS,SIZE=0x037FBE90,212


def oracle(original,rebuilt,address):
    if address!=ADDRESS or len(original)!=SIZE or original!=rebuilt:
        raise ValueError('Complete ordinary scheduler C must genuinely link every original byte')
    callback_probe=build_probe()
    records=[]
    scenarios=[(scenario,0) for scenario in ('roundtrip','disabled','disabled-max','irq-depth','irq-depth-max','irq-mode','same-current','no-ready')]
    scenarios.extend(('roundtrip',mask) for mask in (1,2,3))
    for scenario,mask in scenarios:
        for seed in range(8):
            native=fixture.execute(original,seed,scenario,callback_mask=mask,callback_probe=callback_probe)
            source=fixture.execute(rebuilt,seed,scenario,callback_mask=mask,callback_probe=callback_probe)
            if not native['actualOuterReturn'] or native!=source:
                raise ValueError('Scheduler supported original/source returns/registers/ordered accesses/full memory/context models differ')
            records.append(dict(native,actualOriginalAndCompiledOuterReturns=2))
    own=set(range(ADDRESS,ADDRESS+204,4))
    visited={pc for row in records for pc in row['visited']}
    if own!=visited:
        raise ValueError('Supported scheduler cases do not reach every own instruction')
    cap=fixture.execute(original,29,'roundtrip',budget=1)
    terminated=fixture.execute(original,29,'terminated-current',budget=1000)
    terminated_source=fixture.execute(rebuilt,29,'terminated-current',budget=1000)
    if cap['actualOuterReturn'] or terminated['actualOuterReturn'] or terminated!=terminated_source:
        raise ValueError('Scheduler unsupported boundary classification differs or gained return credit')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    compressed=gzip.compress(raw,compresslevel=9,mtime=0)
    product=ROOT/'work/arm7-bulk-20261030/lane-scheduler212-final/supported-records.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(compressed)
    normal=2*sum(row['ordinarySaveReturns'] for row in records)
    resumed=2*sum(row['resumedSaveContinuations'] for row in records)
    provider_free=2*sum(not row['callbackMask'] for row in records)
    callback_assisted=2*sum(bool(row['callbackMask']) for row in records)
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),
        providerFreeOriginalAndCompiledReturns=provider_free,syntheticCallbackContractOriginalAndCompiledReturns=callback_assisted,
        syntheticBiosContractOriginalAndCompiledReturns=0,actualSeparatelyObservedNestedReturns={'0x37fc64c':normal},
        resumedSaveContextContinuations=resumed,actualNonlocalContextTransfers=2*sum(row['realContextTransfers'] for row in records),
        actualSyntheticCallbackReturns=2*sum(row['actualSyntheticCallbackReturns'] for row in records),
        ordinaryLoadContextReturns=0,completedSecondaryThreadReturns=0,suspendedSecondarySleepAndSchedulerContexts=2*sum(row['scenario']=='roundtrip' for row in records),
        separatelyScopedOriginalPrerequisiteReturns=2*sum(len(row['originalPrerequisites']) for row in records),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,
        independentSavedAndLoadedContextAbiModel=True,independentMemoryExceptDeclaredExecutionStacks=True,independentExecutionStackByteModel=False,
        allOwnInstructionAddressesVisited=sorted(own),freshMachinePerScenario=True,persistentEntryCallsPerScenario=1,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=20000,timeoutMicroseconds=500000,
        providerReplacements=[dict(kind='source-compiled-two-pointer-callback-contract',originalCalleeCredit=0,sourceCredit=0)],
        syntheticCallbackProof=callback_probe[1],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        meaningfulReturnContract='Void outer caller actually returns through a real saved continuation; context transfers and suspended secondary calls are distinct',
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=len(compressed),
            rawSha256=fixture.linker.digest(raw),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0),dict(kind='terminated-current',execution=terminated,returnCredit=0)],
        unsupportedReturnCredit=0,functionMatchedBytes=212,moduleAdopted=False,
        limitations=['Independent models check every saved context word, all restored registers/CPSR/SVC-SP, callback argument order/effects and all mapped memory outside declared execution stacks',
            'Execution-stack bytes and every ordered data read/write are compared original/source; stack bytes are not independently prescribed',
            'Real native init/create/disable/wakeup/enable and SaveContext/LoadContext run; restored continuations, ordinary save returns, nonlocal loads and suspended secondary frames have separate counts',
            'Provider-free and separately compiled synthetic callback-contract outer returns are distinct; probe instructions/log words have0 original-callee/data/source credit',
            'All own instruction addresses are reached, without claiming exhaustive input/real-game or concurrency validation',
            'Terminated-current fault/budget boundary and prologue cap have0 own-return credit and no post-boundary state evidence',
            'Real game callback semantics, broader scheduler/error domains, physical interrupts/hardware, malformed pointers and arbitrary list cycles remain unsupported',
            'Full212-byte source matching and supported-domain execution are evidence independent from shared module/ROM adoption'])
