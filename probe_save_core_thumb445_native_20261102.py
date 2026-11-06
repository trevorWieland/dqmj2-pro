import gzip
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
import capstone
import unicorn
from unicorn import arm_const as R
from link_runtime_unit import measured_module
import lower_thumb_internal_branches424_20261102 as L
import restore_thumb_flags426_20261102 as F
REGS=[getattr(R,'UC_ARM_REG_R'+str(i)) for i in range(13)]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 identity=json.loads((ROOT/'evidence/lanes/save-core/thumb443-identities-20261102.json').read_text());history=identity['history'];packed=(ROOT/history['path']).read_bytes();assert sha(packed)==history['sha256'];archive=json.loads(gzip.decompress(packed))['archive'];arm=measured_module('main')[1];queue=json.loads((ROOT/'evidence/lanes/save-core/breadth423-queue-20261102.json').read_text());proofs=[];samples={};local=[];decoder=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_THUMB);decoder.detail=True;rejected=[]
 for job in queue['jobs']:
  p=ROOT/job['work']/'input.s';a=int(job['address'],0);native=arm[a-0x02000000:a-0x02000000+job['bytes']];assembly=archive[(Path(job['work'])/'input.s').as_posix()];text,proof=F.apply(assembly,native,a);proofs.append(proof)
  for item in proof['flagSettingEdits']+proof['nonFlagSettersKept']:
   insn=list(decoder.disasm(arm[item['address']-0x02000000:item['address']-0x02000000+4],item['address'],count=1))[0];key=(insn.mnemonic,'after' in item)
   if key not in samples:samples[key]=dict(address=insn.address,bytes=insn.bytes.hex(),mnemonic=insn.mnemonic,operands=insn.op_str,flagSetter='after' in item,destination=insn.reg_name(insn.operands[0].reg))
  try:changed,branch=L.apply(assembly,native,a);local.extend(branch['localBranches'])
  except AssertionError as error:rejected.append(dict(address=hex(a),reason=str(error)))
 u=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);u.mem_map(0x02000000,0x200000);u.mem_write(0x02000000,arm);u.mem_map(0x02700000,0x20000);rows=[];dropped=forced=0
 for sample in samples.values():
  for nibble in range(16):
   for profile in range(4):
    for i,reg in enumerate(REGS):u.reg_write(reg,(0,1,0x80000000,0xFFFFFFFF)[(i+profile)%4])
    u.reg_write(R.UC_ARM_REG_SP,0x02710000);u.reg_write(R.UC_ARM_REG_LR,0x02711001);u.reg_write(R.UC_ARM_REG_CPSR,nibble<<28|0x30);u.emu_start(sample['address']|1,0,count=1);after=u.reg_read(R.UC_ARM_REG_CPSR)>>28;dest=sample['destination'];reg=getattr(R,'UC_ARM_REG_'+dest.upper()) if dest not in ('ip','sb','sl','fp') else REGS[{'ip':12,'sb':9,'sl':10,'fp':11}[dest]];value=u.reg_read(reg);nz=(value>>31<<1)|int(value==0)
    if sample['flagSetter']:assert after>>2==nz;dropped+=int(after!=nibble)
    else:assert after==nibble;forced+=int((nibble>>2)!=nz)
    rows.append(dict(sample=sample,nzcvBefore=nibble,profile=profile,nzcvAfter=after,destinationWord=value))
 branch_rows=[]
 for site in local:
  for nibble in range(16):
   u.reg_write(R.UC_ARM_REG_CPSR,nibble<<28|0x30);u.reg_write(R.UC_ARM_REG_LR,0xAAAAAAAA);u.emu_start(site['address']|1,0,count=1);pc=u.reg_read(R.UC_ARM_REG_PC);lr=u.reg_read(R.UC_ARM_REG_LR);after=u.reg_read(R.UC_ARM_REG_CPSR)>>28;assert pc==site['target'] and lr==(site['address']+4|1) and after==nibble;branch_rows.append(dict(address=hex(site['address']),target=hex(pc),lr=hex(lr),nzcv=nibble))
 raw=(json.dumps(dict(flagSteps=rows,localBlSteps=branch_rows),sort_keys=True,separators=(',',':'))+'\n').encode();p=ROOT/'evidence/vectors/save-core-thumb445-native-20261102.json.gz';p.write_bytes(gzip.compress(raw,mtime=0));out=dict(schema=1,sourceCredit=0,properFunctionReturns=0,nativeArithmeticSingleSteps=len(rows),nativeLocalBlSingleSteps=len(branch_rows),uniqueArithmeticClasses=len(samples),flagAnnotations=sum(len(x['flagSettingEdits']) for x in proofs),nonflagInstructionsPreserved=sum(len(x['nonFlagSettersKept']) for x in proofs),droppedFlagWrongObservations=dropped,forcedFlagWrongObservations=forced,closedLocalBranchSites=len(local),rejectedFunctionQualifications=rejected,sidecar=dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p.read_bytes()),caseSha256=sha(raw)),tools=[dict(path=p,sha256=sha((ROOT/p).read_bytes())) for p in ('restore_thumb_flags426_20261102.py','lower_thumb_internal_branches424_20261102.py')],generatorSha256=sha(Path(__file__).read_bytes()),limits=['Single-step native instruction evidence only;zero functionreturns,parent semantics ormatching source credit. NZmatches actual destinationword;nonflag opcode preservesNZCV. FullC/Vcarry model,M2C backend semantics andlarger callers remain separate.','OnlycertifiedlocalBLsites haveLRdead withinclosedfunction CFG:entryPUSHonly LRread,noBX/indirectcalls/externaltailbranches,localPCtable shapes. Original BLchanges LR butpreservesNZCV;no executable opcodes areedited.','Analysisflags restoredfromactual Thumbopcode update_flags instead ofassuming ARMtextdefaults. Allpreviousfrozen assembler/source/report paths stayunchanged.']);p=ROOT/'evidence/verification/save-core-thumb445-native-20261102.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('nativeArithmeticSingleSteps','nativeLocalBlSingleSteps','flagAnnotations','nonflagInstructionsPreserved','droppedFlagWrongObservations','forcedFlagWrongObservations','closedLocalBranchSites')}))
if __name__=='__main__':main()
