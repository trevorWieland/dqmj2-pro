import struct
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put,signed

Q,B,I,S,O=0x2170000,0x2172000,0x2174000,0x2176000,0x2178000
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700800,0x20e1714
SPLIT,SEND,SINGLE=0x20b7b00,0x20a8c34,0x20b7ac8
ARITY={SPLIT:3,SEND:6,SINGLE:8}
PROGRESS_FIELDS=[0,4,8,12,16,276]


def initial(address,v):
    if address!=0x20b7cfc:raise ValueError('Caller outside fourth scope')
    raw=bytes.fromhex(v.get('data',''));regions={Q:bytes(176),B:bytes([0xa7])*1404,I:raw+bytes(1024-len(raw)),S:bytes.fromhex('080212347f000001'),O:bytes(16),SP-0x1000:bytes(0x1000)}
    memory=Memory(regions);put(memory,Q,v.get('socket',0x89abcdef));put(memory,B+1400,v.get('initialLength',5))
    return memory,[Q,B,I,v.get('length',len(raw)),S]


def effect(target,args,memory,v):
    a=[value&0xffffffff for value in args];result=0;normalized=a[:]
    if target==SPLIT:
        step=word(memory,O);progress=[word(memory,a[2]+offset) for offset in PROGRESS_FIELDS]
        normalized=[a[0],a[1],progress,word(memory,B+1400)]
        results=v.get('results',[1,0]);numbers=v.get('packetNumbers',[]);result=results[step] if step<len(results) else 0;number=numbers[step] if step<len(numbers) else step+1
        for offset,value in zip(PROGRESS_FIELDS,[2,number,step+1,step+3,step+2,step%254]):put(memory,a[2]+offset,value)
        raw=b'opaque'+bytes([step&255]);memory.write(B,raw);put(memory,B+1400,len(raw));put(memory,O,step+1)
    elif target==SEND:
        raw=memory.read(a[1],a[2]);peer=memory.read(a[4],a[5]);normalized=[a[0],raw.hex(),a[2],a[3],a[4],peer.hex(),a[5]];put(memory,O+4,word(memory,O+4)+1);result=v.get('sendResult',0)
    elif target==SINGLE:
        normalized=a[:2]
        for count,pointer in [(a[2],a[3]),(a[4],a[5]),(a[6],a[7])]:normalized.extend([count,None if pointer==0 else memory.read(pointer,count).hex()])
        old=word(memory,B+1400);raw=bytes([a[2]&255,a[4]&255,a[6]&255]);memory.write(B+old,raw);put(memory,B+1400,old+len(raw));result=0x12345678
    else:raise ValueError('Unqualified fourth-packet supplied contract')
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[];left=signed(args[3]&0xffffffff);cursor=0;counts=[];pointers=[];valid=left>=3
    def call(target,*arguments):
        returned,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return returned
    if valid:
        for index in range(3):
            if left<3-index:valid=False;break
            count=memory.read(I+cursor,1)[0];cursor+=1;left-=1;pointer=0
            if count not in [0,255]:pointer=I+cursor;cursor+=count;left-=count
            counts.append(count);pointers.append(pointer)
        valid=valid and left>=0
    if valid:
        flags=memory.read(I+cursor,1)[0] if left>0 else 0
        if flags&1:
            for offset in PROGRESS_FIELDS:put(memory,TMP+offset,0)
            while call(SPLIT,Q,B,TMP)==1:
                call(SEND,word(memory,Q),B,word(memory,B+1400),0,S,8);put(memory,B+1400,5)
                if signed(word(memory,TMP+4))>7:break
        else:
            arguments=[Q,B]
            for count,pointer in zip(counts,pointers):arguments.extend([count,pointer])
            call(SINGLE,*arguments);call(SEND,word(memory,Q),B,word(memory,B+1400),0,S,8)
    external={at:bytes(raw) for at,raw in memory.regions.items() if at!=SP-0x1000}
    return external,calls,'void',0


def packet(counts,flags=None):
    raw=bytearray()
    for count in counts:
        raw.append(count)
        if count not in [0,255]:raw.extend((index*37+count)&255 for index in range(count))
    if flags is not None:raw.append(flags)
    return bytes(raw)


def cases(address):
    if address!=0x20b7cfc:raise ValueError('Fourth caller lacks vectors')
    result=[dict(data=packet([server,player,team],flags).hex(),initialLength=5,results=[1,0]) for server in [0,1,254,255] for player in [0,2,255] for team in [0,3,255] for flags in [None,0,1,2,255]]
    for results in [[0],[2],[0xffffffff],[1,0],[1,2],[1,1,0],[1]*12+[0]]:
        for numbers in [[],[7,8],[8],[-1,7,8]]:
            for initial in [0,5]:
                for status in [0,-1]:result.append(dict(data=packet([0,0,0],1).hex(),results=results,packetNumbers=numbers,initialLength=initial,sendResult=status))
    raws=[b'',b'\0',b'\0\0',b'\0\0\0',b'\xfe\0\0',b'\0\xfe\0',b'\0\0\xfe',b'\xff\xff\xff',packet([1,1,1]),packet([254,0,0]),packet([0,254,0]),packet([0,0,254])]
    for raw in raws:
        for length in sorted(set([-2147483648,-1,0,1,2,3,4,len(raw)-1,len(raw),0x7fffffff])):result.append(dict(data=raw.hex(),length=length,results=[0]))
    return result
