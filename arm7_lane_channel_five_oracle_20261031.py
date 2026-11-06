import json
import arm7_lane_channel_five_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Complete channel ordinary C must match its genuine linked native span')
    records,visited,actual,nested=[],set(),0,0
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] or row['fault'] for row in native['states']):
            raise ValueError('Native/source channel complete registers/flags/stack/memory/accesses/returns differ')
        visited.update(native['visited'])
        here=len(native['states'])*2
        actual+=here
        nested+=sum(row['actualNestedScaleReturns'] for row in native['states']+source['states'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),
            independentCompleteWramMmioAndOrderedStoreModel=True,
            originalScaleReturnsPerEntry=native['states'][0]['actualNestedScaleReturns']))
    own=set(range(address,address+fixture.CODES[address],4))
    if own-visited:
        raise ValueError('Channel source full instruction coverage incomplete')
    capped=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],91),budget=1)
    if capped['states'][0]['actualReturn']:
        raise ValueError('Channel instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns={hex(fixture.SCALE):nested},allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=10000,timeoutMicroseconds=100000,providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        meaningfulReturnContract='void; incidental R0 is compared as machine state only',
        actualScaleHelperContract=dict(program='',processor='arm7',module='arm7-wram',mode='arm',address=hex(fixture.SCALE),
            inputTypes=['u32 volume','s32 pan'],returnType='u32',factorWord=hex(fixture.FACTOR),calleeSourceCredit=0,
            originalCodeExecuted=True,independentWordWrapAndArithmeticShiftModel=True),
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=capped['states'][0],returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Logical channels0..15 are supported; out-of-range C array indices, arbitrary enclosing callers and physical hardware/audio behavior are not established',
            'Cache bytes preserve the requested low8 bits before signed master override; the one factor word is tested by signed positive condition',
            'All remaining incoming parameter words, pointer bit patterns, shift operands and timer values are exercised as32-bit words; C uses unsigned shifts/subtraction to avoid signed overflow',
            'The actual scale helper executes and receiveszero new source credit; its modulo32-bit multiplication and arithmetic shift are modeled independently',
            'Full mapped guards and actual returns are required; synthetic MMIO reads/stores are CPU evidence only, with no providers,BIOS or device/emulator execution'])
