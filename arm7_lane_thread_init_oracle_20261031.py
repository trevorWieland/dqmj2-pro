import json
from collections import Counter
import arm7_lane_thread_init_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Thread-init ordinary C must genuinely link its complete unit')
    visited,records=set(),[]
    nested=Counter()
    predicates={}
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Original/source thread-init complete returns/full memory/access/register records differ')
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
        for pc,counts in native['observedConditionalPredicates'].items():
            dest=predicates.setdefault(pc,dict(executed=0,skipped=0))
            for key,value in counts.items():
                dest[key]+=value
        visited.update(native['visited'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            completeNativeAndCompiledStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),
            independentWholeMappedMemoryModel=True,independentWriteFootprintModel=False))
    own=set(range(address,address+fixture.CODES[address],4))
    if own-visited:
        raise ValueError('Thread-init complete owned instruction coverage is missing: '+repr(sorted(own-visited)))
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],91),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Thread-init prologue exhaustion received return credit')
    count=4*len(records)
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=count,
        providerFreeOriginalAndCompiledReturns=count,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,independentStoreFootprintModel=False,
        physicalArgumentWords=0,absoluteSdkIntegerSymbols={'SDK_SYS_STACKSIZE':1024,'SDK_IRQ_STACKSIZE':1024},
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=100000,timeoutMicroseconds=500000,
        meaningfulReturnContract='Initialization is void; current/list/launcher/stack/callback/shared-word effects are checked without executing a thread',
        providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],unsupportedReturnCredit=0,records=records,observedOriginalConditionalPredicates=predicates,
        fixedBuildExcludedPredicateOutcomes={'0x37fbfb8':'LE true impossible for actual positive SYS stack-length1024'},
        limitations=['Actual constant-valued SDK linker symbols are independently qualified integer roles for this exact caller, not memory locations',
            'Original callback setter and IRQ helpers execute without providers; old callback values are returned but never invoked',
            'Synthetic initialized0/1/2/FFFFFFFF fields cover active initialization versus idempotent return and all untouched counter/unknown words are preserved',
            'Launcher metadata, fixed canaries, shared thread-info pointer, flags and callback slot are independently modeled over complete mapped RAM',
            'The actual length1024 makes LE true unreachable; instruction addresses fetched and executed/skipped conditional outcomes are separate, with no modified constant or forced PC',
            'Full original/source ordered accesses/registers/flags agree, while redundant store multiplicity is not independently prescribed',
            'No launcher context execution, startup reachability, actual stack adequacy, physical mirrors/hardware/concurrency or arbitrary layout is qualified'])
