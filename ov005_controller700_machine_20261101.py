import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE=0x02000000,0x021D7240,0x021E1600,952
STACK,STOP=0x027F0000,0x027FF800
CONTEXT,AUX,BUFFER,SENTINEL=0x021ED438,0x021ED494,0x021EDFE0,0x021E7764
MODE,INFO,FLAG,ACTOR,ALLOC=0x02610000,0x02611000,0x02612000,0x02613000,0x02620000
CALLER,CALLCTX,CALLFLAG=0x021DF630,0x021ED1B0,0x0210276C
PROVIDERS={0x0200F3E0:1,0x02089804:0,0x02089AA4:2,0x021DECB0:0,0x02041538:3,0x02063F6C:0,0x021DFACC:0,0x020642DC:0,0x02064340:0,0x020BEF58:0,0x020BF084:0,0x021E155C:1,0x021E0DE0:1,0x021E026C:6,0x021E0DF8:1,0x01FF8580:1,0x021E1048:1,0x021E00B4:4,0x020BF4D4:0,0x021E0FB0:1,0x02048094:2,0x021E0730:3,0x020BF218:0,0x02048034:2,0x021E0708:3,0x021E0E28:0,0x020BEF48:1,0x020642CC:1,0x0202A37C:3,0x020851D4:0,0x02085200:0,0x0204176C:0}
REGS=c.REGISTERS[:13]


def inputs():
    main,arm,unused=measured_module('main')
    module,overlay,unused=measured_module('ov005')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or module['sha256']!='efd21cd223735980e3f83f95c796725b0abd677043c40ca26d9762e4ea9a97c8':raise ValueError('700 measured images differ')
    return dict(main=main,arm=arm,module=module,overlay=overlay)


class Machine:
    def __init__(self,original,profile,body=None,connected=False,private=False):
        self.p,self.original,self.connected=profile,original,connected
        if private and connected:raise ValueError('700 private control is direct-entry only')
        self.code=0x02650000 if private else ENTRY
        self.entry=CALLER if connected else self.code
        self.extent=len(body)if body is not None else SIZE
        if self.extent>SIZE and not private:raise ValueError('700 canonical image would overlap following helper')
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE,0x800000)
        self.u.mem_map(0x01FF0000,0x10000)
        self.u.mem_write(BASE,original['arm'])
        self.u.mem_write(OVERLAY,original['overlay'])
        if body is not None:self.u.mem_write(self.code,body)
        self.u.mem_write(CONTEXT,bytes(profile['initialContext']))
        self.u.mem_write(BUFFER,b'\xA5'*0x2300)
        self.u.mem_write(MODE,bytes([profile['menuByte']]))
        self.word(SENTINEL,profile['sentinelWord'])
        self.word(INFO+0x44,profile['infoWord'])
        self.word(FLAG,profile['specialWord'])
        self.u.mem_write(ACTOR+0xAF,bytes([profile['actorByte']]))
        self.word(AUX,profile['auxWord'])
        self.word(CALLCTX,0)
        self.word(CALLCTX+4,0)
        self.word(CALLFLAG,0xA7001234)
        self.initial=[0xA7000000+index*256 for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR,0xA0000010)
        for register,value in zip(REGS,self.initial):self.u.reg_write(register,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK)
        self.u.reg_write(UC_ARM_REG_LR,STOP)
        self.frames,self.returns,self.providers,self.writes=[],[],[],[]
        self.own,self.caller,self.native,self.instructions=set(),set(),set(),0
        self.before=bytes(self.u.mem_read(BASE,0x800000))
        self.u.hook_add(UC_HOOK_CODE,self.observe)
        self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)

    def word(self,address,value):self.u.mem_write(address,struct.pack('<I',value&0xFFFFFFFF))

    def write(self,u,access,address,size,value,data):
        if STACK-65536<=address<STACK+256:return
        allowed=[(CONTEXT,CONTEXT+128),(BUFFER,BUFFER+0x2300),(SENTINEL,SENTINEL+4),(FLAG,FLAG+4)]
        if self.connected:allowed.extend([(CALLCTX,CALLCTX+16),(CALLFLAG,CALLFLAG+4)])
        if not any(lo<=address and address+size<=hi for lo,hi in allowed):raise ValueError(('700 unexpected nonstack effect',hex(address),size,hex(u.reg_read(UC_ARM_REG_PC))))
        self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&((1<<(8*size))-1)])

    def service(self,u,address):
        words=[u.reg_read(register)for register in REGS[:4]]
        arity=PROVIDERS[address]
        prepared=words[:min(4,arity)]
        if arity>4:prepared+=list(struct.unpack('<'+'I'*(arity-4),bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP),(arity-4)*4))))
        value,effects=0xE7000000|(address&65535),[]
        if address==0x0200F3E0:
            if prepared!=[CONTEXT+0x4C]:raise ValueError('700 raw output-buffer pointer differs')
            payload=struct.pack('<4I',*self.p['outputWords']);u.mem_write(CONTEXT+0x4C,payload);effects=[dict(address=CONTEXT+0x4C,bytes=payload.hex())]
        elif address==0x021DECB0:value=MODE
        elif address==0x02063F6C:value=INFO
        elif address==0x020642DC:value=self.p['selector']
        elif address==0x02064340:value=FLAG
        elif address==0x020BEF58:value=self.p['pathWord']
        elif address==0x020BF084:value=self.p['subpathWord']
        elif address==0x020BF4D4:value=self.p['modeWord']
        elif address==0x021E0FB0:value=0x02630000 if self.p['resourcePresent']else 0
        elif address==0x020BF218:value=ACTOR
        elif address==0x0202A37C:value=ALLOC if self.p['allocationPresent']else 0
        self.providers.append(dict(entry=address,preparedWords=prepared,rawRegisterWords=words,providedR0=value,ramEffects=effects,enteredThumb=bool(u.reg_read(UC_ARM_REG_CPSR)&32)))
        lr=u.reg_read(UC_ARM_REG_LR)
        u.reg_write(UC_ARM_REG_R0,value)
        for register,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(register,0xDE000000|index)
        cpsr=(u.reg_read(UC_ARM_REG_CPSR)&~0xF0000020)|0x60000000|(32 if lr&1 else 0)
        u.reg_write(UC_ARM_REG_CPSR,cpsr)
        u.reg_write(UC_ARM_REG_PC,lr&~1)

    def observe(self,u,address,length,data):
        self.instructions+=1
        while self.frames and address==(self.frames[-1]['lr']&~1)and u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            frame=self.frames.pop()
            if [u.reg_read(reg)for reg in REGS[4:12]]!=frame['preserved']or bool(u.reg_read(UC_ARM_REG_CPSR)&32)!=bool(frame['lr']&1):raise ValueError('700 watched native frame differs')
            self.returns.append(dict(entry=frame['entry'],preparedWords=frame['words'],returnedWords=[u.reg_read(reg)for reg in REGS[:4]],actualReturn=True,returnPc=address))
        if address==0x02008C58 or(self.connected and address in[ENTRY,0x021DFAB0]):self.frames.append(dict(entry=address,lr=u.reg_read(UC_ARM_REG_LR),sp=u.reg_read(UC_ARM_REG_SP),words=[u.reg_read(reg)for reg in REGS[:4]],preserved=[u.reg_read(reg)for reg in REGS[4:12]]))
        if self.code<=address<self.code+self.extent:self.own.add(address);return
        if self.connected and CALLER<=address<CALLER+348:self.caller.add(address);return
        if address in PROVIDERS:self.service(u,address);return
        if BASE<=address<BASE+len(self.original['arm'])or(self.connected and 0x021DFAB0<=address<0x021DFABC):self.native.add(address);return
        raise ValueError(('700 PC outside own/native/provided scopes',hex(address)))

    def run(self):
        self.u.emu_start(self.entry,STOP,count=100000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(reg)for reg in REGS[4:12]]!=self.initial[4:12]or self.frames:raise ValueError('700 top did not actually return preserving frame')
        result=dict(profile=self.p,connected=self.connected,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),coreRegistersAndCpsr=[self.u.reg_read(reg)for reg in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],watchedNativeReturns=self.returns,providedCalls=self.providers,nonstackWrites=self.writes,ownObserved=sorted(self.own),callerObserved=sorted(self.caller),nativeObserved=sorted(self.native),instructions=self.instructions)
        self.u=None;gc.collect();return result
