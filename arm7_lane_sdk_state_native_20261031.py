import random
import match_runtime
from arm7_lane_channel_five_native_20261031 import digest
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,DATA,STACK,RETURN,MMIO=0x037F8000,0x023C0000,0x023E0000,0x023FF000,0x04000000
SIZES={0x03801C8C:152,0x03801D24:44}
CODES={0x03801C8C:148,0x03801D24:40}
SHARED_POINTER,ALARMS=0x03807EDC,0x03808E60
HELPERS={0x037FEB50:28,0x037FF14C:24}


def cases(address):
    if address==0x03801D24:
        return [dict(pattern=index,passes=2) for index in range(64)]
    result=[dict(pointer=DATA+0x100+(value%2)*0x200,channels=[(value+index*17)&255 for index in range(16)],
        captures=[value,value^255],passes=2) for value in range(256)]
    result.extend(dict(pointer=DATA+0x100,channels=[0xFF if index==selected else 0x7F for index in range(16)],
        captures=[0,0],passes=2) for selected in range(16))
    result.extend(dict(pointer=DATA+0x100,channels=[255]*16,captures=[128 if bits&1 else 127,128 if bits&2 else 127],passes=2) for bits in range(4))
    result.extend(dict(pointer=DATA+0x100,channels=list(random.Random(index+193).randbytes(16)),
        captures=list(random.Random(index+257).randbytes(2)),passes=2) for index in range(64))
    result.extend(dict(pointer=0,channels=list(random.Random(index+311).randbytes(16)),captures=[255,255],passes=2) for index in range(32))
    return result


def setup(address,body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZES[address]:
        raise ValueError('Complete measured host SDK state function differs')
    wram=bytearray(raw+random.Random(seed+67).randbytes(0x18000-len(raw)))
    wram[address-BASE:address-BASE+len(body)]=body
    if address==0x03801D24:
        for index in range(8):
            wram[ALARMS-BASE+index*64]=(case['pattern']*8+index)&255
            wram[ALARMS-BASE+index*64+1]=(case['pattern']*8+index*17)&255
    else:
        wram[SHARED_POINTER-BASE:SHARED_POINTER-BASE+4]=case['pointer'].to_bytes(4,'little')
    regions={BASE:bytes(wram),DATA:random.Random(seed+113).randbytes(0x1000),STACK:random.Random(seed+179).randbytes(0x4000),
        RETURN:bytes(0x1000),MMIO:random.Random(seed+239).randbytes(0x10000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    if address==0x03801C8C:
        for index,value in enumerate(case['channels']):
            cpu.mem_write(0x04000403+index*16,bytes([value]))
        cpu.mem_write(0x04000508,bytes(case['captures']))
    writes,reads,visited,calls=[],[],set(),[]
    state=dict(instructions=0,helperLr=None,nestedReturns=0)
    def code(machine,pc,size,unused):
        state['instructions']+=1
        if machine.reg_read(UC_ARM_REG_CPSR)&32 or not (address<=pc<address+CODES[address]
            or address==0x03801C8C and any(first<=pc<first+length for first,length in HELPERS.items())):
            raise ValueError('SDK state execution escaped exact caller/leaf-helper code')
        if pc==state['helperLr']:
            state['nestedReturns']+=1
            state['helperLr']=None
        if address<=pc<address+CODES[address]:
            visited.add(pc)
        if pc in HELPERS:
            calls.append([pc,machine.reg_read(match_runtime.REGISTERS[0])])
            state['helperLr']=machine.reg_read(match_runtime.REGISTERS[14])
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1 << size*8)-1)])
    def read(machine,access,target,size,value,unused):
        reads.append([target,size])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    return dict(cpu=cpu,address=address,case=case,seed=seed,regions=regions,writes=writes,reads=reads,calls=calls,visited=visited,state=state)


def execute(prepared,budget=10000):
    cpu,address,case,seed=prepared['cpu'],prepared['address'],prepared['case'],prepared['seed']
    records=[]
    for iteration in range(case['passes']):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[13:]=[STACK+0x3000,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,0x1F|((seed&1)*128)|((seed&15)<<28))
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in prepared['regions'].items() if base!=STACK}
        stores,calls=[],[]
        if address==0x03801D24:
            stores=[[ALARMS+index*64+offset,1,0] for index in range(8) for offset in range(2)]
        elif case['pointer']:
            channels=sum((1<<index) for index,value in enumerate(case['channels']) if value&128)
            captures=sum((1<<index) for index,value in enumerate(case['captures']) if value&128)
            stores=[[case['pointer']+8,2,channels],[case['pointer']+10,2,captures]]
            calls=[[0x037FEB50,index] for index in range(16)]+[[0x037FF14C,0],[0x037FF14C,1]]
        for target,size,value in stores:
            base=BASE if BASE<=target<BASE+0x18000 else DATA
            expected[base][target-base:target-base+size]=value.to_bytes(size,'little')
        prepared['writes'].clear()
        prepared['reads'].clear()
        prepared['calls'].clear()
        prepared['state'].update(helperLr=None,nestedReturns=0)
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
        nonstack=[row for row in prepared['writes'] if not STACK<=row[0]<STACK+0x4000]
        if nonstack!=stores or prepared['calls']!=calls or prepared['state']['nestedReturns']!=len(calls):
            raise ValueError('Independent SDK state fields/mask/ordered-store/leaf-ABI model differs')
        if any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):
            raise ValueError('SDK state function changed unrelated mapped memory guards')
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:]:
            raise ValueError('SDK state changed preserved registers/caller SP/LR')
        if bytes(cpu.mem_read(STACK+0x3000,0x1000))!=prepared['regions'][STACK][0x3000:]:
            raise ValueError('SDK state changed caller-visible stack guards')
        records.append(dict(actualReturn=True,fault=None,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),nonstackWrites=nonstack,
            nonstackReads=[row for row in prepared['reads'] if not STACK<=row[0]<STACK+0x4000],leafCalls=list(prepared['calls']),
            actualNestedReturns=prepared['state']['nestedReturns'],instructions=prepared['state']['instructions']-first,
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()},independentCompleteMemoryModel=True))
    return dict(case=case,states=records,visited=sorted(prepared['visited']))
