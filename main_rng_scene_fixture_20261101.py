import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from project import ROOT,read_json

ENTRY=0x02043844
STATE=0x020F69C4
RNG=0x020F6044
STACK=0x03030000
STOP=0x0F000000
PROVIDERS=[0x021D9710,0x021F92D8,0x0220B48C,0x0220B634,0x0220B3BC,0x022139E8,0x0220268C,0x0220345C]
HELPERS=[0x02044508,0x020443EC,0x0204457C,0x0203D2EC]
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
SIZES={int(f["address"],0):f["size"]for m in read_json(ROOT/"evidence/regions/canonical-symbol-functions.json")["canonicalModules"]
 for f in m["functions"]if m["module"]=="main"}


def inputs(index):
    rng=random.Random(0x43844000+index);frame=bytearray(rng.randbytes(64))
    mode=index%256 if index<1024 else 2
    values=[0,0xFFFFFFFF,0x80000000,0x12345678]
    seed=values[(index//256)%4]if index<1024 else rng.getrandbits(32)
    mirror=values[((index//256)+1)%4]if index<1024 else rng.getrandbits(32)
    frame[0x24]=mode;struct.pack_into("<I",frame,12,mirror)
    expected=bytearray(frame);expected[0]=1;expected[3]=3
    return bytes(frame),seed,mirror,mode,bytes(expected)


def execute(image,body,index,bound=4096):
    frame,seed,mirror,mode,expected_frame=inputs(index);rng=random.Random(0x43844ABC+index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image)
    machine.mem_write(ENTRY,body);machine.mem_write(STATE,frame);machine.mem_write(RNG,struct.pack("<I",seed))
    before=bytes(machine.mem_read(0x02000000,0x100000));expected=bytearray(before)
    expected[STATE-0x02000000:STATE-0x02000000+64]=expected_frame
    struct.pack_into("<I",expected,RNG-0x02000000,mirror if mode==2 else seed)
    machine.mem_map(0x021D0000,0x90000);machine.mem_map(STACK,4096);machine.mem_map(STOP,4096)
    stack=rng.randbytes(4096);machine.mem_write(STACK,stack)
    initial=[rng.getrandbits(32)for register in REGS]
    for register,value in zip(REGS,initial):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    allowed=set(range(ENTRY,ENTRY+len(body),4))|{pc for address in HELPERS for pc in range(address,address+SIZES[address],4)}
    own=set();calls=[];provided=[];frames=[];completed=[];reads=[];writes=[]
    def code(uc,address,size,unused):
        while frames and address==frames[-1]["lr"]:completed.append(frames.pop())
        if address in PROVIDERS:
            arguments=[uc.reg_read(r)for r in REGS[:4]]
            if address in[0x022139E8,0x0220268C]:assert arguments[0]==0
            if address==0x0220345C:assert arguments[0]==1
            result=(0xA5438440^index^address)&0xFFFFFFFF
            provided.append(dict(target=address,r0=arguments[0]if address in[0x022139E8,0x0220268C,0x0220345C]else None,result=result))
            uc.reg_write(UC_ARM_REG_R0,result)
            for register in[UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12]:uc.reg_write(register,(result^register^0xC10BBE00)&0xFFFFFFFF)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR));return
        assert address in allowed,hex(address)
        if address in HELPERS or address==ENTRY:
            item=dict(entry=address,lr=uc.reg_read(UC_ARM_REG_LR),sp=uc.reg_read(UC_ARM_REG_SP))
            frames.append(item);calls.append(dict(**item,r0=uc.reg_read(UC_ARM_REG_R0)))
        if ENTRY<=address<ENTRY+len(body):own.add(address)
    def read(uc,access,address,size,value,unused):
        assert 0x02000000<=address and address+size<=0x02100000 or STACK<=address and address+size<=STACK+4096
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        assert STACK+1536<=address and address+size<=STACK+2048 or STATE<=address and address+size<=STATE+64 or RNG<=address and address+size<=RNG+4
        writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(ENTRY,STOP,count=bound);assert machine.reg_read(UC_ARM_REG_PC)==STOP,"Prefix is not actual return"
    while frames and frames[-1]["lr"]==STOP:completed.append(frames.pop())
    assert not frames and machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(r)==value for r,value in zip(REGS[4:12],initial[4:12]))
    after=bytes(machine.mem_read(0x02000000,0x100000));after_stack=bytes(machine.mem_read(STACK,4096))
    assert after_stack[:1536]==stack[:1536]and after_stack[2048:]==stack[2048:]
    setter=[call for call in calls if call["entry"]==0x0203D2EC]
    expected_calls=PROVIDERS[:7]+([PROVIDERS[-1]]if mode==2 else[])
    model=after==expected and machine.reg_read(UC_ARM_REG_R0)==1
    model=model and[len(setter),[c["r0"]for c in setter]]==([1,[mirror]]if mode==2 else[0,[]])
    model=model and [c["target"]for c in provided]==expected_calls
    return dict(index=index,mode=mode,seed=seed,mirror=mirror,actualReturn=True,modelPassed=model,
     rawR0=machine.reg_read(UC_ARM_REG_R0),registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),
     lr=machine.reg_read(UC_ARM_REG_LR),ownedObserved=sorted(own),calls=calls,providedCalls=provided,
     actualNativeHelperReturns=sum(c["entry"]!=ENTRY for c in completed),reads=reads,writes=writes,
     resultingSeed=struct.unpack_from("<I",after,RNG-0x02000000)[0],resultingFrame=after[STATE-0x02000000:STATE-0x02000000+64].hex(),
     mainSha256=hashlib.sha256(after).hexdigest(),stackSha256=hashlib.sha256(after_stack).hexdigest())
