from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
G,N0,N1,H,P,B0,B1,ST=0x21d1914,0x2170000,0x2173000,0x2176000,0x2179000,0x217a000,0x217a100,0x217b000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
AP,AT,FP,FT=0x2234000,0x2234004,0x2234100,0x2234104
ARITY={AP:2,AT:2,FP:3,FT:3,0x2008d78:3,0x2007074:1,0x2099178:0,0x20987b0:1,0x2097618:0,0x20983d0:1,0x20975b8:0,0x2006890:1,0x200708c:1,0x2007110:1}
OBSERVED=set()
DATA={int(at,0):bytes.fromhex(v['expectedHex'])for at,v in read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/fifth/original-imports.json')['dataViews'].items()if v['storage']=='data'}
TAGS={raw[:-1].decode('ascii'):at for at,raw in DATA.items()}
def dynamic_callbacks(v):return{AP:dict(mode='arm'),AT:dict(mode='thumb'),FP:dict(mode='arm'),FT:dict(mode='thumb')}
def expected_reads(address,v):return []
def allocator(v):return AT|1 if v.get('callbackMode',0)&1 else AP
def freer(v):return FT|1 if v.get('callbackMode',0)&2 else FP
def initial(address,v):
 m=Memory({**DATA,G:bytes([0x95])*24,N0:bytes((i*13+1)&255 for i in range(4596)),N1:bytes((i*7+5)&255 for i in range(4596)),H:bytes([0x77])*7188,P:bytes(12),B0:bytes([0xa7])*128,B1:bytes([0xb8])*128,ST:bytes(128),SP-0x1000:bytes(4096)})
 put(m,G,0 if v.get('nullNet')else N0);put(m,G+4,7);put(m,G+20,H if v.get('http')else 0)
 for n in [N0,N1]:
  put(m,n+4360,allocator(v));put(m,n+4364,freer(v));put(m,n+4368,0x12345000);put(m,n+4372,B0 if v.get('bodyMask',0)&1 else 0);put(m,n+4376,B1 if v.get('bodyMask',0)&2 else 0);put(m,n+4488,v.get('threadId',1))
 put(m,P,allocator(v));put(m,P+4,freer(v));put(m,P+8,0x11112222)
 return m,[P]if address==0x2098fbc else[v.get('error',0)]if address==0x2099bc8 else[]
def effect(at,a,m,v):
 result=0x76543210;norm=a[:]
 if at in [AP,AT]:
  count=word(m,ST);put(m,ST,count+1);result=0 if count==v.get('failAllocation',-1)else N0 if count==0 else H
  if v.get('allocationChangesParam'):
   put(m,P,AP if allocator(v)==(AT|1)else AT|1);put(m,P+4,FP if freer(v)==(FT|1)else FT|1);put(m,P+8,0x33334444)
 elif at in [FP,FT]:
  count=word(m,ST+4);put(m,ST+4,count+1)
  if v.get('freeSwapsNet')and count==0:put(m,G,N1)
  if v.get('freeChangesCallbacks')and word(m,G):put(m,word(m,G)+4364,FP if freer(v)==(FT|1)else FT|1)
 elif at==0x2008d78:
  m.write(a[0],bytes([a[1]&255])*a[2])
  if v.get('fillSwapsNet'):put(m,G,N1)
 elif at==0x2097618:
  if v.get('authClearsNet'):put(m,G,0)
  if v.get('authSwapsNet'):put(m,G,N1)
 elif at==0x20975b8:
  if v.get('authSwapsNet'):put(m,G,N1)
 elif at==0x2006890:
  if v.get('joinSwapsNet'):put(m,G,N1)
 elif at==0x200708c:
  if v.get('lockSwapsNet'):put(m,G,N1)
 elif at in [0x2007074,0x2099178,0x20987b0,0x20983d0,0x2007110]:pass
 else:raise ValueError(('Outside supplied Netcheck provider scope',hex(at)))
 return result&0xffffffff,norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0;contract='void'
 def call(at,a):
  r,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return r
 if address==0x2098fbc:
  contract='ARM R0 word';result=4;alloc=word(m,P)
  if not word(m,G):
   n=call(alloc&~1,[TAGS['ALLOC DWCnetcheck'],4596]);put(m,G,n)
   if n:
    call(0x2008d78,[word(m,G),0,4596]);put(m,word(m,G)+4100,-99999);m.write(word(m,G)+4360,m.read(P,12))
    if not word(m,G+20):
     h=call(alloc&~1,[TAGS['ALLOC DWChttp'],7188]);put(m,G+20,h)
     if h:put(m,G+4,0);call(0x2007074,[word(m,G)+4572]);call(0x2099178,[]);result=0
 elif address==0x2099058:
  free=word(m,word(m,G)+4364)
  if word(m,G+20):call(0x20987b0,[word(m,G+20)]);call(free&~1,[TAGS['FREE DWChttp'],word(m,G+20),0]);put(m,G+20,0)
  call(0x2097618,[])
  if word(m,G):
   for off,tag in [(4372,'FREE DWCnetcheck->body_302'),(4376,'FREE DWCnetcheck->body_wayport')]:
    if word(m,word(m,G)+off):call(free&~1,[TAGS[tag],word(m,word(m,G)+off),0]);put(m,word(m,G)+off,0)
   call(free&~1,[TAGS['FREE DWCnetcheck'],word(m,G),0]);put(m,G,0)
 elif address==0x20990f0:
  if word(m,G):
   if word(m,G+20):call(0x20983d0,[word(m,G+20)])
   call(0x20975b8,[])
   if word(m,word(m,G)+4488):call(0x2006890,[word(m,G)+4380])
   put(m,word(m,G)+4100,-7)
 elif address==0x2099bc8:call(0x200708c,[word(m,G)+4572]);put(m,word(m,G)+4096,args[0]);call(0x2007110,[word(m,G)+4572])
 else:raise ValueError('Outside four Netcheck callers')
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result

def cases(address):
 if address==0x2098fbc:return[dict(nullNet=n,http=h,failAllocation=f,callbackMode=c,**flags)for n in [False,True]for h in [False,True]for f in [-1,0,1]for c in range(4)for flags in [{},{'allocationChangesParam':True},{'fillSwapsNet':True}]]
 if address==0x2099058:return[dict(http=h,bodyMask=b,callbackMode=c,**flags)for h in [False,True]for b in [0,1,2,3]for c in range(4)for flags in [{},{'authClearsNet':True},{'authSwapsNet':True},{'freeSwapsNet':True,'freeChangesCallbacks':True}]]
 if address==0x20990f0:return[dict(nullNet=n,http=h,threadId=i,**flags)for n in [False,True]for h in [False,True]for i in [0,1,2,0xffffffff]for flags in [{},{'authSwapsNet':True},{'joinSwapsNet':True}]]
 if address==0x2099bc8:return[dict(error=e,lockSwapsNet=b)for e in [0,1,4,11,-1,-7,-2147483648,0x7fffffff]for b in [False,True]]
 raise ValueError('No Netcheck caller cases')
