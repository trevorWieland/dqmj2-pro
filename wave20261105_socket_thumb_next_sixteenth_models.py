import itertools
from wave20261105_socket_thumb_next_memory import Memory
from wave20261105_socket_thumb_next_sixteenth_callbacks import TARGETS
SOCKETS=[0x02402000,0x02402200]
SENDS=[0x02403000,0x02403200]
RECEIVES=[0x02404000,0x02404200]
PACKETS=[0x02405000,0x02405200,0x02405400]
COMMANDS=[0x02406000,0x02406200]
CONFIGS=[0x02407000,0x02407200]
QUEUE=0x02408000
CONFIG_POINTER=0x020de7cc
TRASH=0x021d15b0
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208fdc8':16,'0208fe74':32,'0208fedc':16}


def fixtures(name):
    if name=='0208fdc8':
        rows=[dict(mode=i,packets=i%4,mutate=bool(i&1),providerMode=['arm','thumb'][i//2%2],null=False) for i in range(256)]
        return rows+[dict(mode=m,packets=n,mutate=t,providerMode=p,null=z) for m,n,t,p,z in itertools.product([0,1,2,4,255],range(4),[False,True],['arm','thumb'],[False,True])]
    if name=='0208fe74':return [dict(stream=s,mutate=t,null=z,response=r) for s,t,z,r in itertools.product(['empty','null','command','reply','mixed'],[False,True],[False,True],[False,True])]
    return [dict(count=n,mutate=t) for n,t in itertools.product(range(3),[False,True])]


def scenario(name,f,ordinal):
    regions={**{p:128 for p in SOCKETS},**{p:272 for p in SENDS},**{p:276 for p in RECEIVES},**{p:12 for p in PACKETS},**{p:16 for p in COMMANDS},**{p:32 for p in CONFIGS},QUEUE:32,CONFIG_POINTER:4,TRASH:4}
    memory=Memory(regions,ordinal);get,setv=memory.get,memory.set
    socket,send,receive=SOCKETS[0],SENDS[0],RECEIVES[0]
    for i,p in enumerate(SOCKETS):setv(p+104,SENDS[i]);setv(p+100,RECEIVES[i]);setv(p+112,0x8005,2);setv(p+115,f.get('mode',0),1)
    for i,p in enumerate(CONFIGS):
        mode=f.get('providerMode','arm') if i==0 else 'thumb' if f.get('providerMode','arm')=='arm' else 'arm';pointer=TARGETS['release',mode]|int(mode=='thumb')
        if f.get('_wrongTag'):pointer^=1
        setv(p+28,pointer)
    setv(CONFIG_POINTER,CONFIGS[0]);setv(TRASH,SOCKETS[0] if f.get('count',0) else 0)
    for i,p in enumerate(PACKETS):setv(p,PACKETS[i+1] if i+1<f.get('packets',0) else 0)
    for p in RECEIVES:setv(p+260,PACKETS[0] if f.get('packets') else 0);setv(p+256,PACKETS[min(2,max(0,f.get('packets',0)-1))]);setv(p+264,63,2)
    for i,p in enumerate(COMMANDS):setv(p+8,QUEUE if i==1 or f.get('response') else 0)
    initial=memory.snapshot();actions=[];allowed=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def put(at,value,size=4):setv(at,value,size);allowed.append((at,size))
    def call(address,args,returned=0x89abcdef,changes=None,kind=None,mode=None,returnEntry=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:
            if SP-SPECS[name]<=at and at+len(raw)<=SP:continue
            memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned&0xffffffff,checks=checks,mutations=changes,kind=kind,mode=mode,returnEntry=returnEntry));return returned&0xffffffff
    def release(pointer,site,changes=None):
        address=get(get(CONFIG_POINTER)+28)&~1;mode=next(m for (k,m),a in TARGETS.items() if k=='release' and a==address)
        return call(address,[pointer],changes=changes,kind='release',mode=mode,returnEntry=(site+2)|1)
    mask=(ordinal*0x1010101^0xa5a5a5a5)&0xffffffff
    if name=='0208fdc8':
        socket=0 if f['null'] else socket;arguments=[socket,0x11223344,0x55667788,0x99aabbcc]
        if socket:
            put(socket+112,0,2);mode=get(socket+115,1)
            if mode in [0,4]:
                call(0x0208fe74,[get(socket+104)],changes=[word(socket+100,RECEIVES[1])] if f['mutate'] else [])
                call(0x0208fe74,[get(socket+100)])
            elif mode==1:
                current=get(get(socket+100)+260)
                while current:
                    nextPacket=get(current)
                    changes=[word(current,current),word(CONFIG_POINTER,CONFIGS[1]),word(socket+100,RECEIVES[1])] if f['mutate'] else []
                    release(current,0x0208fe0e,changes);current=nextPacket
                put(get(socket+100)+264,0,2);put(get(socket+100)+256,0);put(get(socket+100)+260,0)
                call(0x02006924,[get(socket+100)+268],changes=[word(socket+100,RECEIVES[0])] if f['mutate'] else [])
                call(0x0208fe74,[get(socket+100)])
            elif mode==2:call(0x0208fe74,[get(socket+104)])
            call(0x02007ff4,[],mask)
            call(0x02090248,[socket],changes=[word(CONFIG_POINTER,CONFIGS[1])] if f['mutate'] else [])
            call(0x02090284,[socket]);release(socket,0x0208fe64,changes=[word(socket+112,0xffff,2)] if f['mutate'] else [])
            call(0x02008008,[mask])
    elif name=='0208fe74':
        pipe=0 if f['null'] else send;arguments=[pipe,0x11223344,0x55667788,0x99aabbcc]
        if pipe:
            call(0x02006890,[pipe+32]);call(0x02007ff4,[],mask);call(0x02006c70,[])
            messages={'empty':[],'null':[0],'command':[COMMANDS[0]],'reply':[COMMANDS[1]],'mixed':[0,COMMANDS[0],COMMANDS[1]]}[f['stream']]
            for command in messages:
                call(0x02006eb8,[pipe,SP-28,0],1,changes=[word(SP-28,command)])
                if command:
                    if get(command+8):call(0x02006e24,[get(command+8),0xfffffff5,0],0 if f['mutate'] else 1)
                    call(0x0208ebfc,[command],changes=[word(command+8,0)] if f['mutate'] else [])
            call(0x02006eb8,[pipe,SP-28,0],0);call(0x02006ca4,[]);call(0x020069dc,[]);call(0x02008008,[mask])
    else:
        arguments=[0x11223344,0x55667788,0x99aabbcc,0x778899aa];remaining=f['count']
        changes=[word(TRASH,SOCKETS[0])] if f['mutate'] and not remaining else []
        if changes:remaining=1
        call(0x02007ff4,[],mask,changes)
        while get(TRASH):
            current=get(TRASH);remaining-=1;nextSocket=SOCKETS[1] if remaining else 0
            call(0x0208fdc8,[current],changes=[word(TRASH,nextSocket)])
        call(0x02008008,[mask])
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=None,args=arguments,allowedWrites=allowed)
