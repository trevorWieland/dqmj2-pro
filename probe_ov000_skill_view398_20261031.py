import gc
import json
import match_runtime as c
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
ENTRY,BASE,OUT,STACK,STOP=0x0221F384,0x02000000,0x02620000,0x027F0000,0x027FF800
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def run():
    metadata,image,unused=measured_module('ov000');data=int.from_bytes(image[ENTRY-0x021D7240+20:ENTRY-0x021D7240+24],'little');results=[]
    for raw in range(256):
        for word in[0,0x02620000,0xFFFFFFFF,0xA5361289]:
            u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_946);u.mem_map(BASE,0x800000);u.mem_write(0x021D7240,image);u.mem_write(data+1,bytes([raw]));u.mem_write(data+4,word.to_bytes(4,'little'));u.mem_write(OUT,b'XXXX')
            before=bytes(u.mem_read(BASE,0x800000));expected=bytearray(before);expected[OUT-BASE:OUT-BASE+4]=word.to_bytes(4,'little');writes=[]
            def write(uc,access,address,size,value,context):writes.append([address,size,value])
            u.hook_add(UC_HOOK_MEM_WRITE,write);u.reg_write(UC_ARM_REG_CPSR,0x10)
            initial=[0xA0398000+i*0x100 for i in range(13)]
            for register,value in zip(REGS,initial):u.reg_write(register,value)
            u.reg_write(UC_ARM_REG_R0,OUT);u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP);u.emu_start(ENTRY,STOP,count=16)
            signed=raw if raw<128 else raw-256;registers=list(initial);registers[0]=signed&0xFFFFFFFF;registers[1]=data;registers[2]=word
            if[u.reg_read(r)for r in REGS]!=registers or u.reg_read(UC_ARM_REG_PC)!=STOP or u.reg_read(UC_ARM_REG_SP)!=STACK or u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or bytes(u.mem_read(BASE,0x800000))!=expected or writes!=[[OUT,4,word]]:raise ValueError('Skill-view398 original return/register/fullRAM differs')
            results.append(dict(rawCountByte=raw,inputOutputPointerWord=OUT,globalWord=word,physicalReturnWord=signed&0xFFFFFFFF,wordStoreAddress=OUT,actualReturns=1,writes=writes));del u
        gc.collect()
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',mode='arm',address=hex(ENTRY),bytes=24,moduleSha256=metadata['sha256'],nativeSpanSha256=c.sha(image[ENTRY-0x021D7240:ENTRY-0x021D7240+24]),sourceCredit=0,actualReturns=len(results),providedCalls=0,cpu='ARM946',instructionBound=16,freshMachinePerExecution=True,globalAddress=hex(data),returnRepresentation='Sign-extendeds8 byte atglobal+1',inputEffect='IncomingR0 points to4writable bytes;fullword atglobal+4 stored there beforecountreturn',callerAlias='B070 passes22460B4,whichis context2246090+24',results=results,limitations=['Disjointmappedoutput only;global/output aliasing andbadpointers not exercised','Pointerword is copied,not dereferenced bythisleaf;no extent/lifetime forpointedskillbuffer inferred','Originalformaltypedefs/game meaning unproven;no source migration ornewbytecredit'],generatorSha256=sha256(__file__),reproductionCommand='python probe_ov000_skill_view398_20261031.py')
    write_json(ROOT/'evidence/verification/ov000-skill-view398-native-20261031.json',report);print(json.dumps(dict(actualReturns=len(results),providedCalls=0,sourceCredit=0)))

if __name__=='__main__':run()
