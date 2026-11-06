import itertools
from wave20261105_socket_thumb_next_memory import Memory

ADDRESS=0x021cfcf8
PACKET=0x02401000
FIRST=0x02402000
OUTPUT=0x02403000
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208d178':16,'0208e53c':24}


def fixtures(name):
    if name=='0208d178':
        rows=[dict(flags=flag,header=(flag*37^0xa5)&255,bytes=[0,1,12,1024,0xffffffff][flag%5],checksum=0,mutate=bool(flag&1)) for flag in range(256)]
        rows += [dict(flags=flag,header=0xb9,bytes=100,checksum=checksum,mutate=mutate) for flag,checksum,mutate in itertools.product([0,1,2,4,16,18,255],[1,65535,0xffffffff],[False,True])]
        rows += [dict(flags=flag,header=high*16+(high^7),bytes=[0,4,100,0xffffffff][high%4],checksum=0,mutate=False) for flag,high in itertools.product([0,1,2,4,16,17,18],range(16))]
        rows += [dict(flags=flag,header=0xb9,bytes=100,checksum=0,mutate=False) for flag in [5,10,26]]
        return rows
    product=list(itertools.product([-1,0,1,2,3],['first','second','third','fourth','exhaust','other'],[119,120,0xffffffff],[False,True]))
    rows=[dict(mode=mode,outcome=outcome,timer=timer,lease=[0,1,0x12345678,0x80000000,0xffffffff][i%5],mutate=mutate,alias=['out','timer','lease'][i%3]) for i,(mode,outcome,timer,mutate) in enumerate(product)]
    rows += [dict(mode=mode,outcome=outcome,timer=119,lease=0xffffffff,mutate=False,alias=alias) for mode,outcome,alias in itertools.product([1,2],['first','exhaust'],['out','timer','lease'])]
    return rows


def scenario(name,f,ordinal):
    memory=Memory({ADDRESS:84,PACKET:14,FIRST:20,OUTPUT:4},ordinal)
    setv,getv=memory.set,memory.get
    setv(ADDRESS+32,0x0a010203);setv(ADDRESS+56,f.get('timer',0));setv(ADDRESS+76,f.get('lease',0));setv(ADDRESS+80,0x0a000001)
    setv(PACKET+12,f.get('header',0),1);setv(PACKET+13,f.get('flags',0),1)
    output={'out':OUTPUT,'timer':ADDRESS+56,'lease':ADDRESS+76}[f.get('alias','out')]
    initial=memory.snapshot();actions=[]

    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=checks,mutations=changes))
        return returned

    result=None
    if name=='0208d178':
        arguments=[FIRST,PACKET,f['bytes'],0x76543210]
        changes=[word(PACKET+12,f['header']^0x98,1),word(PACKET+13,f['flags']^0x1c,1)] if f['mutate'] else []
        call(0x0208bbac,[PACKET,f['bytes'],FIRST,6],f['checksum'],changes)
        if f['checksum']==0:
            flags=getv(PACKET+13,1);length=(f['bytes']-(getv(PACKET+12,1)&0xf0)//4)&0xffffffff;masked=flags&0x17
            if masked in [2,18]:
                if flags&0x28==0:call(0x0208cdd0 if masked==2 else 0x0208ce58,[FIRST,PACKET,length])
            elif masked in [16,17]:call(0x0208cef0,[FIRST,PACKET,length])
            elif masked==1:call(0x0208d0e0,[FIRST,PACKET,length])
            elif flags&4:call(0x0208d154,[FIRST,PACKET])
            else:call(0x0208cc24,[FIRST,PACKET,length,0])
    else:
        arguments=[output,f['mode']&0xffffffff,0x55667788,0x99aabbcc]
        changes=[word(ADDRESS+32,0xc0a80102)] if f['mutate'] else []
        call(0x0208d7c0,[],changes=changes);call(0x0208d764,[])
        call(0x0208d780,[68,67,getv(ADDRESS+32) if f['mode']==1 else 0xffffffff])
        terminal={'first':1,'second':2,'third':3,'fourth':4,'exhaust':5,'other':2}[f['outcome']]
        for retry in range(4):
            value=(0xa5000000|ordinal<<4|retry)&0xffffffff
            call(0x0208e250,[f['mode']],value)
            response=([1,7,0xffffffff][ordinal%3] if f['outcome']=='other' else 2) if retry+1>=terminal else 0
            changes=[word(ADDRESS+56,getv(ADDRESS+56)^0x80000000),word(ADDRESS+76,getv(ADDRESS+76)^0x13579bdf)] if f['mutate'] else []
            call(0x0208e2e0,[value,retry],response,changes)
            if response:break
        changes=[word(ADDRESS+56,f['timer']),word(ADDRESS+76,f['lease']^0xa5a5a5a5)] if f['mutate'] else []
        call(0x0208d7e0,[],changes=changes)
        if response==2:
            setv(output,getv(ADDRESS+76)>>1);setv(ADDRESS+56,((getv(ADDRESS+76)*3)&0xffffffff)>>3);result=1
        else:
            timer=getv(ADDRESS+56)>>1;setv(ADDRESS+56,timer);setv(output,timer)
            if f['mode'] in [1,2] and timer<60:
                setv(output,1)
                if f['mode']==1:setv(ADDRESS+56,getv(ADDRESS+76)>>3)
            result=0
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result,args=arguments,output=output)
