import gc
import json
import re
import struct
import match_runtime as c
from project import ROOT,sha256
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,STACK,STOP=0x02000000,0x021D7240,0x022122AC,240,0x027F0000,0x027FF800
ROOTOBJ,TARGETS,HANDLE=0x02600000,0x02650000,0xD0740001
CONVERT,POWER,TRUNC,DIV,POWERTARGET=0x020244C4,0x0202298C,0x02024394,0x02026144,0x020212F8
GETTER,SETTER=0x0205F98C,0x021F1BA0
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def inputs():
    main,arm,ms=measured_module('main');module,overlay,os=measured_module('ov001');contract=ROOT/'evidence/abi/main-float-word-contracts-20261101.json'
    if sha256(contract)!='e49d32e959bdcb1ff9b2e8182a61c483b57fb1fc4d182819f47554240a241a99'or main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or module['sha256']!='39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92':raise ValueError('574 frozen identities differ')
    report=json.loads(contract.read_text());allowed=set(address for row in report['cases']for address in row['observedAddresses']);return dict(main=main,arm=arm,module=module,overlay=overlay,allowedMath=allowed)


class Machine:
    def __init__(self,original,p,body=None):
        self.i,self.p=original,p;self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay']);self.extent=len(body)if body is not None else SIZE;self.frames=[];self.returns=[];self.events=[];self.powerTargets=[];self.writes=[];self.observed=set();self.instructions=0
        if body is not None:self.u.mem_write(ENTRY,body)
        self.word(ROOTOBJ+0x1C,HANDLE)
        for index in range(11):self.word(TARGETS+index*256+0x7C,0xA0740000|(index<<4)|(2 if p.get('flagsSet')else 0))
        self.before=bytes(self.u.mem_read(BASE,0x800000));self.initial=[0xA0740000+i*0x100 for i in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for reg,value in zip(REGS,self.initial):self.u.reg_write(reg,value)
        for reg,value in zip(REGS[:3],[ROOTOBJ,p['limit'],p['number']]):self.u.reg_write(reg,value&0xFFFFFFFF)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)

    def word(self,address,value):self.u.mem_write(address,struct.pack('<I',value&0xFFFFFFFF))
    def write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+4096:self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&((1<<(size*8))-1)])

    def observe(self,u,address,length,data):
        self.instructions+=1
        while self.frames and address==self.frames[-1]['lr']and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            f=self.frames.pop()
            if[u.reg_read(reg)for reg in REGS[4:12]]!=f['preserved']or u.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('574 actual native frame differs')
            self.returns.append(dict(entry=f['entry'],callPc=f['lr']-4,direct=f['direct'],inputWords=f['words'],returnedWords=[u.reg_read(reg)for reg in REGS[:4]]))
        if ENTRY<=address<ENTRY+self.extent:self.observed.add(address);return
        if address in[GETTER,SETTER]:
            words=[u.reg_read(reg)for reg in REGS[:4]];self.events.append(dict(kind='provided',entry=address,words=words,preparedWords=words[:2],callPc=u.reg_read(UC_ARM_REG_LR)-4))
            if address==GETTER:
                if words[0]!=HANDLE or not 0<=words[1]<=10:raise ValueError('574 provided getter view outside bounded domain')
                value=TARGETS+words[1]*256
            else:value=0xE0740000|len(self.events)
            u.reg_write(UC_ARM_REG_R0,value)
            for reg,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE740000|(len(self.events)<<8)|index)
            nibble=len(self.events)&15;u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&0x0FFFFFFF)|(nibble<<28));self.events[-1].update(providedR0=value,providedFlagsNibble=nibble)
            u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        if address==POWERTARGET:self.powerTargets.append([u.reg_read(reg)for reg in REGS[:4]])
        if address in[CONVERT,POWER,TRUNC,DIV]:
            lr=u.reg_read(UC_ARM_REG_LR);direct=ENTRY<=lr<ENTRY+self.extent;words=[u.reg_read(reg)for reg in REGS[:4]];self.frames.append(dict(entry=address,lr=lr,sp=u.reg_read(UC_ARM_REG_SP),preserved=[u.reg_read(reg)for reg in REGS[4:12]],words=words,direct=direct))
            if direct:self.events.append(dict(kind='native',entry=address,words=words,callPc=lr-4))
        if address not in self.i['allowedMath']and not DIV<=address<DIV+524:raise ValueError(('574 native PC not in frozen finite math paths',hex(address)))

    def run(self):
        self.u.emu_start(ENTRY,STOP,count=500000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(reg)for reg in REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('574 actual top return differs')
        result=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),allArmCoreRegistersAndCpsr=[self.u.reg_read(reg)for reg in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],returnedWords=[self.u.reg_read(reg)for reg in REGS[:4]],nativeReturns=self.returns,callEvents=self.events,powerTargetWords=self.powerTargets,nonstackWrites=self.writes,ownObserved=sorted(self.observed),instructions=self.instructions);self.u=None;gc.collect();return result
