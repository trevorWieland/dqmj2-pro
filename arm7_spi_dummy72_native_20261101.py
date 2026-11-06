import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
BASE=0x037f8000
CONTROL=0x040001c0
DATA=CONTROL+2
STACK=0x03030000
STOP=0x0f000000
ENTRIES=(0x03803e3c,0x03804498)


def cases():
    values=[0,1,0x7f,0x80,255,256,0x1234,0x8000,65535]+[(i<<8)|((73*i+11)&255)for i in range(256)]
    return [dict(status=value,busy=busy)for value,busy in itertools.product(values,(0,1,3))]


def execute(original,entry,code,case,index,budget=1000,allow_no_return=False):
    rng=random.Random(entry*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(BASE,0x20000);cpu.mem_write(BASE,original);cpu.mem_write(entry,code);before=bytes(cpu.mem_read(BASE,0x20000));cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04000000,4096));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,rng.randbytes(4096));stack_before=bytes(cpu.mem_read(STACK,4096));cpu.mem_map(STOP,4096)
    mode=0x10|((index%4)<<6);flags=index%16;cpu.reg_write(UC_ARM_REG_CPSR,(flags<<28)|mode);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    returned=False;writes=[];reads=[];supplied=[];visited=[];poll=0
    def instruction(machine,address,width,user):
        nonlocal returned
        if address==STOP:returned=True;machine.emu_stop();return
        if not entry<=address<entry+32 or address%4:raise ValueError('Dummy transfer fetched outside complete ARM code')
        visited.append(address)
    def write(machine,access,address,width,value,user):
        if address!=DATA or width!=2:raise ValueError('Dummy transfer wrote outside its measured halfword port')
        writes.append([address,width,value&65535])
    def read(machine,access,address,width,value,user):
        nonlocal poll
        reads.append([address,width])
        if address==CONTROL and width==2:
            raw=(case['status']&~0x80)|(0x80 if poll<case['busy']or case.get('stuck')else 0);poll+=1;supplied.append(raw);machine.mem_write(CONTROL,struct.pack('<H',raw))
        elif address==entry+32 and width==4:pass
        else:raise ValueError('Dummy transfer read outside its measured pool or halfword port')
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualNestedReturns=0,instructionCount=len(visited),busyPortReached=bool(supplied),postStateCredit=0,returnCredit=0)
        raise ValueError('Bounded dummy transfer did not actually return')
    result=case['status']&~0x80;expected_io=bytearray(io_before);struct.pack_into('<HH',expected_io,0x1c0,result,0);expected_supply=[result|0x80]*case['busy']+[result];abi=cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(2,13))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode
    checks=dict(abi=abi,result=cpu.reg_read(REGISTERS[0])==result,scratchControlAddress=cpu.reg_read(REGISTERS[1])==CONTROL,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==((flags&3)|4),writes=writes==[[DATA,2,0]],reads=reads==[[entry+32,4]]+[[CONTROL,2]]*(case['busy']+1),supplied=supplied==expected_supply,ram=bytes(cpu.mem_read(BASE,0x20000))==before,stack=bytes(cpu.mem_read(STACK,4096))==stack_before,io=bytes(cpu.mem_read(0x04000000,4096))==bytes(expected_io))
    return dict(actualOwnReturn=True,actualNestedReturns=0,modelPassed=all(checks.values()),modelChecks=checks,rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x20000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,suppliedHalfwords=supplied,visited=sorted(set(visited)),providerReplacements=[],physicalPeripheralExecution=False)
