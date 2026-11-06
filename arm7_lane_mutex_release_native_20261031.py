import arm7_lane_mutex_release_engine_20261031 as engine

BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
SIZES,CODES=engine.SIZES,engine.CODES
CURRENT,OTHER,PRIVATE=DATA+0x1000,DATA+0x7000,0x038076F0
digest=engine.digest


def cases(address):
    rows=[]
    for count in ((1,3) if address==0x037FC90C else (0,1,3)):
        for target in (range(count) if address==0x037FC90C else (0,)):
            for owner in ('current','other','none'):
                for depth in (0,1,2,0xFFFFFFFF):
                    for waiters in (0,1,3):
                        rows.append(dict(count=count,target=target,owner=owner,depth=depth,waiters=waiters))
    return rows


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed)
    cpu=machine['cpu']
    def put(target,value):
        cpu.mem_write(target,(value&0xFFFFFFFF).to_bytes(4,'little'))
    put(0x03807718,CURRENT)
    put(PRIVATE+4,1)
    put(CURRENT+0x6C,0)
    put(CURRENT+0x70,0)
    mutexes=[DATA+0x2000+index*0x100 for index in range(case['count'])]
    prerequisites=[]
    for mutex in mutexes:
        for entry in (0x037FC870,0x037FC888):
            execution=machine['invoke'](entry,[mutex])
            if not execution['actualReturn']:
                raise ValueError('Original mutex initialization/uncontended lock prerequisite failed')
            prerequisites.append(dict(entry=hex(entry),actualReturn=True,arguments=[mutex]))
    for index,mutex in enumerate(mutexes):
        if address==0x037FC96C or index==case['target']:
            put(mutex+8,dict(current=CURRENT,other=OTHER,none=0)[case['owner']])
            put(mutex+12,case['depth'])
        waiting=[DATA+0x4000+index*0x500+offset*0x100 for offset in range(case['waiters'])]
        put(mutex,waiting[0] if waiting else 0)
        put(mutex+4,waiting[-1] if waiting else 0)
        for offset,thread in enumerate(waiting):
            put(thread+0x48,0)
            put(thread+0x54,offset)
            put(thread+0x5C,mutex)
            put(thread+0x60,waiting[offset-1] if offset else 0)
            put(thread+0x64,waiting[offset+1] if offset+1<len(waiting) else 0)
            put(thread+0x68,mutex)
    machine.update(case=case,mutexes=mutexes,prerequisites=prerequisites)
    return machine


def model(memory,address,args):
    stores=[]
    read=lambda target:engine.word(memory,target)
    put=lambda target,value:engine.store(memory,target,value,stores)
    def wake(queue):
        thread=read(queue)
        while thread:
            following=read(thread+0x64)
            put(thread+0x48,1)
            put(thread+0x5C,0)
            put(thread+0x60,0)
            put(thread+0x64,0)
            thread=following
        put(queue,0)
        put(queue+4,0)
    if address==0x037FC90C:
        mutex=args[0]
        if read(mutex+8)==read(0x03807718):
            depth=(read(mutex+12)-1)&0xFFFFFFFF
            put(mutex+12,depth)
            if not depth:
                following,previous=read(mutex+0x10),read(mutex+0x14)
                put(following+0x14 if following else CURRENT+0x70,previous)
                put(previous+0x10 if previous else CURRENT+0x6C,following)
                put(mutex+8,0)
                wake(mutex)
    else:
        thread=args[0]
        mutex=read(thread+0x6C)
        while mutex:
            following=read(mutex+0x10)
            put(thread+0x6C,following)
            put(following+0x14 if following else thread+0x70,0)
            put(mutex+12,0)
            put(mutex+8,0)
            wake(mutex)
            mutex=following
    return None,None


def execute(machine,budget=100000):
    address,case=machine['address'],machine['case']
    args=[machine['mutexes'][case['target']]] if address==0x037FC90C else [CURRENT]
    states=[]
    for iteration in range(2):
        expected=engine.snapshot(machine)
        value,writes=model(expected,address,args)
        execution=machine['invoke'](address,args,True,budget)
        states.append(engine.result(machine,execution,expected,value,writes))
        if not execution['actualReturn']:
            break
    return dict(case=case,states=states,visited=sorted(machine['visited']),originalPrerequisiteReturns=machine['prerequisites'])
