import random
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT
from arm7_lane_channel_five_native_20261031 import digest

BASE,STACK,RETURN,MMIO=0x037F8000,0x023E0000,0x023FF000,0x04000000
SIZES={0x037FF0FC:80,0x037FE7CC:56}
CODES={0x037FF0FC:80,0x037FE7CC:52}


def cases(address):
    result=[]
    if address==0x037FF0FC:
        for index in (0,1):
            for value in range(256):
                loop=(0,1,0x80000000,0xFFFFFFFF)[value%4]
                args=[index,value|((value^0xFF)<<24),(0x12345678+value*0x10203)&0xFFFFFFFF,
                    ((value<<24)|(0x1234^value))&0xFFFFFFFF,loop,(value^0xA5)|0x80000000,(value*0x01010101)&0xFFFFFFFF]
                result.append(dict(arguments=args,initial=(value*257)^0xA551,passes=2))
        result.extend(dict(arguments=[index,word,word,word,loop,word,word],initial=word&0xFFFF,passes=2)
            for index in (0,1) for loop in (0,1,2,0x80000000,0xFFFFFFFF) for word in (0,0xFFFFFFFF,0x80000000,0x12345678))
    else:
        for value in range(256):
            result.append(dict(arguments=[0,0,0,0],initial=value,passes=2))
            result.append(dict(arguments=[(value*0x01010101)&0xFFFFFFFF,(0xFFFFFFFF-value)&0xFFFFFFFF,
                (value<<24)|0x80000000,(value^0xA5)|0x80000000],initial=value,passes=2))
        result.extend(dict(arguments=list(words),initial=initial,passes=2) for initial in (0,0x80,0xFF)
            for words in ((0xFFFFFFFF,)*4,(0x80000000,)*4,(3,3,1,1),(0xFFFFFFFF,0,0,0),(0,0xFFFFFFFF,0,0),(0,0,0xFFFFFFFF,0),(0,0,0,0xFFFFFFFF),(0x12345678,0x87654321,0xA5A5A5A5,0x5A5A5A5A)))
    return result


def setup(address,body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZES[address]:
        raise ValueError('Complete measured host ARM7 MMIO source differs')
    wram=bytearray(raw+bytes(0x18000-len(raw)))
    wram[address-BASE:address-BASE+len(body)]=body
    regions={BASE:bytes(wram),STACK:random.Random(seed+77).randbytes(0x4000),RETURN:bytes(0x1000),MMIO:random.Random(seed+131).randbytes(0x10000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    cpu.mem_write(0x04000501,bytes([case['initial']&0xFF]))
    writes,reads,visited=[],[],set()
    state=dict(instructions=0)
    def code(machine,pc,size,unused):
        state['instructions']+=1
        if machine.reg_read(UC_ARM_REG_CPSR)&32 or not address<=pc<address+CODES[address]:
            raise ValueError('MMIO pair escaped exact complete ARM source body')
        visited.add(pc)
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1 << size*8)-1)])
    def read(machine,access,target,size,value,unused):
        reads.append([target,size])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    return dict(cpu=cpu,address=address,case=case,seed=seed,regions=regions,writes=writes,reads=reads,visited=visited,state=state)


def execute(prepared,budget=1000):
    cpu,address,case,seed=prepared['cpu'],prepared['address'],prepared['case'],prepared['seed']
    records=[]
    for iteration in range(case['passes']):
        args=case['arguments']
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:4]=args[:4]
        initial[13:]=[STACK+0x3000,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,0x1F|((seed&1)*128)|((seed&15)<<28))
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        cpu.mem_write(STACK+0x3000,b''.join(word.to_bytes(4,'little') for word in args[4:]))
        caller_stack=bytes(cpu.mem_read(STACK+0x3000,0x1000))
        mmio=bytearray(cpu.mem_read(MMIO,0x10000))
        if address==0x037FF0FC:
            index,fmt,data,length,loop,source,destination=args
            if index not in (0,1):
                raise ValueError('MMIO capture model qualifies indices0/1 only')
            value=((fmt<<3)|((0 if loop else 1)<<2)|(source<<1)|destination)&255
            expected=[[0x04000508+index,1,value],[0x04000510+index*8,4,data],[0x04000514+index*8,2,length&0xFFFF]]
            expected_reads=[]
        else:
            left,right,first,third=args
            value=((mmio[0x501]&0x80)|(third<<5)|(first<<4)|(right<<2)|left)&255
            expected=[[0x04000501,1,value]]
            expected_reads=[[0x04000501,1]]
        for target,size,value in expected:
            mmio[target-MMIO:target-MMIO+size]=value.to_bytes(size,'little')
        prepared['writes'].clear()
        prepared['reads'].clear()
        first=prepared['state']['instructions']
        fault=None
        try:
            cpu.emu_start(address,RETURN,timeout=100000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not returned:
            records.append(dict(actualReturn=False,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateExcluded=True))
            break
        writes=[row for row in prepared['writes'] if not STACK<=row[0]<STACK+0x4000]
        reads=[row for row in prepared['reads'] if not STACK<=row[0]<STACK+0x4000 and not address+CODES[address]<=row[0]<address+SIZES[address]]
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if writes!=expected or reads!=expected_reads or bytes(cpu.mem_read(MMIO,0x10000))!=mmio:
            raise ValueError('Independent MMIO/boolean/full-word/truncation/ordered-access model differs')
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:]:
            raise ValueError('MMIO pair changed preserved registers/caller SP/LR')
        if bytes(cpu.mem_read(STACK+0x3000,0x1000))!=caller_stack:
            raise ValueError('MMIO pair changed caller-visible stack/argument guards')
        for base in (BASE,RETURN):
            if bytes(cpu.mem_read(base,len(prepared['regions'][base])))!=prepared['regions'][base]:
                raise ValueError('MMIO pair changed unrelated code/RAM/return memory')
        records.append(dict(actualReturn=True,fault=None,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            nonstackWrites=writes,nonstackReads=reads,instructions=prepared['state']['instructions']-first,
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()},independentCompleteMemoryModel=True))
    return dict(case=case,states=records,visited=sorted(prepared['visited']))
