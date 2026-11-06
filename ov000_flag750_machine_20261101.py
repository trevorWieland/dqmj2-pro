import gc
import struct
import match_runtime as c
from project import ROOT
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,PRIVATE=0x02000000,0x021D7240,0x022198EC,80,0x02650000
RESOURCE,FLAG,OBJECT,STACK,STOP=0x02245F2C,0x02245E55,0x02610000,0x027F0000,0x027FF800
REGS=c.REGISTERS[:13]
def inputs():
    main,arm,unused=measured_module('main');module,overlay,unused=measured_module('ov000')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or module['sha256']!='783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6':raise ValueError('750 original images differ')
    return dict(main=main,arm=arm,module=module,overlay=overlay)
class Machine:
    def __init__(self,original,profile,body=None,private=False):
        self.p=profile;self.code=PRIVATE if private else ENTRY;self.extent=len(body)if body is not None else SIZE
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay'])
        if body is not None:self.u.mem_write(self.code,body)
        self.u.mem_write(RESOURCE,struct.pack('<I',profile['resourceWord']));self.u.mem_write(RESOURCE+0x1C,struct.pack('<I',profile['pointer']));self.u.mem_write(FLAG,bytes([profile['flag']]));self.u.mem_write(OBJECT,bytes((i*17+profile['seed'])&255 for i in range(128)));self.u.mem_write(OBJECT+0x7C,struct.pack('<I',profile['word']))
        self.initial=[0xA7500000+i*256 for i in range(13)];self.initial[:4]=profile['poison'];self.u.reg_write(UC_ARM_REG_CPSR,0xA0000010)
        for register,value in zip(REGS,self.initial):self.u.reg_write(register,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.before=bytes(self.u.mem_read(BASE,0x800000));self.own=set();self.native=set();self.writes=[];self.calls=[];self.returns=[];self.frames=[]
        self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
    def write(self,u,access,address,size,value,data):
        if STACK-256<=address<STACK+32:return
        if(address,size)!=(OBJECT+0x7C,4):raise ValueError(('750 unexpected write',hex(address),size))
        self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&0xFFFFFFFF])
    def observe(self,u,address,size,data):
        if self.frames and address==self.frames[-1]['returnPc']:
            frame=self.frames.pop()
            if u.reg_read(UC_ARM_REG_SP)!=frame['sp']or[u.reg_read(r)for r in REGS[4:12]]!=frame['saved']:raise ValueError('750 native leaf frame differs')
            self.returns.append(dict(entry=0x0205F98C,rawR0=u.reg_read(UC_ARM_REG_R0),actuallyReturned=True))
        if self.code<=address<self.code+self.extent:self.own.add(address);return
        if address==0x0205F98C:
            words=[u.reg_read(r)for r in REGS[:4]];self.calls.append(dict(entry=address,preparedWords=words[:2],rawRegisterWords=words));self.frames.append(dict(returnPc=u.reg_read(UC_ARM_REG_LR)&~1,sp=u.reg_read(UC_ARM_REG_SP),saved=[u.reg_read(r)for r in REGS[4:12]]))
        if not 0x0205F98C<=address<0x0205F998:raise ValueError(('750 unsupported native PC',hex(address)))
        self.native.add(address)
    def run(self):
        self.u.emu_start(self.code,STOP,count=1000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.frames or[self.u.reg_read(r)for r in REGS[4:12]]!=self.initial[4:12]or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16:raise ValueError('750 did not actually return preserving frame')
        result=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),coreRegistersAndCpsr=[self.u.reg_read(r)for r in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],nativeCalls=self.calls,watchedNativeReturns=self.returns,nonstackWrites=self.writes,ownObserved=sorted(self.own),nativeObserved=sorted(self.native))
        self.u=None;gc.collect();return result
