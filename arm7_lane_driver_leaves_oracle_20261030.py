import arm7_lane_driver_leaves_native_20261030 as fixture


def oracle(original,rebuilt,address):
    if original!=rebuilt:
        raise ValueError('Driver leaf complete source-only output differs')
    records,visited,returns=[],set(),0
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(address,original,case,seed)
        source=fixture.execute(address,rebuilt,case,seed)
        if native!=source or len(native['states'])!=case['passes'] or any(not x['actualReturn'] or x['fault'] is not None for x in native['states']):
            raise ValueError('Driver native/source full machine state, memory, writes or return differs')
        visited.update(native['visited'])
        here=len(native['states'])*2
        returns+=here
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,stateSha256=fixture.digest(repr(native).encode())))
    own=set(range(address,address+fixture.SIZES[address],4))
    if not own.issubset(visited):
        raise ValueError('Driver own instruction coverage incomplete')
    cap=fixture.execute(address,original,fixture.cases(address)[0],0,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Driver instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=returns,
        providerFreeOriginalAndCompiledReturns=returns,actualSeparatelyObservedNestedReturns={},
        allOwnInstructionAddressesVisited=sorted(own),fullRegistersFlagsStackAndMemoryCompared=True,
        meaningfulReturnContract='void; incidental R0 receives no result credit',independentFullMmioAndUntouchedMemoryModel=True,
        freshMachinePerScenario=True,cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=10000,timeoutMicroseconds=100000,
        providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,records=records,
        unsupportedControls=[dict(kind='instruction-cap',actualReturn=False,returnCredit=0)],unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Disposable MMIO backing verifies CPU reads/stores, not physical audio or peripheral behavior',
            'Logical channel0..15 is qualified; arbitrary indices and game-scene reachability are not established',
            'Stop preserves existing hold bit when input bit0 is clear; timer uses actual halfword truncation',
            'No function providers, BIOS services, device deployment or emulator execution'])
