import arm7_lane_child_counter_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if original!=rebuilt or address!=fixture.ADDRESS:
        raise ValueError('Complete utility counter source-only body/root differs')
    records,visited,returns=[],set(),0
    nested={'0x37fe41c':0,'0x37fe430':0}
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or len(native['states'])!=case['passes'] or any(not state['actualReturn'] or state['fault'] is not None for state in native['states']):
            raise ValueError('Counter full original/source machine or actual return differs')
        visited.update(native['visited'])
        here=2*len(native['states'])
        returns+=here
        for state in native['states']:
            for key in nested:
                nested[key]+=state['actualFunctionReturns'][key]*2
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,stateSha256=fixture.digest(repr(native).encode())))
    own=set(range(address,address+fixture.CODE,4))
    if not own.issubset(visited):
        raise ValueError('Counter own instruction coverage incomplete')
    cap=fixture.execute(original,fixture.cases()[0],0,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Counter exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=returns,
        providerFreeOriginalAndCompiledReturns=returns,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=nested,allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,meaningfulReturnContract='current unsigned32 counter after conditional wrapping increment and original IRQ restoration',
        independentModel='signed32 comparison, u32 increment/wrap, ordered words, full-WRAM preservation, CMP NZCV and IRQ bit',
        freshMachinePerScenario=True,persistentCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=2000,timeoutMicroseconds=100000,providerReplacements=[],originalBiosExecutionCredit=0,
        hardwareExecutionCredit=0,records=records,unsupportedControls=[dict(kind='instruction-cap',actualReturn=False,returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,limitations=['Embedded utility program namespace; host addresses never substitute for child bytes or state',
            'Original CPSR helpers execute; no provider, BIOS, device or asynchronous interrupt execution',
            'Sample and counter remain raw native values with no physical time/frame or scene interpretation'])
