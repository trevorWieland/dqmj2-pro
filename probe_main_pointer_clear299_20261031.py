import hashlib
import json
import random
import match_runtime
from link_runtime_unit import measured_module
from project import ROOT,configuration,sha256,write_json
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM
from unicorn.arm_const import *
ENTRY,STOP,BUFFER=0x020485B4,0x08000000,0x023F0000
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]

def run():
    config=configuration()
    if sha256(config['rom'])!=config['romSha256']:
        raise ValueError('Pointer299 measured private ROM differs')
    meta,main,_=measured_module('main')
    results=[]
    for seed in range(16):
        rng=random.Random(299000+seed)
        payload=rng.randbytes(32)
        values=[rng.getrandbits(32)for r in REGS]
        for pointer in[0,BUFFER+8]:
            for incoming in[0,1,2,0x7FFFFFFF,0x80000000,0xFFFFFFFF,0x12345678,rng.getrandbits(32)]:
                vm=Uc(UC_ARCH_ARM,UC_MODE_ARM)
                vm.ctl_set_cpu_model(UC_CPU_ARM_946)
                vm.mem_map(0x02000000,0x400000)
                vm.mem_map(0x03000000,0x20000)
                vm.mem_map(STOP,0x1000)
                vm.mem_write(0x02000000,main)
                vm.mem_write(BUFFER,payload)
                expected=bytearray(vm.mem_read(0x02000000,0x400000))
                if pointer:
                    expected[pointer-0x02000000:pointer-0x02000000+8]=bytes(8)
                for r,v in zip(REGS,values):
                    vm.reg_write(r,v)
                vm.reg_write(REGS[0],pointer)
                vm.reg_write(REGS[1],incoming)
                vm.reg_write(UC_ARM_REG_CPSR,seed%16<<28|0x10)
                vm.reg_write(UC_ARM_REG_SP,0x0301FF00)
                vm.reg_write(UC_ARM_REG_LR,STOP)
                vm.emu_start(ENTRY,STOP,count=10)
                actual=[vm.reg_read(r)for r in REGS]
                if vm.reg_read(UC_ARM_REG_PC)!=STOP or vm.reg_read(UC_ARM_REG_SP)!=0x0301FF00 or actual[0]!=pointer or actual[1]!=(0 if pointer else incoming)or actual[4:12]!=values[4:12]or bytes(vm.mem_read(0x02000000,0x400000))!=expected:
                    raise ValueError('Pointer299 independent return/frame/RAM differs')
                results.append(dict(seed=seed,pointer=hex(pointer),incomingR1=hex(incoming),returnR0=hex(actual[0]),physicalR1After=hex(actual[1]),actualReturn=True,ramSha256=hashlib.sha256(expected).hexdigest()))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',mode='arm',address=hex(ENTRY),bytes=20,moduleSha256=meta['sha256'],nativeSpanSha256=hashlib.sha256(main[ENTRY-0x02000000:ENTRY-0x02000000+20]).hexdigest(),actualReturns=len(results),instructionBound=10,freshMachinePerExecution=True,providers=0,sourceCredit=0,results=results,generatorSha256=sha256(__file__),interpretation='Correlated MOVNE/STRNE ensure incomingR1 never changes RAM or returnR0; the null path preserves incidentalR1 and the nonnull path defines it as0',limitations=['Native nullable pointer and aligned8-byte writable object fixtures only; no resource object/lifecycle meaning inferred','PhysicalR1After is not a semantic second return or evidence for a wide C return','Raw conservative incoming-mask review leads must not be treated as complete signatures','Accepted source and historical datasets remain unchanged'])
    write_json(ROOT/'evidence/verification/main-pointer-clear299-20261031.json',report)
    print(json.dumps(dict(actualReturns=len(results),sourceCredit=0)))

if __name__=='__main__':
    run()
