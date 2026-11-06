from wave20261105_gamespy_qr2_next_first_models import Memory,word,put

N,G,GD,GAME=0x2170000,0x21d2bc4,0x20e172c,0x21d23f0
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700800,0x20e1738
ARITY={0x201d69c:1,0x201b19c:3,0x20b6670:5}


def cstring(memory,address):
    out=bytearray()
    for index in range(64):
        ch=memory.read(address+index,1)
        if ch==b'\0':return bytes(out)
        out.extend(ch)
    raise ValueError('Bounded game name must fit64-byte source view')


def initial(address,v):
    if address!=0x20b6708:raise ValueError('Caller outside thirteenth scope')
    memory=Memory({N:bytes(84),G:bytes(44),GD:bytes(4),GAME:bytes(64),MAGIC:bytes.fromhex('fdfc1e666ab2'),SP-0x1000:bytes(0x1000)})
    for offset,value in [(0,7),(8,v.get('cookie',0x12345678)),(12,v.get('clientIndex',1)),(68,v['result'])]:put(memory,N+offset,value)
    put(memory,G+8,v['scheme']);put(memory,G+40,0x01020304);put(memory,GD,v['natType']);memory.write(GAME,v['game'].encode()+b'\0')
    return memory,[N]


def effect(target,args,memory,v):
    if target==0x201d69c:
        raw=cstring(memory,args[0]);return len(raw),[raw.hex()]
    if target==0x201b19c:
        raw=memory.read(args[1],args[2]);memory.write(args[0],raw);return args[0],[raw.hex(),args[2]]
    if target==0x20b6670:
        raw=memory.read(args[3],args[4]);initialized=raw[:12]+raw[13:23]+(raw[23:73]if v['game']else b'')
        return 0x12345678,[args[0],args[1],args[2],initialized.hex(),args[4]]
    raise ValueError('Unexpected report helper contract')


def model(address,v):
    memory,args=initial(address,v);calls=[]
    def call(target,*arguments):
        value,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return value
    memory.write(TMP,bytes.fromhex('fdfc1e666ab2030d'));memory.write(TMP+8,word(memory,N+8).to_bytes(4,'big'));memory.write(TMP+13,bytes([word(memory,N+12)&255,int(word(memory,N+68)==0)]));memory.write(TMP+15,memory.read(GD,4));memory.write(TMP+19,memory.read(G+8,4))
    if call(0x201d69c,GAME)>0:call(0x201b19c,TMP+23,GAME,50)
    call(0x20b6670,word(memory,N),word(memory,G+40),27901,TMP,73)
    return {at:bytes(raw)for at,raw in memory.regions.items()if at!=SP-0x1000},calls,'void',0


def cases(address):
    if address!=0x20b6708:raise ValueError('No thirteenth caller vectors')
    vectors=[dict(result=result,natType=kind,scheme=scheme,game=game)for result in [0,1,2,3,0xffffffff]for kind in [0,6,0xffffffff]for scheme in [0,0x11223344]for game in ['', 'dqm','g'*49,'g'*50,'g'*63]]
    vectors +=[dict(result=0,natType=6,scheme=4,game='dqm',cookie=cookie,clientIndex=index)for cookie in [0,0xffffffff,0x80ff01fe]for index in [-1,0,255,256]]
    return vectors
