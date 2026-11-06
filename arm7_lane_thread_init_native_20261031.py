import arm7_lane_thread_init_engine_20261031 as engine

BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
SIZES,CODES=engine.SIZES,engine.CODES
PRIVATE,LAUNCHER=0x038076F0,0x038077C8
digest=engine.digest


def cases(address):
    return [dict(initialized=initialized,callback=callback,counter=counter) for initialized in (0,1,2,0xFFFFFFFF)
        for callback in (0,0x037FDD00,0x80000000,0xFFFFFFFF) for counter in (0,7,0xFFFFFFFF,0x7FFFFFFF)]


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed)
    for target,value in ((PRIVATE+12,case['initialized']),(PRIVATE+0x30,case['callback']),(PRIVATE+0x20,case['counter'])):
        machine['cpu'].mem_write(target,value.to_bytes(4,'little'))
    machine['case']=case
    return machine


def model(memory):
    stores=[]
    read=lambda target:engine.word(memory,target)
    put=lambda target,value:engine.store(memory,target,value,stores)
    if not read(PRIVATE+12):
        put(PRIVATE+12,1)
        put(PRIVATE+8,PRIVATE+0x28)
        for offset,value in ((0x54,16),(0x50,0),(0x48,1),(0x4C,0),(0x58,0),
            (0x78,0x0380FB80),(0x74,0x0380F780),(0x7C,0),(0x80,0),(0x84,0)):
            put(LAUNCHER+offset,value)
        put(PRIVATE+0x2C,LAUNCHER)
        put(PRIVATE+0x28,LAUNCHER)
        put(0x0380FB7C,0xD73BFDF7)
        put(0x0380F780,0xFBDD37BB)
        put(PRIVATE+0x24,0)
        put(0x027FFFA4,PRIVATE+0x24)
        put(PRIVATE+0x30,0)
    return None,None


def execute(machine,budget=100000):
    states=[]
    for iteration in range(2):
        expected=engine.snapshot(machine)
        value,writes=model(expected)
        execution=machine['invoke'](machine['address'],[],True,budget)
        states.append(engine.result(machine,execution,expected,value,writes))
        if not execution['actualReturn']:
            break
    return dict(case=machine['case'],states=states,visited=sorted(machine['visited']),
        observedConditionalPredicates=machine['state']['conditionalPredicates'])
