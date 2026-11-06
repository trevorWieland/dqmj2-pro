import json
from collections import Counter
import arm7_lane_scheduler_counter_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address!=fixture.ADDRESS or len(original)!=56 or original!=rebuilt:
        raise ValueError('Scheduler-counter ordinary C must genuinely link its complete56 bytes')
    records,visited=[],set()
    nested=Counter()
    actual=0
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=case['passes'] or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Original/source scheduler increment/return/full memory/access/register proof differs')
        actual+=2*case['passes']
        for result in (native,source):
            for row in result['states']:
                nested.update(row['actualNestedReturns'])
        visited.update(native['visited'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=2*case['passes'],
            fullOriginalAndCompiledStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),independentFullMemoryAndSingleWordWriteModel=True))
    own=set(range(address,address+52,4))
    if visited!=own:
        raise ValueError('Supported scheduler-counter cases omit owned instruction addresses')
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],91),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Scheduler-counter prologue exhaustion received return credit')
    saturation=[fixture.original_saturation(original,seed) for seed in range(16)]
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario='one boundary call or two defined-domain calls',
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,independentExactStoreFootprintModel=True,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=100000,timeoutMicroseconds=500000,
        meaningfulReturnContract='For counter0..FFFFFFFE, return prior u32 count and increment by1; saturated source return remains undefined/unqualified',
        providerReplacements=[],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,records=records,
        originalOnlySaturationProbes=saturation,actualOriginalOnlySaturationReturns=len(saturation),compiledSaturationReturnCredit=0,
        unsupportedControls=[dict(kind='prologue-cap',execution=cap['states'][0],returnCredit=0)],unsupportedReturnCredit=0,
        limitations=['Actual IRQ helpers execute unchanged; full counter words and old return values are independently modeled with every other mapped byte preserved',
            'All16 initial NZCV patterns and IRQ/FIQ combinations are covered, with persistent reentry that never crosses into an undefined C return call',
            'Original-only saturation probes observe unchanged memory and incoming-R4 bits in R0 but assign no portable C result meaning or compiled return credit',
            'The public SDK C localcount really has no assignment at saturation; original undefined source behavior is retained explicitly rather than repaired or disguised as assembly',
            'No scheduler/context switch, caller legality, physical concurrency/hardware or saturation semantics beyond the observed native-only bits are claimed'])
