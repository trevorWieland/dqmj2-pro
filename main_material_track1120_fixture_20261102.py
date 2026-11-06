import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=0x02000000,0x02400000,0x03030000,0x0F000000
SPANS={0x02033930:360,0x02033A98:236,0x02033D48:256,0x02033E48:268}
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def inputs(index):
    rng=random.Random(0x1120+index);page=bytearray(rng.randbytes(16384));kind=index%4
    mode=index//4%4;constant=bool(index//16%2);narrow=bool(index//32%2);frame=index//64%32
    last=[0,frame][index//2048%2];offset=0x1000
    if kind<2:
        constant_value=rng.randrange(65536);info=(mode<<30)|(last<<16)|(0x20000000 if constant else 0)
        info|=constant_value if constant else offset
        samples=[rng.randrange(65536 if kind==0 else 256)for _ in range(256)]
        struct.pack_into('<'+('H'if kind==0 else'B')*256,page,offset,*samples)
        args=[DATA,info,frame]
    else:
        constant_value=rng.getrandbits(32);info=(mode<<30)|last|(0x20000000 if constant else 0)|(0x10000000 if narrow else 0)
        samples=[[rng.randrange(-32768,32768)for _ in range(2 if kind==3 else 1)]for _ in range(256)]
        if kind==2:
            struct.pack_into('<'+('h'if narrow else'i')*256,page,offset,*[v[0]for v in samples])
        else:struct.pack_into('<'+'h'*512,page,offset,*[v for pair in samples for v in pair])
        args=[DATA,info,constant_value if constant else offset,frame]
    step=1 if mode==0 else 2 if mode&1 else 4;remainder=frame%step
    if remainder and frame>last:indices=[last//step+remainder];weights=[1];divisor=1
    elif remainder:indices=[frame//step,frame//step+1];weights=[step-remainder,remainder];divisor=step
    else:indices=[frame//step];weights=[1];divisor=1
    if constant:result=constant_value
    elif len(indices)==1:
        value=samples[indices[0]]
        result=value if kind<2 else value[0]if kind==2 else(value[0]&65535)|((value[1]&65535)<<16)
    elif kind==0:
        result=sum((sum(((samples[i]>>shift)&31)*w for i,w in zip(indices,weights))//divisor)<<shift for shift in[0,5,10])
    elif kind==1:result=sum(samples[i]*w for i,w in zip(indices,weights))//divisor
    else:
        values=[sum(samples[i][c]*w for i,w in zip(indices,weights))//divisor for c in range(2 if kind==3 else 1)]
        result=values[0]if kind==2 else(values[0]&65535)|((values[1]&65535)<<16)
    context=dict(kind=kind,mode=mode,constant=constant,narrow=narrow,frame=frame,last=last,indices=indices,
     weights=weights,divisor=divisor,expectedReturn=result&0xFFFFFFFF,encodedAssetValidityProven=False)
    return page,list(SPANS)[kind],args,context


def execute(image,bodies,index,bound=5000):
    page,entry,args,context=inputs(index);rng=random.Random(0x1120F+index)
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
        assert STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096
    assert bytes(machine.mem_read(DATA,16384))==bytes(page)
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    return dict(index=index,entry=entry,args=args,context=context,actualReturn=True,
     modelPassed=machine.reg_read(UC_ARM_REG_R0)==context['expectedReturn'],registers=[machine.reg_read(r)for r in REGS],
     flags=machine.reg_read(UC_ARM_REG_CPSR),reads=reads,writes=writes,
     dataSha256=hashlib.sha256(bytes(page)).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     ownObserved=sorted(seen),functionProviders=0)
