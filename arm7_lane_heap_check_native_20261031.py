import arm7_lane_heap_check_engine_v2_20261031 as engine

ADDRESS,SIZE=0x037FCF6C,416
INFO=engine.DATA+0x1000


def cases():
    layouts=('plain','mixed','fragmented','full','zero-request','empty-descriptor','global-arena-other-span','global-arena-lower-bound')
    faults=('array-null','selector-negative','selector-high','count-zero','descriptor-negative','allocated-head-prev',
        'allocated-low','allocated-high','allocated-unaligned','allocated-next-prev','allocated-short','allocated-size-align',
        'allocated-total-excess','free-head-prev','free-low','free-high','free-unaligned','free-next-prev','free-short',
        'free-size-align','free-adjacent','free-overlap','free-total-excess','total-deficit')
    return [dict(id=arena,selector=selector,kind=kind,passes=2) for arena in (0,8) for selector in (-1,0) for kind in layouts+faults]


def model(memory,args):
    read=lambda address:engine.word(memory,address)
    info=read(engine.TABLE+args[0]*4)
    heap=engine.signed(args[1]&0xFFFFFFFF)
    if heap==-1:
        heap=engine.signed(read(info))
    array=read(info+16)
    if not array or not 0<=heap<engine.signed(read(info+4)):
        return 0xFFFFFFFF
    descriptor=array+heap*12
    size=engine.signed(read(descriptor))
    if size<0:
        return 0xFFFFFFFF
    lower,upper=read(info+8),read(info+12)
    total,available=0,0
    for allocated in (True,False):
        cell=read(descriptor+(8 if allocated else 4))
        if cell and read(cell):
            return 0xFFFFFFFF
        count=0
        while cell:
            if not lower<=cell<upper or cell&31:
                return 0xFFFFFFFF
            following=read(cell+4)
            if following and read(following)!=cell:
                return 0xFFFFFFFF
            amount=engine.signed(read(cell+8))
            if amount<64 or amount&31:
                return 0xFFFFFFFF
            if not allocated and following and cell+amount>=following:
                return 0xFFFFFFFF
            total+=amount
            if total>0x7FFFFFFF:
                raise ValueError('Heap-check source/model withholds unsupported signed accumulation overflow')
            if not 0<total<=size:
                return 0xFFFFFFFF
            if not allocated:
                available+=amount-32
            cell=following
            count+=1
            if count>16:
                raise ValueError('Heap-check model withholds unsupported excessive/cyclic lists')
    return available if total==size else 0xFFFFFFFF


def execute(body,case,seed,budget=100000):
    machine=engine.setup(ADDRESS,body,seed)
    cpu,invoke=machine['cpu'],machine['invoke']
    prerequisites=[]
    patches=[]
    def word(address):
        return int.from_bytes(cpu.mem_read(address,4),'little')
    def put(address,value):
        cpu.mem_write(address,(value&0xFFFFFFFF).to_bytes(4,'little'))
        patches.append([address,4,value&0xFFFFFFFF])
    def original(entry,args):
        result=invoke(entry,args)
        prerequisites.append(result)
        if not result['actualReturn']:
            raise ValueError('Original heap-check context producer did not actually return')
        return result['registers'][0]
    original(0x037FCE24,[case['id'],INFO,engine.DATA+0x6000,1])
    original(0x037FCECC,[case['id'],engine.DATA+0x3000,engine.DATA+0x3800])
    original(0x037FCDF0,[case['id'],0])
    kind=case['kind']
    allocations=[]
    if kind=='full':
        allocations.append(original(0x037FCC74,[case['id'],0,2016]))
    elif kind=='zero-request':
        allocations.append(original(0x037FCC74,[case['id'],0,0]))
    elif kind in ('mixed','fragmented'):
        allocations=[original(0x037FCC74,[case['id'],0,size]) for size in (32,64,32)]
        if kind=='fragmented':
            for index in (0,2):
                original(0x037FCD84,[case['id'],0,allocations[index]])
    elif kind not in ('plain','empty-descriptor'):
        allocations=[original(0x037FCC74,[case['id'],0,size]) for size in (32,64)]
    descriptor=word(INFO+16)
    allocated,free=word(descriptor+8),word(descriptor+4)
    args=[case['id'],case['selector']]
    if kind in ('global-arena-other-span','global-arena-lower-bound'):
        replacement=engine.DATA+0x2000 if kind=='global-arena-other-span' else word(INFO+8)
        put(descriptor,2048)
        put(descriptor+4,replacement)
        put(descriptor+8,0)
        put(replacement,0)
        put(replacement+4,0)
        put(replacement+8,2048)
    elif kind=='empty-descriptor':
        for offset in (0,4,8):
            put(descriptor+offset,0)
    elif kind=='array-null':
        put(INFO+16,0)
    elif kind=='selector-negative':
        args[1]=-2
    elif kind=='selector-high':
        args[1]=1
    elif kind=='count-zero':
        put(INFO+4,0)
    elif kind=='descriptor-negative':
        put(descriptor,-1)
    elif kind in ('allocated-head-prev','free-head-prev'):
        put(allocated if kind.startswith('allocated') else free,0x12345678)
    elif kind in ('allocated-low','allocated-high','free-low','free-high','allocated-unaligned','free-unaligned'):
        is_allocated=kind.startswith('allocated')
        pointer=(word(INFO+8)-32 if kind.endswith('low') else word(INFO+12) if kind.endswith('high')
            else (allocated if is_allocated else free)+4)
        put(descriptor+(8 if is_allocated else 4),pointer)
        put(pointer,0)
    elif kind=='allocated-next-prev':
        put(word(allocated+4),0x12345678)
    elif kind=='free-next-prev':
        put(free+4,free+0x100)
        put(free+0x100,0x12345678)
    elif kind in ('allocated-short','free-short','allocated-size-align','free-size-align'):
        pointer=allocated if kind.startswith('allocated') else free
        put(pointer+8,32 if kind.endswith('short') else 65)
    elif kind=='allocated-total-excess':
        put(descriptor,64)
    elif kind in ('free-adjacent','free-overlap'):
        following=free+(64 if kind.endswith('adjacent') else 32)
        put(free+8,64)
        put(free+4,following)
        put(following,free)
        put(following+4,0)
        put(following+8,64)
    elif kind=='free-total-excess':
        put(descriptor,160)
    elif kind=='total-deficit':
        put(descriptor,2080)
    states=[]
    for iteration in range(case['passes']):
        expected=engine.snapshot(machine)
        value=model(expected,args)
        returned=invoke(ADDRESS,args,caller=True,budget=budget)
        row=engine.result(machine,returned,expected,value,[])
        states.append(row)
        if not row['actualReturn']:
            break
        if row['actualNestedReturns']!={'0x37fdd00':1,'0x37fdd14':1}:
            raise ValueError('Heap check did not actually complete original IRQ helper returns')
    return dict(case=case,states=states,prerequisites=prerequisites,explicitSyntheticFieldStores=patches,
        visited=sorted(machine['visited']),limitations=['Original init/create/set-current/allocate/release producers actually return; selected malformed fields are then explicit controlled mutations',
            'Range checks use OSHeapInfo global arena, not a per-heap origin; a distinct explicit within-global-arena span remains accepted by the native checker',
            'All backing remains mapped and word-aligned; alignment rejection uses word-aligned cells that violate the stronger32-byte heap rule',
            'Signed sum overflow/excessive cycles and unmapped pointer faults remain unsupported; no return or meaning follows from post-fault state',
            'Positive-cell nonoverflow domains cannot take the total<=0 failure; this excluded predicate outcome is not forced by PC/register injection',
            'Native API behavior does not establish enclosing scene reachability, allocation legality, import policy or physical concurrency'])
