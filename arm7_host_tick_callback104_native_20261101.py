import gzip
import json
from pathlib import Path
import arm7_host_tick_callback104_engine_20261101 as engine

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/arm7-bulk-20261030/lane-host-tick-callback104-final'
ENTRY,REGISTER,STATE=0x037FD1B4,0x037FB858,0x03807898


def cases():
    return [{'counter':counter,'reset':reset,'master':master,'mask':mask,'argument':argument}
        for counter in (0,0xFFFFFFFF,0xFFFFFFFFFFFFFFFF,0x123456789ABC)
        for reset in (0,1,0x80000000,0xFFFFFFFF) for master in (0,1,0xFFFF)
        for mask in (0,0x80000000,0xFFFFFFFF) for argument in (0,0xFFFFFFFF)]


def execute(bodies,case,seed,budget=100000):
    machine=engine.setup(bodies,seed)
    cpu=machine['cpu']
    launch=machine['invoke'](0x037FD128,[])
    if not launch['actualReturn'] or int.from_bytes(cpu.mem_read(0x038076B0,4),'little')!=ENTRY:
        raise ValueError('Actual original initializer did not install the complete callback')
    for address,width,value in [(STATE+8,8,case['counter']),(STATE+4,4,case['reset']),
        (0x04000208,2,case['master']),(0x04000210,4,case['mask']),
        (0x04000100,2,0xA5A5),(0x04000102,2,0x5A5A)]:
        cpu.mem_write(address,value.to_bytes(width,'little'))
    memory,stores=machine['snapshot'](),[]
    def put(address,width,value):
        for base,data in memory.items():
            if base<=address and address+width<=base+len(data):
                data[address-base:address-base+width]=value.to_bytes(width,'little')
                stores.append([address,width,value])
                return
        raise ValueError('Independent host tick model escaped mapped backing')
    counter=(case['counter']+1)&0xFFFFFFFFFFFFFFFF
    put(STATE+8,4,counter&0xFFFFFFFF)
    put(STATE+12,4,counter>>32)
    if case['reset']:
        put(0x04000102,2,0)
        put(0x04000100,2,0)
        put(0x04000102,2,0xC1)
        put(STATE+4,4,0)
    for address,width,value in [(0x038076B0,4,ENTRY),(0x038076B8,4,0),(0x04000208,2,0),
        (0x04000210,4,case['mask']|8),(0x04000208,2,case['master']),(0x038076B4,4,1)]:
        put(address,width,value)
    result=machine['invoke'](ENTRY,[case['argument']],budget)
    if not result['actualReturn']:
        return {'actualReturn':False,'actualInitializerReturnSeparate':True,'case':case,'execution':result,'sourceReturnCredit':0}
    actual=[item for item in result['writes']if not engine.STACK<=item[0]<engine.STACK+0x4000]
    if actual!=stores or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in memory.items()):
        raise ValueError('Independent complete counter/reset/timer/reregistration/full-memory model differs')
    expected_tail=[{'arguments':[0,ENTRY,0],'lr':engine.RETURN,'sp':engine.STACK+0x3000}]
    if result['timerWriterEntries']!=expected_tail:
        raise ValueError('Actual three-word writer tail ABI/LR/SP differs')
    if result['registers'][0]!=0x038076B4 or REGISTER not in result['visited']:
        raise ValueError('Actual tail writer path/R0 address residue differs')
    return {'actualReturn':True,'case':case,'originalInitializer':launch,'expectedOrderedStores':stores,
        'execution':result,'actualSourceLinkedWriterTailTransferThroughOriginalLr':True,
        'tailReturnAddsNoSecondOwnedReturn':True,'providerReplacements':[]}


def oracle(body,register):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    original={ENTRY:raw[ENTRY-engine.BASE:ENTRY-engine.BASE+104],REGISTER:raw[REGISTER-engine.BASE:REGISTER-engine.BASE+76]}
    if {ENTRY:body,REGISTER:register}!=original:
        raise ValueError('Both complete freshly linked callback and writer must equal native bytes')
    source={ENTRY:body,REGISTER:register}
    records,visited,helpers=[],set(),{}
    for seed,case in enumerate(cases()):
        native,compiled=execute({},case,seed),execute(source,case,seed)
        if native!=compiled or not native['actualReturn']:
            raise ValueError('Fresh original/callback-C/writer-C actual return/effects differ')
        records.append(native)
        visited.update(pc for pc in native['execution']['visited']if ENTRY<=pc<ENTRY+88)
        for frame in native['execution']['nestedReturns']:
            helpers[frame['entry']]=helpers.get(frame['entry'],0)+2
    cap=execute({},cases()[0],0,1)
    if cap['actualReturn']:
        raise ValueError('Exhausted callback prefix acquired normal return credit')
    data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    path=WORK/'supported-native-records.json.gz'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
    return {'vectors':len(records),'actualOriginalAndCompiledReturns':len(records)*2,
        'actualFreshSourceLinkedWriterTailTransfersSeparate':len(records)*2,'tailTransfersAddNoSecondOwnedReturn':True,
        'actualOriginalInitializerReturnsSeparate':len(records)*2,'additionalExhaustionInitializerReturnsSeparate':1,
        'actualOriginalHelperReturnsSeparate':helpers,
        'instructionCoverage':{'visited':sorted(visited),'unvisited':sorted(set(range(ENTRY,ENTRY+88,4))-visited)},
        'allRawRegistersFlagsStackAndFullMemoryCompared':True,'independentUnsigned64ResetAndIoModel':True,
        'trace':{'path':path.relative_to(ROOT).as_posix(),'rawSha256':engine.digest(data),'compressedSha256':engine.digest(path.read_bytes()),
            'rawBytes':len(data),'compressedBytes':path.stat().st_size,'gzipMtime':0},
        'providerReplacements':[],'writerAdditionalCoverageCredit':0,'dataOrAssemblyCredit':0,
        'unsupportedControls':[cap],'unsupportedReturnCredit':0,
        'limitations':['Actual original initializer installs callback, then synchronous isolated call; no asynchronous IRQ delivery or scene proof',
            'Counter/reset/IME/IE case setup deliberately overrides initialized fields after the real prefix',
            'Unused full-word pointer argument ignored; raw R0 residue has no API return meaning',
            'Tail writer transfers are separately observed, never added to owned return counts',
            'Absolute measured16-bit timer MMIO only; no ordinary-data pointer exception or physical timing/concurrency claim']}
