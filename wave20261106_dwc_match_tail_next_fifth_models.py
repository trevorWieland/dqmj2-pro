import struct
from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
P0,P1,INPUT,OUTPUT,SOCKET=0x2170000,0x2171000,0x2172000,0x2174000,0x2175000
RELIABLE=0x20a3f84
OBSERVED=set()
ARITY={0x20a0330:3,0x201f114:3,0x20a039c:6,0x20a3d70:0,0x20a16e4:1,0x209f4bc:2,0x20061ac:4,0x209b26c:4,0x209b294:4,0x209d1c8:3,0x20a3d7c:1,0x20a249c:2,0x20a2c80:1,0x20a19b4:1,RELIABLE:4,0x2007a9c:0,0x209bc88:0,0x209f130:2,0x20b6c90:1,0x20b4540:1,0x20a22b4:0,0x20a21e0:1}
VIEWS=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/fifth/original-imports.json')['dataViews']
STRINGS={bytes.fromhex(v['expectedHex'])[:-1]:int(a,0)for a,v in VIEWS.items()}
MASK=(1<<64)-1

def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def arity(at,values,m):return ARITY[at]
def byte(m,a):return m.read(a,1)[0]
def half(m,a):return int.from_bytes(m.read(a,2),'little')
def pbyte(m,a,v):m.write(a,bytes([v&255]))
def phalf(m,a,v):m.write(a,struct.pack('<H',v&65535))
def tickput(m,a,v):m.write(a,struct.pack('<Q',v&MASK))
def cstring(m,a):
 out=bytearray()
 while len(out)<4096:
  b=m.read(a+len(out),1)
  if b==bytes([0]):return bytes(out)
  out.extend(b)
 raise ValueError('Unterminated bounded provided string')

def initial(address,v):
 m=Memory({P0:bytes((i*7+11)&255 for i in range(0x500)),P1:bytes(0x500),INPUT:bytes(4096),OUTPUT:bytes(64),SOCKET:struct.pack('<I',0x2176100),SP-0x1000:bytes(4096)})
 for a,view in VIEWS.items():m.regions[int(a,0)]=bytearray.fromhex(view['expectedHex'])
 for off,value in {4:SOCKET,0x19c:v.get('cookie',0),0x1a0:v.get('state',1),0x1d4:v.get('ackBits',0),0x200:v.get('profile',123),0x208:v.get('prior',0),0x20c:654}.items():put(m,P0+off,value)
 pbyte(m,P0+0xd,v.get('connections',2));pbyte(m,P0+0x15,v.get('matchType',1));pbyte(m,P0+0x16,v.get('entries',3));pbyte(m,P0+0x1a8,v.get('closeState',0));pbyte(m,P0+0x1a9,v.get('cancelState',0));phalf(m,P0+0x1b0,v.get('latency',0x1234))
 for i in range(32):put(m,P0+0xf4+4*i,1000+i);pbyte(m,P0+0x2d0+i,i+4)
 if address==0x209f0c4:
  tokens=v.get('tokens',['1','2','4294967295']);payload='/'.join(tokens).encode();raw=bytes([v.get('command',128)])+payload+bytes([0]);assert len(raw)<=4096;m.write(INPUT,raw);args=[0x2176200,v.get('profileArg',321),INPUT]
 elif address==0x209f460:args=[321]
 elif address==0x209f47c:args=[v.get('profileArg',1001),v.get('length',3)]
 elif address==0x209f1e8:m.write(INPUT,bytes([v.get('first',1),v.get('index',1),v.get('wireAid',31),0xa5]));args=[v.get('aid',5),v.get('type',2),INPUT]
 elif address==0x20a249c:args=[v.get('aid',5),v.get('type',2)]
 elif address==0x209f334:args=[v.get('error',0),v.get('errorCode',123),321]
 else:args=[]
 return m,args

def wire_prefix_length(v):
 if v.get('type',2)==3:return 2
 if v.get('type',2)==2:return 3 if 1<=v.get('aid',5)-4<=v.get('connections',2)else 1
 return 0

def effect(at,a,m,v):
 norm=a[:];result=0x76543210
 if at==0x20a3d70:result=0 if v.get('nullControl')else P0
 elif at==0x20a0330:
  tokens=cstring(m,a[1]).split(b'/');index=a[2]
  if index>=len(tokens)or not tokens[index]:result=0xffffffff
  else:
   assert len(tokens[index])<=15;m.write(a[0],tokens[index]+bytes([0]));result=len(tokens[index])
 elif at==0x201f114:
  raw=cstring(m,a[0]);assert a[1:]==[0,10];result=min(int(raw),0xffffffff);norm+=[raw.hex()]
 elif at==0x20a039c:
  assert a[5]<=128;norm+=[m.read(a[4],a[5]*4).hex()];result=v.get('result',0)
 elif at in [0x20a16e4,0x209f4bc,0x20a3d7c,0x20a249c,0x20a19b4,0x209f130,0x20b6c90,0x20b4540,0x20a22b4,0x20a21e0]:pass
 elif at==0x20061ac:
  assert a[1]==12 and cstring(m,a[2])==b'%u';text=str(a[3]).encode();m.write(a[0],text+bytes([0]));result=len(text);norm+=[b'%u'.hex()]
 elif at in [0x209b26c,0x209b294]:
  key,val=cstring(m,a[0]),cstring(m,a[1]);norm+=[key.hex(),val.hex()];text=(b''if at==0x209b26c else cstring(m,a[2]))+key+b'='+val+b';';assert len(text)<32;m.write(a[2],text+bytes([0]));result=len(text)
 elif at==0x209d1c8:norm+=[cstring(m,a[1]).hex()];result=v.get('result',0)
 elif at==0x20a2c80:result=v.get('wantedMask',0x20)
 elif at==RELIABLE:
  assert a[3]==4;n=wire_prefix_length(v);norm+=[n,m.read(a[2],n).hex()];result=v.get('result',0)
 elif at==0x2007a9c:result=v.get('tick',0x100000001)&MASK
 elif at==0x209bc88:result=v.get('dwcState',5)
 else:raise ValueError(('Outside receive/handshake provider boundary',hex(at)))
 return result&(MASK if at==0x2007a9c else 0xffffffff),norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0;contract='void'
 def call(at,a):
  value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
 def get():return call(0x20a3d70,[])
 if address==0x209f0c4:
  tmp,data=SP-548,SP-532;i=0
  while i<128:
   if call(0x20a0330,[tmp,INPUT+1,i])==0xffffffff:break
   put(m,data+4*i,call(0x201f114,[tmp,0,10]));i+=1
  call(0x20a039c,[byte(m,INPUT),args[1],0,0,data,i])
 elif address==0x209f460:
  if byte(m,get()+0x1a8)!=2:call(0x20a16e4,args)
 elif address==0x209f47c:
  contract='ARM R0 word'
  if get():
   for i in range(args[1]):
    if word(m,get()+0xf4+4*i)==(args[0]&0xffffffff):call(0x209f4bc,[i,args[1]]);result=1;break
 elif address==0x209f724:
  contract='ARM R0 word'
  if byte(m,get()+0x15)==2:
   value,key=SP-16,SP-48;call(0x20061ac,[value,12,STRINGS[b'%u'],byte(m,get()+0x16)+1]);call(0x209b26c,[STRINGS[b'SCM'],value,key,47]);call(0x20061ac,[value,12,STRINGS[b'%u'],byte(m,get()+0xd)+1]);call(0x209b294,[STRINGS[b'SCN'],value,key,47]);call(0x20061ac,[value,12,STRINGS[b'%u'],3]);call(0x209b294,[STRINGS[b'VER'],value,key,47]);result=call(0x209d1c8,[6,key,0])
 elif address==0x20a249c:
  aid,kind=args;packet=SP-24
  if kind==2:
   target=get();pbyte(m,packet,int(aid==byte(m,target+0x2d0+byte(m,get()+0xd))));i=1
   while i<=byte(m,get()+0xd):
    if aid==byte(m,get()+0x2d0+i):pbyte(m,packet+1,i);pbyte(m,packet+2,aid);break
    i+=1
  elif kind==3:pbyte(m,packet,half(m,get()+0x1b0));pbyte(m,packet+1,half(m,get()+0x1b0)>>8)
  call(RELIABLE,[kind,aid,packet,4]);target=get();tickput(m,target+0x1e0,call(0x2007a9c,[]))
 elif address==0x209f1e8:
  aid,kind,data=args
  if kind==2:
   if word(m,get()+0x1a0)==1:
    if byte(m,data)==1:put(m,get()+0x20c,0)
    index=byte(m,data+1);pbyte(m,get()+0x2d0+index,byte(m,data+2));target=get();put(m,target+0xf4+4*index,word(m,get()+0x200))
    if byte(m,get()+0x15)==0 or byte(m,get()+0x15)==1:target=get();pbyte(m,target+0x16,byte(m,get()+0xd))
    pbyte(m,get()+0x1ad,0);call(0x20a3d7c,[9])
   call(0x20a249c,[aid,3])
  elif kind==3:
   if word(m,get()+0x1a0)==16:
    target=get();put(m,target+0x1d4,word(m,target+0x1d4)|(1<<aid))
    latency=byte(m,data)|(byte(m,data+1)<<8)
    if latency>half(m,get()+0x1b0):phalf(m,get()+0x1b0,latency)
    wanted=call(0x20a2c80,[0])
    if word(m,get()+0x1d4)==wanted:
     i=1
     while i<=byte(m,get()+0xd):call(0x20a249c,[byte(m,get()+0x2d0+i),4]);i+=1
     call(0x20a3d7c,[17])
   else:call(0x20a249c,[aid,4])
  elif kind==4:
   if word(m,get()+0x1a0)==9:call(0x20a19b4,[4])
 elif address==0x209f334:
  contract='ARM R0 word'
  if call(0x209bc88,[])!=5:pass
  elif byte(m,get()+0x15)==2:result=1
  elif args[0]:call(0x209f130,[args[0],args[1]-80000]);result=1
  else:
   pbyte(m,get()+0x2d0,0);result=1
   if byte(m,get()+0x1a9)==1 or byte(m,get()+0x1a8)==1 or byte(m,get()+0x1a8)==2:pass
   else:
    if word(m,get()+0x19c):call(0x20b6c90,[word(m,get()+0x19c)]);put(m,get()+0x19c,0)
    if byte(m,get()+0xd):
     if byte(m,get()+0x1a8)==0:pbyte(m,get()+0x1a8,3);call(0x20b4540,[word(m,word(m,get()+4))])
    elif byte(m,get()+0x15)==3:call(0x209f130,[6,-80430])
    elif word(m,get()+0x208):call(0x20a22b4,[])
    elif word(m,get()+0x1a0)==1:call(0x20a3d7c,[18]);target=get();tickput(m,target+0x1f0,call(0x2007a9c,[]))
    else:call(0x20a21e0,[1])
 else:raise ValueError(hex(address))
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result

def cases(address):
 if address==0x209f0c4:return[dict(tokens=x,command=c,profileArg=p)for x in [[],['0'],['1','2'],['1',''],['4294967295'],['4294967296'],['000001']*128]for c,p in [(0,0),(128,-1),(255,321)]]
 if address==0x209f460:return[dict(closeState=x)for x in [0,1,2,3,255]]
 if address==0x209f47c:return[dict(nullControl=z,length=n,profileArg=p)for z,n,p in [(True,3,1001),(False,0,1000),(False,-1,1000),(False,3,1000),(False,3,1002),(False,31,1030),(False,32,-1)]]
 if address==0x209f724:return[dict(matchType=t,connections=n,entries=e,result=r)for t in [0,1,2,3]for n,e,r in [(0,0,0),(31,31,7),(255,255,-1)]]
 if address==0x20a249c:return[dict(type=t,aid=a,connections=n,latency=l,tick=k)for t,a,n,l,k in [(t,a,n,l,0x100000001)for t in [2,3,4]for a,n in [(5,2),(6,2),(0,0)]for l in [0,0x1234,65535]]]
 if address==0x209f1e8:return[dict(type=t,state=s,matchType=m,connections=n,index=i,first=f,aid=a,ackBits=b,wantedMask=w,latency=l)for t,s,m,n,i,f,a,b,w,l in [(2,s,m,n,i,f,5,0,0,0)for s,m,n,i,f in [(1,0,2,1,1),(1,1,31,31,0),(1,2,0,0,1),(0,0,2,1,1)]]+[(3,s,1,n,1,1,a,b,w,l)for s in [0,16]for n,a,b,w,l in [(0,0,0,1,65535),(2,5,0,32,0),(3,31,1,0x80000001,1),(1,5,0,0,65535)]]+[(4,s,1,2,1,1,5,0,0,0)for s in [0,9,16]]+[(255,1,1,2,1,1,5,0,0,0)]]
 if address==0x209f334:return[dict(dwcState=d,matchType=t,error=e,connections=n,closeState=c,cancelState=z,cookie=k,prior=p,state=s,tick=tick)for d,t,e,n,c,z,k,p,s,tick in [(4,0,0,2,0,0,0,0,1,0),(5,2,6,2,0,0,0,0,1,0)]+[(5,t,0,n,c,z,k,p,s,0xffffffffffffffff)for t in [0,1,3]for n,c,z,k,p,s in [(2,0,0,7,0,1),(2,3,0,0,0,1),(2,1,0,7,0,1),(2,2,0,7,0,1),(2,0,1,7,0,1),(0,0,0,7,123,1),(0,0,0,0,0,1),(0,0,0,0,0,4)]]+[(5,1,6,2,0,0,7,0,1,0)]]
 raise ValueError(hex(address))
