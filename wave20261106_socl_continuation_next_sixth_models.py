import hashlib
from wave20261105_socket_thumb_next_memory import Memory

CTX,OUT,INPUT,SALT,SP,STOP=0x02400000,0x02410000,0x02420000,0x02430000,0x027f0000,0x027d0000
SPECS={'02091518':16,'0209158c':24,'020917f8':40,'02091864':56}
NAMES=list(SPECS)


def fixtures(name):
    if name=='02091518':return [dict(count=n,width=w,values=v,method=m)for n,w,v,m in [(0,2,[1],1),(-1,2,[1],1),(1,2,[0x1234],0x1234),(2,2,[1,4],4),(2,2,[1,4],3),(2,3,[0x12345,0x2345],0x2345),(1,3,[0x10001],1),(3,0,[4],4)]]
    if name=='0209158c':return [dict(version=v,selected=s,methods=m,sessions=n,challenge=c)for v,s,m,n,c in [(0,4,6,1,32),(1,0,3,0,32),(1,4,6,0,0),(1,4,6,1,1),(1,4,7,3,31),(1,4,3,2,32),(1,4,6,1,40),(1,0xffff0005,3,0,16)]]
    if name=='020917f8':return [dict(salt=s,alias=a,pattern=p)for s,a,p in [('',False,0),('A',False,1),('BB',False,2),('CCC',True,3),('bounded-seed',False,4)]]
    return [dict(pattern=p)for p in range(4)]


def scenario(name,f,ordinal):
    memory=Memory({CTX:1216,OUT:64,INPUT:512,SALT:32},ordinal);actions=[];extras=[];result=None;checks=[]
    def call(address,args,returned=0xa7000000,mutations=None,extra=None):
        action=dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=[(base,raw)for base,raw in memory.snapshot().items()]+list(extra or []),mutations=list(mutations or []),stackWords=[]);actions.append(action)
        for base,raw in action['mutations']:
            if CTX<=base<CTX+1216 or OUT<=base<OUT+64 or INPUT<=base<INPUT+512 or SALT<=base<SALT+32:memory.put(base,raw)
    if name=='02091518':
        for i,value in enumerate(f['values']):memory.put(INPUT+i*f['width'],value.to_bytes(3 if f['width']==3 else 2,'big'))
        initial=memory.snapshot();result=0;at=INPUT
        for i in range(max(f['count'],0)):
            value=memory.get(at,1)*256+memory.get(at+1,1)
            if f['width']==3:value=value*256+memory.get(at+2,1)
            if value==f['method']:result=1;break
            at+=f['width']
        args=[INPUT,f['count']&0xffffffff,f['width'],f['method']]
    elif name=='0209158c':
        memory.put(INPUT,bytes([2,0])+f['methods'].to_bytes(2,'big')+f['sessions'].to_bytes(2,'big')+f['challenge'].to_bytes(2,'big'));memory.put(INPUT+8,bytes((i*17+ordinal*3)&255 for i in range(256)));initial=memory.snapshot();call(0x2091580,[2,0],f['version'])
        if f['version']:
            call(0x2026144,[f['methods'],3],f['methods']//3);call(0x209154c,[INPUT+8,f['methods']//3,3],f['selected']);method=f['selected']&65535
            if method:
                memory.set(CTX+50,method,2);memory.set(CTX+48,0,1);source=INPUT+8+f['methods']+f['sessions'];length=f['challenge']
                if length>=32:call(0x2008e0c,[source,CTX+52,32],mutations=[(CTX+52,memory.read(source,32))])
                else:
                    call(0x2008d78,[CTX+52,0,32-length],mutations=[(CTX+52,bytes(32-length))]);call(0x2008e0c,[source,CTX+84-length,length],mutations=[(CTX+84-length,memory.read(source,length))])
                memory.set(CTX+0x455,1,1)
        args=[CTX,INPUT,0x22334455,0x33445566]
    elif name=='020917f8':
        master=bytes((i*13+f['pattern']*19)&255 for i in range(48));randoms=bytes((i*37+f['pattern']*31)&255 for i in range(64));salt=f['salt'].encode();memory.put(CTX,master);memory.put(CTX+52,randoms);memory.put(SALT,salt+b'\0');initial=memory.snapshot();destination=CTX if f['alias']else OUT;sha=CTX+0x348;md5=CTX+0x3fc;temporary=SP-40
        call(0x20936bc,[sha],mutations=[(sha,bytes.fromhex('0123456789abcdeffedcba9876543210f0e1d2c3')+bytes(8))]);call(0x201d69c,[SALT],len(salt));message=b''
        for source,data in [(SALT,salt),(CTX,master),(CTX+52,randoms)]:
            message+=data;marker=hashlib.sha1(message).digest()+len(message).to_bytes(8,'little');call(0x20936f4,[sha,source,len(data)],mutations=[(sha,marker)])
        digest=hashlib.sha1(message).digest();call(0x2093774,[sha,temporary],mutations=[(temporary,digest)]);extras=[(temporary,digest)];call(0x2092ffc,[md5],mutations=[(md5,bytes.fromhex('0123456789abcdeffedcba9876543210')+bytes(8))],extra=extras)
        message=b''
        for source,data in [(CTX,master),(temporary,digest)]:
            message+=data;marker=hashlib.md5(message).digest()+len(message).to_bytes(8,'little');call(0x209302c,[md5,source,len(data)],mutations=[(md5,marker)],extra=extras)
        call(0x20930ac,[md5,destination],mutations=[(destination,hashlib.md5(message).digest())],extra=extras);args=[destination,SALT,CTX,0x33445566]
    else:
        master=bytes((i*23+f['pattern']*29)&255 for i in range(48));randoms=bytes((i*43+f['pattern']*47)&255 for i in range(64));memory.put(CTX,master);memory.put(CTX+52,randoms);initial=memory.snapshot();temporary=SP-56;combined=b''
        for i,(salt,address)in enumerate([(b'A',0x20de87c),(b'BB',0x20de880),(b'CCC',0x20de884)]):
            digest=hashlib.sha1(salt+master+randoms).digest();part=hashlib.md5(master+digest).digest();mutations=[(CTX+0x348,digest+len(salt+master+randoms).to_bytes(8,'little')),(CTX+0x3fc,hashlib.md5(master+digest).digest()+len(master+digest).to_bytes(8,'little')),(temporary+16*i,part)];call(0x20917f8,[temporary+16*i,address,CTX],mutations=mutations,extra=[(temporary,combined)]if combined else []);combined+=part
        extras=[(temporary,combined)];call(0x2008e0c,[temporary,CTX,48],mutations=[(CTX,combined)],extra=extras);args=[CTX,0x11773355,0x22334455,0x33445566]
    return dict(initial=initial,regions=memory.snapshot(),args=args,actions=actions,result=result,volatileStateReads=None,readable=[(CTX,1216),(OUT,64),(INPUT,512),(SALT,32)],extraChecks=extras)
