import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR

ENTRY=0x027E0564
BASE=0x027E0000
STATE=0x027F8DD8
STACK=0x03030000
STOP=0x0F000000


def execute(original,code,index,budget=2000):
    rng=random.Random(ENTRY*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE,0x20000);cpu.mem_write(BASE,original);cpu.mem_write(ENTRY,code)
    context=bytearray(rng.randbytes(128))
    if index%16==0:context[:]=bytes(128)
    if index%16==1:context[:]=bytes([255])*128
    cpu.mem_write(STATE-32,bytes(context));before=bytearray(cpu.mem_read(BASE,0x20000));expected=bytearray(before)
    fill_value=index&255;expected[STATE-BASE:STATE+32-BASE]=bytes([fill_value])*32;struct.pack_into('<I',expected,STATE+32-BASE,0)
    cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xA5])*4096);cpu.mem_map(STOP,4096)
    control=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|control)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=fill_value;initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    writes=[];reads=[];visited=[];stopped=False
    def instruction(machine,address,width,user):
        nonlocal stopped
        if address==STOP:stopped=True;machine.emu_stop();return
        if not ENTRY<=address<ENTRY+len(code)-8:raise ValueError('Initializer executed outside its code range or entered a literal')
        visited.append(address)
    def write(machine,access,address,width,value,user):
        if not(STATE<=address and address+width<=STATE+36):raise ValueError('Initializer write escaped the measured state prefix')
        writes.append([address,width,value&((1<<(width*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_MEM_READ,lambda machine,access,address,width,value,user:reads.append([address,width]))
    cpu.emu_start(ENTRY,STOP+4,count=budget)
    if not stopped or cpu.reg_read(REGISTERS[-2])!=STACK+0x800:raise ValueError('Initializer did not return')
    if any(cpu.reg_read(REGISTERS[i])!=initial[i]for i in range(4,12))or cpu.reg_read(UC_ARM_REG_CPSR)&0xDF!=control:raise ValueError('Initializer callee-save/control ABI differs')
    if bytes(cpu.mem_read(STACK,4096))!=bytes([0xA5])*4096:raise ValueError('Leaf initializer changed its stack')
    actual=bytes(cpu.mem_read(BASE,0x20000));actual_result=cpu.reg_read(REGISTERS[0])
    expected_writes=[[STATE+i,1,fill_value]for i in range(32)]+[[STATE+32,4,0]]
    return dict(modelPassed=actual==bytes(expected)and actual_result==0x027F8884 and writes==expected_writes,
        actualOwnReturn=True,result=actual_result,rawRegisters=[cpu.reg_read(reg)for reg in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
        mappedMemorySha256=hashlib.sha256(actual).hexdigest(),expectedMappedMemorySha256=hashlib.sha256(expected).hexdigest(),
        orderedWrites=writes,orderedReads=reads,visited=sorted(set(visited)),instructionCount=len(visited),providerReplacements=[])
