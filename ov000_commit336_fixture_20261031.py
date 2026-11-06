import json
import struct
import match_runtime
import prove_ov000_selection333_20261031 as S
import probe_ov000_birth329_20261031 as B
from link_runtime_unit import measured_module
from project import ROOT,sha256,write_json
from unicorn.arm_const import *
ENTRY=0x0222900C
WATCH={ENTRY,
    0x02229100,
    0x0222976C,
    0x0222985C,
    0x0206271C,
    0x020627A0,
    0x02062828,
    0x020628B0,
    0x02062980,
    0x02062A10,
    0x02062A50,
    0x02062A88,
    0x02062D24,
    0x02062FD4,
    0x02063038,
    0x02063050,
    0x02063068,
    0x02063080,
    0x02063098,
    0x0203D294,
    *B.CAPS,
    0x02008E0C}

class Machine(S.Machine):
    def observe(self,uc,address,size,data):
        self.steps+=1
        self.close_returns(uc,address)
        if address in WATCH or address in self.providers:
            self.trace.append(dict(entry=hex(address),
                    arguments=[uc.reg_read(r)for r in B.REGS[:4]],
                    sp=hex(uc.reg_read(UC_ARM_REG_SP)),
                    provider=address in self.providers))
            if address in WATCH:
                self.frames.append(dict(entry=address,
                        returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,
                        returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),
                        sp=uc.reg_read(UC_ARM_REG_SP),
                        preserved=[uc.reg_read(r)for r in B.REGS[4:12]]))
        if address in self.providers:
            value=self.providers[address](self,[uc.reg_read(r)for r in B.REGS[:4]])
            uc.reg_write(UC_ARM_REG_R0,value)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def commit(self,args):
        self.u.mem_write(B.STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xCD000000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        for r,v in zip(B.REGS[:2],args):self.u.reg_write(r,v)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.trace,self.returned,self.frames,self.writes=[],[],[],[]
        self.steps=0
        self.u.emu_start(ENTRY,B.STOP,count=2000000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.frames or self.u.reg_read(UC_ARM_REG_PC)!=B.STOP or self.u.reg_read(UC_ARM_REG_SP)!=B.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]:raise ValueError(('Commit336 actual return/frame differs',
                hex(self.u.reg_read(UC_ARM_REG_PC)),
                hex(self.u.reg_read(UC_ARM_REG_SP)),
                self.steps,
                self.frames[-3:]))
        return self.u.reg_read(UC_ARM_REG_R0)
