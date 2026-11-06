import itertools
from project import ROOT
from wave20261106_wcm_manager_next_cps_first_models import Memory
STOP=0x4000000
SP=0x3010000
A=0x22e1000
B=0x22e3000
SOC=0x22e6000
RECV=0x22e8000
THREAD=0x22e7000
THREADINFO=0x20e33e4
SCAV=0x21cff60
RESET=0x21cfdf8
RSOC=RESET+68
DISABLE=0x2007ff4
RESTORE=0x2008008
COPY=0x2008e0c
FILL=0x2008d78
TICK=0x2007a9c
YIELD=0x20069f8
WAKE=0x200698c
RELIABLE=-1
DIV=-1
RET64={TICK}
OBSERVED=set()
READ_ONLY=set()
ARITY={DISABLE:0,RESTORE:1,COPY:3,FILL:3,TICK:0,YIELD:0,WAKE:1,0x208cbb0:1,0x208c55c:5,0x208bc18:1,0x208bf98:1,0x208cbc4:3,0x208cb5c:2,0x208cb1c:2,0x208ccec:3,0x208cc24:4,0x208c97c:2,0x208cd80:3,0x208ca18:2,0x208cc0c:2,0x208cc18:2}
def r32(m,a):return int.from_bytes(m.read(a,4),'little')
def r16(m,a):return int.from_bytes(m.read(a,2),'little')
def number(m,a,v,n=4):m.write(a,(v&((1<<(8*n))-1)).to_bytes(n,'little'))
def be(m,a,v,n=4):m.write(a,(v&((1<<(8*n))-1)).to_bytes(n,'big'))
def arity(a,values,memory):return ARITY[a]
def dynamic_callbacks(v):return {}
def expected_reads(a,v):return []
def cases(a):
 if a==0x208ca9c:
  return[dict(state=s,bad=b)for s,b in [(s,0)for s in range(12)]+[(4,b)for b in [1,2,3]]]
 if a==0x208cbc4:return[dict(known=k,scav=s,flag=f,urgent=u,target=t)for k,s,f,u,t in [(0,0,0x12,0,0x0a000001),(0,1,0x12,1,0x0a000001),(1,1,4,0xffff,0x0a000001),(1,0,0xff,0xffff,0),(0,1,0x10,0xffff,0),(0,0,0,1,0)]]
 if a==0x208cc24:return[dict(flag=f,length=n,sequence=s,ack=q,urgent=u)for f,n,s,q,u in [(0,0,0,0,0),(1,0,0xffffffff,0,1),(2,8,0xffffffff,0,0xffff),(3,8,0xfffffff0,1,0),(0x10,8,1,0xffffffff,0xffff),(0x12,0,0,0x12345678,1)]]
 if a==0x208ccec:return[dict(sequence=s,tick=t,mss=m)for s,t,m in [(0,0,536),(0xffffffff,0x123456789abc,1460),(0x12345678,0xffffffffffff,0)]]
 if a==0x208cd80:return[dict(found=f,state=s,sequence=n)for f,s,n in [(0,0,0)]+[(1,s,0 if s==3 else 0xffffffff)for s in range(12)]]
 if a==0x208cdd0:return[dict(valid=v,specific=s,first=f,second=z)for v,s,f,z in [(0,0,0,0),(1,1,0,0),(1,0,1,0),(1,0,0,1),(1,0,0,0)]]
 if a==0x208ce58:return[dict(found=f,state=s,blocked=b,afteryield=y)for f,s,b,y in [(0,0,0,-1),(1,1,0,-1),(1,2,0,-1),(1,2,1,-1),(1,2,2,-1),(1,2,1,9)]]
 if a==0x208cef0:
  base=dict(found=1,state=4,length=0,flag=0,capacity=64,used=0,blocked=0,sequence=100,ackno=100,oldremote=10,remote=11,header=20)
  variations=[dict(found=0),*[dict(state=s)for s in range(12)],dict(state=3,flag=1,blocked=1),dict(state=4,flag=1,blocked=2),dict(length=8,blocked=2),dict(length=8,flag=1,blocked=2),dict(length=64,capacity=8,flag=1,blocked=2),dict(length=8,capacity=0,flag=1,blocked=2),dict(length=8,used=4,capacity=16,header=24),dict(state=7,length=3,flag=1,blocked=2),dict(state=8,length=3),dict(state=6,blocked=2),dict(state=9,blocked=2),dict(ackno=99),dict(sequence=0xffffffff,ackno=0xffffffff,length=1,flag=1),dict(oldremote=0xfffffff0,remote=16),dict(oldremote=16,remote=0x80000010),dict(length=0,oldremote=11,remote=10)]
  return[base|v for v in variations]
 raise ValueError('Unowned CPS TCP model')

def initial(a,v):
 m=Memory()
 for at,n in [(A,2048),(B,2048),(SOC,100),(RECV,256),(THREADINFO,12),(SCAV,1),(RESET,168)]:m.add(at,n)
 m.write(A,bytes((i*7+3)&255 for i in range(2048)));m.write(B,bytes((i*11+5)&255 for i in range(2048)));m.write(RESET,bytes([0x55])*168);m.write(RECV,bytes([0x66])*256)
 be(m,A+12,0x0a987654);be(m,A+16,0x0a123456);be(m,B,5000,2);be(m,B+2,6000,2);be(m,B+4,v.get('sequence',100));be(m,B+8,v.get('remote',v.get('ack',11)));number(m,B+12,(v.get('header',20)//4)<<4,1);number(m,B+13,v.get('flag',0),1);be(m,B+14,0x4321,2)
 number(m,SOC,THREAD);number(m,SOC+4,v.get('blocked',0));number(m,SOC+8,v.get('state',4),1);number(m,SOC+10,6000,2);number(m,SOC+24,5000,2);number(m,SOC+28,0x0a987654);number(m,SOC+36,v.get('ackno',100));number(m,SOC+40,v.get('sequence',100));number(m,SOC+48,v.get('oldremote',10));number(m,SOC+60,v.get('capacity',64));number(m,SOC+64,RECV);number(m,SOC+68,v.get('used',0));number(m,THREADINFO+4,SCAV if v.get('scav')else THREAD)
 if a==0x208ca9c:
  if v['bad']==1:number(m,SOC+10,6001,2)
  if v['bad']==2:number(m,SOC+24,5001,2)
  if v['bad']==3:number(m,SOC+28,0x0a010203)
  args=[A,B,SOC]
 elif a==0x208cbc4:args=[SOC,v['flag'],v['urgent']]
 elif a==0x208cc24:args=[A,B,v['length'],v['urgent']]
 elif a==0x208ccec:args=[A,B,SOC]
 elif a==0x208cd80:args=[A,B,8]
 elif a==0x208cdd0:
  if not v['valid']:be(m,A+12,0)
  args=[A,B,8]
 elif a==0x208ce58:args=[A,B,8]
 elif a==0x208cef0:args=[A,B,v['length']]
 else:raise ValueError('Unowned CPS TCP initialization')
 return m,args

def effect(a,values,m,v):
 normalized=list(values)
 if a in [DISABLE,RESTORE]:return 0x80,normalized
 if a==COPY:m.write(values[1],m.read(values[0],values[2]));return 0,normalized
 if a==FILL:m.write(values[0],bytes([values[1]&255])*values[2]);return 0,normalized
 if a==TICK:return v['tick'],normalized
 if a==YIELD:
  if v.get('afteryield',-1)>=0:number(m,SOC+8,v['afteryield'],1)
  return 0,normalized
 if a==WAKE:return 0,normalized
 if a==0x208cbb0:return v['known'],normalized
 if a==0x208c55c:return 0,normalized+[m.read(values[2],100).hex()]
 if a==0x208bc18:return v['target'],normalized
 if a==0x208bf98:return 0,normalized
 if a==0x208cbc4:return 0,normalized+[m.read(values[0],100).hex()]
 if a==0x208cb5c:number(m,values[1]+46,v.get('mss',1460),2);return 0,normalized
 if a==0x208cb1c:return SOC if v['found']else 0,normalized
 if a==0x208ccec:return 0,normalized+[m.read(values[2],100).hex()]
 if a==0x208cc24:return 0,normalized
 if a==0x208c97c:return int(values[0]not in [0,0xffffffff]and values[1]not in [0,0xffffffff]),normalized
 if a==0x208cd80:return v['specific'],normalized
 if a==0x208ca18:
  count=getattr(m,'listenerCount',0);m.listenerCount=count+1;return SOC if(v['first']if count==0 else v['second'])else 0,normalized
 if a in [0x208cc0c,0x208cc18]:return 0,normalized+[m.read(values[0],100).hex()]
 raise ValueError(('Unmodeled CPS TCP provider',hex(a)))

def model(a,v):
 m,args=initial(a,v);calls=[];result=0;contract='void'
 def call(at,*values):
  answer,normalized=effect(at,[x&0xffffffff for x in values],m,v);calls.append((hex(at),normalized));return answer
 def wake(kind):
  if r32(m,SOC+4)==kind:number(m,SOC+4,0);call(WAKE,r32(m,SOC))
 if a==0x208ca9c:result=int(v['state']not in [10,11]and v['bad']==0);contract='word'
 elif a==0x208cbc4:
  if call(0x208cbb0,0x0a987654)or not v['scav']:call(0x208c55c,0,0,SOC,v['flag'],v['urgent'])
  else:call(0x208bf98,call(0x208bc18,0x0a987654))
 elif a==0x208cc24:
  call(FILL,RSOC,0,100);number(m,RSOC+10,6000,2);number(m,RSOC+24,5000,2);number(m,RSOC+28,0x0a987654)
  if v['flag']&0x10:number(m,RSOC+40,v['ack']);call(0x208cbc4,RSOC,4,v['urgent'])
  else:number(m,RSOC+40,0);number(m,RSOC+36,v['sequence']+v['length']+int(bool(v['flag']&3)));call(0x208cbc4,RSOC,0x14,v['urgent'])
 elif a==0x208ccec:
  number(m,SOC+8,3,1);number(m,SOC+16,call(TICK)>>16);number(m,SOC+20,0x0a123456);number(m,SOC+24,5000,2);number(m,SOC+28,0x0a987654);number(m,SOC+36,v['sequence']+1);call(0x208cb5c,B,SOC);call(0x208cbc4,SOC,0x12,0)
 elif a==0x208cd80:
  found=call(0x208cb1c,A,B);result=int(bool(found));contract='word'
  if found:
   if v['state']==1:call(0x208ccec,A,B,SOC)
   elif v['state']in [3,4]:number(m,SOC+40,v['sequence']-1);call(0x208ccec,A,B,SOC)
   else:call(0x208cc24,A,B,8,0)
 elif a==0x208cdd0:
  source=0x0a987654 if v['valid']else 0
  if call(0x208c97c,source,0x0a123456)and not call(0x208cd80,A,B,8):
   found=call(0x208ca18,A,B)
   if found:call(0x208ccec,A,B,found)
   else:
    call(YIELD);found=call(0x208ca18,A,B)
    if found:call(0x208ccec,A,B,found)
 elif a==0x208ce58:
  found=call(0x208cb1c,A,B)
  if not found or v['state']!=2:call(0x208cc24,A,B,8,0)
  else:
   call(YIELD);number(m,SOC+36,101);number(m,SOC+48,11);number(m,SOC+44,0x4321,2);call(0x208cb5c,B,SOC);call(0x208cc0c,SOC,0);number(m,SOC+8,4,1);wake(1)
 elif a==0x208cef0:
  if not call(0x208cb1c,A,B):call(0x208cc24,A,B,v['length'],0)
  else:
   delta=(v['remote']-v['oldremote'])&0xffffffff
   if 0<delta<0x80000000:number(m,SOC+48,v['remote'])
   if v['state']==4 and v['ackno']!=v['sequence']:call(0x208cc0c,SOC,0)
   else:
    number(m,SOC+44,0x4321,2);state,n,flag=v['state'],v['length'],v['flag']
    if state in [0,2]:call(0x208cc24,A,B,n,0)
    elif state in [3,4]:
     if state==3:number(m,SOC+8,4,1);wake(1)
     if state==4 or n:
      number(m,SOC+52,r32(m,SOC+52)+1);free=v['capacity']-v['used'];fits=n<=free;n=min(n,free)
      if n:
       saved=call(DISABLE);call(COPY,B+v['header'],RECV+v['used'],n);number(m,SOC+68,v['used']+n);number(m,SOC+36,v['ackno']+n);call(RESTORE,saved);wake(2)
      if fits and flag&1:
       number(m,SOC+8,6,1);number(m,SOC+36,r32(m,SOC+36)+1);call(0x208cc18,SOC,0)
       if n==0:wake(2)
      elif n:call(0x208cc0c,SOC,0)
    elif state in [7,8]:
     if flag&1:number(m,SOC+36,v['ackno']+n+1);call(0x208cc0c,SOC,0);number(m,SOC+8,0,1);wake(2)
     else:
      if n:number(m,SOC+36,v['ackno']+n);call(0x208cc0c,SOC,0)
      number(m,SOC+8,8,1)
    elif state in [6,9]:number(m,SOC+8,0,1);wake(2)
    else:
     if flag&1:number(m,SOC+36,v['ackno']+1)
     call(0x208cc0c,SOC,0)
    call(YIELD)
 else:raise ValueError('Unowned CPS TCP result')
 return{at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
