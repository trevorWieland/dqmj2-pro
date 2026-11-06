from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
G,I0,I1,ST=0x21d19a4,0x2170000,0x2174000,0x2178000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
AP,AT,FP,FT=0x2234000,0x2234004,0x2234100,0x2234104
ARITY={AP:2,AT:2,FP:3,FT:3,0x209a9f8:2,0x2008d78:3,0x20987b0:1,0x20983d0:1,0x20068c0:1}
OBSERVED=set()
DATA={int(at,0):bytes.fromhex(v['expectedHex'])for at,v in read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/sixth/original-imports.json')['dataViews'].items()if v['storage']=='data'}
TAGS={raw[:-1].decode('ascii'):at for at,raw in DATA.items()}
def dynamic_callbacks(v):return{AP:dict(mode='arm'),AT:dict(mode='thumb'),FP:dict(mode='arm'),FT:dict(mode='thumb')}
def expected_reads(address,v):return []
def allocator(v):return AT|1 if v.get('callbackMode',0)&1 else AP
def freer(v):return FT|1 if v.get('callbackMode',0)&2 else FP
def initial(address,v):
 m=Memory({**DATA,G:bytes(4),I0:bytes((i*13+5)&255 for i in range(7200)),I1:bytes((i*7+3)&255 for i in range(7200)),ST:bytes(128),SP-0x1000:bytes(4096)})
 put(m,G,0 if v.get('nullWork')else I0)
 for at in [I0,I1]:put(m,at,allocator(v));put(m,at+4,freer(v));put(m,at+7084,v.get('threadId',1))
 return m,[allocator(v),freer(v)]if address==0x2099d6c else[]
def effect(at,a,m,v):
 result=0x76543210;norm=a[:]
 if at in [AP,AT]:result=0 if v.get('allocationFails')else I0
 elif at==0x2008d78:
  m.write(a[0],bytes([a[1]&255])*a[2])
  if v.get('fillSwapsWork'):put(m,G,I1)
 elif at==0x20987b0:
  if v.get('destroySwapsWork'):put(m,G,I1)
  if v.get('destroyChangesFree'):put(m,word(m,G)+4,FP if freer(v)==(FT|1)else FT|1)
 elif at==0x20068c0:
  result=v.get('terminated',0)&0xffffffff
  if v.get('probeSwapsWork'):put(m,G,I1)
 elif at in [FP,FT,0x209a9f8,0x20983d0]:pass
 else:raise ValueError(('Outside SVL provider boundary',hex(at)))
 return result&0xffffffff,norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0;contract='void'
 def call(at,a):
  r,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return r
 if address==0x2099d6c:
  contract='ARM R0 word'
  if word(m,G):call(0x209a9f8,[9,-24100])
  else:
   p=call(args[0]&~1,[TAGS['ALLOC intwork'],7200]);put(m,G,p)
   if not p:call(0x209a9f8,[9,-24100])
   else:call(0x2008d78,[word(m,G),0,7200]);put(m,word(m,G),args[0]);put(m,word(m,G)+4,args[1]);result=1
 elif address==0x2099dc8:
  if word(m,G):call(0x20987b0,[word(m,G)+8]);call(word(m,word(m,G)+4)&~1,[TAGS['FREE intwork'],word(m,G),0]);put(m,G,0)
 elif address==0x209a008:
  if word(m,G)and word(m,word(m,G)+7084):
   if call(0x20068c0,[word(m,G)+6976])==0:call(0x20983d0,[word(m,G)+8])
 else:raise ValueError('Outside selected SVL lifecycle')
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result

def cases(address):
 if address==0x2099d6c:return[dict(nullWork=n,allocationFails=f,callbackMode=c,**flags)for n in [False,True]for f in [False,True]for c in range(4)for flags in [{},{'fillSwapsWork':True}]]
 if address==0x2099dc8:return[dict(nullWork=n,callbackMode=c,**flags)for n in [False,True]for c in range(4)for flags in [{},{'destroySwapsWork':True},{'destroyChangesFree':True},{'destroySwapsWork':True,'destroyChangesFree':True}]]
 if address==0x209a008:return[dict(nullWork=n,threadId=i,terminated=t,probeSwapsWork=s)for n in [False,True]for i in [0,1,0xffffffff]for t in [-1,0,1,2]for s in [False,True]]
 raise ValueError('No selected SVL cases')
