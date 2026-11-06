import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,STACK,STOP=0x02000000,0x021D7240,0x0222CD00,132,0x027F0000,0x027FF800
ROWS,OUTPUT,STATE,GETTER,FILL=0x022498FC,0x0224983C,0x021D637C,0x020C5938,0x02008D78
STEPS=[0x0222CD84,0x0222CEB8,0x0222CF34,0x0222D240]
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def inputs():
    main,arm,ms=measured_module('main');module,overlay,os=measured_module('ov001')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or module['sha256']!='39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92':raise ValueError('598 measured module differs')
    return dict(main=main,arm=arm,module=module,overlay=overlay)


class Machine:
    def __init__(self,original,p,body=None):
        self.p=p;self.extent=len(body)if body is not None else SIZE;self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay']);self.frames=[];self.returns=[];self.events=[];self.writes=[];self.observed=set();self.helperObserved={GETTER:set(),FILL:set()};self.instructions=0;self.lastPc=None;self.callEdges=[]
        if body is not None:self.u.mem_write(ENTRY,body)
        self.word(STATE,0xABCD0000|p['modifier']);self.u.mem_write(ROWS,b'\xCC'*396);self.u.mem_write(OUTPUT,b'\xA5'*192);self.word(OUTPUT-4,0xC5981234);self.word(ROWS+396,0xC5985678);self.before=bytes(self.u.mem_read(BASE,0x800000));self.initial=[0xA5980000+(index<<8)for index in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for reg,value in zip(REGS,self.initial):self.u.reg_write(reg,value)
        self.u.reg_write(UC_ARM_REG_R0,p['count']);self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
    def word(self,address,value):self.u.mem_write(address,struct.pack('<I',value&0xFFFFFFFF))
    def write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+4096:self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&((1<<(size*8))-1)])
    def observe(self,u,address,length,data):
        self.instructions+=1;previousPc=self.lastPc;self.lastPc=address;providedCall=False
        if address in STEPS and previousPc is not None:
            word=int.from_bytes(bytes(u.mem_read(previousPc,4)),'little');immediate=word&0xFFFFFF;immediate=immediate-0x1000000 if immediate&0x800000 else immediate;target=(previousPc+8+4*immediate)&0xFFFFFFFF;providedCall=word&0xFF000000==0xEB000000 and target==address and u.reg_read(UC_ARM_REG_LR)==previousPc+4
        while self.frames and address==self.frames[-1]['lr']and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            f=self.frames.pop()
            if[u.reg_read(reg)for reg in REGS[4:12]]!=f['preserved']or u.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('598 actual helper return differs')
            self.returns.append(dict(entry=f['entry'],inputWords=f['words'],returnedWords=[u.reg_read(reg)for reg in REGS[:4]]))
        if providedCall:
            self.callEdges.append(dict(callPc=hex(previousPc),instructionWord=hex(word),target=hex(address),lr=hex(u.reg_read(UC_ARM_REG_LR))));self.lastPc=None
            words=[u.reg_read(reg)for reg in REGS[:4]];value=0xE5980000|(STEPS.index(address)<<8)|words[0];self.events.append(dict(entry=address,preparedWords=words[:1 if address==STEPS[0]else 2],providedR0=value,rowsAlreadyZero=bytes(u.mem_read(ROWS,396))==bytes(396),outputAlreadyZero=bytes(u.mem_read(OUTPUT,192))==bytes(192)));u.reg_write(UC_ARM_REG_R0,value)
            for reg,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE980000|index)
            u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&0x0FFFFFFF)|0xA0000000);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        if ENTRY<=address<ENTRY+self.extent:self.observed.add(address);return
        if address in STEPS:raise ValueError('598 provided boundary without a verified actual ARM BL edge')
        if address in[GETTER,FILL]:self.frames.append(dict(entry=address,lr=u.reg_read(UC_ARM_REG_LR),sp=u.reg_read(UC_ARM_REG_SP),preserved=[u.reg_read(reg)for reg in REGS[4:12]],words=[u.reg_read(reg)for reg in REGS[:4]]))
        for entry,size in[(GETTER,12),(FILL,148)]:
            if entry<=address<entry+size:self.helperObserved[entry].add(address);return
        raise ValueError(('598 PC outside source/native/provided ranges',hex(address)))
    def run(self):
        self.u.emu_start(ENTRY,STOP,count=100000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(reg)for reg in REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('598 actual top return differs')
        r=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),allArmCoreRegistersAndCpsr=[self.u.reg_read(reg)for reg in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],returnedWords=[self.u.reg_read(reg)for reg in REGS[:4]],nativeReturns=self.returns,providedCalls=self.events,providedCallEdges=self.callEdges,nonstackWrites=self.writes,ownObserved=sorted(self.observed),helperObserved={str(k):sorted(v)for k,v in self.helperObserved.items()},instructions=self.instructions);self.u=None;gc.collect();return r
