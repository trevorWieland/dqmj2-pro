import gzip
import hashlib
import json
import arm7_child_lock_initializer136_native_20261031 as native
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address!=native.ADDRESS or len(original)!=native.SIZE or original!=rebuilt:raise ValueError('Full freshly linked child C must match all136 original bytes')
    records=[];normal=set();boundary=set();owned=0;unsupported=0
    for index,case in enumerate(native.cases()):
        for flags in range(4):
            seed=index*4+flags;a=native.execute(native.setup(original,case,seed));b=native.execute(native.setup(rebuilt,case,seed))
            if a!=b:raise ValueError('Original/compiled child initializer CPU/memory/access/termination comparison differs')
            records.append(dict(case=case,seed=seed,state=a))
            if a['actualReturn']:
                owned+=2*a['actualEntryReturns']
                for step in a['steps']:normal.update(step['ownVisited'])
            else:
                if not a['actualWaitBoundary']:raise ValueError('Unsupported child state is not its measured natural wait boundary')
                unsupported+=2;boundary.update(a['ownInstructionsBeforeBoundary'])
    if normal|boundary!=set(range(address,address+native.CODE,4)):raise ValueError('Actual normal/boundary union must cover all owned instructions')
    cap=native.execute(native.setup(original,native.cases()[0],0),budget=1)
    encoded=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();product=ROOT/'work/arm7-bulk-20261030/lane-child-lock-initializer136-final/supported-records.json.gz';product.parent.mkdir(parents=True,exist_ok=True);product.write_bytes(gzip.compress(encoded,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=owned,unsupportedNaturalWaitBoundaries=unsupported,
        actualWaitOrBiosExecutions=0,actualCalleeReturns=0,originalDeviceOrConcurrentExecutionCredit=0,originalSharedDataSourceCredit=0,
        fullRegistersFlagsStackMemoryAndAccessComparedForActualReturns=True,independentCompleteNonstackMemoryAndOrderedWriteModel=True,
        allOwnInstructionAddressesFromActualReturningCases=sorted(normal),additionalOwnInstructionAddressesFromZeroReturnBoundaries=sorted(boundary-normal),
        allOwnInstructionAddressesObservedAcrossBothScopes=sorted(normal|boundary),allOwnInstructionsVisitedInReturningCases=normal==set(range(address,address+native.CODE,4)),
        freshMachinePerScenario=True,persistentEntryCallsPerSupportedScenario='1 or2; second call preserves state after owner becomes0',instructionLimit=5000,timeoutMicroseconds=500000,
        sourceAbiContract=dict(argumentWords=0,returnType='void',nativeWordBytes=4,partialHandshakeViewBytes=8,ownerOffset=4,extensionOffset=6,originalObjectExtentProved=False),
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,rawSha256=hashlib.sha256(encoded).hexdigest(),rawBytes=len(encoded),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],moduleAdopted=False,functionMatchedBytes=136,
        limitations=['All returns occur with nonzero private initialization flag or synthetic shared owner007F; this does not prove enclosing kernel/scene reachability',
            'Unready states stop naturally at the wait thunk before its execution and have zero normal-return/physical wait/Bios credit',
            'The two instructions observed only on boundary paths are source matched but are not returned execution coverage',
            'Only the two approved partial runtime windows/typed relocation starts are qualified; no original object extent, module data ownership or original data recovery follows',
            'Normal and reentry effects are independently modeled; no original assembly source or all692-byte group approval is inferred'])
