import json
import struct
import match_runtime
import probe_ov000_birth329_20261031 as B
from link_runtime_unit import measured_module
from project import ROOT,sha256,write_json
from unicorn.arm_const import *
ENTRY,TEMPLATE,ACTOR,PARAM=0x021FB214,0x02239ABC,0x02360000,0x02361000
WATCH={ENTRY,0x02008D78,0x02008E0C,0x021FB1DC,0x020443EC,0x02044FCC,0x02044F9C,0x02063C00,0x0203D294}

class Machine(B.BirthMachine):
    def __init__(self,*args):
        super().__init__(*args)
        self.providers={}
        self.observed=set()
    def write(self,uc,access,address,size,value,data):
        if TEMPLATE<=address and address+size<=TEMPLATE+132:
            self.writes.append([hex(address),size,value])
            return
        super().write(uc,access,address,size,value,data)
    def observe(self,uc,address,size,data):
        self.steps+=1
        if getattr(self,
            'captureOriginal',
            False)and ENTRY<=address<ENTRY+1316:self.observed.update(range(address,
                address+size))
        self.close_returns(uc,address)
        if address in WATCH:
            self.trace.append(dict(entry=hex(address),
                    arguments=[uc.reg_read(r)for r in B.REGS[:4]],
                    sp=hex(uc.reg_read(UC_ARM_REG_SP))))
            self.frames.append(dict(entry=address,
                    returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,
                    returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),
                    sp=uc.reg_read(UC_ARM_REG_SP),
                    preserved=[uc.reg_read(r)for r in B.REGS[4:12]]))
    def setup_actor(self,stat):
        self.u.mem_write(0x020F69E8,bytes([3]))
        self.u.mem_write(TEMPLATE,bytes([0xA5])*132)
        self.u.mem_write(ACTOR,bytes(0x440))
        self.u.mem_write(PARAM,bytes(0x200))
        self.word(ACTOR+0x1E8,PARAM)
        for offset in[0x1EC,
            0x1EE,
            0x1F4,
            0x1F6,
            0x1F8,
            0x1FA]:self.u.mem_write(ACTOR+offset,
            struct.pack('<h',
                stat))
        self.u.mem_write(ACTOR+0x1FC,bytes([10]))
        self.word(ACTOR+0x200,123)
        self.word(ACTOR+0x204,456)
        self.u.mem_write(ACTOR+0x208,struct.pack('<h',100))
        self.u.mem_write(PARAM+0x2A,struct.pack('<h',367))
        self.u.mem_write(PARAM+0x2C,bytes([0]))
        self.u.mem_write(PARAM+0xAD,bytes([1]))
        self.u.mem_write(PARAM+0xAE,bytes([5]))
        self.u.mem_write(PARAM+0xAB,bytes([6]))
    def call_template(self,actor):
        self.u.mem_write(B.STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xAB450000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        self.u.reg_write(UC_ARM_REG_R0,actor)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.steps=0
        self.frames,self.returned,self.trace,self.writes=[],[],[],[]
        self.u.emu_start(ENTRY,B.STOP,count=200000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.frames or self.u.reg_read(UC_ARM_REG_PC)!=B.STOP or self.u.reg_read(UC_ARM_REG_SP)!=B.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]:raise ValueError('Template349 actual return/frame differs')
        return self.u.reg_read(UC_ARM_REG_R0)
