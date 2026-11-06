import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,OVERLAY,ENTRY,SIZE,PRIVATE=0x02000000,0x021D7240,0x021EB240,1000,0x02650000
STACK,STOP,GLOBAL=0x027F0000,0x027FF800,0x0220D3B8
RECORD,STATS,TEXT_A,TEXT_B=0x02610000,0x02611000,0x02612000,0x02613000
ARITIES={0x020685F0:1,0x0206877C:1,0x021E75EC:1,0x021E749C:5,0x021E7B64:1,0x021E7824:7,0x021E791C:7,0x021E796C:4,0x0220769C:1,0x021E92BC:1,0x021E78AC:8,0x021E775C:7}
REGS=c.REGISTERS[:13]


def inputs():
    main,arm,unused=measured_module('main');module,overlay,unused=measured_module('ov006')
    if main['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or module['sha256']!='fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341':raise ValueError('712 images differ')
    return dict(main=main,arm=arm,module=module,overlay=overlay)


class Machine:
    def __init__(self,original,profile,body=None,private=False):
        self.p,self.code=profile,PRIVATE if private else ENTRY
        self.extent=len(body)if body is not None else SIZE
        if not private and self.extent>SIZE:raise ValueError('712 canonical body would overlap next native function')
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,original['arm']);self.u.mem_write(OVERLAY,original['overlay'])
        if body is not None:self.u.mem_write(self.code,body)
        self.u.mem_write(RECORD,bytes(profile['record']));self.u.mem_write(STATS,struct.pack('<3I',*profile['stats']));self.u.mem_write(GLOBAL+8,struct.pack('<I',profile['recordWord']))
        self.initial=[0xA7120000+index*256 for index in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0xA0000010)
        for register,value in zip(REGS,self.initial):self.u.reg_write(register,value)
        self.u.reg_write(UC_ARM_REG_R0,profile['resetWord']);self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP)
        self.before=bytes(self.u.mem_read(BASE,0x800000));self.providers,self.own,self.instructions=[],set(),0
        self.u.hook_add(UC_HOOK_CODE,self.observe);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)

    def write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+256:raise ValueError(('712 unexpected nonstack write',hex(address),size))

    def observe(self,u,address,length,data):
        self.instructions+=1
        if self.code<=address<self.code+self.extent:self.own.add(address);return
        if address not in ARITIES:raise ValueError(('712 unexpected native PC outside provided interface',hex(address)))
        words=[u.reg_read(reg)for reg in REGS[:4]];arity=ARITIES[address];prepared=words[:min(4,arity)]
        if arity>4:prepared+=list(struct.unpack('<'+'I'*(arity-4),bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP),(arity-4)*4))))
        value=0xE7120000|(address&65535)
        if address==0x020685F0:value=RECORD
        elif address==0x0206877C:value=STATS
        elif address==0x0220769C:value=TEXT_A
        elif address==0x021E92BC:value=TEXT_B
        elif address==0x021E791C and prepared==[46,0x02208510,23,0,5,1,0]:value=self.p['returnWord']
        self.providers.append(dict(entry=address,preparedWords=prepared,rawRegisterWords=words,providedR0=value,ramEffects=[]))
        u.reg_write(UC_ARM_REG_R0,value)
        for register,index in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(register,0xDE120000|index)
        lr=u.reg_read(UC_ARM_REG_LR);u.reg_write(UC_ARM_REG_CPSR,(u.reg_read(UC_ARM_REG_CPSR)&~0xF0000020)|0x60000000|(32 if lr&1 else 0));u.reg_write(UC_ARM_REG_PC,lr&~1)

    def run(self):
        self.u.emu_start(self.code,STOP,count=10000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(reg)for reg in REGS[4:12]]!=self.initial[4:12]:raise ValueError('712 did not actually return preserving frame')
        result=dict(profile=self.p,before=self.before,after=bytes(self.u.mem_read(BASE,0x800000)),coreRegistersAndCpsr=[self.u.reg_read(reg)for reg in REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],providedCalls=self.providers,ownObserved=sorted(self.own),instructions=self.instructions)
        self.u=None;gc.collect();return result
