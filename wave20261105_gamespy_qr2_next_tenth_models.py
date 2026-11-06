from wave20261105_gamespy_qr2_next_first_models import Memory,word,put

P,A,R,G=0x2170000,0x2171000,0x2172000,0x21d2bc4
SP,STOP,TMP,MAGIC=0x2701000,0x27e0000,0x2700800,0
ARITY={0x20a8c68:3,0x20a85dc:3,0x20a865c:2,0x20a8640:1,0x20a8644:2}


def initial(address,v):
    memory=Memory({P:bytes.fromhex('efbeadde3412000078563412cdab0000'),A:bytes(64),R:bytes(1024),G:bytes(4),SP-0x1000:bytes(0x1000)})
    put(memory,G,A if v.get('existing')else 0)
    args={0x20b6100:[v.get('socket',7)],0x20b66e0:[v.get('socket',7)],0x20b6128:[P if v.get('nonnull',True)else 0],0x20b65a4:[]}
    return memory,args[address]


def effect(target,args,memory,v):
    if target==0x20a8c68:
        if word(memory,args[2])!=8:raise ValueError('Socket query must pass original8-byte view')
        if not(SP-0x1000<=args[1]and args[1]+8<=SP and SP-0x1000<=args[2]and args[2]+4<=SP):raise ValueError('Socket query pointers leave bounded stack')
        memory.write(args[1],bytes([8,2])+v['port'].to_bytes(2,'little')+bytes.fromhex('04030201'));put(memory,args[2],8)
        return v['helper']&0xffffffff,[args[0],8]
    if target==0x20a85dc:return A,args
    if target==0x20a865c:return 0x11223344,[args[0],memory.read(args[1],84).hex()]
    if target==0x20a8640:return v['count'],args
    if target==0x20a8644:return R+84*args[1],args
    raise ValueError('Unqualified NAT view contract')


def model(address,v):
    memory,args=initial(address,v);calls=[];result=0;contract='word'
    def call(target,*arguments):
        value,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return value
    if address in [0x20b6100,0x20b66e0]:
        put(memory,TMP+16,8);ret=call(0x20a8c68,args[0]&0xffffffff,TMP,TMP+16);result=0 if ret==0xffffffff else v['port']
    elif address==0x20b6128:contract='void'
    elif address==0x20b65a4:
        array=word(memory,G)
        if array==0:array=call(0x20a85dc,84,4,0);put(memory,G,array)
        memory.write(TMP,bytes(84));call(0x20a865c,array,TMP);length=call(0x20a8640,array);result=call(0x20a8644,array,length-1)
    else:raise ValueError('NAT caller outside tenth scope')
    return {at:bytes(raw)for at,raw in memory.regions.items()if at!=SP-0x1000},calls,contract,result


def cases(address):
    if address in [0x20b6100,0x20b66e0]:return[dict(socket=s,helper=h,port=p)for s in [-1,0,7]for h in [-2,-1,0,1,0x80000000]for p in [0,1,0x80ff,65535]]
    if address==0x20b6128:return[dict(nonnull=b)for b in [False,True]]
    if address==0x20b65a4:return[dict(existing=b,count=n)for b in [False,True]for n in [1,2,7]]
    raise ValueError('No tenth caller vectors')
