import hashlib
import random
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,STACK,RETURN,MMIO=0x037F8000,0x023E0000,0x023FF000,0x04000000
SIZES={0x037FE804:204,0x037FE8D0:172,0x037FE97C:164,0x037FEA48:120,0x037FEAD8:120}
CODES={0x037FE804:184,0x037FE8D0:152,0x037FE97C:144,0x037FEA48:108,0x037FEAD8:100}
MASTER,FACTOR,PANS,VOLUMES=0x038075C8,0x03807980,0x03807984,0x03807994
SCALE,SCALE_CODE=0x037FEC40,100


def digest(data):
    return hashlib.sha256(data).hexdigest()


def signed(value):
    value&=0xFFFFFFFF
    return value-0x100000000 if value&0x80000000 else value


def scaled(volume,pan,factor):
    pan=signed(pan)
    if pan<24:
        coefficient=(factor*((pan+40)&0xFFFFFFFF)+(((32767-factor)&0xFFFFFFFF)<<6))&0xFFFFFFFF
    elif pan>104:
        coefficient=(((-factor)&0xFFFFFFFF)*((pan-40)&0xFFFFFFFF)+(((factor+32767)&0xFFFFFFFF)<<6))&0xFFFFFFFF
    else:
        return volume&0xFFFFFFFF
    return (signed((volume*coefficient)&0xFFFFFFFF)>>21)&0xFFFFFFFF


def cases(address):
    settings=((0xFFFFFFFF,0),(0xFFFFFFFF,1),(0xFFFFFFFF,32767),(0xFFFFFFFF,32768),(0xFFFFFFFF,0x7FFFFFFF),
        (0xFFFFFFFF,0x80000000),(0x80000000,0xFFFFFFFF),(0,1),(23,1),(24,32767),(104,1),(0x7FFFFFFF,1))
    rows=[dict(channel=channel,master=master,factor=factor,pattern=(channel+index)%6,
        pan=(0,23,24,104,105,127,255,0xFFFFFFFF,0x80000000,0x7FFFFFFF)[(channel+index)%10],passes=2)
        for channel in range(16) for index,(master,factor) in enumerate(settings)]
    rows.extend(dict(channel=channel,master=master,factor=factor,pattern=(index+channel)%6,pan=pan,passes=2)
        for index,pan in enumerate((0,23,24,104,105,127,255,0xFFFFFFFF,0x80000000,0x7FFFFFFF))
        for channel in (0,1,3,15) for master in (0xFFFFFFFF,0,127) for factor in (0,1,32767))
    for row in rows:
        patterns=((0,)*9,(0xFFFFFFFF,)*9,(0x80000000,)*9,
            (0x02000004,3,2,0xFFFF,0x3FFFFF,127,3,0xFFFF,7),
            (0x80000001,0x7FFFFFFF,0x80000000,0xFFFFFFFF,0x10000,0x80000000,0xFFFFFFFF,0x80000000,0xFFFFFFFF),
            (0x12345678,1,0,0x1234,0x1020304,0xCAFEBABE,0x10203,0x12345678,5))
        data,fmt,loop,start,length,volume,divisor,timer,duty=patterns[row['pattern']]
        channel,pan=row['channel'],row['pan']
        args={0x037FE804:[channel,data,fmt,loop,start,length,volume,divisor,timer,pan],
            0x037FE8D0:[channel,duty,volume,divisor,timer,pan],0x037FE97C:[channel,volume,divisor,timer,pan],
            0x037FEA48:[channel,volume,divisor],0x037FEAD8:[channel,pan]}[address]
        row['arguments']=list(args)
    return rows


def model(address,wram,mmio,args):
    wram,mmio=bytearray(wram),bytearray(mmio)
    writes,calls=[],[]
    channel=args[0]
    if not 0<=channel<16:
        raise ValueError('Channel source/model only supports measured indices0..15')
    def read(target,size=4):
        data,base=(wram,BASE) if BASE<=target<BASE+len(wram) else (mmio,MMIO)
        return int.from_bytes(data[target-base:target-base+size],'little')
    def store(target,value,size):
        value&=(1 << size*8)-1
        data,base=(wram,BASE) if BASE<=target<BASE+len(wram) else (mmio,MMIO)
        data[target-base:target-base+size]=value.to_bytes(size,'little')
        writes.append([target,size,value])
    master,factor=signed(read(MASTER)),read(FACTOR)
    should_scale=signed(factor)>0 and bool(0xFFF5&(1<<channel))
    def calculate(volume,pan):
        calls.append([volume&0xFFFFFFFF,pan&0xFFFFFFFF])
        return scaled(volume,pan,factor)
    control=0x04000400+channel*16
    if address in (0x037FE804,0x037FE8D0,0x037FE97C):
        pan=args[-1]
        store(PANS+channel,pan,1)
        if master>=0:
            pan=master
        volume=args[{0x037FE804:6,0x037FE8D0:2,0x037FE97C:1}[address]]
        store(VOLUMES+channel,volume,1)
        if should_scale:
            volume=calculate(volume,pan)
        if address==0x037FE804:
            unused,data,fmt,loop,start,length,unused,divisor,timer,unused=args
            value=(fmt<<29)|(loop<<27)|(pan<<16)|(divisor<<8)|volume
        elif address==0x037FE8D0:
            unused,duty,unused,divisor,timer,unused=args
            value=0x60000000|(duty<<24)|(pan<<16)|(divisor<<8)|volume
        else:
            unused,unused,divisor,timer,unused=args
            value=0x60000000|(pan<<16)|(divisor<<8)|volume
        store(control,value,4)
        store(control+8,-timer,2)
        if address==0x037FE804:
            store(control+10,start,2)
            store(control+12,length,4)
            store(control+4,data,4)
    elif address==0x037FEA48:
        unused,volume,divisor=args
        store(VOLUMES+channel,volume,1)
        if should_scale:
            volume=calculate(volume,read(control+2,1))
        store(control,(divisor<<8)|volume,2)
    else:
        pan=args[1]
        store(PANS+channel,pan,1)
        if master>=0:
            pan=master
        store(control+2,pan,1)
        if should_scale:
            store(control,calculate(read(VOLUMES+channel,1),pan),1)
    return dict(wram=bytes(wram),mmio=bytes(mmio),orderedStores=writes,scaleArguments=calls)


def setup(address,body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZES[address]:
        raise ValueError('Measured host WRAM namespace/complete channel source differs')
    wram=bytearray(raw+random.Random(seed+43).randbytes(0x18000-len(raw)))
    wram[address-BASE:address-BASE+len(body)]=body
    wram[MASTER-BASE:MASTER-BASE+4]=case['master'].to_bytes(4,'little')
    wram[FACTOR-BASE:FACTOR-BASE+4]=case['factor'].to_bytes(4,'little')
    regions={BASE:bytes(wram),STACK:random.Random(seed+67).randbytes(0x4000),RETURN:bytes(0x1000),MMIO:random.Random(seed+173).randbytes(0x10000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first,data in regions.items():
        cpu.mem_map(first,len(data))
        cpu.mem_write(first,data)
    cpu.mem_write(0x04000402+case['channel']*16,bytes([case['pan']&0xFF]))
    writes,reads,visited,calls=[],[],set(),[]
    state=dict(instructions=0,scaleLr=None,nestedReturns=0)
    def code(machine,pc,size,unused):
        state['instructions']+=1
        if machine.reg_read(UC_ARM_REG_CPSR)&32 or not (address<=pc<address+CODES[address] or SCALE<=pc<SCALE+SCALE_CODE):
            raise ValueError('Channel source execution escaped exact ARM caller/scale-helper code')
        if state['scaleLr']==pc:
            state['nestedReturns']+=1
            state['scaleLr']=None
        if address<=pc<address+CODES[address]:
            visited.add(pc)
        if pc==SCALE:
            calls.append([machine.reg_read(register) for register in match_runtime.REGISTERS[:2]])
            state['scaleLr']=machine.reg_read(match_runtime.REGISTERS[14])
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1 << size*8)-1)])
    def read(machine,access,target,size,value,unused):
        reads.append([target,size])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    return dict(cpu=cpu,case=case,seed=seed,address=address,regions=regions,writes=writes,reads=reads,visited=visited,calls=calls,state=state)


def execute(prepared,budget=10000):
    cpu,case,address,seed=prepared['cpu'],prepared['case'],prepared['address'],prepared['seed']
    states=[]
    for iteration in range(case['passes']):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:min(4,len(case['arguments']))]=case['arguments'][:4]
        initial[13:]=[STACK+0x3000,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,0x1F|((seed&1)*128)|((seed&15)<<28))
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        extra=case['arguments'][4:]
        cpu.mem_write(STACK+0x3000,b''.join(word.to_bytes(4,'little') for word in extra))
        caller_stack=bytes(cpu.mem_read(STACK+0x3000,0x1000))
        before_wram=bytes(cpu.mem_read(BASE,0x18000))
        before_mmio=bytes(cpu.mem_read(MMIO,0x10000))
        prepared['writes'].clear()
        prepared['reads'].clear()
        prepared['calls'].clear()
        prepared['state'].update(scaleLr=None,nestedReturns=0)
        first=prepared['state']['instructions']
        fault=None
        try:
            cpu.emu_start(address,RETURN,timeout=100000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not returned:
            states.append(dict(actualReturn=False,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateExcluded=True))
            break
        expected=model(address,before_wram,before_mmio,case['arguments'])
        nonstack=[row for row in prepared['writes'] if not STACK<=row[0]<STACK+0x4000]
        if nonstack!=expected['orderedStores'] or prepared['calls']!=expected['scaleArguments']:
            raise ValueError('Independent channel/cache/scale-ABI/ordered-store model differs')
        if bytes(cpu.mem_read(BASE,0x18000))!=expected['wram'] or bytes(cpu.mem_read(MMIO,0x10000))!=expected['mmio']:
            raise ValueError('Independent complete WRAM/MMIO/guard model differs')
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:]:
            raise ValueError('Channel source changed preserved registers or caller SP/LR')
        if bytes(cpu.mem_read(STACK+0x3000,0x1000))!=caller_stack or bytes(cpu.mem_read(RETURN,0x1000))!=prepared['regions'][RETURN]:
            raise ValueError('Channel source changed caller-visible stack/return guards')
        states.append(dict(actualReturn=True,fault=None,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            instructions=prepared['state']['instructions']-first,nonstackWrites=nonstack,
            nonstackReads=[row for row in prepared['reads'] if not STACK<=row[0]<STACK+0x4000],
            scaleArguments=list(prepared['calls']),actualNestedScaleReturns=prepared['state']['nestedReturns'],
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()},
            independentCompleteMemoryAndOrderedStoreModel=True))
    return dict(case=case,states=states,visited=sorted(prepared['visited']))
