import hashlib
import random
import prove_arm7_lane_halfword_pointer_20261031 as producer
from project import ROOT
HOST,CHILD=0x027e926c,0x027e944c
CONTROL=0x027eadb8
DATA,STACK,HARDWARE=producer.DATA,producer.STACK,producer.HARDWARE
SIZES={HOST:48,CHILD:48,CONTROL:92}
CODES={HOST:44,CHILD:44,CONTROL:80}
PROGRAMS={HOST:'',CHILD:'dwc/utility.bin/move/child.srl',CONTROL:'dwc/utility.bin/move/child.srl'}


def digest(data):return hashlib.sha256(data).hexdigest()


def cases(address):
    if address==HOST:return [dict(offset=offset,pattern=pattern,source=source,passes=1) for offset in (0x40,0x800) for pattern in ('ascending','edges','random') for source in ('separate','identity','before','after')]
    if address==CHILD:
        pairs=((0,0),(0,0xffff),(1,0),(1,0xffff),(2,1),(0x7fff,0x8000),(0x8000,0x8000),(0xffff,0xffff),(0xffff,1),(0x8000,0xffff),(0x7fff,0xffff),(2,0xffff))
        return [dict(offset=offset,multiplier=a,increment=b,current=value,passes=3) for offset in (0x40,0x800) for a,b in pairs for value in (0,1,0x7fff,0x8000,0xffff)]
    if address==CONTROL:return [dict(offset=offset,enabled=enabled,control=control,received=value,passes=1) for offset in (0x40,0x800) for enabled in (0,1,2,255,256,0x7fffffff,0x80000000,0xffffffff) for control in (0,0x7f,0x80,0x8000,0xffff) for value in (0,1,0x7fff,0x8000,0xffff)]
    raise ValueError('Unqualified halfword entry')


def setup(address,body,case,seed):
    if address not in SIZES or len(body)!=SIZES[address]:raise ValueError('Complete halfword source span differs')
    machine=producer.setup(PROGRAMS[address],seed,case['offset'],(address,body,CODES[address]));cpu=machine['cpu'];target=machine['target'];args=[]
    def put16(where,value):cpu.mem_write(where,(value&0xffff).to_bytes(2,'little'))
    if address==HOST:
        destination=target+0x384
        source={'separate':DATA+0x2000,'identity':destination,'before':destination-4,'after':destination+4}[case['source']]
        values=list(range(16)) if case['pattern']=='ascending' else ([0,1,255,256,0x7fff,0x8000,0xffff]*3)[:16] if case['pattern']=='edges' else [random.Random(seed+i*317).getrandbits(16) for i in range(16)]
        cpu.mem_write(source,b''.join(v.to_bytes(2,'little') for v in values));args=[source];machine.update(source=source)
    elif address==CHILD:
        for offset,value in ((0x5f0,case['multiplier']),(0x5f2,case['increment']),(0x5f4,case['current'])):put16(target+offset,value)
    else:
        put16(target+0x33a,case['control']);put16(HARDWARE+0x2a,case['received']);args=[case['enabled']]
    machine.update(arguments=args,case=case)
    return machine


def snapshot(machine):return {base:bytearray(machine['cpu'].mem_read(base,len(data))) for base,data in machine['regions'].items()}


def read(memory,address,width):
    for base,data in memory.items():
        if base<=address and address+width<=base+len(data):return int.from_bytes(data[address-base:address-base+width],'little')
    raise ValueError('Independent halfword model read escaped mapping')


def store(memory,address,width,value):
    for base,data in memory.items():
        if base<=address and address+width<=base+len(data):data[address-base:address-base+width]=(value&((1<<(width*8))-1)).to_bytes(width,'little');return
    raise ValueError('Independent halfword model store escaped mapping')


def execute(address,body,case,seed,budget=1000):
    machine=setup(address,body,case,seed);cpu=machine['cpu'];expected=snapshot(machine);steps=[];target=machine['target']
    for iteration in range(case['passes']):
        wanted=[];wanted_reads=[];returned=0
        if address==HOST:
            wanted_reads=[[producer.POINTER,4]]
            for i in range(16):
                source=machine['source']+i*2;value=read(expected,source,2);destination=target+0x384+i*2
                wanted_reads.append([source,2]);wanted.append([destination,2,value]);store(expected,destination,2,value)
        elif address==CHILD:
            current=read(expected,target+0x5f4,2);returned=(current*case['multiplier']+case['increment'])&0xffff
            wanted=[[target+0x5f4,2,returned]];store(expected,target+0x5f4,2,returned)
            wanted_reads=[[producer.POINTER,4],[target+0x5f2,2],[target+0x5f4,2],[target+0x5f0,2],[target+0x5f4,2]]
        else:
            if case['enabled']>1:returned=5
            else:
                value=(case['control']&~0x80)|((case['enabled']&1)<<7);wanted=[[target+0x33a,2,value]];store(expected,target+0x33a,2,value)
                wanted_reads=[[producer.POINTER,4],[target+0x33a,2]]
                if case['enabled']==1:wanted_reads.append([HARDWARE+0x2a,2]);wanted.append([HARDWARE+0x28,2,case['received']]);store(expected,HARDWARE+0x28,2,case['received'])
        execution=machine['invoke'](address,machine['arguments'],budget)
        if not execution['actualReturn']:return dict(actualReturn=False,execution=execution,actualEntryReturns=0,postFaultStateExcluded=True)
        if execution['registers'][0]!=returned:raise ValueError('Independent full-word halfword return differs')
        writes=[r for r in machine['writes'] if not STACK<=r[0]<STACK+0x4000]
        reads=[r for r in machine['reads'] if not STACK<=r[0]<STACK+0x4000]
        data_reads=[r for r in reads if not address+CODES[address]<=r[0]<address+SIZES[address]]
        if writes!=wanted or data_reads!=wanted_reads:raise ValueError('Independent halfword data-read/write width/order/stride footprint differs')
        if any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):raise ValueError('Independent complete halfword mapped-memory effects differ')
        steps.append(dict(execution=execution,expectedReturn=returned,orderedReads=reads,independentlyModeledDataReads=data_reads,orderedWrites=writes,ownVisited=sorted(set(machine['visited']))))
    return dict(actualReturn=True,actualEntryReturns=len(steps),steps=steps,producerPrefix=machine['prefix'],actualOriginalInitializerFillReturns=1,constructorReturnCredit=0,
        independentCompleteMappedMemoryModel=True,independentOrderedAccessWidthAndStrideModel=True,
        memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in machine['regions'].items()},physicalHardwareCredit=0,ordinaryGameMeaning=None)
