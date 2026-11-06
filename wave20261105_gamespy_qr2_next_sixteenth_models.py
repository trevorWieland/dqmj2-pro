from wave20261105_gamespy_qr2_next_first_models import Memory,word,put

N,G=0x2170000,0x21d23ec
SP,STOP,MAGIC=0x2701000,0x27e0000,0
ARITY={0x20b6b9c:0,0x20b65a4:0,0x20a8b5c:3,0x20b65f8:1,0x20b6840:1}


def initial(address,v):
    if address!=0x20b6c08:raise ValueError('Caller outside sixteenth scope')
    memory=Memory({N:bytes([0xa5])*84,G:bytes(4),SP-0x1000:bytes(0x1000)})
    put(memory,G,v.get('available',1))
    return memory,[v.get('gameSocket',27),v.get('cookie',0x12345678),v.get('clientIndex',1),v.get('progress',0x12345678),v.get('completed',0x89abcdef),v.get('userdata',0x11223344)]


def effect(target,args,memory,v):
    normalized=[a&0xffffffff for a in args];result=0x12345678
    if target==0x20b6b9c:result=v.get('resolve',1)
    elif target==0x20b65a4:result=N if v.get('allocate',True)else 0
    elif target==0x20a8b5c:result=v.get('socketResult',7)
    elif target==0x20b65f8:pass
    elif target==0x20b6840:put(memory,N+44,0x55667788);put(memory,N+40,10)
    else:raise ValueError('Unqualified six-word constructor import')
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[];result=2
    def call(target,*arguments):
        value,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return value
    if word(memory,G)==1:
        if call(0x20b6b9c)==0:result=3
        elif call(0x20b65a4)==0:result=1
        else:
            for offset,value in [(4,args[0]),(12,args[2]),(8,args[1]),(56,args[3]),(60,args[4]),(64,args[5])]:put(memory,N+offset,value)
            socket=call(0x20a8b5c,2,2,0);put(memory,N,socket)
            for offset,value in [(36,0),(48,0),(40,0),(68,5)]:put(memory,N+offset,value)
            memory.write(N+54,b'\0\0');put(memory,N+52,0,2)
            if socket==0xffffffff:call(0x20b65f8,N);result=2
            else:call(0x20b6840,N);result=0
    return{at:bytes(raw)for at,raw in memory.regions.items()if at!=SP-0x1000},calls,'word',result


def cases(address):
    if address!=0x20b6c08:raise ValueError('No sixteenth constructor vectors')
    vectors=[dict(available=value)for value in [0,2,0xffffffff]]+[dict(resolve=0),dict(allocate=False)]
    vectors +=[dict(socketResult=socket,progress=p,completed=c,userdata=u,cookie=k,clientIndex=i,gameSocket=g)for socket in [-1,-2,0,7]for p,c in [(0,0),(0x27e0100,0x27e0141),(0x27e0101,0x27e0140),(0xffffffff,0x80000000)]for u in [0,0x11223344]for k in [0,0xffffffff]for i in [-1,0,258]for g in [-1,0,27]]
    vectors +=[dict(resolve=0x80000000,userdata=0xffffffff,progress=0x27e0101,completed=0x27e0140)]
    return vectors
