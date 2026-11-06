import json
from collections import Counter
import arm7_lane_sdk_state_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('SDK state ordinary C must match its complete real-linked function')
    records,visited,actual,nested=[],set(),0,0
    qualified=Counter()
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] or row['fault'] for row in native['states']):
            raise ValueError('SDK state complete native/source return/machine/memory/ABI evidence differs')
        visited.update(native['visited'])
        actual+=4
        nested+=sum(row['actualNestedReturns'] for row in native['states']+source['states'])
        for row in native['states']+source['states']:
            qualified.update(hex(call[0]) for call in row['leafCalls'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),independentCompleteMemoryAndStatusModel=True))
    own=set(range(address,address+fixture.CODES[address],4))
    if own-visited:
        raise ValueError('SDK state complete instruction coverage is missing')
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],17),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('SDK state instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(qualified.items())),
        allOwnInstructionAddressesVisited=sorted(own),fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=10000,timeoutMicroseconds=100000,providerReplacements=[],
        originalBiosExecutionCredit=0,hardwareExecutionCredit=0,meaningfulReturnContract='void; incidental R0 is compared as machine state only',
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Alarm initialization clears only enable/id bytes for eight64-byte records; all other work bytes remain preserved',
            'Shared-work null returns are supported; other cases use bounded synthetic pointers and actual channel/capture getter bodies',
            'Bit7 determines measured status masks; full incoming register bytes and walking-bit/random patterns are tested',
            'Synthetic MMIO establishes CPU effects only; enclosing scene access, physical audio/device timing and invalid pointer behavior are unqualified',
            'No providers,BIOS,input uploads,emulator/device execution or new callee-source/data-source credit'])
