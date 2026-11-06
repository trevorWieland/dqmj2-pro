from wave20261105_gamespy_qr2_next_first_models import Memory,word,put

N,S=0x2170000,0x2171000
SP,STOP,MAGIC,CB=0x2701000,0x27e0000,0,0x27e0100
ARITY={0x20b6c90:1,0x20b6708:1,0x20a8ef8:0,CB:4}


def dynamic_callbacks(v):return{CB:dict(mode=v['mode'],kind='function',fixtureOnly=True,runtimeTargetNamespaceUnresolved=True)}


def initial(address,v):
    if address!=0x20b67e0:raise ValueError('Caller outside fifteenth scope')
    memory=Memory({N:bytes(84),S:bytes.fromhex('7f02aa5588776655'),SP-0x1000:bytes(0x1000)})
    for offset,value in [(0,7),(4,0xffffffff),(8,0x11223344),(16,0),(36,7),(40,8),(44,9),(60,CB|(1 if v['mode']=='thumb'else 0)),(64,0x89abcdef),(68,0x55667788),(72,99)]:put(memory,N+offset,value)
    memory.write(N+76,bytes.fromhex('0802beef04030201'))
    return memory,[N,v['result'],v['socket'],S if v['peer']else 0]


def effect(target,args,memory,v):
    a=[x&0xffffffff for x in args];normalized=a[:];result=0x12345678
    if target==CB:
        normalized=[a[0],a[1],a[2],memory.read(a[2],8).hex(),a[3]]
        if v.get('postCookie')is not None:put(memory,N+8,v['postCookie'])
        put(memory,N+16,6)
    elif target==0x20b6c90:put(memory,N,0xffffffff);put(memory,N+16,4)
    elif target==0x20b6708:put(memory,N+36,55);put(memory,N+40,56)
    elif target==0x20a8ef8:result=v['now']
    else:raise ValueError('Unqualified completed-report caller contract')
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[]
    def call(target,*arguments):
        value,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return value
    put(memory,N+68,args[1]);put(memory,N+72,args[2])
    if args[3]:memory.write(N+76,memory.read(S,8))
    if args[1]in [1,2]:put(memory,N+16,3);call(CB,word(memory,N+68),word(memory,N+72),N+76,word(memory,N+64));call(0x20b6c90,word(memory,N+8))
    else:call(0x20b6708,N);put(memory,N+16,5);put(memory,N+44,call(0x20a8ef8)+1000);put(memory,N+36,0);put(memory,N+40,5)
    return{at:bytes(raw)for at,raw in memory.regions.items()if at!=SP-0x1000},calls,'void',0


def cases(address):
    if address!=0x20b67e0:raise ValueError('No fifteenth vectors')
    return[dict(result=r,socket=s,peer=p,mode=m,now=n,postCookie=c)for r in [0,1,2,3,4,0xffffffff]for s in [0xffffffff,0,7,0x80000000]for p in [False,True]for m in ['arm','thumb']for n in [0,0xfffffff0]for c in [None,0xffffffff]]
