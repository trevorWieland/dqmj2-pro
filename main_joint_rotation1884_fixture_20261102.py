import hashlib
import math
import random
import struct
import main_joint_scalar752_fixture_20261102 as scalar
from joint_math_hardware_20261102 import JointMathHardware
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=scalar.BASE,scalar.DATA,scalar.STACK,scalar.STOP
OWN={0x02033068:1048,0x02033480:836}
HELPERS={0x02002618:280,0x020337C4:364}
SPANS={**OWN,**HELPERS}


class DegenerateRotation(ValueError):
    pass


def normalize(values):
    squared=sum(v*v for v in values)
    if not squared:raise DegenerateRotation('Synthetic interpolated axis is zero; division-by-zero hardware is outside this fixture')
    coefficient=((1<<56)//squared)*math.isqrt(4*squared)
    assert all(-(1<<63)<=coefficient*v+(1<<44)<1<<63 for v in values)
    return[(coefficient*v+(1<<44))//(1<<45)for v in values]


def cross(a,b):
    return[(a[1]*b[2]-a[2]*b[1])//4096,(a[2]*b[0]-a[0]*b[2])//4096,(a[0]*b[1]-a[1]*b[0])//4096]


def decode(info,triples,quintuples):
    index=info&32767
    if info&32768:
        header,a,b=triples[index];pivot=header&15;flags=header>>4;matrix=[0]*9
        matrix[pivot]=-4096 if flags&1 else 4096
        positions=[r*3+c for r in range(3)for c in range(3)if r!=pivot//3 and c!=pivot%3]
        for at,value in zip(positions,[a,b,-b if flags&2 else b,-a if flags&4 else a]):matrix[at]=value
        return matrix,False
    code=quintuples[index];packed=0
    for value in[code[4],code[0],code[1],code[2],code[3]]:packed=packed*8+(value&7)
    packed&=8191
    return[code[0]//8,code[1]//8,code[2]//8,code[3]//8,code[4]//8,packed-8192 if packed&4096 else packed,0,0,0],True


def result_model(indices,weights,divisor,triples,quintuples):
    decoded=[decode(i,triples,quintuples)for i in indices]
    do_cross=any(flag for matrix,flag in decoded)
    if len(indices)==1:
        matrix=list(decoded[0][0]);matrix[6:9]=cross(matrix[:3],matrix[3:6])if do_cross else normalize(matrix[6:9])
    else:
        matrix=[sum(row[c]*w for(row,flag),w in zip(decoded,weights))//divisor for c in range(9)]
        matrix[:3]=normalize(matrix[:3]);matrix[3:6]=normalize(matrix[3:6])
        matrix[6:9]=cross(matrix[:3],matrix[3:6])if do_cross else normalize(matrix[6:9])
    return matrix


def inputs(index):
    rng=random.Random(0x1884+index);page=bytearray(rng.randbytes(32768));fractional=bool(index%2)
    mode=index//2%4;wrap=bool(index//8%2);frames=[1,2,3,5,8,9,17,33][index//16%8];end=frames-1
    frame=[0,end//2,end,max(0,end-1)][index//128%4];fraction=[0,1,2047,4095][index//512%4]
    last=rng.choice([0,end,frame,2*(frame//2),4*(frame//4)]);info=(mode<<30)|(last<<16)
    struct.pack_into('<II',page,0x900,info,0x1000);struct.pack_into('<HHIII',page,0x1004,frames,32,2 if wrap else 0,0x2000,0x3000)
    triples=[(i%9|(rng.randrange(8)<<4),rng.randrange(1,4097),rng.randrange(-4096,4097))for i in range(32)]
    quintuples=[tuple(rng.randrange(-32768,32768)for _ in range(5))for i in range(32)]
    codes=[rng.randrange(32)|(0x8000 if rng.randrange(2)else 0)for _ in range(128)]
    struct.pack_into('<'+'h'*96,page,0x3000,*[v for row in triples for v in row])
    struct.pack_into('<'+'h'*160,page,0x4000,*[v for row in quintuples for v in row])
    struct.pack_into('<'+'H'*128,page,0x2000,*codes)
    step=1 if mode==0 else 2 if mode&1 else 4;remainder=frame%step
    if fractional:
        if frame==end and not wrap:indices=[frame//step+remainder];weights=[1];divisor=1
        else:
            if frame==end:left=frame//step+remainder;right=0;rem=fraction;stride=1
            elif step==1:left=frame;right=left+1;rem=fraction;stride=1
            elif frame<last:left=frame//step;right=left+1;rem=remainder*4096+fraction;stride=step
            else:left=last//2 if step==2 else frame//4+frame%4;right=left+1;rem=fraction;stride=1
            indices=[left,right];weights=[stride*4096-rem,rem];divisor=4096
    elif remainder and frame>last:indices=[last//step+remainder];weights=[1];divisor=1
    elif remainder:
        indices=[frame//step,frame//step+1]
        weights=[1,1]if step==2 or remainder==2 else[step-remainder,remainder];divisor=1
    else:indices=[frame//step];weights=[1];divisor=1
    matrix=result_model([codes[i]for i in indices],weights,divisor,triples,quintuples)
    expected=bytearray(page);struct.pack_into('<9i',expected,0x800,*matrix)
    entry=0x02033480 if fractional else 0x02033068;args=[DATA+0x800,frame*4096+fraction,DATA+0x900,DATA+0x1000]
    context=dict(fractional=fractional,mode=mode,wrap=wrap,frames=frames,frame=frame,fraction=fraction,last=last,
     indices=indices,codes=[codes[i]for i in indices],weights=weights,divisor=divisor,expectedMatrix=matrix,
     encodedAssetValidityProven=False)
    return page,bytes(expected),entry,args,context


def execute(image,bodies,index,bound=12000):
    page,expected,entry,args,context=inputs(index);rng=random.Random(0x1884F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,32768);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_map(0x04000000,4096);hardware=JointMathHardware(machine)
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in scalar.REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(scalar.REGS,args):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];returned=False;pending=[];helper_returns=[]
    def code(uc,address,size,user):
        nonlocal returned
        if pending and address==pending[-1][1]:helper_returns.append(pending.pop()[0])
        if address in HELPERS:pending.append((address,uc.reg_read(UC_ARM_REG_LR)))
        if address==STOP:assert not pending;returned=True;uc.emu_stop();return
        assert any(base<=address<base+n for base,n in SPANS.items()),hex(address);seen.add(address)
    def read(uc,access,address,size,value,user):
        if 0x04000000<=address<0x04001000:hardware.read(address,size)
        reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        if 0x04000000<=address<0x04001000:hardware.write(address,size,value)
        else:assert DATA<=address and address+size<=DATA+32768 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096;hardware.verify();output=bytes(machine.mem_read(DATA,32768))
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    return dict(index=index,entry=entry,args=args,context=context,actualReturn=True,modelPassed=output==expected,
     registers=[machine.reg_read(r)for r in scalar.REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(output).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),functionProviders=0,hardwareOperations=hardware.operations,actualHelperReturns=helper_returns)
