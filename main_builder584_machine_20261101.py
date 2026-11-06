import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,ENTRY,SIZE,STACK,STOP=0x02000000,0x02049794,168,0x027F0000,0x027FF800
COUNTER,MODE,SLOTS,LOWER=0x02102978,0x020DDB09,0x02102A18,0x02049BE4
GETTER,TAIL,RESOURCE,INCREMENT=0x02049AA8,0x02049AD0,0x0204975C,0x0204977C
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
RANGES={GETTER:32,TAIL:16,RESOURCE:12,INCREMENT:20}


def inputs():
    module,arm,symbols=measured_module('main')
    if module['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('584 measured main differs')
    return dict(module=module,arm=arm)


class Machine:
    def __init__(self,original,p,body=None):
        self.p=p;self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.extent=len(body)if body is not None else SIZE;self.frames=[];self.returns=[];self.events=[];self.writes=[];self.observed=set();self.helperObserved={str(a):set()for a in RANGES};self.tailViews=[];self.instructions=0
        if body is not None:self.u.mem_write(ENTRY,body)
        self.word(COUNTER,p['counter']);self.u.mem_write(MODE,bytes([p['mode']]));index=p['args'][1]
        if not p['mode']:index=((index+36+128)&255)-128
        self.slot=(SLOTS+12*index)&0xFFFFFFFF
        if not BASE<=self.slot<BASE+0x800000-4:raise ValueError('584 supplied mapped slot outside RAM')
        self.word(self.slot,p['occupied']);self.u.reg_write(UC_ARM_REG_CPSR,0x10);self.initial=[0xA5840000+i*0x100 for i in range(13)]
        for reg,value in zip(REGS,self.initial):self.u.reg_write(reg,value)
        for reg,value in zip(REGS[:4],p['args'][:4]):self.u.reg_write(reg,value&0xFFFFFFFF)
        for offset,value in enumerate(p['args'][4:]):self.word(STACK+offset*4,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.before=bytes(self.u.mem_read(BASE,0x800000));self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)

    def word(self,address,value):self.u.mem_write(address,struct.pack('<I',value&0xFFFFFFFF))
    def write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+4096:self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&((1<<(size*8))-1)])

    def observe(self,u,address,length,data):
        self.instructions+=1
        while self.frames and address==self.frames[-1]['lr']and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            f=self.frames.pop()
            if[u.reg_read(reg)for reg in REGS[4:12]]!=f['preserved']or u.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('584 actual helper return differs')
            self.returns.append(dict(entry=f['entry'],inputWords=f['words'],returnedWords=[u.reg_read(reg)for reg in REGS[:4]]))
        if ENTRY<=address<ENTRY+self.extent:self.observed.add(address);return
        if address==LOWER:
            words=[u.reg_read(reg)for reg in REGS[:4]]+list(struct.unpack('<7I',bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP),28))));value=0xE5840001;self.events.append(dict(entry=LOWER,preparedWords=words,providedR0=value));u.reg_write(UC_ARM_REG_R0,value)
            for reg,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE840000|index)
            u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&0x0FFFFFFF)|0xA0000000);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        if address in[GETTER,RESOURCE,INCREMENT]:self.frames.append(dict(entry=address,lr=u.reg_read(UC_ARM_REG_LR),sp=u.reg_read(UC_ARM_REG_SP),preserved=[u.reg_read(reg)for reg in REGS[4:12]],words=[u.reg_read(reg)for reg in REGS[:4]]))
        if address==TAIL:self.tailViews.append(u.reg_read(UC_ARM_REG_R0))
        for entry,size in RANGES.items():
            if entry<=address<entry+size:self.helperObserved[str(entry)].add(address);return
        raise ValueError(('584 PC outside measured own/helper paths',hex(address)))

    def run(self):
        self.u.emu_start(ENTRY,STOP,count=10000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(reg)for reg in REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('584 actual top return differs')
        result=dict(profile=self.p,slot=self.slot,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),allArmCoreRegistersAndCpsr=[self.u.reg_read(reg)for reg in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],returnedWords=[self.u.reg_read(reg)for reg in REGS[:4]],nativeReturns=self.returns,providedCalls=self.events,tailForwardings=self.tailViews,nonstackWrites=self.writes,ownObserved=sorted(self.observed),helperObserved={k:sorted(v)for k,v in self.helperObserved.items()},instructions=self.instructions);self.u=None;gc.collect();return result
