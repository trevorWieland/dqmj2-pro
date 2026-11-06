from wave20261105_gamespy_qr2_next_first_models import Memory,word,half,put,signed

N,P,S,I,O,D,ST=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x2176000
G,GD,DI,GAME=0x21d2bc4,0x20e172c,0x21d2cc8,0x21d23f0
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700800,0x20e1740
PROGRESS,COMPLETE=0x27e0100,0x27e0140
ARITY={0x20a8c34:6,0x20061ac:5,0x20b6b4c:1,0x20b6564:1,0x20a8b6c:1,0x20b6aa8:1,0x20b65f8:1,0x20a8d88:1,0x20a8c00:6,0x20b70c8:3,0x20a8ef8:0,0x20b67e0:4,0x20b6840:1,0x20b69e4:1,0x20b6c90:1,0x20b6708:1,0x20b6eac:2,PROGRESS:2,COMPLETE:4}


def dynamic_callbacks(v):
    mode=v.get('mode','mixed')
    return {address:dict(mode='thumb'if mode=='thumb'or mode=='mixed'and index else'arm',kind='function',fixtureOnly=True,runtimeTargetNamespaceUnresolved=True)for index,address in enumerate([PROGRESS,COMPLETE])}


def cstring(memory,address):
    out=bytearray()
    for index in range(1024):
        ch=memory.read(address+index,1)
        if ch==b'\0':return bytes(out)
        out.extend(ch)
    raise ValueError('Bounded NAT hostname lacks terminator')


def peer(memory,address):
    return None if address==0 else[memory.read(address+1,1).hex(),memory.read(address+2,2).hex(),memory.read(address+4,4).hex()]


def initial(address,v):
    regions={N:bytes(84),P:bytes(80),S:bytes.fromhex('0802341204030201'),I:bytes(range(64)),O:bytes(128),D:bytes(128),ST:bytes(64),G:bytes(32),GD:bytes.fromhex('060000000b0000000a000000'),DI:bytes(512),GAME:bytes(64),MAGIC:b'%s.%s\0',SP-0x1000:bytes(0x1000)}
    memory=Memory(regions)
    for offset,value in [(0,v.get('socket',-1)),(4,v.get('gameSocket',-1)),(8,0x10203040),(16,v.get('state',0)),(36,v.get('retryCount',0)),(40,v.get('maxRetry',1)),(44,v.get('retryTime',100)),(48,0x04030201),(64,0x89abcdef),(68,3),(72,27)]:put(memory,N+offset,value)
    put(memory,N+52,v.get('port',0x80ff),2);memory.write(N+54,bytes([v.get('gotRemote',0),v.get('sentRemote',0)]));memory.write(N+76,bytes.fromhex('0802ff8004030201'))
    for callback,binding in dynamic_callbacks(v).items():put(memory,N+(56 if callback==PROGRESS else 60),callback|(1 if binding['mode']=='thumb'else 0))
    put(memory,P+12,0x11223344);put(memory,P+16,v.get('wirePort',0x3412),2);memory.write(P+18,bytes([v.get('gotData',1),v.get('finished',0)]));put(memory,G+28,v.get('active',0))
    memory.write(O,v.get('override','override.example').encode()+b'\0');memory.write(D,v.get('default','nat.example').encode()+b'\0');memory.write(GAME,v.get('game','dqm').encode()+b'\0')
    args={0x20b6670:[v.get('socket',7),0x04030201,v.get('port',0x80ff),I,v.get('length',8)],0x20b6b74:[0 if v.get('useDefault')else O,D],0x20b6c90:[v.get('cookie',0x10203040)],0x20b6cb4:[0 if v.get('null')else N],0x20b6f3c:[N,P,S],0x20b6fa8:[N,P,S]}
    return memory,args[address]


def effect(target,args,memory,v):
    a=[item&0xffffffff for item in args];normalized=a[:];result=0x11223344
    if target==0x20a8c34:
        length=signed(a[2]);normalized=[a[0],memory.read(a[1],max(0,min(length,64))).hex(),a[2],a[3],peer(memory,a[4]),a[5]]
    elif target==0x20061ac:
        fmt=cstring(memory,a[2]);game=cstring(memory,a[3]);default=cstring(memory,a[4]);raw=game+b'.'+default
        if fmt!=b'%s.%s':raise ValueError('Unexpected bounded NAT hostname format')
        memory.write(a[0],raw[:max(a[1]-1,0)]+b'\0');normalized=[a[1],fmt.hex(),game.hex(),default.hex()];result=len(raw)
    elif target==0x20b6b4c:normalized=[cstring(memory,a[0]).hex()];result=v.get('resolved',0x12345678)
    elif target==0x20b6564:result=N if v.get('found',True)else 0
    elif target in [0x20a8b6c,0x20b65f8,0x20b6840,0x20b6708]:pass
    elif target==0x20b6aa8:result=v.get('activeFirst',1)if a[0]==10 else v.get('activeSecond',0)
    elif target==0x20a8d88:
        count=word(memory,ST);put(memory,ST,count+1);result=int(count<v.get('receiveCount',0))
    elif target==0x20a8c00:
        if a[2:4]!=[512,0]or word(memory,a[5])!=8:raise ValueError('Original recvfrom fixed ABI differs')
        raw=bytes.fromhex('fdfe1e6600000000');memory.write(a[1],raw);memory.write(a[4],bytes.fromhex('0802341204030201'));put(memory,a[5],8);normalized=[a[0],a[1],a[2],a[3],8];result=v.get('receiveResult',8)
    elif target==0x20b70c8:
        normalized=[a[0],a[1],peer(memory,a[2])]
        if v.get('receiveAction')=='cancel':put(memory,N+16,4)
        if v.get('receiveAction')=='close':put(memory,N,0xffffffff)
    elif target==0x20a8ef8:
        count=word(memory,ST+4);put(memory,ST+4,count+1);times=v.get('times',[v.get('now',101)]);result=times[min(count,len(times)-1)]
    elif target==0x20b67e0:
        normalized=[a[0],a[1],a[2],peer(memory,a[3])]
        if v.get('reportState')is not None:put(memory,N+16,v['reportState'])
    elif target==0x20b69e4:
        if v.get('markSent'):memory.write(N+55,b'\1')
    elif target==0x20b6c90:put(memory,N,0xffffffff);put(memory,N+16,4)
    elif target==0x20b6eac:
        if v.get('ackState')is not None:put(memory,N+16,v['ackState'])
    elif target==PROGRESS:
        if v.get('progressState')is not None:put(memory,N+16,v['progressState'])
    elif target==COMPLETE:normalized=[a[0],a[1],peer(memory,a[2]),a[3]]
    else:raise ValueError(('Unqualified NAT caller contract',hex(target)))
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[];contract='void';result=0
    def call(target,*arguments):
        value,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return value
    state=lambda:signed(word(memory,N+16))
    if address==0x20b6670:
        memory.write(TMP+1,b'\2');memory.write(TMP+2,args[2].to_bytes(2,'big'));put(memory,TMP+4,args[1]);call(0x20a8c34,args[0]&0xffffffff,args[3],args[4]&0xffffffff,0,TMP,8)
    elif address==0x20b6b74:
        contract='word';host=O
        if args[0]==0:call(0x20061ac,TMP,64,MAGIC,GAME,D);host=TMP
        result=call(0x20b6b4c,host)
    elif address==0x20b6c90:
        neg=call(0x20b6564,args[0]&0xffffffff)
        if neg:
            if word(memory,neg)!=0xffffffff:call(0x20a8b6c,word(memory,neg))
            put(memory,neg,0xffffffff);put(memory,neg+16,4)
    elif address==0x20b6f3c:
        finished=v.get('finished',0)
        if finished==0:call(0x20b6eac,N,S)
        if state()<2:
            if finished!=0:call(0x20b67e0,N,1 if finished==1 else 2 if finished==2 else 4,0xffffffff,0)
            else:
                put(memory,N+48,word(memory,P+12));put(memory,N+52,int.from_bytes(memory.read(P+16,2),'big'),2);put(memory,N+36,0);put(memory,N+16,2);call(PROGRESS,2,word(memory,N+64));call(0x20b69e4,N)
    elif address==0x20b6fa8:
        if state()>=2:
            put(memory,N+48,word(memory,S+4));put(memory,N+52,int.from_bytes(memory.read(S+2,2),'big'),2);memory.write(N+54,b'\1')
            if not v.get('gotData',1):call(0x20b69e4,N)
            elif state()==2:
                if memory.read(N+55,1)==b'\0':call(0x20b69e4,N)
                put(memory,N+16,3);put(memory,N+44,call(0x20a8ef8)+5000)
            elif not v.get('finished',0):call(0x20b69e4,N)
    elif address==0x20b6cb4:
        if word(memory,G+28):put(memory,G+28,call(0x20b6aa8,10));put(memory,G+28,call(0x20b6aa8,11))
        if args[0]and state()==4:call(0x20b65f8,N)
        elif args[0]:
            if word(memory,N)!=0xffffffff:
                put(memory,TMP+16,8)
                while call(0x20a8d88,word(memory,N)):
                    error=call(0x20a8c00,word(memory,N),DI,512,0,TMP,TMP+16)
                    if error==0xffffffff:break
                    call(0x20b70c8,DI,error,TMP)
                    if state()==4 or word(memory,N)==0xffffffff:break
            if state()in [0,2]and call(0x20a8ef8)>word(memory,N+44):
                if signed(word(memory,N+36))>signed(word(memory,N+40)):call(0x20b67e0,N,2 if state()==0 else 3,0xffffffff,0)
                else:put(memory,N+36,word(memory,N+36)+1);call(0x20b6840 if state()==0 else 0x20b69e4,N)
            if state()==3 and call(0x20a8ef8)>word(memory,N+44):
                memory.write(TMP+1,b'\2');memory.write(TMP+2,half(memory,N+52).to_bytes(2,'big'));put(memory,TMP+4,word(memory,N+48));call(0x20b67e0,N,0,word(memory,N)if word(memory,N+4)==0xffffffff else word(memory,N+4),TMP)
            if state()==1 and call(0x20a8ef8)>word(memory,N+44):call(0x20b67e0,N,1,0xffffffff,0)
            if state()==5 and call(0x20a8ef8)>word(memory,N+44):
                if signed(word(memory,N+36))>signed(word(memory,N+40)):
                    call(COMPLETE,word(memory,N+68),word(memory,N+72),N+76,word(memory,N+64))
                    if word(memory,N+4)==0xffffffff:put(memory,N,0xffffffff)
                    call(0x20b6c90,word(memory,N+8))
                else:call(0x20b6708,N);put(memory,N+36,word(memory,N+36)+1);put(memory,N+44,call(0x20a8ef8)+1000)
    else:raise ValueError('Caller outside eleventh source scope')
    return {at:bytes(raw)for at,raw in memory.regions.items()if at!=SP-0x1000},calls,contract,result


def cases(address):
    if address==0x20b6670:return[dict(socket=s,port=p,length=n)for s in [-1,0,7]for p in [0,1,0x80ff,65535]for n in [0,1,8,-1]]
    if address==0x20b6b74:return[dict(useDefault=d,game=g,default=h,resolved=r)for d in [False,True]for g in ['','dqm','g'*50]for h in ['','nat.example','n'*90]for r in [0,0x12345678,0xffffffff]]
    if address==0x20b6c90:return[dict(found=f,socket=s,cookie=c)for f in [False,True]for s in [-1,0,7]for c in [0,0x10203040,0xffffffff]]
    if address==0x20b6f3c:return[dict(state=s,finished=f,mode=m,ackState=a,progressState=p)for s in [-1,0,1,2,3,4]for f in [0,1,2,3,255]for m in ['arm','thumb','mixed']for a,p in [(None,None),(4,None),(None,4)]]
    if address==0x20b6fa8:return[dict(state=s,gotData=g,finished=f,sentRemote=t,now=n,markSent=b)for s in [-1,0,1,2,3,4,5]for g in [0,1,255]for f in [0,1]for t in [0,1]for n in [0,0xfffffff0]for b in [False,True]]
    if address==0x20b6cb4:
        vectors=[dict(state=s,retryTime=t,now=n,retryCount=c,maxRetry=1,gameSocket=g,mode=m)for s in [-1,0,1,2,3,4,5,6]for t,n in [(100,99),(100,100),(100,101),(0xfffffff0,0)]for c in [0,1,2]for g in [-1,7]for m in ['arm','thumb','mixed']]
        vectors +=[dict(null=z,active=a,activeFirst=f,activeSecond=b,state=6)for z in [False,True]for a in [0,1,0xffffffff]for f,b in [(0,0),(0,1),(1,0),(0x80000000,2)]]
        vectors +=[dict(state=s,socket=7,receiveCount=n,receiveResult=r,receiveAction=a,now=101)for s in [0,2,5]for n in [0,1,2]for r in [-2,-1,0,8]for a in ['', 'cancel','close']]
        vectors +=[dict(state=state,retryCount=2,now=101,reportState=5,times=[101,102,105],mode='mixed')for state in [0,1,2,3]]
        return vectors
    raise ValueError('No eleventh source vectors')
