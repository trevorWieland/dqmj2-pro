import gzip
import json
from pathlib import Path
import main_sdk_thread_remove124_engine_20261101 as engine
import probe_main_sdk_thread_remove124_native_20261101 as setup_api

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/main-sdk-aux/20261101/thread-remove124-final'
ENTRY=0x020067FC
G,TARGET,CURRENT,QUEUE,WAITER,MUTEX=setup_api.G,setup_api.TARGET,setup_api.CURRENT,setup_api.QUEUE,setup_api.WAITER,setup_api.MUTEX


def cases():
    return [{'count':count,'depth':depth,'order':order,'features':features,'control':control,'state':index%3}
        for index,(count,depth,order,features,control)in enumerate(
            (count,depth,order,features,control)for count in(0,1,0xFFFFFFFF)for depth in(0,1)for order in(0,1)
            for features in('empty','queue','join','mutex','alarm','all')for control in(0,0x80))]


def put(memory,stores,address,width,value):
    for base,data in memory.items():
        if base<=address and address+width<=base+len(data):
            data[address-base:address-base+width]=value.to_bytes(width,'little');stores.append([address,width,value]);return
    raise ValueError('Independent thread-removal model escaped mapped backing')


def model(memory,case):
    stores=[]
    def p(address,value,width=4):put(memory,stores,address,width,value)
    count=case['count']
    if count<0xFFFFFFFF:count+=1;p(G+4,count)
    features=case['features']
    if features in('mutex','all'):
        p(TARGET+0x88,0);p(TARGET+0x8C,0);p(MUTEX+0xC,0);p(MUTEX+8,0)
    if features in('queue','all'):
        p(QUEUE,0);p(QUEUE+4,0)
    if case['order']:p(CURRENT+0x68,0)
    else:p(G+0x2C,CURRENT)
    p(TARGET+0x64,2)
    if features in('join','all'):
        p(TARGET+0x9C,0);p(TARGET+0xA0,0);p(WAITER+0x78,0)
        p(WAITER+0x64,1);p(WAITER+0x78,0);p(WAITER+0x80,0);p(WAITER+0x7C,0)
        p(TARGET+0xA0,0);p(TARGET+0x9C,0)
    if count>0:count-=1;p(G+4,count)
    if count==0 and case['depth']!=0:p(G+0x24,1,2)
    return stores,count


def execute(bodies,case,seed,budget=100000):
    machine=setup_api.setup(case,seed,bodies);cpu=machine['cpu'];memory=machine['snapshot']()
    stores,count=model(memory,case)
    result=machine['invoke'](ENTRY,[TARGET],budget)
    if not result['actualReturn']:return {'actualReturn':False,'case':case,'execution':result,'sourceReturnCredit':0}
    actual=[row for row in result['writes']if not engine.STACK<=row[0]<engine.STACK+0x4000]
    if actual!=stores or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in memory.items()):
        raise ValueError('Actual mutex/queue/list/state/join/scheduler full-memory and ordered-store model differs')
    if result['registers'][0]!=0x80 or result['cpsr']&0xC0!=case['control']:
        raise ValueError('Raw restore-helper R0 residue or initial IRQ/FIQ restoration differs')
    return {'actualReturn':True,'case':case,'execution':result,'expectedOrderedStores':stores,'finalSchedulerCount':count,
        'rawR0IsRestoreHelperResidueNotStatus':True,'waitingQueuePointerPreservedDespiteQueueUnlink':case['features']in('queue','all'),
        'providerReplacements':[],'currentThreadContextWasNotRemoved':True}


def current_control(bodies):
    machine=setup_api.setup({'currentTarget':True,'depth':1},0,bodies)
    result=machine['invoke'](ENTRY,[TARGET],20000)
    return {'actualReturn':result['actualReturn'],'execution':result,'instructionLimit':20000,
        'currentTargetAndSyntheticIrqDepthOne':True,'ownedReturnCredit':0,'postBoundaryStateExcluded':not result['actualReturn']}


def oracle(body):
    raw=engine.MODULE.read_bytes();native=raw[ENTRY-engine.BASE:ENTRY-engine.BASE+124]
    if body!=native:raise ValueError('Complete freshly linked thread-removal C must equal current native')
    source={ENTRY:body};records,visited,helpers=[],set(),{}
    for seed,case in enumerate(cases()):
        original,compiled=execute({},case,seed),execute(source,case,seed)
        if original!=compiled or not original['actualReturn']:
            raise ValueError('Original/C thread-removal typed ABI/full-state execution differs')
        records.append(original)
        visited.update(pc for pc in original['execution']['visited']if ENTRY<=pc<ENTRY+120)
        for frame in original['execution']['nestedReturns']:helpers[frame['entry']]=helpers.get(frame['entry'],0)+2
    cap=execute({},cases()[0],0,1)
    current_original,current_c=current_control({}),current_control(source)
    if cap['actualReturn']or current_original['actualReturn']or current_c['actualReturn']or current_original!=current_c:
        raise ValueError('Exhaustion/current-target path acquired false return or differs between source and native')
    data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/'supported-native-records.json.gz'
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
    return {'vectors':len(records),'actualOriginalAndCompiledReturns':len(records)*2,
        'actualOriginalHelperReturnsSeparate':helpers,'instructionCoverage':{'supportedVisited':sorted(visited),
            'unsupportedCurrentPathOwnVisited':sorted(pc for pc in current_original['execution']['visited']if ENTRY<=pc<ENTRY+120),
            'supportedUnvisited':sorted(set(range(ENTRY,ENTRY+120,4))-visited)},
        'independentMutexWaitQueueGlobalListStateJoinAndSchedulerModel':True,'allCpuFlagsStackAndMappedMemoryCompared':True,
        'noProviderReplacements':True,'initialSchedulerFFFFFFFFHasNetDecrementToFFFFFFFE':True,
        'waitingQueueUnlinkDoesNotClearTargetQueuePointer':True,'observedReturnIsRawRestoreMaskResidue':True,
        'trace':{'path':path.relative_to(ROOT).as_posix(),'rawSha256':engine.digest(data),'compressedSha256':engine.digest(path.read_bytes()),
            'rawBytes':len(data),'compressedBytes':path.stat().st_size,'gzipMtime':0},
        'unsupportedControls':[cap,current_original,current_c],'unsupportedReturnCredit':0,'originalHelperOrDataSourceCredit':0,
        'limitations':['Synthetic noncurrent-target normal-return domains; no scene, ownership or complete OS lifecycle validity claim',
            'Mutexes have empty wait queues and alarms have null callbacks; active alarm lists, arbitrary switch hooks, context-load paths and concurrency remain unqualified',
            'Selected-current target with explicit depth1 reaches a bounded no-return halt loop; zero owned normal-return/error-policy credit and no post-boundary state credit',
            'All helpers are original native bodies, not pure providers or new reconstructed source',
            'Minimum B4-byte typed thread view and raw field offsets are not proof of total original object allocation or game meanings']}
