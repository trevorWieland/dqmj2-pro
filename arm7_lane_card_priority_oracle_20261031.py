import gzip
import hashlib
import json
import arm7_lane_card_priority_native_20261031 as normal
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    fixture=normal
    if original!=rebuilt or len(original)!=normal.engine.SIZES[address]:raise ValueError('Fresh ordinary C must genuinely link the full original control span')
    records=[];nested={};visited=set();sleeps=0;providerfree=0
    for index,case in enumerate(fixture.cases(address)):
        for flag in range(4):
            seed=index*4+flag
            native=fixture.execute(address,original,case,seed);compiled=fixture.execute(address,rebuilt,case,seed)
            if native!=compiled or not native['actualReturn']:raise ValueError('Fresh original/compiled control CPU/flags/memory/access/return model differs')
            for entry,count in native['actualNestedReturns'].items():nested[entry]=nested.get(entry,0)+2*count
            actualsleeps=native.get('actualSleepProviderCalls',[]);sleeps+=2*len(actualsleeps)
            if not actualsleeps:providerfree+=2
            visited.update(native['ownVisited']);records.append(dict(case=case,seed=seed,state=native))
    cap=fixture.execute(address,original,fixture.cases(address)[0],0,budget=1)
    if cap['actualReturn']:raise ValueError('Bounded control prologue cap gained return')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/f'work/arm7-bulk-20261030/lane-card-priority64-final/{address:08x}-records.json.gz';product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),
        actualSeparatelyObservedNestedReturns=nested,providerFreeOriginalAndCompiledReturns=providerfree,
        syntheticBiosContractOriginalAndCompiledReturns=0,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        actualSleepProviderCalls=sleeps,originalSleepExecutionCredit=0,fullRegistersFlagsStackAndMemoryCompared=True,
        independentOwnOrderedStoreAndProtocolOrReturnModel=True,independentCompleteMappedMemoryModel=False,
        allOwnInstructionAddressesVisited=sorted(visited),freshMachinePerScenario=True,persistentEntryCallsPerScenario=1,
        instructionLimit=20000,timeoutMicroseconds=500000,nativeCalleeSourceCredit=0,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,
        limitations=['Actual original kernel, scheduler-disable and CARD initialization produce the thread/list context',
            'Original SetThreadPriority, IRQ controls and list/state effects execute without providers; scheduling stays disabled and context save/load is rejected',
            'Independent models check the own priority word/store, full-word old return, real helper arguments and actual thread-priority word; full helper RAM effects are compared rather than independently modeled',
            'Previous common priority overrides and priorities above31 are raw synthetic domains with no ordinary scheduler validity or game reachability claim',
            'Original native callees and unchanged data receive no new source credit'])
