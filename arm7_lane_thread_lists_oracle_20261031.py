import json
import arm7_lane_thread_lists_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Thread-list C must genuinely match its complete own code/pool extent')
    records,visited,actual=[],set(),0
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Thread-list complete original/source actual-return/state/access records differ')
        visited.update(native['visited'])
        actual+=4
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),independentCompletePriorityLinksAndMemoryModel=True))
    own=set(range(address,address+fixture.CODES[address],4))
    if own-visited:
        raise ValueError('Thread-list complete own instruction coverage is missing: '+str(sorted(own-visited)))
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],19),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Thread-list instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns={},allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=10000,timeoutMicroseconds=100000,providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        meaningfulReturnContract='Specified queue removal returns matching pointer or0; other routines are void with incidental R0 compared only as state',
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Synthetic bounded sorted thread lists establish empty/single/multiple/equal/extreme-u32 priority insertion and first/middle/last/missing removal',
            'Queue insertion uses <= priority and preserves duplicate membership; global insertion uses < and a distinct node on reentry',
            'Removal preserves fields that the actual routine does not clear; global removal does not establish a membership-validation or ownership policy',
            'Independent models check complete memory and exact store targets/widths/values/multiplicity; original/source ordered accesses and full registers/flags match',
            'No helper/provider/BIOS execution, scheduler switch, asynchronous behavior or enclosing caller/scene reachability is claimed',
            'Cyclic/excessive lists, invalid pointers, concurrent actors and arbitrary unsorted insertion contexts remain unsupported',
            'BSS context fields, original data, callee, module, ROM, blob and assembly source credit remain zero'])
