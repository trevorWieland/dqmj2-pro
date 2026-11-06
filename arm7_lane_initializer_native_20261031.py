import hashlib
import random
from pathlib import Path
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC

ROOT=Path(__file__).resolve().parent
BASE,STACK,RETURN=0x037F8000,0x023E0000,0x023FF000
ADDRESS,SIZE,CODE=0x037FF164,92,84
CHANNELS,MASKS=0x03807EE0,0x03807EB8


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    return [dict(flagBase=index*16,passes=2) for index in range(32)]


def execute(body,case,seed,budget=3000):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZE:
        raise ValueError('Initializer measured image or source extent differs')
    wram=bytearray(0x14000)
    wram[:len(raw)]=raw
    wram[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    wram[CHANNELS-BASE:CHANNELS-BASE+16*84]=random.Random(seed+271).randbytes(16*84)
    wram[MASKS-BASE:MASKS-BASE+8]=random.Random(seed+722).randbytes(8)
    for index in range(16):
        wram[CHANNELS-BASE+index*84+3]=(case['flagBase']+index)&255
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    stack=random.Random(seed+213).randbytes(0x4000)
    for first,data in ((BASE,bytes(wram)),(STACK,stack),(RETURN,bytes(0x1000))):
        cpu.mem_map(first,len(data))
        cpu.mem_write(first,data)
    visited,writes=set(),[]
    def code(machine,pc,size,unused):
        if not ADDRESS<=pc<ADDRESS+CODE or machine.reg_read(UC_ARM_REG_CPSR)&32:
            raise ValueError('Initializer escaped complete qualified ARM source body')
        visited.add(pc)
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1 << size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    records=[]
    for phase in range(case['passes']):
        expected=[]
        for index in range(16):
            first=CHANNELS-BASE+index*84
            flag=wram[first+3]&6
            expected.extend([[CHANNELS+index*84,1,index],[CHANNELS+index*84+3,1,flag]])
            wram[first],wram[first+3]=index,flag
        expected.extend([[MASKS+4,4,0],[MASKS,4,0]])
        wram[MASKS-BASE:MASKS-BASE+8]=bytes(8)
        registers=[random.Random(seed+phase*31+i).getrandbits(32) for i in range(15)]
        registers[-2:]=[STACK+0x3F00,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,seed%16 << 28 | 0xD3)
        for register,value in zip(match_runtime.REGISTERS,registers):
            cpu.reg_write(register,value)
        first_write=len(writes)
        fault=None
        try:
            cpu.emu_start(ADDRESS,RETURN,count=budget,timeout=100000)
        except UcError as error:
            fault=error.errno
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN
        actual=[cpu.reg_read(r) for r in match_runtime.REGISTERS]
        if returned:
            effects=[row for row in writes[first_write:] if not STACK<=row[0]<STACK+0x4000]
            if effects!=expected or bytes(cpu.mem_read(BASE,len(wram)))!=bytes(wram):
                raise ValueError('Independent initializer full-state/ordered-byte-store model differs')
            if actual[4:12]!=registers[4:12] or actual[-2:]!=registers[-2:]:
                raise ValueError('Initializer actual return/saved-register ABI differs')
        records.append(dict(actualReturn=returned,fault=fault,pc=cpu.reg_read(UC_ARM_REG_PC),registers=actual,
            cpsr=cpu.reg_read(UC_ARM_REG_CPSR),writes=writes[first_write:],
            stackSha256=digest(bytes(cpu.mem_read(STACK,len(stack)))),wramSha256=digest(bytes(cpu.mem_read(BASE,len(wram))))))
        if not returned:
            break
    return dict(states=records,visited=sorted(visited),providerCalls=0,sourceCredit=0)
