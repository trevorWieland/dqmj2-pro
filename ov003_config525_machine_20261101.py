import gc
import re
import struct
import match_runtime
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
BASE,OVERLAY,STACK,STOP=0x02000000,0x021D7240,0x027F0000,0x027FF800
ENTRY,SIZE,STATE,COPY,TABLE=0x021DD300,756,0x021E0A18,0x021E0A30,0x021E038C
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
PROVIDERS={0x021DA3E4:1,0x021DA3D0:0,0x0205E7A8:2,0x021DEAF8:1,0x021DEA38:6}
NATIVE=[0x0202A634,0x021DAD9C,0x020C36AC,0x020C35EC,0x020C360C,0x020C362C,0x020C364C,0x020C366C,0x020C368C]


def inputs():
    mm,arm,ms=measured_module('main');om,overlay,os=measured_module('ov003');functions={}
    for module,text in [('main',ms),('ov003',os)]:
        for line in text.splitlines():
            m=re.search(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',line)
            if m:functions[int(m[3],0)]=dict(module=module,mode=m[1],bytes=int(m[2],0))
    def literal(address,module='main'):
        data,base=(arm,BASE)if module=='main'else(overlay,OVERLAY)
        return struct.unpack_from('<I',data,address-base)[0]
    return dict(main=mm,module=om,arm=arm,overlay=overlay,ranges={a:functions[a]for a in NATIVE},providers={a:functions[a]for a in PROVIDERS},keys=literal(0x0202A63C),kind=literal(0x021DADA4,'ov003'),config=literal(0x020C36B4),setters=[literal(a+12)+offset for a,offset in zip(NATIVE[3:],[4,8,12,16,20,24])])


class Machine:
    def __init__(self,original,profile,body=None):
        self.i,self.p=original,profile;self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay']);self.extent=len(body)if body is not None else SIZE
        if body is not None:self.u.mem_write(ENTRY,body)
        self.frames,self.returns,self.events,self.writes=[],[],[],[];self.observed=set();self.instructions=0
        self.u.mem_write(STATE,bytes([0xA5])*0x30);self.u.mem_write(TABLE,bytes((index*37+13)&255 for index in range(256)));self.word(original['kind'],profile['kind']);self.half(original['keys']+2,profile['keys'])
        for index in range(6):self.word(original['config']+index*4,(profile['seed']+index*0x11111111)&0xFFFFFFFF)
        self.before=bytes(self.u.mem_read(BASE,0x800000));self.initial=[0xA0550000+index*0x100 for index in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for reg,value in zip(REGS,self.initial):self.u.reg_write(reg,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.observe_write)

    def word(self,a,v):self.u.mem_write(a,struct.pack('<I',v&0xFFFFFFFF))
    def half(self,a,v):self.u.mem_write(a,struct.pack('<H',v&65535))
    def observe_write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+4096:self.writes.append([address,size,value&((1<<(8*size))-1)])

    def observe(self,u,a,length,data):
        self.instructions+=1
        while self.frames and a==(self.frames[-1]['lr']&~1)and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            f=self.frames.pop()
            if [u.reg_read(r)for r in REGS[4:12]]!=f['preserved']or bool(u.reg_read(UC_ARM_REG_CPSR)&32)!=bool(f['lr']&1):raise ValueError('525 native frame differs')
            self.returns.append(dict(entry=f['entry'],aliases=f['aliases'],returnedR0=u.reg_read(UC_ARM_REG_R0)))
        if a in PROVIDERS:
            words=[u.reg_read(r)for r in REGS[:4]];sp=u.reg_read(UC_ARM_REG_SP);prepared=words[:PROVIDERS[a]]
            if PROVIDERS[a]>4:prepared=words+list(struct.unpack('<2I',bytes(u.mem_read(sp,8))))
            e=dict(address=a,rawCallerWords=words,preparedWords=prepared);value=0
            if a==0x021DA3E4:
                if not STACK-512<=words[0]<=STACK-24:raise ValueError('525 config pointer not in bounded stack')
                e['configuration']=list(struct.unpack('<6I',bytes(u.mem_read(words[0],24))))
            if a==0x021DA3D0 and self.p['mutateKind']is not None:self.word(self.i['kind'],self.p['mutateKind'])
            if a==0x0205E7A8:value=0xB0550000|(words[1]&65535)
            if a==0x021DEAF8:
                if words[0]!=self.i['kind']:raise ValueError('525 selection pointer differs')
                self.word(words[0],self.p['selectionAfter'])
            self.events.append(e);u.reg_write(UC_ARM_REG_R0,value)
            for reg,number in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE000000|len(self.events)<<8|number)
            u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        if ENTRY<=a<ENTRY+self.extent:self.observed.add(a);return
        if ENTRY<=a<ENTRY+SIZE:raise ValueError('525 escaped substituted code')
        if a in self.i['ranges']:
            f=dict(entry=a,sp=u.reg_read(UC_ARM_REG_SP),lr=u.reg_read(UC_ARM_REG_LR),preserved=[u.reg_read(r)for r in REGS[4:12]],aliases=[])
            if self.frames and(f['sp'],f['lr'])==(self.frames[-1]['sp'],self.frames[-1]['lr']):self.frames[-1]['aliases'].append(a)
            else:self.frames.append(f)
            if bool(u.reg_read(UC_ARM_REG_CPSR)&32)!=(self.i['ranges'][a]['mode']=='thumb'):raise ValueError('525 native mode differs')
        if not any(start<=a<start+row['bytes']for start,row in self.i['ranges'].items()):raise ValueError(('525 unexpected PC',hex(a)))

    def run(self):
        self.u.emu_start(ENTRY,STOP,count=20000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(r)for r in REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('525 did not actually return in expected state')
        result=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),nativeReturns=self.returns,ownObserved=sorted(self.observed),providedEvents=self.events,nonstackWrites=self.writes,instructions=self.instructions,returnedR0=self.u.reg_read(UC_ARM_REG_R0),extent=self.extent)
        self.u=None;gc.collect();return result
