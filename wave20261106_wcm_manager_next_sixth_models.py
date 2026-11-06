import itertools
import wave20261106_wcm_manager_next_fifth_models as P
from wave20261106_wcm_manager_next_fifth_models import WORK,CONFIG,A,B,BUFFER,GLOBAL,INDEX,RSSI,STOP,SP,CALLBACK,DISABLE,RESTORE,DIV,RET64,RELIABLE,OBSERVED,STATUS,EVENT,RX,BSS,WEP,READ_ONLY,CPS

HEADER=0x22e2000
BODY=0x22e3000
ARITY=dict(P.ARITY)
ARITY.update({0x200708c:1,0x2007110:1,0x20068d4:1})


def cases(a):
 if a!=0x208b580:raise ValueError('Unowned five-argument transmit model')
 return [dict(existing=e,post=p,phase=s,resetting=r,wm=w,result=z,headlen=h,bodylen=b,offset=o)for e,p,s,r,w,z,h,b,o in [(0,1,9,0,2,0,4,8,0),(1,0,9,0,2,0,4,8,0)]+[(1,1,s,r,2,0,4,8,0)for s,r in itertools.product(range(15),[0,1,255])]+[(1,1,9,0,w,z,4,8,0)for w,z in itertools.product([0,1,2,3,6,8,0xffff],[0,1,8,0xffff])]+[(1,1,9,0,2,0,h,b,o)for h,b,o in [(0,0,0),(0,1,0),(1,0,0),(1,1,0),(2,3,1),(31,32,1),(32,0,0),(1508,0,0),(0,1536,0),(768,768,0),(1,-1,0),(33,-1,0)]]]


def initial(a,v):
 m,args=P.initial(a,v);m.add(HEADER,1538);m.add(BODY,1538);m.write(HEADER,bytes((i*7+3)&255 for i in range(1538)));m.write(BODY,bytes((i*11+5)&255 for i in range(1538)));return m,[A,HEADER+v['offset'],v['headlen'],BODY+v['offset']if v['bodylen']else 0,v['bodylen']]


def arity(a,values,memory):return ARITY[a]


def effect(a,values,memory,v):
 if a==0x208a31c:
  n=getattr(memory,'getCalls',0);memory.getCalls=n+1
  return WORK if(v['existing']if n==0 else v['post'])else 0,list(values)
 if a in [0x200708c,0x2007110]:return 0,list(values)
 if a==0x20068d4:memory.write(CPS+36,v['result'].to_bytes(4,'little'));return 0,list(values)
 if a==0x2013328:return v['wm'],list(values)
 return P.effect(a,values,memory,v)


def dynamic_callbacks(v):return {}


def expected_reads(a,v):return []


def model(a,v):
 m,args=initial(a,v);calls=[];result=0
 def call(at,*values):calls.append((hex(at),list(values)))
 call(DISABLE);call(0x208a31c)
 if not v['existing']:result=0xffffffff
 else:
  call(0x200708c,CPS+12);call(0x208a31c)
  if not v['post']:result=0xffffffff
  elif v['phase']!=9 or v['resetting']==1:result=0xfffffffc
  else:
   h,b=v['headlen'],v['bodylen'];src=HEADER+v['offset'];call(0x2008e0c,src,WORK+0xf00,h);m.write(WORK+0xf00,m.read(src,h))
   if b>0:src=BODY+v['offset'];call(0x2008e0c,src,WORK+0xf00+h,b);m.write(WORK+0xf00+h,m.read(src,b))
   call(0x2013328,0x208b6a9,A,WORK+0xf00,(h+b)&0xffff)
   if v['wm']!=2:result=0xfffffffb
   else:call(0x20068d4,CPS+4);m.number(CPS+36,v['result']);result=h+b if v['result']==0 else 0xfffffffb
  call(0x2007110,CPS+12)
 call(RESTORE,0x80);return {at:bytes(raw)for at,raw in m.regions.items()},calls,'word',result&0xffffffff
