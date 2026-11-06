import itertools
from wave20261105_socket_thumb_next_memory import Memory

SOCKET=0x02401000
RECEIVE=0x02402000
DATAGRAM=0x02403000
CONNECTING=0x020de7d0
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208eff0':16,'02090138':16,'020901e4':8}


def fixtures(name):
    if name=='020901e4':return [dict(receive=r,mode=m,datagram=d,received=count,consumed=c,size=[0,1,65535][i%3]) for i,(r,m,d,count,c) in enumerate(itertools.product([False,True],[0,1,2,3,4,255],[False,True],[0,1,17,65535],[0,1,17]))]
    if name=='0208eff0':
        rows=[dict(state=s,mode=[0,1,2,3,4,255][s%6],block=[0,1,3,128,255][s%5],invalid=False,mutate=bool(s&8),returned=[0,-42,0x80000000,0xffffffff][s%4],connecting=[-26,0x80000000,7][s%3],result=[-42,0x80000000,0xffffffff][s%3],port=[0,1,32768,65535][s%4],ip=[0,1,0x7f000001,0xffffffff][s%4]) for s in range(256)]
        rows += [dict(state=s,mode=m,block=b,invalid=False,mutate=t,returned=0x80000000,connecting=-26,result=-42,port=65535,ip=0x89abcdef) for s,m,b,t in itertools.product([1,3,5,0x41,0x43,0x45],[0,1,4],[0,1,3],[False,True])]
        rows += [dict(state=3,mode=mode,block=1,invalid=False,mutate=False,returned=0,connecting=code,result=-42,port=1,ip=0x12345678) for mode,code in itertools.product([0,4],[7,0x80000000])]
        rows += [dict(rows[0],invalid=True,handle=0),dict(rows[0],invalid=True,handle=SOCKET)]
        rows += [dict(state=1,mode=0,block=1,invalid=False,mutate=False,returned=7,connecting=-26,result=-42,port=1,ip=0x12345678,volatileTransitions=[(at,value)]) for at,value in [(1,0),(2,4),(3,2),(4,0x42)]]
        return rows
    rows=[dict(state=s,mode=[0,1,2,3,4,255][s%6],cps=[0,4,7,255][s%4],invalid=False,mutate=bool(s&8),read=[-1,0,1,0x80000000][s%4],write=[-1,0,1,0x80000000][s//4%4]) for s in range(256)]
    rows += [dict(state=s,mode=m,cps=c,invalid=False,mutate=t,read=0,write=1) for s,m,c,t in itertools.product([0x8000,0x8001,0x8005,0xffff],[0,1,4],[0,4],[False,True])]
    rows += [dict(state=state,mode=mode,cps=cps,invalid=False,mutate=False,read=read,write=write) for state,mode,cps,(read,write) in itertools.product([1,3,5,7,0x41,0x43,0x45],[0,4],[0,4],[(-1,-1),(0,0),(1,1)])]
    rows += [dict(rows[0],invalid=True,handle=0),dict(rows[0],invalid=True,handle=SOCKET)]
    rows += [dict(state=5,mode=0,cps=0,invalid=False,mutate=False,read=0,write=0,volatileTransitions=[(at,value)]) for at,value in [(2,0),(3,0x8007),(4,2),(5,4)]]
    return rows


def scenario(name,f,ordinal):
    memory=Memory({SOCKET:128,RECEIVE:264,DATAGRAM:6,CONNECTING:4},ordinal);setv,getv=memory.set,memory.get
    setv(SOCKET+8,f.get('cps',4),1);setv(SOCKET+68,f.get('received',7));setv(SOCKET+100,RECEIVE if f.get('receive',True) else 0)
    setv(SOCKET+108,f.get('result',-42));setv(SOCKET+112,f.get('state',1),2);setv(SOCKET+114,f.get('block',1),1);setv(SOCKET+115,f['mode'],1)
    setv(RECEIVE+248,f.get('consumed',0));setv(RECEIVE+260,DATAGRAM if f.get('datagram',True) else 0);setv(DATAGRAM+4,f.get('size',17),2);setv(CONNECTING,f.get('connecting',-26))
    initial=memory.snapshot();actions=[];reads=0;events=f.get('volatileTransitions',[])
    def state():
        nonlocal reads
        for at,value in events:
            if at==reads:setv(SOCKET+112,value,2)
        reads+=1;return getv(SOCKET+112,2)
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=returned,checks=checks,mutations=changes));return returned
    def signed(value):return value if value<0x80000000 else value-(1<<32)
    handle=f.get('handle',SOCKET);arguments=[handle,f.get('port',0),f.get('ip',0),0x99aabbcc];result=0
    if name=='020901e4':
        if f['receive']:
            if f['mode']==1:result=f['size'] if f['datagram'] else 0
            elif f['mode'] in [0,4]:result=f['received']-f['consumed']
    else:
        changes=[]
        if f.get('mutate'):changes=[word(SOCKET+112,f['state']^0x40,2),word(SOCKET+115,4 if f['mode']==0 else 0,1),word(SOCKET+114,0 if f.get('block',1)==1 else 1,1)]
        call(0x02090294,[handle],int(f['invalid']),changes)
        if name=='0208eff0':
            if f['invalid'] or state()&8:result=-28
            elif handle==0 or not state()&1:result=-39
            elif getv(SOCKET+115,1) in [0,4]:
                if state()&4:result=-30 if getv(SOCKET+114,1)==1 else 0
                elif state()&2:result=signed(getv(SOCKET+108)) if state()&0x40 else signed(getv(CONNECTING))
                else:
                    setv(SOCKET+118,f['port'],2);setv(SOCKET+120,f['ip'])
                    call(0x0208f0a0,[SOCKET],f['returned']&0xffffffff,[word(SOCKET+114,3,1),word(SOCKET+112,0x8005,2)] if f['mutate'] else [])
                    result=f['returned'] if getv(SOCKET+114,1)==1 else -26
            else:setv(SOCKET+118,f['port'],2);setv(SOCKET+120,f['ip']);result=0
        elif f['invalid']:result=0x80
        else:
            if state()&0x40:result|=0x20
            if getv(SOCKET+115,1)==1 or state()&4:
                level=0x98760080^ordinal;call(0x02007ff4,[],level)
                call(0x020901e4,[SOCKET],f['read']&0xffffffff)
                if signed(f['read']&0xffffffff)>0:result|=1
                call(0x0208f900,[SOCKET],f['write']&0xffffffff)
                if signed(f['write']&0xffffffff)>0:result|=8
                call(0x02008008,[level],changes=[word(SOCKET+115,0,1),word(SOCKET+112,f['state'],2)] if f['mutate'] else [])
            if getv(SOCKET+115,1) in [0,4]:
                if state()&4 and getv(SOCKET+8,1)!=4 and not result&1:setv(SOCKET+112,state()&~6,2)
                if not state()&2 and not state()&4:result|=0x40
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result&0xffffffff,args=arguments,volatileReadEvents=events,volatileReads=reads)
