import struct
import match_runtime
import probe_ov000_birth329_20261031 as B
import ov001_recruit364_fixture_20261031 as OLD
from unicorn.arm_const import *
REFRESH,ELIGIBILITY=0x02209B4C,0x02209C34
EXTRA={REFRESH,0x02209AC0,0x021DBCBC,0x021DB788,0x021DBCF0,0x021DB7CC,0x021DBD30,0x0207C2B8,0x0207C3D8,0x0207C1E4,0x0207C304,0x0207B674,0x0206259C}

class Machine(OLD.Machine):
    def __init__(self,*args):
        super().__init__(*args)
        self.targetObserved={REFRESH:set(),ELIGIBILITY:set()}
    def write(self,uc,access,address,size,value,data):
        if any(base<=address and address+size<=base+3*0x440 for base in[0x02236F6C,0x022355EC]):
            self.writes.append([hex(address),size,value])
            return
        super().write(uc,access,address,size,value,data)
    def observe(self,uc,address,size,data):
        for target,code_size in[(REFRESH,232),(ELIGIBILITY,136)]:
            if target<=address<target+code_size:self.targetObserved[target].update(range(address,address+size))
        if getattr(self,'subjectEntry',0)<address<getattr(self,'subjectEnd',0) and(address in EXTRA or address in OLD.WATCH or address in OLD.PROVIDERS):
            self.steps+=1
            self.close_returns(uc,address)
            return
        if address not in EXTRA:
            super().observe(uc,address,size,data)
            return
        self.steps+=1
        self.close_returns(uc,address)
        self.trace.append(dict(entry=hex(address),arguments=[uc.reg_read(r)for r in B.REGS[:4]],sp=hex(uc.reg_read(UC_ARM_REG_SP)),provider=False))
        self.frames.append(dict(entry=address,returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),sp=uc.reg_read(UC_ARM_REG_SP),preserved=[uc.reg_read(r)for r in B.REGS[4:12]]))
    def call(self,entry):
        self.u.mem_write(B.STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xB3730000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.steps=0
        self.trace,self.returned,self.frames,self.writes,self.provided=[],[],[],[],[]
        self.u.emu_start(entry,B.STOP,count=200000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.frames or self.u.reg_read(UC_ARM_REG_PC)!=B.STOP or self.u.reg_read(UC_ARM_REG_SP)!=B.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]:raise ValueError('Recruit373 actual return/frame differs')
        return self.u.reg_read(UC_ARM_REG_R0)
