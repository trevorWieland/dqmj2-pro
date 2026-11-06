import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR

MAIN,WRAM,DATA,STACK,MAC,HW,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04804000,0x04000000,0x0f000000,0x0380fff4
MAIN_SHA='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'
WRAM_SHA='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'

def call(cpu,entry,args=(),budget=100000):
    state=dict(returned=False,instructions=0)
    def hook(machine,pc,size,user):
        if pc==STOP:state['returned']=True;machine.emu_stop();return
        state['instructions']+=1
    token=cpu.hook_add(UC_HOOK_CODE,hook);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP)
    for reg,value in zip(REGISTERS,args):cpu.reg_write(reg,value)
    try:cpu.emu_start(entry,STOP+4,count=budget)
    finally:cpu.hook_del(token)
    if not state['returned']:raise ValueError('Actual prerequisite return not reached:'+hex(entry)+' at '+hex(cpu.reg_read(UC_ARM_REG_PC)))
    return dict(entry=hex(entry),arguments=list(args),actualReturn=True,instructions=state['instructions'],outgoingR0=cpu.reg_read(REGISTERS[0]),sourceCredit=0)

def setup(main,wram,index,mode=1,initialize_transmit=True,context_offset=0):
    if hashlib.sha256(main).hexdigest()!=MAIN_SHA or hashlib.sha256(wram).hexdigest()!=WRAM_SHA:raise ValueError('Complete measured runtime modules changed')
    rng=random.Random(0x288000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),MAC:bytes(0x5000),HW:bytes(0x1000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+context_offset;cpu.mem_write(DATA+0x7000,struct.pack('<I',context));cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or bytes(cpu.mem_read(context,0x694))!=bytes(0x694)or int.from_bytes(cpu.mem_read(WORD,4),'little')!=context:raise ValueError('Measured descriptor prefix installation or clear changed')
    cpu.mem_write(context+0x31c,struct.pack('<I',DATA+0x6000));cpu.mem_write(context+0x320,struct.pack('<HH',2,2));cpu.mem_write(context+0x304,struct.pack('<I',DATA+0x6400));stages=[('queue',0x037fc6ac,[DATA+0x6400,DATA+0x6800,16]),('mode',0x027e8f3c,[mode]),('cam',0x027ec51c,[])]
    if initialize_transmit:stages.append(('tx',0x037faec0,[]))
    returns=[dict(name=name,**call(cpu,entry,args))for name,entry,args in stages]
    return cpu,dict(context=context,regions={address:len(raw)for address,raw in regions.items()},prefixBoundaryReached=True,prefixNormalReturnCredit=0,prerequisiteReturns=returns,modeArgument=mode,syntheticContext=True,providers=[])
