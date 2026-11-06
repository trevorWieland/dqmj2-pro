import hashlib
import random
import struct

from ov001_ability28_fixture_20261031 import REGS
from main_file_size250_models_20261031 import FILE,ERROR,SP,construct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY,STOP=0x0202A8E0,0x08000000
NATIVE={0x0200BD04:40}


def execute(main,recipe,candidate=None):
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for a,n in [(0x02000000,0x400000),(0x03000000,0x20000),(STOP,0x1000)]:machine.mem_map(a,n)
    machine.mem_write(0x02000000,main)
    if candidate is not None:
        if len(candidate)!=116:raise ValueError('FileSize250 preserve116 caller bytes')
        machine.mem_write(ENTRY,candidate)
    rng=random.Random(recipe['seed']);stack=rng.randbytes(0x20000);machine.mem_write(0x03000000,stack)
    old_error=rng.getrandbits(32);machine.mem_write(ERROR,struct.pack('<I',old_error))
    initial_file=bytes(machine.mem_read(FILE,72))
    initialized,expected_file,expected_error,services,result=construct(recipe,initial_file,old_error)
    expected_ram=bytearray(machine.mem_read(0x02000000,0x400000));expected_ram[ERROR-0x02000000:ERROR-0x02000000+4]=struct.pack('<I',expected_error)
    values=[rng.getrandbits(32)for r in REGS];values[0]=recipe['path']
    for r,v in zip(REGS,values):machine.reg_write(r,v)
    machine.reg_write(UC_ARM_REG_CPSR,rng.getrandbits(4)<<28|0x10);machine.reg_write(UC_ARM_REG_SP,SP);machine.reg_write(UC_ARM_REG_LR,STOP)
    frame=None;returned=[];calls=[];trace=[];writes=[];observed=set()
    def step(engine,pc,width,data):
        nonlocal frame
        if frame and pc==frame['returnAddress']:
            if engine.reg_read(UC_ARM_REG_SP)!=frame['sp']or[engine.reg_read(r)for r in REGS[4:12]]!=frame['preserved']or bytes(engine.mem_read(FILE,72))!=initialized:
                raise ValueError('FileSize250 actual initializer return/full72-byte effects differ')
            returned.append(dict(address=hex(0x0200BD04),result=engine.reg_read(REGS[0])));frame=None
        if pc==STOP:engine.emu_stop();return
        trace.append(pc)
        if len(trace)>1000 or engine.reg_read(UC_ARM_REG_CPSR)&255!=0x10:raise ValueError('FileSize250 bounded ARM mode differs')
        if pc==0x0200BD04:
            if frame or returned or engine.reg_read(REGS[0])!=FILE:raise ValueError('FileSize250 native initializer arguments differ')
            frame=dict(returnAddress=engine.reg_read(UC_ARM_REG_LR),sp=engine.reg_read(UC_ARM_REG_SP),preserved=[engine.reg_read(r)for r in REGS[4:12]])
        if ENTRY<=pc<ENTRY+112:observed.update(range(pc,pc+width));return
        if any(a<=pc<a+n for a,n in NATIVE.items()):return
        i=len(calls)
        if i>=len(services)or pc!=services[i]['address']:raise ValueError('FileSize250 independent provider order differs')
        event=services[i];arguments=[engine.reg_read(REGS[k])for k in range(len(event['arguments']))]
        if arguments!=event['arguments']or engine.reg_read(UC_ARM_REG_SP)!=FILE:raise ValueError('FileSize250 independent path/block arguments differ')
        if bytes(engine.mem_read(FILE,72))!=event['fileBefore']:raise ValueError('FileSize250 independent file block differs')
        if struct.unpack('<I',bytes(engine.mem_read(ERROR,4)))[0]!=event['errorBefore']:raise ValueError('FileSize250 independent error word differs')
        calls.append(dict(address=hex(pc),arguments=arguments,result=event['result'],fileAfterSha256=hashlib.sha256(event['fileAfter']).hexdigest(),errorAfter=event['errorAfter']))
        engine.mem_write(FILE,event['fileAfter']);engine.mem_write(ERROR,struct.pack('<I',event['errorAfter']))
        engine.reg_write(REGS[0],event['result'])
        for k in [1,2,3,12]:engine.reg_write(REGS[k],(recipe['seed']*0x9E3779B9+i*13+k)&0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC,engine.reg_read(UC_ARM_REG_LR))
    def written(engine,access,a,n,value,data):
        if not(FILE<=a<=SP-n or ERROR<=a<=ERROR+4-n):raise ValueError('FileSize250 unexpected native write region')
        writes.append((a,n,value))
    machine.hook_add(UC_HOOK_CODE,step);machine.hook_add(UC_HOOK_MEM_WRITE,written);machine.emu_start(ENTRY,STOP+4,count=1001)
    actual=[machine.reg_read(r)for r in REGS]
    if machine.reg_read(UC_ARM_REG_PC)!=STOP or machine.reg_read(UC_ARM_REG_SP)!=SP or frame or len(returned)!=1 or actual[0]!=result or actual[4:12]!=values[4:12]or len(calls)!=len(services):raise ValueError('FileSize250 actual caller/initializer return protocol differs')
    ram=bytes(machine.mem_read(0x02000000,0x400000));final_stack=bytes(machine.mem_read(0x03000000,0x20000));offset=FILE-0x03000000
    if ram!=expected_ram or bytes(machine.mem_read(FILE,72))!=expected_file or final_stack[:offset]!=stack[:offset]or final_stack[SP-0x03000000:]!=stack[SP-0x03000000:]:raise ValueError('FileSize250 complete RAM/file/outside-frame stack differs')
    return dict(actualReturn=True,returnWord=actual[0],restoredSP=True,preservedRegisters=actual[4:12],nativeDependencyActualReturns=returned,providedCalls=calls,instructions=len(trace)-len(calls),observedCallerInstructionBytes=sorted(observed),ramSha256=hashlib.sha256(ram).hexdigest(),stackSha256=hashlib.sha256(final_stack).hexdigest(),pcTrace=trace,writes=writes)
