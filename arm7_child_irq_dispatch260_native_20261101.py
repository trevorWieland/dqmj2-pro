import gzip
import json
import random
from pathlib import Path
import arm7_child_irq_dispatch_source_engine_20261101 as engine
import arm7_child_tick324_native_20261031 as ticks
import arm7_child_alarm_programmer156_native_20261031 as scalar_model

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-irq-dispatch260-final'
SIZES = {address:16 for address in range(0x037FBB14,0x037FBB84,16)} | {0x037FBB84:148}
CODES = {address:12 for address in range(0x037FBB14,0x037FBB84,16)} | {0x037FBB84:128}
INDEXES = [8,9,10,11,3,4,5,6,0]


def cases(address):
    indexes = range(9) if address==0x037FBB84 else [6-(address-0x037FBB14)//16]
    return [{'entry':address,'index':index,'callback':callback,'enabled':enabled,'argument':argument}
        for index in indexes for callback in (0,0x037FD900,0x037FD7D4)
        for enabled in (0,1,0x80000000,0xFFFFFFFF) for argument in (0,0xFFFFFFFF)]


def execute(bodies,case,seed,budget=100000):
    machine=engine.setup(bodies,seed)
    cpu=machine['cpu']
    table=bytearray(random.Random(seed+7201).randbytes(9*12+32))
    cpu.mem_write(0x0380594C-16,bytes(table))
    slot=0x0380594C+12*case['index']
    cpu.mem_write(slot,case['callback'].to_bytes(4,'little')+case['enabled'].to_bytes(4,'little')+case['argument'].to_bytes(4,'little'))
    for address,width,value in [(0x03805B60,8,(0,0xFFFFFFFF,0xFFFFFFFFFFFFFFFF)[seed%3]),
        (0x03805B5C,4,(0,1,0xFFFFFFFF)[seed%3]),(0x04000100,2,(0,0x7FFF,0x8000)[seed%3]),
        (0x04000214,4,(0,8)[seed%2]),(0x04000208,2,(0,1,0xFFFF)[seed%3]),
        (0x04000210,4,(0,0x80000000,0xFFFFFFFF)[seed%3]),(0x0380FFF8,4,(0,0x80000000,0xFFFFFFFF)[seed%3])]:
        cpu.mem_write(address,value.to_bytes(width,'little'))
    memory,stores=machine['snapshot'](),[]
    def put(address,width,value):
        scalar_model.store(memory,address,width,value,stores)
    def disable(mask):
        prior=engine.word(memory,0x04000210)
        master=engine.word(memory,0x04000208)&0xFFFF
        put(0x04000208,2,0)
        put(0x04000210,4,prior&(~mask&0xFFFFFFFF))
        put(0x04000208,2,master)
    put(slot,4,0)
    if case['callback']==0x037FD7D4:
        ticks.callback(memory,stores)
    elif case['callback']==0x037FD900:
        put(0x04000106,2,0)
        disable(16)
        put(0x0380FFF8,4,engine.word(memory,0x0380FFF8)|16)
    put(0x0380FFF8,4,engine.word(memory,0x0380FFF8)|(1<<INDEXES[case['index']]))
    if engine.word(memory,slot+4)==0:
        disable(1<<INDEXES[case['index']])
    arguments=[case['index']] if case['entry']==0x037FBB84 else []
    execution=machine['invoke'](case['entry'],arguments,budget)
    if not execution['actualReturn']:
        return {'actualReturn':False,'case':case,'execution':execution,'sourceReturnCredit':0}
    writes=[item for item in execution['writes'] if not engine.STACK<=item[0]<engine.STACK+0x4000]
    if writes!=stores:
        mismatch=next((i for i,pair in enumerate(zip(writes,stores))if pair[0]!=pair[1]),min(len(writes),len(stores)))
        raise ValueError({'dispatchWriteMismatch':mismatch,'case':case,'actual':writes[mismatch:mismatch+3],'model':stores[mismatch:mismatch+3]})
    if any(bytes(cpu.mem_read(base,len(data)))!=bytes(data) for base,data in memory.items()):
        raise ValueError('Independent complete callback-table/clock/IRQ/platform-word preservation model differs')
    return {'actualReturn':True,'case':case,'mask':1<<INDEXES[case['index']],
        'expectedOrderedStores':stores,'enabledAfterCallback':engine.word(memory,slot+4),
        'callbackFunctionAfterReturn':engine.word(memory,slot),'execution':execution,'providerReplacements':[]}


def oracle(bodies):
    raw=(ROOT/'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    original={address:raw[address-engine.BASE:address-engine.BASE+size]for address,size in SIZES.items()}
    if bodies!=original:
        raise ValueError('All eight full freshly linked C units must match original code/pool bytes')
    records,result=[],{}
    for address in SIZES:
        visited,callbacks,tail_entries=set(),{},0
        for index,case in enumerate(cases(address)):
            native,compiled=execute({},case,index),execute(bodies,case,index)
            if native!=compiled or not native['actualReturn']:
                raise ValueError('Fresh original/eight-source callback/dispatcher executions did not return/equal')
            records.append(native)
            visited.update(pc for pc in native['execution']['visited']if address<=pc<address+CODES[address])
            for frame in native['execution']['nestedReturns']:
                callbacks[frame['entry']]=callbacks.get(frame['entry'],0)+2
            if address!=0x037FBB84:
                tail_entries+=2*sum(pc==0x037FBB84 for pc in native['execution']['visited'])
        cap=execute({},cases(address)[0],0,1)
        if cap['actualReturn']:
            raise ValueError('Exhausted source unit prefix acquired a normal return')
        result[address]={'vectors':len(cases(address)),'actualOriginalAndCompiledReturns':2*len(cases(address)),
            'sourceLinkedDispatcherTailEntriesSeparate':tail_entries,'actualOriginalNestedReturnsSeparate':callbacks,
            'instructionCoverage':{'visited':sorted(visited),'unvisited':sorted(set(range(address,address+CODES[address],4))-visited)},
            'definedDispatcherIndexDomain':[0,8],'callbackCaseDomain':['null','original-callback16','original-tick-callback136'],
            'allRawRegistersFlagsStackAndFullMemoryCompared':True,'independentExactOrderedStoreAndFullMemoryModel':True,
            'rearmingOriginalTickCallbackRetained':True,'providerReplacements':[],'originalCallbackCodeOrDataCredit':0,
            'unsupportedControls':[cap],'unsupportedReturnCredit':0,
            'limitations':['Normal synchronous synthetic function calls, no hardware IRQ exception/concurrency or game reachability',
                'Opaque callback pointers and out-of-domain dispatcher indexes are not generalized',
                'Original tick callback can rearm record4, so enabled state is checked after the actual callback',
                'Original callback16 remains zero-source scaffolding without assembly justification']}
    data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    path=WORK/'supported-native-records.json.gz'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
    trace={'path':path.relative_to(ROOT).as_posix(),'rawSha256':engine.digest(data),'compressedSha256':engine.digest(path.read_bytes()),
        'rawBytes':len(data),'compressedBytes':path.stat().st_size,'gzipMtime':0}
    for value in result.values():
        value['trace']=trace
    return result
