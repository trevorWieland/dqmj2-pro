from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
ER,AL=0x21d19ac,0x21d19b4
KEY,VALUE,SOURCE,OUT,O0,O1,OLD,NEW,ST=0x2170000,0x2171000,0x2172000,0x2174000,0x2176000,0x2176100,0x2177000,0x2178000,0x2179000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
AP,AT,FP,FT=0x2234000,0x2234004,0x2234100,0x2234104
ARITY={AP:3,AT:3,FP:3,FT:3,0x20061ac:7,0x201d69c:1,0x201d948:2,0x201d914:3,0x201d780:3,0x209aa10:2,0x209aa0c:1,0x209aa98:5,0x209aa44:3,0x209aa20:1,0x2008e0c:3,0x209aa64:3}
OBSERVED=set()
DATA={int(at,0):bytes.fromhex(v['expectedHex'])for at,v in read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/tenth/original-imports.json')['dataViews'].items()if v['storage']=='data'}
TYPES=[0,7,6,6,6,6,3,4,6,7,1,1,1,1,5,6,2,6,2,6,2,2]
def dynamic_callbacks(v):return{AP:dict(mode='arm'),AT:dict(mode='thumb'),FP:dict(mode='arm'),FT:dict(mode='thumb')}
def expected_reads(address,v):return []
def alloc(v):return AT|1 if v.get('callbackMode',0)&1 else AP
def free(v):return FT|1 if v.get('callbackMode',0)&2 else FP
def s8(n):return n-256 if n&128 else n
def raw(v,key,default=''):return v.get(key,default).encode('latin1')
def cstring(m,at):
 out=bytearray()
 for index in range(4096):
  b=m.read(at+index,1)
  if b==bytes([0]):return bytes(out)
  out+=b
 raise ValueError('Outside bounded SDK string')
def initial(address,v):
 m=Memory({**DATA,ER:bytes(8),AL:bytes(8),KEY:bytes(512),VALUE:bytes(512),SOURCE:bytes(4096),OUT:bytes([0xa5])*4096,O0:bytes([0x77])*16,O1:bytes([0x88])*16,OLD:bytes((i*13+3)&255 for i in range(512)),NEW:bytes([0x66])*512,ST:bytes(128),SP-0x1000:bytes(4096)})
 put(m,ER,v.get('error',0));put(m,ER+4,v.get('errorCode',77));put(m,AL,free(v));put(m,AL+4,alloc(v));m.write(KEY,raw(v,'key','key')+bytes([0]));m.write(VALUE,raw(v,'value','value')+bytes([0]));m.write(SOURCE,raw(v,'string','|key|value')+bytes([0]));put(m,OLD,0x4457434d);put(m,OLD+4,v.get('oldLength',16));put(m,NEW,0x4457434d);put(m,NEW+4,v.get('newLength',8))
 code=0 if v.get('nullCode')else ER if v.get('codeAliasesError')else O0;kind=0 if v.get('nullType')else ER if v.get('typeAliasesError')else ER+4 if v.get('typeAliasesCode')else O1;pointer=0 if v.get('nullOld')else OLD+32;separator=s8(v.get('separator',124)&255)
 args={0x209a944:[code,kind],0x209a9d0:[],0x209aa44:[v.get('tag',3),v.get('newLength',8),v.get('align',32)],0x209aa64:[v.get('tag',3),pointer,v.get('oldArgument',999)],0x209aa88:[v.get('tag',3),pointer,v.get('oldArgument',999),v.get('newLength',8)],0x209aa98:[v.get('tag',3),pointer,v.get('oldArgument',999),v.get('newLength',8),v.get('align',32)],0x209b26c:[KEY,VALUE,OUT,separator],0x209b2bc:[KEY,0 if v.get('nullOut')else OUT,SOURCE,separator]}
 return m,args[address]
def effect(at,a,m,v):
 result=0x76543210;norm=a[:]
 if at in [AP,AT]:result=0 if v.get('allocationFails')else NEW
 elif at in [FP,FT]:put(m,ST+4,word(m,ST+4)+1)
 elif at==0x209aa10:put(m,a[0],0x4457434d);put(m,a[0]+4,a[1]);result=a[0]+32
 elif at==0x209aa0c:result=a[0]-32
 elif at==0x209aa20:result=word(m,a[0]-28)
 elif at==0x209aa98:result=0 if v.get('allocationFails')else NEW+32
 elif at==0x209aa44:
  result=0 if v.get('allocationFails')else NEW+32
  if result:put(m,NEW,0x4457434d);put(m,NEW+4,a[1])
 elif at==0x2008e0c:payload=m.read(a[0],a[2]);m.write(a[1],payload);norm=a+[payload.hex()]
 elif at==0x209aa64:put(m,ST+8,word(m,ST+8)+1)
 elif at==0x201d69c:payload=cstring(m,a[0]);result=len(payload);norm=a+[payload.hex()]
 elif at==0x201d948:
  payload=cstring(m,a[0]);index=(payload+bytes([0])).find(bytes([a[1]&255]));result=a[0]+index if index>=0 else 0;norm=a+[payload.hex()]
 elif at==0x201d914:
  left,right=cstring(m,a[0])[:a[2]],cstring(m,a[1])[:a[2]];result=0 if left==right else 1 if left>right else 0xffffffff;norm=a+[left.hex(),right.hex()]
 elif at==0x201d780:
  payload=cstring(m,a[1])[:a[2]].ljust(a[2],bytes([0]));m.write(a[0],payload);result=a[0];norm=a+[payload.hex()]
 elif at==0x20061ac:
  key,value=cstring(m,a[4]),cstring(m,a[6]);payload=bytes([a[3]&255])+key+bytes([a[5]&255])+value;output=payload[:max(0,a[1]-1)]+bytes([0]);m.write(a[0],output);result=len(payload);norm=a+[cstring(m,a[2]).hex(),key.hex(),value.hex()]
 else:raise ValueError(('Outside SDK common/memory provider',hex(at)))
 return result&0xffffffff,norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0;contract='ARM R0 word'
 def call(at,a):
  r,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return r
 if address==0x209a944:
  if args[0]:put(m,args[0],word(m,ER+4))
  if args[1]:e=word(m,ER);put(m,args[1],TYPES[e]if e<len(TYPES)else 0)
  result=word(m,ER)
 elif address==0x209a9d0:
  contract='void'
  if word(m,ER)!=9:put(m,ER,0);put(m,ER+4,0)
 elif address==0x209aa44:
  pointer=call(word(m,AL+4)&~1,[args[0],args[1]+32,args[2]])
  if pointer:result=call(0x209aa10,[pointer,args[1]])
 elif address==0x209aa64:
  contract='void'
  if args[1]:pointer=call(0x209aa0c,[args[1]]);call(word(m,AL)&~1,[args[0],pointer,word(m,pointer+4)+32])
 elif address==0x209aa88:result=call(0x209aa98,args+[32])
 elif address==0x209aa98:
  result=call(0x209aa44,[args[0],args[3],args[4]])
  if result and args[1]:old=call(0x209aa20,[args[1]]);call(0x2008e0c,[args[1],result,min(old,args[3])]);call(0x209aa64,[args[0],args[1],old])
 elif address==0x209b26c:
  call(0x20061ac,[OUT,4096,next(iter(DATA)),args[3],KEY,args[3],VALUE]);result=call(0x201d69c,[OUT])
 elif address==0x209b2bc:
  result=0xffffffff
  if args[1]:
   sep=args[3]&255;p=call(0x201d948,[SOURCE,args[3]])
   while p:
    n=call(0x201d69c,[KEY]);same=call(0x201d914,[p+1,KEY,n])==0
    if same:
     n=call(0x201d69c,[KEY])
     if m.read(p+n+1,1)==bytes([sep]):break
    p=call(0x201d948,[p+1,args[3]])
    if not p:break
    p=call(0x201d948,[p+1,args[3]])
   if p:
    p=call(0x201d948,[p+1,args[3]])
    if p:
     begin=p+1;end=call(0x201d948,[begin,args[3]]);n=end-begin if end else call(0x201d69c,[begin]);call(0x201d780,[OUT,begin,n]);m.write(OUT+n,bytes([0]));result=n
 else:raise ValueError('Outside common/memory subset')
 if address==0x209b2bc:
  wanted=None
  if not v.get('nullOut'):
   source=raw(v,'string','|key|value');sep=bytes([v.get('separator',124)&255]);first=source.find(sep)
   if first>=0:
    tokens=source[first+1:].split(sep)
    for index in range(0,len(tokens)-1,2):
     if tokens[index]==raw(v,'key','key'):wanted=tokens[index+1];break
  oracle=0xffffffff if wanted is None else len(wanted)
  if result&0xffffffff!=oracle or wanted is not None and cstring(m,OUT)!=wanted:raise ValueError('Independent split-pair key/value oracle differs')
 return{at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,contract,result&0xffffffff

def cases(address):
 if address==0x209a944:return[dict(error=e,errorCode=c,**flags)for e in [-1,0,1,2,6,7,9,13,14,16,19,20,21,22,0x7fffffff]for c in [0,9,77]for flags in [{},{'nullCode':True},{'nullType':True},{'nullCode':True,'nullType':True},{'codeAliasesError':True},{'typeAliasesError':True},{'typeAliasesCode':True}]]
 if address==0x209a9d0:return[dict(error=e,errorCode=c)for e in [-1,0,1,8,9,10,20,21,22]for c in [0,77,0xffffffff]]
 if address in [0x209aa44,0x209aa64,0x209aa88,0x209aa98]:return[dict(newLength=n,oldLength=o,nullOld=z,allocationFails=f,callbackMode=c,align=a,oldArgument=argument)for n,o in [(0,0),(0,16),(1,16),(16,1),(16,16),(32,64)]for z in [False,True]for f in [False,True]for c in [0,3]for a in [-32,0,32]for argument in [0,999]]
 if address==0x209b26c:return[dict(key=k,value=value,separator=s)for k,value in [('', ''),('a','b'),('key','value'),('x'*127,'y'*127)]for s in [0,1,32,59,124,127,128,255]]
 if address==0x209b2bc:
  examples=[('key',''),('key','noise'),('key','|other|x'),('key','|key|'),('key','|key|value'),('key','|key|value|'),('key','prefix|other|x|key|v|'),('key','|keyX|bad|key|good'),('','||empty'),('x'*20,'|'+'x'*20+'|value')]
  return[dict(key=key,string=text.replace('|',chr(sep)),separator=sep,nullOut=z)for key,text in examples for sep in [1,59,124,128,255]for z in [False,True]]
 raise ValueError('No common/memory cases')
