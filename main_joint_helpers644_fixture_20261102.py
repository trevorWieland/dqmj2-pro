import hashlib
import math
import random
import struct
import main_joint_scalar752_fixture_20261102 as scalar
from joint_math_hardware_20261102 import JointMathHardware
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=scalar.BASE,scalar.DATA,scalar.STACK,scalar.STOP
SPANS={0x02002618:280,0x020337C4:364}


def inputs(index):
    rng=random.Random(0x644+index);page=bytearray(rng.randbytes(16384));decode=bool(index%2);context={}
    if decode:
        pivot=bool(index//2%2);element=index//4%32;flags=index//128%8;pivot_index=index//1024%9
        triples=[];quintuples=[]
        for i in range(32):
            triples.append((pivot_index|(flags<<4),rng.randrange(-4096,4097),rng.randrange(-4096,4097)))
            quintuples.append(tuple(rng.randrange(-32768,32768)for _ in range(5)))
        struct.pack_into('<'+'h'*96,page,0x1000,*[v for row in triples for v in row])
        struct.pack_into('<'+'h'*160,page,0x2000,*[v for row in quintuples for v in row])
        matrix=list(struct.unpack_from('<9i',page,0x800));info=(0x8000 if pivot else 0)|element
        if pivot:
            matrix=[0]*9;header,a,b=triples[element];matrix[pivot_index]=-4096 if flags&1 else 4096
            remaining=[r*3+c for r in range(3)for c in range(3)if r!=pivot_index//3 and c!=pivot_index%3]
            for at,value in zip(remaining,[a,b,-b if flags&2 else b,-a if flags&4 else a]):matrix[at]=value
            result=0
        else:
            code=quintuples[element];matrix[:6]=[code[i]//8 for i in range(5)]+[0]
            packed=0
            for value in[code[4],code[0],code[1],code[2],code[3]]:packed=packed*8+(value&7)
            packed&=8191;matrix[4]=code[4]//8;matrix[5]=packed-8192 if packed&4096 else packed;result=1
        expected=bytearray(page);struct.pack_into('<9i',expected,0x800,*matrix)
        entry=0x020337C4;args=[DATA+0x800,DATA+0x1000,DATA+0x2000,info]
        context=dict(decode=True,pivot=pivot,element=element,flags=flags,pivotIndex=pivot_index,expectedReturn=result,expectedMatrix=matrix)
    else:
        edges=[(4096,0,0),(-4096,0,0),(0,4096,0),(0,0,-4096),(1,1,1),(-1,-1,-1),(32767,-32768,0)]
        vector=edges[index//2%len(edges)]if index//2<56 else tuple(rng.randrange(-32768,32768)for _ in range(3))
        if not any(vector):vector=(1,0,0)
        struct.pack_into('<3i',page,0x800,*vector);same=bool(index//2%2);destination=0x800 if same else 0x900
        length=sum(v*v for v in vector);root=math.isqrt(4*length);coefficient=((1<<56)//length)*root
        output=[(coefficient*v+(1<<44))//(1<<45)for v in vector]
        expected=bytearray(page);struct.pack_into('<3i',expected,destination,*output)
        entry=0x02002618;args=[DATA+0x800,DATA+destination]
        context=dict(decode=False,vector=vector,sameDestination=same,expectedVector=output,lengthSquared=length,sqrtArgument=4*length)
    return page,bytes(expected),entry,args,context


def execute(image,bodies,index,bound=5000):
    page,expected,entry,args,context=inputs(index);rng=random.Random(0x644F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_map(0x04000000,4096);hardware=JointMathHardware(machine)
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in scalar.REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(scalar.REGS,args):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];returned=False
    def code(uc,address,size,user):
        nonlocal returned
        if address==STOP:returned=True;uc.emu_stop();return
        assert any(base<=address<base+n for base,n in SPANS.items()),hex(address);seen.add(address)
    def read(uc,access,address,size,value,user):
        if 0x04000000<=address<0x04001000:hardware.read(address,size)
        reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        if 0x04000000<=address<0x04001000:hardware.write(address,size,value)
        else:assert DATA<=address and address+size<=DATA+16384 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096;hardware.verify()
    assert len(hardware.operations)==(0 if context['decode']else 2)
    output=bytes(machine.mem_read(DATA,16384));passed=output==expected
    if context['decode']:passed=passed and machine.reg_read(UC_ARM_REG_R0)==context['expectedReturn']
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    return dict(index=index,entry=entry,args=args,context=context,actualReturn=True,modelPassed=passed,
     registers=[machine.reg_read(r)for r in scalar.REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),functionProviders=0,hardwareOperations=hardware.operations)
