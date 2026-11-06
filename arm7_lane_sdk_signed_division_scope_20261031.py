import json
import random
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT,sha256,write_json

BASE,ENTRY,FIRST,LAST,END,RETURN=0x037F8000,0x03806C38,0x03806CA8,0x03806E30,0x03806E44,0x022FF000
MODULE_SHA='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
SCOPE_SHA='e8183a62ffe6a54210cd7d025b01431ff792025c1b45a0e8537abd8cec16ccfb'


def validate_scope(raw):
    from hashlib import sha256 as digest
    if digest(raw).hexdigest()!=MODULE_SHA or digest(raw[ENTRY-BASE:END-BASE]).hexdigest()!=SCOPE_SHA:
        raise ValueError('Original ARM7 signed division module/complete instruction span changed')
    word=lambda address:int.from_bytes(raw[address-BASE:address-BASE+4],'little')
    if word(FIRST-4)!=0xE08FF102 or word(FIRST)!=0xE1A00000 or word(LAST-4)!=0xE1A01003 or word(END-4)!=0xE12FFF1E:
        raise ValueError('Signed division computed dispatch/nop/remainder/return framing differs')
    for index in range(32):
        if [word(FIRST+4+index*12+offset) for offset in (0,4,8)]!=[0xE0B13083,0x30433001,0xE0B00000]:
            raise ValueError('Signed division repeated carry/subtract instruction roles differ')
    return dict(moduleSha256=MODULE_SHA,entry=hex(ENTRY),originalFullRange=[hex(ENTRY),hex(END)],originalFullRangeSha256=SCOPE_SHA,
        additionalArmRange=[hex(FIRST+4),hex(LAST)],additionalInstructionBytes=388,skippedCompilerNopRange=[hex(FIRST),hex(FIRST+4)],
        alreadyInventoriedSignedEpilogue=[hex(LAST),hex(END)],
        physicalAbi='R0 signed numerator,R1 positive signed denominator; R0 quotient,R1 signed remainder; R2,R3,IP,arithmetic flags are caller-saved',
        computedTargetFormula='0x03806CAC + 12 * shift; shift is one of0,4,8,12,16,20,24,28',
        newFunctionOrCSourceCredit=0,originalBlobOrAssemblySourceCredit=0,sharedInventoryOrConfigEdited=False)


def additional(pc,size,thumb):
    return not thumb and size==4 and pc%4==0 and FIRST<pc and pc+size<=LAST


def exercise(raw,numerator,denominator,seed):
    if not -0x80000000<=numerator<=0x7FFFFFFF or not 1<=denominator<=0x7FFFFFFF:
        raise ValueError('Signed division fixture withholds zero/negative denominator or out-of-domain words')
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    image=raw+bytes(0x10000-len(raw))
    cpu.mem_map(BASE,len(image))
    cpu.mem_write(BASE,image)
    cpu.mem_map(RETURN,0x1000)
    initial=[(0x39A57217+index*0x1020305+seed)&0xFFFFFFFF for index in range(15)]
    initial[:2]=[numerator&0xFFFFFFFF,denominator]
    initial[14]=RETURN
    cpu.reg_write(UC_ARM_REG_CPSR,0x1F|((seed&15)<<28))
    for register,value in zip(match_runtime.REGISTERS,initial):
        cpu.reg_write(register,value)
    visited,targets=set(),[]
    pending=[None]
    def code(machine,pc,size,unused):
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not ENTRY<=pc<END or pc==FIRST:
            raise ValueError('Signed division escaped exact original ARM span or executed skipped nop')
        visited.add(pc)
        if pending[0] is not None:
            if pc!=pending[0]:
                raise ValueError('Signed division computed target differs from actual register arithmetic')
            targets.append(pc)
            pending[0]=None
        if pc==FIRST-4:
            value=machine.reg_read(match_runtime.REGISTERS[2])
            if value not in range(0,85,12):
                raise ValueError('Signed division dispatch escaped its discrete shift domain')
            pending[0]=FIRST+4+value*4
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.emu_start(ENTRY,RETURN,timeout=100000,count=10000)
    result=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
    quotient=abs(numerator)//denominator
    if numerator<0:
        quotient=-quotient
    expected=[quotient&0xFFFFFFFF,(numerator-quotient*denominator)&0xFFFFFFFF]
    if cpu.reg_read(UC_ARM_REG_PC)!=RETURN or pending[0] is not None or result[:2]!=expected:
        raise ValueError('Original signed division did not actually return independent quotient/remainder words')
    if result[4:12]!=initial[4:12] or result[13:]!=initial[13:] or bytes(cpu.mem_read(BASE,len(image)))!=image:
        raise ValueError('Signed division preserved registers/SP/LR/whole memory differ')
    return dict(numerator=numerator,denominator=denominator,actualReturn=True,quotient=result[0],remainder=result[1],
        registers=result,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),visited=sorted(visited),computedTargets=targets)


def main():
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    scope=validate_scope(raw)
    cases=[(n,d) for n in (-0x80000000,-65535,-1,0,1,65535,0x7FFFFFFF) for d in (1,2,3,255,65535,0x7FFFFFFF)]
    cases.extend((1<<bit,1) for bit in range(31))
    cases.append((-0x80000000,1))
    randomizer=random.Random(0x31D532)
    cases.extend((randomizer.randrange(-0x80000000,0x80000000),randomizer.randrange(1,0x80000000)) for unused in range(64))
    records=[exercise(raw,n,d,seed) for seed,(n,d) in enumerate(cases)]
    targets=sorted({pc for row in records for pc in row['computedTargets']})
    if targets!=list(range(FIRST+4,FIRST+4+337,48)):
        raise ValueError('Signed division fixture did not exercise all eight computed targets')
    visited={pc for row in records for pc in row['visited']}
    if set(range(FIRST+4,END,4))-visited:
        raise ValueError('Signed division fixture omitted some unrolled/signed-epilogue instructions')
    guards=[not additional(FIRST-4,4,False),not additional(FIRST,4,False),not additional(FIRST+4,4,True),
        not additional(LAST,4,False),not additional(FIRST+6,4,False),not additional(FIRST+4,2,False)]
    changed=bytearray(raw)
    changed[FIRST+4-BASE]^=1
    try:
        validate_scope(bytes(changed))
    except ValueError:
        guards.append(True)
    if len(guards)!=7 or not all(guards):
        raise ValueError('Specific signed division qualifier failed mode/range/byte negative guards')
    target=ROOT/'evidence/arm7/sdk-signed-division-scope-20261031.json'
    write_json(target,dict(generator=__file__.split('\\')[-1],generatorSha256=sha256(__file__),scope=scope,
        actualOriginalReturns=len(records),records=records,computedTargets=targets,negativeControls=7,allPassed=True,
        zeroOrNegativeDenominatorSupported=False,sourceCredit=0,calleeSourceCredit=0,wholeModuleOrRomCredit=0))
    print(json.dumps(dict(report=target.relative_to(ROOT).as_posix(),sha256=sha256(target),actualOriginalReturns=len(records),sourceCredit=0)))


if __name__=='__main__':
    main()
