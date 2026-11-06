import json
from collections import Counter
import arm7_lane_thread_create_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Thread-create ordinary C must genuinely link its complete unit')
    visited,records=set(),[]
    nested=Counter()
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Original/source thread-create complete returns/full memory/access/register records differ')
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
        visited.update(native['visited'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            completeNativeAndCompiledStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),
            independentWholeMappedMemoryModel=True,independentWriteFootprintModel=False))
    own=set(range(address,address+fixture.CODES[address],4))
    if own-visited:
        raise ValueError('Thread-create complete owned instruction coverage is missing: '+repr(sorted(own-visited)))
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],91),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Thread-create prologue exhaustion received return credit')
    count=4*len(records)
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=count,
        providerFreeOriginalAndCompiledReturns=count,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,independentStoreFootprintModel=False,
        measuredIdCounterAddress=hex(fixture.COUNTER),physicalArgumentWords=6,registerArgumentWords=4,stackArgumentWords=2,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=100000,timeoutMicroseconds=500000,
        meaningfulReturnContract='Thread creation is void; generated context PC/SP/LR/argument/state effects are independently checked without executing the new context',
        providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],unsupportedReturnCredit=0,records=records,
        limitations=['All six physical arguments are placed independently: four core registers plus stack-size and priority words on the caller stack',
            'Actual IRQ, unsigned-priority list insert, context initializer and word-clear helpers execute without providers; created contexts are never scheduled',
            'Thread-ID counter03807710 is independently derived from native literal038076F0 plus displacement32; unknown prefix word038076F0 is preserved',
            'New context CPSR/PC/SP/SVC-SP/LR/register zeroing, full32 argument, stack guards/clear, list placement and untouched user/errno fields are modeled',
            'Eight-to256-byte bounded stacks, both four-byte alignments, raw ARM/Thumb context tags, full priority/argument words and defined signed-ID increments are covered',
            'The Thumb pointer is a raw synthetic context-tag probe, not verified executable code or a scheduled thread',
            'Complete mapped memory is independently modeled and original/source ordered accesses match; redundant store multiplicity is not independently prescribed',
            'No new-thread execution, stack adequacy, ID/priority legality, physical scheduling/hardware, invalid buffers or signed-ID overflow is qualified'])
