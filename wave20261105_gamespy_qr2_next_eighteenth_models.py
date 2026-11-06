from wave20261105_gamespy_qr2_next_first_models import Memory,word,put

Q,N,S,D,H,SECRET,OUT,HE,LIST,IPS,ST=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2174100,0x2174200,0x2174300,0x2174400,0x2174500,0x2174600
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700800,0x20e2554
CUR,STATIC,HOST,INBUF,NUM,IPLIST=0x20e179c,0x20e17a0,0x21d2ee0,0x21d2f20,0x21d2ec8,0x21d2ecc
DIV=0x2026144
ARITY={0x20b6654:1,0x20b6564:1,0x20b6f3c:3,0x20b6fa8:3,0x20b7014:3,0x20b73c0:1,0x20b7360:1,0x20b8068:1,0x20a8ef8:0,0x20b8380:2,0x20b8334:1,0x20a8d88:1,0x20a8c00:6,0x20b80a0:4,0x20a8b6c:1,0x20a8ef4:0,0x20a929c:1,0x2019dd4:4,0x20a927c:1,0x201d608:1,0x201d6b8:2,0x201d5d4:0,DIV:2,0x201b208:3,0x20b75cc:0,0x200616c:3,0x20b760c:4,0x20a8dc0:0,0x20a8c84:1,0x201d800:2,0x209046c:1}
for target in [0x27e0100,0x27e0110,0x27e0200,0x27e0210]:ARITY[target]=3


def cb(v,role):return (0x27e0100 if role=='error'else 0x27e0200)+(0x11 if v.get('thumb',False)else 0)
def dynamic_callbacks(v):return{cb(v,role)&~1:dict(mode='thumb'if cb(v,role)&1 else'arm')for role in ['error','public']}
def z(m,p):
    raw=bytearray()
    for i in range(256):
        byte=m.read(p+i,1)[0]
        if not byte:return bytes(raw)
        raw.append(byte)
    raise ValueError('Bounded string lacks terminator')
def s32(n):return n-0x100000000 if n&0x80000000 else n
def mod(a,b):return a-(abs(a)//abs(b)*(-1 if(a<0)!=(b<0)else 1))*b
def qptr(v):return STATIC if v.get('static',False)else Q


def initial(address,v):
    q=qptr(v);m=Memory({Q:bytes([0xa5])*3476,STATIC:bytes([0x5a])*3476,N:bytes(84),S:bytes.fromhex('7f02674504030201'),D:bytes((i*17+3)&255 for i in range(64)),H:bytes(256),SECRET:bytes(128),OUT:bytes.fromhex('ddccbbaa')+bytes(28),HE:bytes(16),LIST:bytes(24),IPS:bytes(24),ST:bytes(32),CUR:q.to_bytes(4,'little'),HOST:bytes(64),INBUF:bytes([0x6d])*256,NUM:(9).to_bytes(4,'little'),IPLIST:bytes([0x71])*20,MAGIC:b'No challenge value was received from the master server.\0',0x20e2534:b'%s.master.gs.nintendowifi.net\0',0x20e2590:b'255.255.255.255\0',0x20e25a0:b'%08X%04X\0',SP-0x1000:bytes(0x1000)})
    m.write(H,v.get('name','example').encode()+bytes([0]));m.write(SECRET,b'secret-key\0');m.write(HOST,v.get('override','').encode()+bytes([0]));put(m,HE+12,LIST)
    for i in range(5):put(m,LIST+i*4,IPS+i*4 if i<v.get('ipCount',2)else 0);put(m,IPS+i*4,0x10203040+i*0x11010101)
    for offset,value in [(0,v.get('socket',7)),(172,v.get('lastHB',100)),(176,v.get('lastKA',100)),(180,v.get('requested',0)),(184,v.get('listed',0)),(188,v.get('public',1)),(192,27900),(196,v.get('read',1)),(200,1),(260,v.get('oldIP',0)),(268,0x12345678)]:put(m,q+offset,value)
    m.write(q+264,v.get('oldPort',0).to_bytes(2,'little'));put(m,q+156,cb(v,'error'));put(m,q+168,cb(v,'public'))
    if address==0x20b70c8:
        m.write(D+7,bytes([v['ptype']]));return m,[D,v['length']&0xffffffff,S]
    if address==0x20b718c:return m,[0 if v.get('static')else OUT,v.get('socket',7),v.get('boundPort',27900),H,SECRET,v.get('public',1),v.get('nat',1),0x11110001,0x22220000,0x33330001,0x44440000,0x55550001,0x66660000,0x77778888]
    if address==0x20b75cc:return m,[]
    if address==0x20b760c:return m,[0 if v.get('nullHost')else H,v.get('port',27900)&0xffffffff,S,OUT if v.get('save',True)else 0]
    if address==0x20b78ac:return m,[q,H]
    return m,[0 if v.get('nullArgument')else q]


def effect(at,a,m,v):
    q=qptr(v);entry=v['entry'];result=0x12345678;norm=a[:]
    if at==0x20a8ef8:
        count=word(m,ST);put(m,ST,count+1);result=v.get('now',1000)if count==0 else v.get('now2',v.get('now',1000))
        if 'afterClockHB'in v:put(m,q+172,v['afterClockHB'])
    elif at==0x20b6654:
        norm=[m.read(a[0],6).hex()];result=v['magic']&0xffffffff
        if 'afterMagicType'in v:m.write(D+7,bytes([v['afterMagicType']]))
    elif at==0x20b6564:
        result=N if v['found']else 0
        if v.get('mutateInputAfterCopy'):m.write(D,bytes([0xee])*21)
    elif at in [0x20b6f3c,0x20b6fa8,0x20b7014]:
        length=20 if at in [0x20b6f3c,0x20b6fa8]else 21;norm=[a[0],m.read(a[1],length).hex(),m.read(a[2],8).hex()];put(m,N+4,0x1a2b3c4d)
    elif at in [0x20b73c0,0x20b7360,0x20b8068]:
        if v.get('mutateHelpers'):put(m,q+188,word(m,q+188)^0x80000000)
    elif at==0x20b8380:
        if 'afterSendListed'in v:put(m,q+184,v['afterSendListed'])
        if 'afterSendHB'in v:put(m,q+172,v['afterSendHB'])
    elif at in [cb(v,'error')&~1,cb(v,'public')&~1]:
        if at==(cb(v,'error')&~1):norm=[a[0],z(m,a[1]).decode(),a[2]]
        put(m,q+268,0xabcdef12)
    elif at==0x20a8d88:result=int(word(m,ST+4)<len(v.get('receives',[])))
    elif at==0x20a8c00:
        index=word(m,ST+4);value=v['receives'][index];norm=[a[0],a[2],a[3],word(m,a[5])];put(m,ST+4,index+1);m.write(a[4],bytes([0x33,2,0x12,0x34,1,2,3,4]));put(m,a[5],v.get('nextAddrLen',8));result=value&0xffffffff
        if value>=0:m.write(a[1],bytes((i*13+index)&255 for i in range(value)))
    elif at==0x20b80a0:
        length=s32(a[2]);norm=[a[0],m.read(a[1],max(0,length)).hex(),a[2],m.read(a[3],8).hex()]
    elif at in [0x20a8b6c,0x20a8ef4,0x20a929c,0x201d608,0x20b8334]:pass
    elif at==0x2019dd4:
        norm=[z(m,a[0]).decode(),z(m,a[1]).decode()];put(m,a[2],v['scanIP']);put(m,a[3],v['scanPort']);result=2
    elif at==0x20a927c:result=Q
    elif at==0x201d6b8:
        raw=z(m,a[1])+bytes([0]);m.write(a[0],raw);norm=[a[0],raw.hex()];result=a[0]
    elif at==0x201d5d4:
        count=word(m,ST+8);put(m,ST+8,count+1);result=v.get('random',[0,1,254,255])[count]&0xffffffff
    elif at==DIV:
        av,bv=s32(a[0]),s32(a[1]);result=(abs(av)//abs(bv)*(-1 if(av<0)!=(bv<0)else 1))&0xffffffff
    elif at==0x201b208:m.write(a[0],bytes([a[1]&255])*a[2]);result=a[0]
    elif at==0x20b75cc:pass
    elif at==0x200616c:
        raw=z(m,a[2])+b'.master.gs.nintendowifi.net';m.write(a[0],raw+bytes([0]));norm=[z(m,a[1]).decode(),z(m,a[2]).decode()];result=len(raw)
    elif at==0x20b760c:
        norm=[z(m,a[0]).decode(),a[1],a[2],a[3]];m.write(a[2]+1,bytes([2]));m.write(a[2]+2,a[1].to_bytes(2,'big'));put(m,a[2]+4,0x01020304);result=v.get('dnsResult',1)&0xffffffff
    elif at==0x20a8dc0:result=HE if v.get('hostPresent',True)else 0
    elif at==0x20a8c84:norm=[z(m,a[0]).decode()];result=v.get('inet',0xffffffff)
    elif at==0x201d800:norm=[z(m,a[0]).decode(),z(m,a[1]).decode()];result=0 if norm[0]==norm[1]else 1
    elif at==0x209046c:norm=[z(m,a[0]).decode()];result=HE if v.get('hostPresent',True)else 0
    else:raise ValueError(('Unqualified measured import',hex(at)))
    return result&0xffffffff,norm


def model(address,v):
    m,args=initial(address,v);q=qptr(v);calls=[];contract='void';result=0
    def call(at,values):
        value,norm=effect(at,[x&0xffffffff for x in values],m,v);calls.append((hex(at),norm));return value
    if address==0x20b70c8:
        if call(0x20b6654,[D]):
            ptype=m.read(D+7,1)[0];length=20 if ptype in [5,7]else 21
            if v['length']>=length:
                m.write(TMP,m.read(D,length));cookie=int.from_bytes(m.read(TMP+8,4),'big');neg=call(0x20b6564,[cookie])
                if neg:call(0x20b6f3c if ptype==5 else 0x20b6fa8 if ptype==7 else 0x20b7014,[neg,TMP,S])
    elif address==0x20b7334:
        if word(m,q+188):call(0x20b73c0,[q])
        call(0x20b7360,[q]);call(0x20b8068,[q])
    elif address==0x20b7360:
        if word(m,q+196):
            length=8
            while call(0x20a8d88,[word(m,q)]):
                put(m,TMP+16,length);ret=call(0x20a8c00,[word(m,q),INBUF,255,0,TMP,TMP+16]);length=word(m,TMP+16)
                if ret!=0xffffffff:m.write(INBUF+s32(ret),bytes([0]));call(0x20b80a0,[q,INBUF,ret,TMP])
    elif address==0x20b73c0:
        tc=call(0x20a8ef8,[]);delta=(tc-word(m,q+172))&0xffffffff;early=False
        if word(m,q)!=0xffffffff:
            listed=s32(word(m,q+184))
            if listed>0 and delta>10000:
                if listed>=4:put(m,q+184,0);call(cb(v,'error')&~1,[5,MAGIC,word(m,q+268)]);early=True
                else:call(0x20b8380,[q,3]);put(m,q+184,word(m,q+184)+1)
            elif word(m,q+180)and delta>10000:call(0x20b8380,[q,1])
            elif delta>60000 or word(m,q+172)==0 or tc<word(m,q+172):call(0x20b8380,[q,0])
            if not early and ((call(0x20a8ef8,[])-word(m,q+176))&0xffffffff)>20000:call(0x20b8334,[q])
    elif address==0x20b748c:
        if word(m,q+188):
            if ((call(0x20a8ef8,[])-word(m,q+172))&0xffffffff)<10000:put(m,q+180,1)
            else:call(0x20b8380,[q,1]);put(m,q+180,0)
    elif address==0x20b74d4:
        if word(m,q+188):call(0x20b8380,[q,2])
        if word(m,q)!=0xffffffff and word(m,q+196):call(0x20a8b6c,[word(m,q)])
        put(m,q,0xffffffff);put(m,q+172,0)
        if word(m,q+196):call(0x20a8ef4,[])
        if q!=STATIC:call(0x20a929c,[q])
    elif address==0x20b75cc:
        host=call(0x20a8dc0,[])
        if host:
            put(m,NUM,0)
            while word(m,NUM)<5:
                i=word(m,NUM);src=word(m,LIST+i*4)
                if not src:break
                m.write(IPLIST+i*4,m.read(src,4));put(m,NUM,i+1)
    elif address==0x20b760c:
        contract='ARM R0 word';m.write(S+1,bytes([2]));m.write(S+2,(v['port']&65535).to_bytes(2,'big'));ip=0 if v.get('nullHost')else call(0x20a8c84,[H]);put(m,S+4,ip);hent=0;result=1
        if ip==0xffffffff and call(0x201d800,[H,0x20e2590]):
            hent=call(0x209046c,[H])
            if not hent:result=0
            else:put(m,S+4,word(m,IPS))
        if result and v.get('save',True):put(m,OUT,hent)
    elif address==0x20b78ac:
        put(m,TMP,0);put(m,TMP+4,0);call(0x2019dd4,[H,0x20e25a0,TMP,TMP+4]);ip=int.from_bytes(word(m,TMP).to_bytes(4,'little'),'big');port=word(m,TMP+4)&65535
        if ip and port and(word(m,q+260)!=ip or int.from_bytes(m.read(q+264,2),'little')!=port):
            put(m,q+260,ip);m.write(q+264,port.to_bytes(2,'little'));call(cb(v,'public')&~1,[ip,port,word(m,q+268)])
    elif address==0x20b718c:
        contract='ARM R0 word'
        if not v.get('static'):q=call(0x20a927c,[3476]);put(m,OUT,q)
        call(0x201d608,[call(0x20a8ef8,[])]);call(0x201d6b8,[q+4,H]);call(0x201d6b8,[q+68,SECRET])
        for off,value in [(192,v.get('boundPort',27900)),(172,0),(176,0),(0,v.get('socket',7)),(184,1),(268,0x77778888),(136,0x11110001),(140,0x22220000),(144,0x33330001),(148,0x44440000),(152,0x55550001),(156,0x66660000),(160,0),(164,0),(212,0),(188,v.get('public',1)),(196,0),(200,v.get('nat',1)),(260,0),(168,0),(180,0)]:put(m,q+off,value)
        m.write(q+264,bytes(2));m.write(q+272,bytes([0]))
        for i in range(4):value=call(0x201d5d4,[]);call(DIV,[value,255]);m.write(q+132+i,bytes([mod(s32(value),255)&255]))
        for i in range(10):put(m,q+216+i*4,0xffffffff)
        put(m,q+256,0);call(0x201b208,[q+276,0,3200]);call(0x20b75cc,[]);ret=1
        if v.get('public',1):
            host=HOST
            if not m.read(HOST,1)[0]:call(0x200616c,[TMP,0x20e2534,H]);host=TMP
            ret=call(0x20b760c,[host,27900,q+204,0])
        result=3 if ret==0 else 0
    else:raise ValueError('Unknown selected ordinary C body')
    return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result


def cases(address):
    def base(**kw):return dict(entry=address,**kw)
    if address==0x20b70c8:
        rows=[base(magic=magic,ptype=ptype,length=length,found=found)for magic in [0,1,-1]for ptype in [0,5,7,255]for length in [-1,0,19,20,21,64]for found in [False,True]]
        rows +=[base(magic=1,ptype=0,length=21,found=True,afterMagicType=ptype,mutateInputAfterCopy=True)for ptype in [0,5,7]];return rows
    if address==0x20b718c:return[base(static=static,public=public,name=name,override=override,dnsResult=result,random=random)for static in [False,True]for public in [0,1,-1]for name in ['game','g']for override in ['', 'override.local']for result in [0,1,-1]for random in [[0,1,254,255],[0xffffffff,0x80000000,0x7fffffff,0xffffff00]]]
    if address==0x20b7334:return[base(static=static,nullArgument=null,public=public,mutateHelpers=mutate)for static in [False,True]for null in [False,True]for public in [0,1,0xffffffff]for mutate in [False,True]]
    if address==0x20b7360:return[base(read=read,receives=receives,nextAddrLen=length)for read in [0,1,0xffffffff]for receives in [[],[-1],[0],[3,-1,0,255],[-2,1]]for length in [8,6]]
    if address==0x20b73c0:
        rows=[base(socket=sock,listed=listed,requested=req,now=now,now2=now,lastHB=100,lastKA=100,thumb=thumb)for sock in [-1,7]for listed in [-1,0,1,3,4,99]for req in [0,1]for now in [99,100,10100,10101,20100,20101,60100,60101,0xfffffff0]for thumb in [False,True]]
        rows +=[base(listed=1,now=20000,now2=30000,afterSendListed=9),base(listed=0,now=1,now2=2,afterClockHB=0xfffffff0),base(listed=0,now=0xffffffff,now2=0,lastHB=0xfffffffe,lastKA=0xfffffffe)];return rows
    if address==0x20b748c:return[base(static=static,nullArgument=null,public=public,lastHB=last,now=now,requested=7)for static in [False,True]for null in [False,True]for public in [0,1,-1]for last,now in [(100,100),(100,10099),(100,10100),(0xfffffff0,30),(0xffffff00,20000)]]
    if address==0x20b74d4:return[base(static=static,nullArgument=null,public=public,socket=sock,read=read)for static in [False,True]for null in [False,True]for public in [0,1,-1]for sock in [-1,-2,0,7]for read in [0,1,-1]]
    if address==0x20b75cc:return[base(hostPresent=present,ipCount=count)for present in [False,True]for count in range(6)]
    if address==0x20b760c:return[base(nullHost=null,port=port,save=save,inet=inet,name=name,hostPresent=present)for null in [False,True]for port in [-1,0,1,27900,65536]for save in [False,True]for inet in [0,0x01020304,0xffffffff]for name in ['example','255.255.255.255']for present in [False,True]]
    if address==0x20b78ac:return[base(scanIP=ip,scanPort=port,oldIP=oldIP,oldPort=oldPort,thumb=thumb)for ip in [0,1,0x01020304,0xffffffff]for port in [0,1,0xffff,0x10000,0x123480ff]for oldIP in [0,0x04030201]for oldPort in [0,1,0x80ff]for thumb in [False,True]]
    raise ValueError('No selected family models')
