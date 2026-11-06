from collections import Counter
import arm7_exchannel_flush_native_20261030_66 as fixture


def oracle(original, rebuilt):
    if original != rebuilt:
        raise ValueError('Full source-only channel flush output differs')
    records, visited, nested = [], set(), Counter()
    returns = 0
    for seed, case in enumerate(fixture.cases()):
        native = fixture.execute(original,case,seed)
        source = fixture.execute(rebuilt,case,seed)
        if native != source:
            raise ValueError('Native and source flush registers, flags, stack, memory, stores or calls differ')
        if len(native['states']) != case['passes'] or any(not row['actualReturn'] or row['fault'] is not None for row in native['states']):
            raise ValueError('Supported flush path did not actually return')
        visited.update(native['visited'])
        here = len(native['states'])*2
        returns += here
        nested.update({key:value*2 for key,value in native['separatelyObservedNestedReturns'].items()})
        records.append(dict(case=case, seed=seed, actualOriginalAndCompiledReturns=here,
            completeStateSha256=fixture.digest(repr(native).encode())))
    own = set(range(fixture.ADDRESS,fixture.ADDRESS+fixture.CODE,4))
    if not own.issubset(visited):
        raise ValueError('Channel flush own instruction coverage is incomplete')
    exhausted = fixture.execute(original,fixture.cases()[1],977,budget=1)
    if exhausted['states'][0]['actualReturn']:
        raise ValueError('Instruction budget control received false return credit')
    return dict(supported=True, verifiedReturn=True, vectors=len(records), actualOriginalAndCompiledReturns=returns,
        providerFreeOriginalAndCompiledReturns=returns, actualSeparatelyObservedNestedReturns=dict(nested),
        allOwnInstructionAddressesVisited=sorted(own), fullRegistersFlagsStackAndMemoryCompared=True,
        freshMachinePerScenario=True, cpuModel='Unicorn TI925T ARMv4T surrogate', instructionLimit=100000,
        timeoutMicroseconds=100000, meaningfulReturnContract='void; incidental R0 receives no result credit',
        providerReplacements=[], originalBiosExecutionCredit=0, hardwareExecutionCredit=0,
        independentFullDriverCallArgumentsAndOrderedStores=True, maximumOutgoingArgumentWords=10,
        nativeAdjustmentFactor=dict(address='0x3807980', gate='signed-positive',
            scaleLiteral=dict(storage='0x37feca4',word='0x3807980'),
            role='One native word both gates and parameterizes scaling; no separate factor object'),
        supportedContextDomains=dict(syncBits=[0,31], kindCases=[0,1,2,255], logicalChannels=[0,15],
            cachedVolume=[0,255], cachedDivisor=[0,255], callerPan=[0,255], timer=[0,65535],
            adjustmentCases=[-1,0,1,16384,32767], overrideCases=[-1,0,64,127]),
        originalCodeRanges=[dict(start=hex(a),end=hex(z),mode='arm',sourceCredit=0) for a,z in fixture.ranges()],
        records=records, unsupportedControls=[dict(kind='instruction-cap',actualReturn=False,returnCredit=0)],
        unsupportedReturnCredit=0, calleeSourceCredit=0,
        limitations=['MMIO is disposable memory: CPU stores and cached state are measured, physical sound behavior is unverified',
            'No function providers or architectural service replacements are used',
            'Pointers, formats, pan and divisor include raw width-edge contexts without claiming legitimate game assets or hardware settings',
            'The same native word at03807980 gates and parameterizes pan-dependent volume scaling',
            'Outside computed pointer producers and game lifecycle are beyond the bounded direct-entry proof'])
