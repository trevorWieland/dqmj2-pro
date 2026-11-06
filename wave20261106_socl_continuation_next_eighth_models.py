import hashlib
from wave20261105_socket_thumb_next_memory import Memory

CTX,OUT,SP,STOP=0x02400000,0x02410000,0x027f0000,0x027d0000
SPECS={'02091a68':64,'02091afc':56}
NAMES=list(SPECS)


def fixtures(name):
    return [dict(server=s,direction=d,alias=a,length=n,pattern=i)for i,(s,d,a,n)in enumerate([(0,0,False,0),(0,1,False,3),(1,0,False,55),(1,1,False,64),(128,256,False,7),(1,0xffffffff,True,9)])]


def scenario(name,f,ordinal):
    memory=Memory({CTX:2176,OUT:64},ordinal);actions=[];md5=name=='02091a68';size=48 if md5 else 40;digest_size=16 if md5 else 20;hash_address=CTX+(932 if md5 else 748);update=0x209302c if md5 else 0x20936f4;final=0x20930ac if md5 else 0x2093774;initialize=0x2092ffc if md5 else 0x20936bc;hasher=hashlib.md5 if md5 else hashlib.sha1;pad_address=SP-SPECS[name];pad=None;output=CTX if f['alias']else OUT;message=bytes((i*19+f['pattern']*7)&255 for i in range(f['length']));master=bytes((i*23+f['pattern']*11)&255 for i in range(48));memory.put(CTX,master);memory.set(CTX+1108,f['server'],1);memory.put(hash_address,hasher(message).digest()+len(message).to_bytes(8,'little'));initial=memory.snapshot()
    def call(address,args,mutations):
        action=dict(address=address,args=[x&0xffffffff for x in args],returned=0xa7000000+len(actions),checks=[(base,raw)for base,raw in memory.snapshot().items()]+([(pad_address,pad)]if pad is not None else []),mutations=mutations,stackWords=[]);actions.append(action)
        for base,raw in mutations:
            if CTX<=base<CTX+2176 or OUT<=base<OUT+64:memory.put(base,raw)
    def append(source,raw):
        nonlocal message
        message+=raw;marker=hasher(message).digest()+len(message).to_bytes(8,'little');call(update,[hash_address,source,len(raw)],[(hash_address,marker)])
    def finish():call(final,[hash_address,output],[(output,hasher(message).digest())])
    role=b'SRVR' if (f['server']^f['direction']) else b'CLNT';role_address=0x20de888 if role==b'SRVR'else 0x20de890;append(role_address,role);append(CTX,memory.read(CTX,48));call(0x2008d78,[pad_address,0x36,size],[(pad_address,bytes([0x36])*size)]);pad=bytes([0x36])*size;append(pad_address,pad);finish();call(initialize,[hash_address],[(hash_address,hasher(b'').digest()+bytes(8))]);message=b'';append(CTX,memory.read(CTX,48));call(0x2008d78,[pad_address,0x5c,size],[(pad_address,bytes([0x5c])*size)]);pad=bytes([0x5c])*size;append(pad_address,pad);append(output,memory.read(output,digest_size));finish()
    return dict(initial=initial,regions=memory.snapshot(),args=[CTX,output,f['direction'],0x33445566],actions=actions,result=None,volatileStateReads=None,readable=[(CTX,2176),(OUT,64)],extraChecks=[(pad_address,pad)])
