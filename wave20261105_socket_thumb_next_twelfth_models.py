import itertools
from wave20261105_socket_thumb_next_memory import Memory
from wave20261105_socket_thumb_next_twelfth_callbacks import TARGETS
SOCKETS=[0x02402000,0x02402200]
RECEIVES=[0x02403000,0x02403200]
PACKETS=[0x02404000,0x02404200]
SOURCE=0x02405000
BUFFER=0x02405200
OUTPUT=0x02406000
CONFIGS=[0x02407000,0x02407200]
CONFIG_POINTER=0x020de7cc
COUNTERS=0x021d15a4
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208f578':40,'0208f660':32}


def fixtures(name):
    if name=='0208f578':
        rows=[]
        for ordinal,(path,flag,noConsume,mode,mutate) in enumerate(itertools.product(range(7),[0,1,2,3,0x80000001,0xffffffff],[0,1,255],['arm','thumb'],[False,True])):
            rows.append(dict(path=path,flag=flag,noConsume=noConsume,mode=mode,mutate=mutate,size=[0,1,16,31][ordinal%4],limit=[1,8,32][ordinal%3],outputs=ordinal%4,alias=ordinal%3,next=bool((ordinal//4)&1)))
        return rows
    rows=[]
    for ordinal,(capacity,allocated,mode,mutate,queues,local) in enumerate(itertools.product([False,True],[False,True],['arm','thumb'],[False,True],range(4),[0,65535])):
        rows.append(dict(capacity=capacity,allocated=allocated,mode=mode,mutate=mutate,queues=queues,local=local,length=[0,1,16,31][ordinal%4],counter=[0,0x7fffffff,0xffffffff][ordinal%3]))
    return rows


def scenario(name,f,ordinal):
    memory=Memory({**{p:128 for p in SOCKETS},**{p:276 for p in RECEIVES},**{p:76 for p in PACKETS},SOURCE:128,BUFFER:128,OUTPUT:32,**{p:32 for p in CONFIGS},CONFIG_POINTER:4,COUNTERS:8},ordinal);get,setv=memory.get,memory.set
    socket,receive,packet=SOCKETS[0],RECEIVES[0],PACKETS[0]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def put(at,value,size=4):setv(at,value,size);allowed.append((at,size))
    def selectedMode(index):return f['mode'] if index==0 else 'thumb' if f['mode']=='arm' else 'arm'
    for index,p in enumerate(CONFIGS):
        for kind,offset in [('allocate',24),('release',28)]:
            mode=selectedMode(index);value=TARGETS[kind,mode]|int(mode=='thumb')
            if f.get('_wrongTag')==kind:value^=1
            setv(p+offset,value)
    setv(CONFIG_POINTER,CONFIGS[0]);setv(COUNTERS,f.get('counter',0));setv(COUNTERS+4,f.get('counter',0))
    for i,p in enumerate(SOCKETS):setv(p+100,RECEIVES[i]);setv(p+112,1,2);setv(p+116,f.get('local',0),2);setv(p+10,0xaabc,2);setv(p+24,0x8012,2);setv(p+26,0x8123,2);setv(p+28,0x89abcdef);setv(p+32,0xaabbccdd)
    for p in PACKETS:setv(p,PACKETS[1] if f.get('next',False) else 0);setv(p+4,f.get('size',16),2);setv(p+6,0x8012,2);setv(p+8,0x89abcdef)
    for p in RECEIVES:setv(p+254,f.get('noConsume',0),1);setv(p+256,PACKETS[1] if f.get('next',False) else packet);setv(p+260,packet if f.get('path',1)==0 else 0);setv(p+264,64,2);setv(p+266,128 if f.get('capacity',True) else 0,2)
    if name=='0208f660':setv(receive+256,PACKETS[1] if f['queues']&1 else 0);setv(receive+260,PACKETS[1] if f['queues']&2 else 0)
    initial=memory.snapshot();actions=[];allowed=[]
    def call(address,args,returned=0x89abcdef,changes=None,kind=None,mode=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned&0xffffffff,checks=checks,mutations=changes,kind=kind,mode=mode));return returned&0xffffffff
    def callback(kind,args,returned=0x89abcdef,changes=None):
        pointer=get(get(CONFIG_POINTER)+(24 if kind=='allocate' else 28));address=pointer&~1;mode=next(m for (k,m),v in TARGETS.items() if k==kind and v==address)
        return call(address,args,returned,changes,kind,mode)
    mask=(ordinal*0x1010101^0xa5a5a5a5)&0xffffffff
    if name=='0208f578':
        port=OUTPUT if f['alias']==0 else packet+4 if f['alias']==1 else socket+116;ip=OUTPUT+4 if f['alias']==0 else packet+8 if f['alias']==1 else socket+120
        arguments=[socket,BUFFER,f['limit'],port if f['outputs']&1 else 0,ip if f['outputs']&2 else 0,f['flag']]
        changes=[word(socket+100,RECEIVES[1]),word(CONFIG_POINTER,CONFIGS[1])] if f['mutate'] else []
        if f['path']==1:changes.append(word(receive+260,packet))
        call(0x02007ff4,[],mask,changes)
        current=get(receive+260);result=0;waited=0
        while not current:
            if not f['flag']&1:result=-6;break
            waited+=1;changes=[]
            if f['path'] in [2,3] and waited>=(2 if f['path']==3 else 1):changes.append(word(receive+260,packet))
            if f['path'] in [0,1,6]:changes.append(word(receive+260,packet))
            if f['path']==5:changes.append(word(socket+112,0,2))
            call(0x020068d4,[receive+268],changes=changes)
            invalid=call(0x02090294,[socket],int(f['path']==4))
            if invalid or not get(socket+112,2)&1:result=-56;break
            current=get(receive+260)
            if waited>2:raise ValueError('Bounded UDP waiting model did not terminate')
        if current:
            copied=min(f['limit'],get(current+4,2));changes=[(BUFFER,bytes(get(current+12+i,1) for i in range(copied)))]
            if f['mutate']:changes += [word(current+4,7,2),word(current+6,0xabcd,2),word(current+8,0xaabbccdd),word(receive+254,0 if f['noConsume'] else 1,1)]
            call(0x02008e0c,[current+12,BUFFER,copied],changes=changes)
            if arguments[3]:put(arguments[3],get(current+6,2),2)
            if arguments[4]:put(arguments[4],get(current+8))
            result=get(current+4,2)
            if get(receive+254,1)==0:
                put(receive+260,get(current))
                if get(current)==0:put(receive+256,0)
                callback('release',[current],changes=[word(receive+264,17,2)] if f['mutate'] else [])
                put(receive+264,get(receive+264,2)-result,2)
        call(0x02008008,[mask])
    else:
        arguments=[SOURCE,f['length'],socket,0x99aabbcc]
        changes=[word(socket+100,RECEIVES[1]),word(CONFIG_POINTER,CONFIGS[1]),word(socket+116,0,2)] if f['mutate'] else []
        call(0x02007ff4,[],mask,changes)
        if get(receive+266,2)>=get(receive+264,2)+f['length']:
            changes=[word(receive+264,4,2),word(socket+24,0xabcd,2),word(socket+28,0xaabbccdd)] if f['mutate'] else []
            allocated=callback('allocate',[12+f['length']],packet if f['allocated'] else 0,changes)
            if allocated:
                put(receive+264,get(receive+264,2)+f['length'],2);put(packet,0);put(packet+4,f['length'],2);put(packet+6,get(socket+24,2),2);put(packet+8,get(socket+28))
                changes=[(packet+12,bytes(get(SOURCE+i,1) for i in range(f['length'])))]
                if f['mutate']:changes += [word(receive+256,PACKETS[1]),word(receive+260,0),word(socket+26,0x1234,2),word(socket+32,0x10203040)]
                call(0x02008e0c,[SOURCE,packet+12,f['length']],changes=changes)
                if get(receive+256):put(get(receive+256),packet)
                put(receive+256,packet)
                if get(receive+260)==0:put(receive+260,packet)
            else:put(COUNTERS,get(COUNTERS)+1)
        else:put(COUNTERS+4,get(COUNTERS+4)+1)
        if get(socket+116,2)==0:put(socket+116,get(socket+10,2),2)
        put(socket+24,get(socket+26,2),2);put(socket+28,get(socket+32))
        call(0x02006924,[receive+268]);call(0x02008008,[mask]);result=1
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result&0xffffffff,args=arguments,allowedWrites=allowed)
