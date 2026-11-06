import arm7_lane_thread_init_engine_20261031 as engine
from arm7_lane_thread_create_native_20261031 import model as create_model
from unicorn import UC_HOOK_CODE

BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
ADDRESS,SIZE,CODE=0x03802624,188,164
FLAG,THREAD,TOP=0x038090A0,0x03809108,0x038096C0
COMMON=0x038090C0
digest=engine.digest


def cases(address):
    if address!=ADDRESS:
        raise ValueError('Unqualified card-init entry')
    return [dict(flag=flag,console=console,passes=1)
        for flag in (0,1,2,0x80000000,0xffffffff) for console in (0,1,2,3,0xffff)]



def setup(address,body,case,seed):
    if address!=ADDRESS or len(body)!=SIZE:
        raise ValueError('Complete card initialization extent differs')
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
    import random
    cpu.mem_write(COMMON,random.Random(seed+83).randbytes(0x100))
    cpu.mem_write(FLAG,case['flag'].to_bytes(4,'little'))
    cpu.mem_write(0x027ffc40,case['console'].to_bytes(2,'little'))
    visited,calls=set(),[]
    def code(uc,pc,size,unused):
        if pc==0x038032B8 or pc in (0x037FC64C,0x037FC680):
            raise ValueError('Card initializer executed its task thread or switched CPU context despite disabled scheduler')
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


def model(memory,case):
    writes=[]
    read=lambda target:engine.word(memory,target)
    put=lambda target,value:engine.store(memory,target,value,writes)
    for offset,value in ((0xc,0xfffffffd),(0xf0,4),(0x10,0),(0x1c,0),(0,0),(8,0),(0x18,0),(0x14,0),(0xf8,0),(0xf4,0)):
        put(COMMON+offset,value)
    args=[THREAD,0x038032b8,0,TOP,1024,4]
    create_model(memory,args)
    put(THREAD+0x48,1)
    put(0x038078d0+11*4,0x038031d4)
    put(0x027fff8c,read(0x027fff8c)|(1<<11))
    if case['console']!=2:put(FLAG,1)
    return [args]



def execute(machine,budget=20000):
    states=[]
    for iteration in range(machine['case']['passes']):
        expected=engine.snapshot(machine)
        create_calls=model(expected,machine['case'])
        machine['createCalls'].clear()
        execution=machine['invoke'](ADDRESS,[],True,budget)
        if not execution['actualReturn']:
            states.append(dict(execution=execution,actualReturn=False,postBoundaryStateExcluded=True))
            break
        checked=engine.result(machine,execution,expected,None,None)
        if machine['createCalls']!=create_calls:
            raise ValueError('Actual thread creation six physical words differ from independent initializer model')
        states.append(dict(checked,createThreadArguments=machine['createCalls'][:],
            actualNativeHelperReturns={hex(key):value for key,value in sorted(machine['helperReturns'].items())}))
    return dict(case=machine['case'],states=states,visited=sorted(machine['ownVisited']),originalPrerequisites=machine['prerequisites'])
