import gzip
import hashlib
import json
import arm7_lane_node_initialization216_native_20261031 as native
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address!=native.ADDRESS or len(original)!=native.SIZE or original!=rebuilt:raise ValueError('Full freshly linked ordinary C must match all216 original bytes before fixture adoption')
    records=[];helpers={};owned=0;visited=set();lower=0
    for index,case in enumerate(native.cases()):
        for flags in range(4):
            seed=index*4+flags;a=native.execute(native.setup(original,case,seed));b=native.execute(native.setup(rebuilt,case,seed))
            if a!=b or not a['actualReturn']:raise ValueError('Original/source node CPU/memory/access/provider/return evidence differs')
            owned+=2*a['actualOwnedReturns'];records.append(dict(case=case,seed=seed,state=a))
            for step in a['steps']:
                visited.update(step['ownVisited']);lower+=2*len(step['lowerAllocationProviders'])
                for entry,count in step['actualNativeHelperReturns'].items():helpers[entry]=helpers.get(entry,0)+2*count
    if visited!=set(range(native.ADDRESS,native.ADDRESS+native.CODE,4)):raise ValueError('Every owned code instruction must actually execute')
    cap=native.execute(native.setup(original,native.cases()[0],0),budget=1)
    if cap['actualReturn']:raise ValueError('Prologue exhaustion gained a return')
    encoded=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();product=ROOT/'work/arm7-bulk-20261030/lane-node-initialization216-final/supported-records.json.gz';product.parent.mkdir(parents=True,exist_ok=True);product.write_bytes(gzip.compress(encoded,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=owned,actualSeparatelyObservedNestedReturns=helpers,
        actualOriginalClearPrerequisiteReturns=2*len(records),constructorPrefixActualReturns=0,constructorPrefixReturnCredit=0,actualLowerAllocationProviderCalls=lower,
        originalLowerHeapAndCallbackImplementationExecutionCredit=0,originalDeviceOrBiosExecutionCredit=0,sourceCreditForCalleesAndOriginalData=0,
        fullRegistersFlagsStackMemoryAndOrderedAccessCompared=True,independentCompleteMappedMemoryAndOwnedStoreModel=True,allOwnInstructionAddressesVisited=sorted(visited),
        sourceAbiContract=dict(argumentWords=1,argument='pointer to three native32 descriptor words',returnType='void',incidentalR0ComparedWithoutMeaning=True,initializerIdConstantsFitS16=True,rawAddressWords32=True),
        supportedAllocatorSelectorWords=[0,1],unsupportedAllocatorSelectorWords='all other raw words; no normal-return or defined-C behavior claim',
        allocatorNullOutcome='Caller still stores12 at context+3E0 and clears halfwords+3E4/+3E8; no success/error meaning assigned',
        freshMachinePerScenario=True,persistentEntryCallsPerScenario='1 or2; complete node/list reinitialization and bounded same-block provider tested',instructionLimit=20000,timeoutMicroseconds=500000,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,rawSha256=hashlib.sha256(encoded).hexdigest(),rawBytes=len(encoded),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],functionMatchedBytes=216,moduleAdopted=False,
        limitations=['Actual original descriptor-prefix clear, eleven accepted node initializers, allocator selector/list routines and IRQ-mask helpers execute',
            'Only the lower OS heap factory or synthetic descriptor callback is replaced; its141-byte request and null/non-null raw return are explicitly bounded',
            'No physical allocation, hardware IRQ behavior, scheduler, game scene or constructor completion follows from mapped-state fixtures',
            'All other selector words remain unsupported because the original allocator reaches an uninitialized-register path; this caller receives no expanded supported-domain claim',
            'The shared native32 pointer storage declaration remains unchanged; only the local work view changes from integer to pointer',
            'Full owned instruction and direct boundary coverage does not establish opaque-reference or full-program coverage'])
