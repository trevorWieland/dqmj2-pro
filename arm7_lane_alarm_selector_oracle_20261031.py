from collections import Counter
import arm7_lane_alarm_selector_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if original!=rebuilt or address!=fixture.ADDRESS:
        raise ValueError('Complete selector source-only root/output differs')
    records,visited,nested=[],set(),Counter()
    returns=prerequisites=0
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or len(native['states'])!=case['passes'] or any(not state['actualReturn'] or state['fault'] is not None for state in native['states']):
            raise ValueError('Selector original/source whole state/actual return differs')
        visited.update(native['visited'])
        here=2*len(native['states'])
        returns+=here
        prerequisites+=2*len(native['prerequisites'])
        for state in native['states']:
            nested.update({a:n*2 for a,n in state['actualFunctionReturns'].items() if int(a,0)!=address})
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,stateSha256=fixture.qualified.digest(repr(native).encode())))
    own=set(range(address,address+fixture.CODE,4))
    if not own.issubset(visited):
        raise ValueError('Selector own instruction coverage incomplete')
    cap=fixture.execute(original,fixture.cases()[0],0,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Selector exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=returns,
        providerFreeOriginalAndCompiledReturns=returns,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualOriginalPrerequisiteReturns=prerequisites,actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),
        allOwnInstructionAddressesVisited=sorted(own),fullRegistersFlagsStackAndMemoryCompared=True,
        meaningfulReturnContract='raw128 for mode1, raw0 for mode2, alarm address for other u16 modes; no assigned application meaning',
        independentModel='mode-specific context words, pending-alarm branch, registered5-word contract and IRQ preservation',
        freshMachinePerScenario=True,persistentCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=100000,timeoutMicroseconds=200000,providerReplacements=[],originalBiosExecutionCredit=0,
        hardwareExecutionCredit=0,records=records,unsupportedControls=[dict(kind='instruction-cap',actualReturn=False,returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,limitations=['Original subsystem/object and conditional pending registration execute first; all lower helpers remain original',
            'Known helper contracts use u32 results and signed16 count/delay; raw return words are measured independently',
            'Callbacks are unexecuted zero-credit original address bindings; complete callback ABI/source remains unproved',
            'Disposable VCOUNT/IRQ/MMIO contexts include synthetic65535; physical display/timing and natural scene/thread reachability remain unproved'])
