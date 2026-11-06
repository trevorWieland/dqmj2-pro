import re
from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_first_models import Memory,word,put
H,URL,B1,B2,STATE=0x2170000,0x2173000,0x2175000,0x2177000,0x2179000
SP,STOP,MAGIC,DIV=0x2701000,0x27e0000,0,0
OBSERVED=set()
ARITY={0x201d69c:1,0x201d780:3,0x201d984:2,0x201f274:1,0x200708c:1,0x2007110:1}
DATA={int(at,0):bytes.fromhex(v['expectedHex'])for at,v in read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/fourth/original-imports.json')['dataViews'].items()}
TAGS={raw[:-1]:at for at,raw in DATA.items()}
def dynamic_callbacks(v):return {}
def expected_reads(address,v):return []
def cstring(m,at):
 out=bytearray()
 for i in range(2048):
  x=m.read(at+i,1)
  if x==bytes([0]):return bytes(out)
  out+=x
 raise ValueError('Outside bounded parser CString')
def encoded(v,key,default=''):return v.get(key,default).encode('latin1')
def initial(address,v):
 m=Memory({**DATA,H:bytes((i*13+3)&255 for i in range(7188)),URL:bytes(4096),B1:bytes(4096),B2:bytes(4096),STATE:bytes(128),SP-0x1000:bytes(4096)})
 m.write(URL,encoded(v,'url')+bytes([0]));a=encoded(v,'response');b=encoded(v,'alternate','HTTP/1.0 200 OK\r\nContent-Length: 71\r\n\r\nabc')
 m.write(B1,a+bytes([0]));m.write(B2,b+bytes([0]));put(m,H+0x1a08,B1);put(m,H+0x1a0c,B1+len(a)+v.get('indexDelta',0));put(m,H+0x1a30,0xfffffffe);put(m,H+0x1a34,0xffffffff)
 return m,[H,URL]if address==0x2098b44 else[H]
def integer(raw):
 match=re.match(rb'[ \t\n\r\v\f]*([+-]?[0-9]+)',raw)
 return int(match[1])&0xffffffff if match else 0
def effect(at,a,m,v):
 result=0x76543210;norm=a[:]
 if at==0x201d69c:raw=cstring(m,a[0]);result=len(raw);norm=a+[raw.hex()]
 elif at==0x201d780:
  raw=cstring(m,a[1]);raw=raw[:v['copyTruncate']]if 'copyTruncate'in v else raw
  output=raw[:a[2]].ljust(a[2],bytes([0]));m.write(a[0],output);result=a[0];norm=a+[output.hex()]
 elif at==0x201d984:
  left,right=cstring(m,a[0]),cstring(m,a[1]);i=left.find(right);result=a[0]+i if i>=0 else 0;norm=a+[left.hex(),right.hex()]
 elif at==0x201f274:raw=cstring(m,a[0]);result=integer(raw);norm=a+[raw.hex()]
 elif at==0x200708c:
  count=word(m,STATE);put(m,STATE,count+1)
  if count==0 and v.get('lockChangesIndex'):put(m,H+0x1a0c,word(m,H+0x1a0c)+v.get('changedDelta',9))
 elif at==0x2007110:
  count=word(m,STATE+4);put(m,STATE+4,count+1)
  if count==0 and v.get('unlockChangesBuffer'):put(m,H+0x1a08,B2)
 else:raise ValueError(('Outside parser provider contract',hex(at)))
 return result&0xffffffff,norm

def model(address,v):
 m,args=initial(address,v);calls=[];result=0
 def call(at,a):
  r,norm=effect(at,[x&0xffffffff for x in a],m,v);calls.append((hex(at),norm));return r
 if address==0x2098b44:
  if call(0x201d69c,[URL])<256:
   call(0x201d780,[H+4132,URL,256]);originalLength=call(0x201d69c,[URL]);copiedLength=call(0x201d69c,[H+4132])
   if originalLength==copiedLength:
    found=call(0x201d984,[H+4132,TAGS[b'http://']]);host=0
    if found:host=H+4132+7;put(m,H+4400,0);put(m,H+4404,80,2)
    else:
     found=call(0x201d984,[H+4132,TAGS[b'https://']])
     if found:host=found+8;put(m,H+4400,1);put(m,H+4404,443,2)
    if host:
     put(m,H+4388,host);port=call(0x201d984,[host,TAGS[b':']])
     if port:m.write(port,bytes([0]))
     path=call(0x201d984,[host,TAGS[b'/']])
     if path:m.write(path,bytes([0]))
     put(m,H+4392,path+1 if path else 0)
     if port:put(m,H+4404,call(0x201f274,[port+1]),2)
     result=1
 elif address==0x20984d0:
  start=word(m,H+0x1a08);head=call(0x201d984,[start,TAGS[b'\r\n\r\n']])
  if head:
   body=call(0x201d984,[start,TAGS[b'\r\n\r\n']])+4;call(0x200708c,[H+0x1a18]);put(m,H+0x1a34,word(m,H+0x1a0c)-body);call(0x2007110,[H+0x1a18])
   value=call(0x201d984,[word(m,H+0x1a08),TAGS[b'Content-Length: ']])
   if value:
    labelSize=call(0x201d69c,[TAGS[b'Content-Length: ']]);end=call(0x201d984,[value+labelSize,TAGS[b'\r\n']]);previous=m.read(end,1);m.write(end,bytes([0]));call(0x200708c,[H+0x1a18]);put(m,H+0x1a30,call(0x201f274,[value+labelSize]));call(0x2007110,[H+0x1a18]);m.write(end,previous)
   result=1
 else:raise ValueError('Outside parser packet')
 return {at:bytes(raw)for at,raw in m.regions.items()if at!=SP-0x1000},calls,'ARM R0 word',result

def cases(address):
 if address==0x2098b44:
  urls=['','ftp://bad','HTTP://host','http://','https://','http://host','http://host/','http://host/a','https://host:443/a','http://host:0','http://host:-1','http://host:65535','http://host:70000','http://host:bad','xxhttp://host/path','xxhttps://host/path','https://host/foo:90','http://host/path:44','http://h\x80/path']
  urls+=['http://'+('a'*(n-7))for n in [254,255,256,257]]
  return [dict(url=url,**flags)for url in urls for flags in [{},{'copyTruncate':3}]]
 if address==0x20984d0:
  responses=['','HTTP/1.1 200 OK\r\n','HTTP/1.1 200 OK\r\n\r\n','HTTP/1.1 200 OK\r\n\r\nabcdef']
  responses+=['HTTP/1.1 200 OK\r\nContent-Length: '+x+'\r\n\r\nabc'for x in ['','0','1','7','65535','-1','+23','  004','invalid','77tail']]
  responses+=['HTTP/1.1 200 OK\r\n\r\nContent-Length: 99\r\n','HTTP/1.1 200 OK\r\ncontent-length: 14\r\n\r\nx']
  return [dict(response=response,indexDelta=n,**flags)for response in responses for n in [-1,0,7]for flags in [{},{'lockChangesIndex':True},{'unlockChangesBuffer':True},{'lockChangesIndex':True,'unlockChangesBuffer':True}]]
 raise ValueError('No parser packet cases')
