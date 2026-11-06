import itertools
from wave20261105_socket_thumb_next_memory import Memory
SOCKETS=[0x02402000,0x02402200]
SENDS=[0x02403000,0x02403200]
COMMANDS=[0x02404000,0x02404200]
SOURCE=0x02405000
RINGS=[0x02406000,0x02406200]
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208f91c':32,'0208fa34':32}


def signed(v):return v if v<0x80000000 else v-0x100000000


def fixtures(name):
    if name=='0208f91c':
        rows=[dict(mode=i,flag=[0,1,3,0x80000000][i%4],allocated=bool(i%5),mutate=bool(i//2&1),wrap=bool(i&1),length=[0,1,7,15][i%4],enqueue=[0,-1,0x80000000][i%3],local=[0,65535][i//4%2],peer=[0,0x11223344][i//8%2],inputPeer=[0,0x89abcdef][i//16%2]) for i in range(256)]
        return rows+[dict(mode=m,flag=b,allocated=a,mutate=t,wrap=w,length=7,enqueue=0 if b==0 else -1,local=0 if w else 65535,peer=0 if t else 0x11223344,inputPeer=0 if w else 0x89abcdef) for m,b,a,t,w in itertools.product([0,1,4,255],[0,1,3],[False,True],[False,True],[False,True])]
    rows=[dict(mode=i,state=[0,1,4,5,8,0x8004,0xffff][i%7],peer=bool(i&1),mutate=bool(i//2&1),path=['zero','one','two','negative'][i%4],write=[0,-1,1,0x80000000][i//4%4]) for i in range(256)]
    return rows+[dict(mode=m,state=s,peer=p,mutate=t,path=c,write=r) for m,s,p,t,c,r in itertools.product([0,1,4],[0,4,0x8004],[False,True],[False,True],['zero','one','two'],[0,-1,1,2,0x80000000])]


def scenario(name,f,ordinal):
    memory=Memory({**{p:128 for p in SOCKETS},**{p:272 for p in SENDS},**{p:44 for p in COMMANDS},SOURCE:128,**{p:128 for p in RINGS}},ordinal);get,setv=memory.get,memory.set
    command,socket,send=COMMANDS[0],SOCKETS[0],SENDS[0]
    for i,p in enumerate(SOCKETS):setv(p+104,SENDS[i]);setv(p+112,f.get('state',5),2);setv(p+115,f['mode'],1);setv(p+116,f.get('local',0),2);setv(p+118,0x8123,2);setv(p+120,f.get('peer',1) if name=='0208f91c' else 0x11223344);setv(p+72,70);setv(p+76,RINGS[0])
    for i,p in enumerate(SENDS):setv(p+248,16);setv(p+252,RINGS[i]);setv(p+256,3,2);setv(p+258,1,2);setv(p+268,SOCKETS[1])
    for i,p in enumerate(COMMANDS):setv(p+4,SOCKETS[i]);setv(p+32,0x8001,2);setv(p+36,0xaabc,2);setv(p+38,0x8012,2);setv(p+40,0x89abcdef if f.get('peer') else 0)
    initial=memory.snapshot();actions=[];allowed=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def put(at,value,size=4):setv(at,value,size);allowed.append((at,size))
    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned&0xffffffff,checks=checks,mutations=changes));return returned&0xffffffff
    if name=='0208f91c':
        writeIn=15 if f['wrap'] else 0;length=f['length'];remote=0x8012;peer=f['inputPeer'];arguments=[socket,SOURCE,length,writeIn,remote,peer,f['flag']]
        changes=[word(socket+104,SENDS[1]),word(send+252,RINGS[1]),word(send+268,SOCKETS[0]),word(socket+115,1 if f['mode']!=1 else 0,1),word(command+4,SOCKETS[1])] if f['mutate'] else []
        allocated=call(0x0208ebd8,[0x0208fa35,get(send+268),f['flag']],command if f['allocated'] else 0,changes)
        if not allocated:result=-33
        else:
            put(command+13,3 if f['flag']&1 and get(socket+115,1)!=1 else 0,1)
            buffer=get(send+252);size=signed(get(send+248))
            def copy(source,target,count):
                changes=[(target,bytes(get(source+i,1) for i in range(count)))]
                if f['mutate']:changes += [word(send+256,0xabcd,2),word(send+268,SOCKETS[1]),word(socket+115,1,1),word(socket+116,0,2)]
                call(0x02008e0c,[source,target,count],changes=changes)
            if writeIn+length<size:
                put(command+16,buffer+writeIn);put(command+20,length);put(command+24,0);put(command+28,0);writeIn+=length
            else:
                put(command+16,buffer+writeIn);put(command+20,size-writeIn);put(command+24,buffer);put(command+28,length-get(command+20));writeIn=get(command+28)
                copy(SOURCE+get(command+20),get(command+24),get(command+28))
            copy(SOURCE,get(command+16),get(command+20));saved=get(send+256,2);put(command+32,writeIn,2);put(send+256,get(command+32,2),2)
            if get(socket+115,1)==1:
                if get(socket+116,2)==0:
                    port=call(0x0208d6b4,[],0xfedc,changes=[word(socket+118,0xff01,2),word(socket+120,0xaabbccdd)] if f['mutate'] else [])
                    put(socket+116,port,2);put(socket+10,get(socket+116,2),2)
                put(command+36,get(socket+116,2),2)
                if get(socket+120)==0 or peer!=0:put(command+40,peer);put(command+38,remote,2)
                else:put(command+40,get(socket+120));put(command+38,get(socket+118,2),2)
            else:put(command+40,0)
            result=call(0x0208ecb0,[get(send+268),command],f['enqueue'],changes=[word(send+256,0x1234,2)] if f['mutate'] else [])
            if result!=0:put(send+256,saved,2);length=0
            result=length
    else:
        arguments=[command,0x11223344,0x55667788,0x99aabbcc];copied=0;connected=get(socket+112,2)&4
        if get(socket+115,1) not in [0,4] or connected:
            if get(command+40):
                changes=[word(socket+115,1 if f['mode'] in [0,4] else 0,1)] if f['mutate'] else []
                call(0x0208d780,[get(command+36,2),get(command+38,2),get(command+40)],changes=changes)
            tcp=get(socket+115,1) in [0,4];offset=54 if tcp else 42;buffer=get(socket+76)+offset;raw=signed(get(socket+72))-offset
            sendLength=call(0x0208fb2c,[raw],8,changes=[word(socket+72,0),word(socket+76,RINGS[1])] if f['mutate'] else []) if tcp else raw
            counts={'zero':[0],'negative':[0xffffffff],'one':[3,0],'two':[3,2,0]}[f['path']]
            for index,count in enumerate(counts):
                changes=[word(command+32,0x8123+index,2),word(socket+104,SENDS[1])] if f['mutate'] else []
                amount=call(0x0208fb94,[buffer,sendLength,command],count,changes)
                if signed(amount)<=0:break
                changes=[word(socket+115,0 if f['mode']==1 else 1,1),word(socket+112,0x800f,2)] if f['mutate'] else []
                written=call(0x0208dd38,[buffer,amount],f['write'],changes)
                if signed(written)<=0:
                    if get(socket+115,1) in [0,4]:
                        put(socket+112,get(socket+112,2)&~14,2);put(socket+112,get(socket+112,2)|128,2)
                        call(0x0208d910,[],changes=[word(socket+112,0x8000,2),word(command+32,0x9234,2)] if f['mutate'] else [])
                    copied=-76;break
                copied+=written
        else:copied=-76
        put(send+258,get(command+32,2),2);call(0x02006924,[send+260]);result=copied
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result&0xffffffff,args=arguments,allowedWrites=allowed)
