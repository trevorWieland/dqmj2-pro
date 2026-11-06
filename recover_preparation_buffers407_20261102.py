import re


def apply(text,assembly,spans):
 declarations={name:(kind,int(name[2:],16)) for kind,name in re.findall(r'^    (u8|s8|u16|s16|u32|s32) (sp[0-9A-Fa-f]+);$',text,re.M)};changes=[]
 frame=[int(value,16) for value in re.findall(r'^\s*sub sp, sp, #0x([0-9a-f]+)$',assembly,re.M)];assert frame
 for base,length,role in spans:
  assert base+length<=sum(frame),(hex(base),length,frame)
  if role=='feature':assert re.search(r'add r3, sp, #0x'+format(base,'x')+r'\b',assembly)
  if role=='text':assert re.search(r'add r1, sp, #0x'+format(base,'x')+r'\b',assembly)
  slots=[(name,kind,offset) for name,(kind,offset) in declarations.items() if base<=offset<base+length];assert slots
  for name,kind,offset in slots:
   text=re.sub(r'^    '+kind+' '+name+r';\n','',text,flags=re.M)
  storage='stack_'+format(base,'x');first=text.index('{',text.index('u32 native_main_'))+1;text=text[:first]+'\n    NativeStack64 '+storage+';'+text[first:]
  for name,kind,offset in sorted(slots,key=lambda x:-len(x[0])):
   replacement='M2C_FIELD('+storage+'.bytes, '+kind+' *, '+hex(offset-base)+')';text=re.sub(r'\b'+name+r'\b',replacement,text)
  changes.append(dict(base=hex(base),bytes=length,role=role,storage=storage,recoveredAliases=[dict(name=name,kind=kind,offset=offset-base) for name,kind,offset in slots],qualification='actual output/clear64-byte contract andnative SP frame;word alignment fromactual typed accesses;no padding/extra machine inputs'))
 if changes:
  at=text.index('extern ');text=text[:at]+'typedef union { u32 alignment; u8 bytes[64]; } NativeStack64;\n'+text[at:]
 return text,dict(changes=changes,scope='ordinary contiguous byte-storage with typed alias views;compiler placement/profile unconstrained')
