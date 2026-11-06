import arm7_lane_card_frontier_engine_20261031 as engine
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
ADDRESS,SIZE,CODE=0x03802ffc,116,112
COMMON,ARGUMENT,CONTEXT,SOURCE,DESTINATION,IO=0x038090c0,DATA,DATA+0x100,DATA+0x200,DATA+0x400,0x040001a0
THREAD=COMMON+0x48
MASK=0xffffffff


def cases(address):
    if address!=ADDRESS:raise ValueError('Unqualified task completion entry')
    return [dict(flags=flags,callback=callback,result=result,count=count,source=source)
        for flags in (0,4,8,0x10,0x40,0x4c,0x5c,0xffffffff)
        for callback in (0,0x038028e4,0x03802924,0x03802974)
        for result in (0,0xffffffff) for count,source in ((0,0),(0xffffffff,0xff))]


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed);cpu=machine['cpu']
    cpu.mem_write(0x03807678,bytes(0x0380b4e4-0x03807678))
    prerequisites=[]
    for entry in (0x037fbf64,0x037fc558,0x03802624):
        call=machine['invoke'](entry)
        if not call['actualReturn']:raise ValueError('Original kernel/disable-scheduler/CARD initialization did not return')
        prerequisites.append(dict(entry=hex(entry),actualReturn=True))
    def put(target,value):cpu.mem_write(target,(value&MASK).to_bytes(4,'little'))
    cpu.mem_write(ARGUMENT,bytes(0x100));put(COMMON,ARGUMENT);put(ARGUMENT,case['result'])
    put(COMMON+0x3c,case['callback']);put(COMMON+0x40,CONTEXT);put(COMMON+0xfc,case['flags'])
    for offset,value in ((0,case['count']),(4,SOURCE),(8,DESTINATION),(12,1)):put(CONTEXT+offset,value)
    cpu.mem_write(SOURCE,bytes((case['source'],)));cpu.mem_write(IO,bytes(4))
    ownwrites,callbacklinks,wakecalls,visited=[],[],[],[];state=dict(pc=None)
    def code(uc,pc,size,unused):
        state['pc']=pc
        if ADDRESS<=pc<ADDRESS+CODE:visited.append(pc)
        if case['callback'] and pc==case['callback']:
            callbacklinks.append([uc.reg_read(engine.match_runtime.REGISTERS[0]),uc.reg_read(engine.match_runtime.REGISTERS[14])])
        if pc in (0x037fc2e4,0x037fc36c):wakecalls.append([pc,uc.reg_read(engine.match_runtime.REGISTERS[0])])
    def write(uc,access,target,size,value,unused):
        if ADDRESS<=state['pc']<ADDRESS+CODE and not STACK<=target<STACK+0x4000:
            ownwrites.append([target,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.update(case=case,prerequisites=prerequisites,ownWrites=ownwrites,callbackLinks=callbacklinks,wakeCalls=wakecalls,ownVisited=visited)
    return machine


def execute(address,body,case,seed,budget=30000):
    machine=setup(address,body,case,seed);expected=engine.snapshot(machine);writes=[]
    engine.store(expected,ARGUMENT,0,writes)
    engine.store(expected,COMMON+0xfc,case['flags']&~0x4c,writes)
    own=writes[:]
    if case['callback']==0x038028e4:
        expected[DATA][DESTINATION-DATA]=0
        engine.store(expected,CONTEXT+8,DESTINATION+1,writes)
    elif case['callback']==0x03802924:
        engine.store(expected,CONTEXT+4,SOURCE+1,writes)
        expected[0x04000000][IO+2-0x04000000]=case['source']
    elif case['callback']==0x03802974:
        engine.store(expected,CONTEXT+4,SOURCE+1,writes)
        if case['source']:
            engine.store(expected,CONTEXT+12,0,writes)
            if case['count']>1:engine.store(expected,CONTEXT,1,writes)
    execution=machine['invoke'](address,[],True,budget)
    if not execution['actualReturn']:return dict(execution=execution,actualReturn=False,postFaultStateExcluded=True)
    cpu=machine['cpu']
    if any(bytes(cpu.mem_read(first,len(data)))!=data for first,data in expected.items()):
        raise ValueError('Independent task completion complete nonstack memory model differs')
    if machine['ownWrites']!=own:raise ValueError('Task completion own ordered writes differ')
    wakecalls=[[0x037fc2e4,COMMON+0xf4]]
    if case['flags']&0x10:wakecalls.append([0x037fc36c,THREAD])
    if machine['wakeCalls']!=wakecalls:raise ValueError('Actual wake targets/order differ')
    links=[[CONTEXT,0x03803064]] if case['callback'] else []
    if machine['callbackLinks']!=links:raise ValueError('Actual callback argument/return link differs')
    if case['callback'] and machine['helperReturns'][case['callback']]!=1:raise ValueError('Original callback did not actually return')
    return dict(execution=execution,actualReturn=True,ownOrderedWrites=own,actualCallbackLinks=links,actualWakeCalls=wakecalls,
        ownVisited=sorted(set(machine['ownVisited'])),originalPrerequisites=machine['prerequisites'],
        actualNestedReturns={hex(entry):count for entry,count in sorted(machine['helperReturns'].items())},
        orderedNonstackWrites=[row for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000],
        nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()},
        independentCompleteMemoryEffectsModel=True,hardwareExecutionCredit=0,
        schedulerDisabled=True,threadReadyFromActualOriginalInitialization=True)
