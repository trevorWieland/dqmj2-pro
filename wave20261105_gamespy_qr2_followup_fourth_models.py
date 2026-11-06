from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32

GP,SGP,ERR=0x21d3028,0x21d3030,0x21d3038
S1,S2,P1,P2,BUF=0x2174000,0x2176000,0x217a000,0x217a100,0x217c000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
ARM_CB,THUMB_CB=0x2231000,0x2231004
OBSERVED={S1+440,S2+440}
ARITY={0x20b90bc:1,0x200708c:1,0x209045c:2,0x2007110:1,0x20b9d08:2,0x209a9d0:0,0x20b8748:0,0x20b8f8c:0,0x20b9c2c:0,0x209aa64:3,0x20b9c74:2,0x2008d78:3,0x20b8780:1,ARM_CB:1,THUMB_CB:1}
BUILDERS={0x20b9ab4,0x20b9b24,0x20b9b90}
WORDS={0x20b8fd8,0x20b9a98,0x20b9bf4,0x20b9a48,0x20b9c74,*BUILDERS}


def dynamic_callbacks(v):return {ARM_CB:dict(mode='arm'),THUMB_CB:dict(mode='thumb')}
def cb(v):return [0,ARM_CB,THUMB_CB|1][v.get('callback',0)]
def toggle(m,gp,a,b):put(m,gp,b if word(m,gp)==a else a)
def switch_status(m,v,key):
    if v.get(key):toggle(m,SGP,P1,P2)


def initial(address,v):
    m=Memory({GP:bytes(4),SGP:bytes(4),ERR:bytes(8),S1:bytes([0x33])*8192,S2:bytes([0xcc])*8192,P1:bytes([0xa5])*128,P2:bytes([0x5a])*128,BUF:bytes(64),SP-0x1000:bytes(0x1000)})
    put(m,GP,0 if v.get('nullState')else S1);put(m,SGP,0 if v.get('nullStatus')else P1)
    for s,status,error in [(S1,v.get('stateStatus',1),v.get('error',7)),(S2,v.get('alternateStatus',2),v.get('alternateError',-59))]:put(m,s+4,status);put(m,s+440,error)
    for p in [P1,P2]:
        for off,value in [(0,v.get('phase',2)),(16,v.get('busy',0)),(44,v.get('amount',0x12345678)),(48,v.get('marker',0)),(60,cb(v))]:put(m,p+off,value)
    put(m,ERR,v.get('errorCode',8));put(m,ERR+4,v.get('errorDetail',0x89abcdef));v['_address']=address
    if address==0x20b909c:return m,[v.get('a',0x80000001),v.get('b',0xffffffff)]
    if address==0x20b9c4c:return m,[v.get('value',0x12345678)]
    if address==0x20b9c74:return m,[v['mode'],v['id']]
    if address in BUILDERS:return m,[v.get('id',7),v.get('buffer',BUF),v.get('capacity',32),v.get('opaque4',0x2230001),v.get('opaque5',0x87654321)]
    return m,[]


def effect(at,a,m,v):
    result=0x76543210;norm=a[:]
    if at==0x20b90bc:
        if v.get('transitionSwitch'):toggle(m,GP,S1,S2)
        if word(m,GP):
            put(m,word(m,GP)+4,a[0])
            if 'afterTransitionError'in v:put(m,word(m,GP)+440,v['afterTransitionError'])
    elif at==0x200708c:
        if v.get('lockSwitch'):toggle(m,GP,S1,S2)
        if 'afterLockError'in v:put(m,word(m,GP)+440,v['afterLockError'])
    elif at==0x209045c:
        result=v.get('shutdownResult',0xffffffff)
        if v.get('shutdownSwitch'):toggle(m,GP,S1,S2)
    elif at==0x2007110:pass
    elif at==0x20b9d08:
        if v.get('errorSideEffect'):put(m,ERR,0x13572468);put(m,ERR+4,0x24681357)
    elif at in [ARM_CB,THUMB_CB]:switch_status(m,v,'callbackSwitch')
    elif at==0x209a9d0:
        if 'cleanupCode'in v:put(m,ERR,v['cleanupCode'])
    elif at==0x20b8748:result=v.get('firstResult',1);switch_status(m,v,'firstSwitch')
    elif at==0x20b8f8c:result=v.get('secondResult',1);switch_status(m,v,'secondSwitch')
    elif at==0x20b9c2c:result=v.get('size',96);switch_status(m,v,'sizeSwitch')
    elif at==0x209aa64:switch_status(m,v,'freeSwitch')
    elif at==0x20b9c74:result=v.get('validate',1);switch_status(m,v,'validateSwitch')
    elif at==0x2008d78:m.write(a[0],bytes([a[1]&255])*a[2]);switch_status(m,v,'fillSwitch')
    elif at==0x20b8780:
        norm=[a[0],m.read(a[0],40).hex()];result=v.get('send',1)
        for offset in [28,32,36]:put(m,a[0]+offset,0)
        switch_status(m,v,'sendSwitch')
    else:raise ValueError(('Unqualified status/request provider',hex(at)))
    return result&0xffffffff,norm


def evaluate(address,v):
    m,args=initial(address,v);calls=[];reads=[];result=0
    def call(at,a):
        value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
    def observed(at):
        value=word(m,at);reads.append((at,4,value));return value
    if address==0x20b8fd8:
        result=1
        if word(m,GP):
            call(0x20b90bc,[2])
            if s32(observed(word(m,GP)+440))>=0:
                call(0x200708c,[word(m,GP)+444])
                if s32(observed(word(m,GP)+440))>=0:call(0x209045c,[observed(word(m,GP)+440),2])
                call(0x2007110,[word(m,GP)+444])
    elif address==0x20b909c:
        if not word(m,GP)or word(m,word(m,GP)+4)!=2:call(0x20b9d08,args);call(0x20b90bc,[2])
    elif address==0x20b9a98:
        if word(m,SGP)and word(m,word(m,SGP)+48)==0:result=word(m,word(m,SGP)+44)
    elif address==0x20b9bf4:
        if word(m,SGP)and word(m,word(m,SGP))in [2,3]:result=1
    elif address==0x20b9c4c:
        if word(m,SGP):
            put(m,word(m,SGP)+4,args[0]);callback=word(m,word(m,SGP)+60)
            if callback:call(callback&~1,args)
            else:call(0x20b9d08,[9,-2])
    elif address==0x20b9cd8:
        call(0x209a9d0,[])
        if word(m,ERR)!=9:put(m,ERR,0);put(m,ERR+4,0)
    elif address==0x20b9a48:
        result=1
        if word(m,SGP):
            put(m,word(m,SGP),3)
            if not call(0x20b8748,[]):result=0
            if not call(0x20b8f8c,[]):result=0
            if result:size=call(0x20b9c2c,[]);call(0x209aa64,[0x53574300,word(m,SGP),size]);put(m,SGP,0)
    elif address==0x20b9c74:
        maximum=255 if v['mode']else 15
        if word(m,SGP)and word(m,word(m,SGP))==2 and word(m,word(m,SGP)+16)==0 and 1<=v['id']&0xffffffff<=maximum:result=1
    elif address in BUILDERS:
        mode=1 if address==0x20b9ab4 else 0
        if call(0x20b9c74,[mode,args[0]]):
            call(0x2008d78,[word(m,SGP)+20,0,40]);put(m,word(m,SGP)+20,3 if address==0x20b9b90 else 2);put(m,word(m,SGP)+24,args[0]+1024 if mode else args[0]);put(m,word(m,SGP)+32,args[1])
            if address!=0x20b9b90:put(m,word(m,SGP)+36,0)
            put(m,word(m,SGP)+40,args[2]);put(m,word(m,SGP)+64,args[3]);put(m,word(m,SGP)+68,args[4])
            if call(0x20b8780,[word(m,SGP)+20]):put(m,word(m,SGP)+16,1);result=1
    else:raise ValueError('Outside status/request caller subset')
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word'if address in WORDS else'void',result,reads


def model(address,v):return evaluate(address,v)[:4]
def expected_reads(address,v):return evaluate(address,v)[4]


def cases(address):
    if address==0x20b8fd8:
        base=[dict(nullState=n,error=e,alternateError=a,transitionSwitch=t,lockSwitch=l,shutdownSwitch=s)for n in [False,True]for e,a in [(-59,7),(0,-1),(7,0x7fffffff),(0x80000000,7)]for t,l,s in [(False,False,False),(True,False,False),(False,True,False),(False,False,True)]]
        return base+[dict(error=7,afterTransitionError=-1),dict(error=7,afterLockError=-1),dict(error=0,afterLockError=0x7fffffff)]
    if address==0x20b909c:return [dict(nullState=n,stateStatus=s,a=a,b=b,errorSideEffect=True,transitionSwitch=t)for n in [False,True]for s in [0,2,0xffffffff]for a,b in [(0,0),(9,0xfffffffe),(0xffffffff,0x80000000)]for t in [False,True]]
    if address==0x20b9a98:return [dict(nullStatus=n,marker=m,amount=a)for n in [False,True]for m in [0,1,0xffffffff]for a in [0,0x80000000,0xffffffff]]
    if address==0x20b9bf4:return [dict(nullStatus=n,phase=p)for n in [False,True]for p in [0,1,2,3,4,0x80000000,0xffffffff]]
    if address==0x20b9c4c:return [dict(nullStatus=n,callback=cb,value=v,callbackSwitch=s,errorSideEffect=True)for n in [False,True]for cb in [0,1,2]for v in [0,0x80000000,0xffffffff]for s in [False,True]]
    if address==0x20b9cd8:return [dict(errorCode=c,errorDetail=d,**mutation)for c in [0,8,9,0xffffffff]for d in [0,0xffffffff]for mutation in [{},{'cleanupCode':9},{'cleanupCode':0xffffffff}]]
    if address==0x20b9a48:return [dict(nullStatus=n,firstResult=a,secondResult=b,size=size,**flags)for n in [False,True]for a,b in [(0,0),(0,1),(1,0),(1,1),(0xffffffff,0x80000000)]for size in [0,96,0xffffffff]for flags in [{},{'firstSwitch':True},{'secondSwitch':True},{'sizeSwitch':True,'freeSwitch':True}]]
    if address==0x20b9c74:return [dict(nullStatus=n,phase=p,busy=busy,mode=mode,id=id)for n in [False,True]for p,busy in [(0,0),(2,0),(2,1),(3,0)]for mode in [0,1,0xffffffff]for id in [0,1,15,16,254,255,256,0xffffffff]]
    if address in BUILDERS:
        rows=[dict(validate=a,send=b,**flags)for a in [0,1,0xffffffff]for b in [0,1,0x80000000]for flags in [{},{'validateSwitch':True},{'fillSwitch':True},{'sendSwitch':True},{'validateSwitch':True,'fillSwitch':True,'sendSwitch':True}]]
        rows +=[dict(**{key:value})for key in ['id','buffer','capacity','opaque4','opaque5']for value in [0,0xffffffff]]
        rows.append(dict(nullStatus=True,validate=0));return rows
    raise ValueError('No status/request vectors')
