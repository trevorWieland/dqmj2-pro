import re,struct
from project import ROOT
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
DATA,ERR,TEXT,TABLE,TEMPLATE=0x21d1990,0x20ec9b0,0x2170000,0x20df1cc,0x20df1fc
ARITY={0x201d69c:1,0x200f540:2,0x200fc74:2,0x201d6b8:2,0x201f274:1,0x201d800:2}
OBSERVED={ERR}
IMAGE=(ROOT/'extract/arm9/arm9.bin').read_bytes()
MONTHS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
POINTERS=list(struct.unpack('<12I',IMAGE[TABLE-0x2000000:TABLE-0x2000000+48]))

def dynamic_callbacks(v):return {}
def cstring(m,a):
 out=bytearray()
 while len(out)<128:
  b=m.read(a+len(out),1)
  if b==bytes([0]):return bytes(out)
  out.extend(b)
 raise ValueError('Unterminated bounded fixture string')

def initial(address,v):
 assert address==0x2099bf8
 text=v.get('text','Fri, 03 Mar 2006 01:28:13 GMT').encode()+bytes([0]);assert len(text)<=64
 regions={DATA:bytes((i*13+7)&255 for i in range(20)),ERR:struct.pack('<I',v.get('initialErrno',34)),TEXT:text+bytes(64-len(text)),SP-0x1000:bytes(4096),TABLE:IMAGE[TABLE-0x2000000:TABLE-0x2000000+48],TEMPLATE:IMAGE[TEMPLATE-0x2000000:TEMPLATE-0x2000000+30]}
 for p in POINTERS:regions[p]=IMAGE[p-0x2000000:p-0x2000000+4]
 return Memory(regions),[TEXT]

def count(m,name):
 if not hasattr(m,'counts'):m.counts={}
 value=m.counts.get(name,0);m.counts[name]=value+1;return value

def effect(at,a,m,v):
 result=0x76543210;norm=a[:]
 if at==0x201d69c:result=len(cstring(m,a[0]));norm+=[cstring(m,a[0]).hex()]
 elif at==0x200f540:
  m.write(a[0],struct.pack('<4I',*v.get('currentDate',[26,11,6,5])));m.write(a[1],struct.pack('<3I',*v.get('currentTime',[12,34,56])));result=v.get('getResult',0)
 elif at==0x200fc74:
  index=count(m,'convert');result=v.get('current',0x100000001)if index==0 else v.get('remote',0x100000000)
  norm+=[list(struct.unpack('<4I',m.read(a[0],16))),list(struct.unpack('<3I',m.read(a[1],12)))];result&=(1<<64)-1
 elif at==0x201d6b8:
  raw=cstring(m,a[1])+bytes([0]);m.write(a[0],raw);result=a[0];norm+=[raw.hex()]
 elif at==0x201f274:
  index=count(m,'atoi');raw=cstring(m,a[0]);match=re.match(rb'\s*([+-]?\d+)',raw);result=int(match[1])if match else 0
  if not -(1<<31)<=result<(1<<31):raise ValueError('atoi overflow is outside qualified fixture domain')
  put(m,ERR,34 if index==v.get('errnoIndex',-1)else v.get('atoiErrno',0));norm+=[raw.hex()]
 elif at==0x201d800:
  left,right=cstring(m,a[0]),cstring(m,a[1]);result=(left>right)-(left<right);norm+=[left.hex(),right.hex()]
 else:raise ValueError(('Outside date provider boundary',hex(at)))
 return result&((1<<64)-1 if at==0x200fc74 else 0xffffffff),norm

def oracle(v):
 m,args=initial(0x2099bf8,v);calls=[];reads=[];text=cstring(m,TEXT);result=0;dateAt,clockAt,buffer=SP-36,SP-48,SP-80
 def call(at,a):
  value,norm=effect(at,a,m,v);calls.append((hex(at),norm));return value
 length=call(0x201d69c,[TEXT]);expected=call(0x201d69c,[TEMPLATE])
 valid=length==expected and all(text[i]==ord(c)for i,c in [(7,' '),(11,' '),(16,' '),(19,':'),(22,':'),(25,' ')])
 if valid and call(0x200f540,[dateAt,clockAt])==0:
  current=call(0x200fc74,[dateAt,clockAt])
  if current!=(1<<64)-1:
   call(0x201d6b8,[buffer,TEXT]);split=bytearray(text+bytes([0]))
   for i in [7,11,16,19,22,25]:split[i]=0
   m.write(buffer,split);put(m,ERR,0);year=call(0x201f274,[buffer+12]);put(m,dateAt,year);error=word(m,ERR);reads.append((ERR,4,error))
   if error!=34:
    put(m,dateAt,(year-2000)&0xffffffff);put(m,dateAt+4,13)
    for i,pointer in enumerate(POINTERS):
     if call(0x201d800,[pointer,buffer+8])==0:put(m,dateAt+4,i+1);break
    if word(m,dateAt+4)<=12:
     success=True
     for offset,destination in [(5,dateAt+8),(17,clockAt),(20,clockAt+4),(23,clockAt+8)]:
      put(m,ERR,0);value=call(0x201f274,[buffer+offset]);put(m,destination,value);error=word(m,ERR);reads.append((ERR,4,error))
      if error==34:success=False;break
     if success:
      remote=call(0x200fc74,[dateAt,clockAt])
      if remote!=(1<<64)-1:
       m.write(DATA+12,struct.pack('<Q',(current-remote)&((1<<64)-1)));m.write(DATA+4,struct.pack('<Q',current));put(m,DATA,1);result=1
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,result,reads

def model(address,v):
 expected,calls,result,reads=oracle(v);return expected,calls,'ARM R0 word',result
def expected_reads(address,v):return oracle(v)[3]

def cases(address):
 normal='Fri, 03 Mar 2006 01:28:13 GMT';out=[]
 for month in MONTHS+['xxx']:
  for year in [1999,2000,2006,2099]:out.append(dict(text=normal[:8]+month+normal[11:12]+str(year)+normal[16:]))
 out+=[dict(text=normal[:i]+replacement+normal[i+1:])for i in [7,11,16,19,22,25]for replacement in ['x',':',' ']]
 out+=[dict(text=text)for text in ['',normal[:-1],normal+'x','xxx'+normal[3:],normal.replace('2006','abcd'),normal.replace('03','-1',1),normal.replace('01:28:13','99:99:99')]]
 out+=[dict(errnoIndex=i,initialErrno=initial)for i in range(5)for initial in [0,34,0xffffffff]]
 out+=[dict(getResult=r)for r in [-1,1,2,0xffffffff]]
 out+=[dict(current=c,remote=r)for c in [-2,-1,0,1,0xffffffff,0x100000000,0x100000001,0x7fffffff00000000]for r in [-2,-1,0,1,0xffffffff,0x100000000,0x100000001]if -(1<<63)<=c-r<(1<<63)]
 return out
