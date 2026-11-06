import zlib

def ksa(key,n):
 s=[i&255 for i in range(n)];j=k=0
 for i in range(n):j=(j+key[k]+s[i])%n;s[j],s[i]=s[i],s[j];k+=1;k=0 if k>=len(key)else k
 return s

def step(x,y,s,n):
 x=(((x+1)&0xffffffff)%n)&255;a=s[x];y=(((y+a)&0xffffffff)%n)&255;b=s[y];s[y]=a;s[x]=b;return x,y,s[(a+b)%n]

def crc_table():
 out=[]
 for i in range(256):
  bits=i
  for j in range(8):bits=bits>>1^(0xedb88320 if bits&1 else 0)
  out.append(bits)
 return out

def crc(seed,data,table):
 for b in data:seed=seed>>8^table[(seed^b)&255]
 return seed

def selfcheck():
 s=ksa(bytes([1,2,3,4,5]),256);x=y=0;out=[]
 for i in range(16):x,y,b=step(x,y,s,256);out.append(b)
 assert bytes(out).hex()=='b2396305f03dc027ccc3524a0a1118a8';t=crc_table();assert crc(0xffffffff,b'123456789',t)^0xffffffff==zlib.crc32(b'123456789')==0xcbf43926
 return dict(allPassed=True,rfc6229Key0102030405First16='b2396305f03dc027ccc3524a0a1118a8',standardCrcCheck='cbf43926')

def cases(address):
 if address==0x21ed86c:return[dict(n=n,keyLength=k)for n,k in[(0,1),(1,1),(2,3),(16,1),(16,3),(255,16),(256,5),(300,5),(16,0)]]
 if address==0x21ed8fc:return[dict(n=n,x=x,y=y)for n,x,y in[(1,0,0),(16,0,0),(255,254,254),(256,255,255),(300,299,299),(256,0xffffffff,0xffffffff)]]
 if address==0x21ed8d0:return[dict(n=n,length=length,alias=alias)for n,length,alias in[(256,0,0),(256,1,0),(256,16,0),(256,33,1),(16,17,2),(300,64,0)]]
 if address==0x21ed964:return[dict(ready=r,length=n,seed=s)for r,n,s in[(0,0,0),(0,9,0xffffffff),(1,9,0xffffffff),(1,1,0),(2,33,0x12345678),(0,-3,0xabcdef01),(1,0,0xffffffff),(1,64,0xffffffff)]]
 return[dict(alias=x,offset=y)for x,y in[(0,0),(0,1),(1,0),(2,0),(3,0),(4,0)]]
