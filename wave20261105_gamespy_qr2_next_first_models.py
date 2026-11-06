import struct

C,S,C2,S2,B,O,A,M=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x2176000,0x2177000
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700f00,0x20e1714


class Memory:
    def __init__(self,regions):self.regions={address:bytearray(value) for address,value in regions.items()}
    def read(self,address,size):
        for start,value in self.regions.items():
            if start<=address and address+size<=start+len(value):return bytes(value[address-start:address-start+size])
        raise ValueError(('Outside bounded model memory',hex(address),size))
    def write(self,address,value):
        for start,data in self.regions.items():
            if start<=address and address+len(value)<=start+len(data):data[address-start:address-start+len(value)]=value;return
        raise ValueError(('Outside bounded model write',hex(address),len(value)))


def word(memory,address):return struct.unpack('<I',memory.read(address,4))[0]
def half(memory,address):return struct.unpack('<H',memory.read(address,2))[0]
def put(memory,address,value,size=4):memory.write(address,(value&((1<<(size*8))-1)).to_bytes(size,'little'))
def signed(value):return value-(1<<32) if value&0x80000000 else value


def initial(address,v):
    regions={C:bytes(160),S:bytes(76),C2:bytes(160),S2:bytes(76),B:bytes([0x77])*512,O:bytes.fromhex('efbeadde'),A:bytes(64),M:bytes(64),MAGIC:bytes.fromhex('fefe00'),SP-0x1000:bytes(0x1000)}
    memory=Memory(regions)
    for c,s in [(C,S),(C2,S2)]:
        for off,val in [(8,s),(12,v.get('state',0)),(16,v.get('initiated',0)),(28,v.get('start',0)),(32,v.get('timeout',100)),(80,B),(84,512),(88,0),(96,A),(136,v.get('last',0)),(144,v.get('pending',1)),(148,v.get('last',0))]:put(memory,c+off,val)
        put(memory,c+100,v.get('serial',65535),2);put(memory,c+102,v.get('expected',0x80ff),2)
        for off,val in [(12,A+0x100+(0x200 if c==C2 else 0)),(16,A+0x200+(0x200 if c==C2 else 0)),(44,v.get('dump',0)),(64,v.get('protocol',0)),(68,v.get('offset',2))]:put(memory,s+off,val)
    for index in range(4):
        put(memory,M+16*index,8*index);put(memory,M+16*index+4,8);put(memory,M+16*index+12,v.get('last',0))
    put(memory,M,v.get('messageStart',8));put(memory,M+4,v.get('messageLength',8))
    at=B+word(memory,M)+v.get('offset',2)+2;memory.write(at,bytes([v.get('messageType',2)&255]))
    arguments={0x20b4134:[C,v.get('now',101)],0x20b4194:[C,v.get('now',1001)],0x20b41d8:[C,v.get('now',101)],0x20b4204:[C,v.get('now',30001)],0x20b4270:[C,v.get('hard',1)],0x20b42a4:[C],0x20b4330:[O,B,v.get('size',512),v.get('incoming',1024),v.get('callback',0x12345679)],0x20b45dc:[C,v.get('result',6),v.get('reason',1)],0x20b514c:[S,0xdeadbeef,v.get('port',65535)],0x20b51dc:[S,0xdeadbeef,v.get('port',65535),v.get('send',1)],0x20b5390:[C,v.get('type',255),v.get('length',16),O],0x20b5900:[C,M]}
    return memory,arguments[address]


def effect(target,args,memory,v):
    a=[value&0xffffffff for value in args];result=v.get('helper',1);normalized=a[:]
    if target==0x20a8640:result=v.get('count',2)
    elif target==0x20a8644:result=M+16*a[1]
    elif target==0x20a89f0:
        normalized=[a[0],word(memory,a[1])]
        if v.get('swap'):put(memory,a[1],C2)
    elif target==0x20a865c:normalized=[a[0],word(memory,a[1])]
    elif target==0x20b42a4:put(memory,a[0]+12,7)
    elif target==0x20b59ac:result=C if v.get('found',1) else 0
    elif target==0x20a8ef8:result=v.get('now',101)
    elif target==0x20b3b50:result=v.get('free',512)
    elif target==0x20b5344:result=v.get('store',1)
    elif target==0x20b4640:result=v.get('memoryError',1)
    elif target==0x20b3b80:
        raw=memory.read(a[1],a[2]);normalized=[a[0],raw.hex(),a[2]];position=word(memory,a[0]+8)
        memory.write(word(memory,a[0])+position,raw);put(memory,a[0]+8,position+len(raw));result=0x77553311
    elif target in [0x20b3b58,0x20b3b64]:
        width=1 if target==0x20b3b58 else 2;position=word(memory,a[0]+8);raw=(a[1]&((1<<(8*width))-1)).to_bytes(width,'big')
        memory.write(word(memory,a[0])+position,raw);put(memory,a[0]+8,position+width);result=0x33557711
    elif target==0x20b45c8:memory.write(a[0]+a[1],(a[2]&65535).to_bytes(2,'big'));result=0x446688aa
    elif target==0x20b4108:
        if result:put(memory,a[0]+136,v.get('newSend',0x12345678))
    elif target==0x20b5900:
        if result:put(memory,a[1]+12,word(memory,a[0]+136))
    return result&0xffffffff,normalized


ARITY={0x20a8640:1,0x20a8644:2,0x20a89f0:2,0x20a865c:2,0x20b42a4:1,0x20b589c:1,0x20b3ca4:4,0x20b5900:2,0x20b57a0:1,0x20b56a8:1,0x20b3d60:2,0x20b5cd0:1,0x20b5668:1,0x20b59d4:6,0x20b59ac:3,0x20b3f00:8,0x20a8ef8:0,0x20b45dc:3,0x20b3b50:1,0x20b4640:1,0x20b5344:3,0x20b3b80:3,0x20b3b58:2,0x20b3b64:2,0x20b45c8:3,0x20b4108:3}


def model(address,v):
    memory,args=initial(address,v);calls=[];result=1;contract='word';now=v.get('now',101)
    def call(target,*arguments):
        value,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return value
    state=signed(word(memory,C+12))
    if address==0x20b4134:
        age=(now-word(memory,C+28))&0xffffffff
        expired=state<5 and ((word(memory,C+16)!=0 and word(memory,C+32)!=0 and age>word(memory,C+32)) or (word(memory,C+16)==0 and state<4 and age>60000))
        if expired:call(0x20b589c,C);call(0x20b42a4,C);result=int(call(0x20b3ca4,C,6,0,0)!=0)
    elif address==0x20b4194:
        count=signed(call(0x20a8640,A))
        for index in range(max(count,0)):
            message=call(0x20a8644,A,index)
            if ((now-word(memory,message+12))&0xffffffff)>1000 and not call(0x20b5900,C,message):result=0;break
    elif address in [0x20b41d8,0x20b4204]:
        threshold,field,target=(100,148,0x20b57a0) if address==0x20b41d8 else (30000,136,0x20b56a8)
        if (address!=0x20b41d8 or word(memory,C+144)!=0) and ((now-word(memory,C+field))&0xffffffff)>threshold:result=int(call(target,C)!=0)
    elif address==0x20b4270:
        contract='void'
        if v.get('hard',1):
            if state<7:call(0x20b42a4,C);call(0x20b589c,C);call(0x20b3d60,C,0);call(0x20b5cd0,C)
        else:put(memory,C+12,6);call(0x20b5668,C)
    elif address==0x20b42a4:
        contract='void'
        if state!=7:
            put(memory,C+12,7);put(memory,TMP,C);call(0x20a89f0,A+0x100,TMP);value=word(memory,TMP);call(0x20a865c,word(memory,word(memory,value+8)+16),TMP)
    elif address==0x20b4330:result=call(0x20b59d4,*args,0)
    elif address==0x20b45dc:
        if state<5:
            if word(memory,C+16):call(0x20b42a4,C);result=int(call(0x20b3ca4,C,args[1],0,0)!=0)
            else:
                if state==4:put(memory,C+20,1)
                call(0x20b42a4,C)
        elif state!=7:call(0x20b42a4,C);result=int(call(0x20b3d60,C,args[2])!=0)
    elif address in [0x20b514c,0x20b51dc]:
        connection=call(0x20b59ac,*args[:3]);result=1
        if word(memory,S+44) and not call(0x20b3f00,S,connection,args[1],args[2],1,0,0,args[3] if address==0x20b51dc else 0):result=0
        elif connection:
            if address==0x20b51dc:result=int(call(0x20b45dc,C,6,1)!=0)
            elif state!=0:result=int(call(0x20b45dc,C,2,1)!=0)
            elif word(memory,C+32) and ((call(0x20a8ef8)-word(memory,C+28))&0xffffffff)>=word(memory,C+32):result=int(call(0x20b45dc,C,6,1)!=0)
    elif address==0x20b5390:
        length=signed(args[2]);free=signed(call(0x20b3b50,C+80));overflow=False
        if free<length or not call(0x20b5344,C,half(memory,C+100),args[2]):
            result=int(call(0x20b4640,C)!=0)
            if result:put(memory,O,1)
        else:
            offset=word(memory,S+68)
            if word(memory,S+64)==2:put(memory,TMP,(length-offset)&65535,2);call(0x20b3b80,C+80,TMP,offset)
            call(0x20b3b80,C+80,MAGIC,2);call(0x20b3b58,C+80,args[1]&255)
            serial=half(memory,C+100);put(memory,C+100,serial+1,2);call(0x20b3b64,C+80,serial);call(0x20b3b64,C+80,half(memory,C+102));put(memory,O,0)
    elif address==0x20b5900:
        start=word(memory,M);offset=word(memory,S+68);call(0x20b45c8,B,start+offset+5,half(memory,C+102));result=int(call(0x20b4108,C,B+start,word(memory,M+4))!=0)
        if result:
            last=word(memory,C+136);put(memory,M+12,last)
            if memory.read(B+start+offset+2,1)==b'\x02':put(memory,C+140,last)
    else:raise ValueError('Caller is outside modeled packet')
    external={at:bytes(raw) for at,raw in memory.regions.items() if at!=SP-0x1000}
    return external,calls,contract,result&0xffffffff


def cases(address):
    if address==0x20b4134:return [dict(state=state,initiated=init,timeout=timeout,start=start,now=(start+age)&0xffffffff,helper=ret) for state in [-1,0,3,4,5,7,8] for init in [0,1] for timeout in [0,100] for start in [0,0xfffffff0] for age in [0,100,101,60000,60001] for ret in [0,1]]
    if address==0x20b4194:return [dict(count=count,last=last,now=(last+age)&0xffffffff,helper=ret) for count in [0,1,3] for last in [0,0xfffffff0] for age in [999,1000,1001,0xffffffff] for ret in [0,1]]
    if address in [0x20b41d8,0x20b4204]:
        threshold=100 if address==0x20b41d8 else 30000
        return [dict(pending=pending,last=last,now=(last+age)&0xffffffff,helper=ret) for pending in [0,1,0xffffffff] for last in [0,0xfffffff0] for age in [0,threshold-1,threshold,threshold+1,0xffffffff] for ret in [0,1,0x80000000]]
    if address in [0x20b4270,0x20b42a4,0x20b45dc]:return [dict(state=state,hard=hard,swap=swap,initiated=init,helper=ret) for state in [-1,0,4,5,6,7,8] for hard in [0,1] for swap in [0,1] for init in [0,1] for ret in [0,1]]
    if address==0x20b4330:return [dict(size=size,incoming=incoming,callback=callback,helper=ret) for size in [0,1,512,-1] for incoming in [0,1024] for callback in [0,0x12345679] for ret in [0,1,0xffffffff]]
    if address in [0x20b514c,0x20b51dc]:return [dict(state=state,found=found,dump=dump,timeout=timeout,start=start,now=(start+age)&0xffffffff,send=send,helper=ret) for state in [0,5] for found in [0,1] for dump in [0,1] for timeout in [0,100] for start in [0,0xfffffff0] for age in [99,100,101] for send in [0,1] for ret in [0,1]]
    if address==0x20b5390:return [dict(length=length,free=free,store=store,memoryError=err,protocol=protocol,serial=serial,type=type) for length in [0,16] for free in [-1,16,512] for store in [0,1] for err in [0,1] for protocol in [0,2] for serial in [0,65535] for type in [0,255]]
    if address==0x20b5900:return [dict(messageStart=start,messageLength=length,messageType=type,offset=offset,expected=expected,helper=ret,newSend=new) for start in [0,8] for length in [0,8] for type in [0,2,7,255] for offset in [0,2] for expected in [0,65535] for ret in [0,1] for new in [0,0xffffffff]]
    raise ValueError('No bounded caller vectors')
