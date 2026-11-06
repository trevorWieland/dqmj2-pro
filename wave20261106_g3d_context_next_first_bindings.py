import copy,re,hashlib,struct
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding
LANE=ROOT/'evidence/lanes/parallel-wave20261106/g3d-context-next/first'
SIZES={0x2031ef0:140,0x202e434:228,0x202e74c:68,0x202e300:92,0x2004668:48}
DATA={0x20dd690,0x20dd6c0,0x20edf90}

def inputs():
 value=read_json(LANE/'native-inputs.json')
 for k in['image','inventory','relocations']:
  if sha256(ROOT/value[k]['path'])!=value[k]['sha256']:raise ValueError('Original G3D namespace changed')
 return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text()

def validate(row,rel,binding,value,image,inventory,records):
 if(row.get('program')or'',row['processor'],row['module'],row['mode'],row['address'],row['bytes'])!=('','arm9','main','arm','0x2031b44',940):raise ValueError('G3D full caller identity differs')
 item=value['entries'][0];native=image[0x31b44:0x31ef0]
 if hashlib.sha256(native).hexdigest()!=row['targetSha256']or item['targetSha256']!=row['targetSha256']or item['canonicalInventoryRecord']not in inventory.splitlines():raise ValueError('G3D original full entry/body differs')
 origin=0x2031b44+rel['offset'];found=[s for s in item['originalRelocationRecords']if s.startswith('from:0x%08x '%origin)]
 if len(found)!=1 or found[0]not in records.splitlines():raise ValueError('G3D original relocation absent')
 match=re.fullmatch(r'from:0x[0-9a-f]+ kind:(arm_call|load) to:(0x[0-9a-f]+) module:main',found[0])
 if not match:raise ValueError('G3D original namespace ambiguous')
 kind,target=match[1],int(match[2],0);base=int(binding['address'],0)
 if(binding.get('program')or'',binding['processor'],binding['module'],int(rel['target'],0))!=('','arm9','main',base):raise ValueError('G3D binding namespace/base differs')
 if kind=='arm_call':
  if(binding['mode'],binding['kind'],base,rel['addend'])!=('arm','function',target,-8)or rel['type']not in[1,28,29]or target not in SIZES:raise ValueError('G3D real function mode/addend differs')
  if not any(re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(SIZES[target],target),s)for s in inventory.splitlines()):raise ValueError('G3D provider whole entry absent')
  ins=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(native[rel['offset']:rel['offset']+4],origin))
  if len(ins)!=1 or ins[0].mnemonic!='bl'or ins[0].op_str!='#'+hex(target):raise ValueError('G3D real original branch differs')
 else:
  if(binding['mode'],binding['kind'],rel['type'])!=('data','data',2)or base not in DATA or base+rel['addend']!=target or struct.unpack_from('<I',native,rel['offset'])[0]!=target:raise ValueError('G3D original data/addend differs')
 verify_binding(rel['symbol'],binding);return dict(originalRecord=found[0],qualifiedNativeBase=hex(base),program='',processor='arm9',module='main',mode=binding['mode'],sourceOrExecutionOrStorageCredit=0)

def verify_original(row,bindings):
 value,image,inventory,records=inputs();return dict(allPassed=True,relocations=[validate(row,r,bindings[r['symbol']],value,image,inventory,records)for r in row['relocations']],suppliedProviderOrDataCredit=0)

def negative_controls(rows):
 value,image,inventory,records=inputs();rejected=[]
 for row in rows:
  for rel in row['relocations']:
   binding=row['nativeSymbolEntries'][rel['symbol']]
   for label,owner,key,wrong in [('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('mode','binding','mode','thumb'),('interior','binding','address',hex(int(binding['address'],0)+4)),('origin','rel','offset',rel['offset']+4),('type','rel','type',10),('addend','rel','addend',rel['addend']+4),('caller-mode','row','mode','thumb')]:
    obj={k:copy.deepcopy(v)for k,v in[('row',row),('rel',rel),('binding',binding)]};obj[owner][key]=wrong
    try:validate(obj['row'],obj['rel'],obj['binding'],value,image,inventory,records)
    except(ValueError,KeyError)as error:rejected.append(dict(caller=row['address'],symbol=rel['symbol'],case=label,rejected=True,reason=str(error)))
    else:raise ValueError('Wrong G3D binding accepted')
 return dict(allPassed=True,cases=rejected,sourceOrExecutionOrStorageCredit=0)
