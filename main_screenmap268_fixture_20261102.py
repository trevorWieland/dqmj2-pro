import hashlib
import random
import struct
import main_joint_scalar752_fixture_20261102 as scalar
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=scalar.BASE,scalar.DATA,scalar.STACK,scalar.STOP
SPANS={0x020363D0:176,0x02036480:92}


def inputs(index):
    rng=random.Random(0x268+index);page=bytearray(rng.randbytes(32768));text=bool(index%2)
    palette=index//2%16;character=[0,1,1023,65535][index//32%4];base=0x1000
    if text:
        stride=[32,64][index//128%2];left=rng.choice([0,1,30,31,32,33,63])%stride;top=rng.choice([0,1,30,31,32,33,63])
        width=rng.randrange(min(12,stride-left)+1);height=rng.randrange(min(12,64-top)+1)
        args=[DATA+base,width,height,left,top,stride,character,palette];entry=0x020363D0
    else:
        stride=[16,32,64,128][index//128%4];left=top=0;width=rng.randrange(min(12,stride)+1);height=rng.randrange(13)
        args=[DATA+base,width,height,stride,character,palette];entry=0x02036480
    expected=bytearray(page)
    for row in range(height):
        for col in range(width):
            x=left+col;y=top+row
            cell=(y//32)*(stride//32)*1024+(x//32)*1024+(y%32)*32+x%32 if text and stride==64 else y*stride+x
            value=((palette<<12)|(character+row*width+col))&65535
            struct.pack_into('<H',expected,base+cell*2,value)
    context=dict(text=text,palette=palette,character=character,stride=stride,left=left,top=top,width=width,height=height)
    return page,bytes(expected),entry,args,context


def execute(image,bodies,index,bound=50000):
    page,expected,entry,args,context=inputs(index);rng=random.Random(0x268F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,32768);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_write(STACK+4096,struct.pack('<'+'I'*len(args[4:]),*args[4:]))
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in scalar.REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(scalar.REGS,args[:4]):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];pending=[];helpers=0;returned=False
    def code(uc,address,size,user):
        nonlocal returned,helpers
        if pending and address==pending[-1]:pending.pop();helpers+=1
        if address==0x02036480 and entry!=address:pending.append(uc.reg_read(UC_ARM_REG_LR))
        if address==STOP:assert not pending;returned=True;uc.emu_stop();return
        assert any(base<=address<base+n for base,n in SPANS.items()),hex(address);seen.add(address)
    def read(uc,access,address,size,value,user):reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        assert DATA<=address and address+size<=DATA+32768 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096;output=bytes(machine.mem_read(DATA,32768))
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    return dict(index=index,entry=entry,args=args,context=context,actualReturn=True,modelPassed=output==expected,
     registers=[machine.reg_read(r)for r in scalar.REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),actualNestedHelperReturns=helpers,functionProviders=0)
