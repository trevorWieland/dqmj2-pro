import gzip
import json
import random
from pathlib import Path
import main_sdk_lock_pair_engine_20261101 as engine

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/main-sdk-aux/20261101/lock-pair-native'
RECORD=engine.DATA+0x800
RELEASE,ACQUIRE=0x02005F08,0x02005F8C


def cases():
    rows=[{'entry':entry,'identity':identity,'flag':flag,'owner':identity&0xFFFF,'both':both,'callback':callback,'control':control}
        for entry in(RELEASE,ACQUIRE)for identity in(0,1,0xFFFF,0x10000,0x80000000,0xFFFFFFFF)
        for flag in(0,1,0x80000000,0xFFFFFFFF)for both in(0,0xFFFFFFFF)
        for callback in(0,0x02007FF4,0x02008020)for control in(0,0x40,0x80,0xC0)]
    rows +=[{'entry':RELEASE,'identity':identity,'flag':0x12345678,'owner':(identity^1)&0xFFFF,
        'both':both,'callback':callback,'control':control}for identity in(0,1,0xFFFF)
        for both in(0,1,0x80000000)for callback in(0,0x02008020)for control in(0,0xC0)]
    return rows


def put(memory,stores,address,width,value):
    for base,data in memory.items():
        if base<=address and address+width<=base+len(data):
            data[address-base:address-base+width]=value.to_bytes(width,'little');stores.append([address,width,value]);return
    raise ValueError('Independent lock model escaped mapped backing')


def record(memory):
    base=engine.BASE;offset=RECORD-base
    return bytes(memory[base][offset:offset+8])


def execute(bodies,case,seed,budget=100000,bad_pointer=False):
    machine=engine.setup(bodies,seed,case['control']);cpu=machine['cpu']
    cpu.mem_write(RECORD-16,random.Random(seed+3191).randbytes(64))
    cpu.mem_write(RECORD,case['flag'].to_bytes(4,'little')+case['owner'].to_bytes(2,'little')+b'\x5A\xA5')
    memory,stores=machine['snapshot'](),[]
    if bad_pointer:
        result=machine['invoke'](case['entry'],[case['identity'],0,case['callback'],case['both']],budget)
        return {'actualReturn':result['actualReturn'],'execution':result,'unsupportedNullPointer':True,'sourceReturnCredit':0}
    control=case['control'];callback_records=[]
    matches=case['identity']==case['owner']
    if case['entry']==RELEASE and not matches:
        expected_return=0xFFFFFFFE
    else:
        mask=0xC0 if case['both']else 0x80
        previous=control&mask;control|=mask
        if case['entry']==RELEASE:
            put(memory,stores,RECORD+4,2,0);expected_return=0
            invokes=bool(case['callback'])
        else:
            expected_return=case['flag'];put(memory,stores,RECORD,4,case['identity'])
            invokes=case['flag']==0 and bool(case['callback'])
        if invokes:
            callback_records.append(record(memory).hex())
            control|=0x80 if case['callback']==0x02007FF4 else 0xC0
        if case['entry']==RELEASE:put(memory,stores,RECORD,4,0)
        elif case['flag']==0:put(memory,stores,RECORD+4,2,case['identity']&0xFFFF)
        control=(control&~mask)|previous
    result=machine['invoke'](case['entry'],[case['identity'],RECORD,case['callback'],case['both']],budget)
    if not result['actualReturn']:
        return {'actualReturn':False,'case':case,'execution':result,'sourceReturnCredit':0}
    actual=[row for row in result['writes']if not engine.STACK<=row[0]<engine.STACK+0x4000]
    callback_events=[row for row in result['entryEvents']if row['lr']in('0x2005f54','0x2005fd4')]
    if actual!=stores or result['registers'][0]!=expected_return or result['cpsr']&0xC0!=control:
        raise ValueError('Actual full-word SWP/halfword owner/sentinel/mask model differs')
    if [row['recordBytes']for row in callback_events]!=callback_records or any(row['arguments'][0]!=0 for row in callback_events):
        raise ValueError('Callback invocation count, raw R0 or pre/post owner-write visibility differs')
    if any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in memory.items()):
        raise ValueError('Full nonstack mapped memory/guard model differs')
    return {'actualReturn':True,'case':case,'expectedRawReturn':expected_return,'expectedOrderedNonstackStores':stores,
        'expectedIrqFiqControlBits':control,'expectedCallbackVisibleRecords':callback_records,'execution':result,
        'callbackReturnIgnored':True,'providerReplacements':[]}


def oracle(bodies):
    raw=engine.MODULE.read_bytes()
    if bodies!={a:raw[a-engine.BASE:a-engine.BASE+n]for a,n in engine.SIZES.items()}:
        raise ValueError('Both complete freshly linked C lock source bodies must equal native')
    records,counts,visited,helpers=[],{a:0 for a in engine.SIZES},{a:set()for a in engine.SIZES},{}
    for seed,case in enumerate(cases()):
        native,compiled=execute({},case,seed),execute(bodies,case,seed)
        if native!=compiled or not native['actualReturn']:
            raise ValueError('Original/C lock ABI/callback/full-state return differs')
        records.append(native);a=case['entry'];counts[a]+=2
        visited[a].update(pc for pc in native['execution']['visited']if a<=pc<a+engine.SIZES[a])
        for frame in native['execution']['nestedReturns']:helpers[frame['entry']]=helpers.get(frame['entry'],0)+2
    caps=[execute({},next(row for row in cases()if row['entry']==a),a,1)for a in engine.SIZES]
    faults=[execute({},next(row for row in cases()if row['entry']==a),a,bad_pointer=True)for a in engine.SIZES]
    if any(row['actualReturn']for row in caps+faults):raise ValueError('Unsupported prefix/null pointer acquired return credit')
    data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/'supported-native-records.json.gz'
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
    return {'vectors':len(records),'actualOriginalAndCompiledReturns':sum(counts.values()),
        'actualOwnReturnCounts':{hex(a):n for a,n in counts.items()},'actualOriginalHelperAndCallbackReturnsSeparate':helpers,
        'instructionCoverage':{hex(a):{'visited':sorted(v),'unvisited':sorted(set(range(a,a+engine.SIZES[a],4))-v)}for a,v in visited.items()},
        'independentFullWordSwapHalfwordOwnerSentinelCallbackAndMaskModel':True,'allCpuFlagsStackAndMappedMemoryCompared':True,
        'callbackProofContract':'original ARM u32(void) CPSR helpers; return ignored and no consumed input arguments',
        'callbackCanRetainFiqDisableUnderIrqOnlyRestore':True,'recordMinimumViewBytes':8,'originalObjectExtentClaimed':False,
        'trace':{'path':path.relative_to(ROOT).as_posix(),'rawSha256':engine.digest(data),'compressedSha256':engine.digest(path.read_bytes()),
            'rawBytes':len(data),'compressedBytes':path.stat().st_size,'gzipMtime':0},
        'providerReplacements':[],'unsupportedControls':caps+faults,'unsupportedReturnCredit':0,'originalHelperOrCallbackSourceCredit':0,
        'limitations':['SWP is actual original8-byte ARM helper; synchronous Unicorn execution does not prove multicore atomicity or lock liveness',
            'Raw full-word IDs/flags and low16-bit owner stores, not a valid-ID range or import/scene policy',
            'Null record is outside defined C context; original fault has zero source/return credit',
            'Only original no-input CPSR callbacks are qualified; arbitrary callback ABI/reentrancy and Thumb callbacks remain untested',
            'No providers, original data/object extent, assembly or caller reachability credit']}
