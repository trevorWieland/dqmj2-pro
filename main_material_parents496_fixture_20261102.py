import hashlib
import random
import struct
import main_material_track1120_fixture_20261102 as leaf
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE,DATA,STACK,STOP=leaf.BASE,leaf.DATA,leaf.STACK,leaf.STOP
SPANS={**leaf.SPANS,0x02033C58:240,0x02033F54:256}
PARENTS={0x02033C58:240,0x02033F54:256}


def inputs(index):
    rng=random.Random(0x496+index);page=bytearray(rng.randbytes(16384));texture=bool(index%2)
    selected=index//2%4;frame=index//8%32;anm=0x1000;result=0x700;obj=0x600;unit=40 if texture else 20
    struct.pack_into('<BBHHH',page,anm+8,0,4,0x100,0,0x40)
    struct.pack_into('<HH',page,anm+0x48,unit,0)
    values=[];arguments=[]
    for channel in range(5):
        kind=3 if texture and channel==2 else 2 if texture else 1 if channel==4 else 0
        leaf_index=(index*117+channel*239)&4095;leaf_index=(leaf_index&~(31<<6))|(frame<<6);leaf_index=(leaf_index&~3)|kind
        original,entry,args,context=leaf.inputs(leaf_index)
        track=0x1000+channel*0x500;page[anm+track:anm+track+1024]=original[0x1000:0x1400]
        info=args[1];constant=context['constant'];value=context['expectedReturn']
        if index//64%4==channel%4:
            constant=True;info|=0x20000000
            value=0 if texture and channel in[3,4]else 4096 if texture and channel in[0,1]else 0x10000000 if texture else rng.randrange(65536)
        if texture:
            data=value if constant else track;arguments.extend([info,data])
        else:
            info=(info&0xFFFF0000)|(value if constant else track);arguments.append(info)
        values.append(value)
    struct.pack_into('<'+'I'*len(arguments),page,anm+0x4C+selected*unit,*arguments)
    expected=bytearray(page)
    if texture:
        scale_s,scale_t,rotation,trans_s,trans_t=values;flags=struct.unpack_from('<I',page,result)[0]
        for bit,condition in[(1,scale_s==4096 and scale_t==4096),(2,rotation==0x10000000),(4,trans_s==0 and trans_t==0)]:
            flags=(flags|bit)if condition else(flags&~bit)
        struct.pack_into('<I',expected,result,flags)
        if not flags&1:struct.pack_into('<II',expected,result+24,scale_s,scale_t)
        if not flags&2:struct.pack_into('<I',expected,result+32,rotation)
        if not flags&4:struct.pack_into('<II',expected,result+36,trans_s,trans_t)
        entry=0x02033F54;args=[DATA+anm,selected,frame,DATA+result]
    else:
        diffuse,ambient,specular,emission,alpha=values
        old0,old1,polygon=struct.unpack_from('<III',page,result+4)
        struct.pack_into('<III',expected,result+4,(diffuse|(ambient<<16)|(old0&0x8000))&0xFFFFFFFF,
         (specular|(emission<<16)|(old1&0x8000))&0xFFFFFFFF,((polygon&~0x1F0000)|(alpha<<16))&0xFFFFFFFF)
        struct.pack_into('<iII',page,obj,(frame<<12)|rng.randrange(4096),rng.randrange(4097),DATA+anm)
        expected[obj:obj+12]=page[obj:obj+12]
        entry=0x02033C58;args=[DATA+result,DATA+obj,selected|(rng.randrange(65536)<<16)]
    context=dict(texture=texture,selected=selected,frame=frame,values=values,encodedAssetValidityProven=False)
    return page,bytes(expected),entry,args,context


def execute(image,bodies,index,bound=5000):
    page,expected,entry,args,context=inputs(index);rng=random.Random(0x496F+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE,0x100000);machine.mem_write(BASE,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    machine.mem_map(DATA,16384);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,8192);machine.mem_write(STACK,rng.randbytes(8192))
    machine.mem_map(STOP,4096);machine.mem_write(STOP,b'\x1e\xff\x2f\xe1');machine.reg_write(UC_ARM_REG_CPSR,0x10|rng.choice([0,0x80000000,0xF0000000]))
    for reg in leaf.REGS:machine.reg_write(reg,rng.getrandbits(32))
    for reg,value in zip(leaf.REGS,args):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+4096);machine.reg_write(UC_ARM_REG_LR,STOP)
    seen=set();reads=[];writes=[];returned=False;pending=[];helper_returns=0
    def code(uc,address,size,user):
        nonlocal returned,helper_returns
        if pending and address==pending[-1]:pending.pop();helper_returns+=1
        if address in leaf.SPANS:pending.append(uc.reg_read(UC_ARM_REG_LR))
        if address==STOP:assert not pending;returned=True;uc.emu_stop();return
        assert any(base<=address<base+n for base,n in SPANS.items()),hex(address);seen.add(address)
    def read(uc,access,address,size,value,user):reads.append((address,size,int.from_bytes(bytes(uc.mem_read(address,size)),'little')))
    def write(uc,access,address,size,value,user):
        assert DATA<=address and address+size<=DATA+16384 or STACK<=address and address+size<=STACK+8192
        writes.append((address,size,value))
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP+4,count=bound);assert returned,('no top return',index)
    assert machine.reg_read(UC_ARM_REG_SP)==STACK+4096 and helper_returns==5
    output=bytes(machine.mem_read(DATA,16384))
    for address,body in bodies.items():machine.mem_write(address,image[address-BASE:address-BASE+len(body)])
    assert bytes(machine.mem_read(BASE,len(image)))==image
    return dict(index=index,entry=entry,args=args,context=context,actualReturn=True,actualNativeHelperReturns=helper_returns,
     modelPassed=output==expected,registers=[machine.reg_read(r)for r in leaf.REGS],flags=machine.reg_read(UC_ARM_REG_CPSR),
     reads=reads,writes=writes,dataSha256=hashlib.sha256(output).hexdigest(),
     stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK,8192))).hexdigest(),ownObserved=sorted(seen),functionProviders=0)
