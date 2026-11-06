import arm7_lane_initializer_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if original!=rebuilt or address!=fixture.ADDRESS:
        raise ValueError('Complete initializer source-only extent/output differs')
    records,visited,returns=[],set(),0
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or len(native['states'])!=case['passes'] or any(not row['actualReturn'] or row['fault'] is not None for row in native['states']):
            raise ValueError('Initializer original/source full machine/return differs')
        visited.update(native['visited'])
        here=2*len(native['states'])
        returns+=here
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,stateSha256=fixture.digest(repr(native).encode())))
    own=set(range(address,address+fixture.CODE,4))
    if not own.issubset(visited):
        raise ValueError('Initializer own instruction coverage incomplete')
    cap=fixture.execute(original,fixture.cases()[0],0,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Initializer exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=returns,
        providerFreeOriginalAndCompiledReturns=returns,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns={},allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,meaningfulReturnContract='void; incidental R0 receives no result credit',
        independentModel='all16 IDs/flag preservation, masks and ordered writes; every other byte preserved',
        freshMachinePerScenario=True,persistentCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=3000,timeoutMicroseconds=100000,providerReplacements=[],originalBiosExecutionCredit=0,
        hardwareExecutionCredit=0,records=records,unsupportedControls=[dict(kind='instruction-cap',actualReturn=False,returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,limitations=['All256 prior flag bytes occur across16 synthetic records and32 contexts',
            'Only ID, flags and two masks change; no ordinary game scene, audio-device or caller lifecycle claims'])
