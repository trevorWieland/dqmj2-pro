from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32
H,BUF,OLD,N1,N2,RES,ENT,LAB,VAL,OUT,STR,ST=0x2170000,0x2173000,0x2174000,0x2175000,0x2176000,0x2177000,0x2177100,0x2178000,0x2178100,0x2179000,0x217a000,0x217f000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
AP,AT,FP,FT=0x2234000,0x2234004,0x2234100,0x2234104
OBSERVED=set();ARITY={AP:2,AT:2,FP:3,FT:3,0x2008e0c:3,0x2008d78:3,0x201d69c:1,0x201d6b8:2,0x201d800:2,0x2098ed8:2,0x209a83c:4,0x200708c:1,0x2007110:1,0x2006890:1}
DATA={int(at,0):bytes.fromhex(v['expectedHex'])for at,v in read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/first/original-imports.json')['dataViews'].items()}
TAGS={raw[:-1].decode('ascii'):at for at,raw in DATA.items()}
WORDS={0x2098a7c,0x2098adc,0x2098c38,0x2098ed8,0x2098f14,0x2098f48}
def dynamic_callbacks(v):return {AP:dict(mode='arm'),AT:dict(mode='thumb'),FP:dict(mode='arm'),FT:dict(mode='thumb')}
def allocator(v):return AT|1 if v.get('callbackMode',0)&1 else AP
def freer(v):return FT|1 if v.get('callbackMode',0)&2 else FP
def cstring(m,at):
    raw=bytearray()
    for i in range(256):
        b=m.read(at+i,1)
        if b==bytes([0]):return bytes(raw)
        raw+=b
    raise ValueError('Outside bounded C string')
def initial(address,v):
    m=Memory({**DATA,H:bytes(7188),BUF:bytes(16),OLD:bytes((i*13+7)&255 for i in range(512)),N1:bytes([0x77])*512,N2:bytes([0x88])*512,RES:bytes(12),ENT:bytes(256),LAB:bytes(128),VAL:bytes(128),OUT:bytes([0xa5])*256,STR:bytes(4096),ST:bytes(128),SP-0x1000:bytes(0x1000)})
    put(m,H+0x1010,allocator(v));put(m,H+0x1014,freer(v));put(m,H+0x1ba4,v.get('threadState',1));put(m,H+0x1c10,5);m.write(H+4096,bytes([v.get('initFlag',255)]));v['_address']=address
    for off,value in [(0,0 if v.get('nullBuffer')else OLD),(4,OLD+v.get('indexOffset',4)),(8,OLD+v.get('oldLength',16)),(12,v.get('oldLength',16))]:put(m,BUF+off,value)
    m.write(LAB,bytes([0x61])*v.get('labelLength',3)+bytes([0]));m.write(VAL,bytes([0x76])*v.get('valueLength',7)+bytes([0]));put(m,RES,ENT);put(m,RES+4,v.get('resultLimit',3));put(m,RES+8,v.get('resultIndex',0))
    for i in range(32):
        lp=STR+i*128;vp=lp+64;m.write(lp,('key%d'%i).encode()+bytes([0]));m.write(vp,('value%d'%i).encode()+bytes([0]));put(m,H+0x1a38+i*8,lp if i<v.get('labelCount',0)and i!=v.get('hole',-1)else 0);put(m,H+0x1a3c+i*8,vp)
        put(m,ENT+i*8,lp if v.get('entryMask',0)&1 else 0);put(m,ENT+i*8+4,vp if v.get('entryMask',0)&2 else 0)
    if address==0x2098ed8:m.write(LAB,('key%d'%v.get('match',-1)).encode()+bytes([0]))
    args={0x20983d0:[H],0x2098a7c:[H,BUF,v.get('increment',8)],0x2098ab4:[H,BUF],0x2098adc:[H,BUF,v.get('increment',8)],0x2098c38:[H,RES,LAB,VAL],0x2098ed8:[H,LAB],0x2098f14:[H,LAB,OUT,v.get('capacity',16)],0x2098f48:[H,LAB,OUT,v.get('capacity',16)],0x2098f74:[H,ENT,v.get('count',3)]}
    return m,args[address]
def effect(at,a,m,v):
    result=0x76543210;norm=a[:]
    if at in [AP,AT]:
        i=word(m,ST);put(m,ST,i+1);result=0 if i==v.get('failAllocationAt',-1)else N1 if i==0 else N2
        if v.get('allocationChangesCallbacks'):put(m,H+0x1010,AP if at==AT else AT|1);put(m,H+0x1014,FP if freer(v)==(FT|1)else FT|1)
        if v.get('allocationChangesIndex'):put(m,RES+8,1)
        if v.get('allocationChangesBuffer'):put(m,BUF+12,8);put(m,BUF+4,OLD+4)
    elif at in [FP,FT]:
        put(m,ST+4,word(m,ST+4)+1)
        if v.get('freeChangesCallback'):put(m,H+0x1014,FP if at==FT else FT|1)
        if v.get('freeChangesBuffer'):put(m,BUF,OLD+4);put(m,BUF+4,OLD+12);put(m,BUF+12,8)
    elif at==0x2008d78:m.write(a[0],bytes([a[1]&255])*a[2])
    elif at==0x2008e0c:
        raw=m.read(a[0],a[2]);m.write(a[1],raw);norm=a+[raw.hex()]
    elif at==0x201d69c:result=len(cstring(m,a[0]));norm=a+[cstring(m,a[0]).hex()]
    elif at==0x201d6b8:
        raw=cstring(m,a[1])+bytes([0]);m.write(a[0],raw);result=a[0];norm=a+[raw.hex()]
    elif at==0x201d800:
        left,right=cstring(m,a[0]),cstring(m,a[1]);result=0 if left==right else 1 if left>right else 0xffffffff;norm=a+[left.hex(),right.hex()]
        if v.get('compareChangesValue')and left==right:
            for i in range(32):
                if word(m,H+0x1a38+i*8)==a[1]:put(m,H+0x1a3c+i*8,OUT)
    elif at==0x2098ed8:result=VAL if v.get('found',True)else 0
    elif at==0x209a83c:
        result=v.get('decodeResult',3)&0xffffffff
        if result<=a[3]and result<=128:m.write(a[2],bytes((i+0x61)&255 for i in range(result)))
    elif at==0x200708c:
        if v.get('lockChangesInit'):m.write(H+4096,bytes([0]))
    elif at==0x2007110:
        if v.get('unlockChangesThread'):put(m,H+0x1ba4,0)
    elif at==0x2006890:put(m,ST+8,word(m,ST+8)+1)
    else:raise ValueError(('Outside typed HTTP provider scope',hex(at)))
    return result&0xffffffff,norm
def evaluate(address,v):
    m,args=initial(address,v);calls=[];result=0;alloc=word(m,H+0x1010);free=word(m,H+0x1014)
    def call(at,a):
        r,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return r
    if address==0x20983d0:
        if m.read(H+4096,1)==bytes([255]):
            call(0x200708c,[H+0x1bf8]);put(m,H+0x1c10,1);call(0x2007110,[H+0x1bf8])
            if word(m,H+0x1ba4):call(0x2006890,[H+0x1b38])
    elif address==0x2098a7c:
        n=args[2]&0xffffffff
        if n:
            p=call(alloc&~1,[TAGS['ALLOC buf->buffer'],n]);put(m,BUF,p)
            if p:put(m,BUF+4,p);put(m,BUF+12,n);put(m,BUF+8,p+n);result=1
    elif address==0x2098ab4:
        if word(m,BUF):call(free&~1,[TAGS['FREE buf->buffer'],word(m,BUF),0])
        call(0x2008d78,[BUF,0,16])
    elif address==0x2098adc:
        n=s32(args[2]&0xffffffff)
        if n>0:
            p=call(alloc&~1,[TAGS['ALLOC newptr'],word(m,BUF+12)+n])
            if p:
                call(0x2008e0c,[word(m,BUF),p,word(m,BUF+12)]);call(free&~1,[TAGS['FREE buf->buffer'],word(m,BUF),0]);put(m,BUF+4,word(m,BUF+4)+p-word(m,BUF));put(m,BUF+12,word(m,BUF+12)+n);put(m,BUF,p);put(m,BUF+8,p+word(m,BUF+12));result=1
    elif address==0x2098c38:
        def cell(off=0):return word(m,RES)+word(m,RES+8)*8+off
        if s32(word(m,RES+8))<=s32(word(m,RES+4)):
            n=call(0x201d69c,[LAB]);p=call(alloc&~1,[TAGS['ALLOC result->entry[i].label'],n+1]);put(m,cell(),p)
            if word(m,cell()):
                n=call(0x201d69c,[VAL]);p=call(alloc&~1,[TAGS['ALLOC result->entry[i].value'],n+1]);put(m,cell(4),p)
                if word(m,cell(4)):
                    call(0x201d6b8,[word(m,cell()),LAB]);call(0x201d6b8,[word(m,cell(4)),VAL]);put(m,RES+8,word(m,RES+8)+1);result=1
            if not result:
                for off,tag in [(0,'FREE result->entry[i].label'),(4,'FREE result->entry[i].value')]:
                    if word(m,cell(off)):call(free&~1,[TAGS[tag],word(m,cell(off)),0]);put(m,cell(off),0)
    elif address==0x2098ed8:
        for i in range(32):
            label=word(m,H+0x1a38+i*8)
            if not label:break
            if not call(0x201d800,[LAB,label]):result=word(m,H+0x1a3c+i*8);break
    elif address in [0x2098f14,0x2098f48]:
        p=call(0x2098ed8,[H,LAB])
        if p:
            n=call(0x201d69c,[p]);cap=args[3]&0xffffffff
            if address==0x2098f14:
                result=call(0x209a83c,[p,n,OUT,cap])
                if result!=0xffffffff and result<cap:m.write(OUT+result,bytes([0]))
            elif s32(n)<s32(cap):call(0x201d6b8,[OUT,p]);result=1
    elif address==0x2098f74:
        for i in range(max(0,args[2])):
            for off,tag in [(0,'FREE array_entry[i].label'),(4,'FREE array_entry[i].value')]:
                at=ENT+i*8+off
                if word(m,at):call(free&~1,[TAGS[tag],word(m,at),0]);put(m,at,0)
    else:raise ValueError('Outside HTTP subset')
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word'if address in WORDS else'void',result&0xffffffff
def model(address,v):return evaluate(address,v)
def expected_reads(address,v):return []
def cases(address):
    if address==0x20983d0:return [dict(initFlag=f,threadState=s,**flags)for f in [0,1,127,128,254,255]for s in [0,1,2,0xffffffff]for flags in [{},{'lockChangesInit':True,'unlockChangesThread':True}]]
    if address==0x2098a7c:return [dict(increment=n,failAllocationAt=f,callbackMode=mode)for n in [0,1,16,32]for f in [-1,0]for mode in range(4)]+[dict(increment=n,failAllocationAt=0)for n in [-1,-2147483648]]
    if address==0x2098ab4:return [dict(nullBuffer=b,callbackMode=mode,**flags)for b in [False,True]for mode in range(4)for flags in [{},{'freeChangesCallback':True},{'freeChangesBuffer':True}]]
    if address==0x2098adc:return [dict(increment=n,failAllocationAt=f,callbackMode=mode,**flags)for n in [-1,0,1,16]for f in [-1,0]for mode in range(4)for flags in [{},{'allocationChangesCallbacks':True},{'allocationChangesBuffer':True,'freeChangesBuffer':True}]]
    if address==0x2098c38:return [dict(resultIndex=i,resultLimit=limit,failAllocationAt=f,entryMask=mask,callbackMode=mode,**flags)for i,limit in [(0,0),(0,3),(3,3),(4,3)]for f in [-1,0,1]for mask in [0,3]for mode in [0,3]for flags in [{},{'allocationChangesCallbacks':True,'freeChangesCallback':True},{'allocationChangesIndex':True}]]
    if address==0x2098ed8:return [dict(labelCount=n,match=i,**flags)for n in [0,1,3,32]for i in [-1,0,n-1]for flags in [{},{'hole':0},{'compareChangesValue':True}]]
    if address==0x2098f14:return [dict(found=f,capacity=c,decodeResult=r,callbackMode=0)for f in [False,True]for c in [0,1,8,16,127]for r in [-1,0,1,c-1,c,c+1]]
    if address==0x2098f48:return [dict(found=f,capacity=c,valueLength=n)for f in [False,True]for c in [-1,0,1,8,16]for n in [0,1,7,15]]
    if address==0x2098f74:return [dict(count=n,entryMask=mask,callbackMode=mode,freeChangesCallback=change)for n in [-1,0,1,3]for mask in [0,1,2,3]for mode in range(4)for change in [False,True]]
    raise ValueError('No bounded HTTP cases')
