import hashlib
from wave20261106_socl_continuation_next_ninth_models import Plan

CTX,OUT,SECRET,ALTERNATE,MESSAGE,ROOT_CERT,SP,STOP=0x02400000,0x02410000,0x02420000,0x02421000,0x02430000,0x02440000,0x027f0000,0x027d0000
SPECS={'020911b0':16,'02091c5c':88}
NAMES=list(SPECS)


def fixtures(name):
    if name=='020911b0':return [dict(flag=f,pub_algorithm=l,algorithm=a,root=r,status=s,message=n,change=c)for f,l,a,r,s,n,c in [(0,0xffffffff,3,True,0,0,False),(128,0xffffffff,4,True,0,1,False),(0,8,2,True,0,3,False),(0,8,3,False,0,63,False),(0,8,4,True,0,64,False),(128,8,4,True,0x4002,129,False),(1,8,3,True,0x80000000,17,True),(0,0xfffffffe,4,True,0xffffffff,0,False)]]
    return [dict(method=method,length=length,bad=bad,outer_change=change,sequence=sequence)for method,length,bad,change,sequence in [(4,0,False,False,0),(4,3,True,False,0x123456789abcdef0),(4,64,False,True,0xffffffffffffffff),(4,257,True,False,0xfffffffffffffffe),(5,0,False,False,0),(5,3,True,False,0x0123456789abcdef),(5,64,False,True,0xffffffffffffffff),(5,257,True,False,0xfffffffffffffffe)]]


def certificate(f,ordinal):
    p=Plan({CTX:2176,MESSAGE:512,ROOT_CERT:32},ordinal);m=p.memory;m.set(CTX+1455,f['flag'],1);m.set(CTX+1116,f['pub_algorithm']);m.set(CTX+1112,f['algorithm']);m.set(CTX+1120,MESSAGE);m.set(CTX+1124,MESSAGE+f['message']);message=bytes((i*17+ordinal*11)&255 for i in range(f['message']));m.put(MESSAGE,message);m.put(CTX+1456,b'CN=measured-certificate\0');initial=m.snapshot();p.writable=[(CTX+1148,4)];flags=0 if f['flag']else 0x8000
    if f['pub_algorithm']==0xffffffff:p.result=flags|4;return p.finish(initial,[CTX,0x11223344,0x55667788,0x99aabbcc])
    if f['algorithm']not in [3,4]:p.result=flags|3;return p.finish(initial,[CTX,0x11223344,0x55667788,0x99aabbcc])
    md5=f['algorithm']==3;hasher=hashlib.md5 if md5 else hashlib.sha1;hash_address=CTX+(1020 if md5 else 840);initialize,update,final=(0x2092ffc,0x209302c,0x20930ac)if md5 else (0x20936bc,0x20936f4,0x2093774);p.call(initialize,[hash_address],mutations=[(hash_address,hasher(b'').digest()+bytes(8))]);p.call(update,[hash_address,MESSAGE,len(message)],mutations=[(hash_address,hasher(message).digest()+len(message).to_bytes(8,'little'))]);p.call(final,[hash_address,CTX+1128],mutations=[(CTX+1128,hasher(message).digest())]);m.set(CTX+1148,16 if md5 else 20);changes=[(CTX+1455,b'\x00')]if f['change']else []
    p.call(0x2090bdc,[CTX,CTX+1456],ROOT_CERT if f['root']else 0,changes)
    if not f['root']:p.result=flags|1
    else:p.call(0x209108c,[CTX,ROOT_CERT],f['status']);p.result=flags|f['status']
    return p.finish(initial,[CTX,0x11223344,0x55667788,0x99aabbcc])


def plaintext(f,ordinal):
    p=Plan({CTX:2176,OUT:2048,SECRET:64,ALTERNATE:64},ordinal);m=p.memory;md5=f['method']==4;hasher=hashlib.md5 if md5 else hashlib.sha1;digest_size=16 if md5 else 20;pad_size=48 if md5 else 40;payload=bytes((i*23+ordinal*19)&255 for i in range(f['length']));sequence=f['sequence'].to_bytes(8,'big');secret=bytes((i*13+ordinal*29)&255 for i in range(digest_size));alternate=bytes((i*31+ordinal*7)&255 for i in range(digest_size));m.put(SECRET,secret);m.put(ALTERNATE,alternate);m.set(CTX+468,SECRET);m.set(CTX+50,f['method'],2);m.set(CTX+1109,7,1);m.put(CTX+740,sequence);wire_length=f['length']+digest_size+7;header=bytes([23,3,0,wire_length>>8,wire_length&255]);m.put(OUT,header);normalized_header=bytes([23,3,0,f['length']>>8,f['length']&255]);inner=hasher(secret+bytes([0x36])*pad_size+sequence+normalized_header[:1]+normalized_header[3:]+payload).digest();outer=hasher((alternate if f['outer_change']else secret)+bytes([0x5c])*pad_size+inner).digest();supplied=bytearray(outer)
    if f['bad']:supplied[-1]^=0x80
    initial=m.snapshot();p.writable=[(OUT+3,2),(CTX+1109,1)];p.call(0x2091c48,[CTX,OUT+5,wire_length],len(payload)+digest_size,[(OUT+5,payload+bytes(supplied))]);m.put(OUT,normalized_header);hash_address=CTX+(1020 if md5 else 840);initialize,update,final=(0x2092ffc,0x209302c,0x20930ac)if md5 else (0x20936bc,0x20936f4,0x2093774);padding=SP-88;digest=SP-40;message=b'';pad=None;digest_value=None
    def checks():return ([(padding,pad)]if pad is not None else [])+([(digest,digest_value)]if digest_value is not None else [])
    def reset():
        nonlocal message
        p.call(initialize,[hash_address],mutations=[(hash_address,hasher(b'').digest()+bytes(8))],checks=checks());message=b''
    def append(source,raw):
        nonlocal message
        message+=raw;p.call(update,[hash_address,source,len(raw)],mutations=[(hash_address,hasher(message).digest()+len(message).to_bytes(8,'little'))],checks=checks())
    def fill(value):
        nonlocal pad
        p.call(0x2008d78,[padding,value,pad_size],checks=checks());pad=bytes([value])*pad_size;p.actions[-1]['mutations']=[(padding,pad)]
    def finish(change=False):
        nonlocal digest_value
        value=hasher(message).digest();p.call(final,[hash_address,digest],checks=checks());p.actions[-1]['mutations']=[(digest,value)];digest_value=value
        if change:p.actions[-1]['mutations'].append((CTX+468,ALTERNATE.to_bytes(4,'little')));m.set(CTX+468,ALTERNATE)
    reset();append(SECRET,secret);fill(0x36);append(padding,pad);append(CTX+740,sequence);append(OUT,normalized_header[:1]);append(OUT+3,normalized_header[3:]+payload);finish(f['outer_change']);reset();append(ALTERNATE if f['outer_change']else SECRET,alternate if f['outer_change']else secret);fill(0x5c);append(padding,pad);append(digest,digest_value);finish();p.call(0x201b248,[OUT+5+len(payload),digest,digest_size],0xffffffff if f['bad']else 0,checks=checks())
    if f['bad']:m.set(CTX+1109,9,1)
    incremented=((f['sequence']+1)&0xffffffffffffffff).to_bytes(8,'big');p.call(0x2091c30,[CTX+748],mutations=[(CTX+740,incremented)],checks=checks());p.extra=checks();p.result=len(payload)+5
    return p.finish(initial,[CTX,OUT,0x55667788,0x99aabbcc])


def scenario(name,f,ordinal):return (certificate if name=='020911b0'else plaintext)(f,ordinal)
