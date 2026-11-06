import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
ENTRY=0x03804C00
HELPER=0x03804C58
BASE=0x037F8000
CONTROL=0x040001C0
DATA=CONTROL+2
STACK=0x03030000
STOP=0x0F000000
VALUES=(0,1,127,128,255,256,0x12345678,0x80000000,0xffffffff)
def cases():
    matrix=[dict(selector=a,value=b,busyBefore=x,busyNested=y,stickyBefore=(0,0x4002,0xff7f)[(x+y)%3],stickyNested=(0,0x8802,0x7f7f)[(x+2*y)%3])for a,b,(x,y)in itertools.product(VALUES,VALUES,((0,0),(0,3),(2,0),(1,2)))]
    return matrix+[dict(selector=0x12340000|i,value=0xf0000000|((73*i+19)&255),busyBefore=i%3,busyNested=(i//3)%4,stickyBefore=0xff7f,stickyNested=0x8802)for i in range(256)]

def execute(original,code,case,index,budget=5000,allow_no_return=False):
    rng=random.Random(ENTRY*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE,0x18000);cpu.mem_write(BASE,original);cpu.mem_write(ENTRY,code)
    cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04000000,4096))
    before=bytes(cpu.mem_read(BASE,0x18000));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(STOP,4096)
    control=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|control)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0:2]=[case['selector'],case['value']];initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    writes=[];reads=[];supplied=[];own_visited=[];nested_visited=[];nested=[];pending=None;returned=False;phase=0;poll=0
    def instruction(machine,address,width,user):
        nonlocal returned,pending
        if address==STOP:returned=True;machine.emu_stop();return
        if pending is not None and address==pending['lr']:
            pending['observedReturn']=machine.reg_read(REGISTERS[0]);pending['actualReturn']=True
            pending['abiPreserved']=machine.reg_read(REGISTERS[-2])==pending['sp']and [machine.reg_read(x)for x in REGISTERS[4:12]]==pending['saved']
            nested.append(pending);pending=None
        if address==HELPER:
            pending=dict(argument=machine.reg_read(REGISTERS[0]),lr=machine.reg_read(REGISTERS[-1]),sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(x)for x in REGISTERS[4:12]])
        if ENTRY<=address<ENTRY+76:own_visited.append(address)
        elif HELPER<=address<HELPER+32:nested_visited.append(address)
        else:raise ValueError('Register routine entered a literal, original tail or external provider')
    def write(machine,access,address,width,value,user):
        nonlocal phase,poll
        if address in (CONTROL,DATA)and width==2:
            writes.append([address,width,value&65535])
            if address==DATA:phase+=1;poll=0
        elif STACK+0x7f8<=address and address+width<=STACK+0x800 and width==4:writes.append([address,width,value&0xffffffff])
        else:raise ValueError('Register routine write escaped modeled stack/halfword ports')
    def read(machine,access,address,width,value,user):
        nonlocal poll
        reads.append([address,width])
        if address==CONTROL and width==2:
            key='Before'if phase==0 else'Nested';busy=case['busy'+key];sticky=case['sticky'+key]&~0x80
            raw=sticky|(0x80 if poll<busy or case.get('stuck')==key else 0);poll+=1
            supplied.append(dict(phase=phase,value=raw));machine.mem_write(CONTROL,struct.pack('<H',raw))
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.emu_start(ENTRY,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualNestedReturns=len(nested),instructionCount=len(own_visited)+len(nested_visited),postStateCredit=0,returnCredit=0)
        raise ValueError('Bounded register routine did not return')
    expected_stack=bytearray(bytes([0xa5])*4096);struct.pack_into('<II',expected_stack,0x7f8,initial[4],initial[-1])
    expected_io=bytearray(io_before);struct.pack_into('<HH',expected_io,0x1c0,0x8002,case['value']&255)
    expected_writes=[[STACK+0x7f8,4,initial[4]],[STACK+0x7fc,4,initial[-1]],[CONTROL,2,0x8202],[CONTROL,2,0x8802],[DATA,2,case['selector']&255],[CONTROL,2,0x8002],[DATA,2,case['value']&255]]
    expected_supply=[dict(phase=phase,value=(case['sticky'+key]&~0x80)|(0x80 if i<case['busy'+key]else 0))for phase,key in [(0,'Before'),(1,'Nested')]for i in range(case['busy'+key]+1)]
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==control
    lower=len(nested)==1 and nested[0]['argument']==case['selector']&255 and nested[0]['observedReturn']==case['stickyNested']&~0x80 and nested[0]['abiPreserved']
    model=abi and lower and writes==expected_writes and supplied==expected_supply and bytes(cpu.mem_read(BASE,0x18000))==before and bytes(cpu.mem_read(STACK,4096))==bytes(expected_stack)and bytes(cpu.mem_read(0x04000000,4096))==bytes(expected_io)and cpu.reg_read(REGISTERS[0])==case['value']&255
    return dict(modelPassed=model,actualOwnReturn=True,actualNestedReturns=len(nested),sourceCalleeCredit=0,nested=nested,
        result=cpu.reg_read(REGISTERS[0]),rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
        ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x18000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),
        orderedWrites=writes,orderedReads=reads,suppliedHalfwordInputs=supplied,visitedOwn=sorted(set(own_visited)),visitedNested=sorted(set(nested_visited)),instructionCount=len(own_visited)+len(nested_visited),
        functionProvidersReplaced=[],physicalPeripheralExecution=False)
