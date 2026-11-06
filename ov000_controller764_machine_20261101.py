import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,PRIVATE=0x02000000,0x021D7240,0x02218D30,1500,0x02650000
STATE,SLOTS,FLAG,RESOURCE=0x02245E54,0x0222FA08,0x0210276C,0x02245F74
TEMPLATE,SPRITES,BUFFERS=0x02630000,0x02640000,[0x02660000,0x02664000,0x02668000]
MODE,INDEX,TABLE=0x020F605E,0x02231BEC,0x0222E32C
STACK,STOP=0x027F0000,0x027FF800
REGS=c.REGISTERS[:13]
NATIVE={0x0202A634:(12,0),0x020404E0:(16,0),0x021DF3BC:(20,1),0x021DF1F0:(16,0),0x02008C58:(76,3),0x02219CE4:(140,1),0x022198E0:(12,0),0x022198EC:(80,0)}
PROVIDED={0x022187B8:0,0x02214FF0:0,0x0205FC10:8,0x0205FD0C:1,0x0221930C:1,0x022189E4:2,0x02218B4C:0,0x02218B60:0,0x0205FD60:0,0x02041538:3,0x02041814:0,0x02219494:0,0x020406B8:0,0x02214FC8:1,0x020418B0:1,0x02214FE0:0,0x02003EDC:0,0x02003F80:0,0x02004078:0,0x0204820C:3,0x02048308:0,0x02218960:0,0x02218330:1,0x022188CC:1,0x022199B8:0,0x02219C6C:0,0x02045680:1,0x022188AC:0,0x022185B4:0,0x02068AE8:0,0x021F7F9C:0,0x02218B74:0,0x02063E38:0,0x0204AEB4:8,0x02219BA4:0,0x02219C88:0,0x02219728:0,0x0221994C:0}

def inputs():
    main,arm,unused=measured_module('main');module,overlay,unused=measured_module('ov000')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or module['sha256']!='783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6':raise ValueError('764 images differ')
    return dict(main=main,arm=arm,module=module,overlay=overlay)

class Machine:
    def __init__(self,original,profile,body,private=False):
        self.p=profile;self.code=PRIVATE if private else ENTRY;self.extent=len(body)if private else SIZE
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay']);self.u.mem_write(PRIVATE,body)
        state=bytearray(0x58);state[3]=profile['state'];struct.pack_into('<I',state,4,profile['renderWord']);struct.pack_into('<I',state,0x14,profile['cleanup14']);struct.pack_into('<I',state,0x18,profile['cleanup18']);struct.pack_into('<I',state,0x30,profile['field30']);struct.pack_into('<I',state,0x3C,profile['field3c']);struct.pack_into('<iii',state,0x40,*profile['reference']);self.u.mem_write(STATE,bytes(state));self.u.mem_write(SLOTS,bytes([0,profile['slot1'],profile['byte2'],0,profile['slot4']]));self.u.mem_write(FLAG,struct.pack('<I',0xDEADBEEF));self.u.mem_write(MODE,bytes([profile['mode']]));self.u.mem_write(INDEX,b'\x7F')
        for index,flag in[(profile['slot4'],profile['rowFlag']),(127,0)]:
            row=bytearray(14);row[3]=flag;row[8]=33;row[9]=25;row[10]=1;self.u.mem_write(TABLE+14*index,bytes(row))
        self.u.mem_write(0x02245F2C,struct.pack('<I',127));self.u.mem_write(0x02245F48,struct.pack('<I',0));self.u.mem_write(RESOURCE,bytes((i*7+profile['seed'])&255 for i in range(208)));self.u.mem_write(TEMPLATE,bytes((i*29+profile['seed']+1)&255 for i in range(208)))
        self.u.mem_write(SPRITES,bytes(0x80));self.u.mem_write(SPRITES+0x64,struct.pack('<h',profile['spriteCount']));self.u.mem_write(SPRITES+0x68,bytes(profile['spriteIds']));self.u.mem_write(SPRITES+0x70,bytes(x&255 for x in profile['spriteValues']))
        for address in BUFFERS:self.u.mem_write(address,bytes([0xA5])*8192)
        self.initial=[0xA7640000+i*256 for i in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0xA0000010)
        for register,value in zip(REGS,self.initial):self.u.reg_write(register,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.before=bytes(self.u.mem_read(BASE,0x800000));self.calls,self.events,self.frames,self.writes=[],[],[],[];self.own,self.native=set(),set();self.lastPC=None;self.invocations=0
        self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
    def write(self,u,access,address,size,value,data):
        if STACK-65536<=address<STACK+256:return
        valid=STATE<=address<STATE+0x58 or SLOTS<=address<SLOTS+5 or(address,size)==(FLAG,4)or RESOURCE<=address<RESOURCE+208 or any(start<=address<start+8192 for start in BUFFERS)
        if not valid:raise ValueError(('764 unsupported write',hex(address),size))
        self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&((1<<(size*8))-1)])
    def observe(self,u,address,size,data):
        finished=[]
        while self.frames and address==self.frames[-1]['returnPc']:
            frame=self.frames.pop()
            if u.reg_read(UC_ARM_REG_SP)!=frame['sp']or[u.reg_read(r)for r in REGS[4:12]]!=frame['saved']:raise ValueError('764 native helper frame changed')
            finished.append(frame['entry'])
        if finished:self.events.append(dict(returnInstructionPc=self.lastPC,returnedTo=address,completedNativeEntries=finished,rawR0=u.reg_read(UC_ARM_REG_R0),actuallyReturned=True))
        self.lastPC=address
        if self.code<=address<self.code+self.extent:
            if address==self.code:
                self.invocations+=1
                if self.invocations>16:raise ValueError('764 recursion bound exceeded')
            self.own.add(address);return
        if address in PROVIDED or address in NATIVE:
            kind='native'if address in NATIVE else'provided';arity=NATIVE[address][1]if kind=='native'else PROVIDED[address];words=[u.reg_read(r)for r in REGS[:4]];args=words[:min(4,arity)]+[struct.unpack('<I',bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP)+4*i,4)))[0]for i in range(max(0,arity-4))];entry=dict(entry=address,kind=kind,preparedWords=args,rawRegisterWords=words)
            if address==0x0204820C:entry['bufferAtEntry']=bytes(u.mem_read(args[0],2)).hex()
            self.calls.append(entry)
            if kind=='provided':
                returns={0x02214FF0:self.p['constructorGate'],0x0205FC10:TEMPLATE,0x0205FD60:self.p['waitGate'],0x02041814:self.p['uiGate'],0x020406B8:self.p['buttonGate'],0x02214FE0:self.p['exitGate'],0x02003EDC:BUFFERS[0],0x02003F80:BUFFERS[1],0x02004078:BUFFERS[2],0x02063E38:SPRITES};value=returns.get(address,0xE7640000|(address&65535));entry.update(providedR0=value,ramEffects=[]);u.reg_write(UC_ARM_REG_R0,value)
                for register,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(register,0xDE640000|index)
                lr=u.reg_read(UC_ARM_REG_LR);u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&~0xF0000020)|0x60000000|(32 if lr&1 else 0));u.reg_write(UC_ARM_REG_PC,lr&~1);return
            self.frames.append(dict(entry=address,returnPc=u.reg_read(UC_ARM_REG_LR)&~1,sp=u.reg_read(UC_ARM_REG_SP),saved=[u.reg_read(r)for r in REGS[4:12]]))
        if not any(start<=address<start+extent for start,(extent,arity)in NATIVE.items()):raise ValueError(('764 unsupported native PC',hex(address)))
        self.native.add(address)
    def run(self):
        self.u.emu_start(self.code,STOP,count=200000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.frames or[self.u.reg_read(r)for r in REGS[4:12]]!=self.initial[4:12]or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16:raise ValueError('764 top did not actually return')
        result=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),coreRegistersAndCpsr=[self.u.reg_read(r)for r in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],calls=self.calls,actualNativeReturnEvents=self.events,nonstackWrites=self.writes,ownObserved=sorted(self.own),nativeObserved=sorted(self.native),ownInvocations=self.invocations)
        self.u=None;gc.collect();return result
