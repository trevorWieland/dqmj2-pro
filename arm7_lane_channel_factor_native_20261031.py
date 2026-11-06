import random
import match_runtime
from arm7_lane_channel_five_native_20261031 import scaled,digest
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,STACK,RETURN,MMIO=0x037F8000,0x023E0000,0x023FF000,0x04000000
ADDRESS,SIZE,CODE,SCALE,SCALE_CODE=0x037FEBE0,96,84,0x037FEC40,100
FACTOR,VOLUMES=0x03807980,0x03807994


def cases():
    rows=[dict(factor=factor,panPattern=pan,volumePattern=volume,passes=2)
        for factor in (0,1,32767,32768,0x7FFFFFFF,0x80000000,0xFFFFFFFF)
        for pan in range(8) for volume in range(4)]
    rows.extend(dict(factor=1,panPattern=pan,volumePattern=page+4,passes=2)
        for pan in range(6) for page in range(16))
    return rows


def setup(body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZE:
        raise ValueError('Measured complete host factor setter differs')
    wram=bytearray(raw+random.Random(seed+41).randbytes(0x18000-len(raw)))
    wram[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    initial_volume=([0]*16,[127]*16,[255]*16,[(index*17+seed)&255 for index in range(16)])[min(case['volumePattern'],3)]
    if case['volumePattern']>=4:
        initial_volume=[((case['volumePattern']-4)*16+index)&255 for index in range(16)]
    wram[VOLUMES-BASE:VOLUMES-BASE+16]=bytes(initial_volume)
    regions={BASE:bytes(wram),STACK:random.Random(seed+97).randbytes(0x4000),RETURN:bytes(0x1000),MMIO:random.Random(seed+157).randbytes(0x10000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    pans=(0,23,24,104,105,255,127,None)
    for index in range(16):
        pan=pans[case['panPattern']]
        cpu.mem_write(0x04000402+index*16,bytes([(index*17 if pan is None else pan)&255]))
    visited,writes,reads,calls=set(),[],[],[]
    state=dict(instructions=0,scaleLr=None,nestedReturns=0)
    def code(machine,pc,size,unused):
        state['instructions']+=1
        if machine.reg_read(UC_ARM_REG_CPSR)&32 or not (ADDRESS<=pc<ADDRESS+CODE or SCALE<=pc<SCALE+SCALE_CODE):
            raise ValueError('Factor setter escaped exact host ARM caller/helper code')
        if pc==state['scaleLr']:
            state['nestedReturns']+=1
            state['scaleLr']=None
        if ADDRESS<=pc<ADDRESS+CODE:
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
    return dict(cpu=cpu,regions=regions,case=case,seed=seed,state=state,visited=visited,writes=writes,reads=reads,calls=calls)


def execute(prepared,budget=20000):
    cpu,case,seed=prepared['cpu'],prepared['case'],prepared['seed']
    records=[]
    for iteration in range(case['passes']):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[0]=case['factor']
        initial[13:]=[STACK+0x3000,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,0x1F|((seed&1)*128)|((seed&15)<<28))
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        before_wram=bytearray(cpu.mem_read(BASE,0x18000))
        before_mmio=bytearray(cpu.mem_read(MMIO,0x10000))
        prepared['writes'].clear()
        prepared['reads'].clear()
        prepared['calls'].clear()
        prepared['state'].update(scaleLr=None,nestedReturns=0)
        first=prepared['state']['instructions']
        fault=None
        try:
            cpu.emu_start(ADDRESS,RETURN,timeout=100000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not returned:
            records.append(dict(actualReturn=False,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateExcluded=True))
            break
        writes=[[FACTOR,4,case['factor']]]
        expected_calls=[]
        before_wram[FACTOR-BASE:FACTOR-BASE+4]=case['factor'].to_bytes(4,'little')
        for channel in range(16):
            if not 0xFFF5&(1<<channel):
                continue
            pan=before_mmio[0x402+channel*16]
            volume=before_wram[VOLUMES-BASE+channel]
            expected_calls.append([volume,pan])
            result=scaled(volume,pan,case['factor'])&255
            before_mmio[0x400+channel*16]=result
            writes.append([0x04000400+channel*16,1,result])
        nonstack=[row for row in prepared['writes'] if not STACK<=row[0]<STACK+0x4000]
        if nonstack!=writes or prepared['calls']!=expected_calls or prepared['state']['nestedReturns']!=14:
            raise ValueError('Independent shared-factor/mask/full-ABI/ordered-store model differs')
        if bytes(cpu.mem_read(BASE,0x18000))!=before_wram or bytes(cpu.mem_read(MMIO,0x10000))!=before_mmio:
            raise ValueError('Factor setter changed independent full-region/MMIO guards')
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:]:
            raise ValueError('Factor setter changed preserved registers/caller SP/LR')
        if bytes(cpu.mem_read(STACK+0x3000,0x1000))!=prepared['regions'][STACK][0x3000:] or bytes(cpu.mem_read(RETURN,0x1000))!=prepared['regions'][RETURN]:
            raise ValueError('Factor setter changed caller-visible stack/return guards')
        records.append(dict(actualReturn=True,fault=None,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            instructions=prepared['state']['instructions']-first,nonstackWrites=nonstack,
            nonstackReads=[row for row in prepared['reads'] if not STACK<=row[0]<STACK+0x4000],
            scaleArguments=list(prepared['calls']),actualNestedScaleReturns=14,
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()},
            independentCompleteStateAndWordWrapModel=True))
    return dict(case=case,states=records,visited=sorted(prepared['visited']))
