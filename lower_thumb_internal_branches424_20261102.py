import re

def certify(assembly,native,entry):
 import capstone
 from capstone.arm import ARM_INS_B,ARM_INS_BL,ARM_INS_BLX,ARM_INS_BX,ARM_INS_POP,ARM_INS_PUSH,ARM_REG_LR,ARM_REG_PC
 assert '.arm' not in assembly and '.code 32' not in assembly
 decoder=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_THUMB);decoder.detail=True;cursor=entry;instructions=[];sites=[];labels={int(x,16) for x in re.findall(r'^\.L_([0-9a-fA-F]+):',assembly,re.M)};lines=assembly.splitlines();tables=re.findall(r'^\s*\.short\s+(.+)$',assembly,re.M)
 for table in tables:
  targets=re.findall(r'\.L_([0-9a-fA-F]+)',table);assert len(targets)==2 and all(entry<=int(x,16)<entry+len(native) for x in targets),('UnclosedLocalTable',table)
 for number,line in enumerate(lines):
  text=line.strip()
  if not text or text.startswith(('.text','.global','.type','.size')) or text.endswith(':') and not text.startswith('.L_'):continue
  if text.startswith('.L_'):
   label,tail=text.split(':',1);assert cursor==int(label[3:],16),('AssemblyCursor',hex(cursor),text);text=tail.strip()
   if not text:continue
  if text.startswith(('.balign','.align')):
   value=int(text.split()[1],0);value=(1<<value) if text.startswith('.align') else value;cursor=(cursor+value-1)&-value;continue
  if text.startswith(('.short','.hword','.word','.long','.byte')):cursor+=1 if text.startswith('.byte') else 2 if text.startswith(('.short','.hword')) else 4;continue
  assert not text.startswith('.'),('UnknownAssemblyDirective',text);decoded=list(decoder.disasm(native[cursor-entry:cursor-entry+4],cursor,count=1));assert len(decoded)==1,('NoNativeInstruction',hex(cursor));insn=decoded[0];reads,writes=insn.regs_access()
  if ARM_REG_LR in reads:assert cursor==entry and insn.id==ARM_INS_PUSH,('LiveLinkRegister',hex(cursor),insn.mnemonic,insn.op_str)
  assert insn.id!=ARM_INS_BX,('IndirectTailOrReturn',hex(cursor))
  if insn.id==ARM_INS_BLX:assert insn.op_str.startswith('#'),('IndirectCall',hex(cursor))
  if insn.id==ARM_INS_B:
   assert insn.op_str.startswith('#') and entry<=int(insn.op_str[1:],0)<entry+len(native),('ExternalBranch',hex(cursor),insn.op_str)
  if ARM_REG_PC in writes and insn.id not in (ARM_INS_B,ARM_INS_BL,ARM_INS_BLX,ARM_INS_POP):
   assert insn.mnemonic=='add' and insn.op_str.startswith('pc, ') and tables,('UnknownPcWrite',hex(cursor),insn.mnemonic,insn.op_str)
   preceding='\n'.join(x.strip() for x in lines[max(0,number-5):number]);assert re.search(r'ldrh ',preceding) and re.search(r'lsl ',preceding) and re.search(r'asr ',preceding),('UnprovedLocalSwitch',hex(cursor))
  if re.fullmatch(r'bl \.L_[0-9a-fA-F]+',text):
   target=int(text.rsplit('_',1)[1],16);assert insn.id==ARM_INS_BL and insn.size==4 and int(insn.op_str[1:],0)==target and entry<target<entry+len(native) and target in labels,('LocalBlIdentity',hex(cursor),text);sites.append(dict(address=cursor,target=target,size=4,line=number))
  instructions.append(dict(address=cursor,size=insn.size,mnemonic=insn.mnemonic,operands=insn.op_str));cursor+=insn.size
 assert cursor==entry+len(native),('AssemblyExtent',hex(cursor),hex(entry+len(native)));assert instructions and instructions[0]['mnemonic']=='push' and 'lr' in instructions[0]['operands'];assert sites,'NoLocalBlSites'
 return dict(entry=entry,bytes=len(native),localBranches=sites,instructionCount=len(instructions),lrReadSites=[entry],localTableEntries=len(tables),scope='Analysis-only local long branches;LRread restricted toentryPUSH;all external tailbranches/indirectcalls/BX rejected;localPC table shapes bounded towithinfunction')

def apply(assembly,native,entry):
 proof=certify(assembly,native,entry);lines=assembly.splitlines(keepends=True)
 for site in proof['localBranches']:
  line=lines[site['line']];assert re.search(r'\bbl \.L_',line);lines[site['line']]=line.replace('bl .L_','b .L_',1)
 return ''.join(lines),proof
