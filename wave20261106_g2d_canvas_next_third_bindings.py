import copy,re,hashlib
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding
LANE=ROOT/'evidence/lanes/parallel-wave20261106/g2d-canvas-next/third'

def inputs():
 value=read_json(LANE/'native-inputs.json')
 for k in['image','inventory','relocations']:
  if sha256(ROOT/value[k]['path'])!=value[k]['sha256']:raise ValueError('Original G2D namespace changed')
 return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text()

def validate(row,rel,binding,value,image,inventory,records):
 if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','arm'):raise ValueError('G2D caller namespace differs')
 item=next((x for x in value['entries']if x['address']==row['address']),None)
 if not item or(item['bytes'],item['targetSha256'])!=(row['bytes'],row['targetSha256']):raise ValueError('G2D full extent differs')
 address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']]
 if hashlib.sha256(native).hexdigest()!=row['targetSha256']or item['canonicalInventoryRecord']not in inventory.splitlines():raise ValueError('G2D original entry/body differs')
 origin=address+rel['offset'];found=[s for s in item['originalRelocationRecords']if s.startswith('from:0x%08x '%origin)]
 if len(found)!=1 or found[0]not in records.splitlines():raise ValueError('G2D original branch absent')
 match=re.fullmatch(r'from:0x[0-9a-f]+ kind:arm_call to:(0x[0-9a-f]+) module:main',found[0])
 if not match:raise ValueError('G2D original namespace absent')
 target=int(match[1],0)
 if(binding.get('program')or'',binding['processor'],binding['module'],binding['mode'],binding['kind'],int(binding['address'],0),int(rel['target'],0))!=('','arm9','main','arm','function',target,target)or rel['type']not in[1,28,29]or rel['addend']!=-8:raise ValueError('G2D typed original branch binding differs')
 ins=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(native[rel['offset']:rel['offset']+4],origin));assert len(ins)==1
 if ins[0].mnemonic!='bl'or ins[0].op_str!='#'+hex(target):raise ValueError('Actual G2D original call differs')
 sizes={0x2087e58:44}
 if target not in sizes or not any(re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(sizes[target],target),s)for s in inventory.splitlines()):raise ValueError('G2D whole original provider entry absent')
 verify_binding(rel['symbol'],binding);return dict(originalRecord=found[0],target=hex(target),program='',processor='arm9',module='main',mode='arm',selectedSamePacket=False,providerSourceOrExecutionCredit=0)

def verify_original(row,bindings):
 value,image,inventory,records=inputs();return dict(allPassed=True,relocations=[validate(row,r,bindings[r['symbol']],value,image,inventory,records)for r in row['relocations']],providerSourceOrExecutionCredit=0)

def negative_controls(rows):
 value,image,inventory,records=inputs();rejected=[]
 for row in rows:
  for rel in row['relocations']:
   binding=row['nativeSymbolEntries'][rel['symbol']]
   for label,owner,key,wrong in [('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('mode','binding','mode','thumb'),('interior','binding','address',hex(int(binding['address'],0)+4)),('origin','rel','offset',rel['offset']+4),('type','rel','type',2),('addend','rel','addend',0),('caller-mode','row','mode','thumb')]:
    obj={k:copy.deepcopy(v)for k,v in[('row',row),('rel',rel),('binding',binding)]};obj[owner][key]=wrong
    try:validate(obj['row'],obj['rel'],obj['binding'],value,image,inventory,records)
    except(ValueError,KeyError)as error:rejected.append(dict(caller=row['address'],case=label,rejected=True,reason=str(error)))
    else:raise ValueError('Wrong G2D binding accepted')
 return dict(allPassed=True,cases=rejected,sourceOrExecutionCredit=0)
