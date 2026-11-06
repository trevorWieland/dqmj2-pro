import re
from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
G,E,TI,U=0x21d19a4,0x20ec9b0,0x20e33e4,0x20deb2c
I0,I1,R0,R1,SVC,T0,T1,TXT,DATE,ALT=0x2170000,0x2174000,0x2178000,0x2178200,0x2179000,0x217a000,0x217a100,0x217b000,0x217b100,0x217c000
SP,STOP,MAGIC,DIV,STATE=0x2701000,0x27e0000,0,0,0x217d000
PARAM,CAL=SP-192,SP-164
TERMINATE=0x2008430
AP,AT,FP,FT=0x2234000,0x2234004,0x2234100,0x2234104
OBSERVED={E}
ARITY={0x2008d78:3,0x20068c0:1,TERMINATE:0,0x201d800:2,0x209820c:2,0x209a9f8:2,0x2097dc4:1,0x2097fac:3,0x20987b0:1,0x2098954:4,0x20982e4:1,0x2006b74:1,0x209834c:2,0x2098d0c:2,0x2098ed8:2,0x2099bf8:1,0x201f274:1,0x2098f14:4}
IMPORTS=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/seventh/original-imports.json')
DATA={int(at,0):bytes.fromhex(v['expectedHex'])for at,v in IMPORTS['dataViews'].items()if v['storage']=='data'}
URLVIEW=IMPORTS['dataViews'][hex(U)];URLPOINTER=int(URLVIEW['pointee'],0);DATA[URLPOINTER]=bytes.fromhex(URLVIEW['pointeeExpectedHex'])
TAGS={raw[:-1].decode('ascii'):at for at,raw in DATA.items()if at!=U}
def dynamic_callbacks(v):return {}
def allocator(v):return AT|1 if v.get('callbackMode',0)&1 else AP
def freer(v):return FT|1 if v.get('callbackMode',0)&2 else FP
def cstring(m,at):
 out=bytearray()
 for index in range(1024):
  b=m.read(at+index,1)
  if not b[0]:return bytes(out)
  out+=b
 raise ValueError('Outside bounded SVL string')
def initial(address,v):
 m=Memory({**DATA,G:bytes(4),E:bytes(4),TI:bytes(8),I0:bytes((i*13+1)&255 for i in range(7200)),I1:bytes((i*7+5)&255 for i in range(7200)),R0:bytes([0x66])*372,R1:bytes([0x77])*372,SVC:b'ABCD'+bytes(60),T0:bytes(192),T1:bytes(192),TXT:bytes(64),DATE:b'Fri, 03 Mar 2006 01:28:13 GMT'+bytes(40),ALT:b'https://private.invalid/ac'+bytes(64),STATE:bytes(128),SP-0x1000:bytes(4096)})
 put(m,G,I0);put(m,E,v.get('initialErrno',0));put(m,TI+4,T1 if v.get('otherThread')else T0);put(m,T0+112,v.get('priority',16));put(m,T1+112,v.get('priority',16));put(m,U,ALT if v.get('customUrl')else URLPOINTER)
 for work,result in [(I0,R0),(I1,R1)]:put(m,work,allocator(v));put(m,work+4,freer(v));put(m,work+7196,result);put(m,work+7084,v.get('threadId',0))
 m.write(TXT,str(v.get('status',200)).encode()+bytes([0]));return m,[SVC,R0]if address==0x2099df4 else[]
def integer(raw):
 match=re.match(rb'[ \t\n\r\v\f]*([+-]?[0-9]+)',raw);return int(match[1])&0xffffffff if match else 0
def effect(at,a,m,v):
 result=0x76543210;norm=a[:]
 if at==0x2008d78:
  m.write(a[0],bytes([a[1]&255])*a[2])
  if v.get('clearSwapsWork'):put(m,G,I1)
 elif at==0x20068c0:
  result=v.get('terminated',1)&0xffffffff
  if v.get('probeSwapsWork'):put(m,G,I1)
 elif at==TERMINATE:result=0
 elif at==0x201d800:
  left,right=cstring(m,a[0]),cstring(m,a[1]);result=0 if left==right else 1 if left>right else 0xffffffff;norm=a+[left.hex(),right.hex()]
  if v.get('compareSwapsWork'):put(m,G,I1)
 elif at==0x209820c:
  norm=a+[m.read(a[1],28).hex()];result=v.get('create',0)
  if v.get('createSwapsWork'):put(m,G,I1)
 elif at==0x2097dc4:m.write(a[0],bytes((i*9+3)&255 for i in range(148)));result=v.get('cal',1)
 elif at==0x2097fac:norm=a+[m.read(a[1],148).hex()];result=v.get('calPost',1)
 elif at==0x2098954:norm=a+[cstring(m,a[1]).hex(),m.read(a[2],a[3]).hex()];result=v.get('postAction',0)if cstring(m,a[1])==b'action'else v.get('postService',0)
 elif at==0x20982e4:result=v.get('finish',0)
 elif at==0x2006b74:result=word(m,a[0]+112)
 elif at==0x209834c:
  put(m,a[0]+7076,v.get('startedId',1))
  if v.get('startSwapsWork'):put(m,G,I1)
 elif at==0x2098d0c:result=v.get('parse',1)
 elif at==0x2098ed8:
  tag=cstring(m,a[1]);norm=a+[tag.hex()];result=DATE if tag==b'Date'and v.get('date')else TXT if tag==b'httpresult'and v.get('httpFound',True)else 0
 elif at==0x2099bf8:
  norm=a+[cstring(m,a[0]).hex()];result=0
  if v.get('dateSwapsWork'):put(m,G,I1)
 elif at==0x201f274:
  raw=cstring(m,a[0]);result=integer(raw);norm=a+[raw.hex()];count=word(m,STATE);put(m,STATE,count+1);key='errnoAfterStatus'if count==0 else'errnoAfterCode'
  if key in v:put(m,E,v[key])
 elif at==0x2098f14:
  tag=cstring(m,a[1]);norm=a+[tag.hex()]
  if tag==b'returncd':payload=str(v.get('returnCode',0)).encode();result=v.get('decodeCode',len(payload))
  elif tag==b'svchost':payload=b'host';result=v.get('decodeHost',4)
  elif tag==b'servicetoken':payload=b'token';result=v.get('decodeToken',5)
  elif tag==b'statusdata':payload=bytes([v.get('statusByte',89)]);result=v.get('decodeStatus',1)
  else:raise ValueError('Unknown SVL result key')
  if result>=0:
   n=min(result,a[3]);m.write(a[2],payload[:n].ljust(n,b'x'))
   if result<a[3]:m.write(a[2]+result,bytes([0]))
  if tag==b'svchost'and v.get('decodeSwapsWork'):put(m,G,I1)
 elif at in [0x209a9f8,0x20987b0]:pass
 else:raise ValueError(('Outside SVL request/result provider',hex(at)))
 return result&0xffffffff,norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0;stopped=False
 def call(at,a):
  r,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return r
 def error(group,code):call(0x209a9f8,[group,code])
 if address==0x2099df4:
  put(m,word(m,G)+7196,R0);call(0x2008d78,[R0,0,372])
  if word(m,word(m,G)+7084)and call(0x20068c0,[word(m,G)+6976])==0:call(TERMINATE,[]);stopped=True
  else:
   url=word(m,U);work=word(m,G);alloc=word(m,work);free=word(m,work+4);different=call(0x201d800,[url,TAGS['https://nas.nintendowifi.net/ac']])!=0
   for offset,value in [(0,url),(4,0),(8,4096),(12,alloc),(16,free),(20,int(different)),(24,20000)]:put(m,PARAM+offset,value)
   if call(0x209820c,[work+8,PARAM]):error(9,-24100)
   else:
    good=call(0x2097dc4,[CAL])and call(0x2097fac,[word(m,G)+8,CAL,0])
    good=good and not call(0x2098954,[word(m,G)+8,TAGS['action'],TAGS['SVCLOC'],6])and not call(0x2098954,[word(m,G)+8,TAGS['svc'],SVC,4])
    good=good and not call(0x20982e4,[word(m,G)+8])
    if good:
     priority=call(0x2006b74,[word(m,TI+4)]);call(0x209834c,[word(m,G)+8,priority-1]);good=word(m,word(m,G)+7084)!=0
    if good:result=1
    else:call(0x20987b0,[word(m,G)+8]);error(9,-24100)
 elif address==0x209a03c:
  http=word(m,G)+8;code=SP-16
  if not call(0x2098d0c,[http,0]):error(16,-25101)
  else:
   date=call(0x2098ed8,[http,TAGS['Date']])
   if date:call(0x2099bf8,[date])
   text=call(0x2098ed8,[http,TAGS['httpresult']])
   if not text:error(16,-25101)
   else:
    status=call(0x201f274,[text])
    if word(m,E)==34:error(16,-25101)
    elif status!=200:error(16,-25000-status)
    else:
     decoded=call(0x2098f14,[http,TAGS['returncd'],code,4]);decoded=decoded-(1<<32)if decoded&0x80000000 else decoded
     if decoded<=0:error(16,-25101)
     else:
      status=call(0x201f274,[code]);status=status-(1<<32)if status&0x80000000 else status
      if word(m,E)==34:error(16,-25101)
      elif status>=100:error(16,-24000-status)
      else:
       passed=True
       for key,offset,cap in [('svchost',4,64),('servicetoken',69,300),('statusdata',None,1)]:
        output=code if offset is None else word(m,word(m,G)+7196)+offset;r=call(0x2098f14,[http,TAGS[key],output,cap])
        if r&0x80000000:passed=False;break
       if not passed:error(16,-25101)
       else:put(m,word(m,word(m,G)+7196),int(m.read(code,1)==b'Y'));result=1
 else:raise ValueError('Outside selected SVL request/result')
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'stopped'if stopped else'ARM R0 word',result

def expected_reads(address,v):
 if address!=0x209a03c:return []
 m,args=initial(address,v)
 if not v.get('parse',1)or not v.get('httpFound',True):return []
 e=v.get('errnoAfterStatus',v.get('initialErrno',0));out=[(E,4,e)]
 if e!=34 and v.get('status',200)==200 and v.get('decodeCode',len(str(v.get('returnCode',0))))>0:out.append((E,4,v.get('errnoAfterCode',e)))
 return out

def cases(address):
 if address==0x2099df4:
  failures=[{},dict(create=1),dict(create=-1),dict(cal=0),dict(calPost=0),dict(postAction=1),dict(postService=1),dict(finish=1),dict(startedId=0)]
  return[dict(callbackMode=c,customUrl=u,**failure)for c in range(4)for u in [False,True]for failure in failures]+[dict(threadId=i,terminated=t,callbackMode=c)for i in [0,1,0xffffffff]for t in [-1,0,1,2]for c in [0,3]]+[dict(callbackMode=c,**flags)for c in [0,3]for flags in [{'clearSwapsWork':True},{'probeSwapsWork':True,'threadId':1},{'compareSwapsWork':True},{'createSwapsWork':True},{'startSwapsWork':True},{'priority':0},{'priority':1},{'priority':31,'otherThread':True}]]
 if address==0x209a03c:
  states=[{},dict(parse=0),dict(httpFound=False),dict(initialErrno=34),dict(errnoAfterStatus=34),dict(errnoAfterCode=34),dict(status=0),dict(status=201),dict(status=500),dict(status=-1),dict(decodeCode=-1),dict(decodeCode=0),dict(returnCode=99),dict(returnCode=100),dict(returnCode=999),dict(returnCode=-1),dict(decodeHost=-1),dict(decodeHost=0),dict(decodeToken=-1),dict(decodeToken=0),dict(decodeStatus=-1),dict(decodeStatus=0)]+[dict(statusByte=b)for b in [0,78,89,128,255]]
  return[dict(**state,**flags)for state in states for flags in [{},{'date':True},{'date':True,'dateSwapsWork':True},{'decodeSwapsWork':True}]]
 raise ValueError('No bounded SVL request/result cases')
