import hashlib
import random
import struct
import main_joint_scalar752_fixture_20261102 as scalar
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=scalar.BASE,scalar.DATA,scalar.STACK,scalar.STOP
OWN={0x02035650:312,0x02035E40:412,0x02035FDC:500}
HELPERS={0x02008C58:76,0x0203553C:276}
SPANS={**OWN,**HELPERS}


def inputs(index):
    rng=random.Random(0x1224+index);page=bytearray(rng.randbytes(32768));kind=index%3;entry=list(OWN)[kind];base=0x1000
    if kind==0:
        bpp=4 if index//3%2==0 else 8;palette=[0,(1<<bpp)-1,rng.getrandbits(bpp)][index//6%3]
        x=rng.randrange(8)if bpp==4 else rng.randrange(4);y=rng.randrange(8)
        w=rng.randrange(1 if bpp==4 else 5-x,9-x);h=rng.randrange(9-y)
        if index//18%8==0:x=y=0;w=h=8
        value=palette*(0x11111111 if bpp==4 else 0x01010101);args=[DATA+base,x,y,w,h,value,bpp]
        width=height=1;stride=1;sw=sh=0
    else:
        bpp=4;palette=[0,15,rng.randrange(16)][index//3%3];width=[1,2,4,8][index//9%4];height=[1,2,4,8][index//36%4]
        stride=width+index//144%3;sw=index//432%(width.bit_length());sh=index//864%(height.bit_length())
        parameter=stride if kind==1 else sw|(sh<<8);struct.pack_into('<IiiB3xII',page,0x100,DATA+base,width,height,bpp,parameter,DATA+0x80)
        x=rng.randrange(width*8);y=rng.randrange(height*8);w=rng.randrange(1,width*8-x+1);h=rng.randrange(1,height*8-y+1)
        if index//2592%4==1:x=y=0;w=0
        if index//2592%4==2:x=y=0;h=0
        args=[DATA+0x100,palette,x,y,w,h]
    expected=bytearray(page)
    if kind==0 and bpp==4 and w!=8:
        assert all(0<=v<32 for v in(x*4,32-(w*4+x*4),32-w*4))
    if kind==0 and bpp==8 and not(w==8 and h==8):assert x<4 and x+w>4
    for py in range(y,y+h):
        for px in range(x,x+w):
            tx,ty=px//8,py//8
            if kind==0:tile=0
            elif kind==1:tile=ty*stride+tx
            else:
                ow,oh=1<<sw,1<<sh;tile=((ty//oh)*(width//ow)+(tx//ow))*ow*oh+(ty%oh)*ow+tx%ow
            bit=((py%8)*8+px%8)*bpp;at=base+tile*8*bpp+bit//8;mask=((1<<bpp)-1)<<(bit%8)
            expected[at]=(expected[at]&(~mask&255))|(palette<<(bit%8))
    return page,bytes(expected),entry,args,dict(kind=kind,bpp=bpp,palette=palette,x=x,y=y,w=w,h=h,width=width,height=height,stride=stride,baseWidthShift=sw,baseHeightShift=sh)


def execute(image,bodies,index,bound=50000):
    page,expected,entry,args,context=inputs(index);rng=random.Random(0x1224F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,32768);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_write(STACK+4096,struct.pack('<'+'I'*len(args[4:]),*args[4:]))
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in scalar.REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(scalar.REGS,args[:4]):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];pending=[];helpers=0;returned=False;source_helpers=0;native_helpers=0;helper_seen=set()
    def code(uc,address,size,user):
        nonlocal returned,helpers,source_helpers,native_helpers
        if pending and address==pending[-1][0]:
            unused,kind=pending.pop()
            if kind=='source':source_helpers+=1
            else:native_helpers+=1
        if address in SPANS and address!=entry:pending.append((uc.reg_read(UC_ARM_REG_LR),'source'if address in OWN else'native'))
        if address==STOP:assert not pending;returned=True;uc.emu_stop();return
        assert any(base<=address<base+n for base,n in SPANS.items()),hex(address)
        (seen if any(base<=address<base+n for base,n in OWN.items())else helper_seen).add(address)
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
     registers=[machine.reg_read(r)for r in[*scalar.REGS,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC]],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),actualSelectedNestedReturns=source_helpers,actualNativeHelperReturns=native_helpers,nativeHelperObserved=sorted(helper_seen),functionProviders=0)
