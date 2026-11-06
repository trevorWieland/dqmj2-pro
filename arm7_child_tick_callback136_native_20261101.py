import gzip
import json
from pathlib import Path
import arm7_child_alarm_engine_20261031 as engine
import arm7_child_tick324_native_20261031 as ticks

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/arm7-bulk-20261030/lane-child-tick-callback136-final'
ENTRY,REGISTER=0x037FD7D4,0x037FBCF8


def cases():
    return [{'counter':counter,'reset':reset,'master':master,'mask':mask,'argument':argument}
        for counter in (0,0xFFFFFFFF,0xFFFFFFFFFFFFFFFF,0x123456789ABC)
        for reset in (0,1,0x80000000,0xFFFFFFFF) for master in (0,1,0xFFFF)
        for mask in (0,0x80000000,0xFFFFFFFF) for argument in (0,0xFFFFFFFF)]


def execute(bodies,case,seed,budget=100000):
    machine=engine.setup(bodies,seed)
    cpu=machine['cpu']
    for address,width,value in [(0x03805B60,8,case['counter']),(0x03805B5C,4,case['reset']),
        (0x04000208,2,case['master']),(0x04000210,4,case['mask']),
        (0x04000100,2,0xA5A5),(0x04000102,2,0x5A5A)]:
        cpu.mem_write(address,value.to_bytes(width,'little'))
    memory,stores=machine['snapshot'](),[]
    ticks.callback(memory,stores)
    result=machine['invoke'](ENTRY,[case['argument']],budget)
    if not result['actualReturn']:
        return {'actualReturn':False,'case':case,'execution':result,'sourceReturnCredit':0}
    actual=[item for item in result['writes']if not engine.STACK<=item[0]<engine.STACK+0x4000]
    if actual!=stores or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in memory.items()):
        raise ValueError('Independent unsigned64 wrap/reset/timer/reregistration/full-memory model differs')
    if result['registers'][0]!=0x03805980:
        raise ValueError('Observed raw callback R0 residue differs; no API return meaning assigned')
    return {'actualReturn':True,'case':case,'expectedOrderedStores':stores,'execution':result,'providerReplacements':[]}


def oracle(body,register):
    raw=(ROOT/'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    original={ENTRY:raw[ENTRY-engine.BASE:ENTRY-engine.BASE+136],REGISTER:raw[REGISTER-engine.BASE:REGISTER-engine.BASE+76]}
    if {ENTRY:body,REGISTER:register}!=original:
        raise ValueError('Both complete freshly linked callback and writer must equal native bytes')
    source={ENTRY:body,REGISTER:register}
    records,visited,nested,helpers=[],set(),0,{}
    for seed,case in enumerate(cases()):
        native,compiled=execute({},case,seed),execute(source,case,seed)
        if native!=compiled or not native['actualReturn']:
            raise ValueError('Fresh original/callback-C/register-C did not return/equal')
        records.append(native)
        visited.update(pc for pc in native['execution']['visited']if ENTRY<=pc<ENTRY+116)
        for frame in native['execution']['nestedReturns']:
            if int(frame['entry'],0)==REGISTER:
                nested+=2
            else:
                helpers[frame['entry']]=helpers.get(frame['entry'],0)+2
    cap=execute({},cases()[0],0,1)
    if cap['actualReturn']:
        raise ValueError('Exhausted callback prefix acquired normal return credit')
    data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    path=WORK/'supported-native-records.json.gz'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
    return {'vectors':len(records),'actualOriginalAndCompiledReturns':len(records)*2,
        'actualFreshSourceLinkedWriterReturnsSeparate':nested,'actualOriginalHelperReturnsSeparate':helpers,
        'instructionCoverage':{'visited':sorted(visited),'unvisited':sorted(set(range(ENTRY,ENTRY+116,4))-visited)},
        'allRawRegistersFlagsStackAndFullMemoryCompared':True,'independentUnsigned64ResetAndIoModel':True,
        'trace':{'path':path.relative_to(ROOT).as_posix(),'rawSha256':engine.digest(data),'compressedSha256':engine.digest(path.read_bytes()),
            'rawBytes':len(data),'compressedBytes':path.stat().st_size,'gzipMtime':0},
        'providerReplacements':[],'writerAdditionalCoverageCredit':0,'dataOrAssemblyCredit':0,
        'unsupportedControls':[cap],'unsupportedReturnCredit':0,
        'limitations':['Synchronous synthetic normal calls, no physical timer/IRQ/concurrency or scene claim',
            'Unused full-word pointer argument is passed and ignored; raw R0 residue is not an API return value',
            'Absolute timer views are measured16-bit MMIO only, no ordinary-data pointer exception']}
