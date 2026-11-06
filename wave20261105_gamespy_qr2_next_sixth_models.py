import struct
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put,signed

Q,B,P,NAMES=0x2170000,0x2172000,0x2174000,0x2176000
SP,STOP,MAGIC,TABLE=0x2701000,0x27e0000,0x20e25b8,0x20e277c
CB={0x27e0100:('keys',3,148),0x27e0140:('count',2,152),0x27e0180:('server',3,136),0x27e01c0:('player',4,140),0x27e0200:('team',4,144)}
ARITY={0x20b7588:2,**{address:value[1] for address,value in CB.items()}}


def dynamic_callbacks(v):
    return {address:dict(mode=('thumb' if v.get('mode','mixed')=='thumb' or v.get('mode','mixed')=='mixed' and index%2 else 'arm'),kind='function',fixtureOnly=True,runtimeTargetNamespaceUnresolved=True) for index,address in enumerate(CB)}


def cstring(memory,address):
    out=bytearray()
    for index in range(2048):
        value=memory.read(address+index,1)
        if value==b'\0':return bytes(out)
        out.extend(value)
    raise ValueError('Bounded split-query key/value string lacks termination')


def append(memory,buffer,raw):
    length=signed(word(memory,buffer+1400));count=min(len(raw)+1,1400-length)
    if count<=0:return 0
    memory.write(buffer+length,(raw+b'\0')[:count]);put(memory,buffer+1400,length+count);memory.write(buffer+length+count-1,b'\0');return 1


def initial(address,v):
    if address!=0x20b7b00:raise ValueError('Caller outside sixth source scope')
    regions={Q:bytes([0xa5])*272,B:bytes([0xce])*1404,P:bytes(280),NAMES:bytes(4096),MAGIC:b'splitnum\0',TABLE:bytes(1020),SP-0x1000:bytes(0x1000)}
    memory=Memory(regions);put(memory,B+1400,v.get('length',0));put(memory,Q+268,0x89abcdef)
    for callback,binding in dynamic_callbacks(v).items():put(memory,Q+CB[callback][2],callback|(1 if binding['mode']=='thumb' else 0))
    keys=v.get('initialKeys',[1]);fields=[v.get('type',0),v.get('packet',0),v.get('keyIndex',0),v.get('subCount',0),v.get('subIndex',0)]
    for index,value in enumerate(fields):put(memory,P+4*index,value)
    put(memory,P+276,len(keys));memory.write(P+20,bytes(keys))
    for index,key in enumerate([1,2,254]):
        pointer=NAMES+index*1024;name=bytes([65+index])*v.get('nameLength',5);memory.write(pointer,name+b'\0');put(memory,TABLE+key*4,pointer)
    return memory,[Q,B,P]


def effect(target,args,memory,v):
    a=[value&0xffffffff for value in args];result=0;normalized=a[:]
    if target==0x20b7588:
        value=cstring(memory,a[1]);normalized=[a[0],value.hex()];result=append(memory,a[0],value)
    elif target in CB:
        name=CB[target][0]
        if name=='keys':
            kind=signed(a[0]);lists=v.get('lists',[[1,2],[1],[254]]);values=lists[kind] if 0<=kind<3 else []
            normalized=[a[0],a[1],a[2]];memory.write(a[1],bytes(values));put(memory,a[1]+256,len(values));result=0x11111111
        elif name=='count':result=v.get('counts',[0,2,1])[a[0]]
        else:
            payload=(name[0]+str(a[0])+(str(a[1]) if name!='server' else '')).encode();payload=payload[:1]*v.get('valueLength',len(payload));buffer=a[1] if name=='server' else a[2];append(memory,buffer,payload);result=0x22222222
    else:raise ValueError('Unqualified sixth caller contract')
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[];result=1
    by_name={value[0]:address for address,value in CB.items()}
    def call(target,*arguments):
        returned,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return returned
    kind=signed(word(memory,P));length=signed(word(memory,B+1400))
    if kind>=3 or 1400-length<32:result=0
    else:
        call(0x20b7588,B,MAGIC);packet_position=word(memory,B+1400);put(memory,B+1400,packet_position+1);memory.write(B+packet_position,bytes([word(memory,P+4)&255]));put(memory,P+4,word(memory,P+4)+1)
        finished=False;stop=False
        while signed(word(memory,P))<3 and not stop:
            kind=signed(word(memory,P))
            if word(memory,P+276)==0:call(by_name['keys'],kind,P+20,word(memory,Q+268))
            if word(memory,P+12)==0 and kind!=0:put(memory,P+12,call(by_name['count'],kind,word(memory,Q+268)))
            if 1400-word(memory,B+1400)<100:stop=True;break
            length=word(memory,B+1400);memory.write(B+length,bytes([kind&255]));put(memory,B+1400,length+1)
            while signed(word(memory,P+8))<signed(word(memory,P+276)):
                key=memory.read(P+20+word(memory,P+8),1)[0];name_pointer=word(memory,TABLE+4*key)
                if not call(0x20b7588,B,name_pointer):stop=True;break
                if kind==0:
                    call(by_name['server'],key,B,word(memory,Q+268))
                    if 1400-word(memory,B+1400)<1:stop=True;break
                else:
                    if 1400-word(memory,B+1400)<1:stop=True;break
                    length=word(memory,B+1400);memory.write(B+length,bytes([word(memory,P+16)&255]));put(memory,B+1400,length+1)
                    while signed(word(memory,P+16))<signed(word(memory,P+12)):
                        call(by_name['player' if kind==1 else 'team'],key,word(memory,P+16),B,word(memory,Q+268))
                        if 1400-word(memory,B+1400)<1:stop=True;break
                        put(memory,P+16,word(memory,P+16)+1)
                    if stop:break
                    if 1400-word(memory,B+1400)>0:
                        length=word(memory,B+1400);memory.write(B+length,b'\0');put(memory,B+1400,length+1)
                put(memory,P+8,word(memory,P+8)+1);put(memory,P+16,0)
            if stop:break
            if 1400-word(memory,B+1400)>0:
                length=word(memory,B+1400);memory.write(B+length,b'\0');put(memory,B+1400,length+1)
            for offset,value in [(0,kind+1),(8,0),(12,0),(16,0),(276,0)]:put(memory,P+offset,value)
        if not stop:memory.write(B+packet_position,bytes([memory.read(B+packet_position,1)[0]|128]))
    external={at:bytes(raw) for at,raw in memory.regions.items() if at!=SP-0x1000}
    return external,calls,'word',result


def cases(address):
    if address!=0x20b7b00:raise ValueError('Sixth caller lacks vectors')
    vectors=[dict(type=kind,length=length,mode=mode,initialKeys=keys,packet=packet) for kind in [0,1,2,3] for length in [0,1260,1290,1368,1369,1400] for mode in ['arm','thumb','mixed'] for keys in [[],[1],[1,2]] for packet in [0,7]]
    vectors += [dict(type=kind,length=length,initialKeys=[1,254],counts=[0,count,count],keyIndex=index,subIndex=sub,mode='mixed') for kind in [0,1,2] for length in [0,1260,1300] for count in [0,1,2] for index in [0,1] for sub in [0,1]]
    vectors += [dict(type=kind,length=length,initialKeys=[1],nameLength=name,valueLength=value,mode='mixed') for kind in [0,1,2] for length in [0,1260,1290] for name in [1,5,254] for value in [0,1,1000]]
    vectors += [dict(type=0,length=0,initialKeys=[],lists=[[],[],[]],counts=[0,0,0],mode=mode) for mode in ['arm','thumb','mixed']]
    return vectors
