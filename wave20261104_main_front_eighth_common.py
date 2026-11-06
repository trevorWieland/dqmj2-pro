import struct
import sys
from project import ROOT
sys.path.insert(0,str(ROOT/'deps/native'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_946
from wave20261104_main_front_compiler import REGISTERS

BASE=0x02000000
RAM=0x02310000
STACK=0x02380000
STOP=0x023f0000
STATUS=0x020f6a08
IMAGE=(ROOT/'extract/arm9/arm9.bin').read_bytes()


def signed(value):
    value&=0xffffffff
    return value if value<0x80000000 else value-0x100000000


class Machine:
    def __init__(self,address,code,memory,args):
        self.uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.uc.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.uc.mem_map(BASE,0x200000);self.uc.mem_write(BASE,IMAGE);self.uc.mem_write(address,code)
        self.uc.mem_map(RAM,0x8000);self.uc.mem_map(STACK,0x10000);self.uc.mem_map(STOP,0x1000)
        self.uc.mem_write(RAM,bytes(memory))
        self.initial=[(0x01234567+i*0x01010101)&0xffffffff for i in range(15)]
        self.initial[:len(args)]=[v&0xffffffff for v in args]
        self.initial[13]=STACK+0x8000;self.initial[14]=STOP
        self.uc.reg_write(UC_ARM_REG_CPSR,0x60000010)
        for register,value in zip(REGISTERS,self.initial):self.uc.reg_write(register,value)
        self.writes=[];self.calls=[]
        self.uc.hook_add(UC_HOOK_MEM_WRITE,self.store)

    def store(self,uc,kind,where,size,value,unused):
        assert STACK<=where<STACK+0x10000 or RAM<=where<RAM+0x8000 or (where==STATUS and size==4)
        self.writes.append(('caller',where,size,value))

    def provide(self,where,data):
        self.uc.mem_write(where,data);self.writes.append(('provided',where,bytes(data)))

    def arguments(self):
        return [self.uc.reg_read(r) for r in REGISTERS[:4]]

    def finish_call(self,result):
        for i in [0,1,2,3,12]:self.uc.reg_write(REGISTERS[i],(0xabcd0000+i*0x1111)&0xffffffff)
        self.uc.reg_write(REGISTERS[0],result&0xffffffff)
        self.uc.reg_write(UC_ARM_REG_CPSR,0xa0000010)
        self.uc.reg_write(UC_ARM_REG_PC,self.uc.reg_read(REGISTERS[14]))

    def snapshot(self,returned):
        registers=[self.uc.reg_read(r) for r in REGISTERS]
        if returned:assert registers[4:12]==self.initial[4:12] and registers[13]==self.initial[13]
        return dict(registers=registers,cpsr=self.uc.reg_read(UC_ARM_REG_CPSR),writes=self.writes,calls=self.calls,
            ram=bytes(self.uc.mem_read(RAM,0x8000)),stack=bytes(self.uc.mem_read(STACK,0x10000)),
            status=struct.unpack('<I',self.uc.mem_read(STATUS,4))[0])
