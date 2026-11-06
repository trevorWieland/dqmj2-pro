import json
from collections import Counter
import arm7_lane_sdk_flow_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Connected SDK C must genuinely link every own code/pool byte')
    records,visited,actual=[],set(),0
    nested,prerequisites=Counter(),Counter()
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(address,original,case,seed)
        source=fixture.execute(address,rebuilt,case,seed)
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Connected SDK original/source actual-return/machine/memory/ABI evidence differs')
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
            for row in result['prerequisites']:
                if not row['actualReturn']:
                    raise ValueError('Connected SDK original prerequisite did not actually return')
                prerequisites[row['entry']]+=1
        visited.update(native['visited'])
        actual+=4
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),
            independentOwnRecordOrderedStoreAndPhysicalCallAbiModel=True))
    own=set(range(address,address+fixture.CODES[address],4))
    if own-visited:
        raise ValueError('Connected SDK complete own instruction coverage is missing: '+str(sorted(own-visited)))
    cap=fixture.execute(address,original,fixture.cases(address)[0],19,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Connected SDK instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),
        separatelyScopedOriginalPrerequisiteReturns=dict(sorted(prerequisites.items())),
        allOwnInstructionAddressesVisited=sorted(own),fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=200000,timeoutMicroseconds=500000,providerReplacements=[],
        originalBiosExecutionCredit=0,hardwareExecutionCredit=0,meaningfulReturnContract='void; incidental R0 is compared as machine state only',
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Own complete entry returns are separate from original prerequisite and nested helper returns; no provider or BIOS substitution occurs',
            'Sequence player indices0..15, bounded synthetic byte streams/banks and actual original prepare/allocation/initialization helpers are exercised',
            'Alarm indices0/7, full u64 tick/period values, byte id truncation and explicit enable0/1/255 contexts are qualified',
            'Physical MW argument words are measured, including unaligned-in-register u64 parameter pairs and fifth/seventh stack words',
            'Original clock getter reads explicit synthetic counter words and timer0 states; periodic tick addition includes low-word carry and u64 wrap',
            'Original callback ARM03801EA8 is registered but not executed; clock interrupts, device/audio behavior and enclosing producer reachability remain unqualified',
            'Invalid indices/pointers, opaque game-resource interpretation and callback/interrupt dispatch are unsupported and receive no return or source credit'])
