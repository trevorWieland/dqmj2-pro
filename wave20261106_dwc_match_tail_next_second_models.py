import struct
from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
P0,P1,INPUT,ADD=0x2170000,0x2171000,0x2172000,0x2175000
KEYS,GLOBAL=0x21d1ba8,0x21d1b88
OBSERVED=set()
ARITY={0x20a3d70:0,0x2008c28:3,0x209fda4:4,0x20061ac:5,0x20a6964:1,0x20a6898:7,0x2007a9c:0}
VIEWS=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/second/original-imports.json')['dataViews']
STRINGS={bytes.fromhex(v['expectedHex'])[:-1]:int(a,0)for a,v in VIEWS.items()if v['storage']=='data'}
MASK=(1<<64)-1

def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def cstring(m,a):
 out=bytearray()
 while len(out)<1024:
  b=m.read(a+len(out),1)
  if b==bytes([0]):return bytes(out)
  out.extend(b)
 raise ValueError('Unterminated bounded SB filter')
def counter(m,key):
 if not hasattr(m,'counts'):m.counts={}
 n=m.counts.get(key,0);m.counts[key]=n+1;return n
def arity(at,values,m):return 4 if at==0x20061ac and cstring(m,values[2])==b' and (%s)'else ARITY[at]

def initial(address,v):
 regions={P0:bytes((i*7+11)&255 for i in range(0x500)),P1:bytes((i*11+3)&255 for i in range(0x500)),INPUT:bytes(132),ADD:v.get('addFilter','X').encode()+bytes(256-len(v.get('addFilter','X'))),GLOBAL:bytes(12),KEYS:bytes(1848),SP-0x1000:bytes(4096)}
 for a,view in VIEWS.items():
  if view['storage']=='data':regions[int(a,0)]=bytes.fromhex(view['expectedHex'])
 m=Memory(regions)
 for p in [P0,P1]:
  m.write(p+0x15,bytes([v.get('matchType',0),v.get('numEntry',4)]));put(m,p+0x1a0,v.get('state',3));put(m,p+0x200,v.get('profile',123));put(m,p+0x204,0x55555555);put(m,p+0x208,v.get('prior',0));put(m,p+0xe4,0x2176000+(0x100 if p==P1 else 0))
 put(m,GLOBAL+8,ADD if v.get('append')else 0)
 for i in range(154):
  if v.get('keys')=='all'or(v.get('keys')=='edges'and i in [0,153]):m.write(KEYS+i*12,bytes([i+100]))
 raw=v.get('count',2);put(m,INPUT,raw)
 for i in range(1,33):put(m,INPUT+i*4,0x11000000+i)
 return m,[v.get('profileArg',321),INPUT]if address==0x20a121c else[v.get('profileArg',321)]

def effect(at,a,m,v):
 result=0x76543210;norm=a[:]
 if at==0x20a3d70:
  n=counter(m,'get');seq=v.get('getSequence',[0]);result=[P0,P1][seq[min(n,len(seq)-1)]]
 elif at==0x2008c28:
  if a[2]>124 or a[2]%4:raise ValueError('Outside bounded backup copy')
  raw=m.read(a[0],a[2]);m.write(a[1],raw);norm+=[raw.hex()]
 elif at==0x209fda4:
  text=b'D'*v.get('defaultLength',4);m.write(a[0],text+bytes([0]));result=len(text)
 elif at==0x20061ac:
  fmt=cstring(m,a[2])
  if fmt==b' and (%s)':raw=cstring(m,a[3]);text=b' and ('+raw+b')';norm+=[fmt.hex(),raw.hex()]
  elif fmt==b'%s = %u':raw=cstring(m,a[3]);text=raw+b' = '+str(a[4]).encode();norm+=[fmt.hex(),raw.hex()]
  else:raise ValueError('Unexpected SB formatter shape')
  if not 1<=a[1]<=256:raise ValueError('Outside valid filter formatter capacity')
  m.write(a[0],text[:a[1]-1]+bytes([0]));result=len(text)
 elif at==0x20a6964:pass
 elif at==0x20a6898:
  if not 7<=a[4]<=161:raise ValueError('Outside measured key-list bound')
  norm+=[m.read(a[3],a[4]).hex(),cstring(m,a[5]).hex()];n=counter(m,'update');seq=v.get('results',[0]);result=seq[min(n,len(seq)-1)]
 elif at==0x2007a9c:result=v.get('tick',0x100000001)&MASK
 else:raise ValueError(('Outside backup/SB provider boundary',hex(at)))
 return result&(MASK if at==0x2007a9c else 0xffffffff),norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0;contract='void'
 def call(at,a):
  value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
 if address==0x20a121c:
  length=(word(m,INPUT)+2)&0xffffffff
  if length>2:target=call(0x20a3d70,[]);call(0x2008c28,[INPUT+4,target+0x350,(length-2)*4])
  target=call(0x20a3d70,[]);put(m,target+0x348,(length-1)&0xffffffff);target=call(0x20a3d70,[]);put(m,target+0x34c,args[0])
 else:
  contract='ARM R0 word';fields=SP-444;filter=SP-283;basic=[8,10,50,51,52,53,54];m.write(fields,bytes(basic));mt=call(0x20a3d70,[])
  if m.read(mt+0x15,1)[0]==0 or m.read(call(0x20a3d70,[])+0x15,1)[0]==1:
   basic+=[m.read(KEYS+i*12,1)[0]for i in range(154)if m.read(KEYS+i*12,1)[0]];m.write(fields,bytes(basic))
  state=word(m,call(0x20a3d70,[])+0x1a0);profile=args[0]
  if state==3 and word(m,call(0x20a3d70,[])+0x208)==0:
   p=call(0x20a3d70,[]);n=call(0x20a3d70,[]);t=call(0x20a3d70,[]);length=call(0x209fda4,[filter,word(m,p+0x200),m.read(n+0x16,1)[0],m.read(t+0x15,1)[0]])
   if word(m,GLOBAL+8):call(0x20061ac,[filter+length,256-length,STRINGS[b' and (%s)'],word(m,GLOBAL+8)])
  else:
   if state not in [2,3,4,5]:raise ValueError('Uninitialized filter states are outside semantic fixtures')
   if state==3:profile=word(m,call(0x20a3d70,[])+0x208)
   call(0x20061ac,[filter,256,STRINGS[b'%s = %u'],STRINGS[b'dwc_pid'],profile]);put(m,call(0x20a3d70,[])+0x204,profile)
  call(0x20a6964,[word(m,call(0x20a3d70,[])+0xe4)])
  for i in range(5):
   result=call(0x20a6898,[word(m,call(0x20a3d70,[])+0xe4),1,0,fields,len(basic),filter,6])
   if result!=2:break
  if result==0:target=call(0x20a3d70,[]);tick=call(0x2007a9c,[]);m.write(target+0x174,struct.pack('<Q',(tick+15709687)&MASK))
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result

def cases(address):
 if address==0x20a121c:return[dict(count=n,profileArg=p,getSequence=seq)for n in [0,1,2,31,0xfffffffe,0xffffffff]for p in [0,123,0xffffffff]for seq in [[0],[1],[0,1,0]]]
 return[dict(state=s,prior=p,matchType=t,keys=k,append=a)for s,p in [(2,0),(3,0),(3,777),(4,0),(5,0)]for t in [0,1,2,3]for k in ['none','edges','all']for a in [False,True]]+[dict(state=s,append=a,results=r,tick=tick)for s in [2,3]for a in [False,True]for r in [[0],[2,2,0],[2],[1],[-1]]for tick in [0,0xffffffff,0x100000001,MASK]]+[dict(state=3,append=True,defaultLength=n,addFilter='Y'*100)for n in [0,17,240,255]]
