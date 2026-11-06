import json
from collections import Counter
import arm7_lane_messages_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Message C must genuinely link its entire own instruction extent')
    records,visited,actual=[],set(),0
    nested,prerequisites=Counter(),Counter()
    division_returns=0
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Message complete original/source return/state/access/ring records differ')
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
                division_returns+=len(row['originalSignedDivisionAbi'])
            prerequisites[result['originalInitializer']['entry']]+=1
        visited.update(native['visited'])
        actual+=4
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            originalDivisionContracts=[row['originalSignedDivisionAbi'] for row in native['states']],
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),independentCompleteMessageWordAndRingModel=True))
    own=set(range(address,address+fixture.SIZES[address],4))
    native_block=fixture.unsupported_block(address,original)
    source_block=fixture.unsupported_block(address,rebuilt)
    if native_block!=source_block:
        raise ValueError('Original/source unsupported bounded blocking execution classification differs')
    blocked_visited=set(native_block['visitedOwnInstructionAddresses'])
    if own-(visited|blocked_visited):
        raise ValueError('Message exact own instruction coverage is missing')
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],19),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Message prologue instruction exhaustion received return credit')
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),separatelyScopedOriginalPrerequisiteReturns=dict(sorted(prerequisites.items())),
        actualIndependentQuotientRemainderAbiReturns=division_returns,allOwnInstructionAddressesVisited=sorted(own),
        returnedScenarioInstructionAddresses=sorted(visited),unsupportedBlockingOnlyInstructionAddresses=sorted(blocked_visited-visited),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=100000,timeoutMicroseconds=500000,providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        meaningfulReturnContract='BOOL word0/1; message0 remains valid data, nullable output controls copying only',records=records,
        unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0),
            dict(kind='blocking-without-scheduler-actor',original=native_block,compiled=source_block,actualCompleteEntryReturns=0)],
        unsupportedReturnCredit=0,calleeSourceCredit=0,
        limitations=['Actual original initializer/wakeup/IRQ/division helpers execute without providers in bounded nonblocking returned cases',
            'Count0 empty queues and valid count1..4 ring states qualify full/empty returns, wrap, zero/high message words and null output',
            'Compiler-generated intrinsic division uses explicit R0 quotient/R1 remainder ABI checked on every actual call, not a generic C int-return helper binding',
            'A separately hash-qualified signed unrolled original range receives zero source/data credit; positive-divisor domain is independently checked',
            'Blocking controls use synthetic current-thread/scheduler-disabled fields and actual sleep/reschedule calls but never complete; only reached PC addresses are retained, all post-boundary state and return credit are excluded',
            'No general asynchronous scheduling, scene/caller reachability, ownership/import policy, physical concurrency or hardware behavior is claimed',
            'Malformed nonpositive-capacity/nonempty backing, invalid pointers and arbitrary inconsistent counters remain unsupported'])
