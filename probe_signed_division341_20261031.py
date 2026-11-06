import json
import random
import match_runtime as c
from project import ROOT,write_json,sha256
from recover_linked_runtime import qualified_bindings
from link_runtime_unit import validate
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM
from unicorn.arm_const import *
BASE=ROOT/'nonmatching/overlay-lane/20261031-division341'
ENTRY,STACK,STOP=0x021FB214,0x027F0000,0x027FF800
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]

def run():
    values=[-0x80000000,-7100000,-10000,-101,-100,-99,-1,0,1,99,100,101,7100000,0x7FFFFFFF]
    rng=random.Random(341)
    values+= [rng.randrange(-0x80000000,0x80000000)for _ in range(128)]
    results=[]
    for name,expression in[('plain','value / 100'),('extra-sign','((unsigned int)value >> 31) + value / 100')]:
        source=BASE/name/'source.c'
        source.parent.mkdir(parents=True,exist_ok=True)
        body='int native_ov001_021fb214(int value) {return '+expression+';}'+chr(10)
        source.write_text(body)
        c.WORK=ROOT/'work/ol341'/name/'compile'
        rows,unused=c.compare(source,'ov001','2','off',True,thumb=False)
        link=ROOT/'work/ol341'/name/'link'
        try:proof=validate(rows[0],qualified_bindings(rows[0]),link)
        except ValueError as error:
            proof=error.args[0]
            if not isinstance(proof,dict)or proof.get('caller')!=rows[0]['name']:raise
        code=(link/'caller.bin').read_bytes()
        observations=[]
        for value in values:
            u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
            u.ctl_set_cpu_model(UC_CPU_ARM_946)
            u.mem_map(0x02000000,0x800000)
            u.mem_write(ENTRY,code)
            u.reg_write(UC_ARM_REG_CPSR,0x10)
            for i,r in enumerate(REGS):u.reg_write(r,0xB3410000+i)
            u.reg_write(UC_ARM_REG_R0,value&0xFFFFFFFF)
            u.reg_write(UC_ARM_REG_SP,STACK)
            u.reg_write(UC_ARM_REG_LR,STOP)
            u.emu_start(ENTRY,STOP,count=2000)
            if u.reg_read(UC_ARM_REG_PC)!=STOP or u.reg_read(UC_ARM_REG_SP)!=STACK or[u.reg_read(r)for r in REGS[4:12]]!=[0xB3410000+i for i in range(4,12)]:raise ValueError('Division341 compiler program did not actually return')
            actual=u.reg_read(UC_ARM_REG_R0)
            native_magic=(((value*0x51EB851F)>>32)>>5)+(1 if value<0 else 0)
            trunc=value//100 if value>=0 else -((-value)//100)
            if native_magic!=trunc:raise ValueError('Division341 independent original magic identity differs')
            observations.append(dict(input=value,compilerReturnWord=actual,originalMagicExpectedWord=trunc&0xFFFFFFFF,equal=actual==(trunc&0xFFFFFFFF)))
        results.append(dict(variant=name,source=str(source.relative_to(ROOT)),sourceSha256=sha256(source),compilation=rows,genuineSandboxLink=proof,compilerTestProgramExecutions=len(values),sourceCredit=0,originalDsFunctionExecutions=0,matches=sum(r['equal']for r in observations),observations=observations))
    report=dict(schemaVersion=1,sourceCredit=0,originalDsFunctionExecutions=0,results=results,scope='Pinned compiler semantics probes only, named/linked at a sandbox slot; no equivalence to the original1352-byte function or source-match credit',nativePattern='ASR5(signed high32(product*0x51EB851F)) + logicalSignBit(product)',limits=['The original machine identity is computed independently; no original DS function executes in these compiler-only programs','This investigates new unaccepted1352-byte draft formulas only; no accepted source is modified or declared defective','Stat multiplication in that draft has its own bounded signed16 inputs and20-valued scale; further native function-level validation remains required'],generatorSha256=sha256(__file__),reproductionCommand='python probe_signed_division341_20261031.py')
    write_json(ROOT/'evidence/verification/signed-division341-compiler-20261031.json',report)
    print(json.dumps([dict(variant=r['variant'],compilerPrograms=r['compilerTestProgramExecutions'],matchesOriginalMagic=r['matches'])for r in results]))

if __name__=='__main__':run()
