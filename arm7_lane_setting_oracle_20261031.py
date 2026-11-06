import arm7_lane_setting_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if original!=rebuilt or address!=fixture.ADDRESS:
        raise ValueError('Complete setting source-only output/entry differs')
    records,visited,returns=[],set(),0
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or len(native['states'])!=case['passes'] or any(not state['actualReturn'] or state['fault'] is not None for state in native['states']):
            raise ValueError('Setting original/source whole machine, read/store order or actual return differs')
        visited.update(native['visited'])
        here=len(native['states'])*2
        returns+=here
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,stateSha256=fixture.digest(repr(native).encode())))
    own=set(range(address,address+fixture.CODE,4))
    if visited!=own:
        raise ValueError('Setting own instruction coverage incomplete')
    cap=fixture.execute(original,fixture.cases()[0],0,budget=1)
    malformed=fixture.execute(original,dict(value=1,pointer=0,passes=1),991)
    if cap['states'][0]['actualReturn'] or malformed['states'][0]['actualReturn'] or malformed['states'][0]['fault'] is None:
        raise ValueError('Setting malformed-pointer/exhaustion context received false return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=returns,
        providerFreeOriginalAndCompiledReturns=returns,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns={},allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,meaningfulReturnContract='native0 for accepted byte values; native5 for larger full-word inputs; no named error semantics',
        independentModel='all256 byte values, full-word guard, absolute pointer read, ordered16-bit RAM/MMIO stores and untouched guards',
        freshMachinePerScenario=True,persistentCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=500,timeoutMicroseconds=100000,providerReplacements=[],originalBiosExecutionCredit=0,
        hardwareExecutionCredit=0,records=records,unsupportedControls=[dict(kind='instruction-cap',actualReturn=False,returnCredit=0),
            dict(kind='null-pointer-valid-input',actualReturn=False,nativeFault=malformed['states'][0]['fault'],returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,limitations=['Absolute0380FFF4 pointer origin is separately measured from an incomplete constructor prefix; no module BSS ownership',
            'Synthetic pointer targets/disposable MMIO only; no assigned register meaning, natural scene/thread reachability or physical hardware claim'])
