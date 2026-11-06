from itertools import product
import arm7_lane_thread_scheduling_engine_20261031 as engine
from arm7_lane_thread_lists_native_20261031 import model as insert_model

BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
SIZES,CODES=engine.SIZES,engine.CODES
PRIVATE,GLOBAL,IDLE,QUEUE=0x038076F0,0x0380771C,0x03807724,DATA+0x100
digest=engine.digest


def cases(address):
    if address==0x037FC398:
        return [dict(states=list(states)) for count in (0,1,3) for states in product((0,1,2,0xFFFFFFFF),repeat=count)]
    if address==0x037FC2E4:
        return [dict(states=[])] + [dict(states=[value]*count) for count in (1,3,5) for value in (0,1,2,0xFFFFFFFF)]
    rows=[]
    for priorities in ([],[1],[0,1,0xFFFFFFFF],[1,1,1]):
        for target in [*range(len(priorities)),'missing']:
            rows.extend(dict(priorities=priorities,target=target,priority=value) for value in (0,1,2,0xFFFFFFFF))
    rows.extend(dict(priorities=[0,1,0xFFFFFFFF],target=index,idle=index,priority=value) for index in (0,2) for value in (0,1,2,0xFFFFFFFF))
    return rows


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed)
    cpu=machine['cpu']
    def put(target,value):
        cpu.mem_write(target,(value&0xFFFFFFFF).to_bytes(4,'little'))
    values=case.get('priorities',case.get('states',[]))
    nodes=[IDLE if case.get('idle')==index else DATA+0x1000+index*0x100 for index in range(len(values))]
    for index,node in enumerate(nodes):
        previous=nodes[index-1] if index else 0
        following=nodes[index+1] if index+1<len(nodes) else 0
        put(node+0x48,case.get('states',[1]*len(nodes))[index])
        put(node+0x4C,following)
        put(node+0x54,case.get('priorities',[1]*len(nodes))[index])
        put(node+0x5C,QUEUE)
        put(node+0x60,previous)
        put(node+0x64,following)
    put(QUEUE,nodes[0] if nodes else 0)
    put(QUEUE+4,nodes[-1] if nodes else 0)
    put(GLOBAL,nodes[0] if nodes else 0)
    put(PRIVATE+4,1)
    machine.update(nodes=nodes,case=case)
    return machine


def model(memory,address,args):
    writes=[]
    read=lambda target:engine.word(memory,target)
    put=lambda target,value:engine.store(memory,target,value,writes)
    if address==0x037FC398:
        node=read(GLOBAL)
        while node and read(node+0x48)!=1:
            node=read(node+0x4C)
        return node,writes
    if address==0x037FC2E4:
        node=read(QUEUE)
        while node:
            following=read(node+0x64)
            put(node+0x48,1)
            put(node+0x5C,0)
            put(node+0x60,0)
            put(node+0x64,0)
            node=following
        put(QUEUE,0)
        put(QUEUE+4,0)
        return None,None
    thread,priority=args
    previous,node=0,read(GLOBAL)
    while node and node!=thread:
        previous,node=node,read(node+0x4C)
    if not node or node==IDLE:
        return 0,writes
    if read(node+0x54)!=priority:
        put(previous+0x4C if previous else GLOBAL,read(node+0x4C))
        put(node+0x54,priority)
        _,nested=insert_model(memory,0x037FBDEC,[thread])
        writes.extend(nested)
    return 1,writes


def execute(machine,budget=100000):
    address,case=machine['address'],machine['case']
    states=[]
    for iteration in range(2):
        args=[] if address==0x037FC398 else [QUEUE] if address==0x037FC2E4 else [
            DATA+0x4000 if case['target']=='missing' else machine['nodes'][case['target']],case['priority']]
        expected=engine.snapshot(machine)
        value,writes=model(expected,address,args)
        execution=machine['invoke'](address,args,True,budget)
        states.append(engine.result(machine,execution,expected,value,writes))
        if not execution['actualReturn']:
            break
    return dict(case=case,states=states,visited=sorted(machine['visited']))
