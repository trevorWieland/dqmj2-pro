import itertools
from wave20261105_socket_thumb_next_memory import Memory
SOCKETS=[0x02402000,0x02402200,0x02402400]
CONFIGS=[0x02403000,0x02403200]
ADDRESS=0x02404000
INPUT=0x02404200
BUFFER=0x02405000
RAW=0x02406000
DNS=0x02407000
CONFIG_POINTER=0x020de7cc
BSS=0x021d1540
LIST=0x021d15ac
TRASH=0x021d15b0
UDP=0x021d154c
WRAPPER=0x021d15b4
SP=0x027f0000
STOP=0x027e0000
TARGETS={('release','thumb'):0x02500100,('release','arm'):0x02500200,('socallocate','thumb'):0x02500300,('socallocate','arm'):0x02500400,('socrelease','thumb'):0x02500500,('socrelease','arm'):0x02500600}
SPECS=dict(zip(['0208ff04','0208ff70','0208ffdc','0209026c','02090294','020902f0','02090310','02090350','02090378','020903d0','020903f8','020904ec','02090554','02090580','02090608','02090624','0209063c'],[16,24,8,0,8,0,16,16,32,16,32,16,16,16,8,8,24]))


def swap(value,width):return int.from_bytes(int(value).to_bytes(width,'little'),'big')


def signed(value):return value if value<0x80000000 else value-0x100000000


def fixtures(name):
    if name=='0208ff04':return [dict(requested=r,waits=w,exit=e,result=s,lan=l,mutate=m,providerMode=p) for r,w,e,s,l,m,p in itertools.product([0,0x12345678],range(3),[0,-1],[-1,0,9],[False,True],[False,True],['arm','thumb'])]
    if name=='0208ff70':return [dict(count=i%4,skip=i//4%8,udp=i//32%4-1,trash=bool(i&1),remove=bool(i&2),mutate=bool(i&16)) for i in range(256)]
    if name=='0208ffdc':return [dict(udp=u,allResult=a,closed=c,scavenge=s,mutate=m) for u,a,c,s,m in itertools.product([False,True],[0,-26,-1],[0,1,0xffffffff],[0,1],[False,True])]
    if name=='0209026c':return [dict(count=n,target=t) for n,t in itertools.product(range(4),range(-1,4))]
    if name=='02090294':return [dict(value=v,found=b) for v,b in itertools.product([0,0xffffffff,0x80000000,1,SOCKETS[0],0x7fffffff],[False,True])]
    if name=='02090608':return [dict(size=s,null=z,providerMode=p) for s,z,p in itertools.product([0,1,4,127,0x7ffffffc,0x80000000,0xfffffffc,0xffffffff],[False,True],['arm','thumb'])]
    if name=='02090624':return [dict(size=s,null=z,providerMode=p) for s,z,p in itertools.product([0,1,0x7fffffff,0x80000000,0xffffffff],[False,True],['arm','thumb'])]
    if name=='0209063c':return [dict(flag=f,index=i,result=r,providerMode=p) for f,i,r,p in itertools.product([0,1,2,0xffffffff],range(6),[-1,0,7],['arm','thumb'])]
    if name=='02090554':return [dict(ip=v) for v in [0,1,0x7fffffff,0x80000000,0xffffffff,0x12345678,0x01020304]]
    if name=='02090580':return [dict(ip=a,ip2=b,result=r,alias=z) for a,b,r,z in itertools.product([0,1,0x12345678,0xffffffff],[0,0x87654321,0xffffffff],[-1,0,7],[False,True])]
    if name=='020904ec':return [dict(null=z,ip=i,port=p,mutate=m) for z,i,p,m in itertools.product([False,True],[0,1,0x12345678,0xffffffff],[0,1,255,256,32768,65535],[False,True])]
    return [dict(port=p,ip=i,result=r,null=z,flags=flag,length=n) for p,i,r,z,flag,n in [(0,0,-1,False,0,0),(1,1,0,True,4,1),(0x1234,0x12345678,7,False,0x80000000,3),(0xffff,0xffffffff,0x7fffffff,True,0xffffffff,0x7fffffff),(0x8000,0x80000000,-26,False,0x10203040,-1),(0x0100,0x01020304,1,False,1,5),(0x1234,0x12345678,0,False,4,2)]]


def scenario(name,f,ordinal):
    sizes={**{p:128 for p in SOCKETS},**{p:44 for p in CONFIGS},ADDRESS:8,INPUT:52,BUFFER:32,RAW:32,DNS:8,CONFIG_POINTER:4,BSS:240,0x021cfd48:4}
    memory=Memory(sizes,ordinal);get,setv=memory.get,memory.set
    for i,p in enumerate(SOCKETS):setv(p+124,SOCKETS[i+1] if i+1<f.get('count',0) else 0);setv(p+112,16 if f.get('skip',0)&(1<<i) else 0,2);setv(p+116,f.get('port',0),2)
    for i,p in enumerate(CONFIGS):
        mode=f.get('providerMode','arm') if not i else 'thumb' if f.get('providerMode','arm')=='arm' else 'arm';setv(p+28,TARGETS['release',mode]|int(mode=='thumb'));setv(p+40,BUFFER if f.get('lan',False) else 0)
    setv(CONFIG_POINTER,CONFIGS[0]);setv(0x021d1544,f.get('requested',0));setv(0x021cfd48,0xaabbccdd);setv(0x021d1550+28,RAW)
    setv(LIST,SOCKETS[0] if f.get('count',0) else 0);setv(TRASH,SOCKETS[2] if f.get('trash',False) else 0)
    udp=f.get('udp',False);setv(UDP,SOCKETS[0] if udp is True else SOCKETS[udp] if type(udp)==int and 0<=udp<3 else 0)
    mode=f.get('providerMode','arm');tag=int(mode=='thumb')
    setv(WRAPPER+12,TARGETS['socallocate',mode]|tag);setv(WRAPPER+4,TARGETS['socrelease',mode]|tag)
    setv(ADDRESS+2,f.get('port',0),2);setv(ADDRESS+4,f.get('ip',0));setv(RAW,f.get('size',0));setv(DNS,f.get('ip',0));setv(DNS+4,f.get('ip2',0))
    if name=='0209063c':
        setv(INPUT+4,TARGETS['socallocate',mode]|tag);setv(INPUT+8,TARGETS['socrelease',mode]|tag);setv(INPUT+12,f['flag'])
        for i,at in enumerate([16,20,24,28,32]):setv(INPUT+at,([0,1,0x12345678,0x80000000,0xffffffff,0x01020304][(f['index']+i)%6]))
        setv(INPUT+44,[0,1,0x7fffffff,0x80000000,0xffffffff,1500][f['index']]);setv(INPUT+48,0xffffffff-ordinal)
    initial=memory.snapshot();actions=[];allowed=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def put(at,value,size=4):setv(at,value,size);allowed.append((at,size))
    def call(address,args,returned=0x89abcdef,changes=None,kind=None,mode=None,returnEntry=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:
            if SP-SPECS[name]<=at and at+len(raw)<=SP:continue
            memory.put(at,raw)
        value=returned&0xffffffff;actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=value,checks=checks,mutations=changes,kind=kind,mode=mode,returnEntry=returnEntry));return value
    def indirect(kind,args,site,returned=0x89abcdef,changes=None):
        pointer=get(get(CONFIG_POINTER)+28) if kind=='release' else get(WRAPPER+(12 if kind=='socallocate' else 4));address=pointer&~1;actualMode=next(m for (k,m),a in TARGETS.items() if k==kind and a==address)
        if f.get('_wrongTag'):
            if kind=='release':setv(get(CONFIG_POINTER)+28,pointer^1)
            else:setv(WRAPPER+(12 if kind=='socallocate' else 4),pointer^1)
        return call(address,args,returned,changes,kind,actualMode,(site+2)|1)
    mask=(ordinal*0x1010101^0xa5a5a5a5)&0xffffffff
    arguments=[0x11223344,0x55667788,0x99aabbcc,0x778899aa];result=0
    if name=='0208ff04':
        if not get(0x021d1544):put(0x021d1544,get(0x021cfd48))
        for i in range(f['waits']):call(0x0208ffdc,[],-26);call(0x02006b7c,[100])
        call(0x0208ffdc,[],f['exit']);result=call(0x0208eb90,[],f['result'])
        if signed(result)>=0:
            call(0x0208baac,[]);call(0x0208baa0,[0],changes=[word(CONFIG_POINTER,CONFIGS[1])] if f['mutate'] else [])
            if not get(get(CONFIG_POINTER)+40):indirect('release',[get(0x021d1550+28)],0x0208ff54)
            put(CONFIG_POINTER,0)
    elif name=='0208ff70':
        while True:
            call(0x02007ff4,[],mask);current=get(LIST)
            while current and (current==get(UDP) or get(current+112,2)&16):current=get(current+124)
            changes=[word(TRASH,SOCKETS[0])] if f['mutate'] else []
            call(0x02008008,[mask],changes=changes)
            if not current:break
            changes=[word(LIST,get(current+124))] if f['remove'] and get(LIST)==current else [word(current+112,get(current+112,2)|16,2)]
            call(0x0208fcb0,[current],-1,changes)
        result=0 if ((get(LIST)==0 or (get(LIST)==get(UDP) and get(get(LIST)+124)==0)) and not get(TRASH)) else 0xffffffe6
    elif name=='0208ffdc':
        result=0xffffffe6
        if get(UDP):
            result=call(0x0208ff70,[],f['allResult'],changes=[word(UDP,SOCKETS[1])] if f['mutate'] else [])
            if result==0:
                call(0x0208fcb0,[get(UDP)],changes=[word(UDP,SOCKETS[2])] if f['mutate'] else [])
                if call(0x0208fc90,[get(UDP)],f['closed']):put(UDP,0)
                result=0xffffffe6
            call(0x0208fedc,[])
        elif call(0x0208ba68,[],f['scavenge']):call(0x0208b568,[0]);result=0
    elif name=='0209026c':
        target=SOCKETS[f['target']] if 0<=f['target']<3 else 0 if f['target']==-1 else BUFFER;arguments=[LIST,target,arguments[2],arguments[3]];location=LIST;current=get(location)
        while current and current!=target:location=current+124;current=get(location)
        result=location if current else 0
    elif name=='02090294':
        arguments[0]=f['value'];result=1
        if signed(f['value'])>0:result=int(call(0x0209026c,[LIST,f['value']],LIST if f['found'] else 0)==0)
    elif name in ['020902f0','02090310']:
        arguments=[SOCKETS[0],ADDRESS,arguments[2],arguments[3]];args=[SOCKETS[0],swap(get(ADDRESS+2,2),2)]
        if name=='02090310':args.append(swap(get(ADDRESS+4),4))
        result=call(0x0208ef98 if name=='020902f0' else 0x0208eff0,args,f['result'])
    elif name in ['02090350','020903d0','02090378','020903f8']:
        arguments=[SOCKETS[0],BUFFER,f['length']&0xffffffff,f['flags']];fromAddress=0 if f['null'] else ADDRESS
        if name in ['02090378','020903f8']:arguments.append(fromAddress)
        target=0x0208f14c if name in ['02090350','02090378'] else 0x0208f724;changes=[]
        if name=='02090378':args=[arguments[0],BUFFER,f['length'],SP-24,SP-20,f['flags']];changes=[word(SP-24,f['port'],2),word(SP-20,f['ip'])]
        elif name=='020903f8':args=[arguments[0],BUFFER,f['length'],swap(get(ADDRESS+2,2),2) if fromAddress else 0,swap(get(ADDRESS+4),4) if fromAddress else 0,f['flags']]
        else:args=[arguments[0],BUFFER,f['length'],0,0,0]
        if name in ['02090350','02090378'] and f['length']>0:changes.append((BUFFER,b'abc'[:min(3,f['length'])]))
        result=call(target,args,f['result'],changes)
        if name=='02090378' and signed(result)>=0 and fromAddress:put(fromAddress+2,swap(f['port'],2),2);put(fromAddress+4,swap(f['ip'],4))
    elif name=='020904ec':
        arguments=[0 if f['null'] else SOCKETS[0],ADDRESS,arguments[2],arguments[3]]
        if not arguments[0]:result=0xffffffd9
        else:
            ip=call(0x020900f4,[],f['ip'],[word(SOCKETS[0]+116,0x2468,2)] if f['mutate'] else []);port=get(SOCKETS[0]+116,2) if ip else 0;put(ADDRESS,8,1);put(ADDRESS+1,2,1);put(ADDRESS+2,swap(port,2),2);put(ADDRESS+4,swap(ip,4))
    elif name=='02090554':result=swap(call(0x020900f4,[],f['ip']),4)
    elif name=='02090580':
        second=DNS if f['alias'] else DNS+4;arguments=[DNS,second,arguments[2],arguments[3]];result=call(0x020900d0,[swap(get(DNS),4),swap(get(second),4)],f['result'])
    elif name=='02090608':
        arguments[0]=f['size'];total=(f['size']+4)&0xffffffff;pointer=indirect('socallocate',[0,total],0x02090614,0 if f['null'] else RAW);result=pointer
        if pointer:put(pointer,total);result=pointer+4
    elif name=='02090624':
        arguments[0]=0 if f['null'] else RAW+4;result=None
        if arguments[0]:indirect('socrelease',[0,RAW,get(RAW)],0x02090634)
    elif name=='0209063c':
        arguments[0]=INPUT;output=WRAPPER+64;put(output,int(get(INPUT+12)==1))
        for source,dest in zip([16,20,24,28,32],[4,8,12,16,20]):put(output+dest,swap(get(INPUT+source),4))
        put(output+24,0x02090609);put(output+28,0x02090625);put(WRAPPER+12,get(INPUT+4));put(WRAPPER+4,get(INPUT+8));put(output+32,64);put(output+48,get(INPUT+44));put(output+52,get(INPUT+48));result=call(0x0208e990,[output],f['result'])
    else:raise ValueError('Unknown independently owned lifecycle/adapter caller')
    if f.get('_wrongTag'):
        for action in actions:
            for i,(base,raw) in enumerate(action['checks']):
                if base in initial:initial[base]=raw
            if action.get('kind'):break
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result,args=arguments,allowedWrites=allowed)
