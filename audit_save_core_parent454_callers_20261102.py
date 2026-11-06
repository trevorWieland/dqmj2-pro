import hashlib
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
import capstone
from capstone.arm import ARM_INS_BL,ARM_INS_BLX,ARM_REG_R0
from link_runtime_unit import measured_module
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 meta,arm,cfg=measured_module('main');rows=[]
 for name,mode,n,a in re.findall(r'^(\S+) kind:function\((arm|thumb),size=0x([0-9a-f]+)\) addr:0x([0-9a-f]+)$',cfg,re.M):
  a=int(a,16);n=int(n,16);decoder=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_THUMB if mode=='thumb' else capstone.CS_MODE_ARM);decoder.detail=True;instructions=list(decoder.disasm(arm[a-0x02000000:a-0x02000000+n],a))
  for i,insn in enumerate(instructions):
   if insn.id not in (ARM_INS_BL,ARM_INS_BLX) or insn.op_str!='#0x209b450':continue
   prefix=[];kill=None
   for item in instructions[i+1:i+17]:
    reads,writes=item.regs_access();assert ARM_REG_R0 not in reads,('ConsumedR0',hex(insn.address),hex(item.address),item.mnemonic,item.op_str);prefix.append(dict(address=hex(item.address),size=item.size,mnemonic=item.mnemonic,operands=item.op_str))
    if ARM_REG_R0 in writes:kill=item.address;break
   assert kill is not None;end=instructions[i+len(prefix)].address+instructions[i+len(prefix)].size;rows.append(dict(caller=name,callerMode=mode,call=hex(insn.address),r0Killed=hex(kill),prefix=prefix,nativeSpanSha256=sha(arm[insn.address-0x02000000:end-0x02000000])))
 assert len(rows)==1;out=dict(schema=1,sourceCredit=0,functionReturns=0,moduleSha256=sha(arm),callerRows=rows,generatorSha256=sha(Path(__file__).read_bytes()),limitations=['Onlyobserved directBL/BLX sites incurrentcanonicalmainfunction inventory;indirect references ororiginalCAPIdeclaration notproven. Theobservedactualprefix overwriteR0 beforeanyconsumption,qualifying a discard-return caller view.']);p=ROOT/'evidence/abi/save-core-parent454-callers-20261102.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(directCallers=1,consumedR0=0,reportSha256=sha(p.read_bytes()))))
if __name__=='__main__':main()
