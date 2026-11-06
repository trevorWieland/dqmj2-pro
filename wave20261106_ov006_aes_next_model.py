def mul(a,b):
 value=0
 for unused in range(8):
  if b&1:value^=a
  a=((a<<1)^0x11b)if a&128 else a<<1;b>>=1
 return value&255

def power(a,n):
 result=1
 while n:
  if n&1:result=mul(result,a)
  a=mul(a,a);n>>=1
 return result

def rol8(a,n):return((a<<n)|(a>>(8-n)))&255
SBOX=[(lambda q:q^rol8(q,1)^rol8(q,2)^rol8(q,3)^rol8(q,4)^0x63)(power(x,254)if x else 0)for x in range(256)]
INV=[SBOX.index(x)for x in range(256)]

def subword(word):return int.from_bytes(bytes(SBOX[x]for x in word.to_bytes(4,'big')),'big')
def schedule(key,bits):
 if bits not in[128,192,256]:return[int.from_bytes(key[i:i+4],'big')for i in range(0,32,4)],0
 count=bits//32;rounds=count+6;words=[int.from_bytes(key[i:i+4],'big')for i in range(0,bits//8,4)];rc=1
 while len(words)<4*(rounds+1):
  i=len(words);temp=words[-1]
  if i%count==0:temp=subword(((temp<<8)|(temp>>24))&0xffffffff)^(rc<<24);rc=mul(rc,2)
  elif count==8 and i%count==4:temp=subword(temp)
  words.append(words[i-count]^temp)
 return words,rounds

def mixcolumn(column,inverse=False):
 matrix=([14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14])if inverse else([2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2])
 return[fold([mul(a,b)for a,b in zip(row,column)])for row in matrix]

def fold(values):
 result=0
 for value in values:result^=value
 return result

def decrypt_schedule(key,bits):
 words,rounds=schedule(key,bits)
 if not rounds:return words,rounds
 result=[]
 for r in range(rounds,-1,-1):
  row=words[r*4:r*4+4]
  if r not in[0,rounds]:row=[int.from_bytes(bytes(mixcolumn(w.to_bytes(4,'big'),True)),'big')for w in row]
  result.extend(row)
 return result,rounds

def addkey(state,words):return[a^b for a,b in zip(state,b''.join(w.to_bytes(4,'big')for w in words))]
def shift(state,inverse=False):return[state[4*((c-r if inverse else c+r)%4)+r]for c in range(4)for r in range(4)]
def mix(state,inverse=False):return[x for c in range(4)for x in mixcolumn(state[c*4:c*4+4],inverse)]
def encrypt(key,bits,plain):
 words,rounds=schedule(key,bits);state=addkey(list(plain),words[:4])
 for r in range(1,rounds+1):
  state=shift([SBOX[x]for x in state])
  if r!=rounds:state=mix(state)
  state=addkey(state,words[4*r:4*r+4])
 return bytes(state)

def decrypt(key,bits,cipher):
 words,rounds=schedule(key,bits);state=addkey(list(cipher),words[4*rounds:4*rounds+4])
 for r in range(rounds-1,-1,-1):
  state=[INV[x]for x in shift(state,True)];state=addkey(state,words[4*r:4*r+4])
  if r:state=mix(state,True)
 return bytes(state)

def cases(address):
 rows=[]
 if address in[0x21f0944,0x21f0bfc]:
  for bits in[128,192,256,0,64,129,512,-1]:
   for style in[0,1]:rows.append(dict(bits=bits,style=style,offset=style))
 else:
  for bits in[128,192,256]:
   for style,inplace,offset in[(0,0,0),(1,0,1),(2,0,0),(3,1,1)]:rows.append(dict(bits=bits,style=style,inplace=inplace,offset=offset))
 return rows

def key_and_plain(vector):
 style=vector['style'];key=bytes(range(32))if style==0 else bytes(32)if style==1 else bytes([255])*32 if style==2 else bytes((i*7+3)&255 for i in range(32));plain=bytes.fromhex('00112233445566778899aabbccddeeff')if style==0 else bytes(16)if style==1 else bytes([255])*16 if style==2 else bytes((i*11+5)&255 for i in range(16));return key,plain

def selfcheck():
 expected={128:'69c4e0d86a7b0430d8cdb78070b4c55a',192:'dda97ca4864cdfe06eaf70a0ec0d7191',256:'8ea2b7ca516745bfeafc49904b496089'}
 for bits,value in expected.items():
  key,plain=key_and_plain(dict(style=0));cipher=encrypt(key,bits,plain)
  if cipher.hex()!=value or decrypt(key,bits,cipher)!=plain:raise ValueError('Independent finite-field known-answer model failed')
 return dict(allPassed=True,roundTrips=3,knownAnswers=expected,fieldPolynomial='0x11b',sboxConstructedByInverseAndAffineMap=True,tableWordsOrCompiledCNotUsed=True)
