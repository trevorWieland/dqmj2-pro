import json
import arm7_lane_mmio_pair_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('MMIO ordinary C must match complete genuine linked code/literals')
    records,visited,actual=[],set(),0
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] or row['fault'] for row in native['states']):
            raise ValueError('MMIO native/source complete machine/memory/access/return differs')
        visited.update(native['visited'])
        actual+=4
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),independentCompleteMmioAndGuardModel=True))
    own=set(range(address,address+fixture.CODES[address],4))
    if own-visited:
        raise ValueError('MMIO pair all source instructions were not reached')
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],17),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('MMIO instruction exhaustion received actual-return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns={},allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=1000,timeoutMicroseconds=100000,providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        meaningfulReturnContract='void; incidental R0 is compared as machine state only',records=records,
        unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],unsupportedReturnCredit=0,
        calleeSourceCredit=0,limitations=['Capture supports indices0/1 and full-word remaining arguments; arbitrary index/address arithmetic is unqualified',
            'Loop is a full-word zero/nonzero BOOL; enum-typed capture constants preserve the exact original conditional instruction layout',
            'Output testsall256 incoming register bytes; only the previousbit7 contributes, while unmasked raw argument bits may also set resultbits',
            'Pointer words are stored to synthetic MMIO and never dereferenced; no physical capture/audio/DMA/device/emulator behavior or game access is claimed',
            'The four-byte compiler pool in the output routine is attributed separately; no padding/original-data/provider/BIOS/callee credit'])
