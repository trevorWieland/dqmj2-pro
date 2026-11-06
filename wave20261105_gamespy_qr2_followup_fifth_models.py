from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_gamespy_qr2_next_eighteenth_models import s32

GP1,GP2=0x21d3020,0x21d3028
C1,C2,S1,S2,R,P,ST,ALERT=0x2170000,0x2171000,0x2174000,0x2176000,0x217a000,0x217b000,0x217c000,0x217d000
IME,SP,STOP,MAGIC,DIV=0x4000208,0x2701000,0x27e0000,0,0
OBSERVED={IME}
ARITY={0x2006e24:3,0x2006c70:0,0x20068c0:1,0x200698c:1,0x2006ca4:0,0x209afe8:0,0x20b9998:0,0x209b6e4:0,0x209a930:1,0x20903d0:3,0x2090350:3,0x20b909c:2,0x2008d78:3}
WORDS={0x20b8780,0x20b9d2c,0x20b9128,0x20b91a0}


def dynamic_callbacks(v):return {}
def half(m,a):return int.from_bytes(m.read(a,2),'little')
def ph(m,a,value):m.write(a,(value&65535).to_bytes(2,'little'))
def thread_group(v):return(GP1,C1,C2)if v['_address']==0x20b87a8 else(GP2,S1,S2)
def toggle(m,gp,a,b):put(m,gp,b if word(m,gp)==a else a)
def thread_switch(m,v,key):
    if v.get(key):toggle(m,*thread_group(v))


def initial(address,v):
    m=Memory({GP1:bytes(4),GP2:bytes(4),C1:bytes([0xa5])*4096,C2:bytes([0x5a])*4096,S1:bytes([0x33])*8192,S2:bytes([0xcc])*8192,R:bytes([0x77])*40,P:bytes([0x99])*1088,ST:bytes(16),ALERT:bytes(16),IME:bytes(2),SP-0x1000:bytes(0x1000)})
    put(m,GP1,0 if v.get('nullControl')else C1);put(m,GP2,0 if v.get('nullState')else S1);put(m,S1+440,v.get('fd',7));put(m,S2+440,v.get('alternateFd',0x80000001));ph(m,IME,v.get('ime',1));put(m,P,v.get('length',12));put(m,P+4,0x44535359);put(m,P+8,0x89abcdef);v['_address']=address
    if address==0x20b8780:return m,[0 if v.get('nullResult')else R]
    if address in [0x20b9128,0x20b91a0]:return m,[P]
    return m,[]


def wire(v):
    raw=bytearray((i*13+7)&255 for i in range(1044));raw[:4]=(v.get('length',12)&0xffffffff).to_bytes(4,'little');raw[4:8]=(0x44535359 if v.get('magic',True)else 0x11223344).to_bytes(4,'little');raw[8:12]=(v.get('code',0x89abcdef)&0xffffffff).to_bytes(4,'little');return bytes(raw)


def effect(at,a,m,v):
    result=0x76543210;norm=a[:]
    if at==0x2006e24:
        norm=a+[m.read(a[1],40).hex()if a[1]else None];result=v.get('sendResult',1)
        if v.get('messageSwitch'):toggle(m,GP1,C1,C2)
    elif at in [0x2006c70,0x20068c0,0x200698c,0x2006ca4]:
        key={0x2006c70:'disable',0x20068c0:'check',0x200698c:'join',0x2006ca4:'enable'}[at];thread_switch(m,v,key+'Switch')
        if key+'Ime'in v:ph(m,IME,v[key+'Ime'])
        if at==0x20068c0:result=v.get('terminated',0)
    elif at==0x209afe8:put(m,ALERT+12,0x55);result=v.get('status',0)
    elif at==0x20b9998:put(m,ST+12,word(m,ST+12)+1)
    elif at==0x209b6e4:put(m,ALERT+12,0x66)
    elif at==0x209a930:put(m,a[0],v.get('output',0x80000001));norm=['private-output',v.get('output',0x80000001)];result=v.get('status',0)
    elif at==0x20b909c:put(m,ALERT,a[0]);put(m,ALERT+4,a[1]);put(m,ALERT+8,word(m,ALERT+8)+1)
    elif at==0x2008d78:m.write(a[0],bytes([a[1]&255])*a[2])
    elif at==0x20903d0:
        index=word(m,ST);put(m,ST,index+1);seq=v.get('writes',['rest']);value=seq[index]if index<len(seq)else'rest';result=a[2]if value=='rest'else min(value,a[2])if value>0 else value;norm=a+[m.read(a[1],a[2]).hex(),result&0xffffffff]
        if v.get('ioSwitch'):toggle(m,GP2,S1,S2)
    elif at==0x2090350:
        index=word(m,ST+4);put(m,ST+4,index+1);seq=v.get('reads',['rest']);value=seq[index]if index<len(seq)else'rest';position=word(m,ST+8);available=1044-position;result=min(a[2],available)if value=='rest'else min(value,a[2],available)if value>0 else value;raw=b''
        if result>0:raw=wire(v)[position:position+result];m.write(a[1],raw);put(m,ST+8,position+result)
        norm=a+[result&0xffffffff,raw.hex()]
        if v.get('ioSwitch'):toggle(m,GP2,S1,S2)
    else:raise ValueError(('Unqualified transport/lifecycle provider',hex(at)))
    return result&0xffffffff,norm


def evaluate(address,v):
    m,args=initial(address,v);calls=[];reads=[];result=0
    def call(at,a):
        value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
    def ime_read():
        value=half(m,IME);reads.append((IME,2,value));return value
    if address==0x20b8780:
        if args[0]:
            for offset in [28,32,36]:put(m,args[0]+offset,0)
        if word(m,GP1):result=call(0x2006e24,[word(m,GP1),args[0],0])
    elif address in [0x20b87a8,0x20b9270]:
        gp,base,alt=thread_group(v);offset=52 if address==0x20b87a8 else 2576;previous=ime_read();ph(m,IME,0);call(0x2006c70,[])
        if not call(0x20068c0,[word(m,gp)+offset]):call(0x200698c,[word(m,gp)+offset])
        call(0x2006ca4,[]);ime_read();ph(m,IME,previous)
    elif address==0x20b9d2c:
        result=call(0x209afe8,[])
        if not result:call(0x20b9998,[])
    elif address==0x20b9d40:
        call(0x209b6e4,[])
        if not call(0x209a930,[SP-8]):call(0x20b9998,[])
    elif address==0x20b9128:
        if not word(m,GP2):result=-28
        else:
            length=word(m,P);sent=0;cursor=P
            if length>1044:call(0x20b909c,[6,-50]);result=-35
            else:
                while sent<length:
                    result=call(0x20903d0,[word(m,word(m,GP2)+440),cursor,length-sent]);signed=s32(result)
                    if signed>0:sent+=signed;cursor+=signed;result=sent
                    elif signed<0:call(0x20b909c,[6,-50]);break
    elif address==0x20b91a0:
        if not word(m,GP2):result=-28
        else:
            call(0x2008d78,[P,0,1044]);received=0;cursor=P;failed=False
            while received<4:
                step=s32(call(0x2090350,[word(m,word(m,GP2)+440),cursor,4-received]))
                if step>0:received+=step;cursor+=step
                else:
                    if received>0 or step!=0:call(0x20b909c,[6,-50])
                    result=received;failed=True;break
            if not failed:
                length=word(m,P)
                if length>1044:call(0x20b909c,[6,-50]);result=-35
                else:
                    while received<length:
                        step=s32(call(0x2090350,[word(m,word(m,GP2)+440),cursor,length-received]))
                        if step>0:received+=step;cursor+=step
                        else:call(0x20b909c,[6,-50]);result=received;failed=True;break
                    if not failed:
                        if received<12 or word(m,P+4)!=0x44535359:call(0x20b909c,[6,-40]);result=0
                        else:result=received
    else:raise ValueError('Outside transport/lifecycle subset')
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word'if address in WORDS else'void',result&0xffffffff,reads


def model(address,v):return evaluate(address,v)[:4]
def expected_reads(address,v):return evaluate(address,v)[4]


def cases(address):
    if address==0x20b8780:return [dict(nullControl=n,nullResult=r,sendResult=s,messageSwitch=change)for n in [False,True]for r in [False,True]for s in [0,1,0x80000000]for change in [False,True]]
    if address in [0x20b87a8,0x20b9270]:
        return [dict(ime=ime,terminated=t,**flags)for ime in [0,1,0x1234,0xffff]for t in [0,1,0xffffffff]for flags in [{},{'disableSwitch':True},{'checkSwitch':True},{'joinSwitch':True},{'disableIme':2,'checkIme':3,'joinIme':4,'enableIme':0xfffd}]]
    if address==0x20b9d2c:return [dict(status=s)for s in [0,1,0x80000000,0xffffffff]]
    if address==0x20b9d40:return [dict(status=s,output=o)for s in [0,1,0x80000000,0xffffffff]for o in [0,0x80000000,0xffffffff]]
    if address==0x20b9128:
        rows=[dict(nullState=n,length=length,writes=seq)for n in [False,True]for length in [0,4,12,1044,1045,0xffffffff]for seq in [['rest'],[0,'rest'],[1,2,'rest'],[-1],[1,-7]]]
        return rows+[dict(length=length,writes=seq,ioSwitch=True,fd=0xffffffff)for length in [12,1044]for seq in [['rest'],[0,'rest'],[1,2,'rest'],[1,-7]]]
    if address==0x20b91a0:
        rows=[dict(nullState=n,length=length,magic=magic,reads=seq)for n in [False,True]for length in [0,4,8,11,12,16,1044,1045,0xffffffff]for magic in [False,True]for seq in [['rest'],[1,1,1,1,'rest'],[0],[-1],[1,0],[1,-7],[4,1,0],[4,-3]]]
        return rows+[dict(length=length,reads=seq,ioSwitch=True,fd=0xffffffff)for length in [12,1044]for seq in [['rest'],[1,1,1,1,'rest'],[4,1,0]]]
    raise ValueError('No transport/lifecycle vectors')
