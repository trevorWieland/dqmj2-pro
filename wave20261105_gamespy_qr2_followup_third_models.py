from wave20261105_gamespy_qr2_next_first_models import Memory,word,put

GP1,GP2,KINFO=0x21d3020,0x21d3028,0x20e33e4
C1,C2,S1,S2,ST=0x2170000,0x2171000,0x2174000,0x2176000,0x2179000
VALUE,CONFIG,EMPTY=0x20e2b78,0x20e2b7c,0x20e2c44
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
ARITY={0x2008d78:3,0x2006dfc:3,0x2007074:1,0x2019d20:3,0x2006b74:1,0x20065f0:6,0x2006ab0:2,0x200708c:1,0x2007110:1,0x20b90ec:1}
HANDLERS={1:0x20b9328,2:0x20b9364,3:0x20b9404,4:0x20b94b0,5:0x20b95d8,6:0x20b9650,7:0x20b97bc}
ARITY.update({at:0 for at in HANDLERS.values()})
OBSERVED={S1,S1+4,S2,S2+4}


def dynamic_callbacks(v):return {}
def group(address):return (GP1,C1,C2)if address==0x20b86cc else(GP2,S1,S2)
def toggle(m,gp,a,b):put(m,gp,b if word(m,gp)==a else a)
def maybe(m,v,key):
    if v.get(key):toggle(m,*group(v['_address']))


def initial(address,v):
    m=Memory({GP1:bytes(4),GP2:bytes(4),KINFO:bytes(8),C1:bytes([0xa5])*4096,C2:bytes([0x5a])*4096,S1:bytes([0x33])*8192,S2:bytes([0xcc])*8192,ST:bytes(16),VALUE:(0x20e2b94).to_bytes(4,'little'),CONFIG:(0x20e2b80).to_bytes(4,'little'),EMPTY:bytes([0]),SP-0x1000:bytes(0x1000)})
    put(m,GP1,C1);put(m,GP2,0 if v.get('null')else S1);put(m,KINFO+4,v.get('currentThread',0x2181000))
    for at,status in [(S1,v.get('status',1)),(S2,v.get('alternateStatus',2))]:put(m,at,v.get('phase',3));put(m,at+4,status)
    v['_address']=address
    if address==0x20b86cc:return m,[C1]
    if address==0x20b8e74:return m,[S1,v.get('alloc',0x2230001),v.get('free',0x2230100)]
    if address in [0x20b8f64,0x20b90bc,0x20b90ec]:return m,[v.get('value',0x12345678)]
    if address==0x20b92b4:return m,[v.get('threadArgument',0xdeadbeef)]
    raise ValueError('Outside initialized-state subset')


def effect(at,a,m,v):
    result=0x76543210;norm=a[:];address=v['_address']
    if at==0x2008d78:m.write(a[0],bytes([a[1]&255])*a[2]);maybe(m,v,'fillSwitch')
    elif at==0x2006dfc:
        m.write(a[0],bytes(32));put(m,a[0]+16,a[1]);put(m,a[0]+20,a[2]);maybe(m,v,'queueSwitch')
    elif at==0x2007074:
        index=word(m,ST+4);put(m,ST+4,index+1);m.write(a[0],bytes(24));maybe(m,v,'firstMutexSwitch'if index==0 else'secondMutexSwitch')
    elif at==0x2019d20:
        raw=bytearray();ended=False
        for i in range(a[2]):
            byte=0 if ended else m.read(a[1]+i,1)[0];raw.append(byte);ended=ended or byte==0
        m.write(a[0],bytes(raw));norm=[a[0],a[1],a[2]];result=a[0];maybe(m,v,'copySwitch')
    elif at==0x2006b74:
        result=v.get('priority',5);maybe(m,v,'prioritySwitch')
        if v.get('kernelMutation'):put(m,KINFO+4,0xffffffff)
    elif at==0x20065f0:maybe(m,v,'createSwitch')
    elif at==0x2006ab0:pass
    elif at==0x200708c:maybe(m,v,'lockSwitch')
    elif at==0x2007110:maybe(m,v,'unlockSwitch')
    elif at==0x20b90ec:
        maybe(m,v,'workerSwitch');put(m,word(m,GP2),a[0]);put(m,ST,0)
    elif at in HANDLERS.values():
        phases=v.get('phases',[1,0]);index=word(m,ST)+1;put(m,ST,index)
        if index>=len(phases):raise ValueError('Finite phase-provider progression exhausted')
        maybe(m,v,'handlerSwitch');put(m,word(m,GP2),phases[index])
    else:raise ValueError(('Unqualified initialized-state helper',hex(at)))
    return result&0xffffffff,norm


def model(address,v):
    m,args=initial(address,v);calls=[]
    def call(at,a):
        result,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return result
    if address==0x20b86cc:
        put(m,GP1,C1);call(0x2008d78,[C1,0,2292]);base=word(m,GP1);call(0x2006dfc,[base,base+32,1]);put(m,word(m,GP1)+36,0);captured=word(m,GP1);priority=call(0x2006b74,[word(m,KINFO+4)]);call(0x20065f0,[captured+52,0x20b87e5,0,captured+2292,2048,priority]);call(0x2006ab0,[word(m,GP1)+52,128])
    elif address==0x20b8e74:
        put(m,GP2,S1);call(0x2008d78,[S1,0,4816]);put(m,word(m,GP2),0);put(m,word(m,GP2)+4,0);call(0x2007074,[word(m,GP2)+8]);put(m,word(m,GP2)+40,args[1]);put(m,word(m,GP2)+44,args[2]);call(0x2019d20,[word(m,GP2)+56,EMPTY,5]);put(m,word(m,GP2)+52,0);put(m,word(m,GP2)+64,0);put(m,word(m,GP2)+440,-59);put(m,word(m,GP2)+2516,word(m,VALUE));put(m,word(m,GP2)+2536,CONFIG);put(m,word(m,GP2)+2540,1);put(m,word(m,GP2)+2532,0x20b9909);call(0x2007074,[word(m,GP2)+444]);pair=word(m,GP2)+2564;put(m,pair+4,0);put(m,pair,0);captured=word(m,GP2);priority=call(0x2006b74,[word(m,KINFO+4)]);call(0x20065f0,[captured+2576,0x20b92b5,0,captured+4816,2048,priority]);call(0x2006ab0,[word(m,GP2)+2576,128])
    elif address==0x20b8f64:
        if word(m,GP2):put(m,word(m,GP2)+48,args[0])
    elif address==0x20b90bc:
        if word(m,GP2):
            call(0x200708c,[word(m,GP2)+8])
            if word(m,word(m,GP2)+4)!=2:put(m,word(m,GP2)+4,args[0])
            call(0x2007110,[word(m,GP2)+8])
    elif address==0x20b90ec:
        if word(m,GP2):put(m,word(m,GP2),args[0])
    elif address==0x20b92b4:
        if word(m,GP2):
            call(0x20b90ec,[1])
            while word(m,word(m,GP2)):
                phase=word(m,word(m,GP2))
                if phase not in HANDLERS:raise ValueError('Unknown/default phase has no supplied termination proof')
                call(HANDLERS[phase],[])
    else:raise ValueError('No initialized-state model')
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'void',0


def expected_reads(address,v):
    if v.get('null')or address in [0x20b86cc,0x20b8e74,0x20b8f64]:return []
    if address==0x20b90ec:return [(S1,4,v.get('phase',3)&0xffffffff)]
    if address==0x20b90bc:
        at=S2 if v.get('lockSwitch')else S1
        return [(S1+4,4,v.get('status',1)&0xffffffff),(at+4,4,v.get('alternateStatus',2)if at==S2 else v.get('status',1))]
    if address==0x20b92b4:
        at=S2 if v.get('workerSwitch')else S1;out=[]
        for phase in v.get('phases',[1,0]):
            out.append((at,4,phase))
            if not phase:break
            out.append((at,4,phase))
            if v.get('handlerSwitch'):at=S1 if at==S2 else S2
        return out
    raise ValueError('Unqualified measured shared-word read oracle')


def cases(address):
    if address==0x20b86cc:
        return [dict(priority=p,currentThread=t,**flags)for p in [0,5,31,0xffffffff]for t in [0x2181000,0xffffffff]for flags in [{},{'fillSwitch':True},{'queueSwitch':True},{'prioritySwitch':True,'kernelMutation':True},{'createSwitch':True},{'fillSwitch':True,'queueSwitch':True,'prioritySwitch':True,'createSwitch':True}]]
    if address==0x20b8e74:
        return [dict(priority=p,alloc=a,free=f,**flags)for p in [0,31,0xffffffff]for a,f in [(0,0),(0x2230001,0x2230100)]for flags in [{},{'fillSwitch':True},{'firstMutexSwitch':True},{'copySwitch':True},{'secondMutexSwitch':True},{'prioritySwitch':True,'kernelMutation':True},{'createSwitch':True},{'fillSwitch':True,'firstMutexSwitch':True,'copySwitch':True,'secondMutexSwitch':True,'prioritySwitch':True,'createSwitch':True}]]
    if address==0x20b8f64:return [dict(null=n,value=v)for n in [False,True]for v in [0,1,0x80000000,0xffffffff]]
    if address==0x20b90bc:return [dict(null=n,status=s,alternateStatus=a,value=v,lockSwitch=ls,unlockSwitch=us)for n in [False,True]for s,a in [(0,2),(2,1),(0xffffffff,0)]for v in [0,2,0x80000000]for ls,us in [(False,False),(True,False),(True,True)]]
    if address==0x20b90ec:return [dict(null=n,phase=p,value=v)for n in [False,True]for p in [0,3,0xffffffff]for v in [0,1,0x80000000,0xffffffff]]
    if address==0x20b92b4:return [dict(null=n,phases=seq,workerSwitch=ws,handlerSwitch=hs)for n in [False,True]for seq in [[1,0],[1,2,3,4,5,6,7,0],[1,7,1,4,0]]for ws in [False,True]for hs in [False,True]]
    raise ValueError('No initialized-state vectors')
