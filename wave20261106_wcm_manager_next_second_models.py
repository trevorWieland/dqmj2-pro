import itertools
import wave20261106_wcm_manager_next_first_models as P
from wave20261106_wcm_manager_next_first_models import WORK,CONFIG,A,B,BUFFER,GLOBAL,INDEX,RSSI,STOP,SP,CALLBACK,DISABLE,RESTORE,DIV,RET64,RELIABLE,OBSERVED

STATUS=0x22c0000
EVENT=0x22c0100
ARITY=dict(P.ARITY,**{})
ARITY.update({0x208a328:2,0x20115b4:2,0x2012290:0,0x20117c4:0,0x2011f14:1,0x2012630:1,0x2012724:1,0x20126a4:1,0x20133f4:1,0x2011e90:0,0x20072d0:2,0x208a698:0})
RETURNS={0x20115b4:('init',0),0x2012290:('allowed',0x3ffe),0x20117c4:('finish',0),0x2011f14:('indication',0),0x2012630:('enable',2),0x2012724:('poweroff',2),0x20126a4:('disable',2),0x20133f4:('enddcf',2),0x20127ec:('reset',2)}


def cases(a):
 if a==0x2089ba0:
  out=[dict(existing=e,phase=p)for e,p in itertools.product([0,1],range(15))]
  out += [dict(existing=1,phase=1,**v)for v in [dict(init=x)for x in [1,2,3,4,6,8,0xffff]]+[dict(allowed=0,finish=x)for x in [0,1,2,8]]+[dict(indication=x)for x in [1,2,3,8]]+[dict(enable=x)for x in [0,1,2,3,4,8,0xffff]]]
  return out
 if a==0x2089cf4:return [dict(existing=e,phase=p,poweroff=w)for e,p,w in [(0,3,2)]+[(1,x,2)for x in range(15)]+[(1,3,x)for x in [0,1,3,4,8,0xffff]]]
 if a==0x208a060:return [dict(existing=e,phase=p,resetting=r,enddcf=w)for e,p,r,w in [(0,9,0,2)]+[(1,x,0,2)for x in range(15)]+[(1,9,r,w)for r,w in itertools.product([0,1,255],[0,1,2,3,4,8,0xffff])]]
 if a==0x208a114:return [dict(existing=e,phase=p,resetting=r,state=s,finish=w,disable=w,poweroff=w,reset=w)for e,p,r,s,w in [(0,3,0,0,0)]+[(1,p,0,0,0)for p in range(15)]+[(1,p,r,s,w)for p,r,s,w in itertools.product([3,9,12],[0,1],[0,1,2,3,0xffff],[0,2,3,8])]]
 if a==0x208a6d8:return [dict(phase=p,err=e,state=s,reason=r)for p,e,s,r in [(p,8,22,37)for p in range(15)]+[(9,e,s,r)for e,s,r in [(0,22,37),(8,21,37),(8,22,36),(8,22,38),(0xffff,22,37)]]]
 if a==0x208ab0c:return [dict(err=e)for e in [0,1,2,3,4,8,0xffff]]
 raise ValueError('Unowned lifecycle model')


def initial(a,v):
 m,args=P.initial(a,v);m.add(STATUS,2);m.add(EVENT,8);m.number(STATUS,v.get('state',0),2);m.number(EVENT+2,v.get('err',0),2);m.number(EVENT+4,v.get('state',0),2);m.number(EVENT+6,v.get('reason',0),2);m.number(WORK+0x226c,0x12345678);m.number(WORK+0x2280,0x5555,2)
 if a==0x2089ba0:args=[CONFIG,0x12345679]
 if a in [0x208a6d8,0x208ab0c]:args=[EVENT]
 return m,args


def arity(a,values,memory):return ARITY[a]


def effect(a,values,memory,v):
 if a==0x2011e90:return STATUS,list(values)
 if a in RETURNS:
  key,default=RETURNS[a];return v.get(key,default),list(values)
 if a in [0x208a328,0x20072d0,0x208a698]:return 0,list(values)
 return P.effect(a,values,memory,v)


def dynamic_callbacks(v):return {}


def expected_reads(a,v):return []


def model(a,v):
 m,args=initial(a,v);calls=[];result=0;contract='word'
 def call(at,*values):calls.append((hex(at),list(values)))
 def phase(n):call(0x208a5ac,n)
 def notice(n,line):call(0x208a550,n,0,0,line)
 def wm(at):call(at,0x208a731);key,default=RETURNS[at];return v.get(key,default)
 def notify(n):m.number(WORK+0x2280,n,2)
 if a in [0x208a6d8,0x208ab0c]:
  contract='void'
  if a==0x208a6d8:
   if v['err']==8 and v['state']==22 and v['reason']==37:
    if v['phase']in [8,10]:phase(12)
    elif v['phase']in [9,12]:call(0x208a698)
  elif v['err']==0:phase(3);notice(0,1923)
  elif v['err']==1:call(0x208a698)
  else:phase(11);notice(7,1939)
  return {at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
 call(DISABLE);p=v.get('phase',1)
 if not v.get('existing',1):result=1
 elif a==0x2089ba0:
  if p==2:result=2
  elif p==3:result=0
  elif p!=1:result=1
  else:
   call(0x208a328,CONFIG,0x12345679);call(0x20115b4,WORK,0x5678);r=v.get('init',0)
   if r!=0:
    if r==4:result=5
    else:phase(11);result=7
   else:
    call(0x2012290)
    if v.get('allowed',0x3ffe)==0:
     call(0x20117c4)
     if v.get('finish',0)==0:result=5
     else:phase(11);result=7
    else:
     call(0x2011f14,0x208a6d9)
     if v.get('indication',0)!=0:phase(11);result=7
     else:
      r=wm(0x2012630)
      if r==2:phase(2);notify(1);result=3
      elif r==8:phase(12);result=1
      else:phase(11);result=7
 elif a==0x2089cf4:
  if p==4:result=2
  elif p==1:result=0
  elif p!=3:result=1
  else:
   r=wm(0x2012724)
   if r==2:phase(4);notify(2);result=3
   elif r==8:result=4
   else:phase(11);result=7
 elif a==0x208a060:
  if p==10:result=2
  elif p==3:result=0
  elif p!=9:result=1
  elif v.get('resetting',0)==1:phase(10);notify(6);result=3
  else:
   call(0x20133f4,0x208ae51);r=v.get('enddcf',2)
   if r==2:phase(10);notify(6);result=3
   elif r==8:result=4
   else:phase(11);result=7
 elif a==0x208a114:
  if p==13:result=2
  elif p==1:result=0
  elif p==6:phase(13);notify(9);result=3
  elif p not in [3,9,12]:result=1
  elif v.get('resetting',0)==1:phase(13);notify(9);result=3
  else:
   call(0x2011e90);call(0x20072d0,STATUS,2);state=v.get('state',0);done=False
   if state==0:
    call(0x20117c4);r=v.get('finish',0)
    if r==0:phase(1);notify(0);result=0;done=True
   elif state==1:r=wm(0x20126a4)
   elif state==2:r=wm(0x2012724)
   else:m.number(WORK+0x226b,1,1);call(0x20127ec,0x208af1d);r=v.get('reset',2)
   if not done:
    if r==2:phase(13);notify(9);result=3
    elif r==8:result=4
    else:phase(11);result=7
 else:raise ValueError('Unowned lifecycle model')
 call(RESTORE,0x80);return {at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
