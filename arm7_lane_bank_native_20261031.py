import random
import match_runtime
from arm7_lane_channel_five_native_20261031 import digest
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,ADDRESS,SIZE=0x037F8000,0x03801948,384
DATA,STACK,RETURN=0x023C0000,0x023E0000,0x023FF000
BANK,OUTPUT=DATA+0x100,DATA+0x7000
HELPERS=(0x037FEFE4,0x037FEFE8)


def signed(value):
    return value if value<0x80000000 else value-0x100000000


def cases():
    rows=[dict(kind='type-page',type=value,program=0,count=1,key=(value*13)&255) for value in range(256)]
    for first,last in ((0,2),(127,129),(254,255),(255,0)):
        for key in (-1,0,1,2,126,127,128,129,130,254,255,256,-0x80000000,0x7FFFFFFF):
            rows.append(dict(kind='drums',type=16,program=0,count=1,key=key,minimum=first,maximum=last))
    thresholds=([0,1,2,3,4,5,6,7],[0]*8,[255]*8,[31,63,95,127,159,191,223,255],[255,223,191,159,127,95,63,31])
    for keys in thresholds:
        for key in (-1,0,1,7,8,31,32,63,64,127,128,223,224,255,256,0x7FFFFFFF):
            rows.append(dict(kind='split',type=17,program=0,count=1,key=key,thresholds=keys))
    for kind in range(1,6):
        for program in (0,1,2):
            for key in (-0x80000000,-1,0,255,0x7FFFFFFF):
                rows.append(dict(kind='normal',type=kind,program=program,count=3,key=key))
    rows.extend(dict(kind='negative-program-null-pointers',type=1,program=program,count=0,key=0,null=True)
        for program in (-1,-0x80000000))
    rows.extend(dict(kind='program-bound',type=1,program=program,count=count,key=0)
        for count,program in ((0,0),(0,0x7FFFFFFF),(1,1),(3,3)))
    return [dict(row,passes=2) for row in rows]


def setup(body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZE:
        raise ValueError('Original ARM7 bank-reader module/complete384-byte unit differs')
    wram=bytearray(raw+random.Random(seed+47).randbytes(0x18000-len(raw)))
    wram[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    data=bytearray(random.Random(seed+131).randbytes(0x8000))
    data[BANK-DATA+0x38:BANK-DATA+0x3C]=case['count'].to_bytes(4,'little')
    for program in range(case['count']):
        payload=BANK+0x400+program*0x1000
        data[BANK-DATA+0x3C+program*4:BANK-DATA+0x40+program*4]=(((payload-BANK)<<8)|case['type']).to_bytes(4,'little')
        if case['type']==16:
            data[payload-DATA:payload-DATA+2]=bytes([case.get('minimum',0),case.get('maximum',255)])
        elif case['type']==17:
            data[payload-DATA:payload-DATA+8]=bytes(case.get('thresholds',[31,63,95,127,159,191,223,255]))
    regions={BASE:bytes(wram),DATA:bytes(data),STACK:random.Random(seed+257).randbytes(0x4000),RETURN:bytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,contents in regions.items():
        cpu.mem_map(base,len(contents))
        cpu.mem_write(base,contents)
    reads,writes,visited,calls=[],[],set(),[]
    state=dict(helperLr=None,helperReturns=0,instructions=0)
    def code(machine,pc,size,unused):
        state['instructions']+=1
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not (ADDRESS<=pc<ADDRESS+SIZE or pc in HELPERS):
            raise ValueError('Bank reader escaped own complete ARM body or exact original mutex leaf instructions')
        if pc==state['helperLr']:
            state['helperReturns']+=1
            state['helperLr']=None
        if ADDRESS<=pc<ADDRESS+SIZE:
            visited.add(pc)
        if pc in HELPERS:
            calls.append(pc)
            state['helperLr']=machine.reg_read(match_runtime.REGISTERS[14])
    def read(machine,access,target,size,value,unused):
        reads.append([target,size])
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1<<size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    return dict(cpu=cpu,case=case,seed=seed,regions=regions,reads=reads,writes=writes,visited=visited,calls=calls,state=state)


def expected_model(memory,case):
    stores,read_ranges=[],[]
    program,key=case['program'],case['key']
    if program<0:
        return 0,stores,[],read_ranges
    calls=list(HELPERS)
    read_ranges.append([BANK+0x38,4])
    if program>=case['count']:
        return 0,stores,calls,read_ranges
    read_ranges.append([BANK+0x3C+program*4,4])
    encoded=int.from_bytes(memory[BANK-DATA+0x3C+program*4:BANK-DATA+0x40+program*4],'little')
    kind=encoded&255
    payload=BANK+(encoded>>8)
    stores.append([OUTPUT,1,kind])
    if 1<=kind<=5:
        start,length,destination=payload,10,OUTPUT+2
    elif kind==16:
        minimum,maximum=memory[payload-DATA:payload-DATA+2]
        read_ranges.extend([[payload,1],[payload+1,1]])
        if not minimum<=key<=maximum:
            return 0,stores,calls,read_ranges
        start,length,destination=payload+2+(key-minimum)*12,12,OUTPUT
    elif kind==17:
        index=0
        while index<8:
            read_ranges.append([payload+index,1])
            if key<=memory[payload-DATA+index]:
                break
            index+=1
        if index==8:
            return 0,stores,calls,read_ranges
        start,length,destination=payload+8+index*12,12,OUTPUT
    else:
        return 0,stores,calls,read_ranges
    for offset in range(0,length,2):
        read_ranges.append([start+offset,2])
        stores.append([destination+offset,2,int.from_bytes(memory[start-DATA+offset:start-DATA+offset+2],'little')])
    return 1,stores,calls,read_ranges


def execute(prepared,budget=10000):
    cpu,case,seed=prepared['cpu'],prepared['case'],prepared['seed']
    states=[]
    for iteration in range(case['passes']):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:4]=[0 if case.get('null') else BANK,case['program']&0xFFFFFFFF,case['key']&0xFFFFFFFF,0 if case.get('null') else OUTPUT]
        initial[13:]=[STACK+0x3000,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,0x1F|((seed&1)*128)|((seed&15)<<28))
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in prepared['regions'].items() if base!=STACK}
        value,stores,calls,reads=expected_model(expected[DATA],case)
        for target,size,word in stores:
            expected[DATA][target-DATA:target-DATA+size]=word.to_bytes(size,'little')
        prepared['reads'].clear()
        prepared['writes'].clear()
        prepared['calls'].clear()
        prepared['state'].update(helperLr=None,helperReturns=0)
        first=prepared['state']['instructions']
        fault=None
        try:
            cpu.emu_start(ADDRESS,RETURN,timeout=100000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not returned:
            states.append(dict(actualReturn=False,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateExcluded=True))
            break
        nonstack=[row for row in prepared['writes'] if not STACK<=row[0]<STACK+0x4000]
        actual_reads=[row for row in prepared['reads'] if not STACK<=row[0]<STACK+0x4000]
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if registers[0]!=value or nonstack!=stores or actual_reads!=reads or prepared['calls']!=calls or prepared['state']['helperReturns']!=len(calls):
            raise ValueError('Independent bank selector/type/bounds/copy/read/store/original-mutex-return model differs')
        if any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):
            raise ValueError('Bank reader changed unrelated mapped memory guards')
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or bytes(cpu.mem_read(STACK+0x3000,0x1000))!=prepared['regions'][STACK][0x3000:]:
            raise ValueError('Bank reader changed preserved registers or caller stack/return guards')
        states.append(dict(actualReturn=True,fault=None,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            result=value,nonstackReads=actual_reads,orderedNonstackWrites=nonstack,actualOriginalLeafCalls=list(prepared['calls']),
            actualNestedReturns=prepared['state']['helperReturns'],instructions=prepared['state']['instructions']-first,
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()},
            independentCompleteBankBoundsAndEffectsModel=True))
    return dict(case=case,states=states,visited=sorted(prepared['visited']))
