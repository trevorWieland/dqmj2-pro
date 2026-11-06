import itertools
from project import ROOT
from wave20261106_wcm_manager_next_cps_first_models import Memory
STOP=0x4000000
SP=0x3010000
A=0x22e1000
B=0x22e3000
RESULT=0x22e5000
RING=0x22e8000
THREAD=0x22e7000
GLOBAL=0x21cfcf8
ARP=0x21cfd78
MAC=0x21d01e0
CONST=0x20de7b4
BROADCAST=0x20de7ac
THREADINFO=0x20e33e4
DISABLE=0x2007ff4
RESTORE=0x2008008
TICK=0x2007a9c
COPY=0x2008e0c
FILL=0x2008d78
SEND=0x208bce8
RELIABLE=SEND
DIV=-1
RET64={TICK}
OBSERVED=set()
READ_ONLY={CONST,BROADCAST}
ARITY={DISABLE:0,RESTORE:1,TICK:0,COPY:3,FILL:3,SEND:4,0x208bd24:6,0x20068c0:1,0x200698c:1,0x20068d4:1,0x208bc30:1,0x208bc58:1,0x208bbe8:1,0x208bc18:1,0x208bf10:1,0x208c038:1}
def r32(m,a):return int.from_bytes(m.read(a,4),'little')
def r16(m,a):return int.from_bytes(m.read(a,2),'little')
def number(m,a,v,n=4):m.write(a,(v&((1<<(8*n))-1)).to_bytes(n,'little'))
def arity(a,values,memory):return ARITY[a]
def dynamic_callbacks(v):return {}
def expected_reads(a,v):return []
def base():return dict(write=0,read=512,capacity=2048,head=16,body=8,bad=0,present=1,bodypresent=1)
def cases(a):
 if a==0x208bd24:
  variations=[{},dict(present=0),dict(capacity=0),dict(head=4,body=0),dict(head=1508,body=0),dict(head=1508,body=1),*[dict(bad=i)for i in [1,2,3,4,5]],dict(write=20,read=30),dict(write=2000,read=0),dict(write=2016,read=0,head=24,body=0),dict(write=2000,read=64),dict(write=1024,read=64,capacity=1025),dict(write=2000,read=8),dict(body=0),dict(bodypresent=0),dict(head=9,body=2)]
  return[base()|x for x in variations]
 if a==0x208be40:return[dict(thread=t,terminated=z,post=p)for t,z,p in [(0,0,0),(1,0,1),(1,1,1),(0,0,1),(1,0,0)]]
 if a==0x208be70:return[dict(read=r,write=w,capacity=c,block=b,sleeps=s)for r,w,c,b,s in [(0,20,2048,20,0),(0,0,2048,20,1),(0,0,2048,20,2),(2047,20,2048,20,0),(2046,20,2048,20,0),(0,512,2048,512,0)]]
 if a==0x208bee4:return[dict(read=r,block=b,capacity=c)for r,b,c in [(0,20,2048),(2000,48,2048),(2000,64,2048),(0,0,2048),(100,20,2048)]]
 if a==0x208bf10:return[dict(ip=ip,hit=h,broadcast=b,tick=t)for ip,h,b,t in [(0x7f000001,-1,0,0),(0x0a123456,-1,0,0),(0xffffffff,-1,1,0),(0xe0000001,-1,0,0),(0x0a987654,-1,0,0),(0x0a987654,0,0,0),(0x0a987654,7,0,0x123456789abc),(0x0a987654,3,0,0xffff0000)]]
 if a==0x208bf98:return[dict(ip=ip,myip=my)for ip,my in itertools.product([0,0xffffffff,0xc0a80102],[0x0a123456,0xc0a80101])]
 if a==0x208c080:
  return[dict(ip=ip,local=local,force=force,hit=hit,empty=empty,now=now,ages=ages)for ip,local,force,hit,empty,now,ages in [(0x7f000001,1,1,-1,-1,100,0),(0x0a123456,1,1,-1,-1,100,0),(0x0a987654,0,1,-1,-1,100,0),(0xe0000001,1,1,-1,-1,100,0),(0x0a987654,1,0,0,-1,100,0),(0x0a987654,1,0,7,-1,0xffff,0),(0x0a987654,1,0,-1,-1,100,0),(0x0a987654,1,1,-1,0,100,0),(0x0a987654,1,-1,-1,7,0xffff,0),(0x0a987654,1,1,-1,-1,100,0),(0x0a987654,1,1,-1,-1,4,1),(0x0a987654,1,1,-1,-1,100,2)]]
 if a==0x208c140:return[dict(ip=ip,target=t,cache=c,request=r,head=h,body=b)for ip,t,c,r,h,b in [(0xe0010203,0,0,0,20,8),(0xefffffff,0,0,0,0,0),(0x0a987654,0,0,0,20,8),(0x0a987654,0x0a000001,1,0,20,8),(0x0a987654,0x0a000001,0,1,20,8),(0x0a987654,0x0a000001,0,0,20,8),(0x0a987654,0x0a000001,1,0,1480,1)]]
 raise ValueError('Unowned CPS packet model')

def initial(a,v):
 m=Memory()
 for at,n in [(A,2048),(B,2048),(RESULT,6),(RING,4096),(GLOBAL,96),(ARP,96),(MAC,6),(CONST,8),(BROADCAST,6),(THREADINFO,8)]:m.add(at,n)
 m.write(A,bytes((i*7+3)&255 for i in range(2048)));m.write(B,bytes((i*11+5)&255 for i in range(2048)));m.write(RING,bytes([0x55])*4096);m.write(RESULT,bytes.fromhex('02123456789a'));m.write(MAC,bytes.fromhex('021122334455'))
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
 for at,n in [(CONST,8),(BROADCAST,6)]:m.write(at,image[at-0x2000000:at-0x2000000+n])
 number(m,GLOBAL+80,0x0a123456);number(m,GLOBAL+88,RING);number(m,GLOBAL+92,2048);number(m,THREADINFO+4,THREAD)
 for i in range(8):number(m,ARP+12*i,0x0a000001+i);m.write(ARP+12*i+4,bytes([2,0x10,0x20,0x30,0x40,i]));number(m,ARP+12*i+10,50+i,2)
 if a==0x208bd24:
  number(m,GLOBAL+40,v['write']);number(m,GLOBAL+48,v['read']);number(m,GLOBAL+88,RING if v['present']else 0);number(m,GLOBAL+92,v['capacity']);m.write(B,m.read(CONST,8))
  if v['bad']:off={1:0,2:1,3:2,4:6,5:7}[v['bad']];m.write(B+off,bytes([m.read(B+off,1)[0]^1]))
  args=[A,A+8,B,v['head'],A+128 if v['bodypresent']else 0,v['body']]
 elif a==0x208be40:number(m,GLOBAL+84,THREAD if v['thread']else 0);args=[A,A+8,B,16]
 elif a==0x208be70:
  number(m,GLOBAL+40,v['write']);number(m,GLOBAL+48,v['read']);number(m,GLOBAL+92,v['capacity']);number(m,RING,v['block'],2)
  if v['read']==v['capacity']-2:number(m,RING+v['read'],0,2)
  args=[B]
 elif a==0x208bee4:number(m,GLOBAL+48,v['read']);number(m,GLOBAL+92,v['capacity']);number(m,RING+v['read'],v['block'],2);args=[]
 elif a==0x208bf10:
  if v['hit']>=0:number(m,ARP+v['hit']*12,v['ip'])
  args=[v['ip']]
 elif a==0x208bf98:m.add(SP-56,42);number(m,GLOBAL+80,v['myip']);args=[v['ip']]
 elif a==0x208c080:
  if v['hit']>=0:number(m,ARP+v['hit']*12,v['ip'])
  if v['empty']>=0:number(m,ARP+v['empty']*12,0)
  for i in range(8):number(m,ARP+i*12+10,((v['now']-(i+1)*3)if v['ages']==0 else v['now']+(i+1)if v['ages']==1 else v['now'])&0xffff,2)
  args=[A,v['ip'],v['force']]
 elif a==0x208c140:args=[A+64,v['head'],B,v['body'],v['ip'],0x800]
 else:raise ValueError('Unowned CPS packet initialization')
 return m,args

def effect(a,values,m,v):
 normalized=list(values)
 if a==DISABLE:return 0x80,normalized
 if a==RESTORE:return 0x80,normalized
 if a==TICK:return v.get('tick',(v.get('now',0)<<16)|0x4321),normalized
 if a==COPY:m.write(values[1],m.read(values[0],values[2]));return 0,normalized
 if a==FILL:m.write(values[0],bytes([values[1]&255])*values[2]);return 0,normalized
 if a==SEND:return 0,normalized+[m.read(values[0],values[1]).hex(),m.read(values[2],values[3]).hex()if values[2]and values[3]else'']
 if a==0x208bd24:number(m,GLOBAL+84,THREAD if v['post']else 0);return 0,normalized
 if a==0x20068c0:return v['terminated'],normalized
 if a==0x200698c:return 0,normalized
 if a==0x20068d4:
  count=getattr(m,'sleepCount',0)+1;m.sleepCount=count
  if count>=v['sleeps']:number(m,GLOBAL+40,v['block'])
  return 0,normalized
 if a==0x208bc30:return v.get('broadcast',0),normalized
 if a==0x208bc58:return int(values[0]>>28==14),normalized
 if a==0x208bbe8:return v['local'],normalized
 if a==0x208bc18:return v['target'],normalized
 if a==0x208bf10:return RESULT if v['cache']else 0,normalized
 if a==0x208c038:return RESULT if v['request']else 0,normalized
 raise ValueError(('Unmodeled CPS packet provider',hex(a)))

def model(a,v):
 m,args=initial(a,v);calls=[];result=0;contract='void'
 def call(at,*values):
  answer,normalized=effect(at,[x&0xffffffff for x in values],m,v);calls.append((hex(at),normalized));return answer
 if a==0x208bd24:
  total=v['head']+v['body'];raw=m.read(B,8);valid=v['present']and v['capacity']and 8<=total<=1508 and raw[:3]==m.read(CONST,3)and raw[6]==8 and raw[7]in [0,6]
  if valid:
   block=(total+9)&~1;write,read,capacity=v['write'],v['read'],v['capacity'];end=write+block;valid=not(write<read<=end)
   if end==capacity:end=0;valid=valid and read!=0
   elif end>capacity:end=block;valid=valid and read>block
   if valid:
    if write+block>capacity:
     if capacity-write>=2:number(m,RING+write,0,2)
     write=0;number(m,GLOBAL+40,0)
    number(m,RING+write,block,2);call(COPY,A+8,RING+write+2,6);call(COPY,A,RING+write+8,6);call(COPY,B+6,RING+write+14,v['head']-6)
    if v['bodypresent']and v['body']:call(COPY,A+128,RING+write+8+v['head'],v['body'])
    number(m,GLOBAL+40,end)
 elif a==0x208be40:
  call(0x208bd24,A,A+8,B,16,0,0)
  if r32(m,GLOBAL+84)and not call(0x20068c0,r32(m,GLOBAL+84)):call(0x200698c,r32(m,GLOBAL+84))
 elif a==0x208be70:
  saved=call(DISABLE)
  while r32(m,GLOBAL+48)==r32(m,GLOBAL+40):number(m,GLOBAL+84,THREAD);call(0x20068d4,0);number(m,GLOBAL+84,0)
  call(RESTORE,saved)
  while True:
   read=r32(m,GLOBAL+48)
   if v['capacity']-read<2:read=0;number(m,GLOBAL+48,0)
   block=r16(m,RING+read)
   if block:break
   number(m,GLOBAL+48,0)
  number(m,B,block-2);result=RING+r32(m,GLOBAL+48)+2;contract='word'
 elif a==0x208bee4:
  saved=call(DISABLE);read=v['read']+v['block'];number(m,GLOBAL+48,read if read<v['capacity']else 0);call(RESTORE,saved)
 elif a==0x208bf10:
  saved=call(DISABLE);ip=v['ip'];result=0
  if ip in [0x7f000001,0x0a123456]:result=MAC
  elif call(0x208bc30,ip)or call(0x208bc58,ip):result=BROADCAST
  else:
   for i in range(8):
    if r32(m,ARP+12*i)==ip:number(m,ARP+12*i+10,(call(TICK)>>16)&0xffff,2);result=ARP+12*i+4;break
  call(RESTORE,saved);contract='word'
 elif a==0x208bf98:
  q=SP-56;call(FILL,q,0,42);call(FILL,q,255,6);call(COPY,MAC,q+6,6);m.write(q+12,bytes.fromhex('08060001080006040001'));call(COPY,MAC,q+22,6);m.write(q+28,v['myip'].to_bytes(4,'big'));m.write(q+38,v['ip'].to_bytes(4,'big'));call(SEND,q,42,0,0)
 elif a==0x208c080:
  ip=v['ip']
  if ip not in [0x7f000001,0x0a123456]and call(0x208bbe8,ip)and not call(0x208bc58,ip):
   now=(call(TICK)>>16)&0xffff;hit=next((i for i in range(8)if r32(m,ARP+i*12)==ip),None)
   if hit is not None:number(m,ARP+hit*12+10,now,2);call(COPY,A,ARP+hit*12+4,6)
   elif v['force']:
    oldest,candidate=0,0
    for i in range(8):
     if r32(m,ARP+i*12)==0:candidate=i;break
     age=(now-r16(m,ARP+i*12+10))&0xffff;signed=age if age<32768 else age-65536
     if signed>oldest:oldest=age;candidate=i
    number(m,ARP+candidate*12,ip);call(COPY,A,ARP+candidate*12+4,6);number(m,ARP+candidate*12+10,now,2)
 elif a==0x208c140:
  hdr=A+64;ip=v['ip'];m.write(hdr-2,bytes.fromhex('0800'));ready=True
  if call(0x208bc58,ip):m.write(hdr-14,bytes([1,0,0x5e,(ip>>16)&127,(ip>>8)&255,ip&255]))
  else:
   target=call(0x208bc18,ip)
   if not target:ready=False
   else:
    mac=call(0x208bf10,target)
    if not mac:mac=call(0x208c038,target)
    if not mac:ready=False
    else:call(COPY,mac,hdr-14,6)
  if ready:call(COPY,MAC,hdr-8,6);call(SEND,hdr-14,v['head']+14,B,v['body'])
 else:raise ValueError('Unowned CPS packet model result')
 return{at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
