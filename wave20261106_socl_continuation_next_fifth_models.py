import hashlib
import math
import struct
from wave20261105_socket_thumb_next_memory import Memory

CTX,INPUT,SP,STOP=0x02400000,0x02420000,0x027f0000,0x027d0000
OUT=INPUT
SPECS={'02092cb8':232}
NAMES=list(SPECS)
INITIAL=[0x67452301,0xefcdab89,0x98badcfe,0x10325476]
CONSTANTS=[int(abs(math.sin(i+1))*(1<<32))for i in range(64)]
INDICES=list(range(16))+[(5*i+1)&15 for i in range(16)]+[(3*i+5)&15 for i in range(16)]+[(7*i)&15 for i in range(16)]
ROTATIONS=[7,12,17,22,5,9,14,20,4,11,16,23,6,10,15,21]


def verify_reference_tables(main):
    if main[0xde898:0xde8d8]!=bytes(INDICES) or main[0xde918:0xdea18]!=struct.pack('<64I',*CONSTANTS):raise ValueError('Actual original tables differ from independent message-word and sine-derived semantics')


def fixtures(name):
    rows=[]
    for message in [b'',b'abc',b'x'*55,b'Native caller block model']:
        block=message+b'\x80'+bytes(55-len(message))+(len(message)*8).to_bytes(8,'little');rows.append(dict(block=block.hex(),state=INITIAL,alias=False,inputOffset=0,message=message.hex()))
    rows+=[dict(block=bytes(64).hex(),state=[0xffffffff]*4,alias=False,inputOffset=4,message=None),dict(block=(bytes([255])*64).hex(),state=[0,1,0xfffffffe,0xffffffff],alias=False,inputOffset=0,message=None)]
    rows+=[dict(block=bytes((i*19+7)&255 for i in range(64)).hex(),state=INITIAL,alias=True,inputOffset=0,message=None)]
    return rows


def scenario(name,f,ordinal):
    memory=Memory({CTX:128,INPUT:128},ordinal)
    for i,value in enumerate(f['state']):memory.set(CTX+4*i,value)
    source=CTX if f['alias']else INPUT+f['inputOffset'];block=bytes.fromhex(f['block']);memory.put(source,block);initial=memory.snapshot();start=[memory.get(CTX+4*i)for i in range(4)];words=struct.unpack('<16I',block);a,b,c,d=start
    for i in range(64):
        if i<16:boolean=(b&c)|((~b)&d)
        elif i<32:boolean=(b&d)|(c&(~d))
        elif i<48:boolean=b^c^d
        else:boolean=c^(b|(~d))
        value=(a+boolean+CONSTANTS[i]+words[INDICES[i]])&0xffffffff;rotation=ROTATIONS[(i//16)*4+i%4];rotated=((value<<rotation)|(value>>(32-rotation)))&0xffffffff;a,b,c,d=d,(b+rotated)&0xffffffff,b,c
    final=[(x+y)&0xffffffff for x,y in zip(start,[a,b,c,d])]
    for i,value in enumerate(final):memory.set(CTX+4*i,value)
    if f['message'] is not None and struct.pack('<4I',*final)!=hashlib.md5(bytes.fromhex(f['message'])).digest():raise ValueError('Independent single-block model disagrees with standard-library digest')
    buffer=SP-84;actions=[dict(address=0x2092ca8,args=[buffer,source,64],returned=0xa7338822,checks=[(base,raw)for base,raw in initial.items()],mutations=[(buffer,block)],stackWords=[])]
    return dict(initial=initial,regions=memory.snapshot(),args=[CTX,source,0x22334455,0x33445566],actions=actions,result=None,volatileStateReads=None,readable=[(CTX,128),(INPUT,128),(0x020de898,64),(0x020de918,256)],decodedBuffer=(buffer,block))
