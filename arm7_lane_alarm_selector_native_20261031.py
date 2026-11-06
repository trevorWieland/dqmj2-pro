import random
from collections import Counter
import arm7_lane_skip_native_20261031 as qualified
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC

ROOT=qualified.ROOT
BASE,WRAM,DATA,STACK,RETURN,MMIO=0x027E0000,0x037F8000,0x023C0000,0x023E0000,0x023FF000,0x04000000
ADDRESS,SIZE,CODE=0x027E5BAC,176,160
ALARM,CONTEXT,SLOT=0x0380B4BC,DATA+0x800,0x027F8DD4


def cases():
    return [dict(mode=mode,pending=pending,vcount=vcount,irq=irq,passes=2)
        for mode in (0,1,2,3,65535) for pending in (False,True)
        for vcount in (0,199,200,202,203,204,262,65535) for irq in (0,128)]


def execute(body,case,seed,budget=100000):
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if qualified.digest(main)!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416' or qualified.digest(wram)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c' or len(body)!=SIZE:
        raise ValueError('Measured host selector modules/complete extent differ')
    main=bytearray(main+bytes(0x20000-len(main)))
    main[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    regions={BASE:bytes(main),WRAM:wram+bytes(0x18000-len(wram)),DATA:random.Random(seed+119).randbytes(0x4000),
        STACK:random.Random(seed+219).randbytes(0x4000),RETURN:bytes(0x1000),MMIO:bytes(0x10000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first,data in regions.items():
        cpu.mem_map(first,len(data))
        cpu.mem_write(first,data)
    cpu.mem_write(SLOT,CONTEXT.to_bytes(4,'little'))
    cpu.mem_write(CONTEXT+0xE6,case['mode'].to_bytes(2,'little'))
    cpu.mem_write(MMIO+6,case['vcount'].to_bytes(2,'little'))
    entries,unused=qualified.inventory()
    visited,writes,frames,direct=set(),[],[],[]
    returned=Counter()
    state={'phase':'prerequisite'}
    def code(machine,pc,size,unused):
        if not qualified.executable(pc,size,bool(machine.reg_read(UC_ARM_REG_CPSR)&32)):
            raise ValueError('Selector escaped inventoried original ARM/Thumb code: '+hex(pc))
        while frames and pc==frames[-1][1]:
            returned[frames.pop()[0]]+=1
        if pc in entries:
            link=machine.reg_read(match_runtime.REGISTERS[-1])&~1
            frames.append((pc,link))
            if state['phase']=='caller' and ADDRESS<=link<ADDRESS+CODE and pc in (0x037FDA38,0x037FD898):
                arity=1 if pc==0x037FDA38 else 5
                args=[machine.reg_read(r) for r in match_runtime.REGISTERS[:min(arity,4)]]
                if arity>4:
                    args.append(int.from_bytes(machine.mem_read(machine.reg_read(match_runtime.REGISTERS[-2]),4),'little'))
                direct.append([pc,args])
        if state['phase']=='caller':
            visited.add(pc)
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1 << size*8)-1)])
    def interrupt(machine,number,unused):
        raise ValueError('Selector reached an unsupported architectural service')
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_INTR,interrupt)
    def run(address,args,phase,limit):
        registers=[random.Random(seed*17+phase*73+i).getrandbits(32) for i in range(15)]
        registers[:min(len(args),4)]=args[:4]
        registers[-2:]=[STACK+0x3F00,RETURN]
        cpu.mem_write(registers[-2],b''.join(value.to_bytes(4,'little') for value in args[4:]))
        cpu.reg_write(UC_ARM_REG_CPSR,(seed%16)<<28 | 0x53 | case['irq'])
        for register,value in zip(match_runtime.REGISTERS,registers):
            cpu.reg_write(register,value)
        frames.clear()
        first_write,first_direct=len(writes),len(direct)
        before=Counter(returned)
        fault=None
        try:
            cpu.emu_start(address,RETURN,count=limit,timeout=200000)
        except UcError as error:
            fault=error.errno
        actual_return=cpu.reg_read(UC_ARM_REG_PC)==RETURN
        actual=[cpu.reg_read(r) for r in match_runtime.REGISTERS]
        if actual_return:
            while frames and frames[-1][1]==RETURN:
                returned[frames.pop()[0]]+=1
            if actual[4:12]!=registers[4:12] or actual[-2:]!=registers[-2:] or frames:
                raise ValueError('Selector actual-return or preserved-register ABI differs')
        delta=returned-before
        return dict(actualReturn=actual_return,fault=fault,pc=cpu.reg_read(UC_ARM_REG_PC),registers=actual,
            cpsr=cpu.reg_read(UC_ARM_REG_CPSR),writes=writes[first_write:],directCallerContracts=direct[first_direct:],
            actualFunctionReturns={hex(a):n for a,n in sorted(delta.items())})
    prerequisites=[run(0x037FD74C,[],0,10000),run(0x037FD884,[ALARM],1,10000)]
    if case['pending']:
        prerequisites.append(run(0x037FD898,[ALARM,91,17,0x027E5C5C,0x12345678],2,10000))
    if not all(row['actualReturn'] for row in prerequisites):
        raise ValueError('Real selector subsystem/object/pending prerequisites did not return')
    initial_context=bytes(cpu.mem_read(CONTEXT,0x100))
    state['phase']='caller'
    records=[]
    for phase in range(case['passes']):
        old_handler=int.from_bytes(cpu.mem_read(ALARM,4),'little')
        expected_calls=[]
        if case['mode'] in (1,2):
            if old_handler:
                expected_calls.append([0x037FDA38,[ALARM]])
            expected_calls.append([0x037FD898,[ALARM,203 if case['mode']==1 else 200,263,
                0x027E5F98 if case['mode']==1 else 0x027E5C5C,3 if case['mode']==1 else 1]])
        before_alarm=bytes(cpu.mem_read(ALARM,40))
        row=run(ADDRESS,[],3+phase,budget)
        if row['actualReturn']:
            if row['directCallerContracts']!=expected_calls:
                raise ValueError('Independent selector direct-call order/5-word ABI differs')
            expected_context=bytearray(initial_context)
            if case['mode']==2:
                expected_context[0x1C:0x20]=bytes(4)
                expected_context[0xD8:0xDC]=bytes(4)
            if bytes(cpu.mem_read(CONTEXT,0x100))!=bytes(expected_context):
                raise ValueError('Independent selector context fields/preservation differ')
            if case['mode'] not in (1,2):
                if row['registers'][0]!=ALARM or bytes(cpu.mem_read(ALARM,40))!=before_alarm or any(not STACK<=a<STACK+0x4000 for a,n,v in row['writes']):
                    raise ValueError('Selector unmatched-mode raw return/state differs')
            else:
                expected_result=128 if case['mode']==1 else 0
                alarm=bytes(cpu.mem_read(ALARM,40))
                fields=(int.from_bytes(alarm[:4],'little'),int.from_bytes(alarm[4:8],'little'),int.from_bytes(alarm[16:18],'little'),int.from_bytes(alarm[18:20],'little'))
                expected_fields=(0x027E5F98 if case['mode']==1 else 0x027E5C5C,3 if case['mode']==1 else 1,203 if case['mode']==1 else 200,263)
                if fields!=expected_fields or row['registers'][0]!=expected_result or cpu.reg_read(UC_ARM_REG_CPSR)&128!=case['irq']:
                    raise ValueError('Selector registered fields/raw return/IRQ preservation differ: '+repr((case,fields,row['registers'][0])))
        row['regions']={hex(first):qualified.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in regions.items()}
        records.append(row)
        if not row['actualReturn']:
            break
    return dict(prerequisites=prerequisites,states=records,visited=sorted(visited),providerCalls=0,sourceCredit=0)
