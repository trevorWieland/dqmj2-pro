import struct
import match_runtime
import probe_ov000_birth329_20261031 as B
from unicorn.arm_const import *
ENTRY,STATE,TEMPLATE,CONTEXT,ROWS,FOOTER=0x02209CC0,0x0223DEF8,0x02239ABC,0x021C48F8,0x021C4A04,0x021C4968
PROVIDERS={0x0207E874:0,0x0206DE44:1,0x0206DE64:1,0x02041538:3,0x0206BE08:2,0x0206A0FC:1,0x02209B4C:0,0x0206A49C:0,0x0220A3D8:3,0x0220A3F0:3,0x0220A408:0,0x0206940C:0,0x020698F4:1,0x0206A04C:0,0x0206A06C:1,0x02068F60:1,0x0206DCD0:1,0x0206DE1C:2,0x020491F8:1,0x02047FF0:3,0x0220B21C:1,0x0220A97C:1}
WATCH={ENTRY,0x0202A634,0x0207F3B0,0x02062E18,0x02062A10,0x02008E0C,0x02062AA0,0x02062A50,0x02044CDC,0x021FBE70,0x02062850,0x02062638,0x02062650,0x020628B0,0x02062980,0x02062904,0x02062B00,0x0206BC80,0x0206BD24,0x0206BDc8,0x0206BF44,0x0206BE2C,0x0206BF34,0x0206C078,0x0206C0B0,0x0206C0E0,0x0206C130,0x0206C0D0,0x02069000,0x02209C34,0x021DC2F8,0x021DB508,0x021DB438,0x021DB8D0,0x02202360}

class Machine(B.BirthMachine):
    def __init__(self,*args):
        super().__init__(*args)
        self.providers={}
        self.observed=set()
        self.provided=[]
    def write(self,uc,access,address,size,value,data):
        if STATE<=address and address+size<=STATE+0x34 or CONTEXT<=address and address+size<=CONTEXT+0x100:
            self.writes.append([hex(address),size,value])
            return
        super().write(uc,access,address,size,value,data)
    def observe(self,uc,address,size,data):
        self.steps+=1
        self.close_returns(uc,address)
        if ENTRY<=address<ENTRY+1088:self.observed.update(range(address,address+size))
        if address in WATCH:
            self.trace.append(dict(entry=hex(address),arguments=[uc.reg_read(r)for r in B.REGS[:4]],sp=hex(uc.reg_read(UC_ARM_REG_SP)),provider=False))
            self.frames.append(dict(entry=address,returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),sp=uc.reg_read(UC_ARM_REG_SP),preserved=[uc.reg_read(r)for r in B.REGS[4:12]]))
        if address in PROVIDERS:
            args=[uc.reg_read(r)for r in B.REGS[:PROVIDERS[address]]]
            values={0x0207E874:self.recipe['ready'],0x0206A0FC:self.recipe['action'],0x0206A49C:self.recipe['alternate'],0x020698F4:self.recipe['selection'],0x0206A04C:self.recipe['confirm']}
            value=values.get(address,self.recipe['ioResult'])
            item=dict(entry=hex(address),arguments=args,provider=True,providedReturnWord=value)
            self.provided.append(item)
            self.trace.append(item)
            uc.reg_write(UC_ARM_REG_R0,value)
            for i in[1,2,3,12]:uc.reg_write(B.REGS[i],(0xDD364000+len(self.provided)*0x100+i)&0xFFFFFFFF)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def controller(self):
        self.u.mem_write(B.STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xB3640000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.steps=0
        self.trace,self.returned,self.frames,self.writes,self.provided=[],[],[],[],[]
        self.u.emu_start(ENTRY,B.STOP,count=200000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.frames or self.u.reg_read(UC_ARM_REG_PC)!=B.STOP or self.u.reg_read(UC_ARM_REG_SP)!=B.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]:raise ValueError('Recruit364 actual return/frame differs')
        return self.u.reg_read(UC_ARM_REG_R0)
