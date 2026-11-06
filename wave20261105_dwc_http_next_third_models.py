import base64
from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
from wave20261105_dwc_http_next_third_division import result as divresult
SRC,DST=0x2170000,0x2171000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
OBSERVED=set();ARITY={0x2026144:2,0x2026350:2,0x2008d78:3,0x2008e0c:3}
DIV_HELPERS={0x2026144,0x2026350};ALPHABET=b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-'
views=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/third/original-imports.json')['dataViews'];DATA={}
for at,v in views.items():DATA[int(at,0)]=bytes.fromhex(v['expectedHex']);DATA[int(v['pointeeAddress'],0)]=bytes.fromhex(v['pointeeExpectedHex'])
def dynamic_callbacks(v):return {}
def remainder(at,a):return divresult(at,a[0],a[1])[1]
def payload(v):return bytes.fromhex(v['inputHex'])
def encoded(raw):return base64.b64encode(raw).translate(bytes.maketrans(b'+/=',b'.-*'))
def decoded(raw):
    needed=sum(x!=42 for x in raw)*6//8
    values={b:i for i,b in enumerate(ALPHABET)};bits=''.join(format(values.get(x,0),'06b')for x in raw);count=max(1,needed)if raw else 0
    return bytes(int(bits[i*8:i*8+8],2)for i in range(count)),needed

def initial(address,v):
    raw=payload(v);m=Memory({**DATA,SRC:bytes([0xcc])*256,DST:bytes([0xa5])*256,SP-0x1000:bytes(0x1000)});m.write(SRC,raw);v['_address']=address
    return m,[0 if v.get('nullSource')else SRC,len(raw),0 if v.get('query')else DST,v.get('capacity',256)]
def effect(at,a,m,v):
    norm=a[:]
    if at in DIV_HELPERS:r,_=divresult(at,a[0],a[1])
    elif at==0x2008d78:m.write(a[0],bytes([a[1]&255])*a[2]);r=0x76543210
    elif at==0x2008e0c:raw=m.read(a[0],a[2]);m.write(a[1],raw);norm=a+[raw.hex()];r=0x76543210
    else:raise ValueError(('Outside custom base64 support',hex(at)))
    return r&0xffffffff,norm

def evaluate(address,v):
    m,args=initial(address,v);calls=[];raw=payload(v);result=0
    def call(at,a):
        r,n=effect(at,a,m,v);calls.append((hex(at),n));return r
    if address==0x209a738:
        call(0x2026350,[len(raw),3]);call(0x2026350,[len(raw),3]);out=encoded(raw);result=len(out)
        if not args[2]:pass
        elif args[3]<len(out):result=0xffffffff
        else:
            for i in range(0,len(raw),3):
                remaining=len(raw)-i;call(0x2026144,[remaining*8,6]);call(0x2026144,[remaining*8,6]);scratch=SP-28;call(0x2008d78,[scratch,0,3]);call(0x2008e0c,[SRC+i,scratch,min(remaining,3)]);m.write(DST+i//3*4,out[i//3*4:i//3*4+4])
    elif address==0x209a83c:
        if len(raw)%4:result=0xffffffff
        else:
            out,needed=decoded(raw);result=needed
            if not args[2]:pass
            elif args[3]<needed:result=0xffffffff
            else:m.write(DST,out);result=len(out)
    else:raise ValueError('Outside admitted custom base64 pair')
    return {at:bytes(value)for at,value in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result

def model(address,v):return evaluate(address,v)
def expected_reads(address,v):return []
def cases(address):
    rows=[]
    if address==0x209a738:
        inputs={bytes((i*17+3)&255 for i in range(n))for n in range(34)}|{bytes([b])*n for b in [0,127,128,255]for n in [1,2,3,4,7]}
        for raw in sorted(inputs):
            need=len(encoded(raw));rows.extend(dict(inputHex=raw.hex(),capacity=cap,query=query)for cap in sorted({0,max(0,need-1),need,need+1})for query in [False,True])
        rows +=[dict(inputHex=bytes(range(n)).hex(),capacity=0,query=True,nullSource=True)for n in [0,1,2,3,7,33]]
    elif address==0x209a83c:
        inputs={encoded(bytes((i*7+1)&255 for i in range(n)))for n in range(25)}|{b'A',b'AA',b'AAA',b'****',b'*A**',b'AAA*',b'AA**',b'....',b'----',bytes([128,255,42,45]),b'A***A***'}
        for raw in sorted(inputs):
            need=sum(x!=42 for x in raw)*6//8;rows.extend(dict(inputHex=raw.hex(),capacity=cap,query=query)for cap in sorted({0,max(0,need-1),need,need+1})for query in [False,True])
    else:raise ValueError('No codec vectors')
    return rows
