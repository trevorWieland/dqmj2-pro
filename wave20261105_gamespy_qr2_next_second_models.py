import base64
import struct
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put,signed

Q,D,B,I,O,T,K=0x2170000,0x20e17a0,0x2172000,0x2174000,0x2176000,0x2178000,0x217a000
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700f00,0x20e1718
INDEX,ARRAY,CURRENT=0x21d2948,0x21d294c,0x20e179c
ALPHABET=b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
ARITY={0x209073c:1,0x200616c:4,0x201d69c:1,0x201b19c:3,0x20b7684:1,0x201d6b8:2,0x20b7740:4,0x20b76bc:3}


def cstring(memory,address):
    result=bytearray()
    for index in range(2048):
        value=memory.read(address+index,1)
        if value==b'\x00':return bytes(result)
        result.extend(value)
    raise ValueError('Supplied bounded string contract escaped termination')


def encode(raw):return base64.b64encode(raw+bytes((-len(raw))%3))


def initial(address,v):
    raw=bytes.fromhex(v.get('data',''));regions={Q:bytes([0x77])*176,D:bytes([0x55])*176,B:bytes([0xcd])*1404,I:raw+b'\0'+bytes([0xee])*(1023-len(raw)),O:bytes([0xbb])*1024,T:bytes(64),K:bytes([0xaa])*260,INDEX:bytes(4),ARRAY:bytes([0x99])*44,CURRENT:struct.pack('<I',D),MAGIC:b'%s:%d\0',0x20e1720:b'%s\0',0x20e1724:b':%d\0',SP-0x1000:bytes(0x1000)}
    memory=Memory(regions);put(memory,B+1400,v.get('length',0));put(memory,K+256,v.get('count',0));put(memory,INDEX,v.get('index',0));memory.write(Q+68,b'secret\0');memory.write(D+68,b'other\0')
    args={0x20b5f38:[v.get('ip',0),v.get('port',0),0 if v.get('static',False) else O],0x20b72f8:[0 if v.get('default') else Q,v.get('callback',0)],0x20b730c:[0 if v.get('default') else Q,v.get('callback',0)],0x20b7320:[0 if v.get('default') else Q,v.get('callback',0)],0x20b753c:[K,v.get('key',1)],0x20b7588:[B,I],0x20b76bc:[I,v.get('size',len(raw)),O],0x20b7848:[Q,B,I,v.get('challengeLength',len(raw)+1)]}
    if address==0x20b7848 and v.get('unterminated'):memory.write(I+v.get('challengeLength',len(raw)+1)-1,b'X')
    return memory,args[address]


def effect(target,args,memory,v):
    a=[value&0xffffffff for value in args];normalized=a[:];result=0
    if target==0x209073c:
        text='.'.join(str(byte) for byte in a[0].to_bytes(4,'little')).encode();memory.write(T,text+b'\0');result=T
    elif target==0x200616c:
        fmt=cstring(memory,a[1])
        if fmt==b'%s:%d':text=cstring(memory,a[2])+b':'+str(a[3]).encode();normalized=a[:4]
        elif fmt==b'%s':text=cstring(memory,a[2]);normalized=a[:3]
        elif fmt==b':%d':text=b':'+str(a[2]).encode();normalized=a[:3]
        else:raise ValueError('Unexpected original address format')
        memory.write(a[0],text+b'\0');result=len(text)
    elif target==0x201d69c:normalized=[cstring(memory,a[0]).hex()];result=len(cstring(memory,a[0]))
    elif target==0x201b19c:
        raw=memory.read(a[1],a[2]);normalized=[a[0],raw.hex(),a[2]];memory.write(a[0],raw);result=a[0]
    elif target==0x20b7684:result=ALPHABET[a[0]] if a[0]<64 else 0
    elif target==0x201d6b8:
        raw=cstring(memory,a[1]);normalized=[raw.hex()];memory.write(a[0],raw+b'\0');result=a[0]
    elif target==0x20b7740:
        raw=memory.read(a[2],a[3]);key=memory.read(a[0],a[1]);normalized=[key.hex(),raw.hex(),a[3]]
        memory.write(a[2],bytes(byte^0x5a for byte in raw));result=0x12345678
    elif target==0x20b76bc:
        size=max(0,signed(a[1]));raw=memory.read(a[0],size);normalized=[raw.hex(),a[1],a[2]];memory.write(a[2],encode(raw)+b'\0');result=0xabcdef01
    else:raise ValueError('Unqualified second-packet supplied contract')
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[];result=0;contract='void'
    def call(target,*arguments):
        value,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return value
    if address==0x20b5f38:
        contract='word';ip,port,string=args
        if not string:
            index=word(memory,INDEX)^1;put(memory,INDEX,index);string=ARRAY+22*index
        if ip:
            text=call(0x209073c,ip)
            if port:call(0x200616c,string,MAGIC,text,port)
            else:call(0x200616c,string,0x20e1720,text)
        elif port:call(0x200616c,string,0x20e1724,port)
        else:memory.write(string,b'\0')
        result=string
    elif address in [0x20b72f8,0x20b730c,0x20b7320]:
        record=args[0] or word(memory,CURRENT);offset={0x20b72f8:160,0x20b730c:164,0x20b7320:168}[address];put(memory,record+offset,args[1])
    elif address==0x20b753c:
        contract='word';count=signed(word(memory,K+256));key=signed(args[1]&0xffffffff)
        if 0<=count<254 and 1<=key<=254:memory.write(K+count,bytes([key]));put(memory,K+256,count+1);result=1
    elif address==0x20b7588:
        contract='word';length=signed(word(memory,B+1400));copy=min(call(0x201d69c,I)+1,1400-length)
        if copy>0:call(0x201b19c,B+length,I,copy);put(memory,B+1400,length+copy);memory.write(B+length+copy-1,b'\0');result=1
    elif address==0x20b76bc:
        size=max(0,signed(args[1]&0xffffffff));raw=memory.read(I,size);expected=encode(raw);quartets=[]
        for start in range(0,size,3):
            number=int.from_bytes(raw[start:start+3].ljust(3,b'\0'),'big');quartets.extend((number>>shift)&63 for shift in [18,12,6,0])
        output=bytes(call(0x20b7684,value) for value in quartets)
        if output!=expected:raise ValueError('Independent Python base64 oracle disagrees with supplied encoding primitive')
        memory.write(O,expected+b'\0')
    elif address==0x20b7848:
        length=signed(args[3]&0xffffffff)
        if 1<=length<=65 and memory.read(I+length-1,1)==b'\0':
            call(0x201d6b8,TMP,I);key_length=call(0x201d69c,Q+68);call(0x20b7740,Q+68,key_length,TMP,length-1)
            destination=B+word(memory,B+1400);call(0x20b76bc,TMP,length-1,destination);count=call(0x201d69c,destination);put(memory,B+1400,word(memory,B+1400)+count+1)
    else:raise ValueError('Caller outside second packet')
    external={at:bytes(raw) for at,raw in memory.regions.items() if at!=SP-0x1000}
    return external,calls,contract,result&0xffffffff


def cases(address):
    if address==0x20b5f38:return [dict(ip=ip,port=port,static=static,index=index) for ip in [0,0x0100007f,0x04030201,0xffffffff] for port in [0,1,65535] for static in [False,True] for index in [0,1]]
    if address in [0x20b72f8,0x20b730c,0x20b7320]:return [dict(default=default,callback=callback) for default in [False,True] for callback in [0,0x2008be0,0x20b4135]]
    if address==0x20b753c:return [dict(count=count,key=key) for count in [0,1,253,254,255] for key in [-1,0,1,2,253,254,255,0x7fffffff]]
    if address==0x20b7588:return [dict(length=length,data=data.hex()) for length in [0,1,1397,1398,1399,1400,1401] for data in [b'',b'A',b'AB',b'hello',b'A'*254,b'A\0B',bytes([0x80,0xff])]]
    if address==0x20b76bc:
        data=[b'',b'A',b'AB',b'ABC',b'ABCD',bytes([255]),bytes([255])*4,bytes(range(64))]
        data+=[bytes([value]) for value in range(256)]+[bytes([value,255-value,value^0xa5]) for value in range(256)]
        return [dict(data=raw.hex(),size=len(raw)) for raw in data]+[dict(data=b'A'.hex(),size=-1)]
    if address==0x20b7848:
        vectors=[dict(data=raw.hex(),challengeLength=len(raw)+1,length=length,unterminated=bad) for raw in [b'',b'A',b'AB',b'ABC',b'challenge',bytes(range(1,65))] for length in [0,3,10] for bad in [False,True]]
        return vectors+[dict(data=b'A'.hex(),challengeLength=length,length=0) for length in [-1,0,66,100]]
    raise ValueError('No second-packet vector family')
