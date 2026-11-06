import itertools
from wave20261105_socket_thumb_next_memory import Memory
SOCKETS=[0x02402000,0x02402200]
SENDS=[0x02403000,0x02403200]
COMMANDS=[0x02404000,0x02404200]
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208fbe8':16,'0208fc70':8,'0208fc90':8,'0208fcb0':8}


def signed(value):return value if value<0x80000000 else value-0x100000000


def fixtures(name):
    if name=='0208fc70':return [dict(mode=i,mutate=bool(i&1)) for i in range(256)]
    if name=='0208fc90':return [dict(value=v,invalid=i,trash=t) for v,i,t in itertools.product([0,1,SOCKETS[0],0x7fffffff,0x80000000,0xffffffff],[0,1,0xffffffff],[0,1,0x80000000])]
    if name=='0208fbe8':
        rows=[dict(mode=i,state=[0,1,5,9,13,0x8005,0xffff][i%7],block=i,invalid=int(i%11==0),send=bool(i%3),executor=bool(i%5),allocated=bool(i%7),mutate=bool(i&1),returned=[0,-42,0x80000000,0xffffffff][i%4],value=SOCKETS[0]) for i in range(256)]
        return rows+[dict(mode=mode,state=state,block=block,invalid=0,send=s,executor=e,allocated=a,mutate=t,returned=0x80000000,value=SOCKETS[0]) for mode,state,block,s,e,a,t in itertools.product([0,1],[5,0x8005],[0,1,128,255],[False,True],[False,True],[False,True],[False,True])]+[dict(mode=0,state=0,block=0,invalid=0,send=False,executor=False,allocated=False,mutate=False,returned=0,value=0)]
    rows=[dict(mode=i,state=[0,1,5,17,0x8001,0xffff][i%6],trash=int(i%11==0),invalid=int(i%13==0),mutate=bool(i&1),returned=[0,-1,0x80000000][i%3],value=SOCKETS[0]) for i in range(256)]
    return rows+[dict(mode=m,state=s,trash=t,invalid=i,mutate=z,returned=0x80000000,value=SOCKETS[0]) for m,s,t,i,z in itertools.product([0,1,4,128],[0,1,5,16,17,0x8001],[0,1],[0,1],[False,True])]+[dict(mode=0,state=0,trash=0,invalid=0,mutate=False,returned=0,value=v) for v in [0,0x80000000,0xffffffff]]


def scenario(name,f,ordinal):
    memory=Memory({**{p:128 for p in SOCKETS},**{p:272 for p in SENDS},**{p:16 for p in COMMANDS}},ordinal);get,setv=memory.get,memory.set
    socket,send,command=SOCKETS[0],SENDS[0],COMMANDS[0]
    for index,p in enumerate(SOCKETS):setv(p+104,SENDS[index] if f.get('send',True) else 0);setv(p+112,f.get('state',1),2);setv(p+114,f.get('block',1),1);setv(p+115,f.get('mode',0),1)
    for p in SENDS:setv(p+268,SOCKETS[1] if f.get('executor',True) else 0)
    for index,p in enumerate(COMMANDS):setv(p+4,SOCKETS[index])
    initial=memory.snapshot();actions=[];allowed=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def put(at,value,size=4):setv(at,value,size);allowed.append((at,size))
    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned&0xffffffff,checks=checks,mutations=changes));return returned&0xffffffff
    if name=='0208fc70':
        arguments=[command,0x11223344,0x55667788,0x99aabbcc]
        if get(socket+115,1) in [0,4]:call(0x0208d8e8,[],changes=[word(command+4,SOCKETS[1]),word(socket+115,1,1)] if f['mutate'] else [])
        result=0
    elif name=='0208fc90':
        arguments=[f['value'],0x11223344,0x55667788,0x99aabbcc];value=f['value'];result=0
        if signed(value)>=0 and call(0x02090294,[value],f['invalid']) and not call(0x020902b4,[value],f['trash']):result=1
    elif name=='0208fbe8':
        socket=f['value'];arguments=[socket,0x11223344,0x55667788,0x99aabbcc]
        invalid=call(0x02090294,[socket],f['invalid'])
        if invalid:result=-28
        elif not socket or not get(socket+112,2)&1:result=-39
        elif not get(socket+112,2)&4 or get(socket+112,2)&8:result=-56
        else:
            put(socket+112,get(socket+112,2)|8,2);send=get(socket+104)
            if send and get(send+268):
                flag=get(socket+114,1);flag=flag if flag<128 else flag-256
                changes=[word(send+268,SOCKETS[0]),word(socket+104,SENDS[1]),word(command+4,SOCKETS[1]),word(socket+114,0,1)] if f['mutate'] else []
                allocated=call(0x0208ebd8,[0x0208fc71,get(send+268),flag],command if f['allocated'] else 0,changes)
                result=call(0x0208ecb0,[get(send+268),command],f['returned']) if allocated else -33
            else:result=0
    else:
        socket=f['value'];arguments=[socket,0x11223344,0x55667788,0x99aabbcc]
        if signed(socket)<=0:result=-28
        elif call(0x020902b4,[socket],f['trash']):result=-26
        elif call(0x02090294,[socket],f['invalid']):result=0
        elif not get(socket+112,2)&1:result=-39
        elif get(socket+112,2)&16:result=-26
        else:
            put(socket+112,get(socket+112,2)|24,2)
            if get(socket+115,1) in [0,4]:call(0x0208ec1c,[get(socket+104),0],changes=[word(socket+115,1,1),word(socket+104,SENDS[1])] if f['mutate'] else [])
            call(0x0208ebd8,[0x0208fd4d,socket,1],command,changes=[word(command+4,SOCKETS[1]),word(socket+112,0xffff,2)] if f['mutate'] else [])
            put(command+8,0);call(0x0208ec50,[socket,command],f['returned']);result=0
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result&0xffffffff,args=arguments,allowedWrites=allowed)
