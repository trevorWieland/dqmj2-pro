import hashlib
import random
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from project import ROOT,read_json
from main_g2d984_graphs_v2_20261101 import build,SPECS,DATA

STACK,STOP=0x03030000,0x0F000000
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
 UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
SIZES={int(f["address"],0):f["size"]for m in read_json(ROOT/"evidence/regions/canonical-symbol-functions.json")["canonicalModules"]
 for f in m["functions"]if m["module"]=="main"}
HELPERS=[0x020346FC,0x02034748,0x020349F4]


def execute(image,entry,bodies,index,bound=131072):
    page,expected,arguments,expected_return,context=build(entry,index)
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(0x02000000,0x100000);machine.mem_write(0x02000000,image)
    for address,body in bodies.items():machine.mem_write(address,body)
    before_main=bytes(machine.mem_read(0x02000000,0x100000))
    machine.mem_map(DATA,65536);machine.mem_write(DATA,bytes(page));machine.mem_map(STACK,4096);machine.mem_map(STOP,4096)
    rng=random.Random(0x984ABC00+index);stack=rng.randbytes(4096);machine.mem_write(STACK,stack)
    initial=[rng.getrandbits(32)for register in REGS]
    for register,value in zip(REGS,initial):machine.reg_write(register,value)
    for register,value in zip(REGS,arguments):machine.reg_write(register,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x1F|((index%16)<<28));machine.reg_write(UC_ARM_REG_SP,STACK+2048);machine.reg_write(UC_ARM_REG_LR,STOP)
    entries={**SPECS,**{address:SIZES[address]for address in HELPERS}}
    for address,body in bodies.items():entries[address]=len(body)
    top_size=len(bodies[entry])if entry in bodies else SPECS[entry]
    entries={address:size for address,size in entries.items()if not entry<address<entry+top_size}
    allowed={pc for address,size in entries.items()for pc in range(address,address+size,4)}
    own=set();reads=[];writes=[];calls=[];frames=[];completed=[]
    def code(uc,address,size,unused):
        assert address in allowed,hex(address)
        while frames and address==frames[-1]["lr"]:completed.append(frames.pop())
        if address in entries:
            frame=dict(entry=address,lr=uc.reg_read(UC_ARM_REG_LR),sp=uc.reg_read(UC_ARM_REG_SP))
            frames.append(frame);calls.append(dict(**frame,args=[uc.reg_read(r)for r in REGS[:4]]))
        if entry<=address<entry+entries[entry]:own.add(address)
    def read(uc,access,address,size,value,unused):
        assert 0x02000000<=address and address+size<=0x02100000 or DATA<=address and address+size<=DATA+65536 or STACK<=address and address+size<=STACK+4096,hex(address)
        reads.append([address,size,bytes(uc.mem_read(address,size)).hex()])
    def write(uc,access,address,size,value,unused):
        if STACK<=address and address+size<=STACK+4096:assert STACK+1536<=address and address+size<=STACK+2048
        else:assert DATA<=address and address+size<=DATA+65536,hex(address)
        writes.append([address,size,value&((1<<(size*8))-1)])
    machine.hook_add(UC_HOOK_CODE,code);machine.hook_add(UC_HOOK_MEM_READ,read);machine.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.emu_start(entry,STOP,count=bound)
    assert machine.reg_read(UC_ARM_REG_PC)==STOP,"Prefix is not actual return"
    while frames and frames[-1]["lr"]==STOP:completed.append(frames.pop())
    assert not frames and machine.reg_read(UC_ARM_REG_SP)==STACK+2048
    assert all(machine.reg_read(r)==value for r,value in zip(REGS[4:12],initial[4:12]))
    assert bytes(machine.mem_read(0x02000000,0x100000))==before_main
    after=bytes(machine.mem_read(DATA,65536));after_stack=bytes(machine.mem_read(STACK,4096))
    assert after_stack[:1536]==stack[:1536]and after_stack[2048:]==stack[2048:]
    value=machine.reg_read(UC_ARM_REG_R0)
    return dict(index=index,arguments=arguments,context=context,actualReturn=True,rawR0=value,
     expectedReturn=expected_return,modelPassed=after==expected and(expected_return is None or value==expected_return),
     registers=[machine.reg_read(r)for r in REGS],cpsr=machine.reg_read(UC_ARM_REG_CPSR),lr=machine.reg_read(UC_ARM_REG_LR),
     ownedObserved=sorted(own),reads=reads,writes=writes,calls=calls,actualNativeHelperReturns=len(completed)-1,
     completedNativeEntries=completed,providedCalls=0,pageSha256=hashlib.sha256(after).hexdigest(),stackSha256=hashlib.sha256(after_stack).hexdigest())
