import itertools
import wave20261106_wcm_manager_next_third_models as P
from wave20261106_wcm_manager_next_third_models import WORK,CONFIG,A,B,BUFFER,GLOBAL,INDEX,RSSI,STOP,SP,CALLBACK,DISABLE,RESTORE,RET64,RELIABLE,OBSERVED,STATUS,EVENT,RX,BSS,WEP

DIV=0x2026350
ANY_BSSID=0x20dc3c8
ANY_SSID=0x20dc3d0
INPUT_BSS=0x22d0000
INPUT_WEP=0x22d1000
NODE=0x22d2000
READ_ONLY=[ANY_BSSID,ANY_SSID]
ARITY=dict(P.ARITY)
ARITY.update({DIV:2,0x2008e0c:3,0x2014200:5,0x20123d0:0,0x208a508:1,0x208a66c:1,0x208a690:1,0x208b260:2,0x208a57c:5,0x2012c78:1,0x208a31c:0,0x208b3a4:1,0x208a28c:1})


def option_update(old,value):
 mask=0
 for test,filter in [(0x8000,0x3ffe),(0x20000,0x10000),(0x80000,0x40000),(0x200000,0x100000),(0x800000,0x400000)]:
  if value&test:
   mask|=filter
   if test==0x8000 and not value&filter:value|=0xa082
 return ((old&~mask)|value)&0xffffffff


def cases(a):
 if a==0x2089ef8:return [dict(existing=e,phase=p,hasbss=b,haswep=w,mode=m,key=k,game=g,provider=r)for e,p,b,w,m,k,g,r in [(0,3,1,1,1,1,0,2)]+[(1,p,1,1,1,1,0,2)for p in range(15)]+[(1,3,b,w,m,k,g,r)for b,w,m,k,g,r in [(0,1,1,1,0,2),(1,1,1,1,1,2),(1,1,4,1,0,2),(1,1,1,4,0,2)]+[(1,w,m,2,0,r)for w,m,r in itertools.product([0,1],[0,1,3],[0,2,3,8])]]]
 if a==0x208a3e0:return [dict(bssid=b,essid=e,length=l,time=t,option=o,next=n)for b,e,l,t,o,n in [(b,e,l,t,0xdeadbeef,5)for b,e,l,t in itertools.product([0,1],[0,1,2],[0,1,31,32],[0,120])]]+[dict(bssid=1,essid=1,length=4,time=0,option=o,next=n)for o,n in itertools.product([0,0x300000],[1,13])]
 if a==0x208a940:return [dict(phase=p,err=e,state=5,found=0,provider=2,option=0,count=0,next=13)for p,e in itertools.product([0,3,5,6,7,11,12,13],[0,1,3,4])]+[dict(phase=6,err=0,state=s,found=f,provider=r,option=o,count=c,next=5)for s,f,r,o,c in [(s,f,r,0,0)for s,f,r in itertools.product([4,5],[0,1,2],[0,2,8])]+[(5,0,2,o,c)for o,c in itertools.product([0xc00000,0xc00002,0xc00082,0xc00000|0x3ffe],[0,1,2,0xffffffff])]]
 if a==0x208b154:return [dict(existing=e,buffer=b,size=n)for e,b,n in itertools.product([0,1],[0,1],[0,1,64,0xffffffff])]
 if a==0x208b1cc:return [dict(existing=e,lock=l,oldlock=o)for e,l,o in itertools.product([0,1],[0,1,0xffffffff],[0,1,255])]
 if a==0x208b224:return [dict(existing=e,index=i,found=f)for e,i,f in itertools.product([0,1],[0,1,0xffffffff],[0,1])]
 raise ValueError('Unowned WCM scan/AP model')


def initial(a,v):
 m,args=P.initial(a,v);m.regions[EVENT]=bytearray(112);m.number(EVENT+2,v.get('err',0),2);m.number(EVENT+8,v.get('state',0),2);m.number(EVENT+10,0x1001,2);m.number(EVENT+14,v.get('found',0),2);m.number(EVENT+16,INPUT_BSS);m.number(EVENT+20,INPUT_BSS);m.number(EVENT+80,3,2);m.number(EVENT+82,1,2)
 m.add(INPUT_BSS,192,0x33);m.number(INPUT_BSS+60,v.get('game',0),2);m.number(INPUT_BSS+46,0x18,2);m.add(INPUT_WEP,82,0x51);m.number(INPUT_WEP,v.get('mode',1),1);m.number(INPUT_WEP+1,v.get('key',1),1);m.add(NODE,208);m.add(ANY_BSSID,6,255);m.add(ANY_SSID,32,255);m.number(WORK+0x2268,v.get('time',0),2);m.number(WORK+0x226a,v.get('oldlock',0),1);m.number(WORK+0x2270,BUFFER if v.get('buffer',1)else 0);m.number(WORK+0x2274,v.get('size',64));m.number(WORK+0x2284,v.get('count',0));m.write(BUFFER,bytes([65]*128))
 if a==0x208a3e0:
  length=v['length'];m.write(BUFFER,bytes([65]*length+[0]*(128-length)))
 args={0x2089ef8:[INPUT_BSS if v.get('hasbss')else 0,INPUT_WEP if v.get('haswep')else 0,0xf80000],0x208a3e0:[A if v.get('bssid')else 0,BUFFER if v.get('essid')==1 else ANY_SSID if v.get('essid')==2 else 0,v.get('option',0)],0x208a940:[EVENT],0x208b1cc:[v.get('lock',0)],0x208b224:[v.get('index',0)]}.get(a,[])
 return m,args


def arity(a,values,memory):return ARITY[a]


def effect(a,values,memory,v):
 if a==DIV:return values[0]//values[1],list(values)
 if a==0x2008e0c:memory.write(values[1],memory.read(values[0],values[2]));return 0,list(values)
 if a==0x208a31c:return WORK if v.get('existing',1)else 0,list(values)
 if a==0x208b3a4:return NODE if v.get('found',0)else 0,list(values)
 if a==0x208a28c:
  old=int.from_bytes(memory.read(WORK+0x2264,4),'little');memory.write(WORK+0x2264,option_update(old,values[0]).to_bytes(4,'little'));return old,list(values)
 if a==0x208a508:return v.get('next',13),list(values)
 if a==0x208a66c:return values[0].bit_count(),list(values)
 if a==0x208a690:return 32-values[0].bit_length(),list(values)
 if a==0x20123d0:return 123,list(values)
 if a in [0x2014200,0x2012b28,0x2012c78]:return v.get('provider',2),list(values)
 if a==0x208a5ac:
  if int.from_bytes(memory.read(WORK+0x2260,4),'little')!=11:memory.write(WORK+0x2260,values[0].to_bytes(4,'little'))
  return 0,list(values)
 if a==0x208a550:memory.write(WORK+0x2280,bytes(2));return 0,list(values)
 if a in [0x208b260,0x208a57c]:return 0,list(values)
 return P.effect(a,values,memory,v)


def dynamic_callbacks(v):return {}


def expected_reads(a,v):return []


def model(a,v):
 m,args=initial(a,v);calls=[];result=0;contract='void';p=v.get('phase',1);r=v.get('provider',2)
 def call(at,*values):calls.append((hex(at),list(values)))
 def phase(n):
  call(0x208a5ac,n)
  if m.value(WORK+0x2260)!=11:m.number(WORK+0x2260,n)
 def notice(n,line):call(0x208a550,n,0,0,line);m.number(WORK+0x2280,0,2)
 def update(value):call(0x208a28c,value);m.number(WORK+0x2264,option_update(m.value(WORK+0x2264),value))
 def copy(src,dst,size):call(0x2008e0c,src,dst,size);m.write(dst,m.read(src,size))
 def fill(dst,size):call(0x2008d78,dst,0,size);m.write(dst,bytes(size))
 if a==0x2089ef8:
  contract='word';call(DISABLE)
  if not v['existing']:result=1
  elif p==8:result=2
  elif p==9:result=0
  elif p!=3 or not v['hasbss']or v['game']or(v['haswep']and(v['mode']>=4 or v['key']>=4)):result=1
  else:
   if v['haswep']:
    m.number(WORK+0x2250,v['mode'],1);m.number(WORK+0x2251,v['key'],1)
    if v['mode']==0:fill(WEP,80)
    else:copy(INPUT_WEP+2,WEP,80)
   else:fill(WEP,82)
   copy(INPUT_BSS,BSS,192);m.number(BSS+48,m.value(BSS+46,2)|3,2);update(0xf80000);call(0x2014200,0x208a731,0xffff,80,0xffff,0xffff)
   if r==2:phase(8);m.number(WORK+0x2280,5,2);result=3
   elif r==8:result=4
   else:phase(11);result=7
  call(RESTORE,0x80)
 elif a==0x208a3e0:
  update(v['option']);m.number(WORK+0x2288,WORK+0x1500);m.number(WORK+0x228c,1024,2);call(0x208a508,0);m.number(WORK+0x228e,1<<(v['next']-1),2)
  if v['time']==0:call(0x20123d0)
  m.number(WORK+0x2290,v['time']or 123,2);m.number(WORK+0x2298,0 if m.value(WORK+0x2264)&0x300000==0x300000 else 1,2);copy(A if v['bssid']else ANY_BSSID,WORK+0x2292,6)
  if v['essid']in [0,2]:copy(ANY_SSID,WORK+0x229c,32);length=0
  else:copy(BUFFER,WORK+0x229c,32);length=v['length']
  m.number(WORK+0x229a,length,2);m.number(WORK+0x2284,0)
 elif a==0x208a940:
  err=v['err']
  if err==0:
   if p==5:phase(6);notice(0,1796)
   p=m.value(WORK+0x2260)
   if p==6:
    m.number(WORK+0x2280,7,2)
    if v['state']==5:
     call(0x20072d0,RX,0x620)
     for i in range(v['found']):call(0x208b260,INPUT_BSS,3 if i==0 else 1);call(0x208a57c,7,0,INPUT_BSS,EVENT,1818)
    if v['option']&0xc00000==0xc00000:
     channels=(v['option']&0x3ffe).bit_count();call(0x208a66c,v['option']&0x3ffe)
     if channels:
      call(DIV,v['count'],channels)
      if v['count']%channels==0:call(0x208a57c,8,0,v['count'],0,1832)
    call(0x208a690,0x1001);call(0x208a508,13);m.number(WORK+0x228e,1<<(v['next']-1),2);call(0x20072d0,RX,0x620);m.number(WORK+0x2284,(v['count']+1)&0xffffffff);call(0x2012b28,0x208a941,WORK+0x2288)
   elif p==7:call(0x2012c78,0x208ab0d)
   elif p==13:call(0x208a698);r=2
   else:r=20
   if r==8:phase(12);notice(1,1875)
   elif r!=2:phase(11);notice(7,1884)
  elif err==1:call(0x208a698)
  else:phase(11);notice(7,1901)
 elif a in [0x208b154,0x208b1cc,0x208b224]:
  call(DISABLE);call(0x208a31c)
  if a==0x208b154:
   if v['existing']and v['buffer']and 0<v['size']<0x80000000:fill(BUFFER,v['size'])
  elif a==0x208b1cc:
   contract='word'
   if v['existing']:result=int(v['oldlock']!=0);m.number(WORK+0x226a,int(v['lock']!=0),1)
  else:
   contract='word'
   if v['existing']:call(0x208b3a4,v['index']);result=NODE+16 if v['found']else 0
  call(RESTORE,0x80)
 else:raise ValueError('Unowned WCM scan/AP function')
 return {at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
