import struct
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
SP,STOP,MAGIC,DIV,RELIABLE=0x2701000,0x27e0000,0,0,0
P0,P1,INPUT,SOCKET,OPTION=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000
OPTION_SLOT=0x21d1b88
ULL=0x20260dc
ADDRESS_CALLBACK=0x20a3a4c
RET64={0x2007a9c,ULL}
OBSERVED=set()
ARITY={0x20a3d70:0,0x209bc88:0,0x20a2cc8:0,0x209f130:2,0x20a1608:1,0x2007a9c:0,0x20a3d7c:1,0x20a13d8:3,0x20b4540:1,0x20a16e4:1,0x20b45a0:1,ADDRESS_CALLBACK:4,0x20a19b4:1,0x20a1878:1,0x20a2394:0,0x20a21e0:1,0x20a277c:3,0x20a2c38:2,0x209bba0:1,0x20a00ac:6,0x20a1258:1,ULL:4}
MASK=(1<<64)-1
COVERED=[0,3,4,5,6,9,12,13,14,15,16,17,18,19,64,65,255]

def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def arity(at,values,m):return ARITY[at]
def byte(m,a):return m.read(a,1)[0]
def pbyte(m,a,v):m.write(a,bytes([v&255]))
def tickput(m,a,v):m.write(a,struct.pack('<Q',v&MASK))
def tickread(m,a):return int.from_bytes(m.read(a,8),'little')
def counter(m,key):
 if not hasattr(m,'counts'):m.counts={}
 n=m.counts.get(key,0);m.counts[key]=n+1;return n

def initial(address,v):
 m=Memory({P0:bytes((i*7+11)&255 for i in range(0x500)),P1:bytes(0x500),INPUT:bytes(260),SOCKET:struct.pack('<I',0x2176000),OPTION:bytes(32),OPTION_SLOT:bytes(4),SP-0x1000:bytes(4096)})
 for off,val in {4:SOCKET,0x20:v.get('reservation',321),0xe8:99,0x18c:0xabababab,0x190:0xcdcdcdcd,0x1a0:v.get('state',4),0x204:v.get('request',321),0x208:v.get('prior',0),0x20c:654}.items():put(m,P0+off,val)
 for off,val in {0xd:v.get('connections',2),0x15:v.get('matchType',0),0x17:v.get('reserved',1),0x1a4:v.get('progress',0),0x1a7:v.get('wait',0)}.items():pbyte(m,P0+off,val)
 for i in range(32):put(m,P0+0xf4+4*i,321+i)
 data=v.get('data',[0xc0000201,0x1234,31]);
 for i,x in enumerate(data):put(m,INPUT+4*i,x)
 if v.get('option'):
  put(m,OPTION_SLOT,OPTION);pbyte(m,OPTION,v.get('optionValid',1));put(m,OPTION+4,v.get('timeout',300));tickput(m,OPTION+16,v.get('start',0))
 return m,[v.get('command',255),v.get('sourcePID',321),0xc6336401,54321,INPUT,v.get('length',len(data))]

def effect(at,a,m,v):
 norm=a[:];result=0x76543210
 if at==0x20a3d70:result=0 if v.get('nullControl')else P0
 elif at==0x209bc88:result=v.get('dwcState',5)
 elif at==0x2007a9c:result=v.get('tick',0x100000001)&MASK
 elif at==ULL:
  assert a[2:]==[33514,0];result=(a[0]|a[1]<<32)//33514
 elif at==0x20b45a0:result=0x55
 elif at==ADDRESS_CALLBACK:norm+=[m.read(a[2]+2,6).hex()]
 elif at in [0x20a2cc8,0x209f130,0x20a3d7c,0x20b4540,0x20a19b4,0x20a2394,0x20a21e0,0x209bba0]:pass
 elif at in [0x20a1608,0x20a13d8]:result=v.get('result',0)
 elif at in [0x20a16e4,0x20a1878,0x20a277c]:result=v.get('cancelResult',1)
 elif at==0x20a2c38:
  aids=v.get('aids',[5]);result=aids[min(counter(m,'aid'),len(aids)-1)]
 elif at==0x20a00ac:
  assert 0<=a[5]<=1;norm+=[m.read(a[4],4*a[5]).hex()if a[5]else ''];result=v.get('result',0)
 elif at==0x20a1258:result=v.get('error',0)
 else:raise ValueError(('Uncovered command/provider remains unqualified',hex(at)))
 return result&(MASK if at in RET64 else 0xffffffff),norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=1;command,pid,ip,port,data,length=args
 if command not in COVERED:raise ValueError('Command is outside independent model subset')
 def call(at,a):
  value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
 def get():return call(0x20a3d70,[])
 active=bool(get())
 if active:active=word(m,get()+0x1a0)!=0
 if active:
  if call(0x209bc88,[])==5 and word(m,get()+0x1a0)==1 and pid==word(m,get()+0xf4):call(0x20a2cc8,[])
  if command==3:
   if word(m,get()+0x1a0)==4 and pid==word(m,get()+0x204):
    if length>0 and word(m,data)==16:call(0x209f130,[13,0]);result=0
    else:result=call(0x20a1608,[word(m,get()+0x204)])
  elif command==4:
   if word(m,get()+0x1a0)==4 and pid==word(m,get()+0x204):
    target=get();tickput(m,target+0x1cc,call(0x2007a9c,[]))
    if(word(m,get()+0x208)and byte(m,get()+0x1a7)<16)or byte(m,get()+0x15)==3:
     put(m,get()+0x1bc,1);target=get();tickput(m,target+0x1c0,call(0x2007a9c,[]))
     if byte(m,get()+0x15)!=3:target=get();pbyte(m,target+0x1a7,byte(m,target+0x1a7)+1)
    else:
     put(m,get()+0x208,0);pbyte(m,get()+0x1a7,0)
     if byte(m,get()+0x15)==0:call(0x20a3d7c,[3]);put(m,get()+0xe8,1);target=get();tickput(m,target+0xec,call(0x2007a9c,[]))
     elif byte(m,get()+0x15)==1:call(0x20a13d8,[1,0,0])
  elif command==5:
   if byte(m,get()+0x17)and pid==word(m,get()+0x20):
    if byte(m,get()+0x15)==2 and byte(m,get()+0xd)==1 and word(m,get()+0xf8)==pid:call(0x20b4540,[word(m,word(m,get()+4))])
    result=int(bool(call(0x20a16e4,[pid])))
  elif command==6:
   address=word(m,data);network=word(m,data+4)&65535;allowed=True
   if word(m,get()+0x1a0)==1:call(0x20a3d7c,[6])
   elif(word(m,get()+0x1a0)!=6 and word(m,get()+0x1a0)!=11)or pid!=word(m,get()+0x20):allowed=False
   if allowed:
    pbyte(m,get()+0x3cc,255);base=get();index=byte(m,get()+0xd)+1
    if word(m,base+0xf4+4*index)!=pid:base=get();index=byte(m,get()+0xd)+1;put(m,base+0xf4+4*index,pid)
    remote=SP-292;m.write(remote+2,network.to_bytes(2,'big'));put(m,remote+4,address);pbyte(m,get()+0x194,1);sock=call(0x20b45a0,[word(m,word(m,get()+4))]);info=get();call(ADDRESS_CALLBACK,[0,sock,remote,info+0x194]);tickput(m,get()+0x18c,0)
  elif command==9:
   if word(m,get()+0x1a0)==13:
    base=get();index=byte(m,get()+0x1a4)+1
    if word(m,base+0xf4+4*index)==word(m,data):target=get();pbyte(m,target+0x1a4,byte(m,target+0x1a4)+1);call(0x20a19b4,[0])
  elif command==12:
   if pid==word(m,get()+0xf4):
    if byte(m,get()+0x15)==0 or byte(m,get()+0x15)==1:result=int(bool(call(0x20a1878,[pid])))
    elif byte(m,get()+0x15)==3:put(m,get()+0x20c,pid);call(0x20a2394,[]);call(0x20a21e0,[0])
  elif command in [13,14,15]:result=int(bool(call(0x20a277c,[pid,command,word(m,data)])))
  elif command==16:
   if pid==word(m,get()+0xf4):
    for i in range(max(0,length)):
     aid=call(0x20a2c38,[word(m,data+4*i),0])
     if aid!=255:call(0x209bba0,[aid])
  elif command==17:
   answer=0
   if word(m,OPTION_SLOT)and byte(m,word(m,OPTION_SLOT)):
    tick=call(0x2007a9c,[]);elapsed=(((tick-tickread(m,word(m,OPTION_SLOT)+16))&MASK)*64)&MASK;elapsed=call(ULL,[elapsed&0xffffffff,elapsed>>32,33514,0]);answer=int(elapsed>=word(m,word(m,OPTION_SLOT)+4))
   payload=SP-280;put(m,payload,answer);r=call(0x20a00ac,[18,pid,ip,port,payload,1]);result=int(not call(0x20a1258,[r]))
  elif command==18:
   if word(m,get()+0x1a0)==19:
    aid=call(0x20a2c38,[pid,0])
    if aid!=255:
     p=word(m,OPTION_SLOT);put(m,p+8,word(m,p+8)|(1<<aid))
     if word(m,data):put(m,p+12,word(m,p+12)|(1<<aid))
  elif command==19:call(0x209f130,[12,0]);result=0
  elif command==64:
   i=1
   while i<=byte(m,get()+0xd):
    if word(m,get()+0xf4+4*i)==pid:
     r=call(0x20a00ac,[65,pid,ip,port,0,0]);result=int(not call(0x20a1258,[r]));break
    i+=1
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result

def ticks(ms):return(ms*33514+63)//64
def cases(address):
 base=[dict(command=c,state=0)for c in COVERED]+[dict(nullControl=True),dict(command=255,state=1),dict(command=0,state=1,sourcePID=999)]
 return base+[dict(command=3,state=s,sourcePID=p,length=n,data=[d],result=r)for s,p,n,d,r in [(4,321,1,16,1),(4,321,0,16,0),(4,321,1,0,-1),(4,999,1,16,1),(1,321,1,16,1)]]+[dict(command=4,state=4,matchType=t,prior=p,wait=w,tick=k)for t,p,w,k in [(0,1,15,MASK),(0,1,16,0),(0,0,0,0),(1,0,0,MASK),(2,0,0,0),(3,0,255,MASK)]]+[dict(command=5,matchType=t,reserved=z,reservation=r,connections=n,cancelResult=c)for t,z,r,n,c in [(0,0,321,2,1),(0,1,999,2,1),(1,1,321,2,0),(2,1,321,1,1),(3,1,321,2,1)]]+[dict(command=6,state=s,sourcePID=p,connections=n,data=[0xc0000201,port],reservation=321)for s,p,n,port in [(1,321,0,0),(6,321,2,0x1234),(11,321,30,0xffff),(6,999,2,0x1234),(4,321,2,0x80ff)]]+[dict(command=9,state=13,progress=p,data=[d])for p,d in [(0,322),(3,325),(0,999)]]+[dict(command=12,matchType=t,cancelResult=r,sourcePID=p)for t,r,p in [(0,1,321),(1,0,321),(2,1,321),(3,1,321),(0,1,999)]]+[dict(command=c,cancelResult=r,data=[0xffffffff])for c in [13,14,15]for r in [0,1]]+[dict(command=16,data=[100,200,300],length=n,aids=[5,255,31])for n in [-1,0,3]]+[dict(command=17,option=o,optionValid=v,timeout=300,tick=ticks(ms),error=e)for o,v,ms,e in [(False,0,300,0),(True,0,300,0),(True,1,299,0),(True,1,300,0),(True,1,301,1)]]+[dict(command=18,state=19,option=True,aids=[a],data=[d])for a,d in [(255,0),(0,0),(31,1)]]+[dict(command=19)]+[dict(command=64,sourcePID=p,connections=n,error=e)for p,n,e in [(322,2,0),(322,2,1),(999,2,0),(321,0,0)]]
