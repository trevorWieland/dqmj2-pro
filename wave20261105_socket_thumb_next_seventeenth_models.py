import itertools
from wave20261105_socket_thumb_next_memory import Memory
KERNEL=0x020e33e4
CONFIG=0x021d1550
THREADS=[0x02401000,0x02401200]
SOCS=[0x02402000,0x02402200]
SP=0x027f0000
STOP=0x027e0000
SPECS={'0208fb2c':16}


def signed(value):return value if value<0x80000000 else value-0x100000000


def fixtures(name):
    return [dict(hasSoc=s,window=w,mss=m,config=c,length=n,mutate=bool(i%5==0)) for i,(s,w,m,c,n) in enumerate(itertools.product([False,True],[0,1,512,65535],[0,1,512,65535],[0,1,128,65535],[0x80000000,0xffffffff,0,1,255,0x7fffffff]))]


def scenario(name,f,ordinal):
    memory=Memory({KERNEL:8,CONFIG:40,**{p:168 for p in THREADS},**{p:48 for p in SOCS}},ordinal);get,setv=memory.get,memory.set
    setv(KERNEL+4,THREADS[0]);setv(THREADS[0]+164,SOCS[0] if f['hasSoc'] else 0);setv(THREADS[1]+164,SOCS[1]);setv(CONFIG+36,f['config'])
    for p in SOCS:setv(p+44,f['window'],2);setv(p+46,f['mss'],2)
    initial=memory.snapshot();actions=[]
    def word(at,value,size=4):return at,int(value&((1<<(size*8))-1)).to_bytes(size,'little')
    def call(address,args,returned=0x89abcdef,changes=None):
        checks=list(memory.snapshot().items());changes=changes or []
        for at,raw in changes:memory.put(at,raw)
        actions.append(dict(address=address,args=[v&0xffffffff for v in args],returned=[v&0xffffffff for v in returned] if isinstance(returned,list) else returned&0xffffffff,checks=checks,mutations=changes))
    arguments=[f['length'],0x11223344,0x55667788,0x99aabbcc];soc=get(get(KERNEL+4)+164);mask=(ordinal*0x1010101^0xa5a5a5a5)&0xffffffff
    changes=[word(KERNEL+4,THREADS[1]),word(THREADS[0]+164,SOCS[1]),word(SOCS[0]+44,65535 if f['window']==0 else 1,2),word(SOCS[0]+46,65535 if f['mss']==0 else 1,2),word(CONFIG+36,f['config']^0x55)] if f['mutate'] else []
    call(0x02007ff4,[],mask,changes)
    temp=2*min(get(soc+46,2),get(soc+44,2),signed(get(CONFIG+36))) if soc and get(soc+46,2)>0 and get(soc+44,2)>0 else 2*signed(get(CONFIG+36))
    call(0x02008008,[mask],changes=[word(CONFIG+36,0),word(SOCS[0]+44,0,2),word(SOCS[0]+46,0,2)] if f['mutate'] else [])
    result=f['length']
    if temp>0:
        length=signed(f['length']);quotient=abs(length)//temp*(-1 if length<0 else 1);remainder=length-quotient*temp
        call(0x02026144,[f['length'],temp],[quotient,remainder])
        if quotient>0:result=temp*quotient
    return dict(initial=initial,regions=memory.snapshot(),actions=actions,result=result&0xffffffff,args=arguments,allowedWrites=[])
