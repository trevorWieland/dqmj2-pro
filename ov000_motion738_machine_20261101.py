import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,CLAMP,CLAMP_SIZE=0x02000000,0x021D7240,0x022199B8,492,0x02219CE4,140
STATE,VECTOR,INDEX,TABLE,ACTOR=0x02245E54,0x02245EA0,0x02231BEC,0x0222E32C,0x022322D4
STACK,STOP,PRIVATE=0x027F0000,0x027FF800,0x02650000
REGS=c.REGISTERS[:13]
ARITIES={0x021DF1F0:0,0x021DF3BC:1,0x021E07AC:0,0x02041F74:2,0x02219CE4:1,0x02025A28:1,0x02025578:2,0x02025AB8:2,0x020259B4:1,0x02024E0C:2,0x02025CA4:2}
RANGES={0x021DF1F0:16,0x021DF3BC:20,0x021E07AC:12,0x02041F74:28,CLAMP:CLAMP_SIZE}
MAIN_SHA='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'

def inputs():
    main,arm,unused=measured_module('main');module,overlay,unused=measured_module('ov000')
    if main['sha256']!=MAIN_SHA:raise ValueError('738 main image differs')
    return dict(main=main,arm=arm,module=module,overlay=overlay)

class Machine:
    def __init__(self,original,profile,bodies=None,direct=False,private_body=None):
        self.p,self.direct=profile,direct;self.code=CLAMP if direct else ENTRY;self.extent=CLAMP_SIZE if direct else SIZE
        if private_body is not None:self.code,self.extent=PRIVATE,len(private_body)
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay'])
        for address,body in(bodies or {}).items():self.u.mem_write(address,body)
        if private_body is not None:self.u.mem_write(PRIVATE,private_body)
        self.u.mem_write(INDEX,bytes([profile['index']]))
        row=bytearray(14);struct.pack_into('<hhBBb',row,4,profile['rowX'],profile['rowZ'],profile['width'],profile['height'],profile['count']);self.u.mem_write(TABLE+14*profile['index'],bytes(row))
        state=bytearray((n*17+profile['seed']*3)&255 for n in range(0x58));struct.pack_into('<hh',state,0x10,*profile['offset']);struct.pack_into('<I',state,0x20,profile['active']);struct.pack_into('<iii',state,0x4C,*profile['vector']);self.u.mem_write(STATE,bytes(state));self.u.mem_write(ACTOR+0x70,struct.pack('<iii',*profile['source']))
        self.initial=[0xA7380000+i*256 for i in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0xA0000010)
        for register,value in zip(REGS,self.initial):self.u.reg_write(register,value)
        if direct:self.u.reg_write(UC_ARM_REG_R0,VECTOR)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);self.before=bytes(self.u.mem_read(BASE,0x800000))
        self.frames,self.returns,self.calls,self.writes=[],[],[],[];self.own,self.native=set(),set();self.instructions=0
        self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)

    def write(self,u,access,address,size,value,data):
        if STACK-65536<=address<STACK+256:return
        if(address,size)not in[(STATE+0x10,2),(STATE+0x12,2),(VECTOR,4),(VECTOR+8,4)]:raise ValueError(('738 unsupported nonstack write',hex(u.reg_read(UC_ARM_REG_PC)),hex(address),size))
        self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&((1<<(size*8))-1)])

    def observe(self,u,address,length,data):
        self.instructions+=1
        while self.frames and address==self.frames[-1]['returnPc']:
            frame=self.frames.pop()
            if u.reg_read(UC_ARM_REG_SP)!=frame['sp']or[u.reg_read(r)for r in REGS[4:12]]!=frame['saved']:raise ValueError(('738 actual native return frame differs',frame))
            self.returns.append(dict(entry=frame['entry'],rawR0=u.reg_read(UC_ARM_REG_R0),actuallyReturned=True))
        if self.code<=address<self.code+self.extent:self.own.add(address);return
        if address in ARITIES:
            arity=ARITIES[address];words=[u.reg_read(r)for r in REGS[:4]];self.calls.append(dict(entry=address,preparedWords=words[:arity],rawRegisterWords=words))
            self.frames.append(dict(entry=address,returnPc=u.reg_read(UC_ARM_REG_LR)&~1,sp=u.reg_read(UC_ARM_REG_SP),saved=[u.reg_read(r)for r in REGS[4:12]]))
        if not(0x02024E0C<=address<0x02025F1C or any(start<=address<start+size for start,size in RANGES.items())):raise ValueError(('738 unexpected native PC',hex(address)))
        self.native.add(address)

    def run(self):
        self.u.emu_start(self.code,STOP,count=30000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.frames or[self.u.reg_read(r)for r in REGS[4:12]]!=self.initial[4:12]or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16:raise ValueError('738 top did not actually return preserving frame')
        result=dict(profile=self.p,direct=self.direct,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),coreRegistersAndCpsr=[self.u.reg_read(r)for r in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],nativeCalls=self.calls,watchedNativeReturns=self.returns,nonstackWrites=self.writes,ownObserved=sorted(self.own),nativeObserved=sorted(self.native),instructions=self.instructions,finalState=bytes(self.u.mem_read(STATE,0x58)))
        self.u=None;gc.collect();return result
