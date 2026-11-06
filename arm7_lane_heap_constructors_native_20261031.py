import arm7_lane_heap_engine_20261031 as engine

SIZES={0x037FCDF0:52,0x037FCE24:168,0x037FCECC:160}
INFO=engine.DATA+0x1000


def cases(address):
    if address==0x037FCDF0:
        return [dict(id=arena,old=old,new=new,passes=2) for arena in range(9)
            for old in (0,1,0x80000000,0xFFFFFFFF) for new in (0,1,0x12345678,0xFFFFFFFF)]
    if address==0x037FCE24:
        return [dict(id=arena,count=count,startOffset=start,endOffset=end,passes=2)
            for arena in (0,8) for count in (0,1,3) for start in (0,4,16,28) for end in (0,1,31,32)]
    return [dict(id=arena,count=count,free=free,startOffset=start,length=length,passes=2)
        for arena in (0,8) for count in (0,1,3) for free in ([None] if count==0 else ([None,0] if count==1 else [None,0,2]))
        for start in (0,1,31) for length in (-32,0,64,256)]


def model(memory,address,args):
    stores=[]
    put=lambda target,value:engine.store(memory,target,value,stores)
    read=lambda target:engine.word(memory,target)
    arena=args[0]
    if address==0x037FCE24:
        info,end,count=args[1:]
        array=info+20
        put(engine.TABLE+arena*4,info)
        put(info+16,array)
        put(info+4,count)
        for index in range(count):
            put(array+index*12,0xFFFFFFFF)
            put(array+index*12+4,0)
            put(array+index*12+8,0)
        put(info,0xFFFFFFFF)
        start=(array+count*12+31)&~31
        put(info+8,start)
        put(info+12,end&~31)
        return start,stores
    info=read(engine.TABLE+arena*4)
    if address==0x037FCDF0:
        previous=read(info)
        put(info,args[1])
        return previous,stores
    start,end=(args[1]+31)&~31,args[2]&~31
    count=engine.signed(read(info+4))
    array=read(info+16)
    for index in range(max(count,0)):
        descriptor=array+index*12
        if engine.signed(read(descriptor))<0:
            size=(end-start)&0xFFFFFFFF
            put(descriptor,size)
            put(start,0)
            put(start+4,0)
            put(start+8,size)
            put(descriptor+4,start)
            put(descriptor+8,0)
            return index,stores
    return 0xFFFFFFFF,stores


def execute(address,body,case,seed,budget=100000):
    machine=engine.setup(address,body,seed)
    cpu,invoke=machine['cpu'],machine['invoke']
    prerequisites=[]
    if address==0x037FCE24:
        args=[case['id'],INFO+case['startOffset'],engine.DATA+0x6000+case['endOffset'],case['count']]
    else:
        count=1 if address==0x037FCDF0 else case['count']
        prerequisites.append(invoke(0x037FCE24,[case['id'],INFO,engine.DATA+0x6000,count]))
        if not prerequisites[-1]['actualReturn']:
            return dict(case=case,states=[],prerequisites=prerequisites,unsupportedPrerequisite=True)
        if address==0x037FCDF0:
            cpu.mem_write(INFO,case['old'].to_bytes(4,'little'))
            args=[case['id'],case['new']]
        else:
            for index in range(count):
                cpu.mem_write(INFO+20+index*12,(0xFFFFFFFF if index==case['free'] else 0).to_bytes(4,'little'))
            args=[case['id'],engine.DATA+0x4000+case['startOffset'],engine.DATA+0x4000+case['length']]
    states=[]
    for iteration in range(case['passes']):
        expected=engine.snapshot(machine)
        value,stores=model(expected,address,args)
        returned=invoke(address,args,caller=True,budget=budget)
        row=engine.result(machine,returned,expected,value,stores)
        if returned['actualReturn'] and row['actualNestedReturns']!={'0x37fdd00':1,'0x37fdd14':1}:
            raise ValueError('Heap constructor did not complete both actual original IRQ state helper returns')
        states.append(row)
        if not row['actualReturn']:
            break
    return dict(case=case,states=states,prerequisites=prerequisites,visited=sorted(machine['visited']),
        limitations=['Original init/IRQ helpers execute without providers; other descriptor statuses are explicit synthetic zero/negative fields',
            'SetCurrentHeap stores full words without an inferred range/legality policy; zero/negative CreateHeap sizes are measured context edges only',
            'OS heap-info backing is word-aligned; unaligned metadata access and physical bus behavior are unsupported',
            'The initialization caller is not proof of scene or ordinary producer reachability; arena ids and table/backing are explicitly bounded'])
