import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
BASE=0x027e0000
STACK=0x03030000
INPUT=0x03040000
STOP=0x0f000000
ENTRIES=(0x027f6ca0,0x027f6db0)


def cases():
    values=(0,0xffffffff,0x80000000,0x7fffffff,0x55555555,0xaaaaaaaa,0x12345678,0x89abcdef)
    rows=[dict(word=(background&~0x7f00)|(code<<8)|(flag<<14))for code,flag,background in itertools.product(range(64),(0,1),values)]
    return rows+[dict(word=(0xa5a50000&~0x7f00)|(((37*i)&63)<<8)|((i&1)<<14)|i)for i in range(256)]


def model(entry,word):
    code=(word>>8)&63;flag=(word>>14)&1;changed=True;default=False
    if entry==ENTRIES[0]:
        if code in list(range(10))+[16,17]:value=word&~0x4000
        elif code in list(range(18,26))+[34,35]:value=((word|0x4000)&~0x3f00)|(((code-18)&63)<<8)
        elif code in(32,33):value=((word|0x4000)&~0x3f00)|(((code-24)&63)<<8)
        else:value=word&~0x7f00;default=True
    else:
        if code in list(range(10))+[16,17]:
            changed=bool(flag);value=(word&~0x3f00)|(((code+(24 if code in(8,9)else 18))&63)<<8)if flag else word
        elif code in list(range(18,26))+list(range(32,36)):value=word|0x4000
        else:value=word&~0x7f00;default=True
    flags=(4 if not flag else 0)if entry==ENTRIES[1]and code in list(range(10))+[16,17]else(8 if code<35 else 6 if code==35 else 2)
    return dict(value=value&0xffffffff,write=changed,reads=2 if default else 1,flags=flags,code=code,flag=flag,default=default)


def execute(original,entry,code,case,index,budget=200,allow_no_return=False):
    rng=random.Random(entry*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(BASE,0x20000);cpu.mem_write(BASE,original);cpu.mem_write(entry,code);before=bytes(cpu.mem_read(BASE,0x20000));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,rng.randbytes(4096));stack_before=bytes(cpu.mem_read(STACK,4096));cpu.mem_map(INPUT,4096);cpu.mem_write(INPUT,rng.randbytes(4096));pointer=INPUT+(0,4,8,252,1020,4092)[index%6];cpu.mem_write(pointer,struct.pack('<I',case['word']));input_before=bytes(cpu.mem_read(INPUT,4096));cpu.mem_map(STOP,4096)
    mode=0x10|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|mode);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=pointer;initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    returned=False;writes=[];reads=[];visited=[]
    def instruction(machine,address,width,user):
        nonlocal returned
        if address==STOP:returned=True;machine.emu_stop();return
        if not entry<=address<entry+272 or address%4:raise ValueError('Bitfield routine fetched outside complete ARM body/table')
        visited.append(address)
    def write(machine,access,address,width,value,user):
        if address!=pointer or width!=4:raise ValueError('Bitfield routine wrote outside measured word view')
        writes.append([address,width,value&0xffffffff])
    def read(machine,access,address,width,value,user):
        if address!=pointer or width!=4:raise ValueError('Bitfield routine read outside measured word view')
        reads.append([address,width])
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualNestedReturns=0,instructionCount=len(visited),postStateCredit=0,returnCredit=0)
        raise ValueError('Bounded bitfield routine did not return')
    expected=model(entry,case['word']);input_expected=bytearray(input_before);struct.pack_into('<I',input_expected,pointer-INPUT,expected['value']);abi=cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,13))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode
    checks=dict(abi=abi,rawInputAddressReturn=cpu.reg_read(REGISTERS[0])==pointer,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==expected['flags'],writes=writes==([[pointer,4,expected['value']]]if expected['write']else[]),reads=reads==[[pointer,4]]*expected['reads'],ram=bytes(cpu.mem_read(BASE,0x20000))==before,stack=bytes(cpu.mem_read(STACK,4096))==stack_before,input=bytes(cpu.mem_read(INPUT,4096))==bytes(input_expected))
    return dict(actualOwnReturn=True,actualNestedReturns=0,modelPassed=all(checks.values()),modelChecks=checks,wordBefore=case['word'],wordAfter=struct.unpack('<I',cpu.mem_read(pointer,4))[0],independentWordModel=expected,rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x20000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),inputSha256=hashlib.sha256(cpu.mem_read(INPUT,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,visited=sorted(set(visited)),providerReplacements=[],physicalHardwareContextProven=False)
