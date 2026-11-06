import struct,datetime
from project import ROOT
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
DATA,DATE,TIME=0x21d1990,0x2170000,0x2171000
ARITY={0x200f540:2,0x200fc74:2,0x200fe50:4}
OBSERVED=set()
MASK=(1<<64)-1
LIMIT=3155759999

def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def signed(value):return value-(1<<64)if value&(1<<63)else value
def initial(address,v):
 assert address==0x209b040
 m=Memory({DATA:struct.pack('<IQQ',v.get('valid',1)&0xffffffff,v.get('base',1000)&MASK,v.get('diff',100)&MASK),DATE:bytes((i*7+11)&255 for i in range(16)),TIME:bytes((i*11+7)&255 for i in range(12)),SP-0x1000:bytes(4096)})
 return m,[DATE,TIME]

def effect(at,a,m,v):
 result=0x76543210;norm=a[:]
 if at==0x200f540:
  m.write(a[0],struct.pack('<4I',*v.get('currentDate',[26,11,6,5])));m.write(a[1],struct.pack('<3I',*v.get('currentTime',[12,34,56])));result=v.get('getResult',0)
 elif at==0x200fc74:
  norm+=[list(struct.unpack('<4I',m.read(a[0],16))),list(struct.unpack('<3I',m.read(a[1],12)))];result=v.get('current',1001)&MASK
 elif at==0x200fe50:
  second=a[2]|(a[3]<<32)
  if not 0<=second<=LIMIT:raise ValueError('Outside qualified century conversion domain')
  value=datetime.datetime(2000,1,1)+datetime.timedelta(seconds=second);m.write(a[0],struct.pack('<4I',value.year-2000,value.month,value.day,(value.weekday()+1)%7));m.write(a[1],struct.pack('<3I',value.hour,value.minute,value.second))
 else:raise ValueError(('Outside date/time provider boundary',hex(at)))
 return result&(MASK if at==0x200fc74 else 0xffffffff),norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0
 def call(at,a):
  value,norm=effect(at,a,m,v);calls.append((hex(at),norm));return value
 if word(m,DATA)and call(0x200f540,[DATE,TIME])==0:
  raw=call(0x200fc74,[DATE,TIME])
  if raw!=MASK:
   current=signed(raw);base=signed(struct.unpack('<Q',m.read(DATA+4,8))[0]);difference=signed(struct.unpack('<Q',m.read(DATA+12,8))[0])
   if current<base:current+=LIMIT+1
   if not -(1<<63)<=current<(1<<63):raise ValueError('Signed64 century addition overflow is outside fixture domain')
   adjusted=current-difference
   if not -(1<<63)<=adjusted<(1<<63):raise ValueError('Signed64 difference overflow is outside fixture domain')
   if 0<=adjusted<=LIMIT:call(0x200fe50,[DATE,TIME,adjusted&0xffffffff,(adjusted>>32)&0xffffffff]);result=1
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result

def cases(address):
 out=[dict(valid=valid,current=current)for valid in [0,1,2,-1]for current in [0,1,-1,1000,1001,LIMIT,LIMIT+1]]
 out+=[dict(getResult=result)for result in [-1,1,2,0xffffffff]]
 out+=[dict(current=current,base=base,diff=diff)for current in [-2,0,1,1000,1001,LIMIT,LIMIT+1,0xffffffff,0x100000000,0x100000001,0x7fffffff00000000]for base in [-1,0,1000,current,current+1]for diff in [-1,0,1,100,LIMIT,LIMIT+1]]
 return out
