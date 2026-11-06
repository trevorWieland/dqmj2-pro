import struct
import match_runtime as C
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
ENTRY=0x021FBD6C
CHILD=0x021FB960
SELECTOR=0x021FAFEC
BUSY=0x021B8E84
NOTICE=0x021E3544
GETTER=0x021FBE70
STATE=0x02239A14
SCRATCH=0x02239ABC
RNG=0x020F6044
SP=0x027F0000
STOP=0x026FF000
REGS=C.REGISTERS
NATIVE={ENTRY:(260,0),CHILD:(904,0),GETTER:(24,0),0x0203D294:(72,1),0x02026350:(484,2),SELECTOR:(496,0),0x0205FD60:(16,0)}

def pack(values):
    return struct.pack('<'+'I'*len(values),*[v&0xFFFFFFFF for v in values])

class Machine:
    def __init__(self,main,overlay,body,profile):
        self.p=profile
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000,0x800000)
        self.u.mem_write(0x02000000,main)
        self.u.mem_write(0x021D7240,overlay)
        self.ranges=dict(NATIVE)
        for address,image in (body or {}).items():
            self.u.mem_write(address,image)
            self.ranges[address]=(len(image),0)
        self.u.mem_write(STATE,bytes(0x200))
        self.u.mem_write(STATE+0xA,bytes([14]))
        self.u.mem_write(STATE+0x18,bytes([profile['counter']]))
        self.u.mem_write(STATE+0x1A,bytes([profile['phase']]))
        self.u.mem_write(SCRATCH+0x67,bytes([profile['gate']]))
        self.u.mem_write(RNG,pack([profile['seed']]))
        self.u.mem_write(STATE+0xA,bytes([profile.get('selector',12)]))
        self.u.mem_write(STATE+0xF,bytes([profile.get('subphase',110)]))
        self.u.mem_write(STATE+0x26,struct.pack('<h',profile['threshold']))
        self.u.mem_write(BUSY,pack([profile['busy']]))
        self.beforeState=bytes(self.u.mem_read(STATE,0x200))
        self.decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
        self.u.hook_add(UC_HOOK_CODE,self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)

    def write(self,u,access,address,size,value,unused):
        if not SP-0x1000<=address<SP:
            self.writes.append([address,size,value&((1<<(size*8))-1)])

    def proper_return(self,frame):
        instruction=next(self.decoder.disasm(bytes(self.u.mem_read(self.previous,4)),self.previous))
        actual=instruction.mnemonic.startswith('pop')and'pc'in instruction.op_str or instruction.mnemonic.startswith('bx')and instruction.op_str=='lr'
        if not actual:raise ValueError(('917 proper return instruction absent',hex(self.previous),instruction.mnemonic,instruction.op_str))
        if self.u.reg_read(REGS[13])!=frame['sp'] or [self.u.reg_read(r)for r in REGS[4:12]]!=frame['saved']:
            raise ValueError('917 return frame differs')
        return dict(entry=hex(frame['entry']),returnPc=hex(self.previous),instruction=instruction.mnemonic+' '+instruction.op_str,rawReturnWords=[self.u.reg_read(r)for r in REGS[:2]])

    def code(self,u,pc,size,unused):
        self.steps+=1
        if self.steps>50000:raise ValueError('917 instruction bound')
        self.privateStackStart=min(self.privateStackStart,u.reg_read(REGS[13]))
        if self.frames and pc==self.frames[-1]['lr']:
            self.returns.append(self.proper_return(self.frames.pop()))
        if pc==STOP:
            self.topReturn=self.proper_return(self.topFrame)
            u.emu_stop()
            return
        if pc==NOTICE:
            words=[u.reg_read(r)for r in REGS[:4]]
            if words[:2]!=[0,1]:raise ValueError(('917 notification inputs',words))
            self.provided.append(dict(target=hex(pc),consumedWords=words[:2],rawCallerWords=words,returnWord=0xC0DEC0DE))
            for index in [0,1,2,3,12]:u.reg_write(REGS[index],(0xC0DE1000+index*17)&0xFFFFFFFF)
            u.reg_write(REGS[0],0xC0DEC0DE)
            flags=u.reg_read(UC_ARM_REG_CPSR)
            u.reg_write(UC_ARM_REG_CPSR,(flags&0x0FFFFFFF)|((self.p['ordinal']&15)<<28))
            u.reg_write(UC_ARM_REG_PC,u.reg_read(REGS[14])&~1)
            return
        if pc in self.ranges and pc!=self.entry:
            size,arity=self.ranges[pc]
            self.entries.append(dict(entry=hex(pc),consumedWords=[u.reg_read(r)for r in REGS[:arity]],callerReturnPc=hex(u.reg_read(REGS[14]))))
            self.frames.append(dict(entry=pc,lr=u.reg_read(REGS[14])&~1,sp=u.reg_read(REGS[13]),saved=[u.reg_read(r)for r in REGS[4:12]]))
        if not any(address<=pc<address+size for address,(size,arity)in self.ranges.items()):
            raise ValueError(('917 unexpected native PC',hex(pc)))
        if SELECTOR<=pc<SELECTOR+496:self.pcs.add(pc)
        self.previous=pc

    def run(self,entry):
        self.entry=entry
        self.frames=[]
        self.entries=[]
        self.returns=[]
        self.writes=[]
        self.provided=[]
        self.pcs=set()
        self.steps=0
        self.previous=None
        self.privateStackStart=SP
        self.u.reg_write(UC_ARM_REG_CPSR,0xD3)
        for i,r in enumerate(REGS[:13]):self.u.reg_write(r,0x11110000+i*0x101)
        self.u.reg_write(REGS[13],SP)
        self.u.reg_write(REGS[14],STOP)
        self.topFrame=dict(entry=entry,sp=SP,saved=[self.u.reg_read(r)for r in REGS[4:12]])
        self.u.emu_start(entry,STOP+4,count=50000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.frames:raise ValueError('917 actual return absent')
        return dict(registers=[self.u.reg_read(r)for r in REGS[:13]],cpsr=self.u.reg_read(UC_ARM_REG_CPSR),memory=bytes(self.u.mem_read(0x02000000,0x800000)),stateHex=bytes(self.u.mem_read(STATE,0x200)).hex(),rngState=struct.unpack('<I',self.u.mem_read(RNG,4))[0],nativeEntries=self.entries,nativePhysicalReturns=self.returns,topReturn=self.topReturn,writes=self.writes,provided=self.provided,privateStackStart=self.privateStackStart,ownPcs=sorted(self.pcs),steps=self.steps)
