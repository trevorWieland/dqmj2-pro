import hashlib
import random
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT,write_json

BASE,STACK,RETURN,IO=0x037F8000,0x023E0000,0x023FF000,0x04000000
SIZES={0x037FE448:96,0x037FE4A8:224}
CODES={0x037FE448:92,0x037FE4A8:216}
IRQ={0x037FDD00:20,0x037FDD14:24}
CONTROL,SEND=IO+0x184,IO+0x188


def digest(data):
    return hashlib.sha256(data).hexdigest()


def execute(address,body,control,word,seed,budget=20000):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or address not in SIZES or len(body)!=SIZES[address]:
        raise ValueError('PXI complete source unit or measured module differs')
    wram=bytearray(raw+random.Random(seed+43).randbytes(0x18000-len(raw)))
    wram[address-BASE:address-BASE+len(body)]=body
    regions={BASE:bytes(wram),STACK:random.Random(seed+67).randbytes(0x4000),RETURN:bytes(0x1000),IO:random.Random(seed+173).randbytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first,data in regions.items():
        cpu.mem_map(first,len(data))
        cpu.mem_write(first,data)
    cpu.mem_write(CONTROL,control.to_bytes(2,'little'))
    expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in regions.items() if base!=STACK}
    stores=[]
    def put(target,value,width):
        expected[IO][target-IO:target-IO+width]=value.to_bytes(width,'little')
        stores.append([target,width,value])
    result=None
    if address==0x037FE448:
        if control&0x4000:
            result=0xFFFFFFFF
            put(CONTROL,control|0xC000,2)
        elif control&2:
            result=0xFFFFFFFE
        else:
            result=0
            put(SEND,word,4)
    writes,reads,visited,frames=[],[],set(),[]
    counts={key:0 for key in IRQ}
    steps=[0]
    def code(uc,pc,size,unused):
        steps[0]+=1
        if uc.reg_read(UC_ARM_REG_CPSR)&32 or size!=4 or pc%4 or not (address<=pc<address+CODES[address] or any(first<=pc<first+length for first,length in IRQ.items())):
            raise ValueError('Plain PXI execution escaped owned ARM/IRQ code')
        if frames and frames[-1][1]==pc:
            counts[frames.pop()[0]]+=1
        if address<=pc<address+CODES[address]:
            visited.add(pc)
        if pc in IRQ:
            frames.append((pc,uc.reg_read(match_runtime.REGISTERS[14])))
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,lambda uc,access,target,size,value,unused:reads.append([target,size]))
    cpu.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,target,size,value,unused:writes.append([target,size,value&((1<<(size*8))-1)]))
    initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
    if address==0x037FE448:
        initial[0]=word
    initial[13:]=[STACK+0x3000,RETURN]
    flags=0x1F|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
    cpu.reg_write(UC_ARM_REG_CPSR,flags)
    for register,value in zip(match_runtime.REGISTERS,initial):
        cpu.reg_write(register,value)
    guard=bytes(cpu.mem_read(STACK+0x3000,0x1000))
    fault=None
    try:
        cpu.emu_start(address,RETURN,timeout=500000,count=budget)
    except (UcError,ValueError) as error:
        fault=str(error)
    actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
    record=dict(address=hex(address),control=control,word=word,seed=seed,actualReturn=actual,
        pc=hex(cpu.reg_read(UC_ARM_REG_PC)),fault=fault,instructions=steps[0],visited=sorted(visited))
    if not actual:
        return dict(record,returnCredit=0,postBoundaryStateExcluded=True)
    registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=flags&255 or bytes(cpu.mem_read(STACK+0x3000,0x1000))!=guard or frames:
        raise ValueError('Plain PXI actual return/callee-preserved register/SP/LR/control guards differ')
    if result is not None and registers[0]!=result:
        raise ValueError('Independent raw-word PXI signed status result differs')
    nonstack=[row for row in writes if not STACK<=row[0]<STACK+0x4000]
    if nonstack!=stores or any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):
        raise ValueError('Independent full memory/exact ordered nonstack store model differs')
    needed=int(not control&0x4000)
    if counts!={key:needed for key in IRQ}:
        raise ValueError('Actual IRQ-helper return counts differ')
    return dict(record,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=reads,orderedWrites=writes,
        actualNativeIRQReturns={hex(key):count for key,count in counts.items()},
        independentCompleteMemoryAndExactNonstackStoreModel=True,
        memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in regions.items()},
        physicalIpcHardwareCredit=0,providerReplacements=[])


def main():
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    records=[]
    controls=(0,2,0x100,0x4000,0x4002,0xC000,0xFFFF,0x8000)
    for control in controls:
        for word in (0,1,0x12345678,0x80000000,0xFFFFFFFF):
            for seed in range(4):
                record=execute(0x037FE448,raw[0x6448:0x64A8],control,word,seed)
                if not record['actualReturn']:
                    raise ValueError(record)
                records.append(record)
    for control in (0x100,0x102,0x8100,0x8102):
        for seed in range(16):
            record=execute(0x037FE4A8,raw[0x64A8:0x6588],control,0,seed)
            if not record['actualReturn']:
                raise ValueError(record)
            records.append(record)
    cap=execute(0x037FE4A8,raw[0x64A8:0x6588],0x4100,0,1,1000)
    if cap['actualReturn']:
        raise ValueError('Plain RAM error acknowledgment must not be assumed physical W1C recovery')
    write_json(ROOT/'evidence/attempts/arm7-lane-pxi-plain-native-20261031.json',dict(sourceCredit=0,records=records,
        actualOriginalReturns=len(records),staticRamErrorLoop=dict(execution=cap,returnCredit=0),
        limitations=['Mapped registers are deterministic RAM inputs, not physical FIFO/W1C hardware',
            'Send status paths and receive-empty paths return; nonempty receive queues remain unqualified here',
            'Static RAM error-bit14 remains set after writing1 and therefore exhausts; no hardware recovery or post-boundary data claim']))
    print(dict(actualOriginalReturns=len(records),sourceCredit=0))


if __name__=='__main__':
    main()
