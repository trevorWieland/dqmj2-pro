import gc
import hashlib
import json
import match_runtime as c
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
GETTER,SETTER,STACK,STOP=0x02048F7C,0x020C484C,0x027F0000,0x027FF800
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def run():
    metadata,image,unused=measured_module('main')
    array=int.from_bytes(image[GETTER-0x02000000+12:GETTER-0x02000000+16],'little')
    state=int.from_bytes(image[SETTER-0x02000000+12:SETTER-0x02000000+16],'little')
    observations=[]
    for entry in[GETTER,SETTER]:
        values=list(range(256))if entry==GETTER else list(range(256))+[0xFFFFFF00|v for v in range(256)]+[0xA5385A00|v for v in range(256)]
        for value in values:
            u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_946);u.mem_map(0x02000000,0x800000);u.mem_write(0x02000000,image)
            u.mem_write(array+1,bytes([value&255]));u.mem_write(state+1,bytes([0xA5]))
            before=bytes(u.mem_read(0x02000000,0x800000))
            expected=bytearray(before)
            if entry==SETTER:expected[state+1-0x02000000]=value&255
            writes=[]
            def write(uc,access,address,size,word,data):writes.append([address,size,word])
            u.hook_add(UC_HOOK_MEM_WRITE,write)
            initial=[0xB3850000+i*0x100 for i in range(13)]
            for register,word in zip(REGS,initial):u.reg_write(register,word)
            u.reg_write(UC_ARM_REG_CPSR,0x10);u.reg_write(UC_ARM_REG_R0,1 if entry==GETTER else value);u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
            u.emu_start(entry,STOP,count=32)
            actual=u.reg_read(UC_ARM_REG_R0)
            expected_registers=list(initial);expected_registers[0]=value&255 if entry==GETTER else value;expected_registers[1]=array if entry==GETTER else state
            if u.reg_read(UC_ARM_REG_PC)!=STOP or u.reg_read(UC_ARM_REG_SP)!=STACK or u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[u.reg_read(r)for r in REGS]!=expected_registers or bytes(u.mem_read(0x02000000,0x800000))!=expected or writes!=([]if entry==GETTER else[[state+1,1,value&255]]):raise ValueError('Byte385 original actual return/register/fullRAM differs')
            observations.append(dict(entry=hex(entry),inputWord=1 if entry==GETTER else value,rawArrayByte=value&255,actualReturns=1,physicalReturnWord=actual,upper24Clean=actual<=255 if entry==GETTER else None,writes=writes))
            del u
            if value%64==0:gc.collect()
    raw=json.dumps(observations,sort_keys=True,separators=(',',':')).encode()
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],sourceCredit=0,actualReturns=len(observations),getterActualReturns=256,setterActualReturns=768,providedCalls=0,freshMachinePerExecution=True,cpu='ARM946',instructionBound=32,getter=dict(address=hex(GETTER),bytes=16,nativeSpanSha256=c.sha(image[GETTER-0x02000000:GETTER-0x02000000+16]),arrayBase=hex(array),supportedIndexWord=1,returnView='cleanu8',inputExtent='Index1 is qualified; no whole-array extent or normal scene lifetime established'),setter=dict(address=hex(SETTER),bytes=16,nativeSpanSha256=c.sha(image[SETTER-0x02000000:SETTER-0x02000000+16]),stateBase=hex(state),argumentEffect='Only low8 bits are stored atbase+1; high24 input bits ignored',returnMeaning='Unproven; physicalR0 remains full incoming word,callers discard it'),observations=observations,observationsSha256=c.sha(raw),limitations=['Only original leaf code executes; no reconstructed source/module credit or global prototype migration','Fresh birth1244 context usesu8getter and a full-word low-byte setter; original formal typedef/arity and UI meaning remain unproven','Only index1 and declared synthetic byte states are exercised; live loaded array/state lifecycle is not inferred','All registersR0..R12,PC/SP/mode,fullRAM and exact byte writes are checked'],generatorSha256=sha256(__file__),reproductionCommand='python probe_main_byte_flow385_20261031.py')
    write_json(ROOT/'evidence/verification/main-byte-flow385-native-20261031.json',report)
    print(json.dumps(dict(actualReturns=len(observations),getterReturns=256,setterReturns=768,providedCalls=0)))

if __name__=='__main__':run()
