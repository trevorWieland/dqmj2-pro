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
 pattern=r'func_0202537c\(([^\n]*)\);\s*\n\s*if\s*\(M2C_ERROR\(/\*\s*Read from unset register \$hi\s*\*/\)\)';edits=[]
 def replace(match):
  args=arguments(match.group(1));assert len(args)==2;edits.append(dict(before=match.group(),arguments=args,predicate='binary32 greater;HI after original2537C',nativeFlagEvidence='377/379',compilerEvidence='378/379'));return 'if (('+args[0]+') > ('+args[1]+'))'
 changed=re.sub(pattern,replace,raw);assert not edits or len(edits)==len(calls),('CompareCallCountMismatch',len(edits),len(calls));return changed,dict(changedComparisons=edits,measuredFlagSites=calls,scope='only exact known2537C call +unmodified HI/BLS flag flow;no generic carry/flag rewriting')


def controls():
 raw='func_0202537c(x, 0.0f);\nif (M2C_ERROR(/* Read from unset register $hi */)) { y=1; }';assembly='bl func_0202537c\nldr r1, [r5, #0x14]\nldr r0, .L_value\nbls .L_else'
 changed,receipt=lower(raw,assembly);assert changed=='if ((x) > (0.0f)) { y=1; }' and len(receipt['changedComparisons'])==1
 assert lower(raw.replace('0202537c','02025314'),assembly.replace('0202537c','02025314'))[0]==raw.replace('0202537c','02025314')
 assert lower(raw.replace('$hi','$lo'),assembly)[0]==raw.replace('$hi','$lo')
 rejected=False
 try:lower(raw,assembly.replace('ldr r0, .L_value','cmp r2, #0'))
 except AssertionError:rejected=True
 assert rejected;return 4
