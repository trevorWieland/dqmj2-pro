import gzip
import json
import prove_arm7_lane_thread_exit_flow_20261031 as fixture
from build_arm7_lane_thread_exit_callback_20261031 import build
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or len(original)!=fixture.SIZES[address] or original!=rebuilt:
        raise ValueError('Full ordinary exit C must genuinely link every original byte')
    probe=build()
    records=[]
    for stack in (False,True):
        for callback in (None,probe):
            for seed in range(16):
                native=fixture.execute(address,original,seed,stack,callback_probe=callback)
                source=fixture.execute(address,rebuilt,seed,stack,callback_probe=callback)
                if not native['actualResumedOuterSleepReturn'] or native!=source:
                    raise ValueError('Nonreturning exit original/source context/effects/resumed SleepThread caller differ')
                records.append(native)
    cap=fixture.execute(address,original,17,False,budget=1)
    if cap['actualResumedOuterSleepReturn'] or cap.get('postBoundaryStateExcluded') is not True:
        raise ValueError('Exit prologue exhaustion gained completion evidence')
    reachable={pc for row in records for pc in row['visited']}
    own=set(range(address,address+fixture.CODES[address],4))
    exclusions={0x037FC1C4,0x037FC1D0,0x037FC1D4} if address==0x037FC180 else {0x037FC214,0x037FC218}
    if reachable!=own-exclusions:
        raise ValueError('Exit reachable instruction/excluded original nonreturn continuation coverage differs')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/f'work/arm7-bulk-20261030/lane-thread-exit160-final/supported-{address:08x}.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    import hashlib
    return dict(supported=True,verifiedReturn=False,verifiedNonreturningExitTransition=True,vectors=len(records),
        actualOriginalAndCompiledReturns=0,actualOwnedNormalReturns=0,actualOriginalAndCompiledOwnedEntries=2*len(records),
        actualResumedOuterSleepReturns=2*len(records),providerFreeResumedOuterSleepReturns=len(records),
        syntheticCallbackContractResumedOuterSleepReturns=len(records),providerFreeOriginalAndCompiledReturns=0,
        syntheticBiosContractOriginalAndCompiledReturns=0,actualSeparatelyObservedNestedReturns={'0x37fc64c':2*len(records)},
        resumedSavedContinuations=2*len(records),actualNonlocalContextTransfers=2*sum(row['actualNonlocalContextTransfers'] for row in records),
        actualSyntheticCallbackReturns=2*sum(row['actualSyntheticCallbackReturns'] for row in records),
        actualRetiredSecondaryThreadExitPaths=2*len(records),ordinaryLoadContextReturns=0,originalTerminationFallbackCredit=0,
        completedSecondaryThreadNormalReturnCredit=0,separatelyScopedOriginalPrerequisiteReturns=10*len(records),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=False,
        independentContextAbiAndAllMemoryOutsideDeclaredExecutionStacks=True,independentExecutionStackByteModel=False,
        allReachableOwnInstructionAddressesVisited=sorted(reachable),excludedOriginalNonreturnContinuations=sorted(exclusions),
        exclusionsJustification='Original LoadContext transfers nonlocally and original destruction returns to a saved sleeping caller; no forced PCs or artificial return hooks',
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=1,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=20000,timeoutMicroseconds=500000,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        providerReplacements=[dict(kind='source-compiled-one-pointer-destructor-contract',physicalArgumentWords=1,originalCalleeCredit=0,sourceCredit=0)],
        syntheticCallbackProof=probe[1],supportedArgumentDomain={'originalOuterProducer':'ARM037FC15C OS_ExitThread(void)','arg':0},
        meaningfulReturnContract='Owned APIs do not normally return; a real created thread exits/destructs and original SleepThread returns through a genuinely restored parent continuation',
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='outer-SleepThread-prologue-cap',execution=cap,returnCredit=0,exitCredit=0)],
        unsupportedReturnCredit=0,functionMatchedBytes=len(original),moduleAdopted=False,
        limitations=['Owned normal returns, actual resumed original SleepThread returns, ordinary SaveContext returns, resumed continuations, nonlocal loads and retired secondary exit paths have distinct counters',
            'Real init/create/wakeup, join-queue SleepThread, thread/mutex list operations and scheduler destruction execute; no enclosing scene/physical concurrency or OS_Terminate success claim',
            'All saved/loaded register words, CPSR/SVC-SP and mapped memory outside declared execution stacks are independently modeled; all stack bytes and ordered accesses are compared original/source only',
            'Destructor callbacks are separately compiled synthetic one-argument C contracts; their code/log data get zero source/original-callee credit',
            'Both NULL and explicitly synthetic allocated destructor-stack contexts are supported; original OS_ExitThread producer supplies argument0 only',
            'Nonzero opaque arguments, real game destructors, malformed stacks/pointers, IRQ/concurrent mutation and arbitrary queue/list cycles remain unqualified',
            'Compiler-emitted post-LoadContext/destruction continuations are included in exact source bytes but not forcibly executed or counted as normal returns'])
