import itertools
from wave20261105_socket_thumb_next_memory import Memory
from wave20261105_socket_thumb_next_seventh_callbacks import TARGETS

CONFIG_SLOT=0x020de7cc
STATE=0x021d1580
QUEUE=STATE+4
CONFIG=0x02402000
PIPE=0x02403000
REPLIES=[0x02403100,0x02403200]
COMMANDS=[0x02401000,0x02401200]
SOCKETS=[0x02404000,0x02404200]
HEAP=0x02405000
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208eb34':16,'0208eb90':8,'0208ebfc':8,'0208ec1c':16,'0208ec60':56,'0208eccc':24}


def fixtures(name):
    if name=='0208eb34':return [dict(maximum=n,fail=fail,mode=mode,mutate=m) for n,fail,mode,m in itertools.product([-1,0,1,2,8,65537],[False,True],['arm','thumb'],[False,True]) if n in [0,1,2,8] or fail]
    if name=='0208eb90':return [dict(count=c,used=u,mode=mode,mutate=m) for c,u,mode,m in itertools.product([-0x80000000,-1,0,1,2,0x7fffffff],[-0x80000000,-1,0,1,2,0x7fffffff],['arm','thumb'],[False,True])]
    if name=='0208ebfc':return [dict(present=p,returned=r,mutate=m) for p,r,m in itertools.product([False,True],[0,1,0xffffffff],[False,True])]
    if name=='0208ec1c':
        rows=[dict(present=True,flag=flag,returned=[0,1,0xffffffff][flag%3],mutate=bool(flag&2)) for flag in range(256)]
        return rows+[dict(present=p,flag=flag,returned=r,mutate=m) for p,flag,r,m in itertools.product([False,True],[0,1,3,127,128,255],[0,1,0xffffffff],[False,True])]
    if name=='0208ec60':
        rows=[dict(flag=flag,sendReturn=[0,1,0xffffffff][flag%3],reply=[0,0x80000000,0xffffffff][flag%3],mutate=bool(flag&2)) for flag in range(256)]
        return rows+[dict(flag=flag,sendReturn=r,reply=reply,mutate=m) for flag,r,reply,m in itertools.product([0,1,3,128,255],[0,1,0x80000000,0xffffffff],[0,0x80000000,0xffffffff],[False,True])]
    return [dict(events=n,mode=mode,socket=s,response=r,mutate=m,returned=value) for n,mode,s,r,m,value in itertools.product([0,1,2,3],['arm','thumb'],[False,True],[False,True],[False,True],[0,0x80000000,0xffffffff])]


def scenario(name,f,ordinal):
    sizes={CONFIG_SLOT:4,STATE:36,CONFIG:32,PIPE:32,HEAP:448,**{p:32 for p in REPLIES},**{p:16 for p in COMMANDS},**{p:112 for p in SOCKETS}}
    memory=Memory(sizes,ordinal);setv,getv=memory.set,memory.get
    mode=f.get('mode','thumb')
    def pointer(kind):
        value=TARGETS[(kind,mode)]|int(mode=='thumb')
        return value^1 if f.get('wrongCallbackTag')==kind else value
    setv(CONFIG_SLOT,CONFIG);setv(CONFIG+24,pointer('allocate'));setv(CONFIG+28,pointer('release'));setv(STATE,HEAP);setv(QUEUE+20,f.get('count',2));setv(QUEUE+28,f.get('used',2))
    for index,p in enumerate(COMMANDS):
        setv(p,pointer('handler'));setv(p+4,SOCKETS[index] if f.get('socket',True) else 0);setv(p+8,REPLIES[index] if f.get('response',True) else 0);setv(p+13,f.get('flag',1),1)
    initial=memory.snapshot();actions=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def call(address,args,returned=0x89abcdef,changes=None,fixtureKind=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:
            if at>=SP-128:continue
            memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=checks,mutations=changes,fixtureMode=mode if fixtureKind else None,fixtureKind=fixtureKind));return returned
    def initialize(queue,array,count):
        raw=bytes(16)+int(array).to_bytes(4,'little')+int(count&0xffffffff).to_bytes(4,'little')+bytes(8)
        return [(queue,raw)]
    result=None;command=COMMANDS[0];arguments=[PIPE,command,0x55667788,0x99aabbcc]
    if name=='0208eb34':
        maximum=f['maximum'];arguments[0]=maximum&0xffffffff;messageBytes=(maximum*4+3)&0xfffffffc;packetBytes=(maximum*44+3)&0xfffffffc
        allocated=0 if f['fail'] else HEAP
        call(TARGETS[('allocate',mode)],[(messageBytes+packetBytes)&0xffffffff],allocated,[word(CONFIG+24,0)] if f['mutate'] else [],'allocate')
        if not allocated:result=0xffffffff
        else:
            call(0x02006dfc,[QUEUE,allocated,maximum],changes=initialize(QUEUE,allocated,maximum))
            for index in range(max(0,maximum)):
                packet=(allocated+messageBytes+44*index)&0xffffffff;changes=[word(allocated+index*4,packet),word(QUEUE+28,index+1)]
                if f['mutate']:changes+=[word(STATE,0)]
                call(0x0208ebfc,[packet],changes=changes)
            setv(STATE,allocated);result=0
    elif name=='0208eb90':
        if f['used']<f['count']:result=0xffffffff
        else:
            call(TARGETS[('release',mode)],[getv(STATE)],changes=[word(STATE,HEAP+128)] if f['mutate'] else [],fixtureKind='release');setv(STATE,0);result=0
    elif name=='0208ebfc':
        arguments[0]=command if f['present'] else 0
        if f['present']:call(0x02006e24,[QUEUE,command,0],f['returned'],[word(command+8,REPLIES[1])] if f['mutate'] else [])
    elif name=='0208ec1c':
        command=command if f['present'] else 0;arguments[1]=command;block=0 if command and not f['flag']&1 else 1
        call(0x02006e24,[PIPE,command,block],f['returned'],[word(COMMANDS[0]+13,f['flag']^0xff,1)] if f['mutate'] else [])
        if not f['returned']:call(0x0208ebfc,[command])
        result=0 if f['returned'] else (-42)&0xffffffff
    elif name=='0208ec60':
        if f['flag']==1:
            queue=SP-48;response=SP-56;reply=SP-52
            call(0x02006dfc,[queue,response,1],changes=initialize(queue,response,1)+[word(response,0)])
            setv(command+8,queue)
            call(0x0208ec1c,[PIPE,command],f['sendReturn'],[word(command+8,REPLIES[1])] if f['mutate'] else [])
            call(0x02006eb8,[queue,reply,1],changes=[word(reply,f['reply'])]);result=f['reply']
        else:
            setv(command+8,0);call(0x0208ec1c,[PIPE,command],f['sendReturn'],[word(command+8,REPLIES[1])] if f['mutate'] else []);result=f['sendReturn']
    else:
        for event in range(f['events']+1):
            command=COMMANDS[event%2] if event<f['events'] else 0
            call(0x02006ff8,[PIPE,SP-24,1],changes=[word(SP-24,command)])
            if not command:break
            returned=(f['returned']^(event<<8))&0xffffffff;changes=[]
            if f['mutate']:changes=[word(command+4,SOCKETS[1]),word(command+8,REPLIES[1])]
            call(TARGETS[('handler',mode)],[command],returned,changes,'handler')
            level=(0x98760080^ordinal^event)&0xffffffff;call(0x02007ff4,[],level);call(0x02006c70,[])
            active=COMMANDS[1-event%2] if f['mutate'] else command
            call(0x02006eb8,[PIPE,0,0],changes=[word(SP-24,active)] if f['mutate'] else [])
            socket=getv(active+4)
            if socket:setv(socket+108,returned)
            response=getv(active+8)
            if response:call(0x02006e24,[response,returned,0])
            call(0x0208ebfc,[active]);call(0x02006ca4,[]);call(0x02008008,[level])
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result,args=arguments)
