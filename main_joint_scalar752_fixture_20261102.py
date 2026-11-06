import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=0x02000000,0x02400000,0x03030000,0x0F000000
SPANS={0x02032B90:348,0x02032ED4:404}
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def inputs(index):
    rng=random.Random(0x752+index);page=bytearray(rng.randbytes(16384));pair=bool(index%2)
    mode=(index//2)%4;narrow=bool((index//8)%2);wrap=bool((index//16)%2)
    frames=[1,2,3,5,8,9,16,33][(index//32)%8];end=frames-1
    frame=[0,end//2,end,max(0,end-1)][(index//256)%4];fraction=[0,1,2047,4095][(index//1024)%4]
    last=rng.choice([0,end,frames,frame,2*(frame//2),4*(frame//4)])
    info=(mode<<30)|(0x20000000 if narrow else 0)|(last<<16)|rng.randrange(65536)
    struct.pack_into('<II',page,0x900,info,0x1000)
    struct.pack_into('<HHIII',page,0x1004,frames,rng.randrange(65),(rng.getrandbits(32)&~2)|(2 if wrap else 0),0,0)
    width=2 if narrow else 4;channels=2 if pair else 1
    samples=[[rng.randrange(-32768,32768)for _ in range(channels)]for _ in range(128)]
    for i,values in enumerate(samples):struct.pack_into('<'+('h'if narrow else'i')*channels,page,0x2000+i*width*channels,*values)
    stride=1 if mode==0 else 2 if mode&1 else 4
    if frame==end:
        left=frame//stride+frame%stride
        right=0 if wrap else left;remainder=fraction if wrap else 0;divisor=4096
    elif stride==1:left=frame;right=left+1;remainder=fraction;divisor=4096
    elif frame<last:left=frame//stride;right=left+1;remainder=(frame%stride)*4096+fraction;divisor=4096*stride
    else:
        left=last//2 if stride==2 else frame//4+frame%4;right=left+1;remainder=fraction;divisor=4096
    output=[samples[left][c]+((samples[right][c]-samples[left][c])*remainder//divisor)for c in range(channels)]
    expected=bytearray(page);struct.pack_into('<'+'i'*channels,expected,0x800,*output)
    entry=0x02032ED4 if pair else 0x02032B90;args=[DATA+0x800,frame*4096+fraction,DATA+0x900,DATA+0x1000]
    context=dict(pair=pair,mode=mode,narrow=narrow,wrap=wrap,frames=frames,frame=frame,fraction=fraction,last=last,left=left,right=right,
     expectedOutput=output,subtractionProductSigned32Representable=True,encodedAssetValidityProven=False)
    return page,bytes(expected),entry,args,context


def execute(image,bodies,index,bound=5000):
    page,expected,entry,args,context=inputs(index);rng=random.Random(0x752F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(REGS,args):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];returned=False
    def code(uc,address,size,user):
        nonlocal returned
        if address==STOP:returned=True;uc.emu_stop();return
        assert any(base<=address<base+n for base,n in SPANS.items()),hex(address);seen.add(address)
    def read(uc,access,address,size,value,user):reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        assert DATA<=address and address+size<=DATA+16384 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096
    output=bytes(machine.mem_read(DATA,16384))
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    return dict(index=index,entry=entry,args=args,context=context,actualReturn=True,modelPassed=output==expected,
     registers=[machine.reg_read(r)for r in REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),functionProviders=0)
