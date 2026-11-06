import random
from collections import Counter
import match_runtime
from arm7_lane_channel_five_native_20261031 import digest
from arm7_lane_skip_native_20261031 import inventory,executable
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,DATA,STACK,RETURN=0x037F8000,0x023C0000,0x023E0000,0x023FF000
TABLE=0x03807870
SIZES={0x037FC558:56}
CODES={0x037FC558:52}


def setup(address,body,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZES[address]:
        raise ValueError('Original ARM7 scheduler-counter runtime/complete owned source extent differs')
    wram=bytearray(raw+random.Random(seed+71).randbytes(0x18000-len(raw)))
    wram[address-BASE:address-BASE+len(body)]=body
    regions={BASE:bytes(wram),DATA:random.Random(seed+137).randbytes(0x8000),
        STACK:random.Random(seed+293).randbytes(0x4000),RETURN:bytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    entries,ranges=inventory()
    reads,writes,visited,frames=[],[],set(),[]
    returned=Counter()
    state=dict(caller=False,instructions=0)
    def code(machine,pc,size,unused):
        state['instructions']+=1
        if not executable(pc,size,bool(machine.reg_read(UC_ARM_REG_CPSR)&32)):
            raise ValueError('Scheduler-counter execution escaped qualified original module ARM/Thumb instruction ranges: '+hex(pc))
        if not state['caller']:
            return
        if address<=pc<address+SIZES[address]:
            if pc>=address+CODES[address]:
                raise ValueError('Scheduler-counter source literal pool executed')
            visited.add(pc)
        while frames and frames[-1][1]==pc:
            returned[frames.pop()[0]]+=1
        if pc in entries and pc!=address:
            lr=machine.reg_read(match_runtime.REGISTERS[14])
            if lr!=RETURN:
                frames.append([pc,lr])
    def read(machine,access,target,size,value,unused):
        if state['caller']:
            reads.append([target,size])
    def write(machine,access,target,size,value,unused):
        if state['caller']:
            writes.append([target,size,value&((1<<size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    def invoke(entry,args=(),caller=False,budget=100000):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:len(args)]=[value&0xFFFFFFFF for value in args]
        initial[13:]=[STACK+0x3000,RETURN]
        cpsr=0x1F|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
        cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        first=state['instructions']
        state['caller']=caller
        reads.clear()
        writes.clear()
        frames.clear()
        returned.clear()
        fault=None
        try:
            cpu.emu_start(entry,RETURN,timeout=500000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not actual:
            return dict(entry=hex(entry),arguments=args,actualReturn=False,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),
                instructions=state['instructions']-first,postFaultStateExcluded=True)
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        final_cpsr=cpu.reg_read(UC_ARM_REG_CPSR)
        if actual and (registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or final_cpsr&255!=cpsr&255):
            raise ValueError('Scheduler-counter preserved register/SP/LR/IRQ-FIQ-mode contract differs')
        if actual and (bytes(cpu.mem_read(STACK+0x3000,0x1000))!=regions[STACK][0x3000:] or bytes(cpu.mem_read(RETURN,0x1000))!=regions[RETURN]):
            raise ValueError('Scheduler-counter caller-visible stack/return guards changed')
        if actual and frames:
            raise ValueError('Original scheduler-counter helper frames did not actually complete')
        return dict(entry=hex(entry),arguments=args,actualReturn=actual,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),
            instructions=state['instructions']-first,registers=registers,cpsr=final_cpsr)
    return dict(cpu=cpu,invoke=invoke,address=address,regions=regions,reads=reads,writes=writes,visited=visited,
        frames=frames,helperReturns=returned,state=state)


def snapshot(machine):
    return {base:bytearray(machine['cpu'].mem_read(base,len(data))) for base,data in machine['regions'].items() if base!=STACK}


def word(memory,address):
    for base,data in memory.items():
        if base<=address and address+4<=base+len(data):
            return int.from_bytes(data[address-base:address-base+4],'little')
    raise ValueError('Independent scheduler-counter model read escaped bounded mapped backing')


def store(memory,address,value,trace):
    for base,data in memory.items():
        if base<=address and address+4<=base+len(data):
            data[address-base:address-base+4]=(value&0xFFFFFFFF).to_bytes(4,'little')
            trace.append([address,4,value&0xFFFFFFFF])
            return
    raise ValueError('Independent scheduler-counter model store escaped bounded mapped backing')


def signed(value):
    return value if value<0x80000000 else value-0x100000000


def result(machine,execution,expected,value,stores):
    if not execution['actualReturn']:
        return dict(execution=execution,actualReturn=False,postFaultStateExcluded=True)
    cpu=machine['cpu']
    if value is not None and execution['registers'][0]!=(value&0xFFFFFFFF):
        raise ValueError('Independent scheduler-counter return-value model differs')
    if any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):
        raise ValueError('Independent complete scheduler-counter memory/effect model differs')
    actual=[row for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000]
    if stores is not None and sorted(actual)!=sorted(stores):
        raise ValueError('Independent scheduler-counter store values/widths/footprint model differs')
    return dict(execution=execution,actualReturn=True,orderedNonstackWrites=actual,
        nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
        memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in machine['regions'].items()},
        actualNestedReturns={hex(address):count for address,count in sorted(machine['helperReturns'].items())},
        independentCompleteMemoryEffectsModel=True,independentWriteFootprintModel=stores is not None)
