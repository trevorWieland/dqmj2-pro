import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,PRIVATE=0x02000000,0x021D7240,0x02204DEC,292,0x02650000
STATE,WORD_BYTE,SETTER=0x02238190,0x021C4FC1,0x0206E634
STACK,STOP=0x027F0000,0x027FF800
REGS=c.REGISTERS[:13]
PROVIDED={0x02061C1C:7,0x0206E2FC:5,0x0206E6C0:1,0x0206E388:2}

def inputs():
    main,arm,unused=measured_module('main');module,overlay,unused=measured_module('ov000')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or module['sha256']!='783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6':raise ValueError('766 original images differ')
    return dict(main=main,arm=arm,module=module,overlay=overlay)

def profiles():
    return[dict(name=f'caller-{gate}-{byte}',gate=gate,byte7=byte,previousByte=(byte*31+7)&255)for gate in[0,1,128,255]for byte in range(256)]

class Machine:
    def __init__(self,original,profile,body=None,private=False):
        self.p=profile;self.code=PRIVATE if private else ENTRY;self.extent=len(body)if body is not None else SIZE
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay'])
        if body is not None:self.u.mem_write(self.code,body)
        self.u.mem_write(STATE+6,bytes([profile['gate'],profile['byte7']]));self.u.mem_write(WORD_BYTE,bytes([profile['previousByte']]));self.initial=[0xA7660000+i*256 for i in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0xA0000010)
        for register,value in zip(REGS,self.initial):self.u.reg_write(register,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.before=bytes(self.u.mem_read(BASE,0x800000));self.calls,self.frames,self.returns,self.writes=[],[],[],[];self.own=set();self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
    def write(self,u,access,address,size,value,data):
        if STACK-65536<=address<STACK+256:return
        if size!=1 or address not in[STATE+6,WORD_BYTE]:raise ValueError(('766 unexpected write',hex(address),size))
        self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&255])
    def observe(self,u,address,size,data):
        if self.frames and address==self.frames[-1]['returnPc']:
            frame=self.frames.pop()
            if u.reg_read(UC_ARM_REG_SP)!=frame['sp']or[u.reg_read(r)for r in REGS[4:12]]!=frame['saved']:raise ValueError('766 native setter frame changed')
            self.returns.append(dict(entry=SETTER,rawR0=u.reg_read(UC_ARM_REG_R0),actuallyReturned=True))
        if self.code<=address<self.code+self.extent:self.own.add(address);return
        if address in PROVIDED or address==SETTER:
            words=[u.reg_read(r)for r in REGS[:4]];arity=1 if address==SETTER else PROVIDED[address];args=words[:min(arity,4)]+[struct.unpack('<I',bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP)+4*i,4)))[0]for i in range(max(0,arity-4))];entry=dict(entry=address,kind='native'if address==SETTER else'provided',preparedWords=args,rawRegisterWords=words);self.calls.append(entry)
            if address==SETTER:self.frames.append(dict(returnPc=u.reg_read(UC_ARM_REG_LR)&~1,sp=u.reg_read(UC_ARM_REG_SP),saved=[u.reg_read(r)for r in REGS[4:12]]))
            else:
                entry.update(providedR0=0xE7660000|(address&65535),ramEffects=[]);u.reg_write(UC_ARM_REG_R0,entry['providedR0'])
                for register,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(register,0xDE660000|index)
                lr=u.reg_read(UC_ARM_REG_LR);u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&~0xF0000020)|0x60000000|(32 if lr&1 else 0));u.reg_write(UC_ARM_REG_PC,lr&~1);return
        if not SETTER<=address<SETTER+16:raise ValueError(('766 unsupported native PC',hex(address)))
    def run(self):
        self.u.emu_start(self.code,STOP,count=5000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.frames or[self.u.reg_read(r)for r in REGS[4:12]]!=self.initial[4:12]or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16:raise ValueError('766 top did not actually return')
        result=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),coreRegistersAndCpsr=[self.u.reg_read(r)for r in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],calls=self.calls,actualNativeReturns=self.returns,nonstackWrites=self.writes,ownObserved=sorted(self.own));self.u=None;gc.collect();return result

def model(result):
    p=result['profile'];expected=bytearray(result['before']);active=p['gate']==0;calls=[];writes=[]
    if active:
        for args in[[3,8,2,16,2,0,1],[0,2,17,22,2,0,1],[1,3,19,24,2,0,1],[2,3,21,24,2,0,1]]:calls.append(dict(entry=0x02061C1C,kind='provided',preparedWords=args))
        for args in[[0,0,13,0,0],[1,31,13,1,0]]:calls.append(dict(entry=0x0206E2FC,kind='provided',preparedWords=args))
        calls.extend([dict(entry=SETTER,kind='native',preparedWords=[2]),dict(entry=0x0206E6C0,kind='provided',preparedWords=[p['byte7']]),dict(entry=0x0206E388,kind='provided',preparedWords=[4,5])]);expected[WORD_BYTE-BASE]=2;expected[STATE+6-BASE]=1;writes=[[WORD_BYTE,1,2],[STATE+6,1,1]];raw=STATE
    else:raw=p['gate']
    actual=[dict(entry=row['entry'],kind=row['kind'],preparedWords=row['preparedWords'])for row in result['calls']]
    if actual!=calls:raise ValueError('766 caller word sequence differs')
    lo,hi=STACK-65536-BASE,STACK+256-BASE
    if expected[:lo]!=result['after'][:lo]or expected[hi:]!=result['after'][hi:]:raise ValueError('766 complete nonstack model differs')
    if[row[1:]for row in result['nonstackWrites']]!=writes:raise ValueError('766 ordered writes differ')
    if result['coreRegistersAndCpsr'][0]!=raw:raise ValueError('766 own raw return differs')
    if len(result['actualNativeReturns'])!=int(active)or any(row['rawR0']!=2 for row in result['actualNativeReturns']):raise ValueError('766 actual setter raw return differs')
    return dict(active=active,rawR0=raw,nativeReturns=int(active),providedCalls=8*int(active),completeNonstackModel=True)
