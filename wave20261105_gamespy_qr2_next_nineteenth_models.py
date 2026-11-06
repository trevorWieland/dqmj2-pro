from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32,mod

Q,S,B,ST=0x2170000,0x2172000,0x2173000,0x2174000
SP,STOP,MAGIC=0x2701000,0x27e0000,0
DIV=0x2026144
ARITY={DIV:2,0x20a8ef8:0,0x201d5d4:0,0x20b7568:2}


def dynamic_callbacks(v):return{}


def initial(address,v):
    m=Memory({Q:bytes(3476),S:bytes([0x7f,0x42])+v.get('port',0x1234).to_bytes(2,'little')+v.get('ip',0x01020304).to_bytes(4,'little'),B:bytes([0xa5])*1404,ST:bytes(32),SP-0x1000:bytes(0x1000)})
    if address==0x20b7ea8:
        for i in range(10):put(m,Q+216+i*4,v['message']if i==v['foundIndex']else 0x90000000+i)
        put(m,Q+256,v['current']);return m,[Q,v['message']]
    if address!=0x20b7eec:raise ValueError('Outside reserved recent/IP subset')
    m.write(Q+272,bytes([v['backend']]))
    for i in range(200):
        at=Q+276+i*16;m.write(at,bytes([i&255,0x66])+bytes.fromhex('a1b2'));put(m,at+4,0x0a000001+i);put(m,at+8,0x10203040+i);put(m,at+12,0xfefefefe-i)
    if v['free']>=0:put(m,Q+276+v['free']*16+4,0)
    chosen=[i for i in range(200)if i!=v['free']][:v['duplicates']]
    for i in chosen:
        at=Q+276+i*16;m.write(at+2,m.read(S+2,2));put(m,at+4,word(m,S+4))
    return m,[Q,B,S]


def effect(at,a,m,v):
    result=0x12345678;norm=a[:]
    if at==DIV:
        av,bv=s32(a[0]),s32(a[1]);result=(av-mod(av,bv))//bv
    elif at==0x20a8ef8:
        result=v['now']
        if 'afterClockBackend'in v:m.write(Q+272,bytes([v['afterClockBackend']]))
    elif at==0x201d5d4:
        i=word(m,ST);put(m,ST,i+1);result=v['random'][i]
    elif at==0x20b7568:
        put(m,B+1400,0x12340000|(a[1]&65535));result=v.get('addResult',0)
    else:raise ValueError(('Unqualified original import',hex(at)))
    return result&0xffffffff,norm


def model(address,v):
    m,args=initial(address,v);calls=[];result=0
    def call(at,args):
        value,norm=effect(at,[a&0xffffffff for a in args],m,v);calls.append((hex(at),norm));return value
    if address==0x20b7ea8:
        if any(word(m,Q+216+i*4)==v['message']for i in range(10)):result=1
        else:
            numerator=(word(m,Q+256)+1)&0xffffffff;call(DIV,[numerator,10]);index=mod(s32(numerator),10);put(m,Q+256,index);put(m,Q+216+index*4,v['message'])
    else:
        now=call(0x20a8ef8,[])
        if not(m.read(Q+272,1)[0]&128):call(0x20b7568,[B,0]);result=1
        else:
            candidates=[i for i in range(200)if word(m,Q+276+i*16+4)==0]
            matches=[i for i in range(200)if word(m,Q+276+i*16+4)==word(m,S+4)and m.read(Q+276+i*16+2,2)==m.read(S+2,2)]
            if len(matches)<=5 and candidates:
                at=Q+276+candidates[0]*16;m.write(at,m.read(S,8));pairs=[]
                for i in range(4):left=call(0x201d5d4,[]);right=call(0x201d5d4,[]);pairs.append(((left<<16)|right)&0xffffffff)
                challenge=((pairs[2]>>24)&255)|((pairs[3]>>8)&0xff00)|((pairs[1]<<8)&0xff0000)|((pairs[0]<<24)&0xff000000)
                put(m,at+8,challenge);put(m,at+12,now);call(0x20b7568,[B,challenge]);result=1
    return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result


def cases(address):
    if address==0x20b7ea8:return[dict(message=key,current=cur,foundIndex=found)for key in [0,0xffffffff,0x12345678]for cur in [-1,0,8,9,10]for found in [-1,0,4,9]]
    if address!=0x20b7eec:raise ValueError('No reserved recent/IP vectors')
    randoms=[[0x1122,0x3344,0x5566,0x7788,0x1234,0x5678,0x1abc,0x2def],[0,1,254,255,256,32767,0x100,0x101]]
    rows=[dict(backend=flag,free=free,duplicates=duplicates,now=now,random=random)for flag in [0,128,255]for free in [-1,0,5,199]for duplicates in [0,5,6]for now in [0,0xffffffff]for random in randoms]
    rows +=[dict(rows[24],backend=before,afterClockBackend=after)for before,after in [(0,128),(128,0)]]
    rows +=[dict(rows[24],backend=128,free=0,duplicates=count,ip=0,port=port)for count in [0,5,6]for port in [0,0xffff]]
    return rows
