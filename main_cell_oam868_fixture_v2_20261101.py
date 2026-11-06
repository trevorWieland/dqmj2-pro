import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY,DATA,STACK,STOP=0x0203519C,0x02400000,0x03030000,0x0F000000
R=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
WIDTHS=[[8,16,32,64],[16,32,32,64],[8,8,16,32]]
HEIGHTS=[[8,16,32,64],[8,8,16,32],[16,32,32,64]]
MATRICES=[None,(4096,0,0,4096),(0,4096,-4096,0),(2048,0,0,8192),
 (-4096,0,0,4096),(4096,1024,-2048,4096),(0,0,0,0)]
TRANSLATIONS=[None,(0,0),(2048,-2048),(8192,-12288),(2047,-2049),(1048576,-524288)]


def execute(image,body,index,bound=32768):
    rng=random.Random(0x3519C00000+index)
    count=[0,1,2,3,4,8,16][index%7]
    capacity=[0,1,2,3,8,16,65535][(index//7)%7]
    matrix=MATRICES[(index//49)%7]
    translation=TRANSLATIONS[(index//13)%6]
    affine=[0,1,15,31][(index//5)%4];double=[0,1,2,0x80000000,0xFFFFFFFF][index%5]
    copied=min(count,capacity)
    page=bytearray(rng.randbytes(16384));cell=DATA+0x100;mat=DATA+0x200;trans=DATA+0x300
    source=DATA+0x1000;destination=DATA+0x3000
    struct.pack_into('<HHI',page,0x100,count,rng.randrange(65536),source)
    if matrix:struct.pack_into('<4i',page,0x200,*matrix)
    if translation:struct.pack_into('<2i',page,0x300,*translation)
    attributes=[]
    for item in range(count):
        shape=(index+item)%3;size=(index//3+item)%4;effect=(index//12+item)%4
        x=[0,1,127,255,256,384,511][(index+item)%7]
        y=[0,1,127,128,255][(index//7+item)%5]
        a0=(rng.randrange(65536)&~0xC3FF)|y|(effect<<8)|(shape<<14)
        a1=(rng.randrange(65536)&~0xC1FF)|x|(size<<14);a2=rng.randrange(65536)
        struct.pack_into('<3H',page,0x1000+item*6,a0,a1,a2);attributes.append([a0,a1,a2])
    expected=bytearray(page)
    for item,(a0,a1,a2)in enumerate(attributes[:copied]):
        value=a0|(a1<<16)
        if matrix is not None or translation is not None:
            x=(a1&511);x=x-512 if x>255 else x
            y=a0&255;y=y-256 if y>127 else y
            fx=x*4096;fy=y*4096
            shape=(a0>>14)&3;size=(a1>>14)&3
            halfw=WIDTHS[shape][size]//2;halfh=HEIGHTS[shape][size]//2
            if matrix is not None:
                if(a0&0x300)==0x300:fx+=halfw*4096;fy+=halfh*4096
                m00,m01,m10,m11=matrix
                original_x,original_y=fx,fy
                fx=(m00*original_x+m10*original_y+4096)>>12
                fy=(m01*original_x+m11*original_y+4096)>>12
                effect=0x300 if double else 0x100
                value=(value&~(0x300|0x3E000000))|effect|(affine<<25)
                fx+=-halfw*4096+m00*halfw+m10*halfh
                fy+=-halfh*4096+m01*halfw+m11*halfh
                if double:fx-=halfw*4096;fy-=halfh*4096
            if translation is not None:fx+=translation[0];fy+=translation[1]
            x=(fx+2048)>>12;y=(fy+2048)>>12
            value=(value&~(0xFF|0x1FF0000))|(y&255)|((x&511)<<16)
        struct.pack_into('<IH',expected,0x3000+item*8,value&0xFFFFFFFF,a2)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image);machine.mem_write(ENTRY,body)
    before_main=bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(page))
    machine.mem_map(STACK,4096);stack=bytearray(rng.randbytes(4096))
    struct.pack_into('<3I',stack,2048,trans if translation is not None else 0,affine,double)
    machine.mem_write(STACK,bytes(stack));machine.mem_map(STOP,4096)
    initial=[rng.getrandbits(32)for register in R]
    for register,value in zip(R,initial):machine.reg_write(register,value)
    for register,value in zip(R,[destination,capacity,cell,mat if matrix is not None else 0]):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    own=set();reads=[];writes=[]
    def code(uc,address,size,unused):
        assert ENTRY<=address<ENTRY+len(body),hex(address)
        own.add(address)
    def read(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:return
        assert 0x02000000<=address and address+size<=0x02100000 or DATA<=address and address+size<=DATA+16384,hex(address)
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:assert STACK+1856<=address and address+size<=STACK+2048,(hex(address),size,hex(value),hex(uc.reg_read(UC_ARM_REG_PC)))
        else:
            assert destination<=address and address+size<=destination+copied*8,hex(address)
            writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(ENTRY,STOP,count=bound)
    assert machine.reg_read(UC_ARM_REG_PC)==STOP,'Bounded prefix is not actual return'
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(register)==value for register,value in zip(R[4:12],initial[4:12]))
    assert bytes(machine.mem_read(0x02000000,0x100000))==before_main
    after=bytes(machine.mem_read(DATA,16384));after_stack=bytes(machine.mem_read(STACK,4096))
    assert after_stack[:1856]==stack[:1856]and after_stack[2048:]==stack[2048:]
    result=machine.reg_read(UC_ARM_REG_R0);passed=after==expected and result==copied
    return dict(index=index,actualReturn=True,modelPassed=passed,count=count,capacity=capacity,matrix=matrix,
        translation=translation,affine=affine,double=double,result=result,expectedCount=copied,
        registers=[machine.reg_read(register)for register in R],cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),
        reads=reads,writes=writes,ownedObserved=sorted(own),providedCalls=0,actualHelperReturns=0,
        pageSha256=hashlib.sha256(after).hexdigest(),stackSha256=hashlib.sha256(after_stack).hexdigest(),
        firstMismatchingByte=next((i for i,(a,b)in enumerate(zip(after,expected))if a!=b),None))
