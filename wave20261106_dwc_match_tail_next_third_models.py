import struct
from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
P0,P1,INPUT,ADDR=0x2170000,0x2171000,0x2172000,0x2173000
OBSERVED=set()
ARITY={0x20a3d70:0,0x2008c28:3,0x2008e0c:3,0x20061ac:4,0x20a020c:5,0x20a02b4:4,0x2007a9c:0,0x20b5f38:3,0x20a68b4:5,0x20b748c:1,0x20a699c:2,0x20a601c:3,0x20a60b0:1,0x20a60b4:1,0x20a00ac:6}
VIEWS=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/third/original-imports.json')['dataViews']
STRINGS={bytes.fromhex(v['expectedHex'])[:-1]:int(a,0)for a,v in VIEWS.items()}
MASK=(1<<64)-1

def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def arity(at,values,m):return ARITY[at]
def cstring(m,a):
 out=bytearray()
 while len(out)<1024:
  b=m.read(a+len(out),1)
  if b==bytes([0]):return bytes(out)
  out.extend(b)
 raise ValueError('Unterminated bounded command string')
def count(m,key):
 if not hasattr(m,'counts'):m.counts={}
 n=m.counts.get(key,0);m.counts[key]=n+1;return n
def byte(m,a):return m.read(a,1)[0]
def half(m,a):return int.from_bytes(m.read(a,2),'little')
def pbyte(m,a,v):m.write(a,bytes([v&255]))
def phalf(m,a,v):m.write(a,struct.pack('<H',v&65535))
def tickput(m,a,v):m.write(a,struct.pack('<Q',v&MASK))

def initial(address,v):
 regions={P0:bytes((i*7+11)&255 for i in range(0x500)),P1:bytes(0x500),INPUT:bytes(256),ADDR:b'192.0.2.1\0'+bytes(54),SP-0x1000:bytes(4096)}
 for a,view in VIEWS.items():regions[int(a,0)]=bytes.fromhex(view['expectedHex'])
 m=Memory(regions)
 for off,value in {0:0x2176000,0x10:0x2176100,0x1c:v.get('localIP',0xc0000201),0x24:0xc6336401,0xe4:0x2176200,0xf4:777,0x200:123,0x204:0xabcdef01,0x208:v.get('prior',0),0x2f0:v.get('bitmap',0)}.items():put(m,P0+off,value)
 pbyte(m,P0+0x15,v.get('matchType',1));pbyte(m,P0+0x1a6,v.get('distant',0));phalf(m,P0+0x1a,v.get('localPort',1234));phalf(m,P0+0xa4,4321)
 for i in range(64):put(m,INPUT+i*4,((i+1)*0x1020304 if not v.get('wide')else 0xffffffff-i)&0xffffffff)
 data=0 if v.get('nullData')else INPUT;command=v.get('command',2);length=v.get('length',3)
 if address==0x20a00ac:args=[command,321,0xcb007105,54321,data,length]
 elif address==0x20a020c:args=[command,0xcb007105,54321,data,length]
 elif address==0x20a1278:args=[321,v.get('delay',0)]
 else:args=[]
 return m,args

def effect(at,a,m,v):
 norm=a[:];result=0x76543210
 if at==0x20a3d70:result=P0
 elif at in [0x2008c28,0x2008e0c]:
  if a[2]>256:raise ValueError('Outside bounded command copy')
  raw=m.read(a[0],a[2]);m.write(a[1],raw);norm+=[raw.hex()]
 elif at==0x20061ac:
  fmt=cstring(m,a[2]);assert fmt in [b'%u',b'/%u'];text=(b'/'if fmt==b'/%u'else b'')+str(a[3]).encode();m.write(a[0],text[:a[1]-1]+bytes([0]));result=len(text);norm+=[fmt.hex()]
 elif at==0x20a020c:
  norm+=[m.read(a[3],min(a[4],32)*4).hex()if a[3]and a[4]else ''];result=v.get('result',3)
 elif at==0x20a02b4:norm+=[cstring(m,a[3]).hex()];result=v.get('result',3)
 elif at==0x2007a9c:result=v.get('tick',0x100000001)&MASK
 elif at==0x20b5f38:result=ADDR
 elif at==0x20a68b4:
  assert 20<=a[4]<=148;norm+=[cstring(m,a[1]).hex(),m.read(a[3],a[4]).hex()];seq=v.get('results',[0]);result=seq[min(count(m,'send'),len(seq)-1)]
 elif at==0x20b748c:pass
 elif at==0x20a699c:result=0x2176300
 elif at==0x20a601c:norm+=[cstring(m,a[1]).hex()];result=v.get('serverPID',999)
 elif at==0x20a60b0:result=v.get('serverIP',0xc63364ff)
 elif at==0x20a60b4:result=v.get('serverPort',65535)
 elif at==0x20a00ac:norm+=[m.read(a[4],a[5]*4).hex()];result=v.get('result',3)
 else:raise ValueError(('Outside command provider boundary',hex(at)))
 return result&(MASK if at==0x2007a9c else 0xffffffff),norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0;contract='void'
 def call(at,a):
  value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
 def get():return call(0x20a3d70,[])
 if address==0x209f110:pbyte(m,get()+0x3cc,255);pbyte(m,get()+0x3cd,0)
 elif address==0x209f640:
  valid=0
  for i in range(32):valid+=bool(word(m,get()+0x2f0)&(1<<i))
  pbyte(m,get()+0xe,max(valid-1,0))
 elif address==0x209f1c0:
  if byte(m,get()+0x15)!=2:pbyte(m,get()+0x14,0);pbyte(m,get()+0x16,0);call(0x20b748c,[word(m,get()+0x10)])
 elif address==0x20a020c:
  contract='ARM R0 word';command,ip,port,data,length=args;length=min(length&0xffffffff,32);packet=SP-172
  if data and length:call(0x2008c28,[data,packet+20,length*4])
  else:length=0
  m.write(packet,b'SBCM');put(m,packet+4,3);pbyte(m,packet+8,command);pbyte(m,packet+9,length*4);phalf(m,packet+10,half(m,get()+0x1a));put(m,packet+12,word(m,get()+0x1c));put(m,packet+16,word(m,get()+0x200))
  for i in range(5):
   sb=get();text=call(0x20b5f38,[ip,0,0]);result=call(0x20a68b4,[word(m,sb+0xe4),text,port,packet,20+length*4])
   if result!=2:break
 elif address==0x20a00ac:
  contract='ARM R0 word';command,profile,ip,port,data,length=args
  sb=byte(m,get()+0x15)==0
  if not sb:sb=(byte(m,get()+0x15)==3 or byte(m,get()+0x1a6)!=0)and command==6
  if sb:result=call(0x20a020c,[command,ip,port,data,length])
  else:
   message=SP-536;tmp=SP-552;size=0
   if data and length:
    size=call(0x20061ac,[message,512,STRINGS[b'%u'],word(m,data)])
    for i in range(1,length):
     more=call(0x20061ac,[tmp,16,STRINGS[b'/%u'],word(m,data+4*i)])
     if size+more+1>512:break
     call(0x2008e0c,[tmp,message+size,more]);size+=more
   pbyte(m,message+size,0);result=call(0x20a02b4,[word(m,get()),command,profile,message])
  if command in [2,6,8,9]:
   pbyte(m,get()+0x3cc,command);phalf(m,get()+0x3ce,port);put(m,get()+0x3d0,ip);put(m,get()+0x454,profile);put(m,get()+0x458,length);target=get();tickput(m,target+0x45c,call(0x2007a9c,[]))
   if data and length:call(0x2008c28,[data,get()+0x3d4,length*4])
 elif address==0x20a1278:
  contract='ARM R0 word';profile,delay=args
  if delay or(word(m,get()+0x1c)==0 and half(m,get()+0x1a)==0):
   put(m,get()+0x1bc,1);target=get();tickput(m,target+0x1c0,call(0x2007a9c,[]));put(m,get()+0xf4,profile);put(m,get()+0x204,0)
  else:
   payload=SP-32
   if byte(m,get()+0x15)==0:
    server=call(0x20a699c,[word(m,get()+0xe4),0]);target=get();put(m,target+0xf4,call(0x20a601c,[server,STRINGS[b'dwc_pid'],0]));target=get();put(m,target+0x24,call(0x20a60b0,[server]));target=get();phalf(m,target+0xa4,call(0x20a60b4,[server]));target=get();put(m,target+0x204,word(m,get()+0xf4));length=1
   else:
    if byte(m,get()+0x15)==1:put(m,get()+0xf4,profile)
    put(m,get()+0x204,profile);put(m,payload+4,word(m,get()+0x1c));put(m,payload+8,half(m,get()+0x1a));length=3
   put(m,get()+0x1c8,6000);target=get();tickput(m,target+0x1cc,call(0x2007a9c,[]));put(m,get()+0x1bc,0);command=11 if word(m,get()+0x208)else 1;put(m,payload,byte(m,get()+0x15));ip=get();port=get();result=call(0x20a00ac,[command,profile,word(m,ip+0x24),half(m,port+0xa4),payload,length])
 else:raise ValueError(hex(address))
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result

def cases(address):
 if address==0x209f110:return[{},dict(matchType=2)]
 if address==0x209f640:return[dict(bitmap=x)for x in [0,1,2,0x80000000,0x80000001,0x55555555,0xffffffff]]
 if address==0x209f1c0:return[dict(matchType=x)for x in [0,1,2,3,255]]
 if address==0x20a020c:return[dict(length=n,nullData=z,results=r,command=255)for n in [0,1,31,32,33,-1]for z in [False,True]for r in [[0],[2,0],[2],[1],[-1]]]
 if address==0x20a00ac:return[dict(matchType=t,distant=d,command=c,length=n,nullData=z,result=r)for t,d,c,n,z,r in [(t,d,c,n,z,3)for t,d in [(0,0),(1,0),(1,1),(3,0)]for c in [1,2,6,8,9,255]for n,z in [(0,False),(3,False),(3,True)]]]+[dict(command=1,length=64,wide=True),dict(command=9,length=32,tick=MASK,result=0xffffffff)]
 if address==0x20a1278:return[dict(matchType=t,delay=d,localIP=ip,localPort=port,prior=p,tick=tick,result=r)for t in [0,1,2,3]for d,ip,port in [(1,123,45),(0,0,0),(0,0,45),(0,123,0)]for p,tick,r in [(0,0,0),(1,MASK,0xffffffff)]]
 raise ValueError(hex(address))
