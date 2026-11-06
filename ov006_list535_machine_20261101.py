import gc
import re
import struct
import match_runtime
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,STACK,STOP=0x02000000,0x021D7240,0x027F0000,0x027FF800
ENTRY,SIZE,STATE,OUTPUT=0x02204E48,220,0x0221C1F0,0x02600000
ALLOC,CLEAR,CLASSIFY=0x0202A44C,0x02008C58,0x020BB144
ACTUAL=[CLEAR,CLASSIFY,0x020685C8,0x02068594,0x02063EA4,0x02096D9C,0x02096CF8,0x02096CE8,0x02096D4C,0x02096D04,0x02096D24,0x02096D6C]
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def inputs():
    mm,arm,ms=measured_module('main');om,overlay,os=measured_module('ov006');functions={}
    for module,text in[('main',ms),('ov006',os)]:
        for line in text.splitlines():
            m=re.search(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',line)
            if m:functions[int(m[3],0)]=dict(module=module,mode=m[1],bytes=int(m[2],0))
    table=struct.unpack_from('<I',arm,0x02063EAC-BASE)[0];mask=struct.unpack_from('<I',arm,0x02096CF4-BASE)[0];veneer=struct.unpack_from('<I',arm,0x02096DA0-BASE)[0]
    if veneer!=0x02096CF9 or mask!=0x1FFFFF:raise ValueError('535 native classifier literal changed')
    return dict(main=mm,module=om,arm=arm,overlay=overlay,ranges={a:functions[a]for a in ACTUAL},allocator=functions[ALLOC],table=table,mask=mask)


class Machine:
    def __init__(self,original,profile,body=None):
        self.i,self.p=original,profile;self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay']);self.extent=len(body)if body is not None else SIZE
        if body is not None:self.u.mem_write(ENTRY,body)
        self.frames,self.returns,self.events,self.writes,self.classifierInputs=[],[],[],[],[];self.observed=set();self.instructions=0;self.clearWords=[]
        self.u.mem_write(STATE,bytes([0xA5])*16);self.u.mem_write(OUTPUT,bytes([profile['poison']])*0x1000)
        for index,word in enumerate(profile['words']):self.u.mem_write(original['table']+index*12,struct.pack('<3I',word,0xA5350000+index,0xB5350000+index))
        self.before=bytes(self.u.mem_read(BASE,0x800000));self.initial=[0xA0350000+index*0x100 for index in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for reg,value in zip(REGS,self.initial):self.u.reg_write(reg,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.observe_write)

    def word(self,a,v):self.u.mem_write(a,struct.pack('<I',v&0xFFFFFFFF))
    def observe_write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+4096:self.writes.append([address,size,value&((1<<(8*size))-1)])

    def observe(self,u,a,length,data):
        self.instructions+=1
        while self.frames and a==(self.frames[-1]['lr']&~1)and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            f=self.frames.pop()
            if [u.reg_read(r)for r in REGS[4:12]]!=f['preserved']or bool(u.reg_read(UC_ARM_REG_CPSR)&32)!=bool(f['lr']&1):raise ValueError('535 native frame differs')
            self.returns.append(dict(entry=f['entry'],aliases=f['aliases'],inputR0=f['inputR0'],returnedR0=u.reg_read(UC_ARM_REG_R0)))
        if a==ALLOC:
            if u.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('535 allocator mode differs')
            words=[u.reg_read(r)for r in REGS[:4]];current=struct.unpack('<I',bytes(u.mem_read(STATE,4)))[0];pointer=self.i['table']if self.p['alias']else OUTPUT;self.events.append(dict(address=a,rawCallerWords=words,preparedWords=words[:3],countBefore=current,returnedPointer=pointer,countAfter=self.p['countAfter']))
            if words[:3]!=[1,current*12,4]or not 1<=current<=64:raise ValueError('535 allocator prepared words differ')
            if self.p['countAfter']is not None:self.word(STATE,self.p['countAfter'])
            u.reg_write(UC_ARM_REG_R0,pointer)
            for reg,number in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE350000|number)
            u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        if ENTRY<=a<ENTRY+self.extent:self.observed.add(a);return
        if ENTRY<=a<ENTRY+SIZE:raise ValueError('535 escaped substituted code')
        if a in self.i['ranges']:
            f=dict(entry=a,sp=u.reg_read(UC_ARM_REG_SP),lr=u.reg_read(UC_ARM_REG_LR),preserved=[u.reg_read(r)for r in REGS[4:12]],inputR0=u.reg_read(UC_ARM_REG_R0),aliases=[])
            if self.frames and(f['sp'],f['lr'])==(self.frames[-1]['sp'],self.frames[-1]['lr']):self.frames[-1]['aliases'].append(a)
            else:self.frames.append(f)
            if bool(u.reg_read(UC_ARM_REG_CPSR)&32)!=(self.i['ranges'][a]['mode']=='thumb'):raise ValueError('535 native mode differs')
            if a==CLASSIFY:self.classifierInputs.append(f['inputR0'])
            if a==CLEAR:
                self.clearWords=[u.reg_read(r)for r in REGS[:4]]
                if self.clearWords[:3]!=[0,STACK-272,256]:raise ValueError('535 native localarray clear differs')
        if not any(start<=a<start+row['bytes']for start,row in self.i['ranges'].items()):raise ValueError(('535 unexpected PC',hex(a)))

    def run(self):
        self.u.emu_start(ENTRY,STOP,count=50000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(r)for r in REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('535 actual top return differs')
        result=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),nativeReturns=self.returns,ownObserved=sorted(self.observed),providedEvents=self.events,nonstackWrites=self.writes,classifierInputs=self.classifierInputs,clearWords=self.clearWords,instructions=self.instructions,returnedR0=self.u.reg_read(UC_ARM_REG_R0),extent=self.extent)
        self.u=None;gc.collect();return result
