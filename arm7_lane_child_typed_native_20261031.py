import random
import match_runtime
from arm7_lane_heap_engine_20261031 import word,store,digest
from arm7_lane_thread_lists_native_20261031 import cases as queue_cases,model as queue_model
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,DATA,STACK,RETURN,SHARED=0x037F8000,0x023C0000,0x023E0000,0x023FF000,0x027FF000
TABLE,QUEUE=0x027FFDA0,DATA+0x100
SIZES={0x037FCA58:120,0x037FD090:20,0x037FD07C:20,0x037FCF7C:20}


def cases(address):
    if address==0x037FCA58:
        return queue_cases(0x037FBCEC)
    return [dict(index=index,value=value,passes=2) for index in range(9) for value in (0,1,0x027E0000,0x0380B4E4,0x80000000,0xFFFFFFFF)]


def setup(address,body,case,seed):
    raw=(ROOT/'extract/utility/runtime/utility-child-arm7-wram.bin').read_bytes()
    if digest(raw)!='13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6' or len(body)!=SIZES[address]:
        raise ValueError('Utility-child ARM7 complete original namespace/module/unit differs')
    image=bytearray(raw+random.Random(seed+89).randbytes(0x18000-len(raw)))
    image[address-BASE:address-BASE+len(body)]=body
    regions={BASE:bytes(image),DATA:random.Random(seed+181).randbytes(0x8000),
        SHARED:random.Random(seed+237).randbytes(0x1000),STACK:random.Random(seed+311).randbytes(0x4000),RETURN:bytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    def put(target,value):
        cpu.mem_write(target,(value&0xFFFFFFFF).to_bytes(4,'little'))
    nodes=[DATA+0x1000+index*0x100 for index in range(len(case.get('priorities',[])))]
    for index,node in enumerate(nodes):
        put(node+0x54,case['priorities'][index])
        put(node+0x60,nodes[index-1] if index else 0)
        put(node+0x64,nodes[index+1] if index+1<len(nodes) else 0)
    put(QUEUE,nodes[0] if nodes else 0)
    put(QUEUE+4,nodes[-1] if nodes else 0)
    put(DATA+0x3000+0x54,case.get('priority',0))
    if 'index' in case:
        for index in range(18):
            put(TABLE+index*4,(case['value']+index*0x1020304)&0xFFFFFFFF)
    reads,writes,visited=[],[],set()
    def code(machine,pc,size,unused):
        if machine.reg_read(UC_ARM_REG_CPSR)&32 or size!=4 or not address<=pc<address+SIZES[address]:
            raise ValueError('Utility-child leaf escaped complete own ARM instructions')
        visited.add(pc)
    def read(machine,access,target,size,value,unused):
        reads.append([target,size])
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1<<size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    return dict(cpu=cpu,address=address,case=case,seed=seed,regions=regions,nodes=nodes,reads=reads,writes=writes,visited=visited)


def execute(machine,budget=10000):
    cpu,address,case,seed=machine['cpu'],machine['address'],machine['case'],machine['seed']
    states=[]
    for iteration in range(2):
        expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in machine['regions'].items() if base!=STACK}
        if address==0x037FCA58:
            pointer=DATA+0x3000 if case['target']=='new' else machine['nodes'][case['target']]
            args=[QUEUE,pointer]
            value,stores=queue_model(expected,0x037FBCEC,args)
        else:
            args=[case['index']]
            cell=TABLE+(36 if address==0x037FD090 else 0)+args[0]*4
            stores=[]
            value=word(expected,cell)
            if address==0x037FCF7C:
                args.append(case['value']^(0xFFFFFFFF if iteration else 0))
                store(expected,cell,args[1],stores)
                value=None
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:len(args)]=args
        initial[13:]=[STACK+0x3000,RETURN]
        cpsr=0x1F|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
        cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
        for register,item in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,item)
        machine['reads'].clear()
        machine['writes'].clear()
        fault=None
        try:
            cpu.emu_start(address,RETURN,timeout=500000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not actual:
            states.append(dict(actualReturn=False,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateExcluded=True))
            break
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        actual_writes=[row for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000]
        if value is not None and registers[0]!=value or sorted(actual_writes)!=sorted(stores):
            raise ValueError('Independent utility-child queue/arena return and exact write model differs')
        if any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):
            raise ValueError('Complete utility-child mapped memory/preservation model differs')
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=cpsr&255:
            raise ValueError('Utility-child saved-register/SP/LR/processor-control ABI differs')
        if bytes(cpu.mem_read(STACK+0x3000,0x1000))!=machine['regions'][STACK][0x3000:]:
            raise ValueError('Utility-child caller stack guard changed')
        states.append(dict(actualReturn=True,arguments=args,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            orderedNonstackWrites=actual_writes,nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in machine['regions'].items()},
            actualNestedReturns={},independentCompleteMemoryEffectsAndWriteFootprintModel=True))
    return dict(case=case,states=states,visited=sorted(machine['visited']))
