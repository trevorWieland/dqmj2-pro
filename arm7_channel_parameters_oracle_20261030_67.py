import arm7_channel_parameters_native_20261030_67 as fixture


def oracle(original,rebuilt,address):
    if original!=rebuilt:
        raise ValueError('Full ordinary C leaf function and pool bytes differ')
    records,visited,returns=[],set(),0
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(address,original,case,seed)
        source=fixture.execute(address,rebuilt,case,seed)
        if native!=source or len(native['states'])!=case['passes'] or any(not row['actualReturn'] or row['fault'] is not None for row in native['states']):
            raise ValueError('Leaf original/source machine, ordered effects or return differ')
        visited.update(native['visited'])
        here=len(native['states'])*2
        returns+=here
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,
            completeStateSha256=fixture.digest(repr(native).encode())))
    code,size=fixture.UNITS[address]
    own=set(range(address,address+code,4))
    if not own.issubset(visited):
        raise ValueError('Incomplete leaf instruction coverage')
    exhausted=fixture.execute(address,original,fixture.cases(address)[0],0,budget=1)
    if exhausted['states'][0]['actualReturn']:
        raise ValueError('Instruction exhaustion received false return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=returns,
        providerFreeOriginalAndCompiledReturns=returns,actualSeparatelyObservedNestedReturns={},
        allOwnInstructionAddressesVisited=sorted(own),fullRegistersFlagsStackAndMemoryCompared=True,
        independentWholeEntryBytesCompared=True,sourceRangeExcludedFromStateHash=size,
        meaningfulReturnContract='s32 attenuation arithmetic-shift-right7 returned as a full32-bit word' if address==0x037FF82C else 'void; incidental R0 receives no result credit',
        independentOrderedStateAndWrapModel=True,freshMachinePerScenario=True,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=10000,timeoutMicroseconds=100000,
        providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        records=records,unsupportedControls=[dict(kind='instruction-cap',actualReturn=False,returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Only the executing source range is excluded from machine-state hashes; every one of those bytes independently matches the original',
            'Raw adjacent table reads are measured without assigning game-validity or parameter-legality meanings',
            'Attack direct-entry positive words above255 remain outside the source data-window contract',
            'No BIOS, function providers, physical sound, game lifecycle or emulator execution is established'])
