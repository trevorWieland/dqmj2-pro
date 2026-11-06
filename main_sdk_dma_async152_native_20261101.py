import gzip
import json
import random
from pathlib import Path
import main_sdk_dma_async152_engine_20261101 as engine
import probe_main_sdk_dma_async152_native_20261101 as setup_api

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/main-sdk-aux/20261101/dma-async152-final'
ENTRY,RECORDS,IO=0x0200867C,0x020E335C,0x04000000


def cases():
    rows=[]
    for channel in range(4):
        for size in(0,1,3,4,8,0xFFFFFFFF):
            for callback in(0,0x02008008):
                for control in(0,0x80):
                    for previous in(0,0xFFFFFFFF):
                        rows.append({'channel':channel,'bytes':size,'callback':callback,'argument':(0x80 if previous else 0)if size==0 else previous,
                            'control':control,'ie':previous,'master':0xFFFF if control else 0,
                            'source':engine.DATA+0x1000+(4 if control else 0),'destination':0xFFFFFFFC if control else engine.DATA+0x2000})
    rows +=[{'channel':channel,'bytes':size,'callback':0x02008008,'argument':0x80,'control':control,'ie':0x80000000,'master':1}
        for channel in(0,3)for size in(0,4)for control in(0x40,0xC0)]
    return rows


def put(memory,stores,address,width,value):
    for base,data in memory.items():
        if base<=address and address+width<=base+len(data):
            data[address-base:address-base+width]=value.to_bytes(width,'little');stores.append([address,width,value]);return
    raise ValueError('Independent DMA programming model escaped mapped backing')


def execute(bodies,case,seed,budget=100000,model=True):
    machine,args=setup_api.setup(case,seed,bodies);cpu=machine['cpu']
    cpu.mem_write(RECORDS-16,random.Random(seed+9971).randbytes(80))
    memory=machine['snapshot']();stores=[]
    control=case.get('control',0)
    if case['bytes']==0:
        if case.get('callback'):
            control=(control&~0x80)|case.get('argument',0)
    else:
        channel=case['channel'];register=IO+0xB0+12*channel
        if channel==0:
            put(memory,stores,register,4,0);put(memory,stores,register+4,4,0);put(memory,stores,register+8,4,0x81400001)
        if case.get('callback'):
            record=RECORDS+12*channel;mask=1<<(channel+8)
            put(memory,stores,record,4,case['callback']);put(memory,stores,record+8,4,case.get('argument',0))
            put(memory,stores,IO+0x208,2,0);put(memory,stores,IO+0x210,4,case.get('ie',0)|mask)
            put(memory,stores,IO+0x208,2,case.get('master',1));put(memory,stores,record+4,4,case.get('ie',0)&mask)
        transfer=args[3]>>2|(0xC4000000 if case.get('callback')else 0x84000000)
        put(memory,stores,register,4,args[1]);put(memory,stores,register+4,4,args[2]);put(memory,stores,register+8,4,transfer)
    result=machine['invoke'](ENTRY,args,budget)
    if not result['actualReturn']or not model:
        return {'actualReturn':result['actualReturn'],'case':case,'execution':result,'sourceReturnCredit':0,
            'postFaultOrBoundaryStateExcluded':not result['actualReturn']}
    actual=[row for row in result['writes']if not engine.STACK<=row[0]<engine.STACK+0x4000]
    callback=[row for row in result['entryEvents']if row['lr']=='0x20086b8']
    if actual!=stores or result['cpsr']&0xC0!=control or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in memory.items()):
        raise ValueError('Full raw DMA/callback/IRQ/IME register and mapped-memory model differs')
    if case['bytes']==0 and case.get('callback'):
        if len(callback)!=1 or callback[0]['arguments'][0]!=case.get('argument',0):
            raise ValueError('Zero-length callback failed actual full-word stack argument ABI')
    elif callback:raise ValueError('Nonzero-length callback was incorrectly invoked synchronously')
    if case['bytes']!=0:
        programs=[row for row in result['entryEvents']if row['entry']=='0x1ff8448']
        expected=[case['channel'],args[1],args[2],transfer]
        if len(programs)!=1 or programs[0]['arguments']!=expected:raise ValueError('Original ITCM programming four-word ABI differs')
    return {'actualReturn':True,'case':case,'execution':result,'expectedOrderedStores':stores,'expectedIrqFiqControlBits':control,
        'sixWordApiWithTwoOriginalCallerStackArguments':True,'nonzeroCallbackStoredNotInvoked':case['bytes']!=0,
        'transferCompletionOrDestinationMutationClaimed':False,'providerReplacements':[],'rawR0HasNoVoidApiMeaning':True}


def oracle(body):
    raw=engine.MODULE.read_bytes();native=raw[ENTRY-engine.BASE:ENTRY-engine.BASE+152]
    if body!=native:raise ValueError('Complete freshly linked DMA async C must equal current native')
    source={ENTRY:body};records,visited,helpers=[],set(),{}
    for seed,case in enumerate(cases()):
        original,compiled=execute({},case,seed),execute(source,case,seed)
        if original!=compiled or not original['actualReturn']:raise ValueError('Original/C complete DMA ABI/programming/callback state differs')
        records.append(original);visited.update(pc for pc in original['execution']['visited']if ENTRY<=pc<ENTRY+152)
        for frame in original['execution']['nestedReturns']:helpers[frame['entry']]=helpers.get(frame['entry'],0)+2
    unsupported=[]
    for kind,case,budget in [('one-instruction',cases()[0],1),
        ('sticky-busy',{'channel':1,'bytes':4,'callback':0,'busy':True},20000),
        ('channel0-rejected-source',{'channel':0,'bytes':4,'source':0x04000000,'callback':0},20000)]:
        a,b=execute({},case,0,budget,False),execute(source,case,0,budget,False)
        if a['actualReturn']or b['actualReturn']or a!=b:raise ValueError('Unsupported busy/rejected/prefix source gained return or differs')
        unsupported.append(dict(kind=kind,instructionLimit=budget,originalAndCEqual=True,**a))
    data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/'supported-native-records.json.gz'
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
    return {'vectors':len(records),'actualOriginalAndCompiledReturns':len(records)*2,'actualOriginalHelperAndCallbackReturnsSeparate':helpers,
        'instructionCoverage':{'visited':sorted(visited),'unvisited':sorted(set(range(ENTRY,ENTRY+152,4))-visited)},
        'independentFullWordControlShiftCallbackPriorMaskAndIoModel':True,'allCpuFlagsStackAndMappedMemoryCompared':True,
        'allMappedNonregisterRamRemainsUnchanged':True,'providerReplacements':[],
        'trace':{'path':path.relative_to(ROOT).as_posix(),'rawSha256':engine.digest(data),'compressedSha256':engine.digest(path.read_bytes()),
            'rawBytes':len(data),'compressedBytes':path.stat().st_size,'gzipMtime':0},
        'unsupportedControls':unsupported,'unsupportedReturnCredit':0,'originalHelperDataAssemblyOrExtentCredit':0,
        'limitations':['Synchronous Unicorn register programming with original main/ITCM helpers; no autonomous DMA transfer, completion or physical bus claim',
            'Channels0..3 are qualified fixture inputs, not a reconstructed input-validation guard or universal caller-validity policy',
            'Actual busy polling and channel0 source rejection preserve bounded no-return paths without post-boundary/error-policy credit',
            'Only original ARM u32(u32) restore-IRQ callback is qualified; arbitrary/Thumb callbacks and external interrupt dispatch remain untested',
            'Raw pointer words, lengths/shifts and prior IRQ mask bits are measured; no source/destination ownership, scene, assets or save meaning inferred',
            'All lower providers are actual original bodies, with zero additional source credit; no code/pool/data/register patches']}
