import hashlib
import random
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,STACK,RETURN=0x037F8000,0x023E0000,0x023FF000
ADDRESS,SIZE,CODE=0x037FEDD8,116,112
VENEER,THUMB,CONTINUATION=0x037FEE4C,0x0380382C,0x037FEE04


def digest(data):
    return hashlib.sha256(data).hexdigest()


def signed(value):
    return value-0x100000000 if value&0x80000000 else value


def model(value,volume):
    value=max(-723,min(0,signed(value)))
    divisor=3 if value<-240 else 2 if value<-120 else 1 if value<-60 else 0
    return value+723,(volume|(divisor<<8))&0xFFFF


def cases(address):
    if address!=ADDRESS:
        raise ValueError('Unqualified volume entry')
    values=sorted(set(range(-725,3))|{-0x80000000,-0x7FFFFFFF,-1000000,1000000,0x7FFFFFFF})
    boundaries={-0x80000000,-724,-723,-241,-240,-121,-120,-61,-60,-1,0,1,0x7FFFFFFF}
    return [dict(value=value&0xFFFFFFFF,volume=volume,passes=2 if value in boundaries else 1)
        for value in values for volume in (0,1,126,127)]


def setup(address,body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or address!=ADDRESS or len(body)!=SIZE:
        raise ValueError('Measured ARM7 namespace or complete volume body differs')
    if int.from_bytes(raw[VENEER-BASE+8:VENEER-BASE+12],'little')!=THUMB|1 or raw[THUMB-BASE:THUMB-BASE+4]!=bytes.fromhex('1cdf7047'):
        raise ValueError('Original ARM-to-Thumb veneer or SVC1C/BX-LR identity differs')
    wram=bytearray(raw+random.Random(seed+43).randbytes(0x18000-len(raw)))
    wram[address-BASE:address-BASE+len(body)]=body
    regions={BASE:bytes(wram),STACK:random.Random(seed+67).randbytes(0x4000),RETURN:bytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first,data in regions.items():
        cpu.mem_map(first,len(data))
        cpu.mem_write(first,data)
    state=dict(instructions=0,pending=None,thumbEntries=0,helperReturns=0,unsupported=None)
    reads,writes,visited,services=[],[],set(),[]
    def code(uc,pc,size,unused):
        state['instructions']+=1
        thumb=bool(uc.reg_read(UC_ARM_REG_CPSR)&32)
        if not ((not thumb and size==4 and pc%4==0 and (ADDRESS<=pc<ADDRESS+CODE or VENEER<=pc<VENEER+8)) or (thumb and size==2 and THUMB<=pc<THUMB+4)):
            raise ValueError('Volume execution escaped qualified ARM caller/veneer/Thumb stub')
        if ADDRESS<=pc<ADDRESS+CODE:
            visited.add(pc)
        if pc==VENEER:
            registers=[uc.reg_read(register) for register in match_runtime.REGISTERS]
            index,_=model(case['value'],0)
            if registers[0]!=index or registers[14]!=CONTINUATION or state['pending'] is not None:
                raise ValueError('Original volume service caller supplied an incorrect index/LR')
            state['pending']=registers
        if pc==THUMB:
            if state['pending'] is None or uc.reg_read(match_runtime.REGISTERS[12])!=THUMB|1:
                raise ValueError('Original ARM veneer did not transfer through its measured Thumb pointer')
            state['thumbEntries']+=1
        if pc==CONTINUATION:
            before=state['pending']
            after=[uc.reg_read(register) for register in match_runtime.REGISTERS]
            if before is None or after[4:12]!=before[4:12] or after[13:]!=before[13:]:
                raise ValueError('Original Thumb wrapper did not actually return with preserved caller ABI')
            state.update(helperReturns=state['helperReturns']+1,pending=None)
    def interrupt(uc,number,unused):
        pc=uc.reg_read(UC_ARM_REG_PC)
        argument=uc.reg_read(match_runtime.REGISTERS[0])
        if number!=2 or pc!=THUMB+2 or not uc.reg_read(UC_ARM_REG_CPSR)&32 or not 0<=argument<=723:
            raise ValueError('Unqualified BIOS service/instruction/argument boundary')
        if case['volume'] is None:
            state['unsupported']=dict(kind='original-BIOS-service-unavailable',service=28,index=argument,pc=hex(pc))
            uc.emu_stop()
            return
        if not 0<=case['volume']<=127:
            raise ValueError('Synthetic volume result exceeded the explicit7-bit service contract')
        services.append([28,argument,case['volume']])
        uc.reg_write(match_runtime.REGISTERS[0],case['volume'])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_INTR,interrupt)
    cpu.hook_add(UC_HOOK_MEM_READ,lambda uc,access,target,size,value,unused:reads.append([target,size]))
    cpu.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,target,size,value,unused:writes.append([target,size,value&((1<<(size*8))-1)]))
    return dict(cpu=cpu,case=case,seed=seed,regions=regions,state=state,reads=reads,writes=writes,visited=visited,services=services)


def execute(prepared,budget=1000):
    cpu,case,seed=prepared['cpu'],prepared['case'],prepared['seed']
    states=[]
    for iteration in range(case['passes']):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[0]=case['value']
        initial[13:]=[STACK+0x3000,RETURN]
        flags=0x1F|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
        cpu.reg_write(UC_ARM_REG_CPSR,flags)
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        guard=bytes(cpu.mem_read(STACK+0x3000,0x1000))
        for name in ('reads','writes','services'):
            prepared[name].clear()
        prepared['state'].update(pending=None,thumbEntries=0,helperReturns=0,unsupported=None)
        first=prepared['state']['instructions']
        fault=None
        try:
            cpu.emu_start(ADDRESS,RETURN,timeout=100000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None and prepared['state']['unsupported'] is None
        if not actual:
            states.append(dict(actualReturn=False,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),fault=fault,
                unsupported=prepared['state']['unsupported'],instructions=prepared['state']['instructions']-first,postBoundaryStateExcluded=True))
            break
        index,expected=model(case['value'],case['volume'])
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if registers[0]!=expected or registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=flags&255:
            raise ValueError('Independent packed-u16 return or preserved CPU ABI model differs')
        if prepared['services']!=[[28,index,case['volume']]] or prepared['state']['thumbEntries']!=1 or prepared['state']['helperReturns']!=1 or prepared['state']['pending'] is not None:
            raise ValueError('Synthetic service call, actual Thumb return and interworking tail transfer counts differ')
        if any(not STACK<=row[0]<STACK+0x4000 for row in prepared['writes']) or any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in prepared['regions'].items() if base!=STACK) or bytes(cpu.mem_read(STACK+0x3000,0x1000))!=guard:
            raise ValueError('Pure volume calculation changed nonstack memory or caller stack guards')
        states.append(dict(actualReturn=True,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            instructions=prepared['state']['instructions']-first,syntheticBiosServices=prepared['services'][:],
            actualThumbWrapperReturns=1,actualArmVeneerTailTransfers=1,ordinaryArmVeneerReturnCredit=0,
            orderedReads=prepared['reads'][:],orderedWrites=prepared['writes'][:],
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()}))
    return dict(case=case,states=states,visited=sorted(prepared['visited']))
