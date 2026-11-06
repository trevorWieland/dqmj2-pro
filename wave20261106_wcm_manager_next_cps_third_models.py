import itertools
from project import ROOT
from wave20261106_wcm_manager_next_cps_first_models import Memory,checksum,complement
STOP=0x4000000
SP=0x3010000
A=0x22e1000
B=0x22e3000
RESULT=0x22e5000
SOC=0x22e6000
NODES=0x22e8000
SOCKETS=0x22e9000
RECV=0x22ea000
GLOBAL=0x21cfcf8
MAC=0x21d01e0
THREADINFO=0x20e33e4
DISABLE=0x2007ff4
RESTORE=0x2008008
COPY=0x2008e0c
SEND=0x208bce8
RELIABLE=SEND
DIV=-1
RET64=set()
OBSERVED=set()
READ_ONLY=set()
ARITY={DISABLE:0,RESTORE:1,COPY:3,SEND:4,0x208bb08:3,0x208bb84:1,0x208bb98:2,0x208c2b4:6,0x208bcc4:2,0x208c080:3,0x208c6f8:1,0x208bc18:1,0x208bf10:1,0x208bf98:1,0x200698c:1,0x208c97c:2,0x208c848:3,0x208c8d0:3}
def r32(m,a):return int.from_bytes(m.read(a,4),'little')
def r16(m,a):return int.from_bytes(m.read(a,2),'little')
def number(m,a,v,n=4):m.write(a,(v&((1<<(8*n))-1)).to_bytes(n,'little'))
def be(m,a,v,n=4):m.write(a,(v&((1<<(8*n))-1)).to_bytes(n,'big'))
def arity(a,values,memory):return ARITY[a]
def dynamic_callbacks(v):return {}
def expected_reads(a,v):return []
def cases(a):
 if a==0x208c418:return[dict(length=n,counter=c,offset=n&1)for n,c in itertools.product([0,1,8,31,1480],[0,0xffff])]
 if a==0x208c6f8:return[dict(myip=ip,mac=i)for ip,i in itertools.product([0,0x0a123456,0xc0a80101],[0,1])]
 if a==0x208c770:
  base=dict(length=28,same=0,myip=0x0a123456,hardware=1,protocol=0x800,sizes=0x604,opcode=1,fromip=0x0a987654,toip=0x0a123456,postip=0x0a123456)
  variants=[{},dict(length=27),dict(same=1),dict(myip=0),dict(hardware=2),dict(protocol=0x86dd),dict(sizes=0x605),dict(opcode=0),dict(opcode=3),dict(toip=0x0a111111),dict(fromip=0x0a123456),dict(opcode=2,fromip=0x0a123456),dict(opcode=2),dict(postip=0)]
  return[base|v for v in variants]
 if a==0x208c848:return[dict(target=t,cache=c,length=n)for t,c,n in [(0,0,8),(0x0a000001,0,32),(0x0a000001,1,8),(0x0a000001,1,64)]]
 if a==0x208c8d0:return[dict(case=c,length=n,capacity=z,blocked=b)for c,n,z,b in [('none',8,64,3),('nullsoc',8,64,3),('nullthread',8,64,3),('state',8,64,3),('id',8,64,3),('sequence',8,64,3),('busy',8,64,3),('ip',8,64,3),('match',8,64,0),('match',9,64,3),('match',72,32,3),('match',16,0,3),('last',40,64,3)]]
 if a==0x208c998:return[dict(valid=c,ipvalid=i,type=t,length=n)for c,i,t,n in [(0,1,8,8),(1,0,8,8),(1,1,8,8),(1,1,0,32),(1,1,3,32),(1,1,255,8),(1,1,9,8)]]
 raise ValueError('Unowned CPS ICMP model')

def initial(a,v):
 m=Memory()
 for at,n in [(A,2048),(B,2048),(RESULT,6),(SOC,100),(NODES,3*192),(SOCKETS,3*128),(RECV,3*128),(GLOBAL,96),(MAC,6),(THREADINFO,12)]:m.add(at,n)
 m.write(A,bytes((i*7+3)&255 for i in range(2048)));m.write(B,bytes((i*11+5)&255 for i in range(2048)));m.write(MAC,bytes.fromhex('021122334455'));m.write(RESULT,bytes.fromhex('02123456789a'));number(m,GLOBAL+80,0x0a123456);number(m,THREADINFO+4,NODES)
 be(m,A+12,0x0a987654);be(m,A+16,0x0a123456)
 if a==0x208c418:number(m,GLOBAL+4,v['counter'],2);number(m,SOC+76,A);number(m,SOC+28,0xc0a80102);args=[B+v['offset'],v['length'],SOC]
 elif a==0x208c6f8:
  number(m,GLOBAL+80,v['myip']);m.write(A+72,bytes([2,0x40,0x50,0x60,0x70,v['mac']]));be(m,A+78,0xc0a80102);args=[A+64]
 elif a==0x208c770:
  q=A+64;number(m,GLOBAL+80,v['myip']);m.write(q+8,m.read(MAC,6)if v['same']else m.read(RESULT,6));be(m,q,v['hardware'],2);be(m,q+2,v['protocol'],2);be(m,q+4,v['sizes'],2);be(m,q+6,v['opcode'],2);be(m,q+14,v['fromip']);be(m,q+24,v['toip']);args=[q,v['length']]
 elif a==0x208c848:m.write(B,bytes([8])+m.read(B+1,2047));args=[A,B,v['length']]
 elif a==0x208c8d0:
  q=v['case'];count=3 if q=='last'else 0 if q=='none'else 1;number(m,THREADINFO+8,NODES if count else 0)
  for i in range(count):
   t=NODES+192*i;s=SOCKETS+128*i;number(m,t+104,t+192 if i+1<count else 0);number(m,t+164,0 if q=='nullsoc'else s);number(m,s,0 if q=='nullthread'else t);number(m,s+8,10 if q=='state'or q=='last'and i<2 else 11,1);number(m,s+10,0x1234 if q!='sequence'else 0x4321,2);number(m,s+28,0x0a987654 if q!='ip'else 0x0a010203);number(m,s+60,v['capacity']);number(m,s+64,RECV+128*i);number(m,s+68,1 if q=='busy'else 0);number(m,s+4,v['blocked'])
  expected=NODES+384 if q=='last'else NODES;number(m,B+4,(expected if q!='id'else expected+2)&0xffff,2);number(m,B+6,0x1234,2);args=[A,B,v['length']]
 elif a==0x208c998:
  m.write(B,bytes([v['type']])+m.read(B+1,2047));number(m,B+2,0,2);be(m,B+2,complement(checksum(m.read(B,v['length']),0)),2)
  assert checksum(m.read(B,v['length']),0)==0xffff
  if not v['valid']:m.write(B+1,bytes([m.read(B+1,1)[0]^1]))
  if not v['ipvalid']:be(m,A+16,0xffffffff)
  args=[A,B,v['length']]
 else:raise ValueError('Unowned CPS ICMP initialization')
 return m,args

def effect(a,values,m,v):
 normalized=list(values)
 if a in [DISABLE,RESTORE]:return 0x80,normalized
 if a==COPY:m.write(values[1],m.read(values[0],values[2]));return 0,normalized
 if a==SEND:return 0,normalized+[m.read(values[0],values[1]).hex(),m.read(values[2],values[3]).hex()if values[2]and values[3]else'']
 if a==0x208bb08:return checksum(m.read(values[0],values[1]),values[2],bool(values[0]&1)),normalized
 if a==0x208bb84:return complement(values[0]),normalized
 if a==0x208bb98:return complement(checksum(m.read(values[0],values[1]),0,bool(values[0]&1))),normalized
 if a==0x208c2b4:return 0,normalized+[m.read(values[0],values[1]).hex(),m.read(values[2],values[3]).hex()if values[2]and values[3]else'']
 if a==0x208bcc4:return int(m.read(values[0],6)!=m.read(values[1],6)),normalized
 if a==0x208c080:number(m,GLOBAL+80,v['postip']);return 0,normalized
 if a in [0x208c6f8,0x208bf98,0x200698c,0x208c848,0x208c8d0]:return 0,normalized
 if a==0x208bc18:return v['target'],normalized
 if a==0x208bf10:return RESULT if v['cache']else 0,normalized
 if a==0x208c97c:return int(values[0]not in [0,0xffffffff]and values[1]not in [0,0xffffffff]),normalized
 raise ValueError(('Unmodeled CPS ICMP provider',hex(a)))

def model(a,v):
 m,args=initial(a,v);calls=[];result=0;contract='void'
 def call(at,*values):
  answer,normalized=effect(at,[x&0xffffffff for x in values],m,v);calls.append((hex(at),normalized));return answer
 if a==0x208c418:
  hdr=A+34;number(m,hdr,8,2);number(m,hdr+4,NODES&0xffff,2);number(m,hdr+2,0,2);number(m,SOC+10,v['counter'],2);number(m,GLOBAL+4,v['counter']+1,2);number(m,hdr+6,v['counter'],2)
  total=call(0x208bb08,hdr,8,0);total=call(0x208bb08,args[0],v['length'],total);be(m,hdr+2,call(0x208bb84,total),2);call(0x208c2b4,hdr,8,args[0],v['length'],0xc0a80102,1)
 elif a==0x208c6f8:
  q=A+64;be(m,q+6,2,2);call(COPY,q+8,q+18,10);call(COPY,MAC,q+8,6);be(m,q+14,v['myip']);call(COPY,q+18,q-14,6);call(COPY,MAC,q-8,6);call(SEND,q-14,42,0,0)
 elif a==0x208c770:
  q=A+64
  if v['length']>=28 and call(0x208bcc4,q+8,MAC)and v['myip']and v['hardware']==1 and v['protocol']==0x800 and v['sizes']==0x604 and v['opcode']in [1,2]:
   from_me=v['fromip']==v['myip'];to_me=v['toip']==v['myip']
   if not from_me:call(0x208c080,q+8,v['fromip'],int(to_me))
   if v['opcode']==1 and to_me:call(0x208c6f8,q)
   elif v['opcode']==2 and to_me and from_me:number(m,GLOBAL+1,1,1)
 elif a==0x208c848:
  ip=int.from_bytes(m.read(A+12,4),'big');target=call(0x208bc18,ip)
  if target:
   if not call(0x208bf10,target):call(0x208bf98,target)
   else:number(m,B,0,1);number(m,B+2,0,2);be(m,B+2,call(0x208bb98,B,v['length']),2);call(0x208c2b4,B,v['length'],0,0,ip,1)
 elif a==0x208c8d0:
  saved=call(DISABLE);t=r32(m,THREADINFO+8)
  while t:
   s=r32(m,t+164)
   if s and r32(m,s)and m.read(s+8,1)[0]==11 and(r32(m,s)&0xffff)==r16(m,B+4)and r16(m,s+10)==r16(m,B+6)and r32(m,s+68)==0 and r32(m,s+28)==int.from_bytes(m.read(A+12,4),'big'):
    length=min(v['length']-8,r32(m,s+60));number(m,s+68,length);call(COPY,B+8,r32(m,s+64),length)
    if r32(m,s+4)==3:number(m,s+4,0);call(0x200698c,r32(m,s))
    break
   t=r32(m,t+104)
  call(RESTORE,saved)
 elif a==0x208c998:
  if call(0x208bb98,B,v['length'])==0xffff and call(0x208c97c,int.from_bytes(m.read(A+12,4),'big'),int.from_bytes(m.read(A+16,4),'big')):
   if v['type']==0:call(0x208c8d0,A,B,v['length'])
   elif v['type']==8:call(0x208c848,A,B,v['length'])
 else:raise ValueError('Unowned CPS ICMP result')
 return{at:bytes(raw)for at,raw in m.regions.items()},calls,contract,result
