import hashlib
import random
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_CPSR,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from match_runtime import REGISTERS
from main_async_reader_models_20261031 import construct,ERROR,INIT,OPEN,SEEK,READ

ENTRY=0x0202A954
STACK=0x03030000
STOP=0x0F000000
SP=STACK+0xF00


def execute(main,case,candidate=None,check=True):
    model=construct(case);machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000,0x400000);machine.mem_write(0x02000000,main)
    machine.mem_map(STACK,4096);machine.mem_map(STOP,4096)
    if candidate is not None:
        assert len(candidate)==260;machine.mem_write(ENTRY,candidate)
    rng=random.Random(case['tag']^0xC170);stack=rng.randbytes(4096);machine.mem_write(STACK,stack)
    machine.mem_write(model['context'],model['initial']);machine.mem_write(ERROR,struct.pack('<I',model['oldError']))
    machine.mem_write(SP,struct.pack('<I',case['offset']))
    initial_stack=bytes(machine.mem_read(STACK,4096));expected=bytearray(machine.mem_read(0x02000000,0x400000))
    offset=model['context']-0x02000000;expected[offset:offset+84]=model['output'];struct.pack_into('<I',expected,ERROR-0x02000000,model['error'])
    machine.reg_write(UC_ARM_REG_CPSR,((case['tag']&15)<<28)|0x1F)
    values=[rng.getrandbits(32)for reg in REGISTERS]
    for reg,value in zip(REGISTERS,values):machine.reg_write(reg,value)
    for reg,value in zip(REGISTERS[:4],[0 if case['default']else model['context'],case['path'],case['buffer'],case['length']]):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,SP);machine.reg_write(UC_ARM_REG_LR,STOP|(case['tag']&1))
    saved=[machine.reg_read(reg)for reg in REGISTERS[4:12]];events=[];pending=None;pcs=set();writes=[]
    state=dict(actualTopReturns=0,actualInitializerReturns=0,providedCompletions=0,instructions=0)
    def code(uc,pc,width,user):
        nonlocal pending
        state['instructions']+=1
        if pending and pc==pending:
            assert bytes(uc.mem_read(model['file'],72))==model['initialized'];state['actualInitializerReturns']+=1;pending=None
        if pc==STOP:state['actualTopReturns']+=1;uc.emu_stop();return
        assert width==4 and not uc.reg_read(UC_ARM_REG_CPSR)&32
        if pc==INIT:
            assert not pending and uc.reg_read(REGISTERS[0])==model['file'];pending=uc.reg_read(UC_ARM_REG_LR)
        if ENTRY<=pc<ENTRY+252:pcs.add(pc);return
        if INIT<=pc<INIT+40:return
        assert pc in [OPEN,SEEK,READ] and len(events)<len(model['events'])
        event=model['events'][len(events)];args=[uc.reg_read(reg)for reg in REGISTERS[:len(event['args'])]]
        matched=pc==event['address'] and args==event['args'] and bytes(uc.mem_read(model['file'],72))==event['fileBefore'] and int.from_bytes(uc.mem_read(ERROR,4),'little')==event['errorBefore']
        if check:assert matched,(hex(pc),args,event['args'])
        events.append(dict(address=pc,args=args,matched=matched))
        uc.mem_write(model['file'],event['fileAfter']);uc.mem_write(ERROR,struct.pack('<I',event['errorAfter']))
        for index in [1,2,3,12]:uc.reg_write(REGISTERS[index],(case['tag']*131+0xE0000000+index*0x101)&0xFFFFFFFF)
        uc.reg_write(REGISTERS[0],event['result']);uc.reg_write(UC_ARM_REG_CPSR,(((case['tag']*3)&15)<<28)|0x1F)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR));state['providedCompletions']+=1
    def write(uc,access,address,size,value,user):
        assert SP-64<=address and address+size<=SP or model['context']<=address and address+size<=model['context']+84 or ERROR<=address and address+size<=ERROR+4
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_WRITE,write);machine.emu_start(ENTRY,STOP+4,count=1500)
    assert state['actualTopReturns']==1 and state['instructions']<1500 and not pending
    assert machine.reg_read(UC_ARM_REG_SP)==SP and [machine.reg_read(reg)for reg in REGISTERS[4:12]]==saved
    final_stack=bytes(machine.mem_read(STACK,4096));assert final_stack[:0xEC0]==initial_stack[:0xEC0] and final_stack[0xF00:]==initial_stack[0xF00:]
    ram=bytes(machine.mem_read(0x02000000,0x400000));passed=ram==bytes(expected) and machine.reg_read(REGISTERS[0])==model['result'] and all(event['matched']for event in events)
    if check:assert passed,case
    return dict(modelPassed=passed,returnWord=machine.reg_read(REGISTERS[0]),state=state,events=events,pcs=sorted(pcs),
        registers=[machine.reg_read(reg)for reg in REGISTERS]+[machine.reg_read(UC_ARM_REG_CPSR)],ramSha256=hashlib.sha256(ram).hexdigest(),
        stackSha256=hashlib.sha256(final_stack).hexdigest(),writes=writes)
