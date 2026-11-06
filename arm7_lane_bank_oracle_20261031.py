import json
from collections import Counter
import arm7_lane_bank_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address!=fixture.ADDRESS or original!=rebuilt:
        raise ValueError('Bank reader ordinary C must match its complete384-byte real-linked unit')
    records,visited,actual=[],set(),0
    nested=Counter()
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(fixture.setup(original,case,seed))
        source=fixture.execute(fixture.setup(rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] or row['fault'] for row in native['states']):
            raise ValueError('Bank reader original/source complete-return/state/memory/ABI records differ')
        for result in (native,source):
            for row in result['states']:
                nested.update(hex(pc) for pc in row['actualOriginalLeafCalls'])
        visited.update(native['visited'])
        actual+=4
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),independentCompleteBankBoundsAndEffectsModel=True))
    own=set(range(address,address+fixture.SIZE,4))
    if own-visited:
        raise ValueError('Bank reader own instruction/control-table coverage incomplete: '+str(sorted(own-visited)))
    cap=fixture.execute(fixture.setup(original,fixture.cases()[0],17),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Bank reader instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=10000,timeoutMicroseconds=100000,providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        meaningfulReturnContract='BOOL word0/1 plus partial output stores on failed type/range checks',records=records,
        unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['All256 stored type bytes, signed negative/out-of-count programs, bounded0..2 program table entries and distinct payloads are exercised',
            'Normal10-byte parameters and complete12-byte drum/split records use independent exact read/store and complete memory-preservation models',
            'Failed type/key validation can still store the selected type byte; successful normal copies preserve output byte1 while complete record copies overwrite it',
            'Drum min/max edges and signed-key extremes plus sorted/unsorted/repeated split thresholds demonstrate measured first-match behavior only',
            'Original mutex leaf bodies execute and actually return; no provider, BIOS or physical synchronization interpretation is substituted',
            'Only negative programs qualify null pointers; other malformed pointers, truncated/overlapping backing and game-resource meanings are unsupported',
            'No original data, callee, whole-module, ROM, assembly or scaffold source credit'])
