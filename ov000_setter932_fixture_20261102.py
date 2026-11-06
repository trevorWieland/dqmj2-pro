import struct
import match_runtime as C
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_PC,UC_ARM_REG_CPSR
ENTRY=0x021DF200
GLOBAL=0x0223142C
OUTPUT=GLOBAL+0x7C0
SP=0x027F0000
STOP=0x026FF000


def profiles():
    rows=[]
    for upper in [0,0x100,0x8000,0x10000,0x7FFF0000,0xFFFF0000,0xFFFFFF00]:
        for low in range(256):rows.append(dict(ordinal=len(rows),word=upper|low,low=low))
    return rows


class Machine:
    def __init__(self,main,overlay,images,p):
        self.p=p
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000,0x800000)
        self.u.mem_write(0x02000000,main)
        self.u.mem_write(0x021D7240,overlay)
        self.ranges={ENTRY:16}
        for address,body in images.items():
            self.u.mem_write(address,body)
            self.ranges[address]=len(body)
        self.u.mem_write(OUTPUT-1,bytes([0x5A,p['low']^0xA5,0xA5]))
        self.writes=[]
        self.pcs=[]
        self.u.hook_add(UC_HOOK_CODE,self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)

    def write(self,u,access,address,size,value,unused):
        self.writes.append([address,size,value&((1<<(8*size))-1)])

    def code(self,u,pc,size,unused):
        if len(self.pcs)>128:raise ValueError('932 instruction bound')
        if pc==STOP:
            u.emu_stop()
            return
        if not any(base<=pc<base+size for base,size in self.ranges.items()):raise ValueError(('932 unexpected PC',hex(pc)))
        self.pcs.append(pc)

    def run(self,entry):
        flags=0x10|((self.p['ordinal']&15)<<28)
        self.u.reg_write(UC_ARM_REG_CPSR,flags)
        for index,register in enumerate(C.REGISTERS[:13]):self.u.reg_write(register,0x11110000+index*0x101)
        self.u.reg_write(C.REGISTERS[0],self.p['word'])
        self.u.reg_write(C.REGISTERS[13],SP)
        self.u.reg_write(C.REGISTERS[14],STOP)
        self.initial=[self.u.reg_read(r)for r in C.REGISTERS[:13]]
        self.u.emu_start(entry,STOP+4,count=128)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(C.REGISTERS[13])!=SP or[self.u.reg_read(r)for r in C.REGISTERS[4:12]]!=self.initial[4:12]:raise ValueError('932 actual top frame/return differs')
        if not self.pcs or bytes(self.u.mem_read(self.pcs[-1],4))!=bytes.fromhex('1eff2fe1'):raise ValueError('932 actual BX LR absent')
        return dict(registers=[self.u.reg_read(r)for r in C.REGISTERS[:13]],cpsr=self.u.reg_read(UC_ARM_REG_CPSR),memory=bytes(self.u.mem_read(0x02000000,0x800000)),outputBytes=bytes(self.u.mem_read(OUTPUT-1,3)).hex(),writes=self.writes,ownPcs=self.pcs,properTopReturnPc=hex(self.pcs[-1]),initialCpsr=flags)


def model(vm,result):
    p=vm.p
    failures=[]
    if result['registers'][0]!=p['word']:failures.append('full incoming raw word return')
    if result['outputBytes']!=bytes([0x5A,p['low'],0xA5]).hex():failures.append('low8 store/canaries')
    if result['writes']!=[[OUTPUT,1,p['low']]]:failures.append('exact onebyte write')
    if result['cpsr']!=result['initialCpsr']:failures.append('flags unexpectedly modified')
    return failures
