import hashlib
import random
from pathlib import Path
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_INTR,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC

ROOT=Path(__file__).resolve().parent
BASE,STACK,RETURN=0x037F8000,0x023E0000,0x023FF000
ADDRESS,CODE,SIZE=0x037FECAC,284,288
MASK64=(1 << 64)-1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def signed(value):
    value &= 0xFFFFFFFF
    return value-0x100000000 if value & 0x80000000 else value


def expected(case):
    octave,index=divmod(-signed(case['pitch']),768)
    result=((case['service']+65536)*(signed(case['timer']) & MASK64)) & MASK64
    shift=octave-16
    if shift<=0:
        if -shift>=64:
            raise ValueError('Right-shift domain is outside defined source arithmetic')
        result >>= -shift
    elif shift<32:
        if result & ((MASK64 << (32-shift)) & MASK64):
            return 65535,index
        result=(result << shift) & MASK64
    else:
        return 65535,index
    return max(16,min(65535,result)),index


def cases():
    return [dict(timer=timer,pitch=pitch,service=service) for timer in
        (0,1,15,16,127,65535,0x7FFFFFFF,0x80000000,0xFFFFFFFF)
        for pitch in (-36864,-36096,-24576,-13056,-12288,-768,-1,0,1,768,12288,24576,36000)
        for service in (0,1,32767,65535)]


def execute(body,case,seed,budget=10000):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZE:
        raise ValueError('Current measured timer module/extent differs')
    wram=bytearray(0x14000)
    wram[:len(raw)]=raw
    wram[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    stack=random.Random(seed+20261030).randbytes(0x4000)
    for base,data in ((BASE,bytes(wram)),(STACK,stack),(RETURN,bytes(0x1000))):
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    visited,services,writes=set(),[],[]
    state=dict(lastPc=None,externalFailure=None,veneerReturns=0)
    def code(machine,pc,size,unused):
        thumb=bool(machine.reg_read(UC_ARM_REG_CPSR)&32)
        valid=(ADDRESS<=pc<ADDRESS+CODE and not thumb) or (0x037FEDCC<=pc<0x037FEDD4 and not thumb) or (0x03803828<=pc<0x0380382C and thumb)
        if not valid:
            raise ValueError('Timer escaped its measured ARM/Thumb source and service veneer')
        if pc==0x037FECE8:
            state['veneerReturns']+=1
        state['lastPc']=pc
        visited.add(pc)
    def interrupt(machine,number,unused):
        if state['lastPc']!=0x03803828 or bytes(machine.mem_read(0x03803828,2))!=bytes.fromhex('1bdf'):
            raise ValueError('Unqualified architectural service')
        if case['service'] is None:
            state['externalFailure']='Original BIOS pitch-table implementation is not provided'
            machine.emu_stop()
            return
        if not 0<=case['service']<=65535:
            raise ValueError('Synthetic pitch-table output exceeds declared halfword contract')
        argument=machine.reg_read(match_runtime.REGISTERS[0])
        if not 0<=argument<=767:
            raise ValueError('Original service index escaped measured normalization')
        services.append([27,argument,case['service']])
        machine.reg_write(match_runtime.REGISTERS[0],case['service'])
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value & ((1 << size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_INTR,interrupt)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    registers=[random.Random(seed*31+i+117).getrandbits(32) for i in range(15)]
    registers[:2]=[case['timer'] & 0xFFFFFFFF,case['pitch'] & 0xFFFFFFFF]
    registers[-2:]=[STACK+0x3F00,RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR,(seed%16)<<28 | 0xD3)
    for register,value in zip(match_runtime.REGISTERS,registers):
        cpu.reg_write(register,value)
    fault=None
    try:
        cpu.emu_start(ADDRESS,RETURN,count=budget,timeout=100000)
    except UcError as error:
        fault=error.errno
    returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN
    actual=[cpu.reg_read(r) for r in match_runtime.REGISTERS]
    if returned:
        value,index=expected(case)
        if actual[0]!=value or services!=[[27,index,case['service']]] or state['veneerReturns']!=1:
            raise ValueError('Independent signed-input/unsigned64 product/shift/clamp or service contract differs: '+repr((case,actual[0],value,services,index)))
        if actual[4:12]!=registers[4:12] or actual[-2:]!=registers[-2:]:
            raise ValueError('Timer saved-register/actual-return ABI differs')
        if bytes(cpu.mem_read(BASE,len(wram)))!=bytes(wram) or any(not STACK<=a<STACK+0x4000 for a,n,v in writes):
            raise ValueError('Timer unexpectedly changes non-stack state')
    return dict(actualReturn=returned,fault=fault,externalFailure=state['externalFailure'],registers=actual,
        cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),services=services,actualVeneerReturns=state['veneerReturns'],
        writes=writes,stackSha256=digest(bytes(cpu.mem_read(STACK,len(stack)))),wramSha256=digest(bytes(cpu.mem_read(BASE,len(wram)))),
        visited=sorted(visited),originalBiosExecutionCredit=0)
