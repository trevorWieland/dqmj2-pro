import hashlib
import random
from collections import Counter
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,DATA,STACK,RETURN,MMIO=0x037F8000,0x023C0000,0x023E0000,0x023FF000,0x04000000
SIZES={0x037FFB30:176,0x037FFBE0:224,0x037FFCC0:56}
CODES={0x037FFB30:168,0x037FFBE0:216,0x037FFCC0:52}
MASKS,CHANNELS,PROBE,LOG=0x03807EB8,0x03807EE0,0x023C7000,0x023C7800
HELPERS={0x037FEA20:40,0x037FFB1C:20}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address):
    masks=(0,0xFFFF,0xFFFFFFFF,0x10000,0x80000000,0x10001,0x80008000,0xAAAA5555)+tuple(1<<i for i in range(16))
    locks=(0,0xFFFFFFFF,0x55555555,0xAAAAAAAA)
    weak=(0,1,2,3,0x80000000,0xFFFFFFFF,0x10000,0x10001)
    rows=[dict(mask=mask,strong=strong,weakLock=(0x12345678^index*0x1020304)&0xFFFFFFFF,
        weak=weak[(index+index2)%len(weak)],callbacks=(0,0xFFFF,0xAAAA,0x5555)[(index+index2)%4],passes=2)
        for index,mask in enumerate(masks) for index2,strong in enumerate(locks)]
    rows.extend(dict(mask=1<<channel,strong=(1<<channel) if locked else 0,weakLock=0x80000000,
        weak=channel&1,callbacks=(1<<channel) if callback else 0,passes=2)
        for channel in range(16) for locked in (False,True) for callback in (False,True))
    return rows


def model(memory,address,args):
    expected={base:bytearray(data) for base,data in memory.items()}
    writes,calls,callbacks=[],[],[]
    def read(target,width=4):
        for base,data in expected.items():
            if base<=target and target+width<=base+len(data):
                return int.from_bytes(data[target-base:target-base+width],'little')
        raise ValueError('Channel-lock model read escaped declared backing')
    def put(target,value,width=4):
        value&=(1<<(width*8))-1
        for base,data in expected.items():
            if base<=target and target+width<=base+len(data):
                data[target-base:target-base+width]=value.to_bytes(width,'little')
                writes.append([target,width,value])
                return
        raise ValueError('Channel-lock model write escaped declared backing')
    mask,weak=args
    if address==0x037FFCC0:
        target=MASKS if weak&1 else MASKS+4
        put(target,read(target)&~mask)
    else:
        for index in range(16):
            if not mask&(1<<index) or read(MASKS+4)&(1<<index):
                continue
            channel=CHANNELS+84*index
            callback=read(channel+0x48)
            if callback:
                if callback!=PROBE:
                    raise ValueError('Only explicitly compiled synthetic callback contracts are supported')
                user=read(channel+0x4C)
                callbacks.append([channel,0,user])
                count=read(LOG)
                if count>=16:
                    raise ValueError('Synthetic callback log exceeds bounded16 events')
                put(LOG+4+12*count,channel)
                put(LOG+8+12*count,0)
                put(LOG+12+12*count,user)
                put(LOG,count+1)
            control=MMIO+0x400+index*16
            calls.append([0x037FEA20,[index,0]])
            put(control,read(control)&0x7FFFFFFF)
            put(channel+0x22,0,1)
            calls.append([0x037FFB1C,[channel]])
            put(channel+0x48,0)
            put(channel+0x4C,0)
            flags=read(channel+3,1)
            if address==0x037FFBE0:
                put(channel+3,flags&7,1)
            put(channel+3,flags&6,1)
        if address==0x037FFBE0:
            target=MASKS if weak&1 else MASKS+4
            put(target,read(target)|mask)
    return dict(memory=expected,writes=writes,calls=calls,callbacks=callbacks)


def setup(address,body,case,seed,callback_probe):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or address not in SIZES or len(body)!=SIZES[address]:
        raise ValueError('Measured host WRAM namespace/full channel-lock body differs')
    payload,proof=callback_probe
    if proof['physicalArgumentWords']!=3 or proof['codeBytes']!=56 or proof['bytes']!=60 or proof['address']!=hex(PROBE) or proof['sourceCredit']!=0 or proof['originalCalleeCredit']!=0 or digest(payload)!=proof['linkedBodySha256']:
        raise ValueError('Synthetic callback scope/ABI/hash differs')
    wram=bytearray(raw+random.Random(seed+43).randbytes(0x18000-len(raw)))
    wram[address-BASE:address-BASE+len(body)]=body
    wram[MASKS-BASE:MASKS-BASE+8]=case['weakLock'].to_bytes(4,'little')+case['strong'].to_bytes(4,'little')
    for index in range(16):
        offset=CHANNELS-BASE+84*index
        wram[offset]=((index+seed)*17)&255
        wram[offset+3]=(index*17+seed*29)&255
        callback=PROBE if case['callbacks']&(1<<index) else 0
        wram[offset+0x48:offset+0x4C]=callback.to_bytes(4,'little')
        user=(0,0x12345678,0x80000000,0xFFFFFFFF)[(index+seed)%4]
        wram[offset+0x4C:offset+0x50]=user.to_bytes(4,'little')
    regions={BASE:bytes(wram),DATA:random.Random(seed+71).randbytes(0x8000),
        STACK:random.Random(seed+67).randbytes(0x4000),RETURN:bytes(0x1000),MMIO:random.Random(seed+173).randbytes(0x10000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first,data in regions.items():
        cpu.mem_map(first,len(data))
        cpu.mem_write(first,data)
    cpu.mem_write(PROBE,payload)
    cpu.mem_write(LOG,bytes(49*4))
    state=dict(instructions=0)
    writes,reads,visited,calls,callbacks,frames=[],[],set(),[],[],[]
    returns=Counter()
    def code(uc,pc,size,unused):
        state['instructions']+=1
        if uc.reg_read(UC_ARM_REG_CPSR)&32 or size!=4 or pc%4 or not (address<=pc<address+CODES[address] or PROBE<=pc<PROBE+56 or any(first<=pc<first+length for first,length in HELPERS.items())):
            raise ValueError('Channel-lock execution escaped qualified ARM source/helper/probe scope')
        if frames and frames[-1][1]==pc:
            returns[frames.pop()[0]]+=1
        if address<=pc<address+CODES[address]:
            visited.add(pc)
        if pc in HELPERS or pc==PROBE:
            args=[uc.reg_read(register) for register in match_runtime.REGISTERS[:3]]
            if pc==PROBE:
                callbacks.append(args)
            else:
                calls.append([pc,args[:2] if pc==0x037FEA20 else args[:1]])
            frames.append((pc,uc.reg_read(match_runtime.REGISTERS[14])))
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,lambda uc,access,target,size,value,unused:reads.append([target,size]))
    cpu.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,target,size,value,unused:writes.append([target,size,value&((1<<(size*8))-1)]))
    return dict(cpu=cpu,address=address,case=case,seed=seed,regions=regions,state=state,writes=writes,reads=reads,
        visited=visited,calls=calls,callbacks=callbacks,frames=frames,returns=returns)


def execute(prepared,budget=20000):
    cpu,address,case,seed=prepared['cpu'],prepared['address'],prepared['case'],prepared['seed']
    states=[]
    for iteration in range(case['passes']):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:2]=[case['mask'],case['weak']]
        initial[13:]=[STACK+0x3000,RETURN]
        flags=0x1F|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
        cpu.reg_write(UC_ARM_REG_CPSR,flags)
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        caller_stack=bytes(cpu.mem_read(STACK+0x3000,0x1000))
        before={base:bytes(cpu.mem_read(base,len(data))) for base,data in prepared['regions'].items() if base!=STACK}
        expected=model(before,address,initial[:2])
        for name in ('writes','reads','calls','callbacks','frames'):
            prepared[name].clear()
        prepared['returns'].clear()
        first=prepared['state']['instructions']
        fault=None
        try:
            cpu.emu_start(address,RETURN,timeout=500000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not actual:
            states.append(dict(actualReturn=False,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),fault=fault,
                instructions=prepared['state']['instructions']-first,postBoundaryStateExcluded=True))
            break
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=flags&255 or bytes(cpu.mem_read(STACK+0x3000,0x1000))!=caller_stack:
            raise ValueError('Channel-lock preserved register/SP/LR/control/stack guards differ')
        if prepared['frames'] or prepared['calls']!=expected['calls'] or prepared['callbacks']!=expected['callbacks']:
            raise ValueError('Independent original helper/callback argument or actual-return model differs')
        stores=[row for row in prepared['writes'] if not STACK<=row[0]<STACK+0x4000]
        if stores!=expected['writes'] or any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected['memory'].items()):
            raise ValueError('Independent complete channel-lock memory/ordered-store model differs')
        states.append(dict(actualReturn=True,pc=hex(RETURN),instructions=prepared['state']['instructions']-first,
            registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=prepared['reads'][:],orderedWrites=prepared['writes'][:],
            helperArguments=prepared['calls'][:],callbackArguments=prepared['callbacks'][:],
            actualNestedReturns={hex(key):value for key,value in sorted(prepared['returns'].items())},
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()}))
    return dict(case=case,states=states,visited=sorted(prepared['visited']))
