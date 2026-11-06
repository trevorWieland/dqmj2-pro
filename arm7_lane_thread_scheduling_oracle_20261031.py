import json
from collections import Counter
import arm7_lane_thread_scheduling_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or original!=rebuilt:
        raise ValueError('Thread-scheduling ordinary C must genuinely link its complete unit')
    visited,records=set(),[]
    nested=Counter()
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Original/source thread-scheduling complete returns/full memory/access/register records differ')
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
        visited.update(native['visited'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=4,
            completeNativeAndCompiledStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),
            independentWholeMappedMemoryModel=True,independentWriteFootprintModel=address!=0x037FC2E4))
    own=set(range(address,address+fixture.CODES[address],4))
    if own-visited:
        raise ValueError('Thread-scheduling complete owned instruction coverage is missing: '+repr(sorted(own-visited)))
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],91),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Thread-scheduling prologue exhaustion received return credit')
    count=4*len(records)
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=count,
        providerFreeOriginalAndCompiledReturns=count,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,independentStoreFootprintModel=address!=0x037FC2E4,
        schedulerContext=dict(rescheduleCount=1,address=hex(fixture.PRIVATE+4),providerReplacement=False),
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=100000,timeoutMicroseconds=500000,
        meaningfulReturnContract='First ready-state1 list pointer or0; priority-change BOOL word; wakeup is void with incidental R0 unassigned',
        providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        unsupportedControls=[dict(kind='instruction-cap',execution=cap['states'][0],returnCredit=0)],unsupportedReturnCredit=0,records=records,
        limitations=['Wakeup/select/priority routines execute unchanged original IRQ, list-insert and reschedule helpers without providers',
            'Synthetic rescheduleCount1 makes actual rescheduler return before any context switch; active scheduling and asynchronous effects are not qualified',
            'Wakeup final complete mapped memory effects are independently modeled; original/source ordered accesses match, but redundant store multiplicity is not independently prescribed',
            'Global sorted singly-linked and waiting doubly-linked synthetic lists are distinct; all original current data and BSS bytes outside modeled fields are preserved',
            'All four state-word patterns and full-word priority extremes are raw native observations, not claims of ordinary lifecycle/priority legality',
            'Idle-thread pointer rejection is measured at its actual BSS address; no BSS ownership or reconstructed original-data credit follows',
            'No physical concurrency, scheduler callback/context save-load, scene reachability, save/import policy, arbitrary cycles or invalid pointers are claimed'])
