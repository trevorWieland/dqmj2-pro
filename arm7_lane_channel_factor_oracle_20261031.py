import json
import arm7_lane_channel_factor_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address!=fixture.ADDRESS or original!=rebuilt:
        raise ValueError('Factor ordinary C must match all96 genuine linked bytes')
    records,visited,actual,nested=[],set(),0,0
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(fixture.setup(original,case,seed))
        source=fixture.execute(fixture.setup(rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] or row['fault'] for row in native['states']):
            raise ValueError('Factor setter native/source full state, effects, arguments or return differs')
        visited.update(native['visited'])
        here=len(native['states'])*2
        actual+=here
        nested+=sum(row['actualNestedScaleReturns'] for row in native['states']+source['states'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),
            independentFullWordFactorAndByteUpdateModel=True,actualScaleReturnsPerEntry=14))
    own=set(range(address,address+fixture.CODE,4))
    if own-visited or actual!=1280 or nested!=17920:
        raise ValueError('Factor setter own coverage/actual outer versus nested returns differ')
    capped=fixture.execute(fixture.setup(original,fixture.cases()[0],17),budget=1)
    if capped['states'][0]['actualReturn']:
        raise ValueError('Factor setter bounded exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns={hex(fixture.SCALE):nested},allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=20000,timeoutMicroseconds=100000,providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        meaningfulReturnContract='void; incidental R0 is compared as machine state only',
        actualScaleHelperContract=dict(program='',processor='arm7',module='arm7-wram',mode='arm',address=hex(fixture.SCALE),
            inputTypes=['u32 cached volume byte','s32 zero-extended pan byte'],returnType='u32',factorWord=hex(fixture.FACTOR),
            actualExecutionsPerEntry=14,calleeSourceCredit=0,originalCodeExecuted=True),
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=capped['states'][0],returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Every input is stored as the same full32-bit factor word; fourteen cache/MMIO scale updates occur even for zero or negative signed interpretations',
            'The mask leaves channels1/3 untouched; original cache bytes, neighboring register bytes and all other mapped state remain guarded',
            'Static mapped MMIO is CPU evidence only; physical audio/timing, enclosing caller reachability and platform replacement are not established',
            'The original scale body executes withzero new callee source credit; no providers,BIOS,device/emulator inputs or executable compiler blobs'])
