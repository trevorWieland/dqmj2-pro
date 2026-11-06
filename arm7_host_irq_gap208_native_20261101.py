import json
import gzip
from pathlib import Path
import arm7_host_irq_gap208_native_engine_20261101 as engine

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/arm7-bulk-20261030/lane-host-irq-gap208-native'
RECORDS,CHECK,COUNTER,TICK,CALLBACK=0x03807680,0x0380FFF8,0x027FFC3C,0x03807898,0x037FD1B4
BITS=(8,9,10,11,3,4,5,6,0)


def cases():
    rows=[]
    for index in range(8):
        for direct in (False,True):
            for enabled in (0,1,0x80000000):
                for callback in (False,True):
                    for flag in (0,0x80000000):
                        rows.append(dict(index=index,direct=direct,enabled=enabled,callback=callback,flag=flag))
    for callback in (False,True):
        for value in (0,0xFFFFFFFF,0x12345678):
            for flag in (0,0xFFFFFFFF):
                rows.append(dict(index=8,direct=False,enabled=1,callback=callback,flag=flag,counter=value))
    return rows


def setup(case,seed):
    machine=engine.setup(seed)
    cpu=machine['cpu']
    def set_word(address,value,width=4):
        cpu.mem_write(address,value.to_bytes(width,'little'))
    for index in range(9):
        for offset,value in [(0,0),(4,0x12345678),(8,0xFFFFFFFF)]:
            set_word(RECORDS+index*12+offset,value)
    initialize=machine['invoke'](0x037FB798,[])
    if not initialize['actualReturn'] or bytes(cpu.mem_read(COUNTER,4))!=bytes(4):
        raise ValueError('Original initialization did not clear the reserved counter word')
    callback=(CALLBACK if case['index']<8 else 0x037FB638)if case['callback']else 0
    install=machine['invoke'](0x037FB7BC,[1<<BITS[case['index']],callback])
    record=RECORDS+12*case['index']
    if not install['actualReturn'] or bytes(cpu.mem_read(record,12))!=callback.to_bytes(4,'little')+(1).to_bytes(4,'little')+bytes(4):
        raise ValueError('Original IRQ bit producer did not install exactly the selected record')
    set_word(record+4,case['enabled'])
    set_word(CHECK,case['flag'])
    set_word(COUNTER,case.get('counter',0xAABBCCDD))
    set_word(TICK+8,0xFFFFFFFFFFFFFFFF if seed&1 else 0xFFFFFFFF,8)
    set_word(TICK+4,0xFFFFFFFF if(seed//4)&1 else 0)
    set_word(0x04000208,0xFFFF if seed&4 else 0,2)
    set_word(0x04000210,0xFFFFFFFF if seed&8 else 0x80000000)
    set_word(0x04000100,0xA5A5,2)
    set_word(0x04000102,0x5A5A,2)
    entry=0x037FB748 if case['index']==8 else(0x037FB63C if case['direct']else 0x037FB6C8+16*case['index'])
    return machine,entry,([case['index']]if case['direct']else []),[initialize,install]


def execute(case,seed,budget=100000):
    machine,entry,args,prefixes=setup(case,seed)
    cpu=machine['cpu'];memory=machine['snapshot']();stores=[]
    def get(address,width=4):
        return int.from_bytes(cpu.mem_read(address,width),'little')
    def put(address,width,value):
        for base,data in memory.items():
            if base<=address and address+width<=base+len(data):
                data[address-base:address-base+width]=value.to_bytes(width,'little')
                stores.append([address,width,value]);return
        raise ValueError('Independent host IRQ model escaped mapped backing')
    index=case['index'];record=RECORDS+12*index;bit=1<<BITS[index]
    mask=get(0x04000210);master=get(0x04000208,2)
    if index==8:
        put(COUNTER,4,(case['counter']+1)&0xFFFFFFFF)
        put(CHECK,4,case['flag']|1)
    else:
        put(record,4,0)
        if case['callback']:
            count=(get(TICK+8,8)+1)&0xFFFFFFFFFFFFFFFF
            put(TICK+8,4,count&0xFFFFFFFF);put(TICK+12,4,count>>32)
            if get(TICK+4):
                put(0x04000102,2,0);put(0x04000100,2,0);put(0x04000102,2,0xC1);put(TICK+4,4,0)
            put(RECORDS+48,4,CALLBACK);put(RECORDS+56,4,0)
            put(0x04000208,2,0);mask|=8;put(0x04000210,4,mask)
            put(0x04000208,2,master);put(RECORDS+52,4,1)
        put(CHECK,4,case['flag']|bit)
        enabled=1 if case['callback']and index==4 else case['enabled']
        if enabled==0:
            put(0x04000208,2,0);put(0x04000210,4,mask&~bit&0xFFFFFFFF);put(0x04000208,2,master)
    result=machine['invoke'](entry,args,budget)
    if not result['actualReturn']:
        return dict(case=case,entry=hex(entry),execution=result,prefixReturnsSeparate=len(prefixes),sourceCredit=0)
    actual=[row for row in result['writes']if not engine.STACK<=row[0]<engine.STACK+0x4000]
    if actual!=stores or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in memory.items()):
        raise ValueError('Independent host IRQ/real-callback/IE/counter complete-memory ordered effects differ')
    if index<8 and case['callback']:
        callbacks=[row for row in result['nestedReturns']if int(row['entry'],0)==CALLBACK]
        if len(callbacks)!=1 or callbacks[0]['tailEntries']!=['0x37fb858'] or len(result['tailTransfers'])!=1:
            raise ValueError('Actual callback return and tail writer transfer were conflated')
    return dict(case=case,entry=hex(entry),prefixes=prefixes,execution=result,expectedOrderedStores=stores,
        allCompleteMemoryAndOrderedEffectsValidated=True,providerReplacements=[],sourceCredit=0)


def run():
    records=[execute(case,seed)for seed,case in enumerate(cases())]
    if not all(row['execution']['actualReturn']for row in records):
        raise ValueError('Host IRQ scope fixture did not actually return')
    exhausted=execute(cases()[0],0,1)
    if exhausted['execution']['actualReturn']:
        raise ValueError('Exhausted host wrapper acquired return credit')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    WORK.mkdir(parents=True,exist_ok=True);path=WORK/'native-records.json.gz';path.write_bytes(gzip.compress(raw,mtime=0))
    visited=set(pc for row in records for pc in row['execution']['visited'])
    expected=set(range(0x037FB63C,0x037FB6B4,4))|set(range(0x037FB748,0x037FB78C,4))
    expected|=set(address+offset for address in range(0x037FB6C8,0x037FB748,16)for offset in(0,4,8))
    if expected-visited:raise ValueError('Supported host IRQ code scope lacks full instruction coverage')
    return dict(actualOwnedNativeReturns=len(records),actualInitializerAndInstallerReturnsSeparate=2*len(records),
        actualCallbackReturnsSeparate=sum(len([x for x in r['execution']['nestedReturns']if int(x['entry'],0)in(CALLBACK,0x037FB638)])for r in records),
        actualTailWriterTransfersSeparate=sum(len(r['execution']['tailTransfers'])for r in records),
        fullOwnCodeCoverageBytes=len(expected)*4,unvisitedCode=[],sourceCredit=0,nativeCodeCredit=0,dataCredit=0,
        trace=dict(path=path.relative_to(ROOT).as_posix(),rawSha256=engine.digest(raw),compressedSha256=engine.digest(path.read_bytes()),gzipMtime=0),
        unsupportedControls=[exhausted],unsupportedReturnCredit=0,
        limitations=['Synthetic isolated synchronous calls after real original initialization and bitmask callback producer; no IRQ delivery or concurrency',
            'Enabled flag, counter, timer, IME, IE and check-word fixtures deliberately overwrite producer state',
            'Only eight measured callback indexes and VBlank record8; no full-u32 index-domain source contract',
            'VBlank dummy callback is original ARM BX LR with incoming registers ignored; no broad callback ABI or original assembly authorship claim',
            'Register-shadow MMIO only; no hardware W1C/timing claim; reserved counter/check words require separate source-binding review',
            'One callback normal return and its original writer tail transfer are distinct; no duplicate return credit'])
