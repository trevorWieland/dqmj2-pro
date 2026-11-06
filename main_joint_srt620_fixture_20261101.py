import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from project import ROOT,read_json

DATA,STACK,STOP=0x02400000,0x03030000,0x0F000000
STATE,FIFO=0x020EDF84,0x04000400
SPECS={0x0202C6CC:124,0x0202C788:196,0x0202CF80:300}
HELPERS=[0x0202E434,0x02008CA4,0x02008C40]
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
SIZES={int(f["address"],0):f["size"]for m in read_json(ROOT/"evidence/regions/canonical-symbol-functions.json")["canonicalModules"]
 for f in m["functions"]if m["module"]=="main"}


def expected_commands(entry,flag,words):
    scale,ex0,ex1,rotation,translation=words[:3],words[3:6],words[6:9],words[9:18],words[18:21]
    commands=[];translate=not(flag&4);rotate=not(flag&2)
    if entry==0x0202C788 and flag&32 and not flag&8:
        if translate:commands.append([0x1C,translation]);translate=False
        commands.append([0x1B,ex0])
    compensated=entry==0x0202CF80 and not(flag&24)
    if compensated:
        commands.append([0x1B,ex1])
        if translate:
            signed=lambda value:value if value<0x80000000 else value-0x100000000
            adjusted=[((signed(a)*signed(b))>>12)&0xFFFFFFFF for a,b in zip(translation,ex0)]
            commands.append([0x1C,adjusted]);translate=False
    tail={(False,False):[],(False,True):[[0x1C,translation]],(True,False):[[0x1A,rotation]],
     (True,True):[[0x19,rotation+translation]]}[(rotate,translate)]
    commands.extend(tail)
    if compensated:commands.append([0x1B,ex0])
    if not flag&1:commands.append([0x1B,scale])
    return commands


def execute(image,entry,body,index,bound=32768):
    rng=random.Random(0x62000000+index);page=bytearray(rng.randbytes(65536));argument=DATA+0x100;buffer=DATA+0x2000
    flag=(index%64)|[0,0x80000000,0x40000000,0xFFFFFFC0][(index//64)%4]
    edges=[0,1,0xFFFFFFFF,0x1000,0xFFFFF000,0x7FFFFFFF,0x80000000,0x12345678]
    words=[edges[(index+i)%len(edges)]if index%2==0 else rng.getrandbits(32)for i in range(21)]
    struct.pack_into("<22I",page,argument-DATA,flag,*words)
    mode=(index//256)%3;async_word=[1,2,0x80000000,0xFFFFFFFF][(index//64)%4]if mode==2 else 0
    pointer=0 if mode==0 else buffer;struct.pack_into("<I",page,buffer-DATA,0)
    commands=expected_commands(entry,flag,words);flattened=[value for op,payload in commands for value in[op,*payload]]
    expected_page=bytearray(page)
    if mode==2:
        struct.pack_into("<I",expected_page,buffer-DATA,len(flattened))
        for i,value in enumerate(flattened):struct.pack_into("<I",expected_page,buffer-DATA+4+i*4,value)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image)
    machine.mem_write(entry,body);machine.mem_write(STATE,struct.pack("<II",pointer,async_word));before_main=bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,4096);machine.mem_map(STOP,4096)
    machine.mem_map(0x04000000,65536);hardware=rng.randbytes(65536);machine.mem_write(0x04000000,hardware)
    stack=rng.randbytes(4096);machine.mem_write(STACK,stack);initial=[rng.getrandbits(32)for register in REGS]
    for register,value in zip(REGS,initial):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_R0,argument);machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28))
    machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    entries={address:SIZES[address]for address in HELPERS};entries[entry]=len(body)
    allowed={pc for address,size in entries.items()for pc in range(address,address+size,4)}
    own=set();reads=[];writes=[];fifo=[];calls=[];frames=[];completed=[];observed_commands=[]
    def code(uc,address,size,unused):
        assert address in allowed,hex(address)
        while frames and address==frames[-1]["lr"]:completed.append(frames.pop())
        if address in entries:
            frame=dict(entry=address,lr=uc.reg_read(UC_ARM_REG_LR),sp=uc.reg_read(UC_ARM_REG_SP))
            frames.append(frame);calls.append(dict(**frame,args=[uc.reg_read(r)for r in REGS[:4]]))
        if address==0x0202E434:
            op=uc.reg_read(UC_ARM_REG_R0);source=uc.reg_read(UC_ARM_REG_R1);count=uc.reg_read(UC_ARM_REG_R2)
            assert count in[3,9,12]
            payload=list(struct.unpack("<"+str(count)+"I",bytes(uc.mem_read(source,count*4))))
            observed_commands.append([op,payload])
        if entry<=address<entry+len(body):own.add(address)
    def read(uc,access,address,size,value,unused):
        assert 0x02000000<=address and address+size<=0x02100000 or DATA<=address and address+size<=DATA+65536 or STACK<=address and address+size<=STACK+4096
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:assert STACK+1536<=address and address+size<=STACK+2048
        elif address==FIFO:assert size==4;fifo.append(value&0xFFFFFFFF)
        else:assert buffer<=address and address+size<=buffer+4+192*4,hex(address)
        writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP,count=bound);assert machine.reg_read(UC_ARM_REG_PC)==STOP,"Prefix is not actual return"
    while frames and frames[-1]["lr"]==STOP:completed.append(frames.pop())
    assert not frames and machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(r)==value for r,value in zip(REGS[4:12],initial[4:12]))
    assert bytes(machine.mem_read(0x02000000,0x100000))==before_main
    after=bytes(machine.mem_read(DATA,65536));after_stack=bytes(machine.mem_read(STACK,4096));after_hardware=bytes(machine.mem_read(0x04000000,65536))
    expected_hardware=bytearray(hardware)
    if mode!=2 and flattened:struct.pack_into("<I",expected_hardware,FIFO-0x04000000,flattened[-1])
    assert after_stack[:1536]==stack[:1536]and after_stack[2048:]==stack[2048:]
    return dict(index=index,mode=mode,flags=flag,inputWords=[flag,*words],asyncWord=async_word,actualReturn=True,rawR0=machine.reg_read(UC_ARM_REG_R0),
     modelPassed=after==expected_page and observed_commands==commands and fifo==([]if mode==2 else flattened)and after_hardware==expected_hardware,
     registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),
     ownedObserved=sorted(own),commands=observed_commands,expectedCommands=commands,fifoWrites=fifo,reads=reads,writes=writes,calls=calls,
     actualNativeHelperReturns=len(completed)-1,providedCalls=0,pageSha256=hashlib.sha256(after).hexdigest(),
     stackSha256=hashlib.sha256(after_stack).hexdigest(),hardwareSha256=hashlib.sha256(after_hardware).hexdigest())
