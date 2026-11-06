import itertools
from wave20261105_socket_thumb_next_memory import Memory

COMMANDS=[0x02401000,0x02401200]
SOCKETS=[0x02402000,0x02402200]
RECEIVES=[0x02403000,0x02403200]
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208f0a0':8,'0208f0e8':24}


def fixtures(name):
    if name=='0208f0a0':
        rows=[dict(block=i,allocated=bool(i%5),mutate=bool(i&1),returned=[0,-42,0x80000000,0xffffffff][i%4],state=(i*257)&65535,local=[0,1,65535][i%3],remote=[1,32768,65535][i%3],ip=[0,1,0x89abcdef,0xffffffff][i%4]) for i in range(256)]
        return rows+[dict(block=block,allocated=allocated,mutate=mutate,returned=0x80000000,state=0x8001,local=65535,remote=32768,ip=0xffffffff) for block,allocated,mutate in itertools.product([0,1,3,127,128,255],[False,True],[False,True])]
    rows=[dict(mode=i,mutate=bool(i&1),returned=[0,1,0x80000000,0xffffffff][i%4],state=(i*257^0x8000)&65535,local=[0,1,65535][i%3],remote=[1,32768,65535][i%3],ip=[0,1,0x89abcdef,0xffffffff][i%4]) for i in range(256)]
    return rows+[dict(mode=mode,mutate=mutate,returned=returned,state=state,local=65535,remote=1,ip=0xffffffff) for mode,mutate,returned,state in itertools.product([0,1,4,255],[False,True],[0,1,0x80000000,0xffffffff],[0,0x8000,0xffff])]


def scenario(name,f,ordinal):
    memory=Memory({**{p:24 for p in COMMANDS},**{p:128 for p in SOCKETS},**{p:264 for p in RECEIVES}},ordinal);setv,getv=memory.set,memory.get
    command=COMMANDS[0];socket=SOCKETS[0];receive=RECEIVES[0]
    for index,p in enumerate(COMMANDS):setv(p,0x0208f0e9);setv(p+4,SOCKETS[index]);setv(p+12,f.get('mode',0),1);setv(p+16,f['local'],2);setv(p+18,f['remote'],2);setv(p+20,f['ip'])
    for index,p in enumerate(SOCKETS):setv(p+100,RECEIVES[index]);setv(p+112,f['state'],2);setv(p+114,f.get('block',1),1);setv(p+116,f['local'],2);setv(p+118,f['remote'],2);setv(p+120,f['ip'])
    initial=memory.snapshot();actions=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=checks,mutations=changes));return returned
    result=0;arguments=[socket,0x11223344,0x55667788,0x99aabbcc]
    if name=='0208f0a0':
        flag=f['block'] if f['block']<128 else f['block']-256
        changes=[word(socket+116,0xabcd,2),word(socket+118,0xff01,2),word(socket+120,0xaabbccdd),word(socket+112,f['state']^0x8001,2),word(command+4,SOCKETS[1])] if f['mutate'] else []
        call(0x0208ebd8,[0x0208f0e9,socket,flag],command if f['allocated'] else 0,changes)
        if not f['allocated']:result=-33
        else:
            setv(command+16,getv(socket+116,2),2);setv(command+18,getv(socket+118,2),2);setv(command+20,getv(socket+120));setv(socket+112,getv(socket+112,2)|2,2)
            changes=[word(socket+112,0xffff,2),word(command+16,7,2),word(command+20,0)] if f['mutate'] else []
            result=call(0x0208eca4,[socket,command],f['returned']&0xffffffff,changes)
    else:
        arguments[0]=command
        changes=[word(command+4,SOCKETS[1]),word(socket+100,RECEIVES[1]),word(command+16,0xabcd,2),word(command+18,0xff01,2),word(command+20,0xaabbccdd)] if f['mutate'] else []
        call(0x0200708c,[receive+224],changes=changes)
        changes=[word(command+12,0 if f['mode']==1 else 1,1)] if f['mutate'] else []
        call(0x0208d780,[getv(command+16,2),getv(command+18,2),getv(command+20)],changes=changes)
        setv(receive+248,0)
        connectResult=call(0x0208d88c,[],f['returned']&0xffffffff) if getv(command+12,1) in [0,4] else 0
        call(0x02007110,[receive+224],changes=[word(socket+112,f['state']^0x8001,2)] if f['mutate'] else [])
        if connectResult:setv(socket+112,getv(socket+112,2)|0x40,2);result=-76
        else:setv(socket+112,getv(socket+112,2)|4,2);result=0
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result&0xffffffff,args=arguments)
