import hashlib
import re
SYMBOLS={0x0202537C:('u32','f32, f32'),0x02025AB8:('f32','f32, f32'),0x02024E0C:('f32','f32, f32'),0x02025CA4:('f32','f32, f32'),0x020259B4:('s32','f32'),0x020259E8:('u32','f32')}


def arguments(text):
 result=[];start=depth=0
 for i,c in enumerate(text):
  if c in '([':depth+=1
  elif c in ')]':depth-=1
  elif c==',' and depth==0:result.append(text[start:i].strip());start=i+1
 assert depth==0;result.append(text[start:].strip());return result


def context_view(context,assembly):
 receipts=[]
 for address,(result,params) in SYMBOLS.items():
  alias='func_'+format(address,'08x');pattern=r'^extern\s+[^;\n]*\b'+alias+r'\([^;\n]*\);';m=re.search(pattern,context,re.M)
  if m and re.search(r'\b'+alias+r'\b',assembly):
   after='extern '+result+' '+alias+'('+params+');';context=context[:m.start()]+after+context[m.end():];receipts.append(dict(alias=alias,returnType=result,contextPrototype=after,sourcePrototype=after.replace(alias,'native_fn_'+alias.removeprefix('func_')),qualification='measured377-380 binary32 interface;unsigned conversion scope limited384;caller domain unproved'))
 return context,receipts


def lower(raw,assembly):
 lines=[s.strip() for s in assembly.splitlines() if s.strip() and not s.strip().endswith(':') and not s.strip().startswith('.')];calls=[]
 for i,line in enumerate(lines):
  if re.fullmatch(r'bl\s+func_0202537c',line):
   after=lines[i+1:i+5];branches=[j for j,s in enumerate(after) if s.startswith('bls ')]
   assert branches,('UnsupportedCompareFlagBranch',after)
   window=after[:branches[0]];assert all(s.startswith(('ldr ','mov ')) for s in window),('UnsupportedFlagLiveness',window);calls.append(dict(callIndex=i,following=after[:branches[0]+1]))
 pattern=r'func_0202537c\(([^\n]*)\);(?P<between>(?:\n[ \t]*(?:temp|var)_r[0-9]+(?:_[0-9]+)? = [^;\n]*;)*)\s*\n\s*if\s*\(M2C_ERROR\(/\*\s*Read from unset register \$hi\s*\*/\)\)';edits=[]
 def replace(match):
  args=arguments(match.group(1));assert len(args)==2
  between=match.group('between');assert 'func_' not in between
  name='measured_greater_'+str(len(edits));edits.append(dict(before=match.group(),arguments=args,capture=name,predicate='binary32 greater;HI after original2537C',nativeFlagEvidence='377/379',compilerEvidence='378/379'))
  return name+' = ('+args[0]+') > ('+args[1]+');'+between+'\n    if ('+name+')'
 changed=re.sub(pattern,replace,raw);assert not edits or len(edits)==len(calls),('CompareCallCountMismatch',len(edits),len(calls))
 if edits:
  at=changed.index('{')+1;changed=changed[:at]+'\n'+''.join('    u32 '+r['capture']+';\n' for r in edits)+changed[at:]
 return changed,dict(changedComparisons=edits,measuredFlagSites=calls,scope='exact known2537C plus unchanged HI/BLS flow;capture occurs at original compare;intervening local loads retained;no generic flag rewriting')


def bitcasts(raw):
 variables={name:kind for kind,name in re.findall(r'\b(f32|s32|u32)\s+([A-Za-z_]\w*)\s*;',raw)};edits=[]
 def kind(expr):
  expr=expr.strip()
  if expr in variables:return variables[expr]
  if re.match(r'^[-+]?[0-9]+(?:\.[0-9]*)?(?:e[-+]?[0-9]+)?f$',expr,re.I):return 'f32'
  if re.match(r'^(?:0x[0-9a-f]+|[0-9]+)[uU]?$',expr,re.I):return 'u32'
  if expr.startswith('M2C_FIELD('):return arguments(expr[10:-1])[1].replace('*','').strip()
  m=re.match(r'^func_([0-9a-f]{8})\(',expr)
  if m:return SYMBOLS.get(int(m[1],16),('u32',''))[0]
  if expr.startswith('observed_word_to_f32('):return 'f32'
  if expr.startswith(('observed_f32_to_word(','(u32)','(s32)')):return 'u32'
  raise AssertionError(('UnsupportedBitcastSource',expr))
 def visit(text):
  token='M2C_BITWISE(';position=text.find(token)
  if position<0:return text
  start=position+len(token);depth=1;end=start
  while depth:
   if text[end]=='(':depth+=1
   elif text[end]==')':depth-=1
   end+=1
  args=arguments(text[start:end-1]);assert len(args)==2;target,expression=args;assert target in ('f32','s32','u32')
  expression=visit(expression);source=kind(expression);assert source in ('f32','s32','u32')
  if target=='f32':replacement=expression if source=='f32' else 'observed_word_to_f32((u32)('+expression+'))'
  elif source=='f32':replacement='('+target+')observed_f32_to_word('+expression+')'
  else:replacement='('+target+')('+expression+')'
  edits.append(dict(target=target,source=source,before=text[position:end],after=replacement));return visit(text[:position]+replacement+text[end:])
 return visit(raw),dict(changes=edits,scope='explicit32-bit M2C_BITWISE types only;union preserves representation;unknown widths/types reject')


def helpers(text):
 defs=[]
 if 'observed_word_to_f32(' in text:defs.append('static inline f32 observed_word_to_f32(u32 value) { union { u32 word; f32 scalar; } bits; bits.word=value; return bits.scalar; }')
 if 'observed_f32_to_word(' in text:defs.append('static inline u32 observed_f32_to_word(f32 value) { union { u32 word; f32 scalar; } bits; bits.scalar=value; return bits.word; }')
 if defs:
  at=text.index('extern ');text=text[:at]+'\n'.join(defs)+'\n\n'+text[at:]
 return text


def controls():
 raw='u32 sample(void) {\nfunc_0202537c(x, 0.0f);\nif (M2C_ERROR(/* Read from unset register $hi */)) { y=1; }\n}'
 assembly='bl func_0202537c\nldr r1, [r5, #0x14]\nldr r0, .L_value\nbls .L_else';changed,receipt=lower(raw,assembly);assert 'measured_greater_0 = (x) > (0.0f);' in changed and len(receipt['changedComparisons'])==1
 assert lower(raw.replace('0202537c','02025314'),assembly.replace('0202537c','02025314'))[0]==raw.replace('0202537c','02025314')
 assert lower(raw.replace('$hi','$lo'),assembly)[0]==raw.replace('$hi','$lo')
 rejected=False
 try:lower(raw,assembly.replace('ldr r0, .L_value','cmp r2, #0'))
 except AssertionError:rejected=True
 assert rejected
 assert 'observed_word_to_f32' in bitcasts('u32 x; f32 y; y=M2C_BITWISE(f32, x);')[0]
 assert 'observed_f32_to_word' in bitcasts('u32 x; f32 y; x=M2C_BITWISE(u32, y);')[0]
 assert 'M2C_BITWISE' not in bitcasts('f32 y; s32 x; y=M2C_BITWISE(f32, M2C_BITWISE(s32, func_02025ab8(1.0f,y)));')[0]
 rejected=False
 try:bitcasts('M2C_BITWISE(f64, 0)')
 except AssertionError:rejected=True
 assert rejected;return 8
