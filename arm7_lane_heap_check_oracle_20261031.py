import json
from collections import Counter
import arm7_lane_heap_check_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address!=fixture.ADDRESS or original!=rebuilt:
        raise ValueError('Heap-check C must genuinely match its complete own code/pool range')
    records,visited,actual=[],set(),0
    nested,prerequisites=Counter(),Counter()
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Heap-check original/source actual-return/state/memory/access records differ')
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
            for row in result['prerequisites']:
                if not row['actualReturn']:
                    raise ValueError('Original-byte heap-check prerequisite did not actually return')
                prerequisites[row['entry']]+=1
        visited.update(native['visited'])
        actual+=4
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            resultWords=[row['execution']['registers'][0] for row in native['states']],
            explicitSyntheticFieldStores=native['explicitSyntheticFieldStores'],
            fullStateSha256=fixture.engine.digest(json.dumps(native,sort_keys=True).encode()),
            independentGlobalArenaListsAlignmentTotalFreeBytesAndReadOnlyMemoryModel=True))
    own=set(range(address,address+fixture.engine.CODES[address],4))
    if own-visited:
        raise ValueError('Heap-check complete own instruction coverage is missing: '+str(sorted(own-visited)))
    cap=fixture.execute(original,fixture.cases()[0],19,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Heap-check instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),separatelyScopedOriginalPrerequisiteReturns=dict(sorted(prerequisites.items())),
        allOwnInstructionAddressesVisited=sorted(own),fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=100000,timeoutMicroseconds=500000,providerReplacements=[],
        originalBiosExecutionCredit=0,hardwareExecutionCredit=0,meaningfulReturnContract='Signed free-payload byte total or-1; all nonstack memory is preserved',
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        excludedPredicateOutcomes=['A total<=0 failure after positive cells requires unsupported signed accumulation overflow in the bounded nonoverflow source domain'],
        limitations=['Real original heap producers return before explicitly recorded malformed-field substitutions; no providers or BIOS substitutions occur',
            'Global arena lower-inclusive/upper-exclusive bounds are distinct from a created heap span; valid explicit global-lower/other-span cells are accepted',
            'Plain/mixed/fragmented/full and zero-size-allocation producer contexts establish return totals and actual minimum-cell rejection',
            'Mapped metadata pointer/range/32-byte-alignment/list-link/size/strict-free-spacing/total failures are independently modeled',
            'No ownership, import-legality, enclosing scene/producer reachability or physical concurrency claim follows from the checker result',
            'Signed accumulation overflow, excessive/cyclic traversal and unmapped pointers remain unsupported and receive no return or source evidence',
            'Original-byte prerequisite/helper returns and BSS references receive no extra source/data credit'])
