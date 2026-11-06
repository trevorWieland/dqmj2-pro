import json
import random
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT,sha256,write_json

BASE,ENTRY,FIRST,LAST,RETURN=0x037F8000,0x03806E4C,0x03806E9C,0x03807028,0x023FF000
SCOPE_SHA='5c91d1640b64a99527e9faff2db6a08378db2a9324a7c1a3ca5dc765b7671f07'
MODULE_SHA='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def validate_scope(raw):
    from hashlib import sha256 as digest
    if digest(raw).hexdigest()!=MODULE_SHA or digest(raw[ENTRY-BASE:LAST-BASE]).hexdigest()!=SCOPE_SHA:
        raise ValueError('Original ARM7 unsigned division range/module changed')
    word=lambda address:int.from_bytes(raw[address-BASE:address-BASE+4],'little')
    if word(0x03806E98)!=0xE08FF102 or word(FIRST)!=0xE1A00000 or [word(LAST-8),word(LAST-4)]!=[0xE1A01003,0xE12FFF1E]:
        raise ValueError('Original unsigned division computed-PC/epilogue framing differs')
    for index in range(32):
        if [word(0x03806EA0+index*12+offset) for offset in (0,4,8)]!=[0xE0B13083,0x30433001,0xE0B00000]:
            raise ValueError('Original unsigned division repeated carry/subtract instruction roles differ')
    return dict(moduleSha256=MODULE_SHA,entry=hex(ENTRY),originalFullRangeSha256=SCOPE_SHA,
        additionalRange=[hex(FIRST),hex(LAST)],additionalInstructionBytes=392,nonexecutedCompilerNopBytes=4,
        indirectDispatchInstruction='0x3806e98',computedTargetFormula='0x03806EA0 + 12 * shift; shift is one of0,4,8,12,16,20,24,28',
        newFunctionOrCSourceCredit=0,originalBlobOrAssemblySourceCredit=0,
        limitations=['A specific original helper instruction qualification only; no shared inventory/config/boundary changes or reconstructed-source credit',
            'The measured call reaches this helper through original u64 division; its positive-denominator u32 quotient/remainder contract is independently tested'])


def additional(pc,size,thumb):
    return not thumb and size==4 and pc%4==0 and FIRST<pc and pc+size<=LAST


def exercise(raw,numerator,denominator,seed):
    if not 0<=numerator<=0xFFFFFFFF or not 1<=denominator<=0xFFFFFFFF:
        raise ValueError('Unsigned division scope fixture requires positive in-domain denominator')
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    image=raw+bytes(0x10000-len(raw))
    cpu.mem_map(BASE,len(image))
    cpu.mem_write(BASE,image)
    cpu.mem_map(RETURN,0x1000)
    initial=[(0x18639217+index*0x1020305+seed)&0xFFFFFFFF for index in range(15)]
    initial[:2]=[numerator,denominator]
    initial[14]=RETURN
    cpu.reg_write(UC_ARM_REG_CPSR,0x1F|((seed&15)<<28))
    for register,value in zip(match_runtime.REGISTERS,initial):
        cpu.reg_write(register,value)
    visited,targets=set(),[]
    pending=[None]
    def code(machine,pc,size,unused):
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not ENTRY<=pc<LAST or pc==FIRST:
            raise ValueError('Original unsigned division escaped qualified ARM code or executed the skipped nop')
        visited.add(pc)
        if pending[0] is not None:
            if pc!=pending[0]:
                raise ValueError('Original unsigned division indirect target differs from actual register arithmetic')
            targets.append(pc)
            pending[0]=None
        if pc==0x03806E98:
            triple_shift=machine.reg_read(match_runtime.REGISTERS[2])
            if triple_shift not in range(0,85,12):
                raise ValueError('Original unsigned division dispatch shift escaped its discrete proven domain')
            pending[0]=0x03806EA0+triple_shift*4
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.emu_start(ENTRY,RETURN,timeout=100000,count=10000)
    result=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
    if cpu.reg_read(UC_ARM_REG_PC)!=RETURN or pending[0] is not None or result[:2]!=list(divmod(numerator,denominator)):
        raise ValueError('Original unsigned division did not actually return the independent quotient/remainder')
    if result[4:]!=initial[4:] or bytes(cpu.mem_read(BASE,len(image)))!=image or bytes(cpu.mem_read(RETURN,0x1000))!=bytes(0x1000):
        raise ValueError('Original unsigned division preserved register/whole memory contract differs')
    return dict(numerator=numerator,denominator=denominator,actualReturn=True,quotient=result[0],remainder=result[1],
        registers=result,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),visited=sorted(visited),computedTargets=targets)


def main():
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    scope=validate_scope(raw)
    edges=(0,1,2,255,65535,0x7FFFFFFF,0x80000000,0xFFFFFFFF)
    cases=[(n,d) for n in edges for d in edges if d]
    cases.extend((1<<shift,1) for shift in range(32))
    randomizer=random.Random(0x31D176)
    cases.extend((randomizer.getrandbits(32),randomizer.getrandbits(32)|1) for unused in range(64))
    rows=[exercise(raw,n,d,seed) for seed,(n,d) in enumerate(cases)]
    targets=sorted({pc for row in rows for pc in row['computedTargets']})
    if targets!=list(range(0x03806EA0,0x03806FF1,48)):
        raise ValueError('Unsigned division fixture did not cover all eight actual computed entry targets')
    visited={pc for row in rows for pc in row['visited']}
    if set(range(0x03806EA0,LAST,4))-visited:
        raise ValueError('Unsigned division native fixture omitted some unrolled carry/subtract/return instructions')
    guards=[not additional(FIRST-4,4,False),not additional(FIRST,4,False),not additional(FIRST,4,True),not additional(LAST,4,False),
        not additional(FIRST+2,4,False),not additional(FIRST,2,False)]
    changed=bytearray(raw)
    changed[0x03806FF0-BASE]^=1
    try:
        validate_scope(bytes(changed))
    except ValueError:
        guards.append(True)
    if len(guards)!=7 or not all(guards):
        raise ValueError('Specific unsigned division qualifier failed a mode/range/byte negative control')
    target=ROOT/'evidence/arm7/sdk-division-scope-20261031.json'
    write_json(target,dict(generator=__file__.split('\\')[-1],generatorSha256=sha256(__file__),scope=scope,
        actualOriginalReturns=len(rows),records=rows,allEightComputedTargets=targets,negativeControls=7,allPassed=True,
        sourceCredit=0,calleeSourceCredit=0,wholeModuleOrRomCredit=0))
    print(json.dumps(dict(report=target.relative_to(ROOT).as_posix(),sha256=sha256(target),actualOriginalReturns=len(rows),sourceCredit=0)))


if __name__=='__main__':
    main()
