import match_runtime
import probe_ov000_birth329_20261031 as B
import ov001_recruit373_fixture_20261031 as OLD
from unicorn.arm_const import *
ENTRY=0x02209AC0

class Machine(OLD.Machine):
    def observe(self,uc,address,size,data):
        if ENTRY<=address<ENTRY+140:
            if not hasattr(self,'membershipObserved'):self.membershipObserved=set()
            self.membershipObserved.update(range(address,address+size))
        if address!=0x02062A88:
            super().observe(uc,address,size,data)
            return
        self.steps+=1
        self.close_returns(uc,address)
        self.trace.append(dict(entry=hex(address),arguments=[uc.reg_read(r)for r in B.REGS[:4]],sp=hex(uc.reg_read(UC_ARM_REG_SP)),provider=False))
        self.frames.append(dict(entry=address,returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),sp=uc.reg_read(UC_ARM_REG_SP),preserved=[uc.reg_read(r)for r in B.REGS[4:12]]))
    def call(self,entry,args=()):
        self.u.mem_write(B.STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xB3770000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        for r,v in zip(B.REGS,args):self.u.reg_write(r,v&0xFFFFFFFF)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.steps=0
        self.trace,self.returned,self.frames,self.writes,self.provided=[],[],[],[],[]
        self.u.emu_start(entry,B.STOP,count=200000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.frames or self.u.reg_read(UC_ARM_REG_PC)!=B.STOP or self.u.reg_read(UC_ARM_REG_SP)!=B.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]:raise ValueError('Recruit373 actual return/frame differs')
        return self.u.reg_read(UC_ARM_REG_R0)
