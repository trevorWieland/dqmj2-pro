from collections import Counter
import arm7_player_step_native_20261030_64_v6 as fixture

ADDRESS, SIZE, CODE = fixture.ADDRESS, fixture.SIZE, fixture.CODE
MASK_DEFAULTS = {0x038010DC, 0x03801100, 0x0380110C}


def oracle(original, rebuilt):
    if original != rebuilt:
        raise ValueError('Player step source does not match every native byte')
    mask_offset = 0x038010B8-ADDRESS
    if original[mask_offset:mask_offset+4].hex() != 'f00006e2':
        raise ValueError('Original masked command dispatch differs')
    records, visited, outer, prepares, nested = [], set(), 0, 0, Counter()
    for seed, case in enumerate(fixture.cases()):
        native = fixture.execute(original, case, seed)
        source = fixture.execute(rebuilt, case, seed)
        if native != source or any(not row['actualReturn'] or row['fault'] is not None for row in native['states']):
            raise ValueError('Original/source full player-step registers, flags, stack, memory, ordered effects or returns differ')
        outer += len(native['states'])*2
        prepares += 2
        visited.update(native['visited'])
        for row in native['states']:
            nested.update({key: count*2 for key,count in row['actualNestedReturns'].items()})
        records.append(dict(case=case, seed=seed, actualOriginalAndCompiledReturns=len(native['states'])*2,
            actualOriginalPreparationReturns=2, results=[row['registers'][0] for row in native['states']],
            completeNativeAndSourceStateSha256=fixture.digest(repr(native).encode())))
    own = set(range(ADDRESS, ADDRESS+CODE, 4))
    if own-visited != MASK_DEFAULTS:
        raise ValueError('Player-step reachable instruction coverage differs: '+repr(sorted(own-visited)))
    unsupported = []
    for name, case in (
        ('unbounded-zero-count-loop', dict(fixture.cases()[0], stream=[212, 0, 193, 55, 252])),
        ('unmapped-current-pointer', dict(fixture.cases()[0], patches=[[fixture.TRACK+0x28, 4, 0x03000000]]))):
        native = fixture.execute(original, case, 20261031, budget=2000)
        source = fixture.execute(rebuilt, case, 20261031, budget=2000)
        if native != source or any(row['actualReturn'] for row in native['states']):
            raise ValueError('Unsupported player-step path received return credit')
        unsupported.append(dict(name=name, returnCredit=0, state=native, instructionLimit=2000))
    return dict(supported=True, verifiedReturn=True, vectors=len(records),
        actualOriginalAndCompiledReturns=outer, actualOriginalPreparationReturns=prepares,
        actualSeparatelyObservedNestedReturns=dict(nested),
        allReachableOwnInstructionAddressesVisited=sorted(own-MASK_DEFAULTS),
        excludedMaskedDispatchDefaults=[dict(address=hex(address), instruction='b loop-command-continuation',
            reason='Dominating byte-command high-bit path and command&0xF0 restrict dispatch to 0x80..0xF0 in steps of16') for address in sorted(MASK_DEFAULTS)],
        originalMaskInstruction=dict(address='0x38010b8', bytes='f00006e2', operation='r0 = r6 & 0xf0'),
        freshMachinePerScenario=True, actualOriginalPreparationBeforeSyntheticPatches=True,
        cpuModel='Unicorn TI925T ARMv4T surrogate', instructionLimit=100000, timeoutMicroseconds=100000,
        providerReplacements=[], independentPlayerTrackChannelAllocationBankVariableCacheModel=True,
        fullRegistersFlagsStackAndMemoryCompared=True, meaningfulReturnContract='u32 result0or1;1 iff no mapped track remains playing',
        noteVelocityProducer=dict(nativeCall='0x3800e40', nativeFunction='0x3800290', actualReturnedByteDomain=[0,255],
            all256PositivePlaybackVelocitiesTested=True, declaredSourceLocalType='u8'),
        records=records, unsupportedControls=unsupported, unsupportedReturnCredit=0, calleeSourceCredit=0,
        limitations=['Deterministic synthetic bank/archive/wave data; no physical audio, game-asset reachability or scene-lifecycle claim',
            'Native lower helpers execute and receive zero new source credit',
            'Malformed and nonterminating original paths retain zero supported-return credit',
            'Variable indexes32..255 qualify raw adjacent synthetic cells without invented semantic names',
            'Shift fixtures exclude negative left operands and counts outside-15..15; arbitrary C undefined-shift domains remain unsupported',
            'Configured direct callers are boundary-qualified separately; opaque computed entry producers remain outside this entry-domain proof'])
