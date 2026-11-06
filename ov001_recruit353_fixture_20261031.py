import struct
import match_runtime
import probe_ov000_birth329_20261031 as B
from unicorn.arm_const import *
ENTRY,STATE,TEMPLATE=0x022095F4,0x0223DEF8,0x02239ABC
WATCH={ENTRY,0x0207A9EC,0x02061238,0x021FBE70,0x0206271C,0x020626E8,0x020626D0,0x02062828,0x02062A10,0x02062D24,0x02062E44,0x02062FD4,0x02063038,0x02063050,0x02063068,0x02063080,0x0207B460,0x0207C2B8,0x0207C3D8,0x0207C1E4,0x0207C304,0x0207B674,0x0206259C,0x02065D88,0x02044424,0x020443EC,0x02008D78,0x02008E0C}

class Machine(B.BirthMachine):
    def __init__(self,*args):
        super().__init__(*args)
        self.providers={}
        self.observed=set()
    def write(self,uc,access,address,size,value,data):
        if STATE<=address and address+size<=STATE+0x24 or 0x021B9BD0<=address and address+size<=0x021B9BD3:
            self.writes.append([hex(address),size,value])
            return
        super().write(uc,access,address,size,value,data)
    def observe(self,uc,address,size,data):
        self.steps+=1
        self.close_returns(uc,address)
        if ENTRY<=address<ENTRY+396:self.observed.update(range(address,address+size))
        if address in WATCH:
            self.trace.append(dict(entry=hex(address),arguments=[uc.reg_read(r)for r in B.REGS[:4]],sp=hex(uc.reg_read(UC_ARM_REG_SP))))
            self.frames.append(dict(entry=address,returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),sp=uc.reg_read(UC_ARM_REG_SP),preserved=[uc.reg_read(r)for r in B.REGS[4:12]]))
    def recruit(self,args):
        self.u.mem_write(B.STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xB3530000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        for r,v in zip(B.REGS[:2],args):self.u.reg_write(r,v&0xFFFFFFFF)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.trace,self.returned,self.frames,self.writes=[],[],[],[]
        self.steps=0
        self.u.emu_start(ENTRY,B.STOP,count=2000000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.frames or self.u.reg_read(UC_ARM_REG_PC)!=B.STOP or self.u.reg_read(UC_ARM_REG_SP)!=B.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]:raise ValueError('Recruit353 actual return/frame differs')
        return self.u.reg_read(UC_ARM_REG_R0)
