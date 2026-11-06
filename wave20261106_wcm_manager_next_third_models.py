import itertools
import wave20261106_wcm_manager_next_second_models as P
from wave20261106_wcm_manager_next_second_models import WORK,CONFIG,A,B,BUFFER,GLOBAL,INDEX,RSSI,STOP,SP,CALLBACK,DISABLE,RESTORE,DIV,RET64,RELIABLE,OBSERVED,STATUS,EVENT

RX=0x22c1000
BSS=WORK+0x2140
WEP=WORK+0x2200
COMMON=0x208a731
CONNECT=0x208ab61
ARITY=dict(P.ARITY)
ARITY.update({0x20126e4:1,0x20141b0:2,0x201407c:4,0x2012cb8:5,0x2012d84:2,0x208b7f0:1,0x208b474:1,0x208a3e0:3,0x2012b28:2})


def cases(a):
 if a==0x208a730:return [dict(api=i,err=0,provider=r,notify=n)for i,r,n in itertools.product([3,4,5,6,29,25,39,0,0xffff],[0,2,3,8],[0,5])]+[dict(api=3,err=e,notify=n)for e,n in itertools.product([1,3,4,0xffff],[0,5])]+[dict(api=39,err=0,provider=2,option=o,notify=5)for o in [0,0x30000,0xc0000,0xf0000]]
 if a==0x208ad04:return [dict(phase=p,err=e)for p,e in itertools.product([0,3,9,10,11,12],[0,1,2,3,4,8,0xffff])]
 if a==0x208ad94:return [dict(phase=p,err=e,state=s,rssi=r)for p,e,s,r in [(p,0,14,0)for p in [0,3,9,12]]+[(3,0,15,r)for r in [0,1,127,255]]+[(3,0,s,0)for s in [0,13,16,0xffff]]+[(3,e,14,0)for e in [1,3,4,8,0xffff]]]
 if a==0x208ae50:return [dict(phase=p,err=e,provider=r)for p,e,r in itertools.product([0,3,9,10,11,12],[0,1,3,4,8,0xffff],[0,2,3,8])]
 if a==0x208af1c:return [dict(phase=p,err=e,provider=2,wlstatus=0,support=0)for p,e in itertools.product(range(15),[0,1,4,0xffff])]+[dict(phase=8,err=0,provider=r,wlstatus=w,support=s,option=o)for r,w,s,o in [(r,w,s,0)for r,w,s in itertools.product([0,2,3,8],[0,18,19],[0,0x20,0x24])]+[(2,18,0,o)for o in [0x30000,0xc0000,0xf0000]]]+[dict(phase=13,err=0,provider=r)for r in [0,2,3,8]]
 if a==0x2089da4:return [dict(existing=e,phase=p,provider=r,count=c)for e,p,r,c in [(0,3,2,0)]+[(1,p,2,0)for p in range(15)]+[(1,3,r,c)for r,c in itertools.product([0,1,2,3,4,8,0xffff],[0,0xffffffff])]]
 raise ValueError('Unowned WCM callback model')


def initial(a,v):
 m,args=P.initial(a,v);m.regions[EVENT]=bytearray(12);m.number(EVENT,v.get('api',0),2);m.number(EVENT+2,v.get('err',0),2);m.number(EVENT+4,v.get('state',0),2);m.add(RX,0x620);m.number(RX+14,v.get('rssi',0)<<8,2);m.number(EVENT+8,RX);m.number(WORK+0x2280,v.get('notify',0),2);m.number(WORK+0x2250,3,1);m.number(WORK+0x2251,2,1);m.number(WORK+0x22f8,v.get('wlstatus',0),2);m.number(BSS+48,v.get('support',0),2);m.number(WORK+0x2284,v.get('count',0));m.number(WORK+0x2288,RX);m.number(WORK+0x228c,0x620,2)
 args=[A,BUFFER,v.get('option',0xdeadbeef)]if a==0x2089da4 else[EVENT]
 return m,args


def arity(a,values,memory):return ARITY[a]


def effect(a,values,memory,v):
 if a in [0x20126e4,0x20141b0,0x201407c,0x2012cb8,0x2012d84,0x2012b28,0x20117c4,0x20126a4,0x2012724]:return v.get('provider',2),list(values)
 if a in [0x208b7f0,0x208b474,0x208a3e0]:return 0,list(values)
 return P.effect(a,values,memory,v)


def dynamic_callbacks(v):return {}


def expected_reads(a,v):return []


def model(a,v):
 m,args=initial(a,v);calls=[];result=0;contract='void';p=v.get('phase',1);err=v.get('err',0);r=v.get('provider',2)
 def call(at,*values):calls.append((hex(at),list(values)))
 def phase(n):call(0x208a5ac,n)
 def notice(n,arg0,arg1,line):call(0x208a550,n,arg0,arg1,line)
 def connect():
  option=v.get('option',0);call(0x2012cb8,CONNECT,BSS,0,0 if option&0x30000==0x30000 else 1,1 if option&0xc0000==0xc0000 else 0)
 if a==0x208a730:
  data=BSS if v.get('notify',0)==5 else 0;api=v.get('api',0)
  if err==0:
   if api==4:
    call(0x20117c4)
    if r==0:phase(1);notice(0,0,0,1635)
    else:phase(11);notice(7,0,0,1644)
   elif api==5:phase(3);notice(0,0,0,1651)
   else:
    if api==3:call(0x20126e4,COMMON)
    elif api==6:call(0x20126a4,COMMON)
    elif api==29:call(0x20141b0,COMMON,0)
    elif api==25:call(0x201407c,COMMON,3,2,WEP)
    elif api==39:connect()
    else:r=20
    if r==8:phase(12);notice(1,data,0,1711)
    elif r!=2:phase(11);notice(7,data,0,1720)
  elif err==1:phase(12);notice(1,data,0,1758)
  else:phase(11);notice(7,data,0,1768)
 elif a==0x208ad04:
  if err==0:
   if p==12:phase(10);call(0x208a698)
   else:m.number(WORK+0x2282,0,2);phase(3);notice(0,BSS,0,2109)
  elif err in [1,3]:phase(10);call(0x208a698)
  else:phase(11);notice(7,BSS,0,2127)
 elif a==0x208ad94:
  if err==0:
   state=v['state']
   if state==14:
    if p==12:phase(8);call(0x208a698)
    else:phase(9);notice(0,BSS,0,2162)
   elif state==15:call(0x208b7f0,v['rssi']);call(0x20072d0,RX,0x620);call(0x208b474,RX)
   else:phase(11);notice(7,BSS,state,2177)
  else:phase(11);notice(7,BSS,0,2188)
 elif a==0x208ae50:
  if err==0:
   if p==12:phase(10);call(0x208a698)
   else:
    call(0x2012d84,0x208ad05,0)
    if r==8:phase(12);notice(1,BSS,0,2228)
    elif r==3:phase(10);call(0x208a698)
    elif r!=2:phase(11);notice(7,BSS,0,2240)
  elif err in [1,3]:phase(10);call(0x208a698)
  else:phase(11);notice(7,BSS,0,2259)
 elif a==0x208af1c:
  if err!=0:phase(11);notice(7,0,0,2400)
  else:
   m.number(WORK+0x226b,0,1);m.number(WORK+0x2282,0,2)
   if p in [5,6]:phase(3);notice(1,0,0,2293)
   elif p==7:phase(3);notice(0,0,0,2299)
   elif p==8:
    status=v.get('wlstatus',0);support=v.get('support',0);m.number(WORK+0x22f8,0,2)
    if status==18 and support&0x24!=0x24:
     m.number(BSS+48,support|0x24,2);connect()
     if r==8:phase(12);notice(1,BSS,status,2332)
     elif r!=2:phase(11);notice(7,BSS,status,2341)
    else:phase(3);notice(1,BSS,status,2349)
   elif p in [9,12]:phase(3);notice(0,BSS,1,2357)
   elif p==10:phase(3);notice(0,BSS,0,2364)
   elif p==13:
    call(0x2012724,COMMON)
    if r==8:phase(12);notice(1,0,0,2378)
    elif r!=2:phase(11);notice(7,0,0,2387)
   else:phase(11);notice(7,0,p,2393)
 elif a==0x2089da4:
  contract='word';call(DISABLE)
  if not v['existing']:result=1
  elif p in [5,6]:call(0x208a3e0,A,BUFFER,0xdeadbeef);result=2 if p==5 else 0
  elif p!=3:result=1
  else:
   call(0x208a3e0,A,BUFFER,0xdeadbeef);call(0x20072d0,RX,0x620);m.number(WORK+0x2284,(v['count']+1)&0xffffffff);call(0x2012b28,0x208a941,WORK+0x2288)
   if r==2:phase(5);m.number(WORK+0x2280,3,2);result=3
   elif r==8:result=4
   else:phase(11);result=7
  call(RESTORE,0x80)
 else:raise ValueError('Unowned WCM callback')
 return {at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
