import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,COPY,DIV,STACK,STOP=0x02000000,0x021D7240,0x021D9AE0,164,0x02008E0C,0x02026144,0x027F0000,0x027FF800
ROOTOBJ,NODE1,NODE2,DATA,OUTPUT,CONTEXT,SOURCE=0x02600000,0x02601000,0x02602000,0x02603000,0x02610040,0x02620000,0x02640040
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def inputs():
    main,arm,ms=measured_module('main');overlay,body,os=measured_module('ov005')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or overlay['sha256']!='efd21cd223735980e3f83f95c796725b0abd677043c40ca26d9762e4ea9a97c8':raise ValueError('568 module identity differs')
    return dict(main=main,arm=arm,module=overlay,overlay=body)


class Machine:
    def __init__(self,original,p,body=None,direct=False):
        self.i,self.p,self.direct=original,p,direct;self.entry=COPY if direct else ENTRY;self.extent=304 if direct else len(body)if body is not None else SIZE;self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay']);self.frames=[];self.returns=[];self.writes=[];self.reads=[];self.observed=set();self.instructions=0
        if body is not None:self.u.mem_write(ENTRY,body)
        self.u.mem_write(OUTPUT-64,bytes((0xA0+3*i)&255 for i in range(512)));self.u.mem_write(SOURCE-64,bytes((17+13*i)&255 for i in range(512)));self.target=OUTPUT+p.get('destAlign',0);self.source=SOURCE+p.get('sourceAlign',0);index=p.get('index',0);stride=p.get('stride',1)
        if p.get('alias'):self.source=self.target+4-((index*stride)&0xFFFFFFFF)
        self.word(ROOTOBJ+0x20,NODE1);self.word(NODE1+0xC,NODE2);self.word(NODE2+0x24,0 if p.get('nullData')else DATA);self.word(DATA+0x420,p.get('total',1));self.word(DATA+0x424,p.get('rows',1));self.half(DATA+0x584,stride);self.word(CONTEXT+8,self.source);self.before=bytes(self.u.mem_read(BASE,0x800000));self.initial=[0xA0680000+i*0x100 for i in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for r,v in zip(REGS,self.initial):self.u.reg_write(r,v)
        arguments=[self.source,self.target,p['length'],self.initial[3]]if direct else[ROOTOBJ,index,self.target,0 if p.get('nullContext')else CONTEXT]
        for reg,value in zip(REGS[:4],arguments):self.u.reg_write(reg,value&0xFFFFFFFF)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write);self.u.hook_add(UC_HOOK_MEM_READ,self.read)

    def word(self,a,v):self.u.mem_write(a,struct.pack('<I',v&0xFFFFFFFF))
    def half(self,a,v):self.u.mem_write(a,struct.pack('<H',v&65535))
    def write(self,u,access,a,size,value,data):
        if not STACK-65536<=a<STACK+4096:self.writes.append([u.reg_read(UC_ARM_REG_PC),a,size,value&((1<<(size*8))-1)])
    def read(self,u,access,a,size,value,data):
        if not STACK-65536<=a<STACK+4096:self.reads.append([u.reg_read(UC_ARM_REG_PC),a,size,bytes(u.mem_read(a,size)).hex()])

    def observe(self,u,a,length,data):
        self.instructions+=1
        while self.frames and a==self.frames[-1]['lr']and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            f=self.frames.pop()
            if[u.reg_read(r)for r in REGS[4:12]]!=f['preserved']or u.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('568 native callee frame differs')
            self.returns.append(dict(entry=f['entry'],callPc=f['lr']-4,inputWords=f['inputs'],returnedWords=[u.reg_read(r)for r in REGS[:4]]))
        if self.entry<=a<self.entry+self.extent:self.observed.add(a);return
        if not self.direct and a in[COPY,DIV]:self.frames.append(dict(entry=a,sp=u.reg_read(UC_ARM_REG_SP),lr=u.reg_read(UC_ARM_REG_LR),preserved=[u.reg_read(r)for r in REGS[4:12]],inputs=[u.reg_read(r)for r in REGS[:4]]))
        if not any(start<=a<start+size for start,size in[(COPY,304),(DIV,524)]):raise ValueError(('568 unexpected PC',hex(a)))

    def run(self):
        self.u.emu_start(self.entry,STOP,count=100000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(r)for r in REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('568 actual top return differs')
        result=dict(allArmCoreRegistersAndCpsr=[self.u.reg_read(reg)for reg in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),returnedWords=[self.u.reg_read(r)for r in REGS[:4]],nativeReturns=self.returns,nonstackWrites=self.writes,dataReads=self.reads,ownObserved=sorted(self.observed),instructions=self.instructions,direct=self.direct,source=self.source&0xFFFFFFFF,target=self.target);self.u=None;gc.collect();return result
