import json
from collections import Counter
import arm7_lane_word_dispatch_native_20261031 as fixture


def oracle(original,rebuilt,address):
    if address!=fixture.ADDRESS or original!=rebuilt:
        raise ValueError('Word-dispatch ordinary C must match all92 genuine linked bytes')
    records,visited,actual=[],set(),0
    nested=Counter()
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(fixture.setup(original,case,seed))
        source=fixture.execute(fixture.setup(rebuilt,case,seed))
        if native!=source or len(native['states'])!=case['passes'] or any(not row['actualReturn'] or row['fault'] for row in native['states']):
            raise ValueError('Word-dispatch complete native/source machine/memory/ABI/return differs')
        visited.update(native['visited'])
        here=len(native['states'])*2
        actual+=here
        for row in native['states']+source['states']:
            nested.update(row['nestedReturns'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,
            fullStateSha256=fixture.digest(json.dumps(native,sort_keys=True).encode()),
            independentFullMmioBufferAndOrderedAccessModel=True,originalHelperReturnsPerEntry=len(native['states'][0]['directCalls'])))
    own=set(range(address,address+fixture.SIZE,4))
    if own-visited:
        raise ValueError('Word-dispatch full23-instruction root coverage is incomplete')
    unsupported=[]
    tests=[('instruction-cap',fixture.cases()[0],1)]
    for command in (6,0x86):
        tests.extend((label,dict(command=command,qualifier=0,pointer=pointer,count=count,initialIo=0xFFFF,pattern=3,passes=1),10000)
            for label,pointer,count in (('zero-count',fixture.DATA+0x100,0),('unmapped-buffer',0x06000000,1),
                ('unbounded-full-word-count',fixture.DATA+0x100,0xFFFFFFFF)))
    for label,case,budget in tests:
        result=fixture.execute(fixture.setup(original,case,7),budget=budget)
        if result['states'][0]['actualReturn']:
            raise ValueError('Unsupported word-dispatch domain received actual-return credit')
        unsupported.append(dict(label=label,case=case,instructionLimit=budget,execution=result['states'][0],returnCredit=0))
    helper_contracts=[]
    binary=(fixture.ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    for target,length in fixture.HELPERS.items():
        helper_contracts.append(dict(program='',processor='arm7',module='arm7-main',mode='arm',address=hex(target),bytes=length,
            nativeSha256=fixture.digest(binary[target-fixture.MAIN:target-fixture.MAIN+length]),
            consumedArgumentWords=fixture.ARITIES[target],calleeSourceCredit=0,
            inputQualification='Zero-argument control helpers overwriteR0/IP/R3 before use and read no incoming flags; header consumesR0/R1; data helpers preserve and consumeR0/R1'))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=actual,
        providerFreeOriginalAndCompiledReturns=actual,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddressesVisited=sorted(own),
        fullRegistersFlagsStackAndMemoryCompared=True,independentFullMmioBufferAndOrderedAccessModel=True,
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=100000,timeoutMicroseconds=100000,providerReplacements=[],originalBiosExecutionCredit=0,
        hardwareExecutionCredit=0,meaningfulReturnContract='void; final incidental hardware-derived R0 is compared as machine state only',
        helperInputContracts=helper_contracts,records=records,unsupportedControls=unsupported,unsupportedReturnCredit=0,
        calleeSourceCredit=0,limitations=['Synthetic mapped04000138 reads/stores establishCPU behavior only, not physical RTC/serial/audio/device semantics',
            'Static MMIO backing returnszero for the sampled bit after its precedingbit0-clear; external bit transitions and hardware timing remain unproved',
            'Positive data counts1..8 and bounded even/odd disposable pointers are supported; raw command/qualifier words includeall0..255 commands and full-word boundarycontrols',
            'Zero/huge counts and unmapped data pointers can exhaust/fault; no enclosing caller reachability or application policy follows',
            'All five original helper bodies execute withzero source credit; no providers,BIOS,emulator/device I/O or original executable compiler input'])
