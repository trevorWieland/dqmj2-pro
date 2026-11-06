from wave20261105_gamespy_qr2_next_sixth_models import CB,dynamic_callbacks,cstring,append
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put,signed

Q,B,K,NAMES=0x2170000,0x2172000,0x2174000,0x2176000
SP,STOP,TMP,MAGIC,TABLE,UNKNOWN=0x2701000,0x27e0000,0x2700800,0x20e25b4,0x20e277c,0x20e25ac
ARITY={0x20b7588:2,**{address:value[1]for address,value in CB.items()}}


def initial(address,v):
    if address!=0x20b7920:raise ValueError('Ninth caller outside owned scope')
    memory=Memory({Q:bytes([0xa5])*272,B:bytes([0xce])*1404,K:bytes(256),NAMES:bytes(4096),MAGIC:b'\0',UNKNOWN:b'unknown\0',TABLE:bytes(1020),SP-0x1000:bytes(0x1000)})
    put(memory,B+1400,v['length']);put(memory,Q+268,0x89abcdef)
    for callback,binding in dynamic_callbacks(v).items():put(memory,Q+CB[callback][2],callback|(1 if binding['mode']=='thumb'else 0))
    memory.write(K,bytes(v.get('keys',[1,254])))
    for index,key in enumerate([1,2]):
        pointer=NAMES+index*1024;memory.write(pointer,bytes([65+index])*v.get('nameLength',3)+b'\0');put(memory,TABLE+key*4,pointer)
    return memory,[Q,B,v['type'],v['keycount'],K]


def effect(target,args,memory,v):
    a=[value&0xffffffff for value in args];result=0;normalized=a[:]
    if target==0x20b7588:
        value=cstring(memory,a[1]);normalized=[a[0],value.hex()];result=append(memory,a[0],value)
    elif target in CB:
        name=CB[target][0]
        if name=='keys':
            lists=v.get('lists',[[1,7],[1,254],[2]]);values=lists[a[0]]if a[0]<3 else []
            if not(SP-0x1000<=a[1]and a[1]+260<=SP):raise ValueError('Callback key-buffer ABI left bounded stack')
            normalized=[a[0],a[2]];memory.write(a[1],bytes(values));put(memory,a[1]+256,len(values));result=0x11111111
        elif name=='count':result=v.get('count',2)
        else:
            if not v.get('noValue',False):
                payload=(name[0]+str(a[0])+(str(a[1])if name!='server'else '')).encode();buffer=a[1]if name=='server'else a[2];append(memory,buffer,payload)
            result=0x22222222
    else:raise ValueError('Ninth callback contract absent')
    return result&0xffffffff,normalized


def model(address,v):
    memory,args=initial(address,v);calls=[];kind=v['type'];keycount=v['keycount'];keys=K;count=1;names={value[0]:address for address,value in CB.items()}
    def call(target,*arguments):
        result,normalized=effect(target,list(arguments),memory,v);calls.append((hex(target),normalized));return result
    stop=keycount==0
    if not stop and kind in (1,2):
        if 1400-word(memory,B+1400)<2:stop=True
        else:
            count=signed(call(names['count'],kind,word(memory,Q+268)));at=word(memory,B+1400);memory.write(B+at,(count&65535).to_bytes(2,'big'));put(memory,B+1400,at+2)
    if not stop and keycount==255:
        call(names['keys'],kind,TMP,word(memory,Q+268));keycount=word(memory,TMP+256);keys=TMP
        for index in range(keycount):
            key=memory.read(keys+index,1)[0];pointer=word(memory,TABLE+4*key)or UNKNOWN;call(0x20b7588,B,pointer)
            if kind==0:
                before=word(memory,B+1400);call(names['server'],key,B,word(memory,Q+268))
                if before==word(memory,B+1400):call(0x20b7588,B,MAGIC)
        if 1400-word(memory,B+1400)<1:stop=True
        else:
            length=word(memory,B+1400);memory.write(B+length,b'\0');put(memory,B+1400,length+1)
            if kind==0:stop=True
    if not stop:
        for position in range(max(count,0)):
            for index in range(keycount):
                key=memory.read(keys+index,1)[0];before=word(memory,B+1400)
                if kind==0:call(names['server'],key,B,word(memory,Q+268))
                elif kind in (1,2):call(names['player'if kind==1 else 'team'],key,position,B,word(memory,Q+268))
                if before==word(memory,B+1400):call(0x20b7588,B,MAGIC)
    return {at:bytes(raw)for at,raw in memory.regions.items()if at!=SP-0x1000},calls,'void',0


def cases(address):
    if address!=0x20b7920:raise ValueError('Ninth caller lacks vectors')
    vectors=[dict(type=kind,keycount=count,length=length,mode=mode,noValue=empty)for kind in [0,1,2,3]for count in [0,1,2,255]for length in [0,1398,1399,1400]for mode in ['arm','thumb','mixed']for empty in [False,True]]
    vectors +=[dict(type=kind,keycount=keycount,length=length,count=count,mode='mixed',noValue=empty)for kind in [1,2]for keycount in [1,255]for length in [0,1398]for count in [-65535,-1,0,1,2]for empty in [False,True]]
    vectors +=[dict(type=kind,keycount=255,length=0,lists=[[],[],[]],mode=mode)for kind in [0,1,2]for mode in ['arm','thumb','mixed']]
    return vectors
