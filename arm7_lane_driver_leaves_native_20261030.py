import random
import hashlib
from pathlib import Path
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC

ROOT=Path(__file__).resolve().parent
BASE,STACK,RETURN,MMIO=0x037F8000,0x023E0000,0x023FF000,0x04000000
SIZES={0x037FEA20:40,0x037FEAC0:24}
RAW_SHA='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address):
    if address==0x037FEA20:
        return [dict(channel=c,value=v,control=w,passes=2) for c in range(16)
            for v in (0,1,2,0xFFFFFFFF) for w in (0,1,0x8000,0x80000000,0x80008000,0xFFFFFFFF)]
    return [dict(channel=c,value=v,control=0xA5A55A5A,passes=2) for c in range(16)
        for v in (0,1,16,65535,65536,0x7FFFFFFF,0x80000000,0xFFFFFFFF)]


def execute(address,body,case,seed,budget=10000):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!=RAW_SHA or len(body)!=SIZES[address]:
        raise ValueError('Measured driver input/complete extent changed')
    wram=bytearray(0x14000)
    wram[:len(raw)]=raw
    wram[address-BASE:address-BASE+len(body)]=body
    io=bytearray(random.Random(seed+20261030).randbytes(0x2000))
    offset=0x400+case['channel']*16
    io[offset:offset+4]=case['control'].to_bytes(4,'little')
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    initial={BASE:bytes(wram),STACK:random.Random(seed+131).randbytes(0x4000),RETURN:bytes(0x1000),MMIO:bytes(io)}
    for base,data in initial.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    visited,writes=set(),[]
    def code(machine,pc,size,unused):
        if not address<=pc<address+len(body) or machine.reg_read(UC_ARM_REG_CPSR)&32:
            raise ValueError('Driver leaf escaped qualified ARM instructions')
        visited.add(pc)
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value & ((1 << size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    records=[]
    for phase in range(case['passes']):
        registers=[random.Random(seed+phase*101+i).getrandbits(32) for i in range(15)]
        registers[:2]=[case['channel'],case['value']]
        registers[-2:]=[STACK+0x3F00,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,(seed%16)<<28 | 0xD3)
        for register,value in zip(match_runtime.REGISTERS,registers):
            cpu.reg_write(register,value)
        first=len(writes)
        fault=None
        try:
            cpu.emu_start(address,RETURN,count=budget,timeout=100000)
        except UcError as error:
            fault=error.errno
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN
        actual=[cpu.reg_read(r) for r in match_runtime.REGISTERS]
        if returned:
            if address==0x037FEA20:
                old=int.from_bytes(io[offset:offset+4],'little')
                value=(old & 0x7FFFFFFF) | (0x8000 if case['value'] & 1 else 0)
                expected=[[MMIO+offset,4,value]]
                io[offset:offset+4]=value.to_bytes(4,'little')
            else:
                value=(65536-case['value']) & 65535
                expected=[[MMIO+offset+8,2,value]]
                io[offset+8:offset+10]=value.to_bytes(2,'little')
            if writes[first:]!=expected or bytes(cpu.mem_read(MMIO,0x2000))!=bytes(io):
                raise ValueError('Independent MMIO width/order/value or guard preservation differs')
            if actual[4:12]!=registers[4:12] or actual[-2:]!=registers[-2:]:
                raise ValueError('Driver leaf saved-register or true return ABI differs')
            for base in (BASE,STACK,RETURN):
                if bytes(cpu.mem_read(base,len(initial[base])))!=initial[base]:
                    raise ValueError('Driver leaf changed non-I/O memory')
        records.append(dict(actualReturn=returned,fault=fault,pc=cpu.reg_read(UC_ARM_REG_PC),registers=actual,
            cpsr=cpu.reg_read(UC_ARM_REG_CPSR),writes=writes[first:],memoryHashes={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in initial.items()}))
        if not returned:
            break
    return dict(states=records,visited=sorted(visited),providerReplacements=[])
