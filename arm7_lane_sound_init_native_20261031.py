import arm7_lane_thread_init_engine_20261031 as engine
from arm7_lane_thread_create_native_20261031 import model as create_model
from unicorn import UC_HOOK_CODE

BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
ADDRESS,SIZE,CODE=0x037FEEF8,108,92
FLAG,THREAD,TOP=0x038079A4,0x03807A14,0x03807EB8
digest=engine.digest


def cases(address):
    if address!=ADDRESS:
        raise ValueError('Unqualified sound-init entry')
    return [dict(flag=flag,priority=priority,flagsSeed=seed,passes=2)
        for flag in (0,1,2,0x80000000,0xFFFFFFFF)
        for priority in (0,1,15,16,17,31,32,0x7FFFFFFF,0x80000000,0xFFFFFFFF)
        for seed in range(4)]


def setup(address,body,case,seed):
    if address!=ADDRESS or len(body)!=SIZE:
        raise ValueError('Complete sound initialization extent differs')
    raw=(engine.ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    machine=engine.setup(0x037FBF64,raw[0x3F64:0x4054],seed)
    cpu=machine['cpu']
    cpu.mem_write(ADDRESS,body)
    cpu.mem_write(0x03807678,bytes(0x0380B4E4-0x03807678))
    prerequisites=[]
    for entry in (0x037FBF64,0x037FC558):
        call=machine['invoke'](entry)
        if not call['actualReturn']:
            raise ValueError('Original thread initialization/disable-scheduler prerequisite failed')
        prerequisites.append(dict(entry=hex(entry),actualReturn=True))
    cpu.mem_write(FLAG,case['flag'].to_bytes(4,'little'))
    visited,calls=set(),[]
    def code(uc,pc,size,unused):
        if pc==0x037FF008 or pc in (0x037FC64C,0x037FC680):
            raise ValueError('Sound initializer executed its sound thread or switched CPU context despite disabled scheduler')
        if ADDRESS<=pc<ADDRESS+CODE:
            visited.add(pc)
        if pc==0x037FC054:
            args=[uc.reg_read(register) for register in engine.match_runtime.REGISTERS[:4]]
            sp=uc.reg_read(engine.match_runtime.REGISTERS[13])
            args.extend(int.from_bytes(uc.mem_read(sp+4*i,4),'little') for i in range(2))
            calls.append(args)
    cpu.hook_add(UC_HOOK_CODE,code)
    machine.update(case=case,ownVisited=visited,createCalls=calls,prerequisites=prerequisites)
    return machine


def model(memory,priority):
    writes=[]
    read=lambda target:engine.word(memory,target)
    put=lambda target,value:engine.store(memory,target,value,writes)
    if read(FLAG):
        return []
    put(FLAG,1)
    for offset,value in ((0,0),(4,0),(8,0),(12,0),(16,0x03809080),(20,8),(24,0),(28,0)):
        put(0x03809060+offset,value)
    put(0x038078D0+7*4,0x038025CC)
    put(0x027FFF8C,read(0x027FFF8C)|(1<<7))
    put(0x03807EDC,0)
    args=[THREAD,0x037FF008,0,TOP,1024,priority]
    create_model(memory,args)
    put(THREAD+0x48,1)
    return [args]


def execute(machine,budget=20000):
    states=[]
    for iteration in range(machine['case']['passes']):
        expected=engine.snapshot(machine)
        create_calls=model(expected,machine['case']['priority'])
        machine['createCalls'].clear()
        execution=machine['invoke'](ADDRESS,[machine['case']['priority']],True,budget)
        if not execution['actualReturn']:
            states.append(dict(execution=execution,actualReturn=False,postBoundaryStateExcluded=True))
            break
        checked=engine.result(machine,execution,expected,None,None)
        if machine['createCalls']!=create_calls:
            raise ValueError('Actual thread creation six physical words differ from independent initializer model')
        states.append(dict(checked,createThreadArguments=machine['createCalls'][:],
            actualNativeHelperReturns={hex(key):value for key,value in sorted(machine['helperReturns'].items())}))
    return dict(case=machine['case'],states=states,visited=sorted(machine['ownVisited']),originalPrerequisites=machine['prerequisites'])
