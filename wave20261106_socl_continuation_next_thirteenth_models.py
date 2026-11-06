import hashlib
from wave20261106_socl_continuation_next_ninth_models import Plan
from wave20261106_socl_continuation_next_thirteenth_callbacks import TARGETS,CONTRACTS

CTX,OTHER,OUT,SECRET,ALTERNATE,SOCKET,SP,STOP=0x02400000,0x02402000,0x02410000,0x02420000,0x02421000,0x02430000,0x027f0000,0x027d0000
SPECS={'02091de0':72,'02092380':24}
NAMES=list(SPECS)


def fixtures(name):
    if name=='02092380':return [dict(mode=mode,failure=f,changed_context=c,length=n)for mode in ['thumb','arm']for f,c,n in [(True,False,0),(False,False,61),(False,True,65),(False,False,69)]]
    return [dict(method=method,length=n,outer_change=change,sequence=sequence)for method,n,change,sequence in [(4,0,False,0),(4,1,False,0x0123456789abcdef),(4,64,True,0xffffffffffffffff),(4,257,False,0xfffffffffffffffe),(5,0,False,0),(5,1,False,0x123456789abcdef0),(5,64,True,0xffffffffffffffff),(5,257,False,0xfffffffffffffffe),(0,3,False,0),(3,0,False,1),(65535,257,False,0xffffffffffffffff)]]


def finish(p,initial,args,providers=None):
    value=p.finish(initial,args);value['indirectProviders']=providers or {};return value


def ciphertext(f,ordinal):
    p=Plan({CTX:2176,OUT:2048,SECRET:64,ALTERNATE:64},ordinal);m=p.memory;md5=f['method']==4;size=16 if md5 else 20;pad_size=48 if md5 else 40;hasher=hashlib.md5 if md5 else hashlib.sha1;payload=bytes((i*17+ordinal*11)&255 for i in range(f['length']));header=bytes([23,3,0,f['length']>>8,f['length']&255]);sequence=f['sequence'].to_bytes(8,'big');secret=bytes((i*29+ordinal*13)&255 for i in range(size));alternate=bytes((i*7+ordinal*19)&255 for i in range(size));m.put(OUT,header+payload);m.set(CTX+50,f['method'],2);m.set(CTX+188,SECRET);m.put(SECRET,secret);m.put(ALTERNATE,alternate);m.put(CTX+460,sequence);initial=m.snapshot();p.writable=[(OUT+3,2)];pad_address=SP-68;pad=None;output_mac=OUT+5+len(payload);message=b'';hash_address=CTX+(1020 if md5 else 840);initialize,update,final=(0x2092ffc,0x209302c,0x20930ac)if md5 else(0x20936bc,0x20936f4,0x2093774)
    def checks():return [(pad_address,pad)]if pad is not None else []
    def reset():
        nonlocal message
        p.call(initialize,[hash_address],mutations=[(hash_address,hasher(b'').digest()+bytes(8))],checks=checks());message=b''
    def append(address,raw):
        nonlocal message
        message+=raw;p.call(update,[hash_address,address,len(raw)],mutations=[(hash_address,hasher(message).digest()+len(message).to_bytes(8,'little'))],checks=checks())
    def fill(value):
        nonlocal pad
        p.call(0x2008d78,[pad_address,value,pad_size],checks=checks());pad=bytes([value])*pad_size;p.actions[-1]['mutations']=[(pad_address,pad)]
    def digest(change=False):
        mutations=[(output_mac,hasher(message).digest())]
        if change:mutations.append((CTX+188,ALTERNATE.to_bytes(4,'little')))
        p.call(final,[hash_address,output_mac],mutations=mutations,checks=checks())
    total=len(payload)
    if f['method']in[4,5]:
        reset();append(SECRET,secret);fill(0x36);append(pad_address,pad);append(CTX+460,sequence);append(OUT,header[:1]);append(OUT+3,header[3:]+payload);digest(f['outer_change']);reset();append(ALTERNATE if f['outer_change']else SECRET,alternate if f['outer_change']else secret);fill(0x5c);append(pad_address,pad);append(output_mac,m.read(output_mac,size));digest();total+=size
    m.set(OUT+3,total>>8,1);m.set(OUT+4,total,1);encrypted=bytes(value^((i*31+ordinal*7)&255)for i,value in enumerate(m.read(OUT+5,total)));p.call(0x2093824,[CTX+200,OUT+5,total],mutations=[(OUT+5,encrypted),(CTX+200,bytes([ordinal^0xa5,ordinal^0x5a]))],checks=checks());p.call(0x2091c30,[CTX+468],mutations=[(CTX+460,((f['sequence']+1)&0xffffffffffffffff).to_bytes(8,'big'))],checks=checks());p.extra=checks();p.result=total+5
    return finish(p,initial,[CTX,OUT,0x55667788,0x99aabbcc])


def sender(f,ordinal):
    p=Plan({CTX:2176,OTHER:2176,OUT:256,SOCKET:32,0x21cfd0c:4,0x21cfd38:4},ordinal);m=p.memory;m.set(SOCKET+12,CTX);m.set(CTX+1109,3,1)
    for slot,kind in [(0x21cfd0c,'allocate'),(0x21cfd38,'release')]:m.set(slot,TARGETS[(kind,f['mode'])]|(int(f['mode']=='thumb')^int(bool(f.get('badTag')))))
    initial=m.snapshot();p.writable=[(OUT,15),(CTX+1109,1)];providers={TARGETS[(kind,f['mode'])]:dict(mode=f['mode'],kind='function',program='',processor='arm9',module='main',fixtureProvider=True)for kind in ['allocate','release']}
    def callback(kind,args,returned=None,mutations=()):
        p.call(TARGETS[(kind,f['mode'])],args,returned,mutations);p.actions[-1]['site']=CONTRACTS['02092380-'+kind]['call']
    changes=[(SOCKET+12,OTHER.to_bytes(4,'little'))]if f['changed_context']else [];callback('allocate',[131],0 if f['failure']else OUT,changes)
    if f['failure']:m.set(CTX+1109,9,1);return finish(p,initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc],providers)
    m.put(OUT,bytes([20,3,0,0,1,1]));p.call(0x2008d78,[CTX+460,0,8],mutations=[(CTX+460,bytes(8))]);m.put(OUT+6,bytes([22,3,0,0,40,20,0,0,36]))
    def copy(source,destination,size):p.call(0x2008e0c,[source,destination,size],mutations=[(destination,m.read(source,size))])
    copy(CTX+932,CTX+1020,88);md5_result=bytes((i*19+ordinal*17)&255 for i in range(16));p.call(0x2091a68,[CTX,OUT+15,0],mutations=[(OUT+15,md5_result),(CTX+932,bytes([0x61+ordinal])*88)]);copy(CTX+1020,CTX+932,88);copy(CTX+748,CTX+840,92);sha_result=bytes((i*23+ordinal*11)&255 for i in range(20));p.call(0x2091afc,[CTX,OUT+31,0],mutations=[(OUT+31,sha_result),(CTX+748,bytes([0x71+ordinal])*92)]);copy(CTX+840,CTX+748,92);p.call(0x2091f98,[CTX,OUT+11,40],mutations=[(CTX+932,bytes([0x81+ordinal])*88),(CTX+748,bytes([0x91+ordinal])*92)]);record=bytes((i*13+ordinal*31)&255 for i in range(f['length']));p.call(0x2091de0,[CTX,OUT+6],f['length'],[(OUT+6,record)]);p.call(0x208db64,[OUT,f['length']+6,0,0],0,stack=[SOCKET]);callback('release',[OUT],mutations=[(OUT,b'\x5a')])
    return finish(p,initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc],providers)


def scenario(name,f,ordinal):return (ciphertext if name=='02091de0'else sender)(f,ordinal)
