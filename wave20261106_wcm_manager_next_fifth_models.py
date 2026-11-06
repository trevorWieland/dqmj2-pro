import itertools
import wave20261106_wcm_manager_next_fourth_models as P
from wave20261106_wcm_manager_next_fourth_models import WORK,CONFIG,A,B,BUFFER,GLOBAL,INDEX,RSSI,STOP,SP,CALLBACK,DISABLE,RESTORE,DIV,RET64,RELIABLE,OBSERVED,STATUS,EVENT,RX,BSS,WEP,READ_ONLY,INPUT_BSS

CPS=0x21cfcb8
EXTRA=0x22e0000
LENGTH=0x22e1000
NODES=[BUFFER+12+i*208 for i in range(3)]
ARITY=dict(P.ARITY)
ARITY.update({0x2013288:3,0x208b35c:1,0x208b2c0:0,0x208b338:0,0x2008ca4:3,0x208b3d8:1,0x208b72c:2,0x208b6e0:1,0x208b70c:1,0x2013328:4})


def cases(a):
 if a==0x208ab60:return [dict(phase=p,err=0,state=s,aid=1,provider=2)for p,s in itertools.product(range(15),[6,8,9,26])]+[dict(phase=p,err=0,state=7,aid=i,provider=r)for p,i,r in itertools.product([3,8,9,12],[0,1,2007,2008],[0,2,3,8])]+[dict(phase=9,err=e,state=0xffff,aid=1,provider=2)for e in [0,1,3,4,6,11,12,0xffff]]
 if a==0x208b260:return [dict(existing=e,lock=l,game=g,found=f,allocate=n,exchange=x,oldest=o)for e,l,g,f,n,x,o in [(0,0,0,0,0,0,0),(1,1,0,0,0,0,0),(1,0,1,0,0,0,0)]+[(1,0,0,f,n,x,o)for f,n,x,o in itertools.product([0,1],[0,1],[0,1],[0,1])]]
 if a==0x208b2c0:return [dict(blocks=n,count=c,occupied=o,buffer=b)for n,c,o,b in [(n,c,o,1)for n,c,o in itertools.product(range(4),range(5),range(8))]+[(1,0,0,0)]]
 if a==0x208b35c:return [dict(blocks=n,target=t,null=x,buffer=b)for n,t,x,b in [(n,t,0,1)for n,t in itertools.product(range(4),[-1,0,1,2])]+[(2,0,1,1),(2,0,0,0)]]
 if a==0x208b3d8:return [dict(blocks=n,node=t,buffer=b)for n,t,b in [(n,t,1)for n,t in itertools.product(range(4),[-2,-1,0,1,2])if t<0 or t<n]+[(2,-1,0)]]
 if a==0x208b498:return [dict(existing=e,phase=p,resetting=z,locked=l,provider=r)for e,p,z,l,r in [(0,9,0,1,2)]+[(1,p,z,l,r)for p,z,l,r in itertools.product([3,9],[0,1,255],[0,1],[0,2,3,8])]]
 if a in [0x208b4ec,0x208b524]:return [dict(existing=e,phase=p,resetting=z,length=x)for e,p,z,x in itertools.product([0,1],[3,9],[0,1,255],[0,1])]
 if a==0x208b568:return [dict(callback=c)for c in [0,0x2400081,0x2400080,0xffffffff]]
 raise ValueError('Unowned WCM table/CPSIF model')


def initial(a,v):
 m,args=P.initial(a,v);m.regions[EVENT]=bytearray(28);m.number(EVENT+2,v.get('err',0),2);m.number(EVENT+8,v.get('state',0),2);m.number(EVENT+10,v.get('aid',0),2);m.number(EVENT+14,18,2);m.regions[BUFFER]=bytearray(12+3*208);m.add(EXTRA,208,0x63);m.add(LENGTH,2,0x77);m.add(CPS,44,0x55);m.number(WORK+0x226a,v.get('lock',0),1);m.number(WORK+0x2278,v.get('exchange',0));m.number(WORK+0x2270,BUFFER if v.get('buffer',1)else 0);m.number(WORK+0x2274,12+208*v.get('blocks',2));m.number(INPUT_BSS+60,v.get('game',0),2);m.number(BSS+10,31,2)
 n=v.get('blocks',2);m.number(BUFFER,v.get('count',n));m.number(BUFFER+4,NODES[0]if n else 0);m.number(BUFFER+8,NODES[n-1]if n else 0)
 for i,at in enumerate(NODES):
  m.number(at,1 if i<n else 0,1);m.number(at+4,i);m.number(at+8,NODES[i-1]if 0<i<n else 0);m.number(at+12,NODES[i+1]if i+1<n else 0);m.write(at+20,bytes([i+1]*6))
 if a==0x208b2c0:
  for i,at in enumerate(NODES):m.number(at,(v['occupied']>>i)&1,1)
 if a==0x208b35c:m.write(A,bytes([v['target']+1]*6)if v['target']>=0 else bytes([0xff]*6))
 if a==0x208b260:args=[INPUT_BSS,0xffff]
 elif a==0x208b35c:args=[0 if v['null']else A]
 elif a==0x208b3d8:args=[0 if v['node']==-2 else EXTRA if v['node']==-1 else NODES[v['node']]]
 elif a==0x208b524:args=[LENGTH if v['length']else 0]
 elif a==0x208b568:args=[v['callback']]
 elif a==0x208ab60:args=[EVENT]
 else:args=[]
 return m,args


def arity(a,values,memory):return ARITY[a]


def effect(a,values,memory,v):
 if a==0x2013288 or a==0x2013328:return v.get('provider',2),list(values)
 if a==0x208b35c:return NODES[0]if v.get('found')else 0,list(values)
 if a==0x208b2c0:return NODES[1]if v.get('allocate')else 0,list(values)
 if a==0x208b338:return NODES[0]if v.get('oldest')else 0,list(values)
 if a==0x2008ca4:memory.write(values[1],memory.read(values[0],values[2]));return 0,list(values)
 if a==0x208b3d8 or a==0x208b70c:return 0,list(values)
 if a==0x208b72c:return int(memory.read(values[0],6)==memory.read(values[1],6)),list(values)
 if a==0x208b6e0:return v['locked'],list(values)
 return P.effect(a,values,memory,v)


def dynamic_callbacks(v):return {}


def expected_reads(a,v):return []


def model(a,v):
 m,args=initial(a,v);calls=[];contract='void';result=0;p=v.get('phase',1);err=v.get('err',0);r=v.get('provider',2)
 def call(at,*values):calls.append((hex(at),list(values)))
 def phase(n):
  call(0x208a5ac,n)
  if m.value(WORK+0x2260)!=11:m.number(WORK+0x2260,n)
 def notice(n,arg0,arg1,line):call(0x208a550,n,arg0,arg1,line);m.number(WORK+0x2280,0,2)
 def get():call(0x208a31c)
 if a==0x208ab60:
  if err==0:
   state=v['state']
   if state in [8,9]:
    if p==10:m.number(WORK+0x2282,0,2);phase(12)
    elif p==8:phase(12)
    elif p==9:m.number(WORK+0x2282,0,2);m.number(WORK+0x2280,6,2);call(0x208a698)
    elif p==12:call(0x208a698)
   elif state==7:
    if p==12:phase(8);call(0x208a698)
    elif 1<=v['aid']<=2007:
     m.number(WORK+0x2282,v['aid'],2);call(0x2013288,0x208ad95,WORK+0x1500,0x620)
     if r==8:phase(12);notice(1,BSS,0,2029)
     elif r!=2:phase(11);notice(7,BSS,0,2038)
    else:call(0x208a698)
   elif state not in [6,26]:phase(11);notice(7,BSS,state,2052)
  elif err in [1,6,11,12]:
   if err==1:m.number(WORK+0x22f8,18,2)
   phase(8);call(0x208a698)
  else:phase(11);notice(7,BSS,0,2075)
 elif a==0x208b260:
  get()
  if v['existing']and not v['lock']and not v['game']:
   call(0x208b35c,INPUT_BSS+4);node=NODES[0]if v['found']else 0
   if not node:call(0x208b2c0);node=NODES[1]if v['allocate']else 0
   if not node and v['exchange']==1:call(0x208b338);node=NODES[0]if v['oldest']else 0
   if node:m.number(node+2,0xffff,2);call(0x2008ca4,INPUT_BSS,node+16,192);m.write(node+16,m.read(INPUT_BSS,192));call(0x208b3d8,node)
 elif a==0x208b2c0:
  contract='word';get();size=12+208*v['blocks']
  if v['buffer']and size>12:
   call(DIV,size-12,208);count=v['count'];n=v['blocks']
   if n>count:
    for i in range(n):
     result=NODES[i]
     if not(v['occupied']>>i)&1:break
    else:i=n
    if i<n:
     node=NODES[i];m.number(node,1,1);m.number(node+4,count);m.number(node+12,0);old=m.value(BUFFER+8);m.number(node+8,old);m.number(BUFFER+8,node)
     if old:m.number(old+12,node)
     else:m.number(BUFFER+4,node)
     m.number(BUFFER,count+1)
 elif a==0x208b35c:
  contract='word';get()
  if not v['null']and v['buffer']and v['blocks']>0:
   for i in range(v['blocks']):
    call(0x208b72c,NODES[i]+20,A)
    if i==v['target']:result=NODES[i];break
 elif a==0x208b3d8:
  get();node=args[0];n=v['blocks']
  if node and v['buffer']and n>0:
   if node in NODES[:n]:
    previous=m.value(node+8);following=m.value(node+12)
    if previous:m.number(previous+12,following)
    else:m.number(BUFFER+4,following)
    if following:m.number(following+8,previous)
    else:m.number(BUFFER+8,previous)
   old=m.value(BUFFER+8);m.number(node+12,0);m.number(node+8,old);m.number(BUFFER+8,node)
   if old:m.number(old+12,node)
   else:m.number(BUFFER+4,node)
   if node not in NODES[:n]:m.number(node+4,n);m.number(BUFFER,n+1)
 elif a==0x208b498:
  get()
  if v['existing']and p==9 and v['resetting']!=1:
   call(0x208b6e0,CPS+12)
   if v['locked']:
    call(0x2013328,0x208b6d1,BSS+4,WORK+0xf00,0)
    if r!=2:call(0x208b70c,CPS+12)
 elif a in [0x208b4ec,0x208b524]:
  contract='word';get();call(DISABLE);valid=v['existing']and p==9 and v['resetting']==0;result=(BSS+4 if a==0x208b4ec else BSS+12)if valid else 0;call(RESTORE,0x80)
  if a==0x208b524 and v['length']:m.number(LENGTH,31 if valid else 0,2)
 elif a==0x208b568:call(DISABLE);m.number(CPS+40,v['callback']);call(RESTORE,0x80)
 else:raise ValueError('Unowned WCM table/CPSIF function')
 return {at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
