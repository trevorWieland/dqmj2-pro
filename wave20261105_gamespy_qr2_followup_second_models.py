from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32

GP,Q,A,R,RA,E,V,ST,TABLE=0x21d3020,0x2170000,0x2170100,0x2171000,0x2171100,0x2172000,0x2173000,0x2174000,0x20e277c
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
ARM_CB,THUMB_CB=0x2230000,0x2230004
ARITY={0x2006ff8:3,0x2006eb8:3,0x20b8d44:1,0x20b8da0:0,0x20b9030:0,0x20b9068:1,0x2006b7c:1,0x20b8fd8:0,ARM_CB:1,THUMB_CB:1}
HANDLERS={1:0x20b88d0,2:0x20b8958,3:0x20b89b4,4:0x20b8b0c,5:0x20b8ab0,6:0x20b8b5c,7:0x20b8bc4,8:0x20b8c2c,9:0x20b8c7c}
ARITY.update({a:0 for a in [0x20b8878,0x20b88a8,*HANDLERS.values()]})


def dynamic_callbacks(v):return {ARM_CB:dict(mode='arm'),THUMB_CB:dict(mode='thumb')}
def callback(v):return [0,ARM_CB,THUMB_CB|1][v.get('callback',0)]
def control(m):return word(m,GP)
def active(m):return word(m,control(m)+36)
def switch(m,v,key):
    if v.get(key):put(m,GP,A)


def initial(address,v):
    m=Memory({GP:bytes(4),Q:bytes([0xa5])*64,A:bytes([0x5a])*64,R:bytes([0x33])*40,RA:bytes([0xcc])*40,E:bytes([0x66])*20,V:bytes(16),ST:bytes(16),TABLE:bytes([0x99])*1088,SP-0x1000:bytes(0x1000)})
    put(m,GP,0 if v.get('nullControl')else Q)
    for q,r in [(Q,R),(A,RA)]:
        put(m,q+36,r if v.get('active',True)else 0);put(m,q+40,callback(v));put(m,q+44,v.get('completion',0))
    for r in [R,RA]:put(m,r+12,V)
    put(m,V,v.get('value',0x12345678));put(m,E,v.get('eventWord',v.get('n',12)));put(m,E+8,v.get('code',201));put(m,E+12,v.get('value',0x12345678))
    v['_address']=address
    if address==0x20b85d8:return m,[v['key'],v['pointer']]
    if address==0x20b8d14:return m,[v['n'],E]
    if address==0x20b8d44:return m,[callback(v)]
    if address in [0x20b8dd8,0x20b8dfc]:return m,[E]
    if address==0x20b87e4:return m,[v.get('threadArgument',0xdeadbeef)]
    return m,[]


def effect(at,args,m,v):
    a=args;result=0x76543210;norm=a[:];address=v['_address']
    if at==0x2006ff8:
        put(m,a[1],R if v.get('active',True)else 0);switch(m,v,'receiveSwitch')
    elif at==0x2006eb8:
        put(m,a[1],0x11223344);norm=[a[0],'private-output',a[2]];switch(m,v,'receiveSwitch')
    elif at==0x20b8d44:
        result=v.get('setup',1);switch(m,v,'setupSwitch')
    elif at==0x20b9030:
        result=v.get('gate',1);switch(m,v,'gateSwitch')
    elif at==0x20b9068:switch(m,v,'registerSwitch')
    elif at in [ARM_CB,THUMB_CB]:
        if a!=[E]:raise ValueError('Measured one-word callback event boundary differs')
        result=v.get('callbackResult',0);switch(m,v,'callbackSwitch')
    elif at==0x2006b7c:
        count=word(m,ST+4)+1;put(m,ST+4,count)
        if address==0x20b8d80 and count>=v.get('loops',1):
            if v.get('nullEscape'):put(m,GP,0)
            else:put(m,control(m)+44,v.get('afterCompletion',1))
    elif at==0x20b8878:
        index=word(m,ST);commands=v.get('commands',[]);put(m,ST,index+1)
        put(m,control(m)+36,R if index<len(commands)else 0)
        if index<len(commands):put(m,R,commands[index])
    elif at==0x20b88a8:
        if active(m):put(m,active(m)+28,1)
        put(m,control(m)+36,0)
    elif at==0x20b8fd8:result=word(m,ST+4)>=v.get('loops',0)
    elif at in HANDLERS.values():
        if address!=0x20b87e4:raise ValueError('Handler supplied outside isolated dispatcher fixture')
    elif at==0x20b8da0:pass
    else:raise ValueError(('Unqualified control caller helper',hex(at)))
    return result&0xffffffff,norm


def model(address,v):
    m,args=initial(address,v);calls=[];result=0;contract='void'
    def call(at,a):
        value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
    if address==0x20b85d8:
        if 50<=s32(v['key'])<=254:put(m,TABLE+v['key']*4,v['pointer'])
    elif address==0x20b8878:
        call(0x2006ff8,[control(m),control(m)+36,1])
        if active(m):
            for off in [28,32,36]:put(m,active(m)+off,0)
    elif address==0x20b88a8:
        call(0x2006eb8,[control(m),SP-8,0])
        if active(m):put(m,active(m)+28,1);put(m,control(m)+36,0)
    elif address==0x20b88d0:
        if call(0x20b8d44,[0]):put(m,active(m)+36,word(m,word(m,active(m)+12)));put(m,active(m)+32,1)
        call(0x20b8da0,[])
    elif address==0x20b8d14:
        value=1;n=v['n']&0xffffffff
        if s32(n)>=0 and n>=12 and word(m,E)==n and word(m,control(m)+40):value=call(word(m,control(m)+40)&~1,[E])
        put(m,control(m)+44,value)
    elif address==0x20b8d44:
        contract='ARM R0 word'
        if control(m)and call(0x20b9030,[]):
            put(m,control(m)+44,0);put(m,control(m)+40,callback(v));call(0x20b9068,[0x20b8d15]);result=1
    elif address==0x20b8d80:
        while control(m)and word(m,control(m)+44)==0:call(0x2006b7c,[100])
    elif address==0x20b8da0:
        if control(m):call(0x20b9068,[0]);put(m,control(m)+40,0);put(m,control(m)+44,1)
    elif address in [0x20b8dd8,0x20b8dfc]:
        contract='ARM R0 word';result=1;code=word(m,E+8);value=word(m,E+12)
        if code==201:put(m,active(m)+36,value);put(m,active(m)+32,1)
        elif address==0x20b8dfc and code==202 and value in [2,3]:put(m,active(m)+36,0);put(m,active(m)+32,1)
    elif address==0x20b87e4:
        if control(m):
            while True:
                call(0x20b8878,[])
                if not active(m):call(0x20b88a8,[]);break
                command=word(m,active(m))
                if command in HANDLERS:call(HANDLERS[command],[])
                call(0x20b88a8,[])
            while not call(0x20b8fd8,[]):call(0x2006b7c,[100])
    else:raise ValueError('Outside frozen control caller subset')
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result


def cases(address):
    if address==0x20b85d8:return [dict(key=n,pointer=p)for n in [-1,0,49,50,51,253,254,255,0x80000000,0x7fffffff]for p in [0,0x2173000,0xffffffff]]
    if address in [0x20b8878,0x20b88a8]:return [dict(active=active,receiveSwitch=sw)for active in [False,True]for sw in [False,True]]
    if address==0x20b88d0:return [dict(setup=r,setupSwitch=sw,value=value)for r in [0,1,0xffffffff]for sw in [False,True]for value in [0,0x80000001,0xffffffff]]
    if address==0x20b8d14:return [dict(n=n,eventWord=n if match else n^1,callback=cb,callbackResult=r,callbackSwitch=sw)for n in [-1,0,11,12,127,0x7fffffff,0x80000000]for match in [False,True]for cb in [0,1,2]for r in [0,1,0xffffffff]for sw in [False,True]]
    if address==0x20b8d44:return [dict(nullControl=null,gate=gate,callback=cb,gateSwitch=gs,registerSwitch=rs)for null in [False,True]for gate in [0,1,0xffffffff]for cb in [0,1,2]for gs,rs in [(False,False),(True,False),(False,True)]]
    if address==0x20b8d80:return [dict(nullControl=null,completion=value,loops=loops,nullEscape=escape,afterCompletion=0x80000001)for null in [False,True]for value in [0,1,0xffffffff]for loops in [1,3]for escape in [False,True]]
    if address==0x20b8da0:return [dict(nullControl=null,callback=cb,registerSwitch=sw)for null in [False,True]for cb in [0,1,2]for sw in [False,True]]
    if address in [0x20b8dd8,0x20b8dfc]:return [dict(code=c,value=v)for c in [0,200,201,202,203,0xffffffff]for v in [0,1,2,3,4,0xffffffff]]
    if address==0x20b87e4:return [dict(nullControl=null,commands=commands,loops=loops)for null in [False,True]for commands in [[],[1],[0,*range(1,10),10,0xffffffff],[9,8,1]]for loops in [0,1,3]]
    raise ValueError('No control subset vectors')
