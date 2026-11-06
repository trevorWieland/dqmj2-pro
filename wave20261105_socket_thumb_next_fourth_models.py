import itertools
from wave20261105_socket_thumb_next_memory import Memory
from wave20261105_socket_thumb_next_fourth_callbacks import TARGETS

SINGLETON=0x020e33e4
THREADS=[0x02400100,0x02400300,0x02400500]
SOCKETS=[0x02401000,0x02401200,0x02401400]
BUFFERS=[0x02402000,0x02402100]
IP=0x02403000
PACKET=0x02403100
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208d228':32}


def fixtures(name):
    product=itertools.product([-1,0,1,2,3],['none','wake','thumb0','thumb1','arm0','arm1'],[False,True],[False,True],[(0,0),(1,0),(1,1),(1,0xffffffff)])
    return [dict(route=route,branch=branch,occupied=occupied,mutate=mutate,checksum=pair[0],checksumStatus=pair[1],skip=i%6,peer=['unbound','broadcast','exact'][i%3],length=[4,8,12,40][i%4],capacity=[0,4,8][i%3],sourcePort=[0,1,0x1234,65535][i%4],destinationPort=[1,0x5678,65535][i%3]) for i,(route,branch,occupied,mutate,pair) in enumerate(product)]


def scenario(name,f,ordinal):
    sizes={SINGLETON:12,IP:20,PACKET:40,**{p:168 for p in THREADS},**{p:100 for p in SOCKETS},**{p:32 for p in BUFFERS}}
    memory=Memory(sizes,ordinal);setv,getv=memory.set,memory.get;sourceIP=0xc0a80102;destinationIP=0x0a0b0c0d
    setv(SINGLETON+4,THREADS[2]);setv(SINGLETON+8,0 if f['route']==-1 else THREADS[0])
    memory.put(IP+12,sourceIP.to_bytes(4,'big'));memory.put(IP+16,destinationIP.to_bytes(4,'big'))
    memory.put(PACKET,f['sourcePort'].to_bytes(2,'big'));memory.put(PACKET+2,f['destinationPort'].to_bytes(2,'big'));setv(PACKET+6,f['checksum'],2)
    mode='thumb' if f['branch'].startswith('thumb') else 'arm'
    callback=TARGETS[mode]|int(mode=='thumb') if f['branch'].startswith(('thumb','arm')) else 0
    if f.get('wrongCallbackTag') and callback:callback^=1
    wantedKind=3 if f['branch']=='wake' else 0
    for index,thread in enumerate(THREADS):
        socket=SOCKETS[index];setv(thread+104,THREADS[index+1] if index<2 else 0);setv(thread+164,socket)
        setv(socket,thread);setv(socket+4,(0 if wantedKind else 3) if f['mutate'] else wantedKind);setv(socket+8,10,1);setv(socket+10,f['destinationPort'],2)
        setv(socket+24,0 if f['peer']=='unbound' else f['sourcePort'],2);setv(socket+28,{'unbound':0,'broadcast':0xffffffff,'exact':sourceIP}[f['peer']]);setv(socket+56,0 if f['mutate'] else callback)
        setv(socket+60,f['capacity']);setv(socket+64,BUFFERS[0]);setv(socket+68,4 if f['occupied'] else 0)
        if index!=f['route']:
            skip=f['skip']
            if skip==0:setv(thread+164,0)
            elif skip==1:setv(socket,0)
            elif skip==2:setv(socket+8,4,1)
            elif skip==3:setv(socket+10,f['destinationPort']^1,2)
            elif skip==4:setv(socket+24,(f['sourcePort']+1)%65536 or 1,2)
            else:setv(socket+28,sourceIP^0x10000)
    initial=memory.snapshot();actions=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def call(address,args,returned=0x89abcdef,changes=None,fixtureMode=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=checks,mutations=changes,fixtureMode=fixtureMode));return returned
    if f['checksum']:
        changes=[word(SINGLETON+4,THREADS[1])] if f['mutate'] else []
        call(0x0208bbac,[PACKET,f['length'],IP,17],f['checksumStatus'],changes)
    if not f['checksum'] or f['checksumStatus']==0:
        level=(0x98760080^ordinal)&0xffffffff
        changes=[word(SINGLETON+8,THREADS[1])] if f['mutate'] else []
        call(0x02007ff4,[],level,changes);thread=getv(SINGLETON+8);seen=set()
        while thread:
            if thread in seen:raise ValueError('Fixture thread list is cyclic')
            seen.add(thread);socket=getv(thread+164)
            sourcePort=int.from_bytes(memory.read(PACKET,2),'big');destinationPort=int.from_bytes(memory.read(PACKET+2,2),'big');src=int.from_bytes(memory.read(IP+12,4),'big')
            valid=socket and getv(socket) and getv(socket+8,1)==10 and getv(socket+10,2)==destinationPort
            valid=valid and (getv(socket+24,2)==0 or getv(socket+24,2)==sourcePort)
            valid=valid and getv(socket+28) in [0,0xffffffff,src]
            if not valid:thread=getv(thread+104);continue
            setv(socket+20,int.from_bytes(memory.read(IP+16,4),'big'))
            if getv(socket+28)==0:setv(socket+28,src);setv(socket+24,sourcePort,2)
            if getv(socket+68):break
            size=min((f['length']-8)&0xffffffff,getv(socket+60));setv(socket+68,size);buffer=getv(socket+64)
            changes=[(buffer,memory.read(PACKET+8,size))]
            if f['mutate']:changes += [word(socket+4,wantedKind),word(socket,THREADS[2]),word(socket+64,BUFFERS[1]),word(socket+68,size+1),word(socket+56,callback)]
            call(0x02008e0c,[PACKET+8,buffer,size],changes=changes)
            if getv(socket+4)==3:
                setv(socket+4,0);call(0x0200698c,[getv(socket)],changes=[word(socket+68,7)] if f['mutate'] else [])
            elif getv(socket+56):
                returned=0 if f['branch'].endswith('0') else 0xffffffff
                call(getv(socket+56)&~1,[getv(socket+64),getv(socket+68),socket],returned,[word(socket+68,9)] if f['mutate'] else [],mode)
                if returned:setv(socket+68,0)
            break
        call(0x02008008,[level],changes=[word(SINGLETON+4,THREADS[0])] if f['mutate'] else [])
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=None,args=[IP,PACKET,f['length'],0x99aabbcc])
