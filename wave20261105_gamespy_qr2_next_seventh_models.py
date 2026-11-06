import re
import struct
from project import ROOT
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put

I,OUTIP,OUTPORT,H,A,V=0x2170000,0x2172000,0x2172010,0x2174000,0x2175000,0x2176000
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700800,0x20d8e04
ARITY={0x201d948:2,0x201b19c:3,0x201f274:1,0x20a8c84:1,0x209046c:1}


def cstring(memory,address):
    out=bytearray()
    for index in range(1024):
        value=memory.read(address+index,1)
        if value==b'\0':return bytes(out)
        out.extend(value)
    raise ValueError('Caller bounded string escaped termination')


def initial(address,v):
    if address!=0x20b5fac:raise ValueError('Caller outside seventh source scope')
    raw=bytes.fromhex(v.get('text',''));image=(ROOT/'extract/arm9/arm9.bin').read_bytes();regions={I:raw+b'\0'+bytes(1023-len(raw)),OUTIP:bytes.fromhex('efbeadde'),OUTPORT:bytes.fromhex('efbe'),H:bytes(16),A:bytes(4),V:bytes(4),MAGIC:image[MAGIC-0x2000000:MAGIC-0x2000000+256],SP-0x1000:bytes(0x1000)}
    memory=Memory(regions);put(memory,H+12,A);put(memory,A,V);put(memory,V,v.get('dnsValue',0x08080808))
    return memory,[0 if v.get('nullString') else I,0 if v.get('nullIp') else OUTIP,0 if v.get('nullPort') else OUTPORT]


def atoi(raw):
    match=re.match(rb'^[\t\n\r\v\f ]*([+-]?\d+)',raw)
    value=int(match[1]) if match else 0
    if not -2147483648<=value<=2147483647:raise ValueError('Undefined C atoi overflow is outside the model')
    return value&0xffffffff


def effect(target,args,memory,v):
    a=[value&0xffffffff for value in args];result=0;normalized=a[:]
    if target==0x201d948:
        raw=cstring(memory,a[0]);normalized=[raw.hex(),a[1]];offset=raw.find(bytes([a[1]&255]));result=a[0]+offset if offset>=0 else 0
    elif target==0x201b19c:
        raw=memory.read(a[1],a[2]);normalized=[raw.hex(),a[2]];memory.write(a[0],raw);result=a[0]
    elif target==0x201f274:raw=cstring(memory,a[0]);normalized=[raw.hex()];result=atoi(raw)
    elif target==0x20a8c84:raw=cstring(memory,a[0]);normalized=[raw.hex()];result=v.get('inetValue',0x04030201)
    elif target==0x209046c:raw=cstring(memory,a[0]);normalized=[raw.hex()];result=H if v.get('dnsSuccess',1) else 0
    else:raise ValueError('Unqualified seventh-packet supplied contract')
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[];result=1;ip=port=0
    def call(target,*arguments):
        returned,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return returned
    if args[0] and cstring(memory,I):
        raw=cstring(memory,I);colon=call(0x201d948,I,58);host=I
        if colon:
            offset=colon-I
            if offset:
                call(0x201b19c,TMP,I,offset);memory.write(TMP+offset,b'\0');host=TMP
            else:host=0
            port_raw=cstring(memory,colon+1)
            if any(not 48<=byte<=57 for byte in port_raw):result=0
            else:
                port_value=call(0x201f274,colon+1)
                if port_value&0x80000000 or port_value>65535:result=0
                else:port=port_value
        if result and host:
            ip=call(0x20a8c84,host)
            if ip==0xffffffff:
                entry=call(0x209046c,host)
                if not entry:result=0
                else:ip=word(memory,word(memory,word(memory,entry+12)))
    if result:
        if args[1]:put(memory,args[1],ip)
        if args[2]:put(memory,args[2],port,2)
    external={at:bytes(raw) for at,raw in memory.regions.items() if at!=SP-0x1000}
    return external,calls,'word',result


def cases(address):
    if address!=0x20b5fac:raise ValueError('Seventh caller lacks vectors')
    strings=[None,b'',b':',b':0',b':1',b':65535',b':65536',b':2147483647',b'127.0.0.1',b'host:9',b'host',b':-1',b':+1',b':1x',b': 1',b':\xff',b'a'*255+b':1']
    vectors=[dict(text=(raw or b'').hex(),nullString=raw is None,nullIp=null_ip,nullPort=null_port,inetValue=ip,dnsSuccess=dns) for raw in strings for null_ip in [False,True] for null_port in [False,True] for ip in [0x04030201,0xffffffff] for dns in [0,1]]
    vectors += [dict(text=(b':'+bytes([value])).hex(),inetValue=0xffffffff,dnsSuccess=0) for value in range(256)]
    return vectors
