from collections import Counter
import arm7_lane_calc_timer_native_20261030 as timer
import arm7_lane_skip_native_20261031 as skip


def oracle(original,rebuilt,address):
    if original!=rebuilt:
        raise ValueError('Complete timing unit source-only output differs')
    fixture=timer if address==timer.ADDRESS else skip
    if address!=fixture.ADDRESS:
        raise ValueError('Unqualified timing source root')
    records,visited,nested=[],set(),Counter()
    returns=prerequisites=0
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        states=native.get('states',[native])
        if native!=source or any(not state['actualReturn'] or state['fault'] is not None for state in states):
            raise ValueError('Timing original/source full machine, memory, effects or actual return differs')
        visited.update(native['visited'])
        here=2*len(states)
        returns+=here
        if fixture is timer:
            nested['0x37fedcc']+=native['actualVeneerReturns']*2
        else:
            if len(states)!=case['passes']:
                raise ValueError('Persistent caller replay is incomplete')
            prerequisites+=len(native['prerequisites'])*2
            for state in states:
                nested.update({a:count*2 for a,count in state['actualFunctionReturns'].items() if int(a,0)!=address})
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,
            originalAndCompiledStateSha256=fixture.digest(repr(native).encode())))
    own=set(range(address,address+fixture.CODE,4))
    if not own.issubset(visited):
        raise ValueError('Timing own instruction coverage incomplete')
    cap=fixture.execute(original,fixture.cases()[0],0,budget=1)
    if cap.get('states',[cap])[0]['actualReturn']:
        raise ValueError('Timing instruction exhaustion received return credit')
    unsupported=[dict(kind='instruction-cap',actualReturn=False,returnCredit=0)]
    if fixture is timer:
        missing=fixture.execute(original,dict(fixture.cases()[0],service=None),991)
        if missing['actualReturn'] or missing['externalFailure'] is None:
            raise ValueError('Missing original BIOS received return credit')
        unsupported.append(dict(kind='missing-original-bios',actualReturn=False,returnCredit=0))
    limitations=(['Synthetic SVC27 input0..767/output0..65535 replaces only R0; original ARM veneer and Thumb BX execute',
        'No original BIOS table, implementation or clobber verification; no original BIOS execution credit',
        'Defined-source bounded shifts only; right-shift counts64 or greater and extreme normalization domains are excluded'] if fixture is timer else
        ['Original alarm/sequence/conditional track constructors execute before explicit synthetic no-channel wait/end contexts',
        'Original timer/alarm/tick helpers execute against zero-clock disposable MMIO; no function or service providers',
        'Independent counter/wrap, wait, slot, active-bit and ordered direct-call checks; opaque helper effects retain measured comparison only'])
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=returns,
        providerFreeOriginalAndCompiledReturns=0 if fixture is timer else returns,
        syntheticBiosContractOriginalAndCompiledReturns=returns if fixture is timer else 0,
        actualOriginalPrerequisiteReturns=prerequisites,actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),
        allOwnInstructionAddressesVisited=sorted(own),fullRegistersFlagsStackAndMemoryCompared=True,
        meaningfulReturnContract='u16 timer clamped16..65535 within declared service/source domain' if fixture is timer else 'void; incidental R0 receives no result credit',
        independentModel='signed-word input, unsigned64 product, normalized pitch, bounded shifts and clamp' if fixture is timer else 'complete-iteration/wait/slot/active/direct-call effects',
        freshMachinePerScenario=True,persistentCallsPerScenario=1 if fixture is timer else 2,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=10000 if fixture is timer else 100000,
        timeoutMicroseconds=100000 if fixture is timer else 200000,
        providerReplacements=['architectural SVC27 synthetic R0 contract'] if fixture is timer else [],
        originalBiosExecutionCredit=0,hardwareExecutionCredit=0,records=records,
        unsupportedControls=unsupported,unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=limitations+['No game assets, physical audio/timing, full scene reachability or ordinary helper source credit'])
