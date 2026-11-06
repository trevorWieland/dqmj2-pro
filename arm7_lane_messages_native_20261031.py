import random
from collections import Counter
import match_runtime
from arm7_lane_heap_engine_20261031 import digest,word,store
from arm7_lane_skip_native_20261031 import inventory,executable
from arm7_lane_sdk_signed_division_scope_20261031 import validate_scope,additional
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,DATA,STACK,RETURN=0x037F8000,0x022C0000,0x022E0000,0x022FF000
SIZES={0x037FC6D4:140,0x037FC760:156,0x037FC7FC:116}
QUEUE,ARRAY,OUTPUT,THREAD=DATA+0x1000,DATA+0x2000,DATA+0x3000,DATA+0x4000


def cases(address):
    rows=[]
    counts=[(0,0,0)]+[(count,first,used) for count in range(1,5) for first in range(count) for used in range(count+1)]
    for count,first,used in counts:
        for flags in (0,2):
            for value in (0,1,0x80000000,0xFFFFFFFF):
                for output in ((False,) if address==0x037FC6D4 else (False,True)):
                    rows.append(dict(count=count,first=first,used=used,flags=flags,value=value,output=output,passes=2))
    return rows


def setup(address,body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZES[address]:
        raise ValueError('Message complete own source extent/original module differs')
    scope=validate_scope(raw)
    image=bytearray(raw+random.Random(seed+79).randbytes(0x18000-len(raw)))
    image[address-BASE:address-BASE+len(body)]=body
    regions={BASE:bytes(image),DATA:random.Random(seed+181).randbytes(0x8000),
        STACK:random.Random(seed+283).randbytes(0x4000),RETURN:bytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    entries,ranges=inventory()
    reads,writes,visited,frames,divisions=[],[],set(),[],[]
    nested=Counter()
    state=dict(caller=False,instructions=0,division=None)
    def code(machine,pc,size,unused):
        state['instructions']+=1
        thumb=bool(machine.reg_read(UC_ARM_REG_CPSR)&32)
        if not executable(pc,size,thumb) and not additional(pc,size,thumb):
            raise ValueError('Message execution escaped original qualified ARM/Thumb code: '+hex(pc))
        if not state['caller']:
            return
        if address<=pc<address+SIZES[address]:
            visited.add(pc)
        if state['division'] is not None and pc==state['division']['lr']:
            quotient=machine.reg_read(match_runtime.REGISTERS[0])
            remainder=machine.reg_read(match_runtime.REGISTERS[1])
            expected=divmod(state['division']['numerator'],state['division']['denominator'])
            if [quotient,remainder]!=list(expected):
                raise ValueError('Original compiler-intrinsic division R0 quotient/R1 remainder ABI differs')
            divisions.append(dict(state['division'],quotient=quotient,remainder=remainder,actualReturn=True))
            state['division']=None
        while frames and frames[-1][1]==pc:
            nested[frames.pop()[0]]+=1
        if pc in entries and pc!=address:
            lr=machine.reg_read(match_runtime.REGISTERS[14])
            if lr!=RETURN:
                frames.append([pc,lr])
                if pc==0x03806C38:
                    numerator=machine.reg_read(match_runtime.REGISTERS[0])
                    denominator=machine.reg_read(match_runtime.REGISTERS[1])
                    if numerator>0x7FFFFFFF or not 0<denominator<=0x7FFFFFFF:
                        raise ValueError('Message division escaped bounded nonnegative numerator/positive denominator contract')
                    state['division']=dict(lr=lr,numerator=numerator,denominator=denominator)
    def read(machine,access,target,size,value,unused):
        if state['caller']:
            reads.append([target,size])
    def write(machine,access,target,size,value,unused):
        if state['caller']:
            writes.append([target,size,value&((1<<size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    def invoke(entry,args,caller=False,budget=100000):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:len(args)]=[value&0xFFFFFFFF for value in args]
        initial[13:]=[STACK+0x3000,RETURN]
        cpsr=0x1F|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
        cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        state.update(caller=caller,division=None)
        reads.clear()
        writes.clear()
        frames.clear()
        divisions.clear()
        nested.clear()
        start=state['instructions']
        fault=None
        try:
            cpu.emu_start(entry,RETURN,timeout=500000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not actual:
            return dict(actualReturn=False,entry=hex(entry),fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),
                instructions=state['instructions']-start,postFaultStateExcluded=True)
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=cpsr&255:
            raise ValueError('Message preserved register/SP/LR/processor-control ABI differs')
        if bytes(cpu.mem_read(STACK+0x3000,0x1000))!=regions[STACK][0x3000:] or bytes(cpu.mem_read(RETURN,0x1000))!=regions[RETURN]:
            raise ValueError('Message caller stack/return guards changed')
        if caller and (frames or state['division'] is not None):
            raise ValueError('Message original helper frames did not actually return')
        return dict(actualReturn=True,entry=hex(entry),arguments=args,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            instructions=state['instructions']-start)
    prerequisite=invoke(0x037FC6AC,[QUEUE,ARRAY,case['count']])
    if not prerequisite['actualReturn']:
        raise ValueError('Original message queue initializer did not actually return')
    for offset,value in ((0x18,case['first']),(0x1C,case['used'])):
        cpu.mem_write(QUEUE+offset,value.to_bytes(4,'little'))
    for index in range(max(case['count'],1)):
        cpu.mem_write(ARRAY+index*4,((case['value']+index*0x71020305)&0xFFFFFFFF).to_bytes(4,'little'))
    return dict(cpu=cpu,address=address,case=case,seed=seed,regions=regions,invoke=invoke,reads=reads,writes=writes,
        visited=visited,frames=frames,nested=nested,divisions=divisions,state=state,prerequisite=prerequisite,signedDivisionScope=scope)


def model(memory,address,args):
    stores=[]
    read=lambda target:word(memory,target)
    put=lambda target,value:store(memory,target,value,stores)
    count,first,used=read(QUEUE+0x14),read(QUEUE+0x18),read(QUEUE+0x1C)
    if address==0x037FC6D4:
        if count<=used:
            return 0,stores
        last=(first+used)%count
        put(read(QUEUE+0x10)+last*4,args[1])
        put(QUEUE+0x1C,used+1)
        return 1,stores
    if used==0:
        return 0,stores
    if args[1]:
        put(args[1],read(read(QUEUE+0x10)+first*4))
    if address==0x037FC760:
        put(QUEUE+0x18,(first+1)%count)
        put(QUEUE+0x1C,used-1)
    return 1,stores


def execute(prepared,budget=100000):
    cpu,address,case=prepared['cpu'],prepared['address'],prepared['case']
    states=[]
    for iteration in range(case['passes']):
        value=case['value'] if address==0x037FC6D4 else OUTPUT if case['output'] else 0
        args=[QUEUE,value,case['flags']]
        expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in prepared['regions'].items() if base!=STACK}
        result,stores=model(expected,address,args)
        returned=prepared['invoke'](address,args,caller=True,budget=budget)
        if not returned['actualReturn']:
            states.append(returned)
            break
        nonstack=[row for row in prepared['writes'] if not STACK<=row[0]<STACK+0x4000]
        if returned['registers'][0]!=result or sorted(nonstack)!=sorted(stores):
            raise ValueError('Independent message capacity/ring-order/null-output/word/store-footprint model differs')
        if any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):
            raise ValueError('Independent complete message queue memory/effect model differs')
        states.append(dict(execution=returned,actualReturn=True,orderedNonstackWrites=nonstack,
            nonstackReads=[row for row in prepared['reads'] if not STACK<=row[0]<STACK+0x4000],
            actualNestedReturns={hex(pc):count for pc,count in sorted(prepared['nested'].items())},
            originalSignedDivisionAbi=list(prepared['divisions']),
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()},
            independentCompleteMessageRingAndFootprintModel=True))
    return dict(case=case,states=states,visited=sorted(prepared['visited']),
        originalInitializer=prepared['prerequisite'],signedDivisionInstructionScope=prepared['signedDivisionScope'])


def unsupported_block(address,body):
    case=dict(count=1,first=0,used=1 if address==0x037FC6D4 else 0,flags=1,value=0x12345678,output=True,passes=1)
    prepared=setup(address,body,case,37)
    cpu=prepared['cpu']
    for target,value in ((0x038076F4,1),(0x038076F8,0x03807718),(0x03807718,THREAD),(THREAD+0x48,1),(THREAD+0x54,1)):
        cpu.mem_write(target,value.to_bytes(4,'little'))
    args=[QUEUE,case['value'] if address==0x037FC6D4 else OUTPUT,1]
    result=prepared['invoke'](address,args,caller=True,budget=1000)
    if result['actualReturn']:
        raise ValueError('Blocked message with no scheduler actor unexpectedly received return credit')
    return dict(execution=result,visitedOwnInstructionAddresses=sorted(prepared['visited']),returnCredit=0,postFaultStateExcluded=True,
        context='Synthetic current-thread pointer and scheduler-disabled count1; actual sleep/queue/reschedule helpers execute without providers',
        limitation='Instruction exhaustion establishes unsupported bounded blocking only; no post-boundary state or general asynchronous behavior is credited')
