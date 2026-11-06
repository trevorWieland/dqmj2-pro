import arm7_lane_heap_engine_20261031 as engine
import arm7_lane_heap_lists_model_20261031 as model

SIZES={0x037FCBCC:168,0x037FCC74:272,0x037FCD84:108}
INFO=engine.DATA+0x1000


def cases(address):
    if address==0x037FCBCC:
        layouts=[([],0x4000,64),([(0x4100,64),(0x4200,64)],0x4000,64),
            ([(0x4100,64),(0x4200,64)],0x40C0,64),([(0x4100,64),(0x4200,64)],0x4140,64),
            ([(0x4100,64),(0x4200,64)],0x41C0,64),([(0x4100,64),(0x4200,64)],0x4140,192),
            ([(0x4100,64),(0x4200,64)],0x4300,64)]
        return [dict(nodes=nodes,cell=cell,size=size,passes=2) for nodes,cell,size in layouts]
    if address==0x037FCD84:
        return [dict(id=arena,selector=selector,neighbors=neighbors,passes=2)
            for arena in (0,8) for selector in (-1,0) for neighbors in range(4)]
    rows=[dict(id=arena,selector=selector,layout=layout,request=request,passes=2)
        for arena in (0,8) for selector in (-1,0) for layout in ('plain','fragmented','full')
        for request in (0,1,31,32,33,64,65,128,1408,1900,1919,1920,1952,1953,1984,2016,2048,4096)]
    rows.extend(dict(id=arena,selector=selector,layout='null-info',request=request,passes=2)
        for arena in (0,8) for selector in (-1,0) for request in (0,1,0xFFFFFFFF))
    return rows


def execute(address,body,case,seed,budget=100000):
    machine=engine.setup(address,body,seed)
    cpu,invoke=machine['cpu'],machine['invoke']
    prerequisites=[]
    def original(entry,args):
        row=invoke(entry,args)
        prerequisites.append(row)
        if not row['actualReturn']:
            raise ValueError('Original connected heap prerequisite failed to return: '+str(row))
        return row['registers'][0]
    if address==0x037FCBCC:
        nodes=case['nodes']
        for index,(offset,size) in enumerate(nodes):
            previous=engine.DATA+nodes[index-1][0] if index else 0
            following=engine.DATA+nodes[index+1][0] if index+1<len(nodes) else 0
            cpu.mem_write(engine.DATA+offset,previous.to_bytes(4,'little')+following.to_bytes(4,'little')+size.to_bytes(4,'little'))
        head=engine.DATA+nodes[0][0] if nodes else 0
        cpu.mem_write(engine.DATA+case['cell']+8,case['size'].to_bytes(4,'little'))
        cpu.mem_write(engine.DATA+0x5008,(64).to_bytes(4,'little'))
    elif case.get('layout')=='null-info':
        cpu.mem_write(engine.TABLE+case['id']*4,bytes(4))
    else:
        original(0x037FCE24,[case['id'],INFO,engine.DATA+0x6000,1])
        original(0x037FCECC,[case['id'],engine.DATA+0x3000,engine.DATA+0x3800])
        cpu.mem_write(INFO,bytes(4))
        if address==0x037FCD84:
            allocations=[original(0x037FCC74,[case['id'],0,size]) for size in (32,64,32)]
            if case['neighbors']&1:
                original(0x037FCD84,[case['id'],0,allocations[0]])
            if case['neighbors']&2:
                original(0x037FCD84,[case['id'],0,allocations[2]])
        elif case['layout']=='fragmented':
            allocations=[original(0x037FCC74,[case['id'],0,size]) for size in (96,64,224,96)]
            for index in (0,2):
                original(0x037FCD84,[case['id'],0,allocations[index]])
        elif case['layout']=='full':
            original(0x037FCC74,[case['id'],0,2016])
    states=[]
    for iteration in range(case['passes']):
        if address==0x037FCBCC:
            args=[head,engine.DATA+(case['cell'] if iteration==0 else 0x5000)]
        elif address==0x037FCD84:
            pointer=allocations[1] if iteration==0 else original(0x037FCC74,[case['id'],0,64])
            if not pointer:
                raise ValueError('Fresh valid allocated release record was unavailable')
            args=[case['id'],case['selector'],pointer]
        else:
            args=[case['id'],case['selector'],case['request']]
        expected=engine.snapshot(machine)
        if address==0x037FCBCC:
            stores=[]
            value=model.insert(expected,*args,stores)
        elif address==0x037FCC74:
            value,stores=model.allocate(expected,args)
        else:
            value,stores=model.release(expected,args)
        returned=invoke(address,args,caller=True,budget=budget)
        row=engine.result(machine,returned,expected,value,stores)
        states.append(row)
        if not row['actualReturn']:
            break
        if address==0x037FCBCC:
            head=returned['registers'][0]
        elif row['actualNestedReturns'].get('0x37fdd00')!=1 or row['actualNestedReturns'].get('0x37fdd14')!=1:
            raise ValueError('Allocation/release did not actually complete original IRQ state helpers')
    return dict(case=case,states=states,prerequisites=prerequisites,visited=sorted(machine['visited']),
        limitations=['Allocation/free contexts use actual original heap init/create/allocation/release producers with explicit current-heap0 selection',
            'Direct insert contexts are bounded synthetic doubly-linked lists; a distinct valid node is inserted on reentry',
            'Release reentry obtains a fresh allocation through the original allocator, avoiding an unsupported double free',
            'Nonnull allocations qualify bounded nonnegative rounded sizes; malformed counts, cyclic lists, double frees and overflowed allocation sizes remain unsupported',
            'No enclosing scene/caller reachability, import/ownership restrictions or physical concurrent-IRQ effects are inferred'])
