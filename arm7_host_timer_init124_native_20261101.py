import gzip
import json
import random
from pathlib import Path
import arm7_host_timer_init124_engine_20261101 as engine

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/arm7-bulk-20261030/lane-host-timer-init124-final'
ENTRY,CALLBACK,WRITER,STATE=0x037FD128,0x037FD1B4,0x037FB858,0x03807898


def cases():
    return [{'initialized':initialized,'reserved':reserved,'counter':counter,'reset':reset,'master':master,'mask':mask}
        for initialized in (0,1,0x8000,0xFFFF) for reserved in (0,1,0xFFFF)
        for counter in (0,0xFFFFFFFFFFFFFFFF,0x123456789ABC) for reset in (0,0xFFFFFFFF)
        for master in (0,0xFFFF) for mask in (0,0xFFFFFFFF)]


def put(memory,stores,address,width,value):
    for base,data in memory.items():
        if base<=address and address+width<=base+len(data):
            data[address-base:address-base+width]=value.to_bytes(width,'little')
            stores.append([address,width,value])
            return
    raise ValueError('Independent initializer model escaped mapped backing')


def get(memory,address,width):
    for base,data in memory.items():
        if base<=address and address+width<=base+len(data):
            return int.from_bytes(data[address-base:address-base+width],'little')
    raise ValueError('Independent initializer model read outside backing')


def enable(memory,stores):
    mask,master=get(memory,0x04000210,4),get(memory,0x04000208,2)
    for address,width,value in [(0x04000208,2,0),(0x04000210,4,mask|8),(0x04000208,2,master)]:
        put(memory,stores,address,width,value)


def initialize(memory,stores):
    if get(memory,STATE,2):
        return
    for address,width,value in [(STATE,2,1),(0x03807894,2,get(memory,0x03807894,2)|1),
        (STATE+8,4,0),(STATE+12,4,0),(0x04000102,2,0),(0x04000100,2,0),(0x04000102,2,0xC1),
        (0x038076B0,4,CALLBACK),(0x038076B4,4,1),(0x038076B8,4,0)]:
        put(memory,stores,address,width,value)
    enable(memory,stores)
    put(memory,stores,STATE+4,4,0)


def callback(memory,stores):
    counter=(get(memory,STATE+8,8)+1)&0xFFFFFFFFFFFFFFFF
    put(memory,stores,STATE+8,4,counter&0xFFFFFFFF)
    put(memory,stores,STATE+12,4,counter>>32)
    if get(memory,STATE+4,4):
        for address,width,value in [(0x04000102,2,0),(0x04000100,2,0),(0x04000102,2,0xC1),(STATE+4,4,0)]:
            put(memory,stores,address,width,value)
    put(memory,stores,0x038076B0,4,CALLBACK)
    put(memory,stores,0x038076B8,4,0)
    enable(memory,stores)
    put(memory,stores,0x038076B4,4,1)


def execute(bodies,case,seed,budget=100000):
    machine=engine.setup(bodies,seed)
    cpu=machine['cpu']
    cpu.mem_write(0x03807670,random.Random(seed+9181).randbytes(0x90))
    for address,width,value in [(STATE,2,case['initialized']),(STATE+2,2,0xA55A),(STATE+4,4,case['reset']),
        (STATE+8,8,case['counter']),(0x03807894,2,case['reserved']),
        (0x04000208,2,case['master']),(0x04000210,4,case['mask']),
        (0x04000100,2,0xA5A5),(0x04000102,2,0x5A5A)]:
        cpu.mem_write(address,value.to_bytes(width,'little'))
    memory,stores=machine['snapshot'](),[]
    initialize(memory,stores)
    result=machine['invoke'](ENTRY,[],budget)
    if not result['actualReturn']:
        return {'actualReturn':False,'case':case,'execution':result,'sourceReturnCredit':0}
    actual=[row for row in result['writes']if not engine.STACK<=row[0]<engine.STACK+0x4000]
    if actual!=stores or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in memory.items()):
        raise ValueError('Actual initializer flag/reservation/counter/timer/installer/IRQ/reset/full-memory model differs')
    expected_r0=case['initialized']or STATE
    if result['registers'][0]!=expected_r0:
        raise ValueError('Raw void initializer residue differs; no API meaning assigned')
    follow=None
    if case['initialized']==0:
        entry=get(memory,0x038076B0,4)
        argument=get(memory,0x038076B8,4)
        if entry!=CALLBACK or argument!=0:
            raise ValueError('Actual initializer failed to produce the reviewed callback/argument')
        next_stores=[]
        callback(memory,next_stores)
        follow=machine['invoke'](entry,[argument])
        actual=[row for row in follow['writes']if not engine.STACK<=row[0]<engine.STACK+0x4000]
        if not follow['actualReturn'] or actual!=next_stores or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in memory.items()):
            raise ValueError('Complete installed source-linked104/writer76 return/state chain differs')
        expected_tail=[{'arguments':[0,CALLBACK,0],'lr':engine.RETURN,'sp':engine.STACK+0x3000}]
        if follow['timerWriterEntries']!=expected_tail:
            raise ValueError('Installed callback failed the actual source-linked three-word tail ABI')
    return {'actualReturn':True,'case':case,'expectedInitializerOrderedStores':stores,'execution':result,
        'installedCallbackInvokedSynchronously':follow,'providerReplacements':[],
        'callbackWasProducedByActualInitializer':case['initialized']==0,'noAsyncIrqOrEnclosingSceneClaim':True}


def oracle(body,callback_body,writer):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    expected={a:raw[a-engine.BASE:a-engine.BASE+size]for a,size in {ENTRY:124,CALLBACK:104,WRITER:76}.items()}
    source={ENTRY:body,CALLBACK:callback_body,WRITER:writer}
    if source!=expected:
        raise ValueError('All three complete freshly linked source bodies must equal current native bytes')
    records,visited,helpers,callback_returns=[],set(),{},0
    for seed,case in enumerate(cases()):
        native,compiled=execute({},case,seed),execute(source,case,seed)
        if native!=compiled or not native['actualReturn']:
            raise ValueError('Fresh native/C initializer and full installed callback chain differ')
        records.append(native)
        visited.update(pc for pc in native['execution']['visited']if ENTRY<=pc<ENTRY+112)
        for item in [native['execution'],native['installedCallbackInvokedSynchronously']]:
            if item is None:continue
            for frame in item['nestedReturns']:
                helpers[frame['entry']]=helpers.get(frame['entry'],0)+2
        if native['installedCallbackInvokedSynchronously']is not None:
            callback_returns+=2
    cap=execute({},cases()[0],0,1)
    if cap['actualReturn']:
        raise ValueError('Exhausted initializer acquired return credit')
    data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    path=WORK/'supported-native-records.json.gz';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
    return {'vectors':len(records),'actualOriginalAndCompiledReturns':len(records)*2,
        'actualFreshSourceLinkedInstalledCallbackReturnsSeparate':callback_returns,
        'actualFreshSourceLinkedWriterTailTransfersSeparate':callback_returns,'tailTransfersAddNoSecondCallbackReturn':True,
        'actualOriginalHelperReturnsSeparate':helpers,
        'instructionCoverage':{'visited':sorted(visited),'unvisited':sorted(set(range(ENTRY,ENTRY+112,4))-visited)},
        'independentFlagReservationCounterTimerRecordIrqAndResetModels':True,'allRawRegistersFlagsStackAndFullMemoryCompared':True,
        'trace':{'path':path.relative_to(ROOT).as_posix(),'rawSha256':engine.digest(data),'compressedSha256':engine.digest(path.read_bytes()),
            'rawBytes':len(data),'compressedBytes':path.stat().st_size,'gzipMtime':0},
        'providerReplacements':[],'callbackAndWriterAdditionalCoverageCredit':0,'dataOrAssemblyCredit':0,
        'unsupportedControls':[cap],'unsupportedReturnCredit':0,
        'limitations':['Synchronous invocation of the pointer produced by actual initialization, no asynchronous IRQ or scene proof',
            'Nonzero initialized flags return without stores; random preexisting callbacks are deliberately not invoked',
            'Model raw16-bit flag,64-bit counter and MMIO values; no physical timing/concurrency or original data/object extent claim',
            'Both reconstructed callback and writer are freshly compiled dependencies with zero additional coverage',
            'Void raw R0 residue receives no invented API meaning']}
