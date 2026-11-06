from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32
H,P,RBUF,SBUF,BODY,BODY2,U,U2,LABEL,DATASTR,ST=0x2170000,0x2182000,0x2180000,0x2181000,0x2183000,0x2186000,0x2190000,0x2190100,0x2191000,0x2191100,0x219f000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
AP,AT,FP,FT=0x2234000,0x2234004,0x2234100,0x2234104
imports=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/second/original-imports.json')
RO={int(at,0):bytes.fromhex(v['expectedHex'])for at,v in imports['dataViews'].items()if v['storage']=='data'}
TAGS={raw[:-1]:at for at,raw in RO.items()};FLAG=next(int(at,0)for at,v in imports['dataViews'].items()if v['storage']=='bss');ENTRY=next(int(at,0)for at in imports['functionPointerViews'])
OBSERVED={H+0x1020};WORDS={0x209820c,0x20982e4,0x2098954}
ARITY={AP:2,AT:2,FP:3,FT:3,0x2008d78:3,0x2098a7c:3,0x2098b44:2,0x2098830:1,0x2098f74:3,0x2098ab4:2,0x20988bc:3,0x201d984:2,0x201d69c:1,0x20061ac:4,0x2007074:1,0x20068c0:1,0x20065f0:6,0x200698c:1,0x209a738:4,0x2098adc:3}
class AuditMemory(Memory):
    def __init__(self,regions):super().__init__(regions);self.observe=False;self.reads=[]
    def read(self,at,size):
        raw=super().read(at,size)
        if self.observe and at in OBSERVED:self.reads.append((at,size,int.from_bytes(raw,'little')))
        return raw
def dynamic_callbacks(v):return {AP:dict(mode='arm'),AT:dict(mode='thumb'),FP:dict(mode='arm'),FT:dict(mode='thumb')}
def allocator(v):return AT|1 if v.get('callbackMode',0)&1 else AP
def freer(v):return FT|1 if v.get('callbackMode',0)&2 else FP
def string(m,at):
    raw=bytearray()
    for i in range(512):
        b=m.read(at+i,1)
        if not b[0]:return bytes(raw)
        raw+=b
    raise ValueError('Outside bounded lifecycle string')
def request(v):return b'POST /p HTTP/1.0\r\nHost: test\r\n\r\n'+b'x'*v.get('bodyLength',15)
def setbuf(m,at,base,offset,capacity):
    for off,value in [(0,base),(4,base+offset),(8,base+capacity),(12,capacity)]:put(m,at+off,value)
def initial(address,v):
    m=AuditMemory({**RO,FLAG:bytes.fromhex('7f7f7f7f'),H:bytes([0xa7])*7188,P:bytes(28),RBUF:bytes([0x88])*4096,SBUF:bytes([0x99])*2048,BODY:bytes(8192),BODY2:bytes(8192),U:bytes(128),U2:bytes(128),LABEL:bytes(128),DATASTR:bytes(128),ST:bytes(128),SP-0x1000:bytes(0x1000)})
    for off,val in [(0,U),(4,v.get('action',0)),(8,v.get('recvSize',64)),(12,allocator(v)),(16,freer(v)),(20,v.get('ignoreCa',1)),(24,0x1234)]:put(m,P+off,val);put(m,H+0x1004+off,val)
    put(m,H+0x1ba4,v.get('threadState',0));put(m,H+0x1c10,5);put(m,H+0x19cc,0 if v.get('nullRecv')else RBUF);put(m,H+0x19d0,0 if v.get('nullSend')else SBUF);put(m,H+0x19f4,v.get('postCount',0));setbuf(m,H+0x19f8,BODY,v.get('writeOffset',0),v.get('capacity',32));setbuf(m,H+0x1a08,BODY2,0,64);m.write(U,b'http://example.test/a'+bytes([0]));m.write(U2,b'http://changed.test/b'+bytes([0]));m.write(LABEL,b'k'*v.get('labelLength',3)+bytes([0]));m.write(DATASTR,bytes((i+1)&255 for i in range(64)));m.write(BODY,request(v)+bytes([0]));m.write(BODY2,request(v)+bytes([0]));v['_address']=address
    args={0x209820c:[H,P],0x20982e4:[H],0x209834c:[H,v.get('priority',7)],0x20987b0:[H],0x2098954:[H,LABEL,DATASTR,v.get('dataLength',8)]}
    return m,args[address]
def effect(at,a,m,v):
    result=0x76543210;norm=a[:]
    if at in [AP,AT]:
        i=word(m,ST);put(m,ST,i+1);result=0 if i==v.get('failAllocationAt',-1)else RBUF if i==0 else SBUF
        if v.get('allocationChangesCallbacks'):put(m,H+0x1010,AP if at==AT else AT|1);put(m,P+12,AP if at==AT else AT|1)
    elif at in [FP,FT]:
        put(m,ST+4,word(m,ST+4)+1)
        if v.get('freeChangesCallback'):put(m,H+0x1014,FP if at==FT else FT|1)
    elif at==0x2008d78:
        m.write(a[0],bytes([a[1]&255])*a[2])
        if v.get('fillChangesParam'):put(m,P+12,AP if allocator(v)==(AT|1)else AT|1)
    elif at==0x2098a7c:
        result=v.get('bufferAllocResult',1)
        if result:setbuf(m,a[1],BODY2,0,a[2])
        if v.get('bufferAllocChangesUrl'):put(m,P,U2)
    elif at==0x2098b44:result=v.get('hostResult',1)
    elif at==0x2098830:result=v.get('basicHeaderResult',0)
    elif at==0x2098f74:
        m.write(a[1],bytes(a[2]*8))
        if v.get('tableChangesFree'):put(m,H+0x1014,FP if freer(v)==(FT|1)else FT|1)
    elif at==0x2098ab4:
        m.write(a[1],bytes(16))
        if v.get('bufferFreeChangesPointers'):put(m,H+0x19cc,0);put(m,H+0x19d0,0)
    elif at==0x20988bc:
        i=word(m,ST+8);put(m,ST+8,i+1);norm=a+[string(m,a[1]).hex(),string(m,a[2]).hex()];result=v.get('firstHeaderResult',0)if i==0 else v.get('secondHeaderResult',0)
        if v.get('headerSwitchBuffer'):put(m,H+0x19f8,BODY2)
    elif at==0x201d984:
        hay,needle=string(m,a[0]),string(m,a[1]);pos=hay.find(needle)
        if pos<0:raise ValueError('Outside delimiter-present precondition')
        result=a[0]+pos;norm=a+[hay.hex(),needle.hex()]
    elif at==0x201d69c:raw=string(m,a[0]);result=len(raw);norm=a+[raw.hex()]
    elif at==0x20061ac:
        fmt=string(m,a[2]);text=str(s32(a[3])).encode()if fmt==b'%d'else fmt.replace(b'%s',string(m,a[3]));result=len(text)
        if a[1]:m.write(a[0],text[:max(0,a[1]-1)]+bytes([0]))
        norm=a+[fmt.hex(),text.hex()]
    elif at==0x2007074:
        m.write(a[0],bytes(24))
        if v.get('mutexChangesThread'):put(m,H+0x1ba4,1)
    elif at==0x20068c0:result=v.get('terminatedResult',1)
    elif at==0x20065f0:put(m,H+0x1ba4,1)
    elif at==0x200698c:put(m,ST+12,word(m,ST+12)+1)
    elif at==0x209a738:
        i=word(m,ST+16);put(m,ST+16,i+1);encoded=v.get('encodedLength',12);norm=a+[m.read(a[0],a[1]).hex()]
        if not i:result=encoded
        else:
            result=v.get('encodeResult',encoded)
            if s32(result&0xffffffff)>=0:m.write(a[2],b'Z'*encoded)
    elif at==0x2098adc:
        result=v.get('growthResult',1)
        if result:
            base=word(m,H+0x19f8);offset=word(m,H+0x19fc)-base;capacity=word(m,H+0x1a00)-base+a[2]
            if v.get('growthSwitchBuffer'):m.write(BODY2,m.read(base,min(capacity,4096)));base=BODY2
            setbuf(m,H+0x19f8,base,offset,capacity)
    else:raise ValueError(('Outside lifecycle provider scope',hex(at)))
    return result&0xffffffff,norm
def evaluate(address,v):
    m,args=initial(address,v);calls=[];result=0;m.observe=True
    def call(at,a):
        m.observe=False;r,n=effect(at,[x&0xffffffff for x in a],m,v);m.observe=True;calls.append((hex(at),n));return r
    if address==0x209820c:
        alloc=word(m,P+12);call(0x2008d78,[H,0,7188]);put(m,H+0x1a30,-1);put(m,H+0x1a34,-1);m.write(H+0x1004,m.read(P,28));p=call(alloc&~1,[TAGS[b'ALLOC http->lowrecvbuf'],2920]);put(m,H+0x19cc,p);ok=bool(p)
        if ok:p=call(alloc&~1,[TAGS[b'ALLOC http->lowsendbuf'],1514]);put(m,H+0x19d0,p);ok=bool(p)
        if ok:ok=bool(call(0x2098a7c,[H,H+0x1a08,word(m,H+0x100c)]))
        if ok:ok=bool(call(0x2098b44,[H,word(m,P)]))
        if not ok:put(m,H+0x1020,1);result=1
        else:
            code=call(0x2098830,[H]);put(m,H+0x1020,code)
            if not word(m,H+0x1020):m.write(H+4096,bytes([255]))
            result=word(m,H+0x1020)
    elif address==0x20982e4:
        first=call(0x20988bc,[H,TAGS[b'Connection'],TAGS[b'close']])
        if first:result=1
        else:
            p=call(0x201d984,[word(m,H+0x19f8),TAGS[b'\r\n\r\n']]);n=call(0x201d69c,[p+4])
            if n:
                scratch=SP-16;call(0x20061ac,[scratch,7,TAGS[b'%d'],n]);result=1 if call(0x20988bc,[H,TAGS[b'Content-Length'],scratch])else 0
    elif address==0x209834c:
        put(m,H+0x1c10,0);call(0x2007074,[H+0x1bf8]);call(0x2007074,[H+0x1a18]);put(m,FLAG,1 if word(m,H+0x1018)==1 else 0)
        if not word(m,H+0x1ba4)or call(0x20068c0,[H+0x1b38]):call(0x20065f0,[H+0x1b38,ENTRY,H,H+4096,4096,args[1]]);call(0x200698c,[H+0x1b38])
    elif address==0x20987b0:
        free=word(m,H+0x1014);call(0x2098f74,[H,H+0x1a38,32]);call(0x2098ab4,[H,H+0x1a08]);call(0x2098ab4,[H,H+0x19f8])
        for offset,tag in [(0x19cc,b'FREE http->lowrecvbuf'),(0x19d0,b'FREE http->lowsendbuf')]:
            if word(m,H+offset):call(free&~1,[TAGS[tag],word(m,H+offset),0]);put(m,H+offset,0)
        call(0x2008d78,[H,0,7188])
    elif address==0x2098954:
        post=word(m,H+0x19f4);fmt=TAGS[b'%s=']if post==0 else TAGS[b'&%s='];put(m,H+0x19f4,post+1);encoded=s32(call(0x209a738,[DATASTR,args[3],0,0]));required=s32(call(0x201d69c,[fmt]))-2+s32(call(0x201d69c,[LABEL]))+encoded;remaining=s32((word(m,H+0x1a00)-word(m,H+0x19fc))&0xffffffff);ok=True
        if required>remaining:
            if not call(0x2098adc,[H,H+0x19f8,required-remaining+1]):ok=False
            else:remaining=s32((word(m,H+0x1a00)-word(m,H+0x19fc))&0xffffffff)
        if not ok:result=1
        else:
            n=call(0x20061ac,[word(m,H+0x19fc),remaining,fmt,LABEL]);put(m,H+0x19fc,word(m,H+0x19fc)+n);remaining=s32((word(m,H+0x1a00)-word(m,H+0x19fc))&0xffffffff);r=call(0x209a738,[DATASTR,args[3],word(m,H+0x19fc),remaining-1])
            if s32(r)<0:result=1
            else:put(m,H+0x19fc,word(m,H+0x19fc)+encoded);m.write(word(m,H+0x19fc),bytes([0]))
    else:raise ValueError('Outside lifecycle callers')
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word'if address in WORDS else'void',result&0xffffffff,m.reads
def model(address,v):return evaluate(address,v)[:4]
def expected_reads(address,v):return evaluate(address,v)[4]
def cases(address):
    if address==0x209820c:
        rows=[dict(failAllocationAt=f,bufferAllocResult=b,hostResult=h,basicHeaderResult=r,callbackMode=mode)for f in [-1,0,1]for b,h in [(0,1),(1,0),(1,1)]for r in [0,1,7,0xffffffff]for mode in [0,3]]
        rows +=[dict(callbackMode=mode,**flags)for mode in range(4)for flags in [{'allocationChangesCallbacks':True},{'fillChangesParam':True},{'bufferAllocChangesUrl':True},{'fillChangesParam':True,'allocationChangesCallbacks':True,'bufferAllocChangesUrl':True}]];return rows
    if address==0x20982e4:return [dict(bodyLength=n,firstHeaderResult=f,secondHeaderResult=s,headerSwitchBuffer=b)for n in [0,1,15,99]for f in [0,1,0xffffffff]for s in [0,1]for b in [False,True]]
    if address==0x209834c:return [dict(ignoreCa=c,threadState=s,terminatedResult=t,priority=p,**flags)for c in [0,1,2,0xffffffff]for s in [0,1,2]for t in [0,1]for p in [0,0xffffffff]for flags in [{},{'mutexChangesThread':True}]]
    if address==0x20987b0:return [dict(nullRecv=r,nullSend=s,callbackMode=mode,**flags)for r in [False,True]for s in [False,True]for mode in range(4)for flags in [{},{'tableChangesFree':True},{'bufferFreeChangesPointers':True},{'freeChangesCallback':True}]]
    if address==0x2098954:
        rows=[dict(postCount=p,capacity=c,writeOffset=o,encodedLength=e,growthResult=g,encodeResult=r)for p in [0,1,0xffffffff]for c,o in [(0,0),(8,0),(16,4),(32,0)]for e in [0,4,12]for g in [0,1]for r in [-1,e]]
        rows +=[dict(postCount=p,capacity=8,encodedLength=12,growthSwitchBuffer=True,labelLength=n)for p in [0,1]for n in [0,1,7]];return rows
    raise ValueError('No lifecycle vectors')
