import hashlib
import random
import struct
import main_joint_scalar752_fixture_20261102 as scalar
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=scalar.BASE,scalar.DATA,scalar.STACK,scalar.STOP
ENTRY,READER=0x02035788,0x02034AB8
SPANS={ENTRY:576,READER:96}


def inputs(index):
    rng=random.Random(0x576+index);page=bytearray(rng.randbytes(16384));dst_bpp=8 if index%2 else 4
    src_bpp=[1,2,4,8][index//2%4];src_bpp=min(src_bpp,dst_bpp)
    x=[-7,0,3,7][index//8%4];y=[-7,0,3,7][index//32%4]
    if index%257==0:y=8
    if index%257==1:x=8
    width=rng.randrange(max(1,1-x),17);height=rng.randrange(max(1,1-y),17);stride=width*src_bpp+rng.randrange(8)
    color=rng.randrange((1<<dst_bpp)-(1<<src_bpp)+1);tile=0x800;glyph=0x1000
    struct.pack_into('<II7iI',page,0x400,DATA+tile,DATA+glyph,x,y,width,height,stride,src_bpp,dst_bpp,color)
    expected=bytearray(page);writes=0
    for dy in range(max(0,y),min(8,y+height)):
        for dx in range(max(0,x),min(8,x+width)):
            position=(dy-y)*stride+(dx-x)*src_bpp;value=0
            for k in range(src_bpp):value=value*2+((page[glyph+(position+k)//8]>>(7-(position+k)%8))&1)
            if value:
                offset=tile+dy*dst_bpp+dx*dst_bpp//8;shift=(dx*dst_bpp)%8;mask=((1<<dst_bpp)-1)<<shift
                expected[offset]=(expected[offset]&~mask)|((color+value)<<shift);writes+=1
    return page,bytes(expected),[DATA+0x400],dict(dstBpp=dst_bpp,srcBpp=src_bpp,x=x,y=y,width=width,height=height,
     glyphStrideBits=stride,color=color,nontransparentPixels=writes,validPaletteSum=True)


def execute(image,bodies,index,bound=30000):
    page,expected,args,context=inputs(index);rng=random.Random(0x576F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in scalar.REGS:machine.reg_write(reg,rng.getrandbits(32))
    machine.reg_write(UC_ARM_REG_R0,args[0]);machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];pending=[];helpers=0;returned=False
    def code(uc,address,size,user):
        nonlocal returned,helpers
        if pending and address==pending[-1]:pending.pop();helpers+=1
        if address==READER:pending.append(uc.reg_read(UC_ARM_REG_LR))
        if address==STOP:assert not pending;returned=True;uc.emu_stop();return
        assert any(base<=address<base+n for base,n in SPANS.items()),hex(address);seen.add(address)
    def read(uc,access,address,size,value,user):reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        assert DATA<=address and address+size<=DATA+16384 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(ENTRY,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096;output=bytes(machine.mem_read(DATA,16384))
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    return dict(index=index,args=args,context=context,actualReturn=True,modelPassed=output==expected,
     registers=[machine.reg_read(r)for r in scalar.REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),actualBitReaderReturns=helpers,functionProviders=0)
