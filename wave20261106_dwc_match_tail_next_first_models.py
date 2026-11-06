from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
CONNECTION,MESSAGE,SOURCE,DEST=0x2170000,0x2171000,0x2172000,0x2173000
ARITY={0x20061ac:6,0x201d69c:1,0x201d948:2,0x2008e0c:3,0x20aa7c0:3}
OBSERVED=set()
IMPORTS=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/first/original-imports.json')
STRINGS={bytes.fromhex(v['expectedHex'])[:-1]:int(a,0)for a,v in IMPORTS['dataViews'].items()}

def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def cstring(m,a):
 out=bytearray()
 while len(out)<1024:
  b=m.read(a+len(out),1)
  if b==bytes([0]):return bytes(out)
  out.extend(b)
 raise ValueError('Unterminated bounded input string')

def initial(address,v):
 message=bytes.fromhex(v.get('messageHex','61'));source=bytes.fromhex(v.get('sourceHex','612f622f63'));assert len(message)<1024 and len(source)<1024
 regions={CONNECTION:bytes([0x55])*4,MESSAGE:message+bytes(1024-len(message)),SOURCE:source+bytes(1024-len(source)),DEST:bytes([0xa5])*1024,SP-0x1000:bytes(4096)}
 for a,view in IMPORTS['dataViews'].items():regions[int(a,0)]=bytes.fromhex(view['expectedHex'])
 m=Memory(regions);args=[CONNECTION,v.get('command',1),v.get('profile',123),0 if v.get('nullMessage')else MESSAGE]if address==0x20a02b4 else[DEST,SOURCE,v.get('index',0)]
 return m,args

def effect(at,a,m,v):
 norm=a[:];result=0x76543210
 if at==0x20061ac:
  fmt,prefix,suffix=cstring(m,a[2]),cstring(m,a[3]),cstring(m,a[5]);assert fmt==b'%s%dv%s';text=prefix+str(a[4]).encode()+b'v'+suffix;size=a[1];assert 1<=size<=512;m.write(a[0],text[:size-1]+bytes([0]));result=len(text);norm+=[fmt.hex(),prefix.hex(),suffix.hex()]
 elif at==0x201d69c:raw=cstring(m,a[0]);result=len(raw);norm+=[raw.hex()]
 elif at==0x201d948:
  raw=cstring(m,a[0])+bytes([0]);index=raw.find(bytes([a[1]&255]));result=0 if index<0 else a[0]+index;norm+=[raw.hex()]
 elif at==0x2008e0c:
  if a[2]>1023:raise ValueError('Unbounded copy contract')
  raw=m.read(a[0],a[2]);m.write(a[1],raw);norm+=[raw.hex()]
 elif at==0x20aa7c0:result=v.get('sentResult',0);norm+=[cstring(m,a[2]).hex()]
 else:raise ValueError(('Outside match command provider boundary',hex(at)))
 return result&0xffffffff,norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0xffffffff
 def call(at,a):
  value,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return value
 if address==0x20a02b4:
  buffer=SP-536;length=call(0x20061ac,[buffer,512,STRINGS[b'%s%dv%s'],STRINGS[b'GPCM'],3,STRINGS[b'MAT']]);m.write(buffer+length,bytes([args[1]&255]));m.write(buffer+length+1,bytes([0]))
  if args[3]:
   size=call(0x201d69c,[args[3]]);count=min(size,512-length-2);call(0x2008e0c,[args[3],buffer+length+1,count]);m.write(buffer+length+1+count,bytes([0]))
  result=call(0x20aa7c0,[CONNECTION,args[2],buffer])
  expected=b'GPCM3vMAT'+bytes([args[1]&255])+(b''if v.get('nullMessage')else bytes.fromhex(v.get('messageHex','61'))[:501]);expected=expected.split(bytes([0]),1)[0];assert cstring(m,buffer)==expected
 else:
  end=call(0x201d948,[SOURCE,0]);begin=SOURCE;index=v.get('index',0);failed=False
  for i in range(max(0,index)):
   next=call(0x201d948,[begin,47])
   if not next:failed=True;break
   begin=next+1
  if not failed:
   next=call(0x201d948,[begin,47])or end
   if begin!=next:count=next-begin;call(0x2008e0c,[begin,DEST,count]);m.write(DEST+count,bytes([0]));result=count
  parts=bytes.fromhex(v.get('sourceHex','612f622f63')).split(b'/');selected=max(0,index);wanted=parts[selected]if selected<len(parts)else b''
  assert result==(len(wanted)if wanted else 0xffffffff)
  if wanted:assert cstring(m,DEST)==wanted
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result

def cases(address):
 if address==0x20a02b4:
  return[dict(nullMessage=True,command=c,profile=p,sentResult=r)for c in [0,1,255]for p in [0,123,0xffffffff]for r in [0,1,0xffffffff]]+[dict(command=c,profile=0xffffffff,sentResult=r,messageHex=(bytes((i%255)+1 for i in range(length))).hex())for c in [0,1,19,64,255]for r in [0,1,0xffffffff]for length in [0,1,500,501,502,700]]
 return[dict(sourceHex=s.hex(),index=i)for s in [b'',b'a',b'/',b'//',b'a/b/c',b'/a/b',b'a/b/',b'a//b',bytes([128,255])+b'/z',b'x'*501+b'/'+b'y'*10]for i in [-2,-1,0,1,2,3,4,10]]
