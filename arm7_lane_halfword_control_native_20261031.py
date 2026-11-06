import hashlib
import prove_arm7_lane_halfword_pointer_20261031 as producer
from project import ROOT
ADDRESS,SIZE,CODE=0x027e9528,80,72
DATA,STACK,HARDWARE=producer.DATA,producer.STACK,producer.HARDWARE


def digest(data):return hashlib.sha256(data).hexdigest()


def cases():
    return [dict(offset=offset,enabled=enabled,control=control,received=value) for offset in (0x40,0x800)
        for enabled in (0,1,2,255,256,0x7fffffff,0x80000000,0xffffffff)
        for control in (0,0x7f,0x80,0x8000,0xffff) for value in (0,1,0x7fff,0x8000,0xffff)]


def setup(body,case,seed):
    if len(body)!=SIZE:raise ValueError('Complete host halfword control span differs')
    machine=producer.setup('',seed,case['offset'],(ADDRESS,body,CODE));cpu=machine['cpu'];target=machine['target']
    cpu.mem_write(target+0x33a,case['control'].to_bytes(2,'little'));cpu.mem_write(HARDWARE+0x2a,case['received'].to_bytes(2,'little'))
    return machine


def execute(body,case,seed,budget=1000):
    machine=setup(body,case,seed);cpu=machine['cpu'];target=machine['target'];expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in machine['regions'].items()}
    reads,writes=[],[];returned=5 if case['enabled']>1 else 0
    if case['enabled']<=1:
        value=(case['control']&~0x80)|((case['enabled']&1)<<7);offset=case['offset']+0x33a
        expected[DATA][offset:offset+2]=value.to_bytes(2,'little');writes.append([target+0x33a,2,value]);reads=[[producer.POINTER,4],[target+0x33a,2]]
        if case['enabled']==1:
            expected[HARDWARE][0x28:0x2a]=case['received'].to_bytes(2,'little');writes.append([HARDWARE+0x28,2,case['received']]);reads.append([HARDWARE+0x2a,2])
    execution=machine['invoke'](ADDRESS,[case['enabled']],budget)
    if not execution['actualReturn']:return dict(actualReturn=False,execution=execution,postFaultStateExcluded=True)
    actual_writes=[r for r in machine['writes'] if not STACK<=r[0]<STACK+0x4000];actual_reads=[r for r in machine['reads'] if not STACK<=r[0]<STACK+0x4000]
    data_reads=[r for r in actual_reads if not ADDRESS+CODE<=r[0]<ADDRESS+SIZE]
    if execution['registers'][0]!=returned or actual_writes!=writes or data_reads!=reads:raise ValueError('Independent host control full-word return/halfword data access model differs')
    if any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):raise ValueError('Independent complete host control mapped-memory effects differ')
    return dict(actualReturn=True,execution=execution,orderedReads=actual_reads,independentlyModeledDataReads=data_reads,orderedWrites=actual_writes,ownVisited=sorted(set(machine['visited'])),
        producerPrefix=machine['prefix'],actualOriginalInitializerFillReturns=1,constructorReturnCredit=0,independentCompleteMappedMemoryModel=True,
        memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in machine['regions'].items()},physicalHardwareCredit=0,ordinaryGameMeaning=None)
