import itertools
import struct
SINGLETON,ADDRESS=0x020e33e4,0x021cfcf8
THREADS=[0x02400100,0x02400300]
SOCKETS=[0x02401000,0x02401200]
SP,STOP=0x027f0000,0x027e0000
SPECS={'0208d0e0':24,'0208d154':8,'0208d764':0,'0208d780':8,'0208d7c0':0,'0208d7e0':0,'0208d88c':8,'0208d8b4':8,'0208d8e8':8}


def fixtures(name):
    if name=='0208d0e0':return [dict(state=s,kind=k,present=p,mutate=m) for s,k,p,m in itertools.product([0,1,2,3,4,5,6,7,8,9,10,255],[0,1,2,3,0xffffffff],[False,True],[False,True])]
    if name=='0208d154':return [dict(kind=k,present=p,mutate=m) for k,p,m in itertools.product([0,1,2,3,0xffffffff],[False,True],[False,True])]
    if name=='0208d780':return [dict(local=l,remote=r,address=a,present=p,mutate=m) for l,r,a,p,m in itertools.product([0,1,65535,65536],[0,1,65535,65537,0xffffffff],[0,0x7f000001,0xffffffff],[False,True],[False,True])]
    if name=='0208d88c':return [dict(mode=s,present=p,returned=r,mutate=m) for s,p,r,m in itertools.product([0,1,255],[False,True],[0,1,0xffffffff,0x80000000,0x12345678],[False,True])]
    if name=='0208d8b4':return [dict(state=s,present=True,mutate=m,pattern=p) for s,m,p in itertools.product([0,1,2,3,4,5,6,7,8,9,10,255],[False,True],range(3))]
    if name=='0208d8e8':return [dict(mode=s,present=p,mutate=m) for s,p,m in itertools.product([0,1,255],[False,True],[False,True])]
    return [dict(present=p,pattern=n) for p,n in itertools.product([False,True],range(4))]


def scenario(name,f,ordinal):
    sizes={SINGLETON:8,ADDRESS:84,THREADS[0]:168,THREADS[1]:168,SOCKETS[0]:100,SOCKETS[1]:100}
    regions={a-16:bytearray((i*31+ordinal*7+a)&255 for i in range(n+32)) for a,n in sizes.items()}

    def put(at,raw):
        for base,data in regions.items():
            if base<=at and at+len(raw)<=base+len(data):data[at-base:at-base+len(raw)]=raw;return
        raise ValueError('Independent socket model write escaped borrowed prefixes')

    def read(at,n):
        for base,data in regions.items():
            if base<=at and at+n<=base+len(data):return bytes(data[at-base:at-base+len(data)])[:n]
        raise ValueError('Independent socket model read escaped borrowed prefixes')

    def setv(at,value,n=4):put(at,int(value&((1<<(8*n))-1)).to_bytes(n,'little'))
    def getv(at,n=4):return int.from_bytes(read(at,n),'little')
    words=[0,1,0x80000000,0xffffffff]
    arguments=[words[ordinal%4],words[(ordinal+1)%4],words[(ordinal+2)%4],0x89abcdef]
    setv(SINGLETON+4,THREADS[0])
    for index,a in enumerate(THREADS):setv(a+164,SOCKETS[index] if index or f['present'] else 0)
    for index,a in enumerate(SOCKETS):
        setv(a,THREADS[index]);setv(a+4,f.get('kind',2));setv(a+8,f.get('state',0),1);setv(a+9,f.get('mode',0),1)
        setv(a+36,[0,1,0xffffffff,0x80000000][ordinal%4])
    setv(ADDRESS+80,0xa1b2c3d4^ordinal)
    if name=='0208d780':arguments[:3]=[f['local'],f['remote'],f['address']]
    if name=='0208d8b4':arguments[0]=SOCKETS[0]
    initial={a:bytes(raw) for a,raw in regions.items()}
    actions=[]

    def call(address,args,returned):
        checks=[(a,bytes(raw)) for a,raw in regions.items()]
        changes=[]
        if f.get('mutate'):
            a=SOCKETS[0];n=len(actions)
            changes=[(a+8,bytes([(getv(a+8,1)+1)&255])),(a+9,bytes([getv(a+9,1)^1])),(a+4,((getv(a+4)+1)&3).to_bytes(4,'little')),
                     (a,THREADS[1].to_bytes(4,'little')),(a+36,((getv(a+36)^0xa5a5a5a5)+n&0xffffffff).to_bytes(4,'little')),
                     (SINGLETON+4,THREADS[1].to_bytes(4,'little'))]
            for at,raw in changes:put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned&0xffffffff,checks=checks,mutations=changes))
        return returned&0xffffffff

    socket=SOCKETS[0] if f['present'] else 0
    result=None
    if name in ['0208d0e0','0208d154']:
        call(0x0208cb1c,arguments[:2],socket)
    if name=='0208d0e0' and socket:
        state=getv(socket+8,1)
        if state in [4,7,8]:
            setv(socket+36,getv(socket+36)+1)
            call(0x0208cc18 if state==4 else 0x0208cc0c,[socket,0],0x24681357)
            setv(socket+8,{4:6,7:9,8:0}[state],1)
            if state==8 and getv(socket+4)==2:
                setv(socket+4,0);call(0x0200698c,[getv(socket)],0x76543210)
        else:call(0x0208cc24,[*arguments[:3],0],0x35792468)
    elif name=='0208d154' and socket:
        call(0x020069f8,[],0x97531246)
        setv(socket+8,0,1)
        if getv(socket+4) in [1,2]:setv(socket+4,0);call(0x0200698c,[getv(socket)],0x76543210)
    elif name=='0208d764' and socket:setv(socket+8,10,1);setv(socket+68,0)
    elif name=='0208d780' and socket:
        address=getv(ADDRESS+80) if f['address']==0x7f000001 else f['address']
        setv(socket+26,f['remote'],2);setv(socket+24,getv(socket+26,2),2);setv(socket+32,address);setv(socket+28,address)
        port=f['local']
        if port==0:port=call(0x0208d6b4,[],[0,1,65535,0x12348001][ordinal%4])
        setv(socket+10,port,2)
    elif name=='0208d7c0' and socket:
        setv(socket,THREADS[0]);setv(socket+8,0,1)
        for offset in [68,96,56]:setv(socket+offset,0)
    elif name=='0208d7e0' and socket:setv(socket,0)
    elif name=='0208d88c':
        result=call(0x0209280c if getv(socket+9,1) else 0x0208d820,[socket],f['returned']) if socket else 1
    elif name=='0208d8b4':
        socket=SOCKETS[0]
        call(0x020069f8,[],0x97531246)
        state=getv(socket+8,1)
        if state in [3,4]:call(0x0208cc18,[socket,25],0x24681357);setv(socket+8,7,1)
        elif state!=0:call(0x0208cc0c,[socket,26],0x24681357)
    elif name=='0208d8e8' and socket:
        if getv(socket+9,1):call(0x02092b50,[socket],0x98765432)
        call(0x0208d8b4,[socket],0x87654321)
    return dict(initial=initial,regions={a:bytes(raw) for a,raw in regions.items()},actions=actions,result=result,args=arguments)
