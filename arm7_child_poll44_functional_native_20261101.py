import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
BASE=0x037f8000
ENTRY=0x037fb78c
PORT=0x0480819c
STACK=0x03030000
STOP=0x0f000000


def cases():
    rows=[dict(background=b,readyAfter=n)for b,n in itertools.product((0,1,0x7f,255,256,0x1234,0x8000,65535,0xaa55),(0,1,2,7,31,127,3998,3999,4000,None))]
    return rows+[dict(background=(i<<8)|((73*i+11)&255),readyAfter=(0,1,2,7,None)[i%5])for i in range(256)]


def execute(original,code,case,index,budget=30000,allow_no_return=False):
    rng=random.Random(ENTRY*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(BASE,0x20000);cpu.mem_write(BASE,original);cpu.mem_write(ENTRY,code);before=bytes(cpu.mem_read(BASE,0x20000));cpu.mem_map(0x04808000,4096);cpu.mem_write(0x04808000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04808000,4096));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,rng.randbytes(4096));stack_before=bytes(cpu.mem_read(STACK,4096));cpu.mem_map(STOP,4096);mode=0x10|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|mode);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    returned=False;writes=[];reads=[];supplied=[];visited=[]
    def instruction(machine,address,width,user):
        nonlocal returned
        if address==STOP:returned=True;machine.emu_stop();return
        if not ENTRY<=address<ENTRY+40 or address%4:raise ValueError('Bounded poll fetched outside its complete ARM code')
        visited.append(address)
    def write(machine,access,address,width,value,user):raise ValueError('Bounded poll performed an original write')
    def read(machine,access,address,width,value,user):
        reads.append([address,width])
        if address==PORT and width==2:
            after=case['readyAfter'];raw=(case['background']&~0x80)|(0x80 if after is not None and len(supplied)>=after else 0);supplied.append(raw);machine.mem_write(PORT,struct.pack('<H',raw))
        elif address==ENTRY+40 and width==4:pass
        else:raise ValueError('Bounded poll read outside measured pool or halfword port')
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(ENTRY,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualNestedReturns=0,instructionCount=len(visited),postStateCredit=0,returnCredit=0)
        raise ValueError('Finite poll did not actually return within explicit budget')
    after=case['readyAfter'];positive=after is not None and after<4000;count=after+1 if positive else 4000;result=128 if positive else 0;remaining=4001-count if positive else 0;expected_supply=[case['background']&~0x80]*count
    if positive:expected_supply[-1]|=0x80
    expected_io=bytearray(io_before);struct.pack_into('<H',expected_io,0x19c,expected_supply[-1]);abi=cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(3,13))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode;checks=dict(abi=abi,result=cpu.reg_read(REGISTERS[0])==result,portAddress=cpu.reg_read(REGISTERS[1])==PORT,remaining=cpu.reg_read(REGISTERS[2])==remaining,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==(2 if positive else 6),reads=reads==[[ENTRY+40,4]]+[[PORT,2]]*count,supplied=supplied==expected_supply,ram=bytes(cpu.mem_read(BASE,0x20000))==before,stack=bytes(cpu.mem_read(STACK,4096))==stack_before,io=bytes(cpu.mem_read(0x04808000,4096))==bytes(expected_io));projection=bytearray(cpu.mem_read(BASE,0x20000));projection[ENTRY-BASE:ENTRY-BASE+44]=original[ENTRY-BASE:ENTRY-BASE+44]
    return dict(actualOwnReturn=True,actualNestedReturns=0,modelPassed=all(checks.values()),modelChecks=checks,rawResult=cpu.reg_read(REGISTERS[0]),readCount=len(supplied),limitExhausted=not positive,rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),nonCodeRamSha256=hashlib.sha256(projection).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04808000,4096)).hexdigest(),orderedReads=reads,orderedWrites=writes,suppliedHalfwords=supplied,visited=sorted(set(visited)),instructionCount=len(visited),providerReplacements=[],physicalHardwareOrTimingProven=False)
