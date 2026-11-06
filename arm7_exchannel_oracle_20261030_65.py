from collections import Counter
import arm7_exchannel_native_20261030_65 as fixture


def oracle(original, rebuilt):
    if original != rebuilt:
        raise ValueError('Complete channel function/literal bytes differ')
    records, unsupported, visited, nested = [], [], set(), Counter()
    free, bios, division = 0, 0, 0
    for seed, case in enumerate(fixture.cases()):
        native = fixture.execute(original, case, seed)
        source = fixture.execute(rebuilt, case, seed)
        if native != source:
            raise ValueError('Channel whole native/source machine state differs')
        visited.update(native['visited'])
        good, free_here, bios_here = 0, 0, 0
        for state in native['states']:
            if not state['actualReturn']:
                if state['externalFailure'] is None:
                    raise ValueError('Unexplained channel fault/nonreturn')
                unsupported.append(dict(case=case, seed=seed, returnCredit=0, state=state))
                continue
            if state['fault'] is not None:
                raise ValueError('Faulting channel execution cannot receive credit')
            good += 2
            if state['biosServices']:
                bios_here += 2
            else:
                free_here += 2
        free += free_here
        bios += bios_here
        division += len(native['independentSigned64Returns'])*2
        nested.update({key:value*2 for key,value in native['separatelyObservedNestedReturns'].items()})
        records.append(dict(case=case, seed=seed, actualOriginalAndCompiledReturns=good,
            providerFreeReturns=free_here, syntheticBiosContractReturns=bios_here,
            completeStateSha256=fixture.digest(repr(native).encode()),
            syntheticSvcCalls=[state['biosServices'] for state in native['states']],
            independentSigned64Returns=native['independentSigned64Returns']))
    own = set(range(fixture.ADDRESS, fixture.ADDRESS+fixture.CODE, 4))
    if not own.issubset(visited):
        raise ValueError('Channel own instruction coverage is incomplete')
    return dict(supported=True, verifiedReturn=True, vectors=len(records),
        actualOriginalAndCompiledReturns=free+bios, providerFreeOriginalAndCompiledReturns=free,
        syntheticBiosContractOriginalAndCompiledReturns=bios,
        actualSeparatelyObservedNestedReturns=dict(nested), independentlyCheckedSigned64Returns=division,
        allOwnInstructionAddressesVisited=sorted(own), fullRegistersFlagsStackAndMemoryCompared=True,
        freshMachinePerScenario=True, cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=100000, timeoutMicroseconds=100000,
        meaningfulReturnContract='void; incidental R0 receives no result credit',
        providerReplacements=[dict(kind='architectural-SVC', service='0x1b', nativeThumbEntry='0x3803828',
            inputRange=[0,767], syntheticReturnRange=[0,65535]),
            dict(kind='architectural-SVC', service='0x1c', nativeThumbEntry='0x380382c',
            inputRange=[0,723], syntheticReturnRange=[0,127])],
        providerContract='Only R0 is replaced; other GP registers/flags are preserved; original Thumb BX LR executes',
        originalBiosExecutionCredit=0, originalBiosTableCorrectnessClaim=False,
        independentChannelEnvelopeSweepLfoPanTimerAndServiceArgumentModel=True,
        originalSigned32SharedRuntimeRange=dict(first='0x3806c38', end='0x3806e44', sourceCredit=0,
            priorFrozenFixture='arm7_note_on_native_20261030_60.py'),
        records=records, unsupportedControls=unsupported, unsupportedReturnCredit=0, calleeSourceCredit=0,
        limitations=['Provider-free and synthetic BIOS-contract caller returns are separate measurements',
            'No BIOS input was sought, installed or executed; BIOS table contents/clobbers are not established',
            'Hardware status reads use disposable memory, without physical audio or hardware execution',
            'Synthetic contexts do not prove game assets, scene lifecycle or arbitrary malformed-state behavior',
            'Velocity128..255 qualifies raw adjacent table data; initialized sine phases stay0..0x7fff'])
