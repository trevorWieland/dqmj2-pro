from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32

GP,SGP,S1,S2,P1,P2,HEAP=0x21d3028,0x21d3030,0x2174000,0x2176000,0x217a000,0x217a100,0x2180000
NAME,PEER,HOST,LIST,ADDR,ST=0x217e000,0x217e100,0x217e200,0x217e300,0x217e400,0x217f000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
ARM_CB,THUMB_CB=0x2232000,0x2232004
OBSERVED=set()
ARITY={0x2019d80:1,0x209075c:2,0x200708c:1,0x209046c:1,0x2008e0c:3,0x2007110:1,0x2008360:1,0x2092338:2,0x20b9cf4:0,0x20b9bf4:0,0x20b9d08:2,0x20b8734:0,0x20b8f74:0,0x20b9c2c:0,0x209aa44:3,0x2008d78:3,0x20b8e6c:0,0x20b86c4:0,0x20b86cc:1,0x20b8e74:3,0x20b8f64:1,ARM_CB:3,THUMB_CB:3}
WORDS={0x20b9848,0x20b9868,0x20b9898,0x20b99ec,0x20b9c2c}


def dynamic_callbacks(v):return {ARM_CB:dict(mode='arm'),THUMB_CB:dict(mode='thumb')}
def cb(v):return [0,ARM_CB,THUMB_CB|1][v.get('callback',0)]
def toggle_state(m):put(m,GP,S2 if word(m,GP)==S1 else S1)
def switch_status(m,v,key):
    if v.get(key):put(m,SGP,P2 if word(m,SGP)==P1 else P1)
def align(n):return(((n+31)&0xffffffff)>>5)<<5
def text(v):return bytes.fromhex(v['text'])if 'text'in v else b'example.test'


def initial(address,v):
    m=Memory({GP:bytes(4),SGP:bytes(4),S1:bytes([0x33])*8192,S2:bytes([0xcc])*8192,P1:bytes([0xa5])*128,P2:bytes([0x5a])*128,HEAP:bytes([0x88])*16384,NAME:bytes(128),PEER:bytes([0x77])*16,HOST:bytes(16),LIST:bytes(4),ADDR:bytes.fromhex('11223344aabbccdd'),ST:bytes(64),SP-0x1000:bytes(0x1000)})
    put(m,GP,0 if v.get('nullState')else S1);put(m,SGP,0 if v.get('nullStatus')else P1);put(m,S1,v.get('statePhase',7));put(m,S2,v.get('statePhase',7));m.write(NAME,text(v)+bytes([0]));put(m,HOST+12,LIST);m.write(HOST+8,(2).to_bytes(2,'little')+(v.get('hostLength',4)&65535).to_bytes(2,'little'));put(m,LIST,ADDR)
    for p in [P1,P2]:
        for off,val in [(0,v.get('phase',2)),(4,v.get('storedWord',1)),(8,HEAP+96),(12,HEAP+4928),(16,v.get('busy',1)),(48,v.get('marker',1)),(52,v.get('word0',0x80000001)),(56,v.get('word1',0xffffffff)),(60,v.get('statusHook',0)),(64,cb(v)),(68,v.get('word2',0x12345678))]:put(m,p+off,val)
    v['_address']=address
    if address==0x20b9868:return m,[0 if v.get('nullName')else NAME]
    if address==0x20b9898:return m,[NAME,v.get('port',0x1234),PEER]
    if address==0x20b9914:return m,[v.get('allocWord',0x2233001),v.get('freeWord',0x2234000)]
    return m,[]


def effect(at,a,m,v):
    result=0x76543210;norm=a[:]
    if at==0x2019d80:result=v.get('lengthOverride',len(text(v)));norm=[text(v).hex()]
    elif at==0x209075c:
        result=v.get('aton',0)
        if result:put(m,a[1],v.get('resolvedIp',0x10203040))
        if v.get('atonSwitch'):toggle_state(m)
    elif at==0x200708c:
        if v.get('lockSwitch'):toggle_state(m)
    elif at==0x209046c:
        result=HOST if v.get('hostFound',True)else 0
        if v.get('hostSwitch'):toggle_state(m)
    elif at==0x2008e0c:
        raw=m.read(a[0],a[2]);m.write(a[1],raw);norm=a+[raw.hex()]
        if v.get('copySwitch'):toggle_state(m)
    elif at==0x2007110:pass
    elif at==0x2008360:
        raw=bytes((i+v.get('seedByte',3))&255 for i in range(32));m.write(a[0],raw);norm=['private-seed',raw.hex()]
    elif at==0x2092338:norm=[m.read(a[0],a[1]).hex(),a[1]];switch_status(m,v,'seedSwitch')
    elif at==0x20b9cf4:result=v.get('errorWord',0);switch_status(m,v,'errorSwitch')
    elif at in [ARM_CB,THUMB_CB]:
        if v.get('callbackNullsStatus'):put(m,SGP,0)
        else:switch_status(m,v,'callbackSwitch')
    elif at==0x20b9bf4:result=v.get('busyResult',0);switch_status(m,v,'checkSwitch')
    elif at==0x20b9d08:put(m,ST+24,a[0]);put(m,ST+28,a[1])
    elif at==0x20b8734:switch_status(m,v,'controlWakeSwitch')
    elif at==0x20b8f74:switch_status(m,v,'stateWakeSwitch')
    elif at==0x20b9c2c:result=v.get('budget',(96+align(v.get('stateSize',4816))+align(v.get('controlSize',2292)))&0xffffffff)
    elif at==0x209aa44:result=0 if v.get('allocationFails')else HEAP
    elif at==0x2008d78:m.write(a[0],bytes([a[1]&255])*a[2]);switch_status(m,v,'fillSwitch')
    elif at==0x20b8e6c:result=v.get('stateSize',4816);switch_status(m,v,'stateSizeSwitch')
    elif at==0x20b86c4:result=v.get('controlSize',2292);switch_status(m,v,'controlSizeSwitch')
    elif at==0x20b86cc:put(m,ST+32,a[0]);switch_status(m,v,'controlCtorSwitch')
    elif at==0x20b8e74:
        for i,val in enumerate(a):put(m,ST+36+i*4,val)
        switch_status(m,v,'stateCtorSwitch')
    elif at==0x20b8f64:put(m,ST+48,a[0])
    else:raise ValueError(('Unqualified runtime provider',hex(at)))
    return result&0xffffffff,norm


def evaluate(address,v):
    m,args=initial(address,v);calls=[];result=0
    def call(at,a):
        value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
    if address==0x20b9848:
        if word(m,GP)and word(m,word(m,GP))==7:result=1
    elif address==0x20b9868:
        if args[0]:
            n=s32(call(0x2019d80,args))
            if 2<n<=64:
                for i in range(1,n-1):
                    if m.read(NAME+i,1)==b'.':result=1;break
    elif address==0x20b9898:
        m.write(PEER,bytes([8,2]));port=s32(args[1]);m.write(PEER+2,(((port>>8)&255)|(((port&0xffffffff)<<8)&0xff00)).to_bytes(2,'little'))
        if not call(0x209075c,[NAME,PEER+4]):
            call(0x200708c,[word(m,GP)+444]);host=call(0x209046c,[NAME])
            if host:
                length=int.from_bytes(m.read(host+10,2),'little',signed=True);call(0x2008e0c,[word(m,word(m,host+12)),PEER+4,length])
            call(0x2007110,[word(m,GP)+444]);result=1 if host else 0
        else:result=1
    elif address==0x20b9998:
        seed=SP-40;call(0x2008360,[seed]);call(0x2092338,[seed,32])
        if not call(0x20b9cf4,[])and word(m,SGP)and word(m,word(m,SGP))==2 and word(m,word(m,SGP)+16)and word(m,word(m,SGP)+48):
            put(m,word(m,SGP)+16,0);put(m,word(m,SGP)+48,0);callback=word(m,word(m,SGP)+64)
            if callback:base=word(m,SGP);call(callback&~1,[word(m,base+52),word(m,base+56),word(m,base+68)])
    elif address==0x20b99ec:
        if not word(m,SGP):call(0x20b9d08,[9,-2])
        elif not call(0x20b9bf4,[]):
            if not word(m,word(m,SGP)+4)and not word(m,word(m,SGP)+60):call(0x20b9d08,[9,-2])
            else:call(0x20b8734,[]);call(0x20b8f74,[]);put(m,word(m,SGP),2);result=1
    elif address==0x20b9914:
        size=call(0x20b9c2c,[]);base=call(0x209aa44,[0x53574300,size,32])
        if not base:call(0x20b9d08,[9,-1])
        else:
            put(m,SGP,base);call(0x2008d78,[base,0,72]);offset=96;put(m,word(m,SGP)+8,base+offset);offset+=align(call(0x20b8e6c,[]));put(m,word(m,SGP)+12,base+offset);call(0x20b86c4,[]);put(m,word(m,SGP)+4,args[1]);call(0x20b86cc,[word(m,word(m,SGP)+12)]);current=word(m,SGP);call(0x20b8e74,[word(m,current+8),args[0],word(m,current+4)]);call(0x20b8f64,[0x20b9c4d])
    elif address==0x20b9c2c:result=(96+align(call(0x20b8e6c,[]))+align(call(0x20b86c4,[])))&0xffffffff
    else:raise ValueError('Outside runtime family')
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word'if address in WORDS else'void',result&0xffffffff,[]


def model(address,v):return evaluate(address,v)[:4]
def expected_reads(address,v):return []


def cases(address):
    if address==0x20b9848:return [dict(nullState=n,statePhase=p)for n in [False,True]for p in [0,6,7,8,0x80000000,0xffffffff]]
    if address==0x20b9868:
        strings=set()
        for n in [0,1,2,3,4,64,65]:
            strings.add((b'a'*n).hex())
            for pos in {0,1,n-2,n-1}:
                if 0<=pos<n:raw=bytearray(b'a'*n);raw[pos]=46;strings.add(bytes(raw).hex())
        rows=[dict(text=s)for s in sorted(strings)];rows +=[dict(nullName=True),dict(text=(b'\x80.\xff').hex())];rows +=[dict(text=(b'a.'+b'a'*68).hex(),lengthOverride=n)for n in [0,2,3,64,65,0x80000000,0xffffffff]];return rows
    if address==0x20b9898:
        rows=[dict(aton=a,hostFound=h,hostLength=n,port=p)for a in [0,1,0xffffffff]for h in [False,True]for n in [0,4]for p in [0,0x1234,0xffffffff,0x12345678]]
        rows +=[dict(aton=0,hostFound=True,hostLength=4,**flags)for flags in [{'atonSwitch':True},{'lockSwitch':True},{'hostSwitch':True},{'copySwitch':True},{'atonSwitch':True,'lockSwitch':True,'hostSwitch':True,'copySwitch':True}]];return rows
    if address==0x20b9998:
        rows=[dict(errorWord=e,nullStatus=n,phase=p,busy=b,marker=m,callback=c)for e in [0,1]for n in [False,True]for p in [0,2,3]for b in [0,1]for m in [0,1]for c in [0,1,2]]
        rows +=[dict(callback=cb,word0=0,word1=0x80000000,word2=0xffffffff,**flags)for cb in [1,2]for flags in [{'seedSwitch':True},{'errorSwitch':True},{'callbackSwitch':True},{'callbackNullsStatus':True}]];return rows
    if address==0x20b99ec:return [dict(nullStatus=n,busyResult=r,storedWord=w,statusHook=h,**flags)for n in [False,True]for r in [0,1,0xffffffff]for w,h in [(0,0),(1,0),(0,0x2230101)]for flags in [{},{'controlWakeSwitch':True,'stateWakeSwitch':True}]]
    if address==0x20b9914:
        return [dict(allocationFails=fail,allocWord=a,freeWord=f,stateSize=size,**flags)for fail in [False,True]for a,f in [(0,0),(0x2233001,0x2234000)]for size in [31,32,4816]for flags in [{},{'fillSwitch':True},{'stateSizeSwitch':True},{'controlSizeSwitch':True},{'controlCtorSwitch':True},{'stateCtorSwitch':True},{'fillSwitch':True,'stateSizeSwitch':True,'controlSizeSwitch':True,'controlCtorSwitch':True,'stateCtorSwitch':True}]]
    if address==0x20b9c2c:return [dict(stateSize=a,controlSize=b)for a in [0,1,31,32,33,4816,0xffffffe0,0xffffffe1,0xffffffff]for b in [0,31,32,2292,0xffffffff]]
    raise ValueError('No runtime vectors')
