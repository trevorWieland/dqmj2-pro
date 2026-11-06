from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eleventh_models import N,P,S,ST,SP,STOP,TMP,PROGRESS,COMPLETE,dynamic_callbacks,cstring,effect as shared_effect

G,GAME,MAGIC=0x21d2bc4,0x21d23f0,0x20e1738
ARITY={0x20b66a4:0,0x201d6b8:2,0x201d69c:1,0x20b6670:5,0x20b66e0:1,0x20a8ef8:0,0x20b6c90:1,PROGRESS:2,COMPLETE:4}


def initial(address,v):
    memory=Memory({N:bytes(84),P:bytes(80),S:bytes.fromhex('0802341204030201'),ST:bytes(64),G:bytes(44),GAME:bytes(64),MAGIC:bytes.fromhex('fdfc1e666ab2'),SP-0x1000:bytes(0x1000)})
    for offset,value in [(0,7),(4,v.get('gameSocket',-1)),(8,v.get('cookie',0x12345678)),(12,v.get('clientIndex',1)),(16,v.get('state',0)),(36,9),(40,2),(44,77),(64,0x89abcdef),(68,3),(72,27)]:put(memory,N+offset,value)
    memory.write(N+76,bytes.fromhex('0802ff8004030201'))
    for callback,binding in dynamic_callbacks(v).items():put(memory,N+(56 if callback==PROGRESS else 60),callback|(1 if binding['mode']=='thumb'else 0))
    for index in range(4):put(memory,N+20+4*index,v.get('ackValue',1)if v.get('ackMask',0)&(1<<index)else 0)
    for offset,value in [(40,0x01020304),(36,0x11223344),(32,0x89abcdef)]:put(memory,G+offset,value)
    memory.write(GAME,v.get('game','dqm').encode()+b'\0');memory.write(P+7,bytes([v.get('packetType',1)]));memory.write(P+12,bytes([v.get('portType',0)]))
    return memory,[N]if address==0x20b6840 else[N,P,S]


def effect(target,args,memory,v):
    if target==0x20b66a4:
        count=word(memory,ST+8);put(memory,ST+8,count+1);values=v.get('ips',[0x0100007f]*4);return values[min(count,len(values)-1)],[]
    if target==0x20b66e0:
        count=word(memory,ST+12);put(memory,ST+12,count+1);values=v.get('ports',[0x3412,0x3412]);return values[min(count,len(values)-1)],[args[0]]
    if target==0x201d6b8:
        raw=cstring(memory,args[1]);memory.write(args[0],raw+b'\0');return args[0],[raw.hex()]
    if target==0x201d69c:
        raw=cstring(memory,args[0]);return len(raw),[raw.hex()]
    if target==0x20b6670:
        return 0x12345678,[args[0],args[1],args[2],memory.read(args[3],args[4]).hex(),args[4]]
    return shared_effect(target,args,memory,v)


def model(address,v):
    memory,args=initial(address,v);calls=[]
    def call(target,*arguments):
        result,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return result
    if address==0x20b6840:
        memory.write(TMP,bytes.fromhex('fdfc1e666ab20300'));memory.write(TMP+8,word(memory,N+8).to_bytes(4,'big'));memory.write(TMP+13,bytes([word(memory,N+12)&255]));use=int(word(memory,N+4)!=0xffffffff);memory.write(TMP+14,bytes([use]))
        ips=[call(0x20b66a4)for unused in range(4)]
        local=((ips[0]<<24)&0xff000000)|((ips[1]<<8)&0xff0000)|((ips[2]>>24)&255)|((ips[3]>>8)&0xff00)
        memory.write(TMP+15,local.to_bytes(4,'big'));memory.write(TMP+19,b'\0\0');call(0x201d6b8,TMP+21,GAME);length=21+call(0x201d69c,GAME)+1
        def send(kind,socket,ip):memory.write(TMP+12,bytes([kind]));call(0x20b6670,socket,ip,27901,TMP,length)
        if use and word(memory,N+20)==0:send(0,word(memory,N+4),word(memory,G+40))
        if word(memory,N+24)==0:send(1,word(memory,N),word(memory,G+40))
        socket=word(memory,N+4)if use else word(memory,N);first=call(0x20b66e0,socket);second=call(0x20b66e0,socket)
        port=((first>>8)&255)|((second<<8)&0xff00);memory.write(TMP+19,port.to_bytes(2,'big'))
        if word(memory,N+28)==0:send(2,word(memory,N),word(memory,G+36))
        if word(memory,N+32)==0:send(3,word(memory,N),word(memory,G+32))
        put(memory,N+44,call(0x20a8ef8)+500);put(memory,N+40,10)
    elif address==0x20b7014:
        kind=v.get('packetType',1)
        if kind==1:
            port=v.get('portType',0)
            if port<=3:
                put(memory,N+20+4*port,1)
                ready=all(word(memory,N+4*i)!=0 for i in [6,7,8])and(word(memory,N+4)==0xffffffff or word(memory,N+20)!=0)
                if word(memory,N+16)==0 and ready:put(memory,N+16,1);put(memory,N+44,call(0x20a8ef8)+10000);call(PROGRESS,1,word(memory,N+64))
        elif kind==2:
            memory.write(P+7,b'\3');call(0x20b6670,word(memory,N),word(memory,S+4),int.from_bytes(memory.read(S+2,2),'big'),P,21)
        elif kind==14:
            put(memory,N+16,6);call(COMPLETE,word(memory,N+68),word(memory,N+72),N+76,word(memory,N+64))
            if word(memory,N+4)==0xffffffff:put(memory,N,0xffffffff)
            call(0x20b6c90,word(memory,N+8))
    else:raise ValueError('Caller outside twelfth source scope')
    return {at:bytes(raw)for at,raw in memory.regions.items()if at!=SP-0x1000},calls,'void',0


def cases(address):
    if address==0x20b6840:
        vectors=[dict(ackMask=mask,gameSocket=socket,ports=port,now=0xfffffff0,cookie=[0,0x12345678,0xffffffff][mask%3])for mask in range(16)for socket in [-1,27]for port in [[0,0],[0x3412,0x3412],[0x12ab,0xcd34]]]
        vectors +=[dict(ackMask=0,gameSocket=27,ips=ips,ports=port,cookie=cookie,clientIndex=index,game=game)for ips in [[0]*4,[0xffffffff]*4,[0x11223344,0x55667788,0x99aabbcc,0xddeeff00]]for port in [[0xffff,0xffff],[0xabcd,0x1234]]for cookie in [0,0xffffffff]for index in [-1,0,258]for game in ['', 'dqm','g'*63]]
        return vectors
    if address==0x20b7014:
        vectors=[dict(packetType=1,state=state,portType=port,ackMask=mask,gameSocket=socket,mode=mode)for state in [0,2]for port in [0,1,2,3,4,255]for mask in [0,14,15]for socket in [-1,27]for mode in ['arm','thumb','mixed']]
        vectors +=[dict(packetType=kind,state=state,gameSocket=socket,mode=mode)for kind in [0,2,14,255]for state in [-1,0,1,2,4,5,6]for socket in [-1,27]for mode in ['arm','thumb','mixed']]
        vectors +=[dict(packetType=1,state=0,portType=1,ackMask=15,now=now,progressState=state,mode='mixed')for now in [0,0xfffffff0,0xffffffff]for state in [None,4]]
        return vectors
    raise ValueError('No twelfth vectors')
