import json
from collections import Counter
import arm7_lane_heap_lists_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Heap list C must genuinely match its complete own code/pool range')
    records,visited,actual=[],set(),0
    nested,prerequisites=Counter(),Counter()
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(address,original,case,seed)
        source=fixture.execute(address,rebuilt,case,seed)
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Heap list original/source actual-return/state/memory/access records differ')
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
            for row in result['prerequisites']:
                if not row['actualReturn']:
                    raise ValueError('Original-byte connected heap prerequisite did not actually return')
                prerequisites[row['entry']]+=1
        visited.update(native['visited'])
        actual+=4
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            fullStateSha256=fixture.engine.digest(json.dumps(native,sort_keys=True).encode()),
            independentCompleteHeapListsCoalescingAllocationAndWriteFootprintModel=True))
    own=set(range(address,address+fixture.engine.CODES[address],4))
    if own-visited:
        raise ValueError('Heap list complete own instruction coverage is missing: '+str(sorted(own-visited)))
    cap=fixture.execute(address,original,fixture.cases(address)[0],19,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Heap list instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),separatelyScopedOriginalPrerequisiteReturns=dict(sorted(prerequisites.items())),
        allOwnInstructionAddressesVisited=sorted(own),fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=100000,timeoutMicroseconds=500000,providerReplacements=[],
        originalBiosExecutionCredit=0,hardwareExecutionCredit=0,meaningfulReturnContract='Updated free-list head / allocated payload pointer or0 / void release',
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Direct insert tests empty/before/middle/after lists and both adjacent coalescing directions; reentry inserts a distinct valid node',
            'Original init/create/allocation/release producers establish ordinary bounded plain,fragmented,full and neighbor-release states',
            'Allocation matrices cover first/nonfirst free nodes, null-info/no-fit/empty lists, minimum rounding, exact64-byte leftover and below-threshold removal',
            'Positive fragmented contexts include splits whose next and previous nodes are both nonnull; no providers or BIOS substitutions occur',
            'Release reentry obtains a new actual allocation instead of applying an unsupported double free',
            'Independent models check complete memory and exact store values/widths/counts; original/source ordered accesses are compared separately',
            'Malformed pointers, excessive/cyclic lists, wrapped nonnull allocation sizes, concurrent actors and enclosing producer/scene/import-legality claims remain unsupported',
            'Original-byte prerequisite/helper returns and BSS pointer words receive zero extra function/data/source credit'])
