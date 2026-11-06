from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
GP,C,C2,A,A2,E,D=0x21d3020,0x2170000,0x2171000,0x2174000,0x2174100,0x2176000,0x2179000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
OBSERVED=set();ARITY={0x2008e0c:3}
def dynamic_callbacks(v):return {}
def initial(address,v):
    assert address==0x20b88fc
    m=Memory({GP:bytes(4),C:bytes(2292),C2:bytes(2292),A:bytes(40),A2:bytes(40),E:bytes((i*17+3)&255 for i in range(276)),D:bytes([0xa5])*8192,SP-0x1000:bytes(0x1000)})
    put(m,GP,C)
    for c,a in [(C,A),(C2,A2)]:
        put(m,c+36,a)
        for off,value in [(12,0 if v.get('nullBuffer')else D),(20,v.get('capacity',32)),(24,v.get('offset',0)),(32,0x77777777),(36,0x88888888)]:put(m,a+off,value)
    for off,value in [(0,20+v.get('length',8)),(8,v.get('code',207)),(12,v.get('continuation',0)),(16,v.get('length',8))]:put(m,E+off,value)
    return m,[E]
def effect(at,a,m,v):
    if at!=0x2008e0c:raise ValueError('Outside original copy boundary')
    if a[2]>256:raise ValueError('Outside bounded copy span')
    raw=m.read(a[0],a[2]);m.write(a[1],raw)
    if v.get('copySwitch'):put(m,GP,C2)
    if v.get('copyChangesContinuation'):put(m,E+12,1)
    return 0x76543210,a+[raw.hex()]
def evaluate(address,v):
    m,args=initial(address,v);calls=[];result=1
    def active():return word(m,word(m,GP)+36)
    if word(m,E+8)==207:
        length=word(m,E+16);offset=word(m,active()+24);capacity=word(m,active()+20);buffer=word(m,active()+12)
        if capacity<((offset+length)&0xffffffff):length=(capacity-offset)&0xffffffff
        if buffer:
            _,norm=effect(0x2008e0c,[E+20,(buffer+offset)&0xffffffff,length],m,v);calls.append(('0x2008e0c',norm))
        total=(offset+length)&0xffffffff;put(m,active()+24,total)
        if word(m,E+12)==0:put(m,active()+36,total);put(m,active()+32,1)
        else:result=0
    return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result
def model(address,v):return evaluate(address,v)
def expected_reads(address,v):return []
def cases(address):
    rows=[dict(capacity=c,offset=o,length=n,nullBuffer=b,continuation=k)for c in [0,1,8,32,64]for o in [0,1,8,32]if o<=c for n in [0,1,8,32]for b in [False,True]for k in [0,1]]
    rows +=[dict(code=c,continuation=k)for c in [0,201,202,206,208,0xffffffff]for k in [0,1]]
    rows +=[dict(offset=o,capacity=c,length=n,nullBuffer=True,continuation=k)for o,c,n in [(0xfffffff0,32,32),(0xffffffff,0,1),(32,8,0),(32,8,32)]for k in [0,1]]
    rows +=[dict(capacity=32,offset=8,length=8,**flags)for flags in [{'copySwitch':True},{'copyChangesContinuation':True},{'copySwitch':True,'copyChangesContinuation':True}]]
    return rows
