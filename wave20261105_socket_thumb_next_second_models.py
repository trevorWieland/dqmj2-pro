import itertools
from wave20261105_socket_thumb_next_memory import Memory
from wave20261105_socket_thumb_next_first_models import SINGLETON,ADDRESS,THREADS,SOCKETS,SP,STOP
BUFFER=[0x02402000,0x02402100]
OUTPUT=0x02403000
SPECS={'0208d820':24,'0208d968':32,'0208d9a0':24,'0208d9f0':8,'0208da30':24,'0208da88':8}


def fixtures(name):
    if name=='0208d820':return [dict(outcome=o,tick=t,mutate=m) for o,t,m in itertools.product(['immediate','second','third','exhaust','inactive','wait-progress','restore-off'],[(0,0),(65535,0),(65536,1),(0x89abcdef,0x12345678),(0xffffffff,0xffffffff)],[False,True])]
    if name=='0208d968':return [dict(size=s,waits=w,mutate=m,alias=a) for s,w,m,a in itertools.product([0,4],[0,1,3],[False,True],[False,True])]
    if name=='0208d9a0':return [dict(size=s,state=state,waits=w,exitState=e,mutate=m,alias=a) for s,state,w,e,m,a in itertools.product([0,4],[0,4,10],[0,1,2],[False,True],[False,True],[False,True])]
    if name=='0208d9f0':return [dict(present=p,state=s,mode=m,returned=r,mutate=c,alias=a) for p,s,m,r,c,a in itertools.product([False,True],[0,4,10,11,255],[0,1,255],[0,BUFFER[0],0xffffffff],[False,True],[False,True])]
    if name=='0208da30':return [dict(size=s,count=c,equal=e,state=state,mutate=m) for (s,c),e,state,m in itertools.product([(0,0),(0,1),(4,0),(4,1),(4,4),(4,8),(8,3),(16,16),(16,0xffffffff)],[False,True],[0,4,10,11],[False,True])]
    return [dict(present=p,mode=m,count=c,mutate=t) for p,m,c,t in itertools.product([False,True],[0,1,255],[0,3,0xffffffff],[False,True])]


def scenario(name,f,ordinal):
    sizes={SINGLETON:8,ADDRESS:84,THREADS[0]:168,THREADS[1]:168,SOCKETS[0]:100,SOCKETS[1]:100,BUFFER[0]:32,BUFFER[1]:32,OUTPUT:4}
    memory=Memory(sizes,ordinal);socket=SOCKETS[0];setv=memory.set;getv=memory.get
    setv(SINGLETON+4,THREADS[0]);setv(ADDRESS+80,0x0a000001)
    for index,a in enumerate(THREADS):setv(a+164,SOCKETS[index] if f.get('present',True) else 0)
    for index,a in enumerate(SOCKETS):
        setv(a,THREADS[index]);setv(a+4,0);setv(a+8,f.get('state',4),1);setv(a+9,f.get('mode',0),1);setv(a+60,f.get('size',4) if f.get('equal') else 31);setv(a+64,BUFFER[index]);setv(a+68,f.get('size',0))
    output=socket+68 if f.get('alias') else OUTPUT
    arguments=[socket,0x11223344,0x55667788,0x99aabbcc]
    if name in ['0208d968','0208d9a0']:arguments[:2]=[output,socket]
    if name=='0208d9f0':arguments[0]=output
    if name=='0208da30':arguments[:2]=[f['count'],socket]
    if name=='0208da88':arguments[0]=f['count']
    initial=memory.snapshot();actions=[]

    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items())
        changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=checks,mutations=changes))
        return returned

    def word(at,value,size=4):return (at,int(value&((1<<(size*8))-1)).to_bytes(size,'little'))
    def switch_buffer():return [word(socket+64,BUFFER[1]),word(SINGLETON+4,THREADS[1])]
    def restore_changes():
        if not f.get('mutate'):return []
        return [*switch_buffer(),word(socket+68,0 if getv(socket+68) else 3),word(socket+4,0x80000000),word(socket+8,{0:0,4:11,10:4,11:10}.get(getv(socket+8,1),0),1)]
    result=None
    if name=='0208d820':
        seed=[0,1,0xffffffff,0x80000000][ordinal%4];call(0x0208d71c,[],seed)
        for attempt in range(1,4):
            setv(socket+40,seed);setv(socket+8,2,1)
            low,high=f['tick'];call(0x02007a9c,[],[low,high]);setv(socket+16,low>>16|high<<16)
            success=f['outcome']=='immediate' or f['outcome']=='second' and attempt==2 or f['outcome']=='third' and attempt==3
            changes=[word(socket+8,4 if success else 2,1),word(ADDRESS+80,0 if f['outcome']=='inactive' else 0x0a000001)]
            if f['mutate']:changes += [word(socket+40,seed^0xa5a5a5a5),word(SINGLETON+4,THREADS[1])]
            call(0x0208cbc4,[socket,2,24],changes=changes)
            level=(0x80|attempt<<8)^ordinal;call(0x02007ff4,[],level)
            if getv(socket+8,1)==2 and getv(ADDRESS+80)!=0:
                setv(socket+4,1);changes=[word(socket+8,4,1)] if f['outcome']=='wait-progress' else []
                call(0x020068d4,[0],changes=changes)
            changes=[word(ADDRESS+80,0)] if f['outcome']=='restore-off' else []
            call(0x02008008,[level],changes=changes)
            if getv(socket+8,1)==4:result=0;break
            if getv(ADDRESS+80)==0:result=1;break
        if result is None:result=1
    elif name=='0208d968':
        waits=f['waits'];call(0x02007ff4,[],0x98760080,changes=[word(socket+68,0 if waits else 4)])
        size=getv(socket+68);done=0
        while size==0:
            setv(socket+4,3);done+=1
            call(0x020068d4,[0],changes=[word(socket+68,8 if done>=waits else 0)])
            size=getv(socket+68)
        call(0x02008008,[0x98760080],changes=restore_changes());setv(output,size);result=getv(socket+64)
    elif name=='0208d9a0':
        if getv(socket+68)==0 and getv(socket+8,1)==4:
            call(0x02007ff4,[],0x98760080,changes=[word(socket+68,4 if f['waits']==0 else 0)])
            done=0
            while getv(socket+68)==0 and getv(socket+8,1)==4:
                setv(socket+4,2);done+=1
                changes=[]
                if done>=f['waits']:changes=[word(socket+8,0,1)] if f['exitState'] else [word(socket+68,8)]
                call(0x020068d4,[0],changes=changes)
            call(0x02008008,[0x98760080],changes=restore_changes())
        else:call(0x020069f8,[],changes=restore_changes())
        size=getv(socket+68);setv(output,size);result=getv(socket+64) if size else 0
    elif name=='0208d9f0':
        if not f['present']:setv(output,0);result=0
        else:
            target=0x0208d968 if f['state'] in [10,11] else 0x02092854 if f['mode'] else 0x0208d9a0
            changes=[word(output,0x12340000+ordinal)]
            if f['mutate']:changes+=switch_buffer()+[word(socket+8,255,1)]
            result=call(target,[output,socket],f['returned'],changes)
    elif name=='0208da30':
        call(0x02007ff4,[],0x98760080)
        size=getv(socket+68);full=size==getv(socket+60) and f['count']!=0
        if f['count']>=size:setv(socket+68,0)
        else:
            buffer=getv(socket+64);remaining=size-f['count'];setv(socket+68,remaining)
            changes=[(buffer,memory.read(buffer+f['count'],remaining))]
            if f['mutate']:changes += [word(socket+60,0),word(socket+64,BUFFER[1])]
            call(0x0201b1bc,[buffer,buffer+f['count'],remaining],changes=changes)
        call(0x02008008,[0x98760080],changes=restore_changes())
        if getv(socket+8,1) not in [10,11] and (getv(socket+68)==0 or full):call(0x0208cc0c,[socket,27])
    elif name=='0208da88' and f['present']:
        changes=switch_buffer()+[word(socket+8,255,1)] if f['mutate'] else []
        call(0x020928f8 if f['mode'] else 0x0208da30,[f['count'],socket],changes=changes)
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result,args=arguments,output=output)
