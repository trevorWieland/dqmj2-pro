import hashlib
import itertools
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x0203CB8C
THUNK=0x0203CC2C
DATA=0x02510000
STACK=0x03020000
STOP=0x0F000000
PROVIDERS={0x0202A8E0:'length',0x0202A250:'heap',0x0202A37C:'allocate',0x0202A818:'read',0x0202A498:'release'}


def cases():
    lengths=[0,1,2,3,4,7,8,31,128,0xFFFFFFFC,0xFFFFFFFD,0xFFFFFFFE,0xFFFFFFFF]
    for values in itertools.product(lengths,[0,1,0x80000000,0xFFFFFFFF],[0,1,0xFFFFFFFF],[False,True],[0,1,0x80000000,0xFFFFFFFF]):yield (*values,False)
    for values in itertools.product([0,1,7,128],[1,0xFFFFFFFF],[False,True],[0,1]):
        length,heap,allocate,reply=values;yield length,heap,0,allocate,reply,True


def execute(arm,case,tag,check=True):
    length,heap,selector,allocate,reply,thunk=case;path=DATA+0x100;buffer=DATA+0x800;current=(0x81234567+tag)&0xFFFFFFFF;actual_heap=current if heap==0xFFFFFFFF else heap
    arena=bytearray(bytes([tag&255])*4096);arena[0x100:0x10C]=b'fixture.bin\0';expected=bytearray(arena)
    protocol=[('length',[path])];result=0
    if length:
        if heap==0xFFFFFFFF:protocol.append(('heap',[]))
        protocol.append(('allocate',[actual_heap,(length+3)&0xFFFFFFFC,4 if selector==0 else 0xFFFFFFFC]))
        if allocate:
            protocol.append(('read',[path,buffer,length,0]));payload=bytes((tag+i*7)&255 for i in range(min(length,16)));expected[0x800:0x800+len(payload)]=payload
            if reply:result=buffer
            else:protocol.append(('release',[actual_heap,buffer]))
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address in [0x0203C000,DATA,STACK,STOP]:uc.mem_map(address,4096)
    uc.mem_map(0x0202A000,4096);uc.mem_write(0x0203C000,arm[0x3C000:0x3D000]);uc.mem_write(0x0202A000,arm[0x2A000:0x2B000]);uc.mem_write(DATA,bytes(arena));uc.mem_write(STACK,b'\xB7'*4096)
    uc.mem_protect(0x0203C000,4096,UC_PROT_READ|UC_PROT_EXEC);uc.mem_protect(0x0202A000,4096,UC_PROT_READ|UC_PROT_EXEC)
    for i,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA0110000+i*0x101+tag)&0xFFFFFFFF)
    for reg,value in zip(REGISTERS[:3],[path,heap,selector]):uc.reg_write(reg,value)
    uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,STACK+0xF00);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(reg) for reg in REGISTERS[4:12]];events=[];pcs=set();writes=[];state={'actualReturns':0,'providerCalls':0,'thunkToBodyEntries':0,'instructions':0};body_return=[]
    def code(machine,address,size,user):
        state['instructions']+=1
        if body_return and address==body_return[-1]:body_return.pop();state['thunkToBodyEntries']+=1
        if address==STOP:state['actualReturns']+=1;machine.emu_stop();return
        if address in PROVIDERS:
            name=PROVIDERS[address];arity={'length':1,'heap':0,'allocate':3,'read':4,'release':2}[name];args=[machine.reg_read(r) for r in REGISTERS[:arity]];events.append((name,args));state['providerCalls']+=1
            if name=='length':returned=length
            elif name=='heap':returned=current
            elif name=='allocate':returned=buffer if allocate else 0
            elif name=='read':
                assert args[1]==buffer and args[2]==length
                payload=bytes((tag+i*7)&255 for i in range(min(length,16)));machine.mem_write(buffer,payload);returned=reply
            else:returned=(0xDEAD0000+tag)&0xFFFFFFFF
            lr=machine.reg_read(UC_ARM_REG_LR)
            for index in [1,2,3,12]:machine.reg_write(REGISTERS[index],(0xC0710000+tag*17+index)&0xFFFFFFFF)
            machine.reg_write(UC_ARM_REG_CPSR,((tag*3&15)<<28)|0x1F);machine.reg_write(REGISTERS[0],returned);machine.reg_write(UC_ARM_REG_PC,lr);return
        assert ENTRY<=address<ENTRY+160 or thunk and THUNK<=address<THUNK+16,hex(address);pcs.add(address)
        if address==ENTRY and thunk:body_return.append(machine.reg_read(UC_ARM_REG_LR)&~1)
    def write(machine,access,address,size,value,user):
        assert STACK<=address and address+size<=STACK+4096;writes.append((address,size,value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.emu_start(THUNK if thunk else ENTRY,STOP+4,count=1000)
    assert state['actualReturns']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0xF00 and not body_return
    assert state['thunkToBodyEntries']==int(thunk) and [uc.reg_read(r) for r in REGISTERS[4:12]]==saved
    memory=bytes(uc.mem_read(DATA,4096));passed=events==protocol and uc.reg_read(REGISTERS[0])==result and memory==bytes(expected)
    if check:assert passed,(case,events,protocol,uc.reg_read(REGISTERS[0]),result)
    return {'actualReturn':True,'modelPassed':passed,'state':state,'events':events,'expectedEvents':protocol,'result':uc.reg_read(REGISTERS[0]),'expectedResult':result,'registers':[uc.reg_read(r) for r in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR),'pcs':sorted(pcs),'writes':writes,'memorySha256':hashlib.sha256(memory).hexdigest(),'stackSha256':hashlib.sha256(bytes(uc.mem_read(STACK,4096))).hexdigest()}
