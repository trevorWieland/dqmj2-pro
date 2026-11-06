import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,SET,GET,DATA,STACK,STOP=0x02000000,0x020379C4,0x020379EC,0x02400000,0x03030000,0x0F000000
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def signed(word):
    return word if word<0x80000000 else word-0x100000000


def execute(image,bodies,index,bound=2000,context=0):
    rng=random.Random(0x379EC92+index);machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    page=bytearray(rng.randbytes(4096));stack=rng.randbytes(8192)
    origin,target=[rng.randrange(-1000000,1000001)for _ in range(2)]
    frame=rng.choice([-1,0,1,2,17,64,127,511]);counter=rng.randrange(-2 if frame>0 else 0,max(2,frame+3))
    values=[origin,target,counter,frame];obj=DATA+256
    expected=target if counter>=frame else origin+(1 if (target-origin)*counter>=0 else -1)*(abs((target-origin)*counter)//frame)
    assert counter>=frame or frame>0
    entry=GET if index%2==0 else SET;fader=obj
    args=[obj,rng.randrange(-1000000,1000001)&0xFFFFFFFF,rng.randrange(-2,512)&0xFFFFFFFF]
    expect_return=expected&0xFFFFFFFF if entry==GET else 0;skip=False
    if context==1:
        entry=0x02038148;fader=obj+0x1C;args=[DATA+64,rng.randrange(4096),rng.randrange(-2,512)&0xFFFFFFFF]
        struct.pack_into('<I',page,64,0 if index%5==0 else obj);page[256+0x2C]=2 if index%5==1 else 1
        skip=index%5 in[0,1];expect_return=None
    elif context==2:
        entry=0x0203861C;fader=obj+0x1C;args=[obj,0x7F00,1];expect_return=0
    elif context==3:
        entry=0x0203A4FC;fader=obj+0xE8;args=[obj,index+1,index+1];expect_return=0
        struct.pack_into('<I',page,256+0x110,rng.getrandbits(32)|2)
    struct.pack_into('<4i',page,fader-DATA,*values);initial=bytes(page)
    if context==2:
        for offset in[0x2E,0x2D,0x2F]:page[256+offset]=0
        for offset in[0x34,0x3E]:struct.pack_into('<H',page,256+offset,0)
        page[256+0x40]=page[256+0x41]=127;expected=0
    if (entry!=GET)and not skip:
        new_target=(args[1]<<8)&0xFFFFFFFF if context==1 else args[1]
        if context==3:new_target=0
        struct.pack_into('<4i',page,fader-DATA,expected,signed(new_target),0,signed(args[2]))
    if context==3:
        flags=struct.unpack_from('<I',page,256+0x110)[0]
        struct.pack_into('<I',page,256+0x110,flags|8);struct.pack_into('<I',page,256+0x150,0)
    expected_page=bytes(page);page=bytearray(initial)
    machine.mem_map(DATA,4096);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,stack)
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1')
    for reg in REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(REGS,args):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x10000000,0x80000000,0xF0000000]))
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];continuations=[];calls=[];returned=False

    def code(uc,address,size,user):
        nonlocal returned
        if address==STOP:returned=True;uc.emu_stop();return
        assert BASE<=address<BASE+len(image),(hex(address),index)
        seen.add(address)
        if address in [GET,0x02026144]:calls.append((address,uc.reg_read(UC_ARM_REG_LR)))
        if address in [SET+20,GET+44]:continuations.append(address)

    def read(uc,access,address,size,value,user):
        reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))

    def write(uc,access,address,size,value,user):
        assert DATA<=address and address+size<=DATA+4096 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))

    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no actual top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096
    actual_page=bytes(machine.mem_read(DATA,4096));expected_return=expect_return
    passed=actual_page==expected_page and (expected_return is None or machine.reg_read(UC_ARM_REG_R0)==expected_return)
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    return dict(index=index,context=context,entry=entry,input=values,args=args,modelPassed=passed,actualReturn=True,
     registers=[machine.reg_read(r)for r in REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),
     pageSha256=hashlib.sha256(actual_page).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),
     reads=reads,writes=writes,calls=calls,divisionCallContinuations=continuations.count(GET+44),
     getterCallContinuations=continuations.count(SET+20),ownedObserved=sorted(a for a in seen if any(b<=a<b+n for b,n in[(SET,92),(0x02038148,44),(0x0203861C,72),(0x0203A4FC,88)])),
     helperObserved=sorted(a for a in seen if not any(b<=a<b+n for b,n in[(SET,92),(0x02038148,44),(0x0203861C,72),(0x0203A4FC,88)])))
