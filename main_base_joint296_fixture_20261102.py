import hashlib
import random
import struct
import main_joint_scalar752_fixture_20261102 as scalar
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=scalar.BASE,scalar.DATA,scalar.STACK,scalar.STOP
SPANS={0x020323DC:152,0x02032474:144}
PROVIDER=STOP+0x100
GLOBAL=0x020EE1F4


def inputs(index):
    rng=random.Random(0x296+index);page=bytearray(rng.randbytes(16384));entry=list(SPANS)[index%2]
    node_index=index//2%8;flags=index//16%16|((index//256%16)<<12);node=0x3000+0x100+node_index*128
    struct.pack_into('<I',page,0x2000,DATA+0x80);struct.pack_into('<I',page,0x2000+212,DATA+0x3000)
    struct.pack_into('<I',page,0x2000+232,PROVIDER);page[0x81]=node_index;page[0x3001]=8
    struct.pack_into('<H',page,0x3006,0x20);struct.pack_into('<HH',page,0x3020,4,0)
    for i in range(8):struct.pack_into('<I',page,0x3024+i*4,0x100+i*128)
    struct.pack_into('<H',page,node,flags)
    expected=bytearray(page);args=[DATA+0x1000];calls=[]
    if entry==0x020323DC:
        if flags&1:
            old=struct.unpack_from('<I',expected,0x1000)[0];struct.pack_into('<I',expected,0x1000,old|4)
        else:expected[0x104C:0x1058]=page[node+4:node+16]
    else:
        payload=node+4+(0 if flags&1 else 12)+(0 if flags&2 else(4 if flags&8 else 16))
        calls=[dict(args=[DATA+0x1000,DATA+payload,DATA+0x80,flags],payload=list(struct.unpack_from('<6i',page,payload)))]
    return page,bytes(expected),entry,args,dict(nodeIndex=node_index,nodeFlags=flags,expectedCalls=calls)


def execute(image,bodies,index,bound=50000):
    page,expected,entry,args,context=inputs(index);rng=random.Random(0x296F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image);machine.mem_write(GLOBAL,struct.pack('<I',DATA+0x2000))
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_write(STACK+4096,struct.pack('<'+'I'*len(args[4:]),*args[4:]))
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in scalar.REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(scalar.REGS,args[:4]):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];pending=[];helpers=0;returned=False;calls=[]
    def code(uc,address,size,user):
        nonlocal returned,helpers
        if address==PROVIDER:
            arguments=[uc.reg_read(r)for r in scalar.REGS[:4]]
            assert DATA<=arguments[1]and arguments[1]+24<=DATA+16384
            calls.append(dict(args=arguments,payload=list(struct.unpack('<6i',bytes(uc.mem_read(arguments[1],24))))))
            for r in scalar.REGS[:4]:uc.reg_write(r,rng.getrandbits(32))
            uc.reg_write(UC_ARM_REG_CPSR,(uc.reg_read(UC_ARM_REG_CPSR)&0x0FFFFFFF)|rng.choice([0,0x80000000,0xF0000000]))
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR));return
        if address==STOP:assert not pending;returned=True;uc.emu_stop();return
        assert any(base<=address<base+n for base,n in SPANS.items()),hex(address);seen.add(address)
    def read(uc,access,address,size,value,user):reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        assert DATA<=address and address+size<=DATA+16384 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096;output=bytes(machine.mem_read(DATA,16384))
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    assert struct.unpack('<I',bytes(machine.mem_read(GLOBAL,4)))[0]==DATA+0x2000
    return dict(index=index,entry=entry,args=args,context=context,actualReturn=True,modelPassed=output==expected and calls==context['expectedCalls'],
     registers=[machine.reg_read(r)for r in scalar.REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),suppliedCalls=calls,functionProviders=len(calls))
