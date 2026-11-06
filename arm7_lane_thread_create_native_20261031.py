import arm7_lane_thread_create_engine_20261031 as engine
from arm7_lane_thread_lists_native_20261031 import model as insert_model

BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
SIZES,CODES=engine.SIZES,engine.CODES
GLOBAL,COUNTER=0x0380771C,0x03807710
digest=engine.digest


def cases(address):
    rows=[]
    counters=(0,1,7,0xFFFFFFFD,0xFFFFFFFF,0x7FFFFFFD)
    arguments=(0,0x12345678,0x80000000,0xFFFFFFFF)
    for members in ([],[1],[0,1,0xFFFFFFFF],[1,1,1]):
        for priority in (0,1,2,0xFFFFFFFF):
            for size in (8,12,32,256):
                for alignment in (0,4):
                    seed=len(rows)
                    rows.append(dict(members=members,priority=priority,size=size,alignment=alignment,
                        counter=counters[seed%len(counters)],argument=arguments[seed%4],function=(0x037FC15C,0x027E1001)[seed%2]))
    for counter in counters:
        for argument in arguments:
            for function in (0x037FC15C,0x027E1001):
                rows.append(dict(members=[1],priority=2,size=32,alignment=0,counter=counter,argument=argument,function=function))
    return rows


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed)
    cpu=machine['cpu']
    def put(target,value):
        cpu.mem_write(target,(value&0xFFFFFFFF).to_bytes(4,'little'))
    members=[DATA+0x2000+index*0x100 for index in range(len(case['members']))]
    for index,node in enumerate(members):
        put(node+0x54,case['members'][index])
        put(node+0x4C,members[index+1] if index+1<len(members) else 0)
    put(GLOBAL,members[0] if members else 0)
    put(COUNTER,case['counter'])
    machine['case']=case
    return machine


def model(memory,args):
    thread,function,argument,stack,size,priority=args
    writes=[]
    read=lambda target:engine.word(memory,target)
    put=lambda target,value:engine.store(memory,target,value,writes)
    identity=(read(COUNTER)+1)&0xFFFFFFFF
    put(COUNTER,identity)
    put(thread+0x54,priority)
    put(thread+0x50,identity)
    put(thread+0x48,0)
    put(thread+0x58,0)
    insert_model(memory,0x037FBDEC,[thread])
    put(thread+0x78,stack)
    put(thread+0x74,stack-size)
    put(thread+0x7C,0)
    put(stack-4,0xD73BFDF7)
    put(stack-size,0xFBDD37BB)
    put(thread+0x80,0)
    put(thread+0x84,0)
    put(thread,0x3F if function&1 else 0x1F)
    for offset in range(4,0x38,4):
        put(thread+offset,0)
    put(thread+0x38,(stack-4-0x40)&~7)
    put(thread+0x3C,0x037FC15C)
    put(thread+0x40,(function+4)&0xFFFFFFFF)
    put(thread+0x44,stack-4)
    put(thread+4,argument)
    for target in range(stack-size+4,stack-4,4):
        put(target,0)
    for offset in (0x68,0x6C,0x70,0x98,0x5C,0x64,0x60,0x88,0x8C,0x90,0x94):
        put(thread+offset,0)
    return None,None


def execute(machine,budget=100000):
    address,case=machine['address'],machine['case']
    states=[]
    for iteration in range(2):
        args=[DATA+0x1000+iteration*0x100,case['function'],case['argument']^(0xFFFFFFFF if iteration else 0),
            DATA+0x5000+iteration*0x1000+case['alignment'],case['size'],case['priority']^(0xFFFFFFFF if iteration else 0)]
        expected=engine.snapshot(machine)
        value,writes=model(expected,args)
        execution=machine['invoke'](address,args,True,budget)
        states.append(engine.result(machine,execution,expected,value,writes))
        if not execution['actualReturn']:
            break
    return dict(case=case,states=states,visited=sorted(machine['visited']))
