import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,STACK,STOP=0x02000000,0x021D7240,0x0222CF34,780,0x027F0000,0x027FF800
ROWS,IDENTITIES,OUTPUT,RNGSTATE=0x022498FC,0x02249830,0x0224983C,0x020F6044
RECORD,PAYLOAD,PATH=0x02610000,0x02630000,0x0222FCF0
LOOKUP,KIND,PREDICATE,OPEN,CLOSE,SINK=0x020449D4,0x02044CDC,0x0207AA98,0x0203CC2C,0x0203CF9C,0x0207B460
RNG,DIV=0x0203D294,0x02026144
MATH=[0x02025A70,0x02025578,0x02025AB8,0x02025930,0x02022480,0x02024394]
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def inputs():
    main,arm,ms=measured_module('main');module,overlay,os=measured_module('ov001')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or module['sha256']!='39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92':raise ValueError('595 measured images differ')
    return dict(main=main,arm=arm,module=module,overlay=overlay)


class Machine:
    def __init__(self,original,p,body=None):
        self.p=p;self.armSize=len(original['arm']);self.extent=len(body)if body is not None else SIZE;self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay']);self.frames=[];self.returns=[];self.events=[];self.observed=set();self.mainObserved=set();self.writes=[];self.instructions=0
        if body is not None:self.u.mem_write(ENTRY,body)
        self.u.mem_write(ROWS,b'\xCC'*(3*132));self.u.mem_write(OUTPUT,b'\xA5'*(3*64));self.word(IDENTITIES+p['row']*4,p['identity']);self.word(RNGSTATE,p['seed']);self.u.mem_write(RECORD+0x5F,bytes([p['firstId']]));self.u.mem_write(RECORD+0x5E,bytes([(p['firstId']+17)&255]));self.u.mem_write(PAYLOAD,bytes(p['payload']));row=ROWS+p['row']*132;self.u.mem_write(row+0x30,bytes([p['fileCount']]));self.u.mem_write(row+0x18,struct.pack('<h',p['species']));self.u.mem_write(row+0x1A,bytes([p['variant']]));self.before=bytes(self.u.mem_read(BASE,0x800000));self.initial=[0xA5950000+(index<<8)for index in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for reg,value in zip(REGS,self.initial):self.u.reg_write(reg,value)
        for reg,value in zip(REGS[:2],[p['row'],p['modifier']]):self.u.reg_write(reg,value&0xFFFFFFFF)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)

    def word(self,address,value):self.u.mem_write(address,struct.pack('<I',value&0xFFFFFFFF))
    def write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+4096:self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&((1<<(size*8))-1)])

    def observe(self,u,address,length,data):
        self.instructions+=1
        while self.frames and address==self.frames[-1]['lr']and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            f=self.frames.pop()
            if[u.reg_read(reg)for reg in REGS[4:12]]!=f['preserved']or u.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('595 actual native return differs')
            self.returns.append(dict(entry=f['entry'],inputWords=f['words'],returnedWords=[u.reg_read(reg)for reg in REGS[:4]]))
        if ENTRY<=address<ENTRY+self.extent:self.observed.add(address);return
        if address in[LOOKUP,KIND,PREDICATE,OPEN,CLOSE,SINK]:
            words=[u.reg_read(reg)for reg in REGS[:4]];prepared=words[:{LOOKUP:1,KIND:1,PREDICATE:1,OPEN:2,CLOSE:2,SINK:4}[address]];value={LOOKUP:RECORD,KIND:self.p['kind'],OPEN:PAYLOAD if self.p['present']else 0,CLOSE:0xE5950001,SINK:0xD5950001}.get(address,1 if not self.p['restricted']or words[0]%4 else 0);self.events.append(dict(entry=address,preparedWords=prepared,providedR0=value))
            u.reg_write(UC_ARM_REG_R0,value)
            for reg,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE950000|index)
            u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&0x0FFFFFFF)|0xA0000000);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        if address in[RNG,DIV]+MATH:self.frames.append(dict(entry=address,lr=u.reg_read(UC_ARM_REG_LR),sp=u.reg_read(UC_ARM_REG_SP),preserved=[u.reg_read(reg)for reg in REGS[4:12]],words=[u.reg_read(reg)for reg in REGS[:4]]))
        if not BASE<=address<BASE+self.armSize:raise ValueError(('595 PC outside own/measured main/provided paths',hex(address)))
        self.mainObserved.add(address)

    def run(self):
        self.u.emu_start(ENTRY,STOP,count=250000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(reg)for reg in REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('595 actual top return differs')
        r=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),returnedWords=[self.u.reg_read(reg)for reg in REGS[:4]],coreRegistersAndCpsr=[self.u.reg_read(reg)for reg in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],nativeReturns=self.returns,providedCalls=self.events,nonstackWrites=self.writes,ownObserved=sorted(self.observed),mainObserved=sorted(self.mainObserved),instructions=self.instructions);self.u=None;gc.collect();return r
