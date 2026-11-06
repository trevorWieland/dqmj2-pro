import struct
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
G,P0,P1=0x21d19bc,0x2170000,0x2171000
OBSERVED=set()
ARITY={0x2008d78:3,0x2090b60:1,0x2094284:1,0x209a9f8:2,0x2096948:0,0x2096b7c:0,0x209abec:5,0x2094398:0,0x208a268:0,0x209ac5c:0,0x2094420:0,0x2090b54:0,0x209ae18:0,0x209ab18:4,0x2096900:2}

def signed(x):return x-(1<<32)if x&(1<<31)else x
def half(m,a):return int.from_bytes(m.read(a,2),'little')
def sethalf(m,a,v):m.write(a,struct.pack('<H',v&65535))
def byte(m,a):return m.read(a,1)[0]
def setbyte(m,a,v):m.write(a,bytes([v&255]))
def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def pointer(m):return word(m,G+4)

def initial(address,v):
 m=Memory({G:struct.pack('<II',v.get('old',-200)&0xffffffff,0 if v.get('null')else P0),P0:bytes((i*7+11)&255 for i in range(100)),P1:bytes((i*13+5)&255 for i in range(100)),SP-0x1000:bytes(4096)})
 for p in [P0,P1]:
  put(m,p,v.get('acState',99));sethalf(m,p+4,v.get('state',1));sethalf(m,p+6,v.get('online',1));sethalf(m,p+8,v.get('dma',3));sethalf(m,p+10,v.get('power',1));setbyte(m,p+12,v.get('wont',0));put(m,p+16,v.get('wds',0));put(m,p+84,v.get('wepMode',3))
 args=[P1,v.get('dma',3),v.get('power',1),v.get('priority',20)]if address==0x209ab18 else[]
 return m,args

def effect(at,a,m,v):
 result=0x76543210;norm=a[:]
 if at==0x2008d78:
  if a[2]not in [12,100]:raise ValueError('Unexpected measured clear extent')
  m.write(a[0],bytes([a[1]&255])*a[2])
 elif at==0x2090b60:pass
 elif at==0x2094284:
  norm+=[m.read(a[0],12).hex()];result=v.get('created',1)
 elif at==0x209a9f8:
  if v.get('errorSwap'):put(m,G+4,P1)
 elif at==0x2096948:
  result=v.get('wdsResult',2)
  if v.get('wdsSwap'):put(m,G+4,P1)
 elif at==0x2096b7c:
  if v.get('cleanupWdsSwap'):put(m,G+4,P1)
 elif at==0x209abec:
  if v.get('debugSwap'):put(m,G+4,P0 if pointer(m)==P1 else P1)
 elif at==0x2094398:
  result=v.get('processed',-7)
  if v.get('processSwap'):put(m,G+4,P1)
 elif at==0x208a268:
  result=v.get('phase',9)
  if v.get('phaseSwap'):put(m,G+4,P1)
 elif at==0x209ac5c:
  if v.get('statusProcessSwap'):put(m,G+4,P1)
  if 'processOld'in v:put(m,G,v['processOld'])
 elif at==0x2094420:
  result=v.get('status',5)
  if v.get('statusSwap'):put(m,G+4,P1)
 elif at==0x2090b54:
  result=v.get('priority',20)
  if v.get('prioritySwap'):put(m,G+4,P1)
 elif at==0x209ae18:put(m,G+4,0)
 elif at==0x209ab18:
  p=a[0];m.write(p,bytes(100));sethalf(m,p+8,a[1]);sethalf(m,p+10,1);sethalf(m,p+4,1);put(m,G+4,p)
 elif at==0x2096900:
  result=v.get('startup',1)
  if v.get('startupSwap'):put(m,G+4,P1)
 else:raise ValueError(('Outside internet-control provider boundary',hex(at)))
 return result&0xffffffff,norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0;contract='void'
 def call(at,a):
  value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
 p=pointer(m)
 if address==0x209ab18:
  if not p:
   target,dma,power,priority=args;call(0x2008d78,[target,0,100]);sethalf(m,target+8,dma);sethalf(m,target+10,1);sethalf(m,target+4,1);sethalf(m,target+6,0);setbyte(m,target+12,0);put(m,target+16,0);put(m,G+4,target);call(0x2090b60,[priority])
 elif address==0x209ab84:
  if not p:call(0x209a9f8,[9,-50199])
  elif half(m,p+4)==1:
   config=SP-16;call(0x2008d78,[config,0,12]);p=pointer(m);setbyte(m,config+8,half(m,p+8));setbyte(m,config+9,half(m,p+10));put(m,config,0x209aa39);put(m,config+4,0x209aa65);sethalf(m,p+4,2)
   if call(0x2094284,[config])==0:call(0x209a9f8,[9,-50199])
 elif address==0x209ac5c:
  if p:
   wds=word(m,p+16)
   if wds==1:put(m,p,0);value=call(0x2096948,[]);put(m,pointer(m)+16,value)
   elif wds==2:
    call(0x2096b7c,[]);p=pointer(m);call(0x209abec,[p+20,p+52,word(m,p+84),p+88,8]);put(m,pointer(m)+16,0)
   elif wds==3:call(0x2096b7c,[]);put(m,pointer(m),-1);setbyte(m,pointer(m)+12,1)
   elif wds not in [4,5]:
    state=half(m,p+4)
    if state==2:value=call(0x2094398,[]);put(m,pointer(m),value)
    elif state==4 and half(m,p+6)and call(0x208a268,[])!=9:sethalf(m,pointer(m)+6,0);sethalf(m,pointer(m)+4,6)
 elif address==0x209ad08:
  contract='ARM R0 word'
  if p:
   wds=word(m,p+16)
   if wds in [1,2]:result=2
   elif wds==3:call(0x209ac5c,[]);call(0x209a9f8,[5,word(m,G)]);sethalf(m,pointer(m)+4,7);put(m,pointer(m)+16,4);result=7
   elif wds==4:result=7
   elif wds==5:result=5
   else:
    result=half(m,p+4)
    if result!=1:
     state=signed(call(0x2094420,[]))
     if state==5:sethalf(m,pointer(m)+4,4);sethalf(m,pointer(m)+6,1);setbyte(m,pointer(m)+12,1);result=4
     elif state<0:
      if state>=-10:setbyte(m,pointer(m)+12,1);call(0x209a9f8,[9,-50199]);sethalf(m,pointer(m)+4,8);result=8
      elif not byte(m,pointer(m)+12):
       oldp=pointer(m);dma=half(m,oldp+8);priority=call(0x2090b54,[]);put(m,G,state);call(0x209ae18,[]);call(0x209ab18,[oldp,dma,1,priority&65535]);call(0x2096900,[pointer(m)+20,1]);put(m,pointer(m)+16,1);put(m,pointer(m),0);result=2
      else:call(0x209a9f8,[5,min(signed(word(m,G)),state)]);sethalf(m,pointer(m)+4,7);result=7
     else:result=2
 else:raise ValueError('Outside four selected internet-control callers')
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result

def cases(address):
 if address==0x209ab18:return[dict(null=False)]+[dict(null=True,dma=d,power=p,priority=r)for d in [0,3,255,256,65535]for p in [0,1,65535]for r in [0,20,65535]]
 if address==0x209ab84:return[dict(null=True)]+[dict(state=s)for s in [0,2,8,65535]]+[dict(state=1,dma=d,power=p,created=c)for d in [0,3,255,256,65535]for p in [0,1,256,65535]for c in [0,1,-1]]
 if address==0x209ac5c:
  flags=[{},{'wdsSwap':True,'cleanupWdsSwap':True,'debugSwap':True,'processSwap':True,'phaseSwap':True}]
  return[dict(null=True)]+[dict(wds=w,wdsResult=r,**f)for w in [1,2,3,4,5]for r in [-1,0,1,2,5]for f in flags]+[dict(wds=w,state=s,online=o,phase=p,**f)for w in [-1,0,6]for s in [0,2,4,8]for o in [0,1]for p in [8,9]for f in flags]
 flags=[{},{'errorSwap':True,'statusProcessSwap':True,'processOld':-77,'statusSwap':True,'prioritySwap':True,'startupSwap':True,'priority':0x12345678}]
 return[dict(null=True)]+[dict(wds=w,**f)for w in [1,2,3,4,5]for f in flags]+[dict(wds=w,state=s,wont=t,status=a,**f)for w in [-1,0,6]for s in [1,2,4,8]for t in [0,1]for a in [-100,-11,-10,-1,0,5,6]for f in flags]
