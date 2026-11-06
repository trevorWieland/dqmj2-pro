from project import ROOT
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
PG,SG,P0,P1,S0,S1,SP,STOP,MAGIC,DIV=0x21d19a8,0x21d19a4,0x2170000,0x2174000,0x2178000,0x217c000,0x2701000,0x27e0000,0,0
ARITY={0x20068c0:1,0x209446c:0,0x209a56c:0,0x209a03c:0,0x209a9f8:2,0x20987b0:1,0x209aa64:3}
OBSERVED=set()
def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def is_prof(address):return address==0x209a4a0
def state(address):return(PG,P0,P1,7076,0)if is_prof(address)else(SG,S0,S1,7084,8)
def initial(address,v):
 m=Memory({PG:bytes(4),SG:bytes(4),P0:bytes((i*7+3)&255 for i in range(7464)),P1:bytes((i*3+7)&255 for i in range(7464)),S0:bytes((i*13+5)&255 for i in range(7200)),S1:bytes((i*5+13)&255 for i in range(7200)),SP-0x1000:bytes(4096)})
 g,w,w1,id_offset,http_offset=state(address);put(m,g,0 if v.get('nullWork')else w)
 for work in [w,w1]:put(m,work+id_offset,v.get('threadId',1));put(m,work+http_offset+4128,v.get('error',8))
 return m,[]
def effect(at,a,m,v):
 address=v['_address'];g,w,w1,id_offset,http_offset=state(address);result=0x76543210;norm=a[:]
 if at==0x20068c0:
  result=v.get('terminated',1)
  if v.get('terminateSwapsWork'):put(m,g,w1)
 elif at==0x209446c:
  result=v.get('apType',0)
  if v.get('apSwapsWork'):put(m,g,w1)
 elif at in [0x209a56c,0x209a03c]:
  result=v.get('parsed',1)
  if v.get('parseSwapsWork'):put(m,g,w1)
 elif at==0x209a9f8:
  if v.get('errorSwapsWork'):put(m,g,w1)
 elif at==0x20987b0:
  if v.get('destroySwapsWork'):put(m,g,w1)
 elif at==0x209aa64:pass
 else:raise ValueError(('Outside state-processing provider boundary',hex(at)))
 return result&0xffffffff,norm

def model(address,v):
 v['_address']=address;m,args=initial(address,v);calls=[];g,w,w1,id_offset,http_offset=state(address);result=0
 def call(at,a):
  r,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return r
 current=word(m,g)
 if current and word(m,current+id_offset):
  if call(0x20068c0,[current+http_offset+6968])!=1:result=1 if is_prof(address)else 2
  elif is_prof(address):
   ap=call(0x209446c,[]);ap=99 if ap>99 else ap;error=word(m,word(m,g)+4128)
   if error==8:result=3 if call(0x209a56c,[])==0 else 2
   elif error==2:call(0x209a9f8,[8,-52100-ap]);result=3
   elif error in [3,4,6]:call(0x209a9f8,[19,-33010]);result=3
   else:call(0x209a9f8,[19,-33030]);result=3
   call(0x20987b0,[word(m,g)]);call(0x209aa64,[0,word(m,g),0]);put(m,g,0)
  else:
   error=word(m,word(m,g)+4136)
   if error==8:
    parsed=call(0x209a03c,[]);call(0x20987b0,[word(m,g)+8]);result=4 if parsed==0 else 3
   elif error==7:call(0x20987b0,[word(m,g)+8]);result=5
   else:call(0x20987b0,[word(m,g)+8]);call(0x209a9f8,[17,-24101]);result=4
 elif current:result=0 if is_prof(address)else 1
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result

def cases(address):
 active=[dict(nullWork=n,threadId=i,terminated=t,terminateSwapsWork=s)for n in [False,True]for i in [0,1,0xffffffff]for t in [-1,0,1,2]for s in [False,True]]
 errors=[-1,0,1,2,3,4,5,6,7,8,9,0x7fffffff]
 if is_prof(address):
  return active+[dict(error=e,apType=a,parsed=p)for e in errors for a in [-1,0,1,99,100,254,255,256]for p in [0,1]]+[dict(error=e,apType=255,parsed=-1,**flags)for e in errors for flags in [{'apSwapsWork':True},{'parseSwapsWork':True},{'errorSwapsWork':True,'destroySwapsWork':True}]]
 return active+[dict(error=e,parsed=p,**flags)for e in errors for p in [0,1,-1,2]for flags in [{},{'parseSwapsWork':True},{'destroySwapsWork':True}]]
