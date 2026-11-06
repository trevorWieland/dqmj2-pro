from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32
GP,S1,S2,ST=0x21d3028,0x2174000,0x2176000,0x217f000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
OBSERVED={s+off for s in [S1,S2]for off in [4,52,64,440]}
ARITY={0x20b90ec:1,0x209b14c:0,0x209b1d0:0,0x2006b7c:1,0x209b264:0,0x20b9100:1,0x209b0dc:2,0x209b12c:0,0x209b144:0,0x200708c:1,0x2007110:1,0x2090464:1,0x20b909c:2}


class AuditMemory(Memory):
    def __init__(self,regions):super().__init__(regions);self.observe=False;self.reads=[]
    def read(self,at,size):
        raw=super().read(at,size)
        if self.observe and at in OBSERVED:self.reads.append((at,size,int.from_bytes(raw,'little')))
        return raw


def dynamic_callbacks(v):return {}
def toggle(m):put(m,GP,S2 if word(m,GP)==S1 else S1)
def initial(address,v):
    m=AuditMemory({GP:bytes(4),S1:bytes([0x33])*8192,S2:bytes([0xcc])*8192,ST:bytes(64),SP-0x1000:bytes(0x1000)})
    put(m,GP,0 if v.get('nullState')else S1)
    for base in [S1,S2]:
        for off,val in [(0,7),(4,v.get('phaseWord',1)),(52,v.get('status',0)),(64,v.get('status',0)),(440,v.get('handle',7)),(2572,0xaabbccdd)]:put(m,base+off,val)
    return m,[v.get('callback',0x2232001)]if address==0x20b9068 else[]


def next_result(m,key,values):
    i=word(m,ST+key)
    if i>=len(values):raise ValueError('Outside finite supplied-provider script')
    put(m,ST+key,i+1);return values[i]


def effect(at,a,m,v):
    result=0x76543210
    if at in [0x209b14c,0x209b0dc]:
        result=v.get('start',1)
        if v.get('startSwitch'):toggle(m)
    elif at in [0x209b1d0,0x209b12c]:
        result=next_result(m,0,v.get('poll',[1,2,3]))
        if v.get('pollSwitch'):toggle(m)
    elif at==0x2006b7c:
        if v.get('sleepSwitch'):toggle(m)
        if v.get('sleepRequestsCancel'):put(m,word(m,GP)+4,2)
    elif at in [0x209b264,0x209b144]:
        if v.get('cancelSwitch'):toggle(m)
    elif at==0x20b90ec:put(m,word(m,GP),a[0])
    elif at==0x20b9100:
        put(m,ST+12,a[0]);put(m,word(m,GP)+52,5);put(m,word(m,GP)+64,5)
    elif at==0x200708c:
        if v.get('lockSwitch'):toggle(m)
    elif at==0x2007110:
        if v.get('unlockSwitch'):toggle(m)
    elif at==0x2090464:result=next_result(m,4,v.get('close',[0,0]))
    elif at==0x20b909c:put(m,ST+20,a[0]);put(m,ST+24,a[1])
    else:raise ValueError(('Outside supplied-provider namespace',hex(at)))
    return result&0xffffffff,a[:]


def evaluate(address,v):
    m,args=initial(address,v);calls=[];m.observe=True
    def call(at,a):
        m.observe=False;value,norm=effect(at,[x&0xffffffff for x in a],m,v);m.observe=True;calls.append((hex(at),norm));return value
    if address==0x20b9068:
        if word(m,GP):put(m,word(m,GP)+2572,args[0])
    elif address in [0x20b9364,0x20b9404]:
        off,phase,start,poll,cancel=(52,3,0x209b14c,0x209b1d0,0x209b264)if address==0x20b9364 else(64,4,0x209b0dc,0x209b12c,0x209b144)
        if word(m,word(m,GP)+4)==1 and word(m,word(m,GP)+off)==3:call(0x20b90ec,[phase])
        else:
            base=word(m,GP);a=[]if address==0x20b9364 else[base+56,base+68]
            if call(start,a):
                for count in range(16):
                    if word(m,word(m,GP)+off)==3 or word(m,word(m,GP)+off)==5 or word(m,word(m,GP)+off)==4:break
                    value=call(poll,[]);put(m,word(m,GP)+off,value);status=word(m,word(m,GP)+off)
                    if status in [1,2]:
                        call(0x2006b7c,[100])
                        if word(m,word(m,GP)+4)==2:call(cancel,[])
                    elif status in [0,3,4,5]:
                        if word(m,word(m,GP)+off)==3 and word(m,word(m,GP)+4)==1:call(0x20b90ec,[phase])
                        else:call(0x20b9100,[1]);word(m,word(m,GP)+off)
                else:raise ValueError('Outside finite poll model')
    elif address==0x20b95d8:
        handle=word(m,word(m,GP)+440);call(0x200708c,[word(m,GP)+444]);put(m,word(m,GP)+440,-59);call(0x2007110,[word(m,GP)+444])
        if s32(handle)>=0:
            if s32(call(0x2090464,[handle]))<0:call(0x20b909c,[5,-50])
            else:
                for count in range(16):
                    call(0x2006b7c,[100]);result=call(0x2090464,[handle])
                    if s32(result)!=-26:break
                else:raise ValueError('Outside finite close model')
                if result!=0:call(0x20b909c,[5,-50])
        call(0x20b90ec,[1])
    else:raise ValueError('Outside poll/close caller scope')
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'void',0,m.reads


def model(address,v):return evaluate(address,v)[:4]
def expected_reads(address,v):return evaluate(address,v)[4]
def cases(address):
    if address==0x20b9068:return [dict(nullState=n,callback=p)for n in [False,True]for p in [0,0x2232000,0x2232001,0xffffffff]]
    if address in [0x20b9364,0x20b9404]:
        rows=[dict(status=s,phaseWord=p,start=a)for s in [0,1,2,3,4,5,6,0xffffffff]for p in [0,1,2]for a in [0,1]]
        rows +=[dict(status=0,phaseWord=p,poll=[s,3])for p in [1,2]for s in [0,1,2,3,4,5,6,0xffffffff]]
        rows +=[dict(status=0,phaseWord=p,**flags)for p in [1,2]for flags in [{'startSwitch':True},{'pollSwitch':True},{'sleepSwitch':True},{'cancelSwitch':True},{'sleepRequestsCancel':True},{'sleepRequestsCancel':True,'cancelSwitch':True},{'pollSwitch':True,'sleepSwitch':True},{'startSwitch':True,'pollSwitch':True,'sleepSwitch':True,'sleepRequestsCancel':True,'cancelSwitch':True}]]
        return rows
    if address==0x20b95d8:return [dict(handle=h,close=script,**flags)for h in [0,7,0x7fffffff,0x80000000,0xffffffc5,0xffffffff]for script in [[-1],[0,0],[7,0],[0,-26,0],[0,-26,-26,0],[0,-1],[0,1]]for flags in [{},{'lockSwitch':True},{'unlockSwitch':True},{'lockSwitch':True,'unlockSwitch':True,'sleepSwitch':True}]]
    raise ValueError('No finite poll vectors')
