import gzip
import hashlib
import json
import arm7_lane_card_control_native_20261031 as normal
import arm7_lane_card_control_receiver_native_20261031 as receiver
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    fixture=receiver if address==receiver.ADDRESS else normal
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
    product=ROOT/f'work/arm7-bulk-20261030/lane-card-control452-final/{address:08x}-records.json.gz';product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),
        actualSeparatelyObservedNestedReturns=nested,providerFreeOriginalAndCompiledReturns=providerfree,
        syntheticBiosContractOriginalAndCompiledReturns=0,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        actualSleepProviderCalls=sleeps,originalSleepExecutionCredit=0,fullRegistersFlagsStackAndMemoryCompared=True,
        independentOwnOrderedStoreAndProtocolOrReturnModel=True,independentCompleteMappedMemoryModel=address==0x03803114,
        allOwnInstructionAddressesVisited=sorted(visited),freshMachinePerScenario=True,persistentEntryCallsPerScenario=1,
        instructionLimit=20000,timeoutMicroseconds=500000,nativeCalleeSourceCredit=0,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,
        limitations=['Preflight independently checks the latest argument pointer after Wait, including an explicit bounded provider changing it during sleep',
            'ROM operation uses static synthetic data-ready/control/receive backing; physical cartridge configuration, timing or persistent storage are unproved',
            'Begin-task independent complete nonstack effects cover busy-clear entries; busy waits, callback invocation and enclosing reachability remain unsupported',
            'Receiver executes actual original kernel/CARD/second-thread prerequisites under disabled scheduling; normal helper effects are original/compiled compared without a complete independent helper-memory model',
            'Receiver tests raw phase/request/tag/enable words and pointer-only stores, including malformed values and wrap; it does not validate later worker dereferences or grant game/access/bank meaning',
            'Explicit volatile protocol reads and measured snapshots preserve native accesses; asynchronous reentrancy and full-program shared-memory semantics are not certified',
            'Original native callees and all unchanged data receive zero source credit'])
