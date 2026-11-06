from wave20261105_socket_thumb_next_memory import Memory

CTX,OTHER,OUT,SOCKET,SP,STOP,CACHE,INFO=0x02400000,0x02402000,0x02410000,0x02420000,0x027f0000,0x027d0000,0x021d1748,0x020e33e4
SPECS={'02092778':16,'02092b50':48,'02092bf0':24}
NAMES=list(SPECS)


def fixtures(name):
    if name=='02092778':return [dict(path=p)for p in ['initial-error','fresh','cached-fresh','resumed','resumed-error','fresh-error','poll-reuse','captured-context','late-cache']]
    if name=='02092b50':return [dict(state=n,length=m)for n,m in [(0,7),(7,23),(8,7),(8,23),(9,27),(255,27)]]
    return [dict(case=n)for n in ['empty','age-boundaries','wrap','negative-age','thread-gates','wake-next-mutation','restore-head-change','socket-wrap','socket-negative-age']]


class Plan:
    def __init__(self,regions,ordinal):
        self.memory=Memory(regions,ordinal);self.actions=[];self.extra=[];self.writable=[];self.result=None

    def call(self,address,args=(),returned=None,mutations=(),checks=(),stack=()):
        action=dict(address=address,args=[a&0xffffffff for a in args],returned=returned if returned is not None else 0xa8000000+len(self.actions),checks=[*self.memory.snapshot().items(),*checks],mutations=list(mutations),stackWords=list(stack));self.actions.append(action)
        for base,raw in mutations:self.memory.put(base,raw)

    def finish(self,initial,args):
        return dict(initial=initial,regions=self.memory.snapshot(),args=args,actions=self.actions,result=self.result,volatileStateReads=None,readable=[(base,len(raw))for base,raw in initial.items()],extraChecks=self.extra,writable=self.writable)


def connect(f,ordinal):
    p=Plan({CTX:2176,OTHER:2176,SOCKET:64},ordinal);m=p.memory;path=f['path'];reuse=path in ['resumed','resumed-error'];cached=path=='cached-fresh';m.set(SOCKET+12,CTX);m.set(SOCKET+24,0xefff,2);m.set(SOCKET+28,0xc0a801ff);m.set(CTX+48,int(cached),1);m.set(CTX+49,int(reuse),1);m.set(CTX+1109,3,1);initial=m.snapshot();p.writable=[(CTX+1109,1)]
    changes=[(SOCKET+12,OTHER.to_bytes(4,'little'))]if path=='captured-context'else []
    p.call(0x2092470,[SOCKET],mutations=changes)
    results=[9]if path=='initial-error'else [4]if reuse or path in ['poll-reuse','fresh-error']else [0,1,4]
    for index,result in enumerate(results):
        changes=[(CTX+49,b'\x01')]if path=='poll-reuse'and index==0 else []
        p.call(0x2092174,[SOCKET],result,changes)
    if results[-1]==9:p.result=1;return p.finish(initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc])
    if reuse or path=='poll-reuse':
        p.call(0x20918a4,[CTX]);error=path=='resumed-error';p.call(0x2092754,[SOCKET],0xffffffff if error else 0)
        if error:p.result=1;return p.finish(initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc])
        p.call(0x2092380,[SOCKET])
    else:
        p.call(0x2092584,[SOCKET]);changes=[]
        if path=='late-cache':changes=[(CTX+48,b'\x80'),(SOCKET+24,b'\xff\xff'),(SOCKET+28,bytes.fromhex('785634f2'))]
        p.call(0x2091864,[CTX],mutations=changes)
        if m.get(CTX+48,1):p.call(0x2090a3c,[CTX,m.get(SOCKET+28),m.get(SOCKET+24,2)])
        p.call(0x20918a4,[CTX]);p.call(0x2092380,[SOCKET]);error=path=='fresh-error';p.call(0x2092754,[SOCKET],0x80000000 if error else 0)
        if error:p.result=1;return p.finish(initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc])
    m.set(CTX+1109,8,1);p.result=0
    return p.finish(initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc])


def shutdown(f,ordinal):
    p=Plan({CTX:2176,OTHER:2176,SOCKET:64},ordinal);m=p.memory;m.set(SOCKET+12,CTX);m.set(CTX+1109,f['state'],1);initial=m.snapshot();p.writable=[(CTX+1109,1)]
    if f['state']==8:
        buffer=SP-44;header=bytes([21,3,0,0,2,1,0]);encrypted=bytes((index*29+ordinal*11)&255 for index in range(f['length']))
        p.call(0x2091de0,[CTX,buffer],f['length'],checks=[(buffer,header)])
        p.actions[-1]['mutations']=[(buffer,encrypted),(SOCKET+12,OTHER.to_bytes(4,'little'))];m.set(SOCKET+12,OTHER)
        p.call(0x208db64,[buffer,f['length'],0,0],stack=[SOCKET],checks=[(buffer,encrypted)]);p.extra=[(buffer,encrypted)]
    m.set(CTX+1109,0,1)
    return p.finish(initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc])


def periodical(f,ordinal):
    case=f['case'];count=9 if case=='thread-gates'else 3 if case in ['wake-next-mutation','restore-head-change','socket-wrap','socket-negative-age']else 0;threads=[0x02430000+i*256 for i in range(count)];sockets=[0x02440000+i*128 for i in range(count)];contexts=[0x02450000+i*2304 for i in range(count)];regions={CACHE:368,INFO:12};regions.update({a:168 for a in threads});regions.update({a:64 for a in sockets});regions.update({a:2176 for a in contexts});p=Plan(regions,ordinal);m=p.memory;now=10 if case in ['wrap','socket-wrap']else 0 if case in ['negative-age','socket-negative-age']else 1000;times=[now-957,now-958,now+1,now-10000];valid=[1,128,255,0]
    if case=='wrap':times=[0xffffff00,0xfffffc00,11,9]
    if case=='negative-age':times=[0x80000000,0x80000001,1,0xfffffc00];valid=[1,1,1,1]
    for i in range(4):m.set(CACHE+i*92+80,times[i]&0xffffffff);m.set(CACHE+i*92+90,valid[i],1)
    for i in range(count):
        m.set(threads[i]+104,threads[i+1]if i+1<count else 0);m.set(threads[i]+164,sockets[i]);m.set(sockets[i],0x02500000+i*256);m.set(sockets[i]+4,2);m.set(sockets[i]+8,4,1);m.set(sockets[i]+9,1,1);m.set(sockets[i]+12,contexts[i]);m.set(sockets[i]+16,(now-240)&0xffffffff);m.set(contexts[i]+1109,7,1)
    if case=='thread-gates':
        m.set(threads[0]+164,0);m.set(sockets[1],0);m.set(sockets[2]+9,0,1);m.set(sockets[3]+8,3,1);m.set(contexts[4]+1109,8,1);m.set(sockets[5]+16,now-239);m.set(sockets[6]+4,1);m.set(sockets[8]+9,128,1)
    if case in ['socket-wrap','socket-negative-age']:
        times=[0xffffff1a,11,(now-239)&0xffffffff]if case=='socket-wrap'else [0x80000000,0x80000001,0xffffff10]
        for i,value in enumerate(times):m.set(sockets[i]+16,value)
    m.set(INFO+8,threads[0]if count else 0);initial=m.snapshot();cookie=0xf1234591;p.call(0x2007ff4,returned=cookie)
    for i in range(4):
        age=(now-m.get(CACHE+i*92+80))&0xffffffff
        if m.get(CACHE+i*92+90,1)and age<0x80000000 and age>957:m.set(CACHE+i*92+90,0,1)
    changes=[(INFO+8,threads[1].to_bytes(4,'little'))]if case=='restore-head-change'else []
    p.call(0x2008008,[cookie],mutations=changes);thread=m.get(INFO+8)
    while thread:
        socket=m.get(thread+164)
        if socket and m.get(socket)and m.get(socket+9,1)and m.get(socket+8,1)==4 and m.get(m.get(socket+12)+1109,1)<8:
            age=(now-m.get(socket+16))&0xffffffff
            if age<0x80000000 and age>239 and m.get(socket+4)==2:
                m.set(socket+8,0,1);m.set(socket+4,0);changes=[(thread+104,(0).to_bytes(4,'little'))]if case=='wake-next-mutation'else []
                p.call(0x200698c,[m.get(socket)],mutations=changes)
        thread=m.get(thread+104)
    p.writable=[(CACHE+i*92+90,1)for i in range(4)]+[(a+8,1)for a in sockets]+[(a+4,4)for a in sockets]
    return p.finish(initial,[now,0x11223344,0x55667788,0x99aabbcc])


def scenario(name,f,ordinal):return {'02092778':connect,'02092b50':shutdown,'02092bf0':periodical}[name](f,ordinal)
