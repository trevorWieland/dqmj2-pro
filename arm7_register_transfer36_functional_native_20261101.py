import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
ENTRY=0x03804C58
BASE=0x037F8000
VIRTUAL=0x026A0000
CONTROL=0x040001C0
DATA=CONTROL+2
STACK=0x03030000
STOP=0x0F000000

def cases():
    values=[0x1234ab00|i for i in range(256)]+[0,1,127,128,255,256,0x12345678,0x80000000,0xffffffff]
    return [dict(selector=value,busy=busy,sticky=sticky)for value in values for busy in (0,1,3)for sticky in (0,0x8802,0xff7f)]

def execute(original,code,case,index,virtual=False,budget=2000,allow_no_return=False):
    rng=random.Random(ENTRY*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE,0x18000);cpu.mem_write(BASE,original);ram_before=bytes(cpu.mem_read(BASE,0x18000))
    entry=VIRTUAL if virtual else ENTRY
    if virtual:cpu.mem_map(VIRTUAL,4096);cpu.mem_write(VIRTUAL,code)
    else:cpu.mem_write(ENTRY,code)
    cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_expected=bytearray(cpu.mem_read(0x04000000,4096))
    struct.pack_into('<HH',io_expected,0x1c0,case['sticky']&~0x80,case['selector']&255)
    cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(STOP,4096)
    control=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|control)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=case['selector'];initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    writes=[];port_reads=[];visited=[];returned=False;poll=0
    def instruction(machine,address,width,user):
        nonlocal returned
        if address==STOP:returned=True;machine.emu_stop();return
        if not entry<=address<entry+len(code)-4:raise ValueError('Complete helper escaped its own generated/native code or fetched a literal')
        visited.append(address-entry)
    def write(machine,access,address,width,value,user):
        if address!=DATA or width!=2:raise ValueError('Helper write escaped the sole measured halfword port')
        writes.append([address,width,value&65535])
    def read(machine,access,address,width,value,user):
        nonlocal poll
        if address==CONTROL and width==2:
            value=(case['sticky']&~0x80)|(0x80 if poll<case['busy']or case.get('stuck')else 0);poll+=1
            port_reads.append([address,width,value]);machine.mem_write(CONTROL,struct.pack('<H',value))
        elif entry+len(code)-4<=address<entry+len(code)and width==4:pass
        else:raise ValueError('Helper read escaped control halfword or its own generated/native pool')
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualReturn=False,instructions=len(visited),returnCredit=0,postStateCredit=0)
        raise ValueError('Bounded helper did not return')
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==control
    expected_reads=[[CONTROL,2,(case['sticky']&~0x80)|(0x80 if i<case['busy']else 0)]for i in range(case['busy']+1)]
    functional=dict(result=cpu.reg_read(REGISTERS[0]),calleeSaved=[cpu.reg_read(x)for x in REGISTERS[4:12]],sp=cpu.reg_read(REGISTERS[-2]),lr=cpu.reg_read(REGISTERS[-1]),returnMode=cpu.reg_read(UC_ARM_REG_CPSR)&0xff,ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x18000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),orderedPortWrites=writes,orderedPortReads=port_reads)
    passed=abi and functional['result']==case['sticky']&~0x80 and writes==[[DATA,2,case['selector']&255]]and port_reads==expected_reads and bytes(cpu.mem_read(BASE,0x18000))==ram_before and bytes(cpu.mem_read(STACK,4096))==bytes([0xa5])*4096 and bytes(cpu.mem_read(0x04000000,4096))==bytes(io_expected)
    return dict(actualReturn=True,modelPassed=passed,functional=functional,internal=dict(rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),visitedOwnInstructionOffsets=sorted(set(visited)),instructionCount=len(visited)),physicalPeripheralExecution=False)
