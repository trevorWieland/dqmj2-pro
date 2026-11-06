import hashlib
import random
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
from match_runtime import REGISTERS
MAIN,WRAM,STACK,STOP,ENTRY=0x027e0000,0x037f8000,0x03030000,0x0f000000,0x03806bf0
def run(main,wram,numerator,denominator,index,budget=20000):
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Canonical ARM7 arithmetic input changed')
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);rng=random.Random(0x177000+index);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),STACK:rng.randbytes(0x4000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    returned=[False];visited=[];writes=[]
    def code(machine,pc,size,user):
        if pc==STOP:returned[0]=True;machine.emu_stop();return
        if not(WRAM<=pc<WRAM+len(wram)or MAIN<=pc<MAIN+len(main)):raise ValueError('Canonical unsigned helper escaped native input modules')
        visited.append([pc,size,machine.reg_read(UC_ARM_REG_CPSR)&32])
    def write(machine,access,address,width,value,user):
        if not(STACK<=address and address+width<=STACK+0x4000):raise ValueError('Canonical unsigned helper wrote outside private stack')
        writes.append([address,width,value&((1<<(8*width))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:4]=[numerator&0xffffffff,numerator>>32,denominator&0xffffffff,denominator>>32];initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    cpu.emu_start(ENTRY,STOP+4,count=budget)
    if not returned[0]:raise ValueError('Canonical unsigned helper did not actually return')
    registers=[cpu.reg_read(r)for r in REGISTERS];quotient=registers[0]|(registers[1]<<32);remainder=registers[2]|(registers[3]<<32)
    return dict(numerator=numerator,denominator=denominator,actualOwnReturn=True,quotient=quotient,observedR2R3=remainder,calleeSaved=registers[4:12]==initial[4:12]and registers[13:]==initial[13:],nonstackUnchanged=all(bytes(cpu.mem_read(a,len(raw)))==raw for a,raw in regions.items()if a!=STACK),registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),writes=writes,visited=visited,instructions=len(visited),providers=[],sourceCredit=0)
