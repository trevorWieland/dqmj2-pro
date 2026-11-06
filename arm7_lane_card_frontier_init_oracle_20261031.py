import gzip
import hashlib
import json
import arm7_lane_card_init_native_20261031 as fixture
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address!=fixture.ADDRESS or len(original)!=fixture.SIZE or original!=rebuilt:
        raise ValueError('Complete ordinary card common initialization C must genuinely link every original byte')
    records=[]
    nested={}
    for index,case in enumerate(fixture.cases(address)):
        for flags in range(4):
            seed=index*4+flags
            native=fixture.execute(fixture.setup(address,original,case,seed))
            source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
            if native!=source or len(native['states'])!=1 or any(not row['actualReturn'] for row in native['states']):
                raise ValueError('Original/source initializer thread/flag ABI/memory/actual returns differ')
            records.append(native)
            for state in native['states']:
                for entry,count in state['actualNativeHelperReturns'].items():
                    nested[entry]=nested.get(entry,0)+2*count
    own=set(range(address,address+fixture.CODE,4))
    if {pc for row in records for pc in row['visited']}!=own:
        raise ValueError('Initialization corpus did not visit every own instruction')
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],91),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Initialization bounded exhaustion gained return credit')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/'work/arm7-bulk-20261030/lane-card-frontier2240-final/supported-records.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),
        providerFreeOriginalAndCompiledReturns=2*len(records),syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=nested,separatelyScopedOriginalPrerequisiteReturns=2*sum(len(row['originalPrerequisites']) for row in records),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=False,
        independentCompleteMappedMemoryModel=True,independentSixWordThreadAndCallbackFlagModel=True,
        independentExactStoreFootprintModel=False,allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=1,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=20000,timeoutMicroseconds=500000,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        providerReplacements=[],taskThreadExecutions=0,contextSwitchExecutions=0,
        meaningfulReturnContract='void; no incidental R0 meaning',actualCreateThreadPhysicalWords=6,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,functionMatchedBytes=188,moduleAdopted=False,
        limitations=['Actual original kernel initialization and scheduler-disable prerequisites execute in every fresh machine',
            'Randomized common-state backing is preserved except measured fields, complete thread creation, callback registration/shared-ready bit and conditional enable word',
            'Six physical thread-create words and fixed priority4 are independently modeled; original native callees receive zero source credit',
            'Console halfword2 preserves existing enable value; other tested halfwords set1. No game-world, bank, entitlement or physical device meaning',
            'Task thread, SaveContext and LoadContext execution is forbidden; no scheduler enable/reentry/concurrency claim',
            'Volatile owner/reference qualifiers follow pinned public SDK structure context and measured exact instructions; same-SDK/version equivalence is not presumed'])
