import struct
from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
SP,STOP,MAGIC,DIV,RELIABLE=0x2701000,0x27e0000,0,0,0
P0,P1,INPUT,FRIENDS,USER=0x2170000,0x2171000,0x2172000,0x2178000,0x2179000
ULL=0x20260dc
RET64={0x2007a9c,ULL}
OBSERVED=set()
ARITY={0x20a3d70:0,0x2007a9c:0,0x20a3d7c:1,0x209fc38:1,0x20a304c:1,0x20a13d8:3,0x20a1258:1,0x209f130:2,0x209c5fc:0,0x20972f4:2,0x20971ac:1,0x20aa4f0:3,0x20aa3e0:3,0x209b2bc:4,0x201f114:3,0x20a1278:2,ULL:4,0x209bc88:0,0x20a1878:1,0x20a249c:2,0x20a2394:0,0x20a21e0:1,0x20a23bc:1,0x20a16e4:1,0x20a19b4:1,0x20a233c:1,0x20a2724:2,0x20a2c38:2,0x20a2c80:1}
VIEWS=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/sixth/original-imports.json')['dataViews']
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
def tickread(m,a):return int.from_bytes(m.read(a,8),'little')
def cstring(m,a):
 out=bytearray()
 while len(out)<1024:
  b=m.read(a+len(out),1)
  if b==bytes([0]):return bytes(out)
  out.extend(b)
 raise ValueError('Unterminated bounded friend field')
def counter(m,key):
 if not hasattr(m,'counts'):m.counts={}
 n=m.counts.get(key,0);m.counts[key]=n+1;return n

def initial(address,v):
 m=Memory({P0:bytes((i*7+11)&255 for i in range(0x500)),P1:bytes(0x500),INPUT:bytes(128),FRIENDS:bytes(768),USER:bytes(64),SP-0x1000:bytes(4096)})
 for a,x in VIEWS.items():m.regions[int(a,0)]=bytearray.fromhex(x['expectedHex'])
 for off,val in {0:0x2176000,0x1a0:v.get('state',9),0x1d4:v.get('ackBits',0),0x1d8:v.get('cancelBits',0),0x204:0xabcdef01,0x208:0x11111111,0x20c:654,0x2fc:FRIENDS,0x300:v.get('friendLength',3),0x344:v.get('friendLength',3)}.items():put(m,P0+off,val)
 for off,val in {0xd:v.get('connections',2),0x15:v.get('matchType',0),0x16:v.get('entries',4),0x1a5:v.get('friendCount',0),0x1a7:9,0x1ab:v.get('resends',0),0x1ad:v.get('waitCount',0)}.items():pbyte(m,P0+off,val)
 phalf(m,P0+0x1b0,v.get('latency',300));phalf(m,P0+0x1b2,v.get('cancelLatency',300));tickput(m,P0+0x1e0,v.get('lastTick',0));tickput(m,P0+0x1e8,v.get('lastTick',0))
 for i in range(32):put(m,P0+0xf4+4*i,1000+i);pbyte(m,P0+0x2d0+i,[0,5,31,7][i%4])
 for i in range(64):pbyte(m,P0+0x304+i,i)
 if address==0x20a1608:args=[321]
 elif address==0x20a13d8:args=[v.get('delay',0),v.get('init',0),v.get('resendPID',0)]
 elif address==0x20a277c:args=[321,v.get('command',13),v.get('data',777)]
 else:args=[]
 return m,args

def effect(at,a,m,v):
 norm=a[:];result=0x76543210
 if at==0x20a3d70:result=P0
 elif at==0x2007a9c:result=v.get('tick',0x100000001)&MASK
 elif at==ULL:
  numerator=a[0]|a[1]<<32;denominator=a[2]|a[3]<<32
  assert denominator==33514;result=numerator//denominator
 elif at in [0x20a3d7c,0x209f130,0x20a249c,0x20a2394,0x20a21e0,0x20a19b4]:pass
 elif at in [0x209fc38,0x20a13d8,0x20a1278]:result=v.get('result',0)
 elif at in [0x20a304c,0x20a1258]:result=v.get('error',0)
 elif at==0x209c5fc:result=USER
 elif at==0x20972f4:
  index=(a[1]-FRIENDS)//12;assert a[0]==USER and 0<=index<64;profiles=v.get('profiles',[2000,2001,2002]);result=profiles[index%len(profiles)]
 elif at==0x20971ac:result=v.get('valid',1)
 elif at==0x20aa4f0:put(m,a[2],a[1]);result=v.get('buddyError',0)
 elif at==0x20aa3e0:
  raw=bytearray(532);struct.pack_into('<ii',raw,0,a[1],v.get('buddyState',4));raw[8:16]=b'fixture\0';m.write(a[2],bytes(raw));result=v.get('statusError',0)
 elif at==0x209b2bc:
  key=cstring(m,a[0]);values={b'VER':v.get('version','3'),b'FME':v.get('number',str(v.get('entries',4))),b'MDF':v.get('distant','1')};text=values[key].encode();assert len(text)<{b'VER':12,b'FME':4,b'MDF':2}[key];m.write(a[1],text+bytes([0]));norm+=[key.hex(),cstring(m,a[2]).hex()];result=len(text)if text else 0xffffffff
 elif at==0x201f114:raw=cstring(m,a[0]);assert a[1:]==[0,10];norm+=[raw.hex()];result=int(raw)
 elif at in [0x20a1878,0x20a23bc,0x20a16e4,0x20a233c]:result=v.get('cancelResult',1)
 elif at==0x20a2724:
  seq=v.get('cancelResults',[1]);result=seq[min(counter(m,'cancel'),len(seq)-1)]
 elif at==0x20a2c38:result=v.get('aid',5)
 elif at==0x20a2c80:result=v.get('wantedMask',32)
 elif at==0x209bc88:result=v.get('dwcState',5)
 else:raise ValueError(('Outside friend/time caller provider boundary',hex(at)))
 return result&(MASK if at in RET64 else 0xffffffff),norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=1
 def call(at,a):
  value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
 def get():return call(0x20a3d70,[])
 def millis(t,last):
  n=(((t-last)&MASK)*64)&MASK;return call(ULL,[n&0xffffffff,n>>32,33514,0])
 if address==0x20a1608:
  put(m,get()+0x208,0);put(m,get()+0x204,0);pbyte(m,get()+0x1a7,0);target=get();tickput(m,target+0x1cc,call(0x2007a9c,[]))
  if byte(m,get()+0x15)==0:call(0x20a3d7c,[3]);r=call(0x209fc38,[0]);result=int(not call(0x20a304c,[r]))
  elif byte(m,get()+0x15)==1:r=call(0x20a13d8,[0,0,args[0]]);result=int(not call(0x20a1258,[r]))
  elif byte(m,get()+0x15)==3:call(0x209f130,[6,-80410]);result=0
 elif address==0x20a13d8:
  delay,init,resend=args
  if init:start=byte(m,get()+0x1a5)
  else:start=byte(m,get()+0x1a5)+1 if byte(m,get()+0x1a5)<word(m,get()+0x344)-1 else 0
  finished=0
  for turn in range(66):
   if not init or finished:
    target=get();pbyte(m,target+0x1a5,byte(m,target+0x1a5)+1)
    if byte(m,get()+0x1a5)>=word(m,get()+0x344):pbyte(m,get()+0x1a5,0)
   if finished and byte(m,get()+0x1a5)==start:
    put(m,get()+0x1c8,3000);target=get();tickput(m,target+0x1cc,call(0x2007a9c,[]));put(m,get()+0x1bc,0);result=0;break
   finished=1;user=call(0x209c5fc,[]);base=get();index=get();count=get();friend=word(m,base+0x2fc)+12*byte(m,index+0x304+byte(m,count+0x1a5));profile=call(0x20972f4,[user,friend])
   if profile in [0,0xffffffff]:continue
   base=get();index=get();count=get();friend=word(m,base+0x2fc)+12*byte(m,index+0x304+byte(m,count+0x1a5))
   if not call(0x20971ac,[friend]):continue
   i=1
   while i<=byte(m,get()+0xd):
    if word(m,get()+0xf4+4*i)==profile:break
    i+=1
   if i<=byte(m,get()+0xd):continue
   buddy,status=SP-572,SP-552;r=call(0x20aa4f0,[word(m,get()),profile,buddy]);r|=call(0x20aa3e0,[word(m,get()),word(m,buddy),status])
   if r or word(m,status+4)!=4:continue
   version,number,distant=SP-564,SP-568,SP-576;vl=call(0x209b2bc,[STRINGS[b'VER'],version,status+8,47]);nl=call(0x209b2bc,[STRINGS[b'FME'],number,status+8,47]);dl=call(0x209b2bc,[STRINGS[b'MDF'],distant,status+8,47])
   if vl==0xffffffff or nl==0xffffffff or dl==0xffffffff or not(vl and nl and dl):continue
   if call(0x201f114,[version,0,10])!=3:continue
   numberValue=call(0x201f114,[number,0,10])
   if numberValue!=byte(m,get()+0x16):continue
   result=call(0x20a1278,[profile,1 if profile==(resend&0xffffffff)else delay]);break
  else:raise ValueError('Friend fixture failed bounded wrap')
 elif address==0x20a2544:
  ready=word(m,get()+0x1a0)==9
  if not ready:ready=word(m,get()+0x1a0)==16
  if not ready:ready=word(m,get()+0x1a0)==17
  if ready:
   now=call(0x2007a9c,[]);elapsed=millis(now,tickread(m,get()+0x1e0));state=word(m,get()+0x1a0)
   if state==9 and elapsed>6000:
    if call(0x209bc88,[])==5 and byte(m,get()+0x1ad)>=5:result=int(bool(call(0x20a1878,[word(m,get()+0xf4)])))
    else:target=get();pbyte(m,target+0x1ad,byte(m,target+0x1ad)+1);call(0x20a249c,[byte(m,get()+0x2d0),3])
   elif state==16 and elapsed>6000:
    target=get();pbyte(m,target+0x1ab,byte(m,target+0x1ab)+1)
    if byte(m,get()+0x1ab)>5:
     if byte(m,get()+0x15)==0 or byte(m,get()+0x15)==1:call(0x20a2394,[]);call(0x20a21e0,[1])
     elif not call(0x20a23bc,[word(m,get()+0x1d4)]):result=0
     elif byte(m,get()+0xd):pbyte(m,get()+0x1ab,0);target=get();tickput(m,target+0x1e0,call(0x2007a9c,[]))
     else:result=int(bool(call(0x20a16e4,[word(m,get()+0x20c)])))
    else:
     i=1
     while i<=byte(m,get()+0xd):
      bits=get();aid=byte(m,get()+0x2d0+i)
      if not word(m,bits+0x1d4)&(1<<aid):call(0x20a249c,[byte(m,get()+0x2d0+i),2])
      i+=1
   elif state==17:
    if elapsed>half(m,get()+0x1b0):call(0x20a19b4,[4])
 elif address==0x20a277c:
  profile,command,data=args
  if call(0x209bc88,[])==6:
   if command==13:
    if word(m,get()+0x1a0)!=8:call(0x20a3d7c,[8]);call(0x20a233c,[data])
    result=int(bool(call(0x20a2724,[profile,14])))
   elif command==14:
    if word(m,get()+0x1a0)==14:
     now=call(0x2007a9c,[]);lat=millis(now,tickread(m,get()+0x1e8))>>1
     if lat>300:
      latency=(millis(now,tickread(m,get()+0x1e8))>>1)-300
      if latency>half(m,get()+0x1b2):phalf(m,get()+0x1b2,latency)
     aid=call(0x20a2c38,[profile,0])
     if aid!=255:target=get();put(m,target+0x1d8,word(m,target+0x1d8)|(1<<aid))
     wanted=call(0x20a2c80,[1])
     if word(m,get()+0x1d8)==wanted:
      i=1
      while i<=byte(m,get()+0xd):
       if not call(0x20a2724,[word(m,get()+0xf4+4*i),15]):result=0;break
       i+=1
      else:call(0x20a3d7c,[15])
    else:result=int(bool(call(0x20a2724,[profile,15])))
   elif command==15:
    if word(m,get()+0x1a0)==8:call(0x20a21e0,[2])
 else:raise ValueError(hex(address))
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result

def ticks(ms):return(ms*33514+63)//64
def cases(address):
 if address==0x20a1608:return[dict(matchType=t,result=r,error=e,tick=k)for t in [0,1,2,3]for r,e,k in [(0,0,0),(7,0,MASK),(7,1,0x100000001),(-1,-1,MASK)]]
 if address==0x20a13d8:
  base=[dict(init=i,delay=d,friendLength=n,friendCount=c,profiles=p,resendPID=r,result=7)for i,d,n,c,p,r in [(0,0,3,0,[2000,2001,2002],0),(1,1,3,0,[2000,2001,2002],2000),(0,0,1,0,[0],0),(1,0,3,2,[-1,0,0],0),(0,0,3,0,[2000,2001,2002],2001)]]
  return base+[dict(dict(init=i,friendLength=3,profiles=[2000,2001,2002]),**bad)for i in [0,1]for bad in [dict(valid=0),dict(profiles=[1001,1002,1001]),dict(buddyError=7),dict(statusError=7),dict(buddyState=3),dict(version='4'),dict(version=''),dict(number='5'),dict(distant='')]]
 if address==0x20a2544:return[dict(state=s,tick=ticks(ms),waitCount=w,resends=r,matchType=t,connections=n,cancelResult=c,ackBits=b,dwcState=d)for s,ms,w,r,t,n,c,b,d in [(s,ms,0,0,0,2,1,0,5)for s in [0,9,16,17]for ms in [300,6000,6001]]+[(9,6001,w,0,0,2,c,0,d)for w,c,d in [(5,0,5),(5,1,5),(255,1,4)]]+[(16,6001,0,r,t,n,c,b,5)for r,t,n,c,b in [(4,0,3,1,0),(4,0,3,1,0x80000020),(5,0,2,1,0),(5,1,2,1,0),(5,2,0,1,0),(5,3,2,0,0),(5,3,2,1,0),(255,2,2,1,0)]]]+[dict(state=17,lastTick=MASK-100,tick=100),dict(state=16,tick=MASK,resends=5,matchType=3,connections=0,cancelResult=0)]
 if address==0x20a277c:return[dict(command=c,state=s,dwcState=d,cancelResults=r)for c,s,d,r in [(13,0,6,[1]),(13,8,6,[0]),(13,0,5,[1]),(15,8,6,[1]),(15,0,6,[1]),(255,14,6,[1])]]+[dict(command=14,state=14,dwcState=6,tick=ticks(ms),aid=a,wantedMask=b,connections=n,cancelResults=r,cancelLatency=l)for ms,a,b,n,r,l in [(600,5,32,2,[1],0),(602,5,32,2,[1,0],0),(2000,31,0x80000000,0,[1],300),(600,255,0,0,[1],0),(2000,5,0,3,[1],65535)]]+[dict(command=14,state=0,dwcState=6,cancelResults=[r])for r in [0,1]]
 raise ValueError(hex(address))
