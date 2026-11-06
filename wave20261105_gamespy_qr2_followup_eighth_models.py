from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
GP,C,C2,A,A2,B,ST=0x21d3020,0x2170000,0x2171000,0x2174000,0x2174100,0x2178000,0x217f000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
OBSERVED=set()
ARITY={0x20b8ccc:2,0x20b8d44:1,0x20b8dc4:1,0x20b8d80:0,0x20b8da0:0,0x2008e0c:3}
INFO={0x20b8958:(24,219,0x20b88fd),0x20b8ab0:(16,206,0x20b8dd9),0x20b8b0c:(16,203,0x20b8dd9),0x20b8b5c:(20,208,0x20b8dd9),0x20b8bc4:(20,218,0x20b8dfd),0x20b8c2c:(16,210,0x20b8dfd),0x20b8c7c:(16,209,0x20b8dd9)}


def dynamic_callbacks(v):return {}
def active(m):return word(m,word(m,GP)+36)
def toggle(m):put(m,GP,C2 if word(m,GP)==C else C)
def buffer(address):return SP-(1064 if address==0x20b89b4 else 1056 if address in [0x20b8b5c,0x20b8bc4]else 1048)
def initial(address,v):
    m=Memory({GP:bytes(4),C:bytes([0x33])*2292,C2:bytes([0xcc])*2292,A:bytes(40),A2:bytes(40),B:bytes((i*17+5)&255 for i in range(8192)),ST:bytes(64),SP-0x1000:bytes(0x1000)})
    put(m,GP,C)
    for control,request in [(C,A),(C2,A2)]:
        put(m,control+36,request);put(m,control+44,0);put(m,control+48,v.get('scratch',1))
        for off,val in [(4,v.get('id',0x11223344)),(8,v.get('kind',0x55)),(12,B),(16,v.get('rawWord',0xabcdef98)),(20,v.get('length',1025)),(24,0x77112233),(32,1),(36,v.get('oldWord9',0x44444444))]:put(m,request+off,val)
    return m,[]


def effect(at,a,m,v):
    result=0x76543210;norm=a[:]
    if at==0x20b8ccc:
        m.write(a[1],bytes([0xa6])*20)
        if v.get('constructorSwitch'):toggle(m)
        put(m,word(m,GP)+48,v.get('scratch',1))
    elif at==0x20b8d44:
        result=v.get('registerResult',1)
        if v.get('registerSwitch'):toggle(m)
    elif at==0x20b8dc4:
        length=word(m,a[0])
        if not 16<=length<=1044:raise ValueError('Outside defined message-header/payload read contract')
        norm=a+[length,m.read(a[0],length).hex()];index=word(m,ST);put(m,ST,index+1);result=0 if index==v.get('sendFailsAt',-1)else 1
        if v.get('sendSwitch'):toggle(m)
    elif at==0x20b8d80:
        if v.get('waitSwitch'):toggle(m)
        put(m,active(m)+36,v.get('returnedWord',v.get('length',1025)))
    elif at==0x20b8da0:
        put(m,ST+4,word(m,ST+4)+1)
        if v.get('cleanupNulls'):put(m,GP,0)
    elif at==0x2008e0c:
        raw=m.read(a[0],a[2]);m.write(a[1],raw);norm=a+[raw.hex()]
        if v.get('copySwitch'):toggle(m)
    else:raise ValueError(('Outside message provider namespace',hex(at)))
    return result&0xffffffff,norm


def evaluate(address,v):
    m,args=initial(address,v);calls=[];p=buffer(address)
    def call(at,a):
        value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
    def header(length,code,param0,param1=None):
        for i,val in enumerate([length,0x44535359,code,param0]):put(m,p+4*i,val)
        if param1 is not None:put(m,p+16,param1)
    if address==0x20b89b4:
        sent=word(m,active(m)+20);source=word(m,active(m)+12);sent=min(sent,1024)
        header(sent+20,205,word(m,active(m)+4),word(m,active(m)+20));call(0x2008e0c,[source,p+20,sent])
        if call(0x20b8d44,[0x20b8dd9])and call(0x20b8dc4,[p]):
            last=1
            for count in range(16):
                if sent>=word(m,active(m)+20):break
                last=1;size=word(m,active(m)+20)-sent
                if size>1024:size=1024;last=0
                header(size+20,207,0 if last else 1,size);call(0x2008e0c,[source+sent,p+20,size])
                if not call(0x20b8dc4,[p]):break
                sent+=size;put(m,active(m)+24,sent)
            else:raise ValueError('Outside finite chunk model')
            if last:
                call(0x20b8d80,[])
                if sent!=word(m,active(m)+36):put(m,active(m)+32,0)
        call(0x20b8da0,[])
    elif address in INFO:
        length,code,callback=INFO[address]
        special=address in [0x20b8b5c,0x20b8bc4]
        if special:call(0x20b8ccc,[word(m,active(m)+8),p])
        param=word(m,word(m,GP)+48)if special else word(m,active(m)+16)if address==0x20b8958 else None
        header(length,code,word(m,active(m)+4),param)
        if address==0x20b8958:put(m,p+20,word(m,active(m)+20))
        if not special or param:
            if call(0x20b8d44,[callback])and call(0x20b8dc4,[p]):
                call(0x20b8d80,[])
                if address==0x20b8ab0:put(m,active(m)+36,0)
            call(0x20b8da0,[])
    else:raise ValueError('Outside message caller scope')
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'void',0


def model(address,v):return evaluate(address,v)
def expected_reads(address,v):return []
def cases(address):
    if address==0x20b89b4:
        rows=[dict(length=n,sendFailsAt=f)for n in [0,1,1023,1024,1025,2048,2049,3072,3073]for f in [-1,0,1,2,3]]
        rows +=[dict(length=n,registerResult=0)for n in [0,1024,1025,3073]]
        rows +=[dict(length=n,returnedWord=r)for n in [0,1024,1025,2049]for r in [0,1,0x80000000,0xffffffff]]
        rows +=[dict(length=3073,**flags)for flags in [{'copySwitch':True},{'registerSwitch':True},{'sendSwitch':True},{'waitSwitch':True},{'cleanupNulls':True},{'copySwitch':True,'registerSwitch':True,'sendSwitch':True,'waitSwitch':True,'cleanupNulls':True}]]
        return rows
    rows=[dict(registerResult=r,sendFailsAt=f,scratch=s)for r in [0,1,0xffffffff]for f in [-1,0]for s in [0,1,0x80000000,0xffffffff]]
    rows +=[dict(id=0,kind=0x80000000,rawWord=0xffffffff,oldWord9=0,**flags)for flags in [{'constructorSwitch':True},{'registerSwitch':True},{'sendSwitch':True},{'waitSwitch':True},{'cleanupNulls':True},{'constructorSwitch':True,'registerSwitch':True,'sendSwitch':True,'waitSwitch':True,'cleanupNulls':True}]]
    return rows
