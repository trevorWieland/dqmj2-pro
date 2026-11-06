import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,PRIVATE=0x02000000,0x021D7240,0x02219494,660,0x02650000
STATE,INDEX,TABLE,TOUCH,KEYS,MODE=0x02245E54,0x02231BEC,0x0222E32C,0x021C36C4,0x020EDEB8,0x020F605E
STACK,STOP=0x027F0000,0x027FF800
REGS=c.REGISTERS[:13]
NATIVE={0x02066C3C:(12,0),0x0202A634:(12,0),0x021DF1F0:(16,0),0x021DF3BC:(20,1),0x020404E0:(16,0),0x020404F0:(16,1),0x0221993C:(16,1),0x02219CE4:(140,1)}
PROVIDED={0x02218800:1,0x02041510:3,0x02041560:1,0x021E7B9C:1,0x020418E8:2}
def inputs():
    main,arm,u=measured_module('main');module,overlay,u=measured_module('ov000')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or module['sha256']!='783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6':raise ValueError('748 images differ')
    return dict(main=main,arm=arm,module=module,overlay=overlay)
class Machine:
    def __init__(self,original,profile,body=None,private=False):
        self.p=profile;self.code=PRIVATE if private else ENTRY;self.extent=len(body)if body is not None else SIZE
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay'])
        if body is not None:self.u.mem_write(self.code,body)
        self.u.mem_write(INDEX,bytes([profile['index']]));row=bytearray(14);row[3]=profile['recordFlag'];row[8]=profile['width'];row[9]=profile['height'];row[10]=1;self.u.mem_write(TABLE+profile['index']*14,bytes(row))
        state=bytearray((n*13+profile['seed'])&255 for n in range(0x58));state[1]=profile['flagByte'];struct.pack_into('<hh',state,0x10,*profile['offset']);struct.pack_into('<hh',state,0x1C,*profile['last']);struct.pack_into('<I',state,0x20,profile['active']);struct.pack_into('<I',state,0x28,profile['secondary']);struct.pack_into('<iii',state,0x40,*profile['reference']);struct.pack_into('<iii',state,0x4C,*profile['vector']);self.u.mem_write(STATE,bytes(state));self.u.mem_write(TOUCH,bytes(profile['touch']));self.u.mem_write(KEYS+2,struct.pack('<H',profile['buttons']));self.u.mem_write(MODE,bytes([profile['mode']]))
        self.initial=[0xA7480000+i*256 for i in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0xA0000010)
        for register,value in zip(REGS,self.initial):self.u.reg_write(register,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.before=bytes(self.u.mem_read(BASE,0x800000));self.calls,self.frames,self.returns,self.writes=[],[],[],[];self.own,self.native=set(),set()
        self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
    def write(self,u,access,address,size,value,data):
        if STACK-65536<=address<STACK+256:return
        if(address,size)not in[(STATE+0x10,2),(STATE+0x12,2),(STATE+0x1C,2),(STATE+0x1E,2),(STATE+0x20,4),(STATE+0x28,4),(STATE+1,1),(MODE,1),(STATE+0x4C,4),(STATE+0x54,4)]:raise ValueError(('748 unsupported nonstack write',hex(address),size))
        self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&((1<<(size*8))-1)])
    def observe(self,u,address,length,data):
        while self.frames and address==self.frames[-1]['returnPc']:
            frame=self.frames.pop()
            if u.reg_read(UC_ARM_REG_SP)!=frame['sp']or[u.reg_read(r)for r in REGS[4:12]]!=frame['saved']:raise ValueError('748 native helper frame changed')
            self.returns.append(dict(entry=frame['entry'],rawR0=u.reg_read(UC_ARM_REG_R0),actuallyReturned=True))
        if self.code<=address<self.code+self.extent:self.own.add(address);return
        if address in NATIVE or address in PROVIDED:
            arity=NATIVE[address][1]if address in NATIVE else PROVIDED[address];words=[u.reg_read(r)for r in REGS[:4]];entry=dict(entry=address,kind='native'if address in NATIVE else'provided',preparedWords=words[:arity],rawRegisterWords=words)
            if address==0x02219CE4:entry['localVectorAtEntry']=list(struct.unpack('<iii',bytes(u.mem_read(words[0],12))))
            self.calls.append(entry)
            if address in PROVIDED:
                value=self.p['guards'][str(words[0])]if address==0x02218800 else self.p['returnWord']if address in[0x021E7B9C,0x020418E8]else 0xE7480000|(address&65535);entry.update(providedR0=value,ramEffects=[])
                u.reg_write(UC_ARM_REG_R0,value)
                for register,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(register,0xDE480000|index)
                lr=u.reg_read(UC_ARM_REG_LR);u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&~0xF0000020)|0x60000000|(32 if lr&1 else 0));u.reg_write(UC_ARM_REG_PC,lr&~1);return
            self.frames.append(dict(entry=address,returnPc=u.reg_read(UC_ARM_REG_LR)&~1,sp=u.reg_read(UC_ARM_REG_SP),saved=[u.reg_read(r)for r in REGS[4:12]]))
        if not any(start<=address<start+size for start,(size,arity)in NATIVE.items()):raise ValueError(('748 unexpected native PC',hex(address)))
        self.native.add(address)
    def run(self):
        self.u.emu_start(self.code,STOP,count=10000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.frames or[self.u.reg_read(r)for r in REGS[4:12]]!=self.initial[4:12]or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16:raise ValueError('748 top did not actually return')
        result=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),coreRegistersAndCpsr=[self.u.reg_read(r)for r in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],calls=self.calls,watchedNativeReturns=self.returns,nonstackWrites=self.writes,ownObserved=sorted(self.own),nativeObserved=sorted(self.native))
        self.u=None;gc.collect();return result
