import random
import hashlib
from pathlib import Path
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,STACK,RETURN=0x037F8000,0x023E0000,0x023FF000
ADDRESS,SIZE,CODE=0x037FDDCC,76,68
PREVIOUS,COUNTER=0x03805B78,0x03805B7C
RANGES={ADDRESS:CODE,0x037FE41C:20,0x037FE430:24}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def signed(value):
    return value-0x100000000 if value&0x80000000 else value


def cases():
    values=(0,1,261,262,65535,0x7FFFFFFF,0x80000000,0xFFFFFFFF)
    return [dict(sample=sample,previous=previous,counter=counter,irq=irq,passes=2)
        for sample in values for previous in values for counter in (0,1,0xFFFFFFFE,0xFFFFFFFF) for irq in (0,128)]


def execute(body,case,seed,budget=2000):
    path=ROOT/'extract/utility/runtime/utility-child-arm7-wram.bin'
    raw=path.read_bytes()
    if digest(raw)!='13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6' or len(body)!=SIZE:
        raise ValueError('Measured utility child WRAM/complete counter extent differs')
    wram=bytearray(0x18000)
    wram[:len(raw)]=raw
    wram[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    wram[PREVIOUS-BASE:PREVIOUS-BASE+4]=case['previous'].to_bytes(4,'little')
    wram[COUNTER-BASE:COUNTER-BASE+4]=case['counter'].to_bytes(4,'little')
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    stack=random.Random(seed+119).randbytes(0x4000)
    for first,data in ((BASE,bytes(wram)),(STACK,stack),(RETURN,bytes(0x1000))):
        cpu.mem_map(first,len(data))
        cpu.mem_write(first,data)
    visited,writes,frames=set(),[],[]
    returns={address:0 for address in RANGES}
    def code(machine,pc,size,unused):
        if not any(first<=pc<first+length for first,length in RANGES.items()) or machine.reg_read(UC_ARM_REG_CPSR)&32:
            raise ValueError('Counter escaped qualified utility-child ARM source/helper code')
        while frames and pc==frames[-1][1]:
            returns[frames.pop()[0]]+=1
        if pc in RANGES:
            frames.append((pc,machine.reg_read(match_runtime.REGISTERS[-1])))
        visited.add(pc)
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1 << size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    records=[]
    previous,counter=case['previous'],case['counter']
    for phase in range(case['passes']):
        sample=case['sample']
        expected=[]
        if signed(sample)<signed(previous):
            counter=(counter+1)&0xFFFFFFFF
            expected.append([COUNTER,4,counter])
            wram[COUNTER-BASE:COUNTER-BASE+4]=counter.to_bytes(4,'little')
        expected.append([PREVIOUS,4,sample])
        wram[PREVIOUS-BASE:PREVIOUS-BASE+4]=sample.to_bytes(4,'little')
        difference=(sample-previous)&0xFFFFFFFF
        flags=(difference&0x80000000)|(int(difference==0)<<30)|(int(sample>=previous)<<29)|(((sample^previous)&(sample^difference)&0x80000000)>>3)
        registers=[random.Random(seed*17+phase*119+i).getrandbits(32) for i in range(15)]
        registers[0]=sample
        registers[-2:]=[STACK+0x3F00,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,(seed%16)<<28 | 0x53 | case['irq'])
        for register,value in zip(match_runtime.REGISTERS,registers):
            cpu.reg_write(register,value)
        first=len(writes)
        before=dict(returns)
        frames.clear()
        fault=None
        try:
            cpu.emu_start(ADDRESS,RETURN,count=budget,timeout=100000)
        except UcError as error:
            fault=error.errno
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN
        actual=[cpu.reg_read(r) for r in match_runtime.REGISTERS]
        if returned:
            while frames and frames[-1][1]==RETURN:
                returns[frames.pop()[0]]+=1
            effects=[row for row in writes[first:] if not STACK<=row[0]<STACK+0x4000]
            if actual[0]!=counter or effects!=expected or bytes(cpu.mem_read(BASE,len(wram)))!=bytes(wram):
                raise ValueError('Independent signed-compare/u32 wrap/store/full-WRAM model differs')
            if cpu.reg_read(UC_ARM_REG_CPSR)&0xF0000080!=flags|case['irq']:
                raise ValueError('Independent CMP N/Z/C/V and IRQ preservation differ')
            if actual[4:12]!=registers[4:12] or actual[-2:]!=registers[-2:] or frames:
                raise ValueError('Counter actual-return/saved-register/nested ABI differs')
        records.append(dict(actualReturn=returned,fault=fault,pc=cpu.reg_read(UC_ARM_REG_PC),registers=actual,
            cpsr=cpu.reg_read(UC_ARM_REG_CPSR),writes=writes[first:],actualFunctionReturns={hex(a):returns[a]-before[a] for a in RANGES},
            stackSha256=digest(bytes(cpu.mem_read(STACK,len(stack)))),wramSha256=digest(bytes(cpu.mem_read(BASE,len(wram))))))
        previous=sample
        if not returned:
            break
    return dict(states=records,visited=sorted(visited),providerCalls=0,sourceCredit=0)
