from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32

C,REMOTE,D,CB,OUT,SK,ST=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x2176000
SP,STOP,TMP,MAGIC,DIV=0x2701000,0x27e0000,0x2700800,0,0
ARITY={0x20b5fac:3,0x20b3ff4:4,0x20b402c:4,0x20b5cd0:1,0x20b4354:1,0x20a8f14:1}


def dynamic_callbacks(v):return{}


def initial(address,v):
    if address!=0x20b438c:raise ValueError('Outside original connect identity')
    m=Memory({C:bytes(160),REMOTE:b'example:1234\0'+bytes(50),D:bytes((i*17+3)&255 for i in range(64)),CB:bytes.fromhex('01001111000022220100333300004444'),OUT:bytes.fromhex('ddccbbaa'),SK:bytes(76),ST:bytes(16),SP-0x1000:bytes(0x1000)})
    put(m,C+12,0);put(m,C+24,v.get('finalResult',2));put(m,C+32,0xaabbccdd);put(m,C+36,v.get('level',0));return m,[SK,OUT if v.get('out',True)else 0,REMOTE,D,v.get('length',32)&0xffffffff,v.get('timeout',1000)&0xffffffff,CB,v.get('blocking',0)&0xffffffff]


def effect(at,a,m,v):
    result=1;norm=a[:]
    if at==0x20b5fac:
        norm=[m.read(a[0],12).hex()];put(m,a[1],v.get('ip',0x04030201));m.write(a[2],v.get('port',1234).to_bytes(2,'little'));result=v.get('parse',1)
    elif at==0x20b3ff4:put(m,a[1],C);norm=[a[0],a[2],a[3]];result=v.get('newResult',0)
    elif at==0x20b402c:norm=[a[0],a[1],a[2],m.read(a[3],16).hex(),word(m,C+32)];result=v.get('startResult',0)
    elif at==0x20b5cd0:put(m,ST+8,1)
    elif at==0x20b4354:
        i=word(m,ST);steps=v.get('steps',[5]);put(m,ST,i+1);put(m,C+12,steps[min(i,len(steps)-1)]);put(m,C+24,v.get('finalResult',2));put(m,C+36,word(m,C+36)+v.get('levelDelta',0))
    elif at==0x20a8f14:put(m,ST+4,word(m,ST+4)+1)
    else:raise ValueError('Unqualified original connect import')
    return result&0xffffffff,norm


def model(address,v):
    m,args=initial(address,v);calls=[];result=4
    def call(at,args):
        value,norm=effect(at,[a&0xffffffff for a in args],m,v);calls.append((hex(at),norm));return value
    parsed=call(0x20b5fac,[REMOTE,TMP,TMP+4]);ip=word(m,TMP);port=int.from_bytes(m.read(TMP+4,2),'little');swapped=int.from_bytes(ip.to_bytes(4,'little'),'big')
    if parsed and ip and port and swapped&0xe0000000!=0xe0000000:
        result=call(0x20b3ff4,[SK,TMP+8,ip,port])
        if result==0:
            put(m,C+32,v.get('timeout',1000));result=call(0x20b402c,[C,D,v.get('length',32),CB])
            if result:call(0x20b5cd0,[C])
            elif not v.get('blocking',0):
                if v.get('out',True):put(m,OUT,C)
            else:
                put(m,C+36,word(m,C+36)+1)
                while True:
                    call(0x20b4354,[SK])
                    if s32(word(m,C+12))>=5:break
                    call(0x20a8f14,[1])
                put(m,C+36,word(m,C+36)-1)
                if word(m,C+12)==5:put(m,OUT,C)
                result=word(m,C+24)
    return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result


def cases(address):
    if address!=0x20b438c:raise ValueError('No original connect vectors')
    rows=[dict(parse=parse,ip=ip,port=port)for parse in [0,1,0x80000000]for ip in [0,0x04030201,0x000000e0,0xffffffff]for port in [0,1,65535]]
    rows +=[dict(newResult=new,startResult=start,out=out,length=length,timeout=timeout)for new in [0,1,0xffffffff]for start in [0,2,0xffffffff]for out in [False,True]for length in [-1,0,32]for timeout in [-1,1000]]
    rows +=[dict(blocking=blocking,steps=steps,level=level,levelDelta=delta,finalResult=result,timeout=timeout)for blocking in [1,-1]for steps in [[5],[0,4,5],[-1,4,7]]for level in [0,3]for delta in [0,2]for result in [0,2,0xffffffff]for timeout in [-1,1000]]
    rows.append(dict(blocking=1,out=False,steps=[7],finalResult=2));return rows
