import struct
import match_runtime
import probe_ov000_birth329_20261031 as B
from unicorn.arm_const import *
ENTRY,STATE,TEMPLATE,ARCHIVE=0x0220984C,0x0223DEF8,0x02239ABC,0x02600000
PROVIDERS={0x0207E720:1,0x0206DCD0:1,0x02041538:3,0x02045680:1,0x02068AE8:0,0x0203CC2C:2,0x02045490:4,0x02045994:4,0x0202A498:2,0x0220AAB8:1,0x0220A5E0:0,0x0220AD70:1,0x0220AF00:2,0x0220AF68:1,0x0220A6CC:1,0x02068EB8:4,0x0206BE08:2,0x0206DE44:1,0x0220AFE4:2,0x0220B0F0:6}
WATCH={ENTRY,0x02062A10,0x021FBE70,0x0204518C,0x02045128,0x0204514C,0x02062AA0,0x02062AD0,0x02062A50,0x02062A88,0x02202360,0x0220AAA0}

class Machine(B.BirthMachine):
    def __init__(self,*args):
        super().__init__(*args)
        self.providers={}
        self.observed=set()
        self.provided=[]
    def write(self,uc,access,address,size,value,data):
        if STATE<=address and address+size<=STATE+0x34 or 0x0223DF3C<=address and address+size<=0x0223DF44:
            self.writes.append([hex(address),size,value])
            return
        super().write(uc,access,address,size,value,data)
    def observe(self,uc,address,size,data):
        self.steps+=1
        self.close_returns(uc,address)
        if ENTRY<=address<ENTRY+604:self.observed.update(range(address,address+size))
        if address in WATCH:
            self.trace.append(dict(entry=hex(address),arguments=[uc.reg_read(r)for r in B.REGS[:4]],sp=hex(uc.reg_read(UC_ARM_REG_SP)),provider=False))
            self.frames.append(dict(entry=address,returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),sp=uc.reg_read(UC_ARM_REG_SP),preserved=[uc.reg_read(r)for r in B.REGS[4:12]]))
        if address in PROVIDERS:
            words=[uc.reg_read(r)for r in B.REGS[:4]]
            if PROVIDERS[address]>4:words.extend(struct.unpack('<2I',uc.mem_read(uc.reg_read(UC_ARM_REG_SP),8)))
            item=dict(entry=hex(address),arguments=words[:PROVIDERS[address]],provider=True)
            if address==0x0207E720:
                raw=bytes(uc.mem_read(words[0],14))
                item['descriptor']=dict(kind=raw[0],species=int.from_bytes(raw[2:4],'little',signed=True),variant=raw[4],raw=raw[5],namePointer=int.from_bytes(raw[8:12],'little'),length=raw[12],last=raw[13])
                item['nameBytes']=bytes(uc.mem_read(item['descriptor']['namePointer'],20)).hex()
            if address==0x0220B0F0:item['coordinates']=list(struct.unpack('<2H',uc.mem_read(words[2],4)))
            value=ARCHIVE if address==0x0203CC2C else self.ioResult
            item['providedReturnWord']=value
            self.provided.append(item)
            self.trace.append(item)
            uc.reg_write(UC_ARM_REG_R0,value)
            for i in[1,2,3,12]:uc.reg_write(B.REGS[i],(0xDD360000+len(self.provided)*0x100+i)&0xFFFFFFFF)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def controller(self):
        self.u.mem_write(B.STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xB3600000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.steps=0
        self.trace,self.returned,self.frames,self.writes,self.provided=[],[],[],[],[]
        self.u.emu_start(ENTRY,B.STOP,count=50000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.frames or self.u.reg_read(UC_ARM_REG_PC)!=B.STOP or self.u.reg_read(UC_ARM_REG_SP)!=B.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]:raise ValueError('Recruit360 actual return/frame differs')
        return self.u.reg_read(UC_ARM_REG_R0)
