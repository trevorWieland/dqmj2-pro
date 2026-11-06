import random
from collections import Counter
import match_runtime
import arm7_runtime
from arm7_lane_channel_five_native_20261031 import digest
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,MAIN,STACK,RETURN=0x037F8000,0x027E0000,0x022E0000,0x022FF000
TABLE=0x027FFDA0
SIZES={0x037FCA58:60,0x037FCA94:20,0x037FCAA8:20,0x037FCB90:20}
HELPERS={0x037FCABC:104,0x037FCB38:80}


def cases(address):
    if address==0x037FCA58:
        return [dict(id=arena,flags=flags,word=flags,passes=2) for arena in range(9) for flags in range(16)]
    words=[0,1,0x7FFFFFFF,0x80000000,0xFFFFFFFF,0x12345678,0x00FF00FF,0xFF00FF00]
    words.extend(1<<bit for bit in range(32))
    randomizer=random.Random(0xA120)
    words.extend(randomizer.getrandbits(32) for unused in range(8))
    return [dict(id=arena,word=word,flags=index&15,passes=2) for arena in range(9) for index,word in enumerate(words)]


def layout_contract(raw):
    layout=arm7_runtime.derive((ROOT/'extract/arm7/arm7.bin').read_bytes())
    modules={row['id']:row for row in layout['modules']}
    values={address:int.from_bytes(raw[address-BASE:address-BASE+4],'little')
        for address in (*range(0x037FCB24,0x037FCB38,4),0x037FCB88,0x037FCB8C)}
    expected={0x037FCB24:0x027FF000,0x037FCB28:0x400,0x037FCB2C:0x0380FF80,
        0x037FCB30:int(modules['arm7-wram']['bssEnd'],0),0x037FCB34:0x400,
        0x037FCB88:int(modules['arm7-main']['bssEnd'],0),0x037FCB8C:int(modules['arm7-wram']['bssEnd'],0)}
    if values!=expected:
        raise ValueError('Original arena initializer linker constants/current BSS endpoints differ')
    return dict(originalLiteralWords={hex(address):hex(value) for address,value in values.items()},
        runtimeDataArrays=dict(address=hex(TABLE),loWords=9,hiOffset=36,hiWords=9,bytes=72,
            originalInitializedModuleOrBssOwnership=False,originalDataSourceCredit=0),
        moduleBssEnds={name:row['bssEnd'] for name,row in modules.items()})


def setup(address,body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    if digest(raw)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or digest(main)!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416' or len(body)!=SIZES[address]:
        raise ValueError('Arena original runtime modules/complete own unit differ')
    contract=layout_contract(raw)
    image=bytearray(raw+random.Random(seed+53).randbytes(0x18000-len(raw)))
    image[address-BASE:address-BASE+len(body)]=body
    regions={BASE:bytes(image),MAIN:main+random.Random(seed+127).randbytes(0x20000-len(main)),
        STACK:random.Random(seed+239).randbytes(0x4000),RETURN:bytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    for index in range(9):
        cpu.mem_write(TABLE+index*4,((case['word']+index*0x1020305)&0xFFFFFFFF).to_bytes(4,'little'))
        cpu.mem_write(TABLE+36+index*4,((case['word']^0xC39275A1^index)&0xFFFFFFFF).to_bytes(4,'little'))
    reads,writes,visited,frames,calls=[],[],set(),[],[]
    nested=Counter()
    state=dict(instructions=0)
    def code(machine,pc,size,unused):
        state['instructions']+=1
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not (address<=pc<address+SIZES[address]
            or address==0x037FCA58 and any(first<=pc<first+length for first,length in HELPERS.items())):
            raise ValueError('Arena execution escaped own exact ARM extent/original initializer helper instructions')
        while frames and frames[-1][1]==pc:
            nested[frames.pop()[0]]+=1
        if address<=pc<address+SIZES[address]:
            visited.add(pc)
        if pc in HELPERS:
            calls.append([pc,machine.reg_read(match_runtime.REGISTERS[0])])
            frames.append([pc,machine.reg_read(match_runtime.REGISTERS[14])])
    def read(machine,access,target,size,value,unused):
        reads.append([target,size])
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1<<size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    return dict(cpu=cpu,address=address,case=case,seed=seed,regions=regions,reads=reads,writes=writes,visited=visited,
        frames=frames,calls=calls,nested=nested,state=state,contract=contract)


def execute(prepared,budget=10000):
    cpu,address,case,seed=prepared['cpu'],prepared['address'],prepared['case'],prepared['seed']
    states=[]
    for iteration in range(case['passes']):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[0]=case['id']
        initial[1]=(case['word']^(0xFFFFFFFF if iteration else 0))&0xFFFFFFFF
        initial[13:]=[STACK+0x3000,RETURN]
        cpsr=0x1F|((seed&1)*128)|((seed&2)*32)|(case['flags']<<28)
        cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in prepared['regions'].items() if base!=STACK}
        stores,calls,result=[],[],None
        target=TABLE+case['id']*4
        if address==0x037FCA58:
            ends=prepared['contract']['moduleBssEnds']
            high={1:0x027FF000,7:0x03800000,8:0x0380FF80-0x400-0x400}.get(case['id'],0)
            low={1:int(ends['arm7-main'],0),7:min(int(ends['arm7-wram'],0),0x03800000),
                8:max(int(ends['arm7-wram'],0),0x03800000)}.get(case['id'],0)
            stores=[[target+36,4,high],[target,4,low]]
            calls=[[0x037FCABC,case['id']],[0x037FCB38,case['id']]]
        elif address==0x037FCB90:
            stores=[[target,4,initial[1]]]
        else:
            result=int.from_bytes(cpu.mem_read(target+(36 if address==0x037FCA94 else 0),4),'little')
        for target,size,value in stores:
            expected[MAIN][target-MAIN:target-MAIN+size]=value.to_bytes(size,'little')
        prepared['reads'].clear()
        prepared['writes'].clear()
        prepared['calls'].clear()
        prepared['frames'].clear()
        prepared['nested'].clear()
        before=prepared['state']['instructions']
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
        if nonstack!=stores or prepared['calls']!=calls or prepared['frames'] or sum(prepared['nested'].values())!=len(calls):
            raise ValueError('Independent arena exact store/call-order/original helper-return model differs')
        if result is not None and registers[0]!=result:
            raise ValueError('Independent arena full-word getter result differs')
        if any(bytes(cpu.mem_read(base,len(data)))!=data for base,data in expected.items()):
            raise ValueError('Independent complete arena memory preservation model differs')
        final_cpsr=cpu.reg_read(UC_ARM_REG_CPSR)
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or final_cpsr&255!=cpsr&255:
            raise ValueError('Arena preserved registers,SP,LR or processor-control flags differ')
        if address!=0x037FCA58 and final_cpsr!=cpsr:
            raise ValueError('Arena leaf unexpectedly changed arithmetic flags')
        if bytes(cpu.mem_read(STACK+0x3000,0x1000))!=prepared['regions'][STACK][0x3000:]:
            raise ValueError('Arena caller-visible stack guards changed')
        states.append(dict(actualReturn=True,fault=None,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            orderedNonstackWrites=nonstack,nonstackReads=[row for row in prepared['reads'] if not STACK<=row[0]<STACK+0x4000],
            actualOriginalHelperCalls=list(prepared['calls']),actualNestedReturns={hex(pc):count for pc,count in sorted(prepared['nested'].items())},
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()},
            instructions=prepared['state']['instructions']-before,independentCompleteArenaMemoryAndValueModel=True))
    return dict(case=case,states=states,visited=sorted(prepared['visited']),layoutContract=prepared['contract'])
