import hashlib
import random
import struct
from functools import cache
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

DATA,STACK,STOP=0x02400000,0x03030000,0x0F000000
SPECS={0x0202BF2C:92,0x0202BFE0:116,0x0202C054:52,0x020364DC:92}
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
SHAPES={(1,1),(2,2),(4,4),(8,8),(2,1),(4,1),(4,2),(8,4),(1,2),(1,4),(2,4),(4,8)}


@cache
def rectangles(width,height):
    if not width or not height:return 0
    if (width,height)in SHAPES:return 1
    choices=[rectangles(cut,height)+rectangles(width-cut,height)for cut in range(1,width//2+1)]
    choices.extend(rectangles(width,cut)+rectangles(width,height-cut)for cut in range(1,height//2+1))
    return min(choices)


def inputs(entry,index):
    rng=random.Random(0x35200000+index);page=bytearray(rng.randbytes(65536))
    resource,base,table,frames=DATA+0x100,DATA+0x1000,DATA+0x120C,DATA+0x6000
    if entry==0x020364DC:
        width,height=index%33,(index//33)%33
        return page,[width,height],rectangles(width,height),dict(width=width,height=height)
    count=[0,1,2,7,31,255][index%6];item=[0,max(0,count-1),count,count+1,0xFFFFFFFF,1][(index//6)%6]
    stride=[4,8,12,16][(index//36)%4]
    if entry==0x0202BF2C:
        header_size=[0,16,20,64][(index//144)%4];block_offset=base-resource
        struct.pack_into('<H',page,resource-DATA+12,header_size)
        struct.pack_into('<I',page,resource-DATA+header_size,block_offset)
        dict_base=base+8;entry_header=dict_base+0x200
        offsets=[0,0x4000,0x4320,0x40][(index//576)%4]
        for i in range(count):struct.pack_into('<I',page,entry_header-DATA+4+stride*i,offsets+i*8)
        page[dict_base-DATA+1]=count;struct.pack_into('<H',page,dict_base-DATA+6,0x200)
        struct.pack_into('<H',page,entry_header-DATA,stride)
        pointer=0 if index%17==0 else resource
        expected=base+offsets+item*8 if pointer and item<count else 0
        return page,[pointer,item],expected,dict(count=count,index=item,stride=stride,headerSize=header_size)
    dict_base=base+12;entry_header=dict_base+0x200
    page[dict_base-DATA+1]=count;struct.pack_into('<H',page,dict_base-DATA+6,0x200)
    struct.pack_into('<H',page,entry_header-DATA,stride)
    if entry==0x0202C054:
        expected=entry_header+4+item*stride if item<count else 0
        return page,[base,item],expected,dict(count=count,index=item,stride=stride)
    count=[1,2,7,16,64,127][index%6];query=(index//6)%count
    frame_count=count;item=(index//762)%3;page[dict_base-DATA+1]=3
    struct.pack_into('<H',page,entry_header-DATA,8)
    item_base=entry_header+4+item*8
    ratios=[0,1,128,512,1024,2048,4096]
    ratio=ratios[(index//18)%len(ratios)]
    struct.pack_into('<HHhH',page,item_base-DATA,frame_count,index&0xFFFF,ratio,frames-base)
    times=[i*2 if index%2 else i//2 for i in range(frame_count)]
    for i,time in enumerate(times):struct.pack_into('<HBB',page,frames-DATA+4*i,time,(i+index)&255,(i*3+index)&255)
    selected=max([i for i,time in enumerate(times)if time<=query],default=0)
    assert ratio*query>>12<frame_count
    return page,[base,item,query],frames+4*selected,dict(count=frame_count,index=item,frame=query,ratio=ratio,selected=selected)


def execute(image,entry,bodies,index,bound=16384):
    page,args,expected,context=inputs(entry,index);rng=random.Random(0x352ABCDE+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    before=bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,4096);machine.mem_map(STOP,4096)
    stack=rng.randbytes(4096);machine.mem_write(STACK,stack);initial=[rng.getrandbits(32)for register in REGS]
    for register,value in zip(REGS,initial):machine.reg_write(register,value)
    for register,value in zip(REGS,args):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    entries={entry:len(bodies.get(entry,b''))or SPECS[entry]}
    if entry==0x0202BFE0:entries[0x0202C054]=len(bodies.get(0x0202C054,b''))or SPECS[0x0202C054]
    allowed={pc for address,size in entries.items()for pc in range(address,address+size,4)}
    own=set();reads=[];writes=[];calls=[];frames=[];completed=[]
    def code(uc,address,size,unused):
        assert address in allowed,hex(address)
        while frames and address==frames[-1]['lr']:completed.append(frames.pop())
        if address in entries:
            frame=dict(entry=address,lr=uc.reg_read(UC_ARM_REG_LR),sp=uc.reg_read(UC_ARM_REG_SP))
            frames.append(frame);calls.append(dict(**frame,args=[uc.reg_read(r)for r in REGS[:4]]))
        if entry<=address<entry+entries[entry]:own.add(address)
    def read(uc,access,address,size,value,unused):
        assert DATA<=address and address+size<=DATA+65536 or STACK<=address and address+size<=STACK+4096
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        assert STACK+1536<=address and address+size<=STACK+2048
        writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP,count=bound);assert machine.reg_read(UC_ARM_REG_PC)==STOP,'Prefix is not actual return'
    while frames and frames[-1]['lr']==STOP:completed.append(frames.pop())
    assert not frames and machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(r)==value for r,value in zip(REGS[4:12],initial[4:12]))
    after_stack=bytes(machine.mem_read(STACK,4096));assert after_stack[:1536]==stack[:1536]and after_stack[2048:]==stack[2048:]
    assert bytes(machine.mem_read(DATA,65536))==page and bytes(machine.mem_read(0x02000000,0x100000))==before
    return dict(index=index,context=context,actualReturn=True,rawR0=machine.reg_read(UC_ARM_REG_R0),expectedR0=expected,
     modelPassed=machine.reg_read(UC_ARM_REG_R0)==expected,registers=[machine.reg_read(r)for r in REGS],
     cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),ownedObserved=sorted(own),
     reads=reads,writes=writes,calls=calls,actualNativeHelperReturns=len(completed)-1,providedCalls=0,
     dataSha256=hashlib.sha256(page).hexdigest(),stackSha256=hashlib.sha256(after_stack).hexdigest())
