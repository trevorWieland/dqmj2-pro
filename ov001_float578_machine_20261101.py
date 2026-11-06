import gc
import struct
import ov001_float574_machine_20261101 as M
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import *
POSITION,PROPERTY=0x02048A60,0x02048A94
ENTRIES={0x0221239C:424,0x022125D0:432}


class Machine(M.Machine):
    def __init__(self,original,p,body=None,smallBody=None):
        super().__init__(original,dict(p,limit=7,number=p['secondary']),None);self.p=p;self.entry=p['entry'];self.extent=len(body)if body is not None else ENTRIES[self.entry];self.smallObserved=set()
        if body is not None:self.u.mem_write(self.entry,body)
        if smallBody is not None:self.u.mem_write(M.ENTRY,smallBody)
        self.half(M.ROOTOBJ+0x14,p['x']);self.half(M.ROOTOBJ+0x16,p['y']);self.half(M.ROOTOBJ+0x26,0xBEEF);self.word(M.ROOTOBJ+0x10,0xD0780001);self.u.mem_write(M.ROOTOBJ+0x23,b'\x7f');self.word(M.ROOTOBJ+0x2C,p['number']);self.word(M.ROOTOBJ+0x30,p['secondary']);self.before=bytes(self.u.mem_read(M.BASE,0x800000))
        for index in[1,2,3]:self.u.reg_write(M.REGS[index],self.initial[index])

    def half(self,address,value):self.u.mem_write(address,struct.pack('<H',value&65535))

    def scope(self,returnAddress):
        if self.entry<=returnAddress<self.entry+self.extent:return'large'
        if M.ENTRY<=returnAddress<M.ENTRY+M.SIZE:return'small'
        return'nested_math'

    def frame(self,address):
        u=self.u;lr=u.reg_read(UC_ARM_REG_LR);scope=self.scope(lr);words=[u.reg_read(reg)for reg in M.REGS[:4]];self.frames.append(dict(entry=address,lr=lr,sp=u.reg_read(UC_ARM_REG_SP),preserved=[u.reg_read(reg)for reg in M.REGS[4:12]],words=words,scope=scope))
        if scope!='nested_math':self.events.append(dict(kind='source-dependency'if address==M.ENTRY else'native',entry=address,scope=scope,words=words,callPc=lr-4))

    def observe(self,u,address,length,data):
        self.instructions+=1
        while self.frames and address==self.frames[-1]['lr']and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            f=self.frames.pop()
            if[u.reg_read(reg)for reg in M.REGS[4:12]]!=f['preserved']or u.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('578 actual dependency frame differs')
            self.returns.append(dict(entry=f['entry'],callPc=f['lr']-4,scope=f['scope'],inputWords=f['words'],returnedWords=[u.reg_read(reg)for reg in M.REGS[:4]]))
        if self.entry<=address<self.entry+self.extent:self.observed.add(address);return
        if M.ENTRY<=address<M.ENTRY+M.SIZE:
            if address==M.ENTRY:self.frame(address)
            self.smallObserved.add(address);return
        if address in[M.GETTER,M.SETTER,POSITION,PROPERTY]:
            words=[u.reg_read(reg)for reg in M.REGS[:4]];prepared=3 if address==POSITION else 2;scope=self.scope(u.reg_read(UC_ARM_REG_LR));event=dict(kind='provided',entry=address,scope=scope,words=words,preparedWords=words[:prepared],callPc=u.reg_read(UC_ARM_REG_LR)-4)
            if address==M.GETTER:
                if words[0]!=M.HANDLE or not 0<=words[1]<=10:raise ValueError('578 getter outside bounded supplied view')
                value=M.TARGETS+words[1]*256;target=value
            else:
                target=words[0]
                if target not in[M.TARGETS+i*256 for i in range(11)]:raise ValueError('578 service target outside supplied view')
                value=0xE0780000|len(self.events)
            event['targetFlagsBefore']=struct.unpack('<I',bytes(u.mem_read(target+0x7C,4)))[0];self.events.append(event);u.reg_write(UC_ARM_REG_R0,value)
            for reg,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE780000|(len(self.events)<<8)|index)
            nibble=len(self.events)&15;u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&0x0FFFFFFF)|(nibble<<28));event.update(providedR0=value,providedFlagsNibble=nibble);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        if address==M.POWERTARGET:self.powerTargets.append([u.reg_read(reg)for reg in M.REGS[:4]])
        if address in[M.CONVERT,M.POWER,M.TRUNC,M.DIV]:self.frame(address)
        if address not in self.i['allowedMath']and not M.DIV<=address<M.DIV+524:raise ValueError(('578 PC outside measured paths',hex(address)))

    def run(self):
        self.u.emu_start(self.entry,M.STOP,count=800000)
        if self.u.reg_read(UC_ARM_REG_PC)!=M.STOP or self.u.reg_read(UC_ARM_REG_SP)!=M.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(reg)for reg in M.REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('578 actual top return differs')
        result=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(M.BASE,0x800000)),allArmCoreRegistersAndCpsr=[self.u.reg_read(reg)for reg in M.REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],returnedWords=[self.u.reg_read(reg)for reg in M.REGS[:4]],nativeReturns=self.returns,callEvents=self.events,powerTargetWords=self.powerTargets,nonstackWrites=self.writes,ownObserved=sorted(self.observed),smallObserved=sorted(self.smallObserved),instructions=self.instructions);self.u=None;gc.collect();return result
