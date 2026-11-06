import gzip
import json
from pathlib import Path
import arm7_host_gettick164_engine_20261101 as engine
import arm7_host_timer_init124_native_20261101 as producers

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/arm7-bulk-20261030/lane-host-gettick164-final'
ENTRY,STATE=0x037FD21C,0x03807898
SIZES={ENTRY:164,0x037FD128:124,0x037FD1B4:104,0x037FB858:76}


def cases():
    return [{'counter':counter,'sample':sample,'pending':pending,'prefix':prefix}
        for counter in (0,1,0xFFFFFFFF,0x100000000,0xFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFF)
        for sample in (0,0x7FFF,0x8000,0xFFFF) for pending in (0,8,0x80000000,0xFFFFFFFF)
        for prefix in ('none','callback0','callbackFFFFFFFF','initialize')]


def execute(bodies,case,seed,budget=100000):
    machine=engine.setup(bodies,seed)
    cpu=machine['cpu']
    for address,width,value in [(STATE,2,0),(STATE+4,4,0xFFFFFFFF if case['prefix']=='callbackFFFFFFFF'else 0),
        (STATE+8,8,case['counter']),(0x03807894,2,0xA5A4),(0x04000100,2,case['sample']),
        (0x04000102,2,0x5AA5),(0x04000214,4,case['pending']),
        (0x04000208,2,(0,1,0xFFFF)[seed%3]),(0x04000210,4,(0,0x80000000,0xFFFFFFFF)[seed%3])]:
        cpu.mem_write(address,value.to_bytes(width,'little'))
    expected=machine['snapshot']()
    prefix=None
    if case['prefix']!='none':
        stores=[]
        if case['prefix']=='initialize':
            producers.initialize(expected,stores)
            address,args=0x037FD128,[]
        else:
            producers.callback(expected,stores)
            address,args=0x037FD1B4,[0xFFFFFFFF]
        prefix=machine['invoke'](address,args)
        actual=[row for row in prefix['writes']if not engine.STACK<=row[0]<engine.STACK+0x4000]
        if not prefix['actualReturn']or actual!=stores or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in expected.items()):
            raise ValueError('Required complete fresh C producer prefix did not return/model correctly')
    counter=producers.get(expected,STATE+8,8)&0xFFFFFFFFFFFF
    sample=producers.get(expected,0x04000100,2)
    pending=producers.get(expected,0x04000214,4)
    correction=bool(pending&8)and sample<0x8000
    predicted=(((counter+int(correction))<<16)|sample)&0xFFFFFFFFFFFFFFFF
    result=machine['invoke'](ENTRY,[],budget)
    if not result['actualReturn']:
        return {'actualReturn':False,'case':case,'prefix':prefix,'execution':result,'sourceReturnCredit':0}
    actual=[row for row in result['writes']if not engine.STACK<=row[0]<engine.STACK+0x4000]
    returned=result['registers'][0]|result['registers'][1]<<32
    accesses=[row for row in result['reads']if row[0]in(0x04000100,STATE+8,STATE+12,0x04000214)]
    expected_accesses=[[0x04000100,2],[STATE+8,4],[STATE+12,4],[0x04000214,4]]
    if actual or returned!=predicted or accesses!=expected_accesses or any(bytes(cpu.mem_read(base,len(data)))!=bytes(data)for base,data in expected.items()):
        raise ValueError('Unsigned48/16 pending correction, exact observation order or full nonstack state differs')
    initial_irq=0 if seed&1 else 0x80
    if result['cpsr']&0x80!=initial_irq:
        raise ValueError('Real disable/restore helpers did not preserve incoming IRQ-control bit')
    return {'actualReturn':True,'case':case,'prefix':prefix,'execution':result,'expectedUnsigned64Return':predicted,
        'pendingCorrection':correction,'observedClockReadsInOrder':accesses,'nonstackWrites':[],
        'incomingIrqControlBitRestored':True,'providerReplacements':[]}


def oracle(bodies):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    expected={address:raw[address-engine.BASE:address-engine.BASE+size]for address,size in SIZES.items()}
    if bodies!=expected:
        raise ValueError('All four complete freshly linked C bodies must equal current native bytes')
    records,visited,helpers,prefix_counts=[],set(),{},{}
    corrections={False:0,True:0}
    for seed,case in enumerate(cases()):
        native,compiled=execute({},case,seed),execute(bodies,case,seed)
        if native!=compiled or not native['actualReturn']:
            raise ValueError('Fresh original/C clock and typed source producer chain differ')
        records.append(native)
        visited.update(pc for pc in native['execution']['visited']if ENTRY<=pc<ENTRY+152)
        corrections[native['pendingCorrection']]+=2
        executions=[native['execution']]
        if native['prefix']is not None:
            prefix_counts[case['prefix']]=prefix_counts.get(case['prefix'],0)+2
            executions.append(native['prefix'])
        for execution in executions:
            for frame in execution['nestedReturns']:
                helpers[frame['entry']]=helpers.get(frame['entry'],0)+2
    caps=[execute({},cases()[0],0,1),execute({},cases()[-1],15,1)]
    if any(row['actualReturn']for row in caps):
        raise ValueError('Exhausted clock prefix acquired return credit')
    data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    path=WORK/'supported-native-records.json.gz';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
    return {'vectors':len(records),'actualOriginalAndCompiledReturns':len(records)*2,
        'actualFreshSourceLinkedProducerReturnsSeparate':prefix_counts,'producerHelpersAndCpsrReturnsSeparate':helpers,
        'additionalExhaustionProducerReturnsSeparate':sum(1 for row in caps if row['prefix']is not None and row['prefix']['actualReturn']),
        'pendingCorrectionOutcomes':{str(key):value for key,value in corrections.items()},
        'instructionCoverage':{'visited':sorted(visited),'unvisited':sorted(set(range(ENTRY,ENTRY+152,4))-visited)},
        'independentUnsigned48Counter16SampleCorrectionModel':True,'exactTimerCounterCounterLowHighPendingObservationOrder':True,
        'allRawRegistersFlagsStackAndFullMemoryCompared':True,'counterObjectDeclarationUnchanged':True,
        'qualifiedVolatileAccessIsNewObservationHypothesis':True,'counterIsNotMmioOrOriginallyVolatileProvenance':True,
        'trace':{'path':path.relative_to(ROOT).as_posix(),'rawSha256':engine.digest(data),'compressedSha256':engine.digest(path.read_bytes()),
            'rawBytes':len(data),'compressedBytes':path.stat().st_size,'gzipMtime':0},
        'providerReplacements':[],'allProducerAdditionalCoverageCredit':0,'dataOrAssemblyCredit':0,
        'unsupportedControls':caps,'unsupportedReturnCredit':0,
        'limitations':['Stable synchronous snapshots, actual original CPSR helpers; no asynchronous IRQ, atomicity/race, BIOS or physical timing claim',
            'Raw48-bit software counter and16-bit hardware sample, no elapsed-unit or scene meaning assigned',
            'Qualified volatile lvalue preserves observed shared-counter read ordering without changing compatible global declarations',
            'Reference static OSTick is not volatile; matching observation-qualified access is a new hypothesis, not original type provenance',
            'Original and fresh source128/104/76 producers are separately counted with zero additional coverage',
            'No ordinary-data absolute address, original object extent, padding, assembly or source-linked callee credit']}
