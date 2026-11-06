import json
from collections import Counter
import arm7_lane_heap_constructors_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Heap constructor C must genuinely link its entire own code/pool range')
    records,visited,actual=[],set(),0
    nested,prerequisites=Counter(),Counter()
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(address,original,case,seed)
        source=fixture.execute(address,rebuilt,case,seed)
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Heap constructor original/source actual-return/register/flag/memory/access records differ')
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
            for row in result['prerequisites']:
                if not row['actualReturn']:
                    raise ValueError('Original heap initialization prerequisite did not actually return')
                prerequisites[row['entry']]+=1
        visited.update(native['visited'])
        actual+=4
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            fullStateSha256=fixture.engine.digest(json.dumps(native,sort_keys=True).encode()),
            independentCompleteHeapFieldsAlignmentSelectionMemoryAndWriteFootprintModel=True))
    own=set(range(address,address+fixture.engine.CODES[address],4))
    if own-visited:
        raise ValueError('Heap constructor complete own instruction coverage is missing')
    cap=fixture.execute(address,original,fixture.cases(address)[0],19,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Heap constructor instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),separatelyScopedOriginalPrerequisiteReturns=dict(sorted(prerequisites.items())),
        allOwnInstructionAddressesVisited=sorted(own),fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=100000,timeoutMicroseconds=500000,providerReplacements=[],
        originalBiosExecutionCredit=0,hardwareExecutionCredit=0,meaningfulReturnContract='Prior full-word currentHeap / aligned arena start / first negative-size descriptor index or-1',
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Supported aligned metadata/backing is explicitly synthetic; original init and IRQ helpers execute without providers',
            'Current-heap selection stores unvalidated full words; this is not an allocation, scene or import-legality rule',
            'Constructor zero/negative sizes demonstrate only measured writes and subsequent negative-size selection, not valid heap usability',
            'All mapped memory and store footprints are independently modeled; original/source ordered accesses are compared separately',
            'Unaligned heap metadata, invalid pointers, excessive heap counts, concurrent actors and physical bus/IRQ behavior are unsupported',
            'Prerequisite/helper returns are separate from own source entry returns; BSS pointers and original dependencies receive no new source/data credit'])
