import json
from collections import Counter
import arm7_lane_mutex_release_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Mutex-release ordinary C must genuinely link its complete unit')
    visited,records=set(),[]
    nested,prerequisites=Counter(),Counter()
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Original/source mutex-release complete returns/full memory/access/register records differ')
        for result in (native,source):
            prerequisites.update(row['entry'] for row in result['originalPrerequisiteReturns'])
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
        visited.update(native['visited'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            completeNativeAndCompiledStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),
            independentWholeMappedMemoryModel=True,independentWriteFootprintModel=False))
    own=set(range(address,address+fixture.CODES[address],4))
    if own-visited:
        raise ValueError('Mutex-release complete owned instruction coverage is missing: '+repr(sorted(own-visited)))
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],91),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Mutex-release prologue exhaustion received return credit')
    count=4*len(records)
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=count,
        providerFreeOriginalAndCompiledReturns=count,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,independentStoreFootprintModel=False,separatelyScopedOriginalPrerequisiteReturns=dict(sorted(prerequisites.items())),
        schedulerContext=dict(rescheduleCount=1,address=hex(fixture.PRIVATE+4),providerReplacement=False),
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=100000,timeoutMicroseconds=500000,
        meaningfulReturnContract='Both mutex-release APIs are void; incidental R0 is compared but not assigned a C result meaning',
        providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],unsupportedReturnCredit=0,records=records,
        limitations=['Actual original InitMutex and uncontended LockMutex construct every mutex list before explicit disposable owner/count/waiter overrides',
            'Current and other owner pointers, zero/one/two/minus-one signed counts, head/interior/tail release and zero/one/three waiters are qualified',
            'Original dequeue, waiting-thread wakeup and IRQ helpers execute without replacements; awakened thread mutex fields remain independently preserved',
            'Synthetic rescheduleCount1 makes actual rescheduler return before context switching; no asynchronous scheduler behavior is qualified',
            'Complete mapped memory effects are independently modeled and original/source ordered accesses match; redundant store multiplicity is not independently prescribed',
            'Source-only header declares the measured two-word void DequeueItem helper rather than relying on the older breadth draft implicit declaration',
            'No ownership/import/game policy or ordinary reachability is inferred from inconsistent disposable owner/list/count cases',
            'INT_MIN decrement overflow, invalid pointers, cycles, concurrent waiters and physical hardware remain unsupported'])
