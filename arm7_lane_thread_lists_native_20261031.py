import random
import match_runtime
from arm7_lane_heap_engine_20261031 import word,store,digest
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,DATA,STACK,RETURN=0x037F8000,0x022C0000,0x022E0000,0x022FF000
SIZES={0x037FBCEC:120,0x037FBD64:88,0x037FBDEC:96,0x037FBE4C:68}
CODES={address:size-(4 if address in (0x037FBDEC,0x037FBE4C) else 0) for address,size in SIZES.items()}
QUEUE,GLOBAL_HEAD=DATA+0x100,0x038076F0+0x2C


def cases(address):
    rows=[]
    for priorities in ([],[1],[0,1,0xFFFFFFFF],[1,1,1]):
        if address in (0x037FBCEC,0x037FBDEC):
            rows.extend(dict(priorities=priorities,priority=priority,target='new',passes=2)
                for priority in (0,1,2,0xFFFFFFFF))
            if address==0x037FBCEC:
                rows.extend(dict(priorities=priorities,priority=priorities[index],target=index,passes=2)
                    for index in range(len(priorities)))
        else:
            rows.extend(dict(priorities=priorities,target=index,passes=2) for index in [*range(len(priorities)),'missing'])
    return rows


def setup(address,body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZES[address]:
        raise ValueError('Thread-list complete own unit/original module differs')
    image=bytearray(raw+random.Random(seed+73).randbytes(0x18000-len(raw)))
    image[address-BASE:address-BASE+len(body)]=body
    regions={BASE:bytes(image),DATA:random.Random(seed+173).randbytes(0x8000),
        STACK:random.Random(seed+271).randbytes(0x4000),RETURN:bytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    def put(target,value):
        cpu.mem_write(target,(value&0xFFFFFFFF).to_bytes(4,'little'))
    nodes=[DATA+0x1000+index*0x100 for index in range(len(case['priorities']))]
    for index,node in enumerate(nodes):
        previous=nodes[index-1] if index else 0
        following=nodes[index+1] if index+1<len(nodes) else 0
        put(node+0x54,case['priorities'][index])
        put(node+0x60,previous)
        put(node+0x64,following)
        put(node+0x4C,following)
    put(QUEUE,nodes[0] if nodes else 0)
    put(QUEUE+4,nodes[-1] if nodes else 0)
    put(GLOBAL_HEAD,nodes[0] if nodes else 0)
    for pointer,priority in ((DATA+0x3000,case.get('priority',0)),(DATA+0x4000,case.get('priority',0)^0xFFFFFFFF)):
        put(pointer+0x54,priority)
        put(pointer+0x4C,0)
    writes,reads,visited=[],[],set()
    def code(machine,pc,size,unused):
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not address<=pc<address+CODES[address]:
            raise ValueError('Thread-list execution escaped exact own ARM code or executed its pool')
        visited.add(pc)
    def read(machine,access,target,size,value,unused):
        reads.append([target,size])
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1<<size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    return dict(cpu=cpu,address=address,case=case,seed=seed,regions=regions,nodes=nodes,reads=reads,writes=writes,visited=visited)


def model(memory,address,args):
    stores=[]
    read=lambda target:word(memory,target)
    put=lambda target,value:store(memory,target,value,stores)
    if address==0x037FBCEC:
        queue,thread=args
        current=read(queue)
        while current and read(current+0x54)<=read(thread+0x54):
            if current==thread:
                return None,stores
            current=read(current+0x64)
        previous=read(current+0x60) if current else read(queue+4)
        if not previous:
            put(queue,thread)
        else:
            put(previous+0x64,thread)
        put(thread+0x60,previous)
        put(thread+0x64,current)
        if current:
            put(current+0x60,thread)
        else:
            put(queue+4,thread)
        return None,stores
    if address==0x037FBD64:
        queue,thread=args
        current=read(queue)
        while current:
            following=read(current+0x64)
            if current==thread:
                previous=read(current+0x60)
                if read(queue)==current:
                    put(queue,following)
                else:
                    put(previous+0x64,following)
                if read(queue+4)==current:
                    put(queue+4,previous)
                else:
                    put(following+0x60,previous)
                break
            current=following
        return current,stores
    thread=args[0]
    current,previous=read(GLOBAL_HEAD),0
    while current and (read(current+0x54)<read(thread+0x54) if address==0x037FBDEC else current!=thread):
        previous,current=current,read(current+0x4C)
    if address==0x037FBDEC:
        if not previous:
            put(thread+0x4C,read(GLOBAL_HEAD))
            put(GLOBAL_HEAD,thread)
        else:
            put(thread+0x4C,read(previous+0x4C))
            put(previous+0x4C,thread)
    else:
        put(GLOBAL_HEAD if not previous else previous+0x4C,read(thread+0x4C))
    return None,stores


def execute(prepared,budget=10000):
    cpu,address,case,seed=prepared['cpu'],prepared['address'],prepared['case'],prepared['seed']
    states=[]
    nodes=prepared['nodes']
    for iteration in range(case['passes']):
        if address==0x037FBCEC:
            pointer=DATA+0x3000 if case['target']=='new' else nodes[case['target']]
            args=[QUEUE,pointer]
        elif address==0x037FBD64:
            args=[QUEUE,DATA+0x3000 if case['target']=='missing' else nodes[case['target']]]
        elif address==0x037FBDEC:
            args=[DATA+(0x3000 if iteration==0 else 0x4000)]
        else:
            first=DATA+0x3000 if case['target']=='missing' else nodes[case['target']]
            second=next((node for node in nodes if node!=first),DATA+0x4000)
            args=[first if iteration==0 else second]
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:len(args)]=args
        initial[13:]=[STACK+0x3000,RETURN]
        cpsr=0x1F|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
        cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in prepared['regions'].items() if base!=STACK}
        value,stores=model(expected,address,args)
        prepared['reads'].clear()
        prepared['writes'].clear()
        fault=None
        try:
            cpu.emu_start(address,RETURN,timeout=100000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not actual:
            states.append(dict(actualReturn=False,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateExcluded=True))
            break
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        nonstack=[row for row in prepared['writes'] if not STACK<=row[0]<STACK+0x4000]
        if value is not None and registers[0]!=value or sorted(nonstack)!=sorted(stores):
            raise ValueError('Independent thread-list unsigned-priority/pointer/link/store-footprint/result model differs')
        if any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):
            raise ValueError('Independent complete thread-list memory effect/preservation model differs')
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=cpsr&255:
            raise ValueError('Thread-list preserved register/SP/LR/processor-control ABI differs')
        if bytes(cpu.mem_read(STACK+0x3000,0x1000))!=prepared['regions'][STACK][0x3000:]:
            raise ValueError('Thread-list caller stack guard changed')
        states.append(dict(actualReturn=True,fault=None,arguments=args,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            orderedNonstackWrites=nonstack,nonstackReads=[row for row in prepared['reads'] if not STACK<=row[0]<STACK+0x4000],
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()},
            actualNestedReturns={},independentCompleteThreadListMemoryAndFootprintModel=True))
    return dict(case=case,states=states,visited=sorted(prepared['visited']))
