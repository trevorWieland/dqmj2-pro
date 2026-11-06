import gzip
import hashlib
import json
import arm7_lane_halfword_native_20261031 as native
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if original!=rebuilt or len(original)!=native.SIZES[address]:raise ValueError('Complete source-only genuine halfword link differs')
    records=[];returns=0;fills=0;visited=set()
    for index,case in enumerate(native.cases(address)):
        for flags in range(4):
            seed=index*4+flags;a=native.execute(address,original,case,seed);b=native.execute(address,rebuilt,case,seed)
            if not a['actualReturn'] or a!=b:raise ValueError('Fresh original/compiled halfword return/register/flags/memory/access/state proof differs')
            returns+=2*a['actualEntryReturns'];fills+=2*a['actualOriginalInitializerFillReturns']
            for step in a['steps']:visited.update(step['ownVisited'])
            records.append(dict(case=case,seed=seed,state=a))
    cap=native.execute(address,original,native.cases(address)[0],0,budget=1)
    if cap['actualReturn']:raise ValueError('Halfword instruction cap acquired a return')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+chr(10)).encode();output=ROOT/f'work/arm7-bulk-20261030/lane-halfword-context188-final/{address:08x}-records.json.gz'
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=returns,actualSeparateOriginalInitializerFillReturns=fills,
        actualOriginalConstructorReturns=0,originalConstructorReturnCredit=0,actualSeparatelyObservedNestedReturns={},providerFreeOriginalAndCompiledReturns=returns,
        allOwnInstructionAddressesVisited=sorted(visited),fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteMappedMemoryModel=True,independentDataReadWriteWidthAndStrideModel=True,
        freshMachinePerScenario=True,persistentCallsPerScenario=3 if address==native.CHILD else 1,instructionLimit=1000,timeoutMicroseconds=200000,
        traceProduct=dict(path=output.relative_to(ROOT).as_posix(),compressedSha256=sha256(output),compressedBytes=output.stat().st_size,rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='instruction-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,hardwareExecutionCredit=0,nativeCalleeSourceCredit=0,originalDataSourceCredit=0,
        limits=['Actual original descriptor/context-clear prefixes produce the runtime word before explicit caller setup; no enclosing constructor or ordinary-game reachability claim',
            'Own units have no callees/providers; prerequisite fills are counted independently from owned normal returns',
            'The recurrence uses defined unsigned multiplication, preserves native low16 stores/reloads and executes three connected state updates',
            'Halfword copying includes identity and forward overlap; widths/strides and all mapped bytes have an independent model',
            'Hardware transfer is tested only against disposable static16-bit register backing; physical device timing/delivery and malformed pointers remain unsupported',
            'Current source remains native32-bit address-word C, without an Android/host-pointer portability claim'])
