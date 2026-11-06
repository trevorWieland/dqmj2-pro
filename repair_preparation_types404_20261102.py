import re
from lower_measured_binary32_flags388_20261102 import arguments


def whole_call(text,name):
 prefix=name+'(';at=text.find(prefix)
 while at>=0:
  begin=at+len(prefix);end=begin;depth=1
  while depth:
   if text[end]=='(':depth+=1
   elif text[end]==')':depth-=1
   end+=1
  yield at,end,arguments(text[begin:end-1]);at=text.find(prefix,end)


def apply(text,assembly,address):
 edits=[];at=text.index('u32 native_main_');head,body=text[:at],text[at:]
 if 'SavedSkill' in head and not re.search(r'\}\s*SavedSkill\s*;',head):
  position=head.index('extern ');definition='typedef struct { u8 skill; u8 allocated; } SavedSkill;\n';head=head[:position]+definition+head[position:];edits.append(dict(kind='emitted-type',bytes=2,qualification='existing frozen features.c two-u8 SavedSkill API;no broader extent'))
 for name,casts in (('native_fn_0207b460',{2:'SavedSkill *',3:'u8 *'}),('native_fn_0207c078',{2:'const u8 *',3:'u8 *'})):
  for start,end,args in reversed(list(whole_call(body,name))):
   assert len(args)==4,('UnqualifiedArity',name,len(args));before=body[start:end]
   for i,kind in casts.items():args[i]='('+kind+')('+args[i]+')'
   after=name+'('+', '.join(args)+')';body=body[:start]+after+body[end:];edits.append(dict(kind='explicit-pointer-word-view',callee=name,before=before,after=after,qualification='selected measured4-word source API;byte/pair pointee view;bounds/path semantics unchanged'))
 if address in (0x02076DEC,0x0207726C):
  assert '.word data_021c64d0' in assembly and 'lsl #0x2]' in assembly
  allowed={'sp14':'u8','sp18':'u8'} if address==0x02076DEC else {'temp_r10':'u8'};start=body.find('*(')
  while start>=0:
   end=start+2;depth=1
   while depth:
    if body[end]=='(':depth+=1
    elif body[end]==')':depth-=1
    end+=1
   expression=body[start+2:end-1];replacement=None
   if expression.startswith('native_data_021c64d0 + '):replacement='M2C_FIELD(native_data_021c64d0, u32 *, '+expression.split(' + ',1)[1]+')'
   else:
    for symbol,kind in allowed.items():
     if expression.startswith(symbol+' + '):replacement='M2C_FIELD((u8 *)'+symbol+', '+kind+' *, '+expression.split(' + ',1)[1]+')'
   if replacement:
    before=body[start:end];body=body[:start]+replacement+body[end:];edits.append(dict(kind='measured-pointer-memory-width',before=before,after=replacement,qualification='descriptor table native LDR/LSL2;rank/record native LDRB;no array extent orlife cycle inferred'));start=body.find('*(',start+len(replacement))
   else:start=body.find('*(',end)
 return head+body,dict(changes=edits,scope='explicit existing selected-source pair/byte pointer views;no arity trimming,unused-argument deletion,saved-register initialization ornew machine inputs')
