import re

def apply(assembly,native,entry):
 import capstone
 decoder=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_THUMB);decoder.detail=True;cursor=entry;lines=assembly.splitlines(keepends=True);edits=[];unchanged=[]
 for number,line in enumerate(lines):
  text=line.strip()
  if not text or text.startswith(('.text','.global','.type','.size')) or text.endswith(':') and not text.startswith('.L_'):continue
  if text.startswith('.L_'):
   label,tail=text.split(':',1);assert cursor==int(label[3:],16),('AssemblyCursor',hex(cursor),text);text=tail.strip()
   if not text:continue
  if text.startswith(('.balign','.align')):
   value=int(text.split()[1],0);value=1<<value if text.startswith('.align') else value;cursor=(cursor+value-1)&-value;continue
  if text.startswith(('.short','.hword','.word','.long','.byte')):cursor+=1 if text.startswith('.byte') else 2 if text.startswith(('.short','.hword')) else 4;continue
  assert not text.startswith('.'),('UnknownAssemblyDirective',text);decoded=list(decoder.disasm(native[cursor-entry:cursor-entry+4],cursor,count=1));assert len(decoded)==1;insn=decoded[0];mnemonic=text.split()[0]
  if insn.update_flags and mnemonic in {'mov','add','sub','lsl','lsr','asr','and','orr','eor','bic','mvn','adc','sbc','mul','ror','neg','rsb'}:
   replacement=mnemonic+'s';lines[number]=line.replace(mnemonic+' ',replacement+' ',1);edits.append(dict(address=cursor,size=insn.size,line=number,before=mnemonic,after=replacement,nativeMnemonic=insn.mnemonic,nativeOperands=insn.op_str,bytes=native[cursor-entry:cursor-entry+insn.size].hex()))
  elif mnemonic in {'mov','add','sub','lsl','lsr','asr','and','orr','eor','bic','mvn','adc','sbc','mul','ror','neg','rsb'}:unchanged.append(dict(address=cursor,mnemonic=mnemonic,nativeFlags=False))
  cursor+=insn.size
 assert cursor==entry+len(native),('AssemblyExtent',hex(cursor),hex(entry+len(native)))
 return ''.join(lines),dict(entry=entry,bytes=len(native),flagSettingEdits=edits,nonFlagSettersKept=unchanged,scope='Analysis-only implicitThumb flag restoration fromactual native opcode;noexecutablebytes changed. C semantic/compile/link evidence remains separate.')
