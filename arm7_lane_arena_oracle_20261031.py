import json
from collections import Counter
import arm7_lane_arena_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Arena C must genuinely match its complete own instruction unit')
    records,visited,actual=[],set(),0
    nested=Counter()
    contract=None
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Arena complete original/source return/register/flag/memory/access records differ')
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
        visited.update(native['visited'])
        actual+=4
        contract=native['layoutContract']
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),independentCompleteArenaWordAndMemoryModel=True))
    own=set(range(address,address+fixture.SIZES[address],4))
    if own-visited:
        raise ValueError('Arena complete own instruction coverage is missing')
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],19),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Arena instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddressesVisited=sorted(own),
        qualifiedRuntimeControlAndOriginalLiteralContract=contract,fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=10000,timeoutMicroseconds=100000,providerReplacements=[],
        originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        meaningfulReturnContract='Raw32-bit lo/hi pointer word for getters; void initializer/setter incidental R0 is compared only as machine state',
        records=records,unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Nine lo/hi runtime words use the measured virtual table base027FFDA0 and hi offset36; the source describes only that72-byte prefix',
            'The table lies outside measured initialized ARM7-main bytes/BSS; neither module data ownership nor data-source credit is asserted',
            'Original init-hi/init-lo helpers execute and return with linker literal words checked against actual module BSS endpoints',
            'Fixed positive stack-size400 literals leave original callee zero/negative branches unexecuted; no callee source or general build-profile claim is made',
            'Only logical virtual memory is mapped; physical RAM-mirror aliasing, cross-processor concurrency, enclosing startup reachability and invalid indices remain unsupported',
            'Returned pointer words are not dereferenced; arbitrary words do not establish object validity or ownership',
            'No providers,BIOS,device/emulator execution,assembly/blob or whole-module/ROM credit'])
