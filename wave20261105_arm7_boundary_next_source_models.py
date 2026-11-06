import itertools
from wave20261105_socket_thumb_next_memory import Memory
WORK=0x027f7884
PACKETS=[0x02002000,0x02002200,0x02002400]
STATUS=[0x02004000,0x02005000]
WM_BUFFER=0x02006000
CALLBACK=0x02007000
SP=0x027fc000
STOP=0x027fb000
FRAME=72


def fixtures():
    rows=[dict(kind='null',code=0,count=0,buf=False,state=0,beacon=0,mutate=False)]
    rows += [dict(kind='confirm',code=c,count=n,buf=True,state=0,beacon=0,mutate=m) for c,n,m in itertools.product([0,1,0x7f,0x0101,0x0200,0x0280,0x7fff,0x8080,0xffff],[1,3],[False,True])]
    rows += [dict(kind='drop',code=c,count=n,buf=b,state=s,beacon=0,mutate=m) for c,n,b,s,m in itertools.product([0x84,0x86,0x8c,0x180,0x182,0x184,0x185,0x186],[1,3],[False,True],[0,1],[False,True]) if not b or s==1]
    rows += [dict(kind='default',code=c,count=n,buf=True,state=s,beacon=0,mutate=m) for c,n,s,m in itertools.product([0x80,0x81,0x82,0x83,0x89,0x8a,0x8e,0xff,0x181,0x187,0x1ff],[1,3],[0,2,65535],[False,True])]
    rows += [dict(kind='beacon',code=0x8c,count=n,buf=True,state=s,beacon=b,mutate=m) for n,s,b,m in itertools.product([1,3],[0,2],[0,1,32768,65535],[False,True])]
    return rows


def scenario(f,ordinal):
    memory=Memory({WORK:5520,**{p:20 for p in PACKETS},**{p:2000 for p in STATUS},WM_BUFFER:720,CALLBACK:48},ordinal);get,setv=memory.get,memory.set
    for p in STATUS:setv(p,f['state'],2);setv(p+194,f['beacon'],2)
    for p in PACKETS:setv(p+12,f['code'],2)
    setv(WORK+5452,WM_BUFFER if f['buf'] else 0);setv(WORK+5456,STATUS[0]);initial=memory.snapshot();actions=[];allowed=[]
    def word(at,value,width=4):return at,int(value&((1<<(width*8))-1)).to_bytes(width,'little')
    def put(at,value,width=4):setv(at,value,width);allowed.append((at,width))
    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:
            if SP-FRAME<=at and at+len(raw)<=SP:continue
            memory.put(at,raw)
        actions.append(dict(address=address,args=[a&0xffffffff for a in args],returned=returned&0xffffffff,checks=checks,mutations=changes));return returned&0xffffffff
    for index in range(f['count']):
        packet=PACKETS[index];changes=[word(SP-44,packet)]
        if f['mutate']:changes += [word(WORK+5456,STATUS[index%2]),word(STATUS[index%2]+194,f['beacon'],2)]
        call(0x037fc760,[WORK+40,SP-44,1],1,changes)
        if f['kind']=='confirm':call(0x037fc6d4,[WORK+88,packet,1],index&1)
        elif not f['buf'] or f['state']==1:pass
        else:
            if f['kind']=='beacon' and f['beacon']:
                call(0x038073f0,[],CALLBACK);put(CALLBACK,8,2);put(CALLBACK+2,0,2);put(CALLBACK+8,2,2);call(0x038073a4,[CALLBACK],changes=[word(WORK+5456,STATUS[(index+1)%2])] if f['mutate'] else [])
            call(0x027e1a08,[packet],changes=[word(packet+12,0,2)] if f['mutate'] else [])
    call(0x037fc760,[WORK+40,SP-44,1],1,[word(SP-44,0)]);call(0x037fc15c,[])
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,allowedWrites=allowed,args=[0x02001234,0x11223344,0x55667788,0x99aabbcc])
