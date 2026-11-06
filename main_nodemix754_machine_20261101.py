import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,ENTRY,SIZE,PRIVATE=0x02000000,0x02030F58,1884,0x02650000
RS,COMMAND,RENDER,MODEL,QUEUE=0x02620000,0x02621000,0x02622000,0x02623000,0x02626000
GLOBAL,CACHE,FLUSH=0x020EE1F8,0x020EF5F8,0x020EDF84
IO,STACK,STOP=0x04000000,0x027F0000,0x027FF800
REGS=c.REGISTERS[:13]
NATIVE={0x02008C58:(76,3),0x0202E300:(92,0),0x02008C40:(24,3),0x02004368:(28,1),0x02004384:(28,1),0x0200434C:(28,1),0x02005994:(36,2),0x02004668:(48,1),0x02004698:(48,1),0x02008D4C:(44,2),0x02008D0C:(28,2)}

def inputs():
    main,arm,unused=measured_module('main')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('754 main image differs')
    return dict(main=main,arm=arm)

class Machine:
    def __init__(self,original,profile,body=None,private=False):
        self.p=profile;self.code=PRIVATE if private else ENTRY;self.extent=len(body)if body is not None else SIZE
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_map(IO,0x10000)
        if body is not None:self.u.mem_write(self.code,body)
        self.u.mem_write(RS,bytes((profile['seed']+13*i)&255 for i in range(0x188)));self.u.mem_write(RS,struct.pack('<II',COMMAND,RENDER));self.u.mem_write(RENDER+4,struct.pack('<I',MODEL));self.u.mem_write(MODEL+0x10,struct.pack('<I',0x100))
        command=bytes([profile['opcode'],profile['destination'],len(profile['entries'])])+b''.join(bytes(row)for row in profile['entries']);self.u.mem_write(COMMAND,command)
        self.u.mem_write(RS+0xCC,struct.pack('<II',*profile['cachedWords']))
        for index in range(64):
            self.u.mem_write(CACHE+index*100,struct.pack('<25i',*profile['cache'][index]))
            self.u.mem_write(MODEL+0x100+index*84,struct.pack('<21i',*profile['inverse'][index]))
        self.u.mem_write(FLUSH,struct.pack('<II',QUEUE if profile['queueEnabled']else 0,0));self.u.mem_write(QUEUE,struct.pack('<I',len(profile['queue']))+b''.join(struct.pack('<I',word)for word in profile['queue']))
        self.u.mem_write(IO+0x600,struct.pack('<I',profile.get('status',0)));self.u.mem_write(IO+0x640,struct.pack('<16i',*profile['clip']));self.u.mem_write(IO+0x680,struct.pack('<9i',*profile['normal']))
        self.initial=[(0xA7540000+i*256+profile['seed'])&0xFFFFFFFF for i in range(13)];self.initial[0]=RS;self.initial[1]=profile['ignoredWord'];self.u.reg_write(UC_ARM_REG_CPSR,0xA0000010)
        for register,value in zip(REGS,self.initial):self.u.reg_write(register,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.before=bytes(self.u.mem_read(BASE,0x800000));self.ioBefore=bytes(self.u.mem_read(IO,0x10000));self.own,self.native=set(),set();self.calls,self.frames,self.events,self.writes=[],[],[],[];self.lastPC=None
        self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
    def write(self,u,access,address,size,value,data):
        if STACK-65536<=address<STACK+256:return
        valid=(address,size)in[(RS,4),(RS+0xCC,4),(RS+0xD0,4),(QUEUE,4)]or CACHE<=address<CACHE+6400 or IO+0x400<=address<IO+0x440 or address in[IO+0x440,IO+0x44C,IO+0x450,IO+0x454]
        if not valid or size!=4:raise ValueError(('754 unsupported nonstack write',hex(address),size))
        self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&0xFFFFFFFF])
    def observe(self,u,address,size,data):
        completed=[]
        while self.frames and address==self.frames[-1]['returnPc']:
            frame=self.frames.pop()
            if u.reg_read(UC_ARM_REG_SP)!=frame['sp']or[u.reg_read(r)for r in REGS[4:12]]!=frame['saved']:raise ValueError('754 native helper frame changed')
            completed.append(frame['entry'])
        if completed:self.events.append(dict(returnInstructionPc=self.lastPC,returnedTo=address,completedNativeEntries=completed,rawR0=u.reg_read(UC_ARM_REG_R0),actuallyReturned=True))
        self.lastPC=address
        if self.code<=address<self.code+self.extent:self.own.add(address);return
        if address in NATIVE:
            arity=NATIVE[address][1];words=[u.reg_read(r)for r in REGS[:4]];entry=dict(entry=address,preparedWords=words[:arity],rawRegisterWords=words)
            if address in[0x0200434C,0x02004368]:entry['matrixWordsAtEntry']=list(struct.unpack('<12i',bytes(u.mem_read(words[0],48))))
            if address==0x02004384:entry['matrixWordsAtEntry']=list(struct.unpack('<9i',bytes(u.mem_read(words[0],36))))
            self.calls.append(entry);self.frames.append(dict(entry=address,returnPc=u.reg_read(UC_ARM_REG_LR)&~1,sp=u.reg_read(UC_ARM_REG_SP),saved=[u.reg_read(r)for r in REGS[4:12]]))
        if not any(start<=address<start+extent for start,(extent,arity)in NATIVE.items()):raise ValueError(('754 unexpected native PC',hex(address)))
        self.native.add(address)
    def run(self,budget=200000):
        self.u.emu_start(self.code,STOP,count=budget)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.frames or[self.u.reg_read(r)for r in REGS[4:12]]!=self.initial[4:12]or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16:raise ValueError(('754 top did not actually return',hex(self.u.reg_read(UC_ARM_REG_PC))))
        result=dict(profile=self.p,initialRegisters=self.initial,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),ioBefore=self.ioBefore,ioAfter=bytes(self.u.mem_read(IO,0x10000)),coreRegistersAndCpsr=[self.u.reg_read(r)for r in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],nativeCalls=self.calls,actualNativeReturnEvents=self.events,nonstackWrites=self.writes,ownObserved=sorted(self.own),nativeObserved=sorted(self.native))
        self.u=None;gc.collect();return result
