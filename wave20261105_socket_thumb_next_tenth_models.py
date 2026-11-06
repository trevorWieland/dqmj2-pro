import itertools
from wave20261105_socket_thumb_next_memory import Memory

SOCKETS=[0x02402000,0x02402200]
RECEIVES=[0x02403000,0x02403200]
CPS=[0x02404000,0x02404200]
SOURCE=0x02405000
BUFFER=0x02405200
OUTPUT=0x02406000
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208f2ac':32,'0208f2f8':48,'0208f3bc':16}


def signed(value):return value if value<0x80000000 else value-0x100000000


def fixtures(name):
    if name=='0208f2ac':
        rows=[dict(mode=i,flag=[0,1,2,255,0x80000001][i%5],first=[-6,-7,0,0x80000000][i%4],second=[0,-1,0x12345678,0x80000000][i%4],mutate=bool(i&1)) for i in range(256)]
        return rows+[dict(mode=m,flag=b,first=a,second=0x80000001,mutate=t) for m,b,a,t in itertools.product([0,1,4,128],[0,1,2,0xffffffff],[-6,-7,0],[False,True])]
    if name=='0208f3bc':
        return [dict(length=length,consumed=consumed,state=state,alias=alias) for length,consumed,state,alias in itertools.product([0,1,16,31,0x7fffffff],[0,1,15,32],[0,4,255],range(4))]
    return [dict(mode=mode,kind=kind,limit=limit,noConsume=noConsume,mutate=mutate,outputs=outputs,local=local) for mode,kind,limit,noConsume,mutate,outputs,local in itertools.product([0,1,4,255],range(5),[1,8,31],[0,1,255],[False,True],range(4),[0,65535])]



def scenario(name,f,ordinal):
    regions={**{p:128 for p in SOCKETS},**{p:264 for p in RECEIVES},**{p:72 for p in CPS},SOURCE:128,BUFFER:128,OUTPUT:32}
    memory=Memory(regions,ordinal);get,setv=memory.get,memory.set
    socket,receive,cps=SOCKETS[0],RECEIVES[0],CPS[0]
    for i,p in enumerate(SOCKETS):setv(p+100,RECEIVES[i]);setv(p+115,f.get('mode',0),1);setv(p+112,0x800f,2);setv(p+116,f.get('local',0),2)
    for i,p in enumerate(RECEIVES):setv(p+196,CPS[i]);setv(p+248,f.get('consumed',3));setv(p+254,f.get('noConsume',0),1)
    for p in CPS:setv(p+8,f.get('state',4),1);setv(p+10,0xaabc,2);setv(p+24,0x8012,2);setv(p+28,0x89abcdef);setv(p+64,SOURCE);setv(p+68,f.get('length',16))
    initial=memory.snapshot();actions=[];allowed=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def put(at,value,size=4):setv(at,value,size);allowed.append((at,size))
    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:
            if SP-SPECS[name]<=at and at+len(raw)<=SP:continue
            memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned&0xffffffff,checks=checks,mutations=changes));return returned&0xffffffff
    if name=='0208f2ac':
        arguments=[socket,BUFFER,31,OUTPUT+8,OUTPUT+12,f['flag']]
        def invoke(address,value):return call(address,arguments[:5],value,changes=[word(socket+115,4 if f['mode']!=4 else 0,1)] if f['mutate'] else [])
        if f['mode']==4:result=invoke(0x0208f404,f['second'])
        else:
            result=invoke(0x0208f2f8,f['first'])
            if result==0xfffffffa and f['flag']&1:result=invoke(0x0208f404,f['second'])
    elif name=='0208f3bc':
        pointerSets=[(OUTPUT,OUTPUT+8,OUTPUT+10,OUTPUT+12),(cps+68,cps+10,cps+24,cps+28),(receive+248,socket+116,socket+118,socket+120),(OUTPUT,OUTPUT+8,OUTPUT+8,OUTPUT+12)]
        lengthPointer,localPointer,remotePointer,ipPointer=pointerSets[f['alias']];arguments=[socket,lengthPointer,localPointer,remotePointer,ipPointer]
        consumed=signed(get(receive+248));length=signed((get(cps+68)-consumed)&0xffffffff)
        if length>=0:
            put(localPointer,get(cps+10,2),2);put(remotePointer,get(cps+24,2),2);put(ipPointer,get(cps+28));put(lengthPointer,length)
            result=(get(cps+64)+consumed)&0xffffffff if length!=0 or get(cps+8,1)==4 else 0
        else:put(lengthPointer,-1);result=0
    else:
        port=OUTPUT+8 if f['outputs'] in [1,3] else 0;ip=OUTPUT+12 if f['outputs'] in [2,3] else 0
        arguments=[socket,BUFFER,f['limit'],port,ip]
        mask=(ordinal*0x1010101^0xa5a5a5a5)&0xffffffff;call(0x02007ff4,[],mask)
        length=[-1,0,0,4,16][f['kind']];pointer=SOURCE if f['kind']>=2 else 0
        changes=[word(SP-28,length),word(SP-34,0xaabc,2),word(SP-36,0x8012,2),word(SP-32,0x89abcdef)]
        if f['mutate']:changes += [word(socket+115,1 if f['mode']==0 else 0,1),word(socket+116,0,2)]
        call(0x0208f3bc,[socket,SP-28,SP-34,SP-36,SP-32],pointer,changes)
        if pointer:
            if length==0:result=-6
            else:
                copied=min(f['limit'],length);consumed=copied if get(socket+115,1) in [0,4] else length
                changes=[(BUFFER,bytes(memory.get(SOURCE+i,1) for i in range(copied)))]
                if f['mutate']:changes += [word(socket+100,RECEIVES[1]),word(RECEIVES[1]+254,f['noConsume']^1,1),word(RECEIVES[1]+248,0x12345678)]
                call(0x02008e0c,[pointer,BUFFER,copied],changes=changes)
                latest=get(socket+100)
                if get(latest+254,1)==0:put(latest+248,get(latest+248)+consumed)
                result=consumed
        else:
            result=0 if length==0 else -28;put(socket+112,get(socket+112,2)&~6,2)
        if result>=0:
            if port and ip:put(port,0x8012,2);put(ip,0x89abcdef)
            if get(socket+116,2)==0:put(socket+116,0xaabc,2)
        call(0x02008008,[mask])
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result&0xffffffff,args=arguments,allowedWrites=allowed)
