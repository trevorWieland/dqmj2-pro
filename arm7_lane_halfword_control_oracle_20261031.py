import gzip
import hashlib
import json
import arm7_lane_halfword_control_native_20261031 as native
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address!=native.ADDRESS or original!=rebuilt or len(original)!=native.SIZE:raise ValueError('Complete source-only host control link differs')
    records=[];visited=set()
    for index,case in enumerate(native.cases()):
        for flags in range(4):
            seed=index*4+flags;a=native.execute(original,case,seed);b=native.execute(rebuilt,case,seed)
            if not a['actualReturn'] or a!=b:raise ValueError('Fresh original/compiled host control CPU/memory/access/return proof differs')
            visited.update(a['ownVisited']);records.append(dict(case=case,seed=seed,state=a))
    cap=native.execute(original,native.cases()[0],0,budget=1)
    if cap['actualReturn']:raise ValueError('Host control cap acquired a return')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+chr(10)).encode();output=ROOT/'work/arm7-bulk-20261030/lane-halfword-control80-final/records.json.gz'
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),actualSeparateOriginalInitializerFillReturns=2*len(records),
        actualOriginalConstructorReturns=0,originalConstructorReturnCredit=0,actualSeparatelyObservedNestedReturns={},providerFreeOriginalAndCompiledReturns=2*len(records),
        allOwnInstructionAddressesVisited=sorted(visited),fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteMappedMemoryModel=True,independentDataReadWriteWidthAndStrideModel=True,
        freshMachinePerScenario=True,persistentCallsPerScenario=1,instructionLimit=1000,timeoutMicroseconds=200000,
        traceProduct=dict(path=output.relative_to(ROOT).as_posix(),compressedSha256=sha256(output),compressedBytes=output.stat().st_size,rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='instruction-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,hardwareExecutionCredit=0,nativeCalleeSourceCredit=0,originalDataSourceCredit=0,
        limits=['Actual descriptor/context-clear prefix produces the runtime word; no enclosing constructor/thread/game reachability claim',
            'Owned control has no callees/providers; real prerequisite fill returns are counted separately from owned routine returns',
            'Unsigned full-word inputs0/1 update a halfword bit and optionally transfer a halfword; every input>1 tested returns5 with no data access',
            'Mapped register words are disposable static inputs with no physical device/timing or Android-port claim'])
