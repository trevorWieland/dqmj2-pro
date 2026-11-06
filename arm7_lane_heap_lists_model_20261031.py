import arm7_lane_heap_engine_20261031 as engine


def insert(memory,head,cell,stores):
    read=lambda address:engine.word(memory,address)
    put=lambda address,value:engine.store(memory,address,value,stores)
    previous,current=0,head
    steps=0
    while current and cell>current:
        previous,current=current,read(current+4)
        steps+=1
        if steps>16:
            raise ValueError('Heap model refuses unsupported cyclic/excessive free-list backing')
    put(cell+4,current)
    put(cell,previous)
    if current:
        put(current,cell)
        if (cell+read(cell+8))&0xFFFFFFFF==current:
            put(cell+8,read(cell+8)+read(current+8))
            current=read(current+4)
            put(cell+4,current)
            if current:
                put(current,cell)
    if previous:
        put(previous+4,cell)
        if (previous+read(previous+8))&0xFFFFFFFF!=cell:
            return head
        put(previous+8,read(previous+8)+read(cell+8))
        put(previous+4,current)
        if current:
            put(current,previous)
        return head
    return cell


def extract(memory,head,cell,stores):
    read=lambda address:engine.word(memory,address)
    put=lambda address,value:engine.store(memory,address,value,stores)
    previous,current=read(cell),read(cell+4)
    if current:
        put(current,previous)
    if not previous:
        return current
    put(previous+4,current)
    return head


def descriptor(memory,args):
    info=engine.word(memory,engine.TABLE+args[0]*4)
    if not info:
        return None
    selected=engine.signed(args[1]&0xFFFFFFFF)
    if selected<0:
        selected=engine.signed(engine.word(memory,info))
    if not 0<=selected<engine.word(memory,info+4):
        raise ValueError('Heap model refuses unsupported negative/out-of-count descriptor selection')
    return engine.word(memory,info+16)+selected*12


def allocate(memory,args):
    stores=[]
    read=lambda address:engine.word(memory,address)
    put=lambda address,value:engine.store(memory,address,value,stores)
    heap=descriptor(memory,args)
    if heap is None:
        return 0,stores
    size=((args[2]+63)&0xFFFFFFFF)&~31
    if not 32<=size<0x80000000:
        raise ValueError('Heap model withholds unsupported nonpositive/wrapped allocation sizes')
    cell=read(heap+4)
    steps=0
    while cell and engine.signed(read(cell+8))<size:
        cell=read(cell+4)
        steps+=1
        if steps>16:
            raise ValueError('Heap model refuses unsupported cyclic/excessive allocation traversal')
    if not cell:
        return 0,stores
    remaining=engine.signed(read(cell+8))-size
    if remaining<64:
        put(heap+4,extract(memory,read(heap+4),cell,stores))
    else:
        put(cell+8,size)
        new=cell+size
        put(new+8,remaining)
        put(new,read(cell))
        put(new+4,read(cell+4))
        if read(new+4):
            put(read(new+4),new)
        if read(new):
            put(read(new)+4,new)
        else:
            put(heap+4,new)
    allocated=read(heap+8)
    put(cell+4,allocated)
    put(cell,0)
    if allocated:
        put(allocated,cell)
    put(heap+8,cell)
    return cell+32,stores


def release(memory,args):
    stores=[]
    heap=descriptor(memory,args)
    if heap is None:
        raise ValueError('Heap model withholds null-info release contexts')
    cell=args[2]-32
    allocated=extract(memory,engine.word(memory,heap+8),cell,stores)
    engine.store(memory,heap+8,allocated,stores)
    free=insert(memory,engine.word(memory,heap+4),cell,stores)
    engine.store(memory,heap+4,free,stores)
    return None,stores
