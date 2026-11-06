from wave20261105_gamespy_qr2_next_first_models import Memory,word,put

N,S=0x2170000,0x2171000
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700800,0x20e1738
ARITY={0x20b6670:5,0x20a8ef8:0}


def initial(address,v):
    if address not in [0x20b6eac,0x20b69e4]:raise ValueError('Caller outside seventeenth scope')
    memory=Memory({N:bytes(84),S:bytes(8),MAGIC:bytes.fromhex('fdfc1e666ab2'),SP-0x1000:bytes(0x1000)})
    for offset,value in [(0,v['socket']),(8,v['cookie']),(12,v.get('clientIndex',0))]:put(memory,N+offset,value)
    memory.write(S,bytes([0x7f,2])+v['port'].to_bytes(2,'little')+v['ip'].to_bytes(4,'little'))
    if address==0x20b6eac:return memory,[N,S]
    for offset,value in [(4,v['gameSocket']),(16,v['state']),(40,37),(44,0x11223344),(48,v['ip'])]:put(memory,N+offset,value)
    memory.write(N+52,v['port'].to_bytes(2,'little')+bytes([v['got'],7]));return memory,[N]


def effect(target,args,memory,v):
    if target==0x20a8ef8:
        if 'gotAfterTime'in v:memory.write(N+54,bytes([v['gotAfterTime']]))
        return v['now'],[]
    if target!=0x20b6670:raise ValueError('Unqualified protocol sender import')
    raw=memory.read(args[3],args[4]);defined=raw if v.get('family')=='ping'else raw[:12]+raw[13:14]
    if 'gotAfterSend'in v:memory.write(N+54,bytes([v['gotAfterSend']]))
    return 0x12345678,[args[0],args[1],args[2],defined.hex(),args[4]]


def model(address,v):
    memory,args=initial(address,v)
    if address==0x20b6eac:
        memory.write(TMP,bytes.fromhex('fdfc1e666ab20306'));memory.write(TMP+8,word(memory,N+8).to_bytes(4,'big'));memory.write(TMP+13,bytes([word(memory,N+12)&255]))
        ignored,normalized=effect(0x20b6670,[word(memory,N),word(memory,S+4),int.from_bytes(memory.read(S+2,2),'big'),TMP,21],memory,v);calls=[(hex(0x20b6670),normalized)]
    else:
        memory.write(TMP,bytes.fromhex('fdfc1e666ab20307')+word(memory,N+8).to_bytes(4,'big')+word(memory,N+48).to_bytes(4,'little')+int.from_bytes(memory.read(N+52,2),'little').to_bytes(2,'big')+bytes([memory.read(N+54,1)[0],int(word(memory,N+16)!=2)]))
        game=word(memory,N+4);sock=word(memory,N)if game==0xffffffff else game
        ignored,normalized=effect(0x20b6670,[sock,word(memory,N+48),int.from_bytes(memory.read(N+52,2),'little'),TMP,20],memory,v);calls=[(hex(0x20b6670),normalized)]
        now,normalized=effect(0x20a8ef8,[],memory,v);calls.append((hex(0x20a8ef8),normalized));put(memory,N+44,now+700);put(memory,N+40,12)
        if memory.read(N+54,1)[0]:memory.write(N+55,bytes([1]))
    return{at:bytes(raw)for at,raw in memory.regions.items()if at!=SP-0x1000},calls,'void',0


def cases(address):
    if address==0x20b6eac:return[dict(clientIndex=index,cookie=cookie,socket=socket,port=port,ip=ip)for index in [-1,0,255,256]for cookie in [0,0x12345678,0xffffffff]for socket in [-1,0,7]for port in [0,1,0x80ff,65535]for ip in [0,0x01020304,0xffffffff]]
    if address!=0x20b69e4:raise ValueError('No peer protocol vectors')
    rows=[dict(family='ping',state=state,cookie=cookie,socket=8,gameSocket=sock,port=port,ip=0x01020304,got=got,now=now)for state in [-1,0,2,3,4]for cookie in [0x12345678,0xffffffff]for sock in [-1,0,27]for port in [0,1,0x80ff,65535]for got in [0,1,255]for now in [0,0xfffffff0]]
    for got in [0,1]:
        for later in [0,1,255]:
            for stage in ['gotAfterSend','gotAfterTime']:
                rows.append(dict(rows[0],got=got,**{stage:later}))
    return rows
