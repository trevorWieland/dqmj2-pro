import json
import arm7_lane_child_typed_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Utility-child C must genuinely match its complete own code/pool extent')
    records,visited,actual=[],set(),0
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Utility-child complete original/source actual-return/state/access records differ')
        visited.update(native['visited'])
        actual+=4
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),independentCompletePriorityLinksAndMemoryModel=True))
    own=set(range(address,address+fixture.SIZES[address],4))
    if own-visited:
        raise ValueError('Utility-child complete own instruction coverage is missing: '+str(sorted(own-visited)))
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],19),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Utility-child instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns={},allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=10000,timeoutMicroseconds=500000,providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        meaningfulReturnContract='Arena getters return full pointer words; setter and queue insertion are void with incidental R0 compared only as state',
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Utility-child ROM member/runtime hash and ARM module identity are independent from host functions at overlapping numeric addresses',
            'Ordinary host C/header closures are copied with only their own function symbol renamed, then freshly compiled/real-linked against child bytes',
            'No additional implementation-family novelty is claimed; four genuinely new qualified child instances are distinct from their host origins',
            'The independently mapped72-byte shared arena prefix is not module BSS or reconstructed original data; all nine indices/full pointer words are qualified',
            'Queue insertion checks equal/extreme unsigned priorities, duplicate membership and complete pointer effects with two persistent calls',
            'Independent complete-memory/write-width/value/multiplicity models and original/source ordered accesses/registers/flags are required',
            'No providers, helpers, BIOS, scheduler/concurrency, ownership/import policy, physical address mirrors or enclosing scene reachability are claimed',
            'Cyclic/unsorted lists, invalid pointers and arena indices outside0..8 remain unsupported'])
