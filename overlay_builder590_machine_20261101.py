import gc
import struct
import main_builder584_machine_20261101 as M
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from link_runtime_unit import measured_module
BASE,STACK,STOP,DESCRIPTOR= M.BASE,M.STACK,M.STOP,0x02600000
DIV=0x02026144
UNITS={'ov005':dict(entry=0x021E00D0,size=412,globalAddress=0x021ED234,globalOffset=0x14),'ov006':dict(entry=0x021DE980,size=284,globalAddress=0x0220F594,globalOffset=0x2C)}


def inputs(module):
    main=M.inputs();info,overlay,symbols=measured_module(module);expected={'ov005':'efd21cd223735980e3f83f95c796725b0abd677043c40ca26d9762e4ea9a97c8','ov006':'fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341'}
    if info['sha256']!=expected[module]:raise ValueError('590 overlay identity differs')
    return dict(main,overlay=overlay,moduleInfo=info,moduleName=module)


def slot(index,mode):
    if not mode:index=((index+36+128)&255)-128
    return(M.SLOTS+12*index)&0xFFFFFFFF


class Machine:
    def __init__(self,original,p,body=None,mainBody=None):
        self.p=p;self.unit=UNITS[original['moduleName']];self.entry=self.unit['entry'];self.extent=len(body)if body is not None else self.unit['size'];self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(0x021D7240,original['overlay']);self.frames=[];self.returns=[];self.mainCalls=[];self.provided=[];self.writes=[];self.observed=set();self.helperObserved={str(a):set()for a in M.RANGES};self.helperObserved[str(M.ENTRY)]=set();self.helperObserved[str(DIV)]=set();self.instructions=0;self.tailViews=[]
        if body is not None:self.u.mem_write(self.entry,body)
        if mainBody is not None:self.u.mem_write(M.ENTRY,mainBody)
        self.word(M.COUNTER,p['counter']);self.u.mem_write(M.MODE,bytes([p['bank']]));self.u.mem_write(DESCRIPTOR,b'\xCC'*32);self.word(self.unit['globalAddress']+self.unit['globalOffset'],0xB590ABCD)
        for index in p.get('occupiedIndices',[]):self.word(slot(index,p['bank']),0x100)
        args=[DESCRIPTOR]+p['args'];self.u.reg_write(UC_ARM_REG_CPSR,0x10);self.initial=[0xA5900000+i*0x100 for i in range(13)]
        for reg,value in zip(M.REGS,self.initial):self.u.reg_write(reg,value)
        for reg,value in zip(M.REGS[:4],args[:4]):self.u.reg_write(reg,value&0xFFFFFFFF)
        for offset,value in enumerate(args[4:]):self.word(STACK+offset*4,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.before=bytes(self.u.mem_read(BASE,0x800000));self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)

    def word(self,address,value):self.u.mem_write(address,struct.pack('<I',value&0xFFFFFFFF))
    def write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+4096:self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&((1<<(size*8))-1)])

    def observe(self,u,address,length,data):
        self.instructions+=1
        while self.frames and address==self.frames[-1]['lr']and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            f=self.frames.pop()
            if[u.reg_read(reg)for reg in M.REGS[4:12]]!=f['preserved']or u.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('590 actual helper frame differs')
            result=dict(entry=f['entry'],inputWords=f['words'],returnedWords=[u.reg_read(reg)for reg in M.REGS[:4]])
            if f['entry']==M.ENTRY:self.mainCalls[f['callIndex']]['returnedR0']=result['returnedWords'][0]
            self.returns.append(result)
        if self.entry<=address<self.entry+self.extent:self.observed.add(address);return
        if address==M.LOWER:
            words=[u.reg_read(reg)for reg in M.REGS[:4]]+list(struct.unpack('<7I',bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP),28))));self.provided.append(dict(entry=M.LOWER,preparedWords=words));u.reg_write(UC_ARM_REG_R0,0xE5900001)
            for reg,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE900000|index)
            u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&0x0FFFFFFF)|0xA0000000);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        if address in[M.ENTRY,M.GETTER,M.RESOURCE,M.INCREMENT,DIV]:
            words=[u.reg_read(reg)for reg in M.REGS[:4]];frame=dict(entry=address,lr=u.reg_read(UC_ARM_REG_LR),sp=u.reg_read(UC_ARM_REG_SP),preserved=[u.reg_read(reg)for reg in M.REGS[4:12]],words=words)
            if address==M.ENTRY:
                words+=list(struct.unpack('<6I',bytes(u.mem_read(frame['sp'],24))));frame['callIndex']=len(self.mainCalls);self.mainCalls.append(dict(preparedWords=words.copy()))
            self.frames.append(frame)
        if address==M.TAIL:self.tailViews.append(u.reg_read(UC_ARM_REG_R0))
        for entry,size in{**M.RANGES,M.ENTRY:M.SIZE,DIV:524}.items():
            if entry<=address<entry+size:self.helperObserved[str(entry)].add(address);return
        raise ValueError(('590 PC outside own/native/provided scopes',hex(address)))

    def run(self):
        self.u.emu_start(self.entry,STOP,count=500000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(reg)for reg in M.REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('590 actual top return differs')
        r=dict(profile=self.p,unit=self.unit,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),returnedWords=[self.u.reg_read(reg)for reg in M.REGS[:4]],coreRegistersAndCpsr=[self.u.reg_read(reg)for reg in M.REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],nativeReturns=self.returns,mainCalls=self.mainCalls,providedCalls=self.provided,nonstackWrites=self.writes,tailForwardings=self.tailViews,ownObserved=sorted(self.observed),helperObserved={k:sorted(v)for k,v in self.helperObserved.items()},instructions=self.instructions);self.u=None;gc.collect();return r
