import hashlib
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
import capstone
from capstone.arm import ARM_INS_BL
from link_runtime_unit import measured_module
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 md,arm,cfg=measured_module('main');snapshot='evidence/verification/accepted-cohort140-identities-v2-20261101.json';claims=[r for r in json.loads((ROOT/snapshot).read_text())['functions'] if r.get('processor')=='arm9' and r.get('program','')=='' and r['module']=='main'];old={int(x['address'],0) for family in (403,415) for x in json.loads((ROOT/('evidence/lanes/save-core/breadth'+str(family)+'-queue-20261102.json')).read_text())['jobs']};old.update((0x020491F8,0x02049794,0x020444EC,0x02043844,0x0206A584));decoder=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_ARM);rows=[]
 for name,mode,size,address in re.findall(r'^(\S+) kind:function\((arm|thumb),size=0x([0-9a-f]+)\) addr:0x([0-9a-f]+)$',cfg,re.M):
  a=int(address,16);n=int(size,16)
  if mode!='arm' or not 0x02040000<=a<0x020D0000 or n<512 or n>5000 or a in old or any(a<x['address']+int(x.get('bytes') or 1) and x['address']<a+n for x in claims):continue
  native=arm[a-0x02000000:a-0x02000000+n];calls=[int(i.op_str[1:],0) for i in decoder.disasm(native,a) if i.id==ARM_INS_BL and i.op_str.startswith('#')]
  if any(0x02024000<=x<0x02026000 for x in calls):continue
  rows.append(dict(module='main',mode=mode,address=hex(a),bytes=n,alias=name,nativeSpanSha256=sha(native),nativeModuleSha256=sha(arm),work='work/save-core/breadth417/'+format(a,'08x'),draftDiscoveryStatus='Fresh context hypothesis;previous draft uniqueness not claimed'))
 rows.sort(key=lambda x:(-x['bytes'],int(x['address'],0)));assert len(rows)==26;out=dict(schema=1,sourceCredit=0,freshExclusionSnapshot=dict(path=snapshot,sha256=sha((ROOT/snapshot).read_bytes())),jobs=rows,limits=['Remaining26 owned canonical ARM functions at512..5000bytes after accepted140,403,415 andownership exclusions. Static direct knownsoftfloat callers excluded.','All newfiles are context refinements;new native discovery/source acceptance notclaimed. Unknown boundaries,ABI,fields,stack aggregates andhelper paths remain unqualified. Two isolated compiler workers with default/speed profiles;previous frozen candidates untouched.']);p=ROOT/'evidence/lanes/save-core/breadth417-queue-20261102.json';p.write_text(json.dumps(out,indent=2)+'\n');print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows)))
if __name__=='__main__':main()
