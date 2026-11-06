import hashlib
import json
import random
from pathlib import Path
import match_runtime
import arm7_channel_parameters_model_20261030_67 as independent
import arm7_seq_neighbor_model_20261030 as memory
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR

ROOT = Path(__file__).resolve().parent
NODE = memory.DATA+0x100
UNITS = {0x037FF82C:(164,168),0x037FF8D4:(28,32),0x037FFDB4:(96,96)}
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address):
    if address == 0x037FF8D4:
        return [dict(value=value,passes=1) for value in [*range(256),-1,-128,-2147483648]]
    if address == 0x037FFDB4:
        return [dict(delay=delay,counter=counter,speed=speed,phase=phase,passes=2)
            for delay,counter in ((0,0),(1,0),(1,1),(65535,65534),(65535,65535))
            for speed in (0,1,127,128,255) for phase in (0,1,255,256,32767,32768,65535)]
    rows=[]
    base=dict(status=0,attenuation=-92544,step=1,attack=64,sustain=127,decay=64,release=128,passes=1)
    words=(0,-1,-127,-128,-92544,-2147483648,2147483647)
    for attenuation in words:
        for attack in (0,1,64,127,255):
            rows.append(dict(base,attenuation=attenuation,attack=attack))
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    for sustain in range(256):
        offset=independent.SQUARE+2*sustain-memory.BASE
        floor=int.from_bytes(raw[offset:offset+2],'little',signed=True)*128
        for delta in (-1,0,1):
            rows.append(dict(base,status=1,sustain=sustain,attenuation=floor+64+delta))
    for attenuation in words:
        for release in (0,1,127,65535):
            rows.append(dict(base,status=3,attenuation=attenuation,release=release,passes=2))
    for status in (0,1,2,3,4,255):
        for step in (0,1,255,0xFFFFFFFF):
            rows.append(dict(base,status=status,step=step,attenuation=-1,attack=0,passes=3))
    return rows


def setup(address,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!=RAW_SHA:
        raise ValueError('Original parameter module changed')
    wram=bytearray(0x14000)
    wram[:len(raw)]=raw
    state=independent.Model(random.Random(seed+20261030).randbytes(0x4000),wram)
    if address==0x037FF82C:
        for offset,size,key in ((2,1,'status'),(0x10,4,'attenuation'),(0x1C,1,'attack'),
            (0x1D,1,'sustain'),(0x1E,2,'decay'),(0x20,2,'release')):
            state.put(NODE+offset,size,case[key])
    elif address==0x037FFDB4:
        for offset,size,key in ((1,1,'speed'),(4,2,'delay'),(6,2,'counter'),(8,2,'phase')):
            state.put(NODE+offset,size,case[key])
    return bytes(state.regions[memory.DATA]),bytes(state.regions[memory.BASE])


def execute(address,body,case,seed,budget=10000):
    code,size=UNITS[address]
    ram,wram=setup(address,case,seed)
    wram=bytearray(wram)
    wram[address-memory.BASE:address-memory.BASE+len(body)]=body
    wram=bytes(wram)
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,length,data in ((memory.BASE,0x14000,wram),(memory.DATA,0x4000,ram),
        (memory.STACK,0x4000,random.Random(seed+531).randbytes(0x4000)),(memory.RETURN,0x1000,bytes(0x1000))):
        cpu.mem_map(base,length)
        cpu.mem_write(base,data)
    visited,writes=set(),[]
    def hook(machine,pc,length,unused):
        if not address<=pc<address+code or machine.reg_read(UC_ARM_REG_CPSR)&32:
            raise ValueError('Leaf parameter function escaped measured ARM instructions')
        visited.add(pc)
    def write(machine,access,target,length,value,unused):
        if not memory.STACK<=target<memory.STACK+0x4000:
            writes.append([target,length,value & ((1 << length*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,hook)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    records=[]
    for phase in range(case['passes']):
        registers=[random.Random(seed+phase*43+i).getrandbits(32) for i in range(15)]
        registers[0]=NODE
        if address!=0x037FFDB4:
            registers[1]=(case['step'] if address==0x037FF82C else case['value']) & 0xFFFFFFFF
        registers[-2:]=[memory.STACK+0x3F00,memory.RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,(seed%16)<<28 | 0xD3)
        for register,value in zip(match_runtime.REGISTERS,registers):
            cpu.reg_write(register,value)
        first=len(writes)
        fault=None
        try:
            cpu.emu_start(address,memory.RETURN,count=budget,timeout=100000)
        except UcError as error:
            fault=error.errno
        returned=cpu.reg_read(UC_ARM_REG_PC)==memory.RETURN
        actual=[cpu.reg_read(r) for r in match_runtime.REGISTERS]
        if returned:
            expected=independent.Model(ram,wram)
            if address==0x037FF82C:
                result=expected.envelope(NODE,case['step'])
                if actual[0]!=result:
                    raise ValueError('Full-word signed attenuation result differs')
            elif address==0x037FF8D4:
                expected.attack(NODE,case['value'])
            else:
                expected.lfo(NODE)
            if expected.writes!=writes[first:]:
                raise ValueError('Independent ordered parameter stores differ: '+repr((address,case,writes[first:],expected.writes)))
            for base in (memory.BASE,memory.DATA):
                if bytes(cpu.mem_read(base,len(expected.regions[base])))!=bytes(expected.regions[base]):
                    raise ValueError('Independent full memory and guard preservation differs')
            if actual[4:12]!=registers[4:12] or actual[-2:]!=registers[-2:]:
                raise ValueError('Leaf saved-register/stack/return ABI differs')
            ram,wram=[bytes(expected.regions[key]) for key in (memory.DATA,memory.BASE)]
        masked=bytearray(cpu.mem_read(memory.BASE,0x14000))
        masked[address-memory.BASE:address-memory.BASE+size]=bytes(size)
        records.append(dict(actualReturn=returned,fault=fault,registers=actual,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            writes=writes[first:],ramSha256=digest(bytes(cpu.mem_read(memory.DATA,0x4000))),
            otherWramAndBssSha256=digest(masked),stackSha256=digest(bytes(cpu.mem_read(memory.STACK,0x4000)))))
        if not returned:
            break
    return dict(states=records,visited=sorted(visited),entryBytesExcludedFromStateComparison=size,
        entryByteIdentityMustBeIndependentlyVerified=True)
