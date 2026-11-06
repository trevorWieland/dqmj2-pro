import math,struct,hashlib
MASK=0xffffffff
K=[int(abs(math.sin(i+1))*2**32)&MASK for i in range(64)]
SHIFTS=([7,12,17,22]*4+[5,9,14,20]*4+[4,11,16,23]*4+[6,10,15,21]*4)
IV=[0x67452301,0xefcdab89,0x98badcfe,0x10325476]

def compress(state,block):
 words=struct.unpack('<16I',block);a,b,c,d=state
 for i in range(64):
  if i<16:f=(b&c)|(~b&d);g=i
  elif i<32:f=(d&b)|(~d&c);g=(5*i+1)%16
  elif i<48:f=b^c^d;g=(3*i+5)%16
  else:f=c^(b|~d);g=(7*i)%16
  n=(a+f+K[i]+words[g])&MASK;s=SHIFTS[i];n=((n<<s)|(n>>(32-s)))&MASK;a,b,c,d=d,(b+n)&MASK,b,c
 return[(state[0]+a)&MASK,(state[1]+b)&MASK,(state[2]+c)&MASK,(state[3]+d)&MASK]

def context():return bytearray(struct.pack('<4I2I',*IV,0,0)+bytes([0xa5])*64)

def update(ctx,payload):
 out=bytearray(ctx);state=list(struct.unpack('<4I',out[:16]));count=struct.unpack('<Q',out[16:24])[0];index=(count>>3)&63;out[16:24]=struct.pack('<Q',(count+8*len(payload))&((1<<64)-1));part=64-index;i=0
 if len(payload)>=part:
  out[24+index:88]=payload[:part];state=compress(state,out[24:88]);i=part
  while i+63<len(payload):state=compress(state,payload[i:i+64]);i+=64
  index=0
 out[24+index:24+index+len(payload)-i]=payload[i:];out[:16]=struct.pack('<4I',*state);assert len(out)==88;return out

def final(ctx):
 count=struct.unpack('<Q',ctx[16:24])[0];index=(count>>3)&63;pad=(56 if index<56 else 120)-index;out=update(ctx,b'\x80'+bytes(pad-1));out=update(out,struct.pack('<Q',count));return bytes(out[:16]),bytearray(88)

def pattern(n,style=0):return bytes((i*37+style*71+13)&255 for i in range(n))

def selfcheck():
 vectors=[b'',b'a',b'abc',pattern(55),pattern(56),pattern(64),pattern(200)];records=[]
 for message in vectors:
  digest,_=final(update(context(),message));assert digest==hashlib.md5(message).digest();records.append(dict(length=len(message),digest=digest.hex()))
 return dict(allPassed=True,independent64StepCompressionConstantsDerivedFromSine=True,standardHashlibKnownAnswerCrossChecks=records)

def cases(address):
 if address==0x21f15f8:return[dict(style=s)for s in range(6)]
 if address==0x21f152c:
  out=[dict(prefix=[0,13,55,56,63][i%5],length=n,offset=i%2,wrap=False)for i,n in enumerate([0,1,7,55,56,63,64,65,127,128,129,192])]
  out.extend(dict(prefix=p,length=n,offset=1,wrap=False)for p,n in[(63,0),(63,1),(55,9),(0,64)])
  out.extend(dict(prefix=63,length=n,offset=0,wrap=True)for n in[1,65]);return out
 return[dict(length=n,style=i%3,offset=i%2)for i,n in enumerate([0,1,3,55,56,63,64,65,119,120,127,128,129,200])]
