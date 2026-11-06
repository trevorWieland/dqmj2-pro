from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32,z

Q,S,NUM,IPS,INET,ST=0x2170000,0x2172000,0x21d2ec8,0x21d2ecc,0x2174000,0x2175000
SP,STOP,B,T,K,MAGIC,DIV=0x2701000,0x27e0000,0x2700400,0x2700a00,0x2700fb0,0,0
STRINGS={0x20e25cc:b'localip%d',0x20e25d8:b'localport',0x20e25e4:b'natneg',0x20e25ec:b'1',0x20e25f0:b'0',0x20e25f4:b'statechanged',0x20e2604:b'gamename',0x20e2610:b'publicip',0x20e261c:b'publicport'}
ARITY={0x20b7828:3,0x20a8c34:6,0x20a8ef8:0,0x200616c:3,0x20b7588:2,0x209073c:1,0x20b7568:2,0x201b19c:3,0x20b7ac8:8}


def dynamic_callbacks(v):return{}
def half(m,a):return int.from_bytes(m.read(a,2),'little')
def ph(m,a,value):m.write(a,(value&65535).to_bytes(2,'little'))


def initial(address,v):
    m=Memory({Q:bytes([0xa5])*3476,S:bytes([0x7f,2])+v.get('port',0x1234).to_bytes(2,'little')+v.get('ip',0x01020304).to_bytes(4,'little'),NUM:v.get('ipCount',0).to_bytes(4,'little'),IPS:bytes(20),INET:bytes(32),ST:bytes(16),SP-0x1000:bytes(0x1000),**{a:s+bytes([0])for a,s in STRINGS.items()}})
    for i in range(5):put(m,IPS+i*4,0x01020304+i*0x11010101)
    for off,val in [(0,v.get('socket',7)),(168,v.get('publicCallback',0)),(172,0x11112222),(176,0x33334444),(180,7),(192,v.get('qport',27900)),(200,v.get('nat',1)),(260,0x10203040)]:put(m,Q+off,val)
    m.write(Q+132,bytes.fromhex('11223344'));m.write(Q+4,b'game-name\0');m.write(Q+204,bytes.fromhex('7f02345604030201'));ph(m,Q+264,0x80ff)
    if address==0x20b8010:
        for i in range(200):
            at=Q+276+i*16;m.write(at,bytes([0x66,0x77,0x88,0x99]));put(m,at+4,0x0a000001+i);put(m,at+8,0x11223344+i);put(m,at+12,0xabcdef01+i)
        if v['slot']>=0:
            at=Q+276+v['slot']*16;m.write(at+2,m.read(S+2,6));put(m,at+8,v['key']if v['match']else v['key']^1)
        if v.get('earlierDuplicate'):
            m.write(Q+276+2,m.read(S+2,6));put(m,Q+276+8,v['key']^1)
        return m,[Q,S,v['key']]
    if address==0x20b8334:return m,[Q]
    if address==0x20b8380:return m,[Q,v.get('change',0)&0xffffffff]
    raise ValueError('Outside first follow-up source scope')


def append(m,buf,raw):
    length=word(m,buf+1400)
    if length+len(raw)>1400:return 0
    m.write(buf+length,raw);put(m,buf+1400,length+len(raw));return 1


def effect(at,a,m,v):
    result=0x12345678;norm=a[:]
    if at==0x20b7828:
        before=word(m,a[0]+1400);length=v.get('initialLen',5);raw=bytes([a[1]&255])+m.read(a[2],4);m.write(a[0],(raw*281)[:length]);put(m,a[0]+1400,length);norm=[before,a[1],m.read(a[2],4).hex()]
    elif at==0x20a8c34:norm=[a[0],m.read(a[1],a[2]).hex(),a[2],a[3],m.read(a[4],8).hex(),a[5]];result=v.get('sendResult',0xffffffff)
    elif at==0x20a8ef8:
        result=v.get('now',0)
        if 'afterClockRequested'in v:put(m,Q+180,v['afterClockRequested'])
    elif at==0x200616c:raw=('localip%d'%a[2]).encode();m.write(a[0],raw+bytes([0]));norm=[z(m,a[1]).decode(),a[2]];result=len(raw)
    elif at==0x209073c:
        raw='.'.join(str(byte)for byte in a[0].to_bytes(4,'little')).encode();m.write(INET,raw+bytes([0]));norm=[a[0]];result=INET
        if 'afterInetCount'in v:put(m,NUM,v['afterInetCount'])
    elif at==0x20b7588:raw=z(m,a[1])+bytes([0]);norm=[raw.hex()];result=append(m,a[0],raw)
    elif at==0x20b7568:raw=str(s32(a[1])).encode()+bytes([0]);norm=[a[1]];result=append(m,a[0],raw)
    elif at==0x201b19c:raw=m.read(a[1],a[2]);m.write(a[0],raw);norm=[raw.hex(),a[2]];result=a[0]
    elif at==0x20b7ac8:
        count=word(m,ST);put(m,ST,count+1);length=word(m,a[1]+1400);norm=[a[0],length,a[2:]];target=1400 if v.get('fallback')and count==0 else min(1400,length+v.get('replyBytes',7));m.write(a[1]+length,bytes([0x91+count])*(target-length));put(m,a[1]+1400,target)
    else:raise ValueError(('Unqualified original first-packet helper',hex(at)))
    return result&0xffffffff,norm


def model(address,v):
    m,args=initial(address,v);calls=[];result=0;contract='void'
    def call(at,args):
        value,norm=effect(at,[a&0xffffffff for a in args],m,v);calls.append((hex(at),norm));return value
    if address==0x20b8010:
        contract='ARM R0 word'
        for i in range(200):
            at=Q+276+i*16
            if word(m,at+4)==word(m,S+4)and half(m,at+2)==half(m,S+2)and word(m,at+8)==v['key']:
                put(m,at+4,0);ph(m,at+2,0);result=1;break
    elif address==0x20b8334:
        put(m,B+1400,0);call(0x20b7828,[B,8,Q+132]);call(0x20a8c34,[word(m,Q),B,word(m,B+1400),0,Q+204,8]);put(m,Q+176,call(0x20a8ef8,[]))
    else:
        change=v.get('change',0)&0xffffffff;put(m,B+1400,0);call(0x20b7828,[B,3,Q+132]);i=0
        while i<s32(word(m,NUM)):
            call(0x200616c,[K,0x20e25cc,i]);call(0x20b7588,[B,K]);ip=call(0x209073c,[word(m,IPS+i*4)]);call(0x20b7588,[B,ip]);i+=1
        for at,args in [(0x20b7588,[B,0x20e25d8]),(0x20b7568,[B,word(m,Q+192)]),(0x20b7588,[B,0x20e25e4]),(0x20b7588,[B,0x20e25ec if word(m,Q+200)else 0x20e25f0])]:call(at,args)
        if change:call(0x20b7588,[B,0x20e25f4]);call(0x20b7568,[B,change])
        call(0x20b7588,[B,0x20e2604]);call(0x20b7588,[B,Q+4])
        if word(m,Q+168):call(0x20b7588,[B,0x20e2610]);call(0x20b7568,[B,word(m,Q+260)]);call(0x20b7588,[B,0x20e261c]);call(0x20b7568,[B,half(m,Q+264)])
        if change!=2:
            length=word(m,B+1400);call(0x201b19c,[T,B,length]);put(m,T+1400,length);call(0x20b7ac8,[Q,T,255,0,255,0,255,0])
            if word(m,T+1400)>=1400:put(m,T+1400,length);call(0x20b7ac8,[Q,T,255,0,0,0,0,0])
            call(0x201b19c,[B,T,word(m,T+1400)]);put(m,B+1400,word(m,T+1400))
        elif word(m,B+1400)<1400:
            length=word(m,B+1400);m.write(B+length,bytes([0]));put(m,B+1400,length+1)
        call(0x20a8c34,[word(m,Q),B,word(m,B+1400),0,Q+204,8]);now=call(0x20a8ef8,[]);put(m,Q+172,now);put(m,Q+176,now)
        if change:put(m,Q+180,0)
    return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result


def cases(address):
    if address==0x20b8010:
        rows=[dict(slot=slot,key=key,match=match,ip=ip,port=port)for slot in [-1,0,5,199]for key in [0,0x12345678,0xffffffff]for match in [False,True]for ip,port in [(0x01020304,0x1234),(0,0),(0xffffffff,65535)]]
        rows.append(dict(slot=5,key=0x12345678,match=True,earlierDuplicate=True));return rows
    if address==0x20b8334:return[dict(initialLen=length,socket=sock,now=now)for length in [5,31]for sock in [-1,0,7]for now in [0,0xffffffff]]
    if address!=0x20b8380:raise ValueError('No first follow-up vectors')
    rows=[dict(ipCount=count,change=change,nat=nat,publicCallback=cb,fallback=fallback,now=0x12345678)for count in [0,1,5]for change in [0,1,2,-1]for nat in [0,1,-1]for cb in [0,1]for fallback in [False,True]]
    rows +=[dict(initialLen=length,change=change,ipCount=1,nat=1,publicCallback=1,fallback=fallback)for length in [1399,1400]for change in [0,2]for fallback in [False,True]]
    rows +=[dict(ipCount=5,afterInetCount=1,change=0),dict(ipCount=1,afterInetCount=5,change=1),dict(ipCount=0,change=0,afterClockRequested=99),dict(ipCount=0,change=1,afterClockRequested=99)];return rows
