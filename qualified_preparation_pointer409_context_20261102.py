import re


def apply(context,assembly):
 edits=[]
 for offset in ('1ec','2c0','2c4'):
  pattern=r'\bu32 field_'+offset+r';'
  context,count=re.subn(pattern,'u8 *field_'+offset+';',context)
  if count:edits.append(dict(field='0x'+offset,before='u32',after='u8 *',qualification='actual constructor/preview record/slot/descriptor address role;ARM32 width unchanged;extent/lifetime not inferred'))
 if '.word data_021c64d0' in assembly:
  assert 'lsl #0x2]' in assembly
  declaration='extern u8 *data_021c64d0[];';context=re.sub(r'^extern[^;\n]*\bdata_021c64d0[^;\n]*;\n','',context,flags=re.M);context+=declaration+'\n';edits.append(dict(globalAddress='0x021c64d0',after=declaration,qualification='original native word-pointer table indexedLSL2 andconstructor stores;unsizedcaller view only'))
 return context,edits
