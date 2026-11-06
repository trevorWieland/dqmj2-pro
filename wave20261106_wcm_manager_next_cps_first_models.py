import itertools
from project import ROOT
STOP=0x4000000
SP=0x3010000
A=0x22e1000
B=0x22e3000
SOC=0x22e5000
GLOBAL=0x21cfcf8
MAC=0x21d01e0
CONST=0x20de7b4
DISABLE=0x2007ff4
RESTORE=0x2008008
RELIABLE=-1
DIV=-1
RET64=set()
OBSERVED=set()
READ_ONLY={CONST}
ARITY={0x208bb08:3,0x208bb84:1,0x208bb98:2,0x208bc58:1,0x208c140:6,0x208bd24:6,0x2008e0c:3,DISABLE:0,RESTORE:1,0x208c2b4:6}
class Memory:
 def __init__(self):self.regions={}
 def add(self,a,n):self.regions[a]=bytearray(n)
 def read(self,a,n):
  for s,b in self.regions.items():
   if s<=a and a+n<=s+len(b):return bytes(b[a-s:a-s+n])
  raise ValueError(('Model read escaped',hex(a),n))
 def write(self,a,raw):
  for s,b in self.regions.items():
   if s<=a and a+len(raw)<=s+len(b):b[a-s:a-s+len(raw)]=raw;return
  raise ValueError(('Model write escaped',hex(a),len(raw)))
 def number(self,a,value,n=4):self.write(a,(value&((1<<(8*n))-1)).to_bytes(n,'little'))

def checksum(raw,seed,odd=False):
 value=seed if odd else seed&0xffff
 for i in range(0,len(raw)-1,2):value=(value+int.from_bytes(raw[i:i+2],'big'))&0xffffffff
 if len(raw)&1:value=(value+(raw[-1]<<8))&0xffffffff
 value=(value&0xffff)+(value>>16)
 return(value+(value>>16))&0xffff

def complement(value):return(value^0xffff)or 0xffff

def cases(a):
 if a==0x208bb08:return[dict(length=n,offset=o,seed=s)for n,o,s in itertools.product([0,1,2,3,8,31,128],[0,1],[0,0xffff,0x12345678,0xffffffff])]
 if a==0x208bb84:return[dict(value=v)for v in [0,1,0xff,0x100,0x7fff,0x8000,0xfffe,0xffff]]
 if a==0x208bbac:return[dict(length=n,proto=p)for n,p in itertools.product([0,1,2,3,15,64],[0,6,17,0xffff])]
 if a==0x208bc58:return[dict(ip=v)for v in [0,1,0xc0000000,0xdfffffff,0xe0000000,0xe0000001,0xefffffff,0xf0000000,0xffffffff]]
 if a==0x208bcc4:return[dict(position=p,value=v)for p,v in itertools.product([-1,0,1,2,3,4,5],[1,0xff])]
 if a==0x208c1e0:return[dict(ip=ip,headlen=h,bodylen=b,fragment=f)for ip,(h,b,f)in itertools.product([0x7f000001,0x0a123456,0xe0000001,0xefffffff,0x0a987654],[(0,0,0),(8,3,0x2000),(32,128,0x1fff),(1480,0,0xffff),(0,1480,185)])]
 if a==0x208c488:return[dict(length=n,port=p,offset=n&1)for n,p in itertools.product([0,1,7,8,31,128,1480],[0,53,0xffff])]
 raise ValueError('Unowned CPS model')

def initial(a,v):
 m=Memory()
 for at,n in [(A,2048),(B,2048),(SOC,100),(GLOBAL,84),(MAC,6),(CONST,8)]:m.add(at,n)
 m.write(A,bytes((i*7+3)&255 for i in range(2048)));m.write(B,bytes((i*11+5)&255 for i in range(2048)))
 raw=(ROOT/'extract/arm9/arm9.bin').read_bytes();m.write(CONST,raw[CONST-0x2000000:CONST-0x2000000+8]);m.write(MAC,bytes.fromhex('021122334455'));m.number(GLOBAL+80,0x0a123456)
 if a==0x208bb08:args=[B+v['offset'],v['length'],v['seed']]
 elif a==0x208bb84:args=[v['value']]
 elif a==0x208bbac:
  if v['proto']==0xffff:m.write(B,bytes(2048));m.write(A,bytes(2048))
  args=[B,v['length'],A,v['proto']]
 elif a==0x208bc58:args=[v['ip']]
 elif a==0x208bcc4:
  m.write(A,bytes.fromhex('001122334455'));m.write(B,m.read(A,6))
  if v['position']>=0:m.write(B+v['position'],bytes([m.read(B+v['position'],1)[0]^v['value']]))
  args=[A,B]
 elif a==0x208c1e0:args=[A+64,v['headlen'],B,v['bodylen'],v['ip'],v['fragment']]
 elif a==0x208c488:
  m.number(SOC+0xa,0xffff-v['port'],2);m.number(SOC+0x18,v['port'],2);m.number(SOC+0x1c,0xc0a80102);m.number(SOC+0x4c,A);args=[B+v['offset'],v['length'],SOC]
 else:raise ValueError('Unowned CPS initialization')
 return m,args

def arity(a,values,memory):return ARITY[a]
def dynamic_callbacks(v):return {}
def expected_reads(a,v):return []

def effect(a,values,memory,v):
 if a==0x208bb08:return checksum(memory.read(values[0],values[1]),values[2],bool(values[0]&1)),list(values)
 if a==0x208bb84:return complement(values[0]),list(values)
 if a==0x208bb98:return complement(checksum(memory.read(values[0],values[1]),0,bool(values[0]&1))),list(values)
 if a==0x208bc58:return int(values[0]>>28==14),list(values)
 if a==0x2008e0c:memory.write(values[1],memory.read(values[0],values[2]));return 0,list(values)
 if a==DISABLE:return 0x80,list(values)
 if a==RESTORE:return 0x80,list(values)
 if a in [0x208c140,0x208bd24,0x208c2b4]:return 0,list(values)
 raise ValueError(('Unmodeled CPS provider',hex(a)))

def model(a,v):
 m,args=initial(a,v);calls=[];result=0;contract='word'
 def call(at,*values):
  vals=[x&0xffffffff for x in values];calls.append((hex(at),vals));return effect(at,vals,m,v)[0]
 def put(a,v):m.write(a,(v&0xffff).to_bytes(2,'big'))
 if a==0x208bb08:result=checksum(m.read(args[0],args[1]),args[2],bool(args[0]&1))
 elif a==0x208bb84:result=complement(v['value'])
 elif a==0x208bbac:
  total=call(0x208bb08,B,v['length'],v['proto']);total=call(0x208bb08,A+12,8,total)+v['length']
  if total&0x10000:total=(total+1)&0xffff
  result=int(total!=0xffff)
 elif a==0x208bc58:result=int(0xe0000000<=v['ip']<0xf0000000)
 elif a==0x208bcc4:result=int(m.read(A,6)!=m.read(B,6))
 elif a==0x208c1e0:
  hdr=args[0];h,b,ip,f=v['headlen'],v['bodylen'],v['ip'],v['fragment'];put(hdr-18,h+20+b);put(hdr-14,f);put(hdr-10,0);put(hdr-10,call(0x208bb98,hdr-20,20))
  if ip not in [0x7f000001,0x0a123456]:call(0x208c140,hdr-20,h+20,B,b,ip,0x800)
  local=ip in [0x7f000001,0x0a123456]
  if not local:local=bool(call(0x208bc58,ip))
  if local:
   call(0x2008e0c,CONST,hdr-28,8);saved=call(DISABLE);call(0x208bd24,MAC,MAC,hdr-28,h+28,B,b);call(RESTORE,saved)
  contract='void'
 elif a==0x208c488:
  hdr=A+34;n=v['length'];data=args[0]
  m.write(hdr-12,(0x0a123456).to_bytes(4,'big'));m.write(hdr-8,(0xc0a80102).to_bytes(4,'big'));put(hdr-4,17);put(hdr+4,n+8);put(hdr-2,n+8);put(hdr+2,v['port']);put(hdr,0xffff-v['port']);put(hdr+6,0)
  total=call(0x208bb08,hdr-12,20,0);total=call(0x208bb08,data,n,total);put(hdr+6,call(0x208bb84,total));call(0x208c2b4,hdr,8,data,n,0xc0a80102,17);contract='void'
 else:raise ValueError('Unowned CPS model result')
 return{at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
