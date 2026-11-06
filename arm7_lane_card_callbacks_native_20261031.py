import struct
import arm7_lane_card_service_engine_20261031 as engine
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_CPSR
from project import ROOT
BASE=0x037f8000
MODULE='extract/arm7/runtime/arm7-wram.bin'
IO,STATE,SOURCE,DESTINATION=0x040001a0,engine.DATA,engine.DATA+0x200,engine.DATA+0x400
SIZES={0x038028e4:64,0x03802924:80,0x03802974:100}


def execute(address,body,case,seed,mediated=False,budget=20000,busy=False):
    raw=(ROOT/MODULE).read_bytes()
    source_body=body
    if len(source_body)!=SIZES[address]:raise ValueError('Complete source callback extent differs')
    transfer_body=raw[0x03802860-BASE:0x03802860-BASE+132]
    machine=engine.setup(0x03802860,transfer_body,seed);cpu=machine['cpu']
    cpu.mem_write(address,source_body)
    cpu.mem_write(STATE,struct.pack('<IIII',case['count'],SOURCE,DESTINATION,case['flag']))
    cpu.mem_write(SOURCE,bytes([case['source']]))
    cpu.mem_write(IO,bytes(4))
    if busy:cpu.mem_write(IO,(0x80).to_bytes(2,'little'))
    snapshots=engine.snapshot(machine)
    entered=[];reads=[];modes=[]
    read_pc={0x038028e4:0x03802908,0x03802924:0x0380295c,0x03802974:0x03802998}[address]
    pc_state=dict(pc=None)
    def code(uc,pc,size,unused):
        pc_state['pc']=pc
        if pc==address:
            entered.append(uc.reg_read(engine.match_runtime.REGISTERS[14]))
            modes.append(bool(uc.reg_read(UC_ARM_REG_CPSR)&32))
    def read(uc,access,target,size,value,unused):
        if pc_state['pc']==read_pc and target==IO+2:
            reads.append(case['response'])
            uc.mem_write(IO+2,case['response'].to_bytes(2,'little'))
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read)
    entry,args=(0x03802860,(SOURCE,DESTINATION,1,address)) if mediated else (address,(STATE,))
    if mediated:
        cpu.mem_write(0x038096c4,case['count'].to_bytes(4,'little'))
        state_address=0x038096c4
        snapshots=engine.snapshot(machine)
    else:state_address=STATE
    execution=machine['invoke'](entry,args,True,budget)
    if not execution['actualReturn']:return dict(actualReturn=False,execution=execution,postFaultStateExcluded=True)
    if not execution['actualReturn'] or len(entered)!=1 or modes!=[False] or reads!=[case['response']]:
        raise ValueError('Callback actual ARM invocation/return/readback contract differs')
    if mediated and machine['helperReturns'][address]!=1:raise ValueError('Indirect callback did not actually return to transfer caller')
    def put(target,size,value):
        for first,data in snapshots.items():
            if first<=target and target+size<=first+len(data):
                data[target-first:target-first+size]=value.to_bytes(size,'little');return
        raise ValueError('Callback model write escaped backing')
    if mediated:
        put(state_address,4,(case['count']-1)&0xffffffff)
        put(state_address+4,4,SOURCE);put(state_address+8,4,DESTINATION)
        put(IO,2,0 if case['count']==1 else 0xa040)
    put(IO+2,2,case['response'])
    if address==0x038028e4:
        put(DESTINATION,1,case['response']&255);put(state_address+8,4,DESTINATION+1)
    elif address==0x03802924:put(state_address+4,4,SOURCE+1)
    else:
        if (case['response']&255)!=case['source']:
            put(state_address+12,4,0)
            current=(case['count']-1)&0xffffffff if mediated else case['count']
            if current>1:put(state_address,4,1)
        put(state_address+4,4,SOURCE+1)
    if any(bytes(cpu.mem_read(first,len(data)))!=data for first,data in snapshots.items()):
        raise ValueError('Independent callback complete nonstack memory model differs')
    return dict(address=hex(address),case=case,seed=seed,callerMediated=mediated,execution=execution,
        actualReturn=True,callbackEntryMode='arm',callbackReturnLinks=[hex(value) for value in entered],
        actualNestedReturns={hex(key):value for key,value in machine['helperReturns'].items()},
        independentCompleteMappedMemoryModel=True,syntheticSpiReadback=case['response'],physicalHardwareCredit=0,
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()})

