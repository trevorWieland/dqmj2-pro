import itertools,struct

WORK=0x2280000
CONFIG=0x2290000
A=0x22a0000
B=0x22a0020
BUFFER=0x22b0000
GLOBAL=0x21cfcb4
INDEX=0x21cfce4
RSSI=0x21cfce8
STOP=0x2400000
SP=0x3004000
CALLBACK=STOP+0x80
DISABLE=0x2007ff4
RESTORE=0x2008008
DIV=0x2026144
RET64=[]
RELIABLE=0
OBSERVED=[]
ARITY={DISABLE:0,RESTORE:1,0x208a4f0:0,0x208b44c:0,0x2007a24:0,0x20079ac:0,0x2007c58:0,0x2007bd8:0,0x2007c68:1,0x2008d78:3,0x2007e10:1,0x2007da4:5,0x20127ec:1,0x208a5ac:1,0x208a550:4,DIV:2,CALLBACK:1}


class Memory:
 def __init__(self):self.regions={}
 def add(self,address,size,fill=0):self.regions[address]=bytearray([fill]*size)
 def read(self,address,size):
  for at,raw in self.regions.items():
   if at<=address and address+size<=at+len(raw):return bytes(raw[address-at:address-at+size])
  raise ValueError(('Model read escaped',hex(address),size))
 def write(self,address,data):
  for at,raw in self.regions.items():
   if at<=address and address+len(data)<=at+len(raw):raw[address-at:address-at+len(data)]=data;return
  raise ValueError(('Model write escaped',hex(address),len(data)))
 def number(self,address,value,size=4):self.write(address,int(value&((1<<(size*8))-1)).to_bytes(size,'little'))
 def value(self,address,size=4):return int.from_bytes(self.read(address,size),'little')


def cases(address):
 if address==0x2089aa4:
  return [dict(existing=e,buffer=p,length=n,tick=t,alarm=a)for e,p,n,t,a in [(1,WORK,0x2300,1,1),(0,0,0x2300,1,1),(0,WORK+1,0x2300,1,1),(0,WORK,0,1,1),(0,WORK,0x22ff,1,1),(0,WORK,0x2300,1,1),(0,WORK,0x2301,0,0),(0,WORK,0xffffffff,0,1),(0,WORK,0x2300,1,0)]]
 if address in [0x2089b64,0x208a268]:return [dict(existing=e,phase=p)for e,p in itertools.product([0,1],[0,1,9,11,0xffffffff])]
 if address==0x208a28c:return [dict(option=x,old=o)for x,o in itertools.product([0,0x8000,0x8002,0x20000,0x80000,0x200000,0x800000,0xffffffff,0x12345678],[0,0xffffffff,0xa55a1234])]
 if address==0x208a328:return [dict(config=c,offset=o,size=n,dma=d,mode=0x76543210)for c,o,n,d in [(0,0,0,0),(1,0,0,3),(1,0,11,0),(1,0,12,1),(1,1,14,0xff),(1,1,15,0xff),(1,2,16,4),(1,3,32,5),(1,0,64,0xffffffff)]]
 if address==0x208a508:return [dict(channel=c,option=o)for c,o in itertools.product([0,1,12,13,65535],[0,2,1<<13,0x3ffe,0x80000000])]
 if address==0x208a57c:return [dict(callback=c,notify=n,result=r,para0=0x12345678,para1=0x87654321,para2=0xffffff80)for c,n,r in itertools.product([0,1],[0,0x7fff,0xffff],[0,0x8000,0xffff])]
 if address==0x208a610:return [dict(phase=x)for x in [0,1,8,9,10,11,0xffffffff]]
 if address==0x208a698:return [dict(resetting=x,wm=w)for x,w in itertools.product([0,1,255],[0,1,2,3,0xffff])]
 if address==0x208b72c:return [dict(different=x)for x in [-1,0,1,2,3,4,5]]
 if address==0x208b77c:return [dict(index=x,pattern=p)for x,p in itertools.product([0,1,2,15,16,17,31,255],[0,1,2])]
 if address==0x208b7f0:return [dict(index=x,rssi=r)for x,r in itertools.product([0,1,15,16,17,31,255],[0,1,2,3,63,128,254,255])]
 raise ValueError('Unowned model')


def initial(address,v):
 m=Memory();m.add(WORK,0x2300,0x42);m.add(GLOBAL,4);m.add(INDEX,1);m.add(RSSI,16);m.add(CONFIG,16);m.add(BUFFER,128,0x71);m.add(A,6);m.add(B,6)
 m.number(GLOBAL,WORK if v.get('existing',1)else 0);m.number(WORK+0x2260,v.get('phase',1));m.number(WORK+0x2264,v.get('old',v.get('option',0)));m.number(WORK+0x226b,v.get('resetting',0),1);m.number(WORK+0x227c,CALLBACK|1 if v.get('callback',0)else 0)
 m.number(INDEX,v.get('index',0),1)
 values=bytes([0]*16)if v.get('pattern',0)==0 else bytes([255]*16)if v['pattern']==1 else bytes(range(16));m.write(RSSI,values)
 m.number(CONFIG,v.get('dma',0));m.number(CONFIG+4,BUFFER+v.get('offset',0));m.number(CONFIG+8,v.get('size',0));m.number(CONFIG+12,v.get('mode',0))
 m.write(A,bytes([0,1,2,253,254,255]));m.write(B,m.read(A,6))
 if v.get('different',-1)>=0:m.number(B+v['different'],0x55,1)
 args={0x2089aa4:[v.get('buffer',WORK),v.get('length',0)],0x208a28c:[v.get('option',0)],0x208a328:[CONFIG if v.get('config')else 0,0x76543211],0x208a508:[v.get('channel',0)],0x208a57c:[v.get('notify',0),v.get('result',0),v.get('para0',0),v.get('para1',0),v.get('para2',0)],0x208b72c:[A,B],0x208b7f0:[v.get('rssi',0)]}.get(address,[])
 return m,args


def arity(address,values,memory):return ARITY[address]


def effect(address,values,memory,v):
 normalized=list(values);value=0
 if address==DISABLE:value=0x80
 elif address==RESTORE:value=0x80
 elif address==0x2007a24:value=v.get('tick',1)
 elif address==0x2007c58:value=v.get('alarm',1)
 elif address==0x2008d78:memory.write(values[0],bytes([values[1]&255])*values[2])
 elif address==0x20127ec:value=v.get('wm',2)
 elif address==DIV:
  dividend=values[0]if values[0]<0x80000000 else values[0]-0x100000000;divisor=values[1]if values[1]<0x80000000 else values[1]-0x100000000;value=abs(dividend)//abs(divisor)*(1 if dividend*divisor>=0 else-1)
 elif address==CALLBACK:normalized=[memory.read(values[0],16).hex()]
 elif address not in ARITY:raise ValueError(('Unexpected provider',hex(address)))
 return value,normalized


def dynamic_callbacks(v):return {CALLBACK:dict(mode='thumb')}if v.get('callback')else{}


def expected_reads(address,v):return []


def model(address,v):
 m,args=initial(address,v);calls=[];contract='void';result=0
 def call(at,*values):calls.append((hex(at),list(values)))
 def bracket():call(DISABLE)
 def restore():call(RESTORE,0x80)
 if address==0x2089aa4:
  bracket();contract='word'
  if v['existing']or not v['buffer']or v['buffer']&31:result=1
  elif v['length']<0x2300:result=6
  else:
   m.number(GLOBAL,WORK);m.number(WORK+0x2260,1)
   for offset,size in [(0x2280,2),(0x2268,2),(0x226a,1),(0x226b,1),(0x2282,2),(0x22f8,2)]:m.number(WORK+offset,0,size)
   call(0x208a4f0);call(0x208b44c);call(0x2007a24)
   if not v['tick']:call(0x20079ac)
   call(0x2007c58)
   if not v['alarm']:call(0x2007bd8)
   call(0x2007c68,WORK+0x22cc)
  restore()
 elif address==0x2089b64:
  bracket();contract='word';result=0 if v['existing']and v['phase']==1 else 1
  if result==0:m.number(GLOBAL,0)
  restore()
 elif address==0x208a268:bracket();contract='word';result=v['phase']if v['existing']else 0;restore()
 elif address==0x208a28c:
  bracket();contract='word';result=v['old'];option=v['option'];mask=0
  for bit,filter in [(0x8000,0x3ffe),(0x20000,0x10000),(0x80000,0x40000),(0x200000,0x100000),(0x800000,0x400000)]:
   if option&bit:
    mask|=filter
    if bit==0x8000 and not(option&filter):option|=0x8000|2|128|8192
  m.number(WORK+0x2264,(v['old']&~mask)|option);restore()
 elif address==0x208a328:
  if not v['config']:
   for offset,value in [(0,3),(4,0),(8,0),(12,0)]:m.number(WORK+0x226c+offset,value)
  else:
   m.number(WORK+0x226c,v['dma']&3);alignment=(-v['offset'])&3
   if alignment+12>v['size']:m.number(WORK+0x2270,0);m.number(WORK+0x2274,0)
   else:
    at=BUFFER+v['offset']+alignment;size=v['size']-alignment;m.number(WORK+0x2270,at);m.number(WORK+0x2274,size);call(0x2008d78,at,0,size);m.write(at,bytes(size))
   m.number(WORK+0x2278,v['mode'])
  m.number(WORK+0x227c,0x76543211)
 elif address==0x208a508:
  contract='word';channel=v['channel'];i=0
  for i in range(13):
   call(DIV,channel+i,13)
   if v['option']&(1<<((channel+i)%13+1)):break
  else:i=13
  call(DIV,channel+i,13);result=(channel+i)%13+1
 elif address==0x208a57c:
  if v['callback']:calls.append((hex(CALLBACK),[struct.pack('<HHIII',v['notify'],v['result'],v['para0'],v['para1'],v['para2']).hex()]))
 elif address==0x208a610:
  bracket();call(0x2007e10,WORK+0x22cc)
  if v['phase']==9:call(0x2007da4,WORK+0x22cc,(33514000*70)//64,0,0x208a661,0)
  restore()
 elif address==0x208a698:
  if v['resetting']==0:
   m.number(WORK+0x226b,1,1);call(0x20127ec,0x208af1d)
   if v['wm']!=2:call(0x208a5ac,11);call(0x208a550,7,0,0,1552)
 elif address==0x208b72c:contract='word';result=int(v['different']==-1)
 elif address==0x208b77c:
  contract='word';count=min(v['index'],16);total=sum(m.read(RSSI,count));result=total//count if count else 0
  if 0<v['index']<=16:call(DIV,total,v['index'])
 elif address==0x208b7f0:
  raw=(v['rssi']>>2)+(0 if v['rssi']&2 else 25);index=v['index'];m.number(RSSI+index%16,raw,1);m.number(INDEX,((index+1)%16)+16 if index>=16 else index+1,1)
 else:raise ValueError('Unowned model')
 return {at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
