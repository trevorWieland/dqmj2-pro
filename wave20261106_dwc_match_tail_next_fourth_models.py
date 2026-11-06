import struct
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
P0,P1,INPUT,REF,SOCKET=0x2170000,0x2171000,0x2172000,0x2173000,0x2173100
OBSERVED=set()
ARITY={0x20a3d70:0,0x20a2b44:1,0x20a2394:0,0x20a21e0:1,0x20a3d7c:1,0x209fc38:1,0x20a304c:1,0x20a1278:2,0x20a1258:1,0x209bdc4:2,0x20b4528:1,0x209f47c:2,0x20a00ac:6,0x2007a9c:0,0x20b4540:1,0x20b748c:1,0x20b6c90:1,0x20a2290:0,0x20a13d8:3,0x20a233c:1,0x20a2724:2}
MASK=(1<<64)-1

def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def arity(at,values,m):return ARITY[at]
def byte(m,a):return m.read(a,1)[0]
def pbyte(m,a,v):m.write(a,bytes([v&255]))
def tickput(m,a,v):m.write(a,struct.pack('<Q',v&MASK))
def count(m,key):
 if not hasattr(m,'counts'):m.counts={}
 n=m.counts.get(key,0);m.counts[key]=n+1;return n

def initial(address,v):
 m=Memory({P0:bytes((i*7+11)&255 for i in range(0x500)),P1:bytes(0x500),INPUT:bytes(128),REF:bytes(4),SOCKET:bytes(4),SP-0x1000:bytes(4096)})
 for off,value in {4:SOCKET,0x10:0x2176000,0x20:v.get('reservation',123),0xe8:99,0x19c:v.get('cookie',0),0x1a0:v.get('state',4),0x200:123,0x204:0x76543210,0x208:v.get('prior',0),0x20c:654,0x348:v.get('backupCount',2)}.items():put(m,P0+off,value)
 pbyte(m,P0+0xd,v.get('connections',2));pbyte(m,P0+0x15,v.get('matchType',0));pbyte(m,P0+0x17,v.get('reserved',0));pbyte(m,P0+0x1a6,v.get('distant',0));put(m,REF,0x2176100);put(m,SOCKET,0x2176200)
 for i in range(32):put(m,P0+0xf4+i*4,1000+i);put(m,INPUT+i*4,[0,123,0xffffffff][i%3])
 for i in range(1,33):put(m,P0+0x348+4*i,0x11000000+i)
 if address==0x20a1edc:args=[INPUT,v.get('length',3)]
 elif address in [0x20a16e4,0x20a233c]:args=[321]
 elif address==0x20a2724:args=[321,v.get('command',13)]
 else:args=[]
 return m,args

def effect(at,a,m,v):
 norm=a[:];result=0x76543210
 def supplied(key,default):
  seq=v.get(key,[default]);return seq[min(count(m,key),len(seq)-1)]
 if at==0x20a3d70:result=P0
 elif at==0x20a2b44:result=supplied('buddy',1)
 elif at in [0x20a2394,0x20a21e0,0x20a3d7c,0x20b4528,0x20b4540,0x20b748c,0x20b6c90,0x20a2290]:pass
 elif at in [0x209fc38,0x20a1278,0x209f47c,0x20a13d8]:result=v.get('result',0)
 elif at in [0x20a304c,0x20a1258]:result=v.get('error',0)
 elif at==0x209bdc4:result=REF if v.get('hasConnection',True)else 0
 elif at==0x20a00ac:
  if not 0<=a[5]<=32:raise ValueError('Outside bounded backup command word count')
  norm+=[m.read(a[4],a[5]*4).hex()if a[5]else ''];result=supplied('sendResults',v.get('result',0))
 elif at==0x2007a9c:result=v.get('tick',0x100000001)&MASK
 elif at==0x20a233c:result=v.get('closeResult',1)
 elif at==0x20a2724:result=supplied('cancelResults',1)
 else:raise ValueError(('Outside recovery provider boundary',hex(at)))
 return result&(MASK if at==0x2007a9c else 0xffffffff),norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0;contract='ARM R0 word'
 def call(at,a):
  value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
 def get():return call(0x20a3d70,[])
 if address==0x20a1edc:
  result=1
  if byte(m,get()+0x1a6)and word(m,get()+0x1a0)==4:pass
  else:
   for i in range(args[1]):
    if not call(0x20a2b44,[word(m,INPUT+i*4)]):result=0;break
    if byte(m,get()+0x1a6)and word(m,get()+0x1a0)==1:break
 elif address==0x20a2290:
  contract='void'
  if byte(m,get()+0x15)!=2 and byte(m,get()+0x15)!=3:call(0x20a2394,[]);call(0x20a21e0,[1])
 elif address==0x20a22b4:
  pbyte(m,get()+0x17,0);put(m,get()+0x20,0);pbyte(m,get()+0x1a8,0)
  if word(m,get()+0x208):
   if byte(m,get()+0x15)==0:
    call(0x20a3d7c,[3]);r=call(0x209fc38,[0])
    if call(0x20a304c,[r]):result=r
   elif byte(m,get()+0x15)==1:
    call(0x20a3d7c,[4]);r=call(0x20a1278,[word(m,get()+0x208),0])
    if call(0x20a1258,[r]):result=r
  else:call(0x20a21e0,[1])
 elif address==0x20a233c:
  put(m,get()+0x20c,args[0]);conn=call(0x209bdc4,[args[0],byte(m,get()+0xd)+1])
  if conn:pbyte(m,get()+0x1a8,2);call(0x20b4528,[word(m,conn)]);pbyte(m,get()+0x1a8,0);result=1
  else:call(0x209f47c,[args[0],byte(m,get()+0xd)+1])
 elif address==0x20a2724:
  payload=SP-16;length=0
  if args[1]==13:put(m,payload,word(m,get()+0x20c));length=1
  r=call(0x20a00ac,[args[1],args[0],0,0,payload,length])
  if not call(0x20a1258,[r]):target=get();tickput(m,target+0x1e8,call(0x2007a9c,[]));result=1
 elif address==0x20a1908:
  i=1
  while i<=byte(m,get()+0xd):
   data=get();length=get();ip=get();port=get();pid=get();r=call(0x20a00ac,[10,word(m,pid+0xf4+4*i),word(m,ip+0x24+4*i),int.from_bytes(m.read(port+0xa4+2*i,2),'little'),data+0x348,(word(m,length+0x348)+1)&0xffffffff])
   if r:result=r;break
   i+=1
  else:
   pbyte(m,get()+0x17,0);put(m,get()+0x20,0);pbyte(m,get()+0x1a8,1);call(0x20b4540,[word(m,word(m,get()+4))]);pbyte(m,get()+0x1a8,0)
 elif address==0x20a16e4:
  isserver=not(byte(m,get()+0x17)and word(m,get()+0x20)==word(m,get()+0x200))
  if isserver:pbyte(m,get()+0x17,0);put(m,get()+0x20,0);call(0x20b748c,[word(m,get()+0x10)])
  if byte(m,get()+0xd)<31:target=get();put(m,target+0xf4+4*(byte(m,get()+0xd)+1),0)
  pbyte(m,get()+0x3cc,255)
  if word(m,get()+0x19c):call(0x20b6c90,[word(m,get()+0x19c)]);put(m,get()+0x19c,0)
  target=get();pbyte(m,target+0x14,byte(m,get()+0xd));put(m,get()+0x204,0);result=1
  if not isserver:
   if byte(m,get()+0x15)!=3:call(0x20a2290,[])
  elif byte(m,get()+0x15)==0:call(0x20a3d7c,[3]);put(m,get()+0xe8,2);target=get();tickput(m,target+0xec,call(0x2007a9c,[]))
  elif byte(m,get()+0x15)==1:call(0x20a3d7c,[4]);call(0x20a13d8,[1,0,0])
  elif byte(m,get()+0x15)==2:
   call(0x20a3d7c,[14]);put(m,get()+0x1d8,0);m.write(get()+0x1b2,bytes(2));call(0x20a233c,[args[0]]);i=1
   while i<=byte(m,get()+0xd):
    if not call(0x20a2724,[word(m,get()+0xf4+4*i),13]):result=0;break
    i+=1
   else:
    if byte(m,get()+0xd)==0:call(0x20a21e0,[2])
 else:raise ValueError(hex(address))
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result

def cases(address):
 if address==0x20a1edc:return[dict(distant=d,state=s,length=n,buddy=b)for d,s in [(0,4),(1,4),(1,1),(1,11)]for n in [0,1,3]for b in [[1],[0],[1,0]]]
 if address==0x20a2290:return[dict(matchType=t)for t in [0,1,2,3,255]]
 if address==0x20a22b4:return[dict(matchType=t,prior=p,error=e,result=r)for t in [0,1,2,3]for p in [0,123]for e,r in [(0,0),(0,7),(1,7),(-1,-1)]]
 if address==0x20a233c:return[dict(hasConnection=b,connections=n)for b in [False,True]for n in [0,1,31]]
 if address==0x20a2724:return[dict(command=c,error=e,result=r,tick=t)for c in [13,14,15,255]for e,r,t in [(0,0,0),(0,7,MASK),(1,7,123),(-1,-1,123)]]
 if address==0x20a1908:return[dict(connections=n,sendResults=r,backupCount=c)for n in [0,1,3,31]for r in [[0],[7],[0,9]]for c in [0,2,31]]
 if address==0x20a16e4:return[dict(matchType=t,reserved=z,reservation=p,connections=n,cookie=k,cancelResults=r,tick=tick)for t,z,p,n,k,r,tick in [(t,z,p,n,k,r,0x100000001)for t in [0,1,2,3]for z,p in [(0,123),(1,123),(1,999)]for n,k,r in [(0,0,[1]),(1,7,[1]),(3,7,[1,0]),(31,0,[1])]]]
 raise ValueError(hex(address))
