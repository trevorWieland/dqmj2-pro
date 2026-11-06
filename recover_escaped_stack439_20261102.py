import re
CONTRACTS={'020b2ae0':(2,3),'020b2a38':(0,2),'0201d780':(0,2),'02008d78':(0,2),'02008c14':(1,2),'02008be0':(1,2)}
def arguments(text,start):
 depth=1;parts=[];mark=start+1
 for pos in range(start+1,len(text)):
  token=text[pos]
  if token=='(':depth+=1
  elif token==')':
   depth-=1
   if depth==0:parts.append(text[mark:pos].strip());return parts
  elif token==',' and depth==1:parts.append(text[mark:pos].strip());mark=pos+1
 raise AssertionError('UnclosedCall')
def frame_extent(assembly):
 extent=0;started=False
 for line in assembly.splitlines():
  line=line.strip()
  if not line or line.startswith('.') or line.endswith(':'):continue
  if line.startswith('push '):started=True;continue
  match=re.fullmatch(r'sub sp(?:, sp)?, #(0x[0-9a-fA-F]+|[0-9]+)',line)
  if match:extent+=int(match[1],0);started=True;continue
  if started:break
 return extent
def apply(raw,assembly):
 original=raw;frame=frame_extent(assembly);declarations={m[2]:(m[1],m.group(),m.start(),m.end()) for m in re.finditer(r'^\s*(u8|s8|M2C_UNK)\s+(sp[0-9A-Fa-f]+);',raw,re.M)};offsets=sorted({int(x,16) for x in re.findall(r'\bsp([0-9A-Fa-f]+)\b',raw)});requests={};receipts=[];rejected=[]
 for match in re.finditer(r'\b(?:func_|native_fn_)(020[0-9a-fA-F]{5})\s*\(',raw):
  key=match[1].lower()
  if key not in CONTRACTS:continue
  args=arguments(raw,raw.index('(',match.start()));slot,count=CONTRACTS[key]
  if max(slot,count)>=len(args):continue
  address=re.fullmatch(r'(?:\([^)]*\)\s*)?&\s*(sp[0-9A-Fa-f]+)',args[slot]);length=re.fullmatch(r'(0x[0-9a-fA-F]+|[0-9]+)[uUlL]*',args[count])
  if address and length and address[1] in declarations:requests.setdefault(address[1],[]).append(dict(callee=key,bytes=int(length[1],0),outputArgument=slot,lengthArgument=count))
 for name,uses in requests.items():
  kind,declaration,start,end=declarations[name];offset=int(name[2:],16);length=max(x['bytes'] for x in uses);neighbor=min([x for x in offsets if x>offset]+[frame]);refs=list(re.finditer(r'\b'+name+r'\b',original));address_only=all(start<=m.start()<end or original[:m.start()].rstrip().endswith('&') for m in refs)
  if not(0<length<=0x10000 and offset+length<=frame and offset+length<=neighbor and address_only):rejected.append(dict(local=name,offset=offset,bytes=length,frame=frame,neighbor=neighbor,addressOnly=address_only));continue
  replacement=declaration.replace(kind+' '+name+';',('u8' if kind=='M2C_UNK' else kind)+' '+name+'['+hex(length)+'];');raw=raw.replace(declaration,replacement,1);receipts.append(dict(local=name,offset=offset,bytes=length,frame=frame,nextNamedSlot=neighbor,requests=uses,qualification='Bounded escaped-output storage hypothesis fromliteral call words+nativeprologue frame;callee output semantics/sourceABI andcallerpaths separatelyunqualified'))
 return raw,dict(frameBytes=frame,recovered=receipts,rejected=rejected,scope='Freshsource only;nopadding,forcedregisters orunknownsaved-state initialization')
def controls():
 asm='push {r4, lr}\nsub sp, sp, #0x40\nmov r4, r0\n';good='    M2C_UNK sp10;\n    func_020b2ae0(arg0, arg1, &sp10, 0x20);\n';text,proof=apply(good,asm);assert 'u8 sp10[0x20];' in text and len(proof['recovered'])==1
 for bad in (good.replace('0x20','0x40'),good+'    u32 sp20;\n',good+'    x = sp10;\n',good.replace('0x20','n')):
  text,proof=apply(bad,asm);assert not proof['recovered']
 return 5
