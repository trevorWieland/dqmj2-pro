import hashlib
import random
import struct
import main_joint_scalar752_fixture_20261102 as scalar
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=scalar.BASE,scalar.DATA,scalar.STACK,scalar.STOP
SPANS={0x02008C58:76,0x02035D70:80,0x02035DC0:128}


def inputs(index):
    rng=random.Random(0x284+index);page=bytearray(rng.randbytes(16384));base=0x1000;kind=index%3
    entry=list(SPANS)[kind];expected=bytearray(page)
    if kind==0:
        size=(index//3%257)*4;value=[0,0xFFFFFFFF,0x89ABCDEF,rng.getrandbits(32)][index//771%4]
        args=[value,DATA+base,size];ranges=[(base,size)];context=dict(kind=kind,size=size,value=value)
    else:
        width=index//3%17;height=index//51%9;bpp=[4,8][index//459%2];palette=index//918%(1<<bpp);stride=width+index//1836%8
        struct.pack_into('<IiiB3xII',page,0x100,DATA+base,width,height,bpp,stride,DATA+0x80);expected=bytearray(page)
        value=palette*(0x11111111 if bpp==4 else 0x01010101);args=[DATA+0x100,palette]
        ranges=[(base,width*height*8*bpp)]if kind==1 else[(base+row*stride*8*bpp,width*8*bpp)for row in range(height)]
        context=dict(kind=kind,width=width,height=height,bpp=bpp,palette=palette,stride=stride)
    for offset,size in ranges:
        assert offset+size<=len(page)
        expected[offset:offset+size]=struct.pack('<I',value)*(size//4)
    return page,bytes(expected),entry,args,context


def execute(image,bodies,index,bound=50000):
    page,expected,entry,args,context=inputs(index);rng=random.Random(0x284F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_write(STACK+4096,struct.pack('<'+'I'*len(args[4:]),*args[4:]))
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in scalar.REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(scalar.REGS,args[:4]):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];pending=[];helpers=0;returned=False
    def code(uc,address,size,user):
        nonlocal returned,helpers
        if pending and address==pending[-1]:pending.pop();helpers+=1
        if address==0x02008C58 and entry!=address:pending.append(uc.reg_read(UC_ARM_REG_LR))
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
    return dict(index=index,entry=entry,args=args,context=context,actualReturn=True,modelPassed=output==expected,
     registers=[machine.reg_read(r)for r in scalar.REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),actualNestedHelperReturns=helpers,functionProviders=0)
