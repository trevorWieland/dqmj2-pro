import gzip
import json
from pathlib import Path
import arm7_host_sleep_callback32_native_engine_20261101 as engine

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/arm7-bulk-20261030/lane-host-sleep-callback32-native'
ENTRY,WAKE,INFO,GLOBALS=0x037FC50C,0x037FC36C,0x03807714,0x038076F0


def cases():
    return [dict(count=count,depth=depth,state=state,alarm=alarm,need=need)
        for count in(0,1,0xFFFFFFFF)for depth in(0,1)for state in(0,0xFFFFFFFF)
        for alarm in(0,0xFFFFFFFF,engine.DATA+0x1000)for need in(0,0xFFFF)]


def setup(case,seed):
    machine=engine.setup(seed);cpu=machine['cpu'];slot=engine.DATA+0x100+4*(seed&1)
    thread,other=engine.DATA+0x400,engine.DATA+0x800
    for address,value,width in[(slot,thread,4),(thread+0x48,case['state'],4),(thread+0x94,case['alarm'],4),
        (thread+0x4C,0,4),(thread+0x54,1,4),(other+0x48,1,4),(other+0x4C,thread,4),(other+0x54,0,4),
        (GLOBALS+4,case['count'],4),(GLOBALS+8,INFO+4,4),(INFO,case['need'],2),(INFO+2,case['depth'],2),
        (INFO+4,other,4),(INFO+8,other,4),(INFO+12,0,4)]:
        cpu.mem_write(address,value.to_bytes(width,'little'))
    return machine,slot,thread


def execute(case,seed,budget=100000):
    machine,slot,thread=setup(case,seed);cpu=machine['cpu'];memory=machine['snapshot']();stores=[]
    def put(address,width,value):
        for base,data in memory.items():
            if base<=address and address+width<=base+len(data):
                data[address-base:address-base+width]=value.to_bytes(width,'little');stores.append([address,width,value]);return
        raise ValueError('Independent sleep-callback model escaped mapped memory')
    put(slot,4,0);put(thread+0x94,4,0);put(thread+0x48,4,1)
    if case['count']==0 and case['depth']!=0:put(INFO,2,1)
    result=machine['invoke'](ENTRY,[slot],budget)
    if not result['actualReturn']:return dict(case=case,execution=result,sourceReturnCredit=0)
    actual=[row for row in result['writes']if not engine.STACK<=row[0]<engine.STACK+0x4000]
    if actual!=stores or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in memory.items()):
        raise ValueError('Actual slot/alarm/wakeup/scheduler ordered and full-memory effects differ')
    expected=[dict(argument=hex(thread),lr=hex(engine.RETURN),sp=hex(engine.STACK+0x3000))]
    if result['wakeDirectTailEntries']!=expected:raise ValueError('Actual original wake tail pointer/LR/SP differs')
    return dict(case=case,slot=hex(slot),thread=hex(thread),execution=result,expectedOrderedStores=stores,
        completeMemoryAndOrderedEffects=True,sourceCredit=0,providerReplacements=[],actualWakeTailTransferSeparate=True)


def prefix(milliseconds,seed):
    machine=engine.setup(seed,stop_at=0x037FC4CC);cpu=machine['cpu'];thread=engine.DATA+0x400
    for address,value in[(GLOBALS+8,engine.DATA+0x80),(engine.DATA+0x80,thread),(thread+0x94,0xFFFFFFFF)]:
        cpu.mem_write(address,value.to_bytes(4,'little'))
    result=machine['invoke'](0x037FC468,[milliseconds])
    registers=result['registers'];sp=registers[13];delay=(milliseconds*33514)>>6
    stack_arg=int.from_bytes(cpu.mem_read(sp,4),'little')
    observed=dict(alarm=registers[0],tickLow=registers[1],tickHigh=registers[2],callback=registers[3],stackArgument=stack_arg)
    expected=dict(alarm=sp+8,tickLow=delay&0xFFFFFFFF,tickHigh=delay>>32,callback=ENTRY,stackArgument=sp+4)
    if result['actualReturn']or result['error']or result['pc']!='0x37fc4cc'or len(result['boundaryStops'])!=1 or observed!=expected:
        raise ValueError('Actual Sleep call-site prefix/64-bit conversion/private slot ABI differs')
    if int.from_bytes(cpu.mem_read(stack_arg,4),'little')!=thread or int.from_bytes(cpu.mem_read(thread+0x94,4),'little')!=registers[0]:
        raise ValueError('Original Sleep producer did not connect local slot and thread alarm pointer')
    if bytes(cpu.mem_read(registers[0],4))!=bytes(4)or bytes(cpu.mem_read(registers[0]+8,4))!=bytes(4):
        raise ValueError('Actual original alarm creation did not clear handler/tag')
    return dict(milliseconds=milliseconds,execution=result,actualCallArguments=observed,expectedCallArguments=expected,
        producerBoundaryOnly=True,outerReturnCredit=0,originalAlarmCreateAndIrqDisableReturnsSeparate=2)


def run():
    records=[execute(case,seed)for seed,case in enumerate(cases())]
    prefixes=[prefix(ms,1000+seed)for seed,ms in enumerate((0,1,63,64,0x7FFFFFFF,0x80000000,0xFFFFFFFF))]
    if not all(row['execution']['actualReturn']for row in records):raise ValueError('Original sleep-callback fixture failed to return')
    exhausted=execute(cases()[0],0,1)
    if exhausted['execution']['actualReturn']:raise ValueError('Exhausted callback acquired return credit')
    visited=set(pc for row in records for pc in row['execution']['visited'])
    if set(range(ENTRY,ENTRY+28,4))-visited:raise ValueError('Complete callback code was not visited')
    raw=(json.dumps(dict(records=records,prefixes=prefixes),sort_keys=True,separators=(',',':'))+'\n').encode()
    WORK.mkdir(parents=True,exist_ok=True);path=WORK/'native-records.json.gz';path.write_bytes(gzip.compress(raw,mtime=0))
    return dict(actualCallbackReturns=len(records),actualWakeTailTransfersSeparate=len(records),callbackCodeCoverageBytes=28,
        sleepCallerPrefixBoundaryStops=len(prefixes),sleepCallerActualOuterReturns=0,sleepCallerReturnCredit=0,
        actualPrefixAlarmCreateAndIrqDisableReturnsSeparate=2*len(prefixes),unsupportedControls=[exhausted],unsupportedReturnCredit=0,
        trace=dict(path=path.relative_to(ROOT).as_posix(),rawSha256=engine.digest(raw),compressedSha256=engine.digest(path.read_bytes()),gzipMtime=0),
        sourceCredit=0,nativeCodeCredit=0,providerReplacements=[],limitations=[
            'Synthetic thread records/list/current/scheduler-count/depth fields; no scene or ownership invariant claim',
            'Count0/depth0 keeps the ready higher-priority current thread selected; no context transfer or asynchronous delivery',
            'Actual full original wake/reschedule/IRQ helpers execute; wake tail transfer is not a second owned callback return',
            'Caller prefix stops before OS_SetAlarm; it proves argument production, not complete Sleep execution, timing or termination',
            'Native malformed pointer/error paths and complete caller source equivalence remain unqualified'])
