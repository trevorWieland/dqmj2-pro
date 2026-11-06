import itertools
from wave20261105_socket_thumb_next_memory import Memory
COMMANDS=[0x02401000,0x02401200]
SOCKETS=[0x02402000,0x02402200]
RECEIVES=[0x02403000,0x02403200]
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208f404':24,'0208f508':8}


def fixtures(name):
    if name=='0208f404':
        return [dict(limit=n,port=port,ip=ip,returned=result,mutate=mutate) for n,port,ip,result,mutate in itertools.product([0,1,32767,0x7fffffff],[0,0x02406000],[0,0x02406004],[0,-1,0x80000000,0x12345678],[False,True])]
    return [dict(consumed=c,minimum=n,allocated=a,returned=r,mutate=t) for c,n,a,r,t in itertools.product([0,1,15,65534,65535,65536,0x7fffffff,0x80000000,0xffffffff],[0,1,16,65535],[False,True],[0,-42,0x80000000],[False,True])]


def signed(v):return v if v<0x80000000 else v-0x100000000


def scenario(name,f,ordinal):
    memory=Memory({**{p:32 for p in COMMANDS},**{p:128 for p in SOCKETS},**{p:264 for p in RECEIVES}},ordinal);get,setv=memory.get,memory.set
    command,socket,receive=COMMANDS[0],SOCKETS[0],RECEIVES[0]
    for i,p in enumerate(COMMANDS):setv(p+4,SOCKETS[i])
    for i,p in enumerate(SOCKETS):setv(p+100,RECEIVES[i])
    for p in RECEIVES:setv(p+248,f.get('consumed',0));setv(p+252,f.get('minimum',0),2)
    initial=memory.snapshot();actions=[];allowed=[]
    def word(at,v,size=4):return at,int(v&((1<<(size*8))-1)).to_bytes(size,'little')
    def call(address,args,returned,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned&0xffffffff,checks=checks,mutations=changes));return returned&0xffffffff
    if name=='0208f404':
        arguments=[socket,0x02405000,f['limit'],f['port'],f['ip']]
        changes=[word(socket+100,RECEIVES[1]),word(command+4,SOCKETS[1])] if f['mutate'] else []
        call(0x0208ebd8,[0x0208f431,socket,1],command,changes)
        for offset,value in zip([16,20,24,28],arguments[1:]):setv(command+offset,value);allowed.append((command+offset,4))
        result=call(0x0208eca4,[socket,command],f['returned'],changes=[word(command+20,0),word(socket+108,0x12345678)] if f['mutate'] else [])
    else:
        arguments=[socket,0x11223344,0x55667788,0x99aabbcc]
        if signed(get(receive+248))<get(receive+252,2):result=0
        else:
            changes=[word(socket+100,RECEIVES[1]),word(receive+248,0),word(receive+252,65535,2),word(command+4,SOCKETS[1])] if f['mutate'] else []
            call(0x0208ebd8,[0x0208f541,socket,0],command if f['allocated'] else 0,changes)
            result=call(0x0208eca4,[socket,command],f['returned']) if f['allocated'] else -33
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result&0xffffffff,args=arguments,allowedWrites=allowed)
