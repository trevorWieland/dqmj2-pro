import copy,re,hashlib
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding
from wave20261106_ov006_crypto_utility_next_helpers import qualify
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next/first'

def inputs():
 value=read_json(LANE/'native-inputs.json')
 for k in ['image','inventory','relocations']:
  if sha256(ROOT/value[k]['path'])!=value[k]['sha256']:raise ValueError('Original crypto namespace changed')
 return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text()

def validate(row,rel,binding,value,image,inventory,records):
 if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','ov006','thumb'):raise ValueError('Crypto caller namespace differs')
 item=next((x for x in value['entries']if x['address']==row['address']),None)
 if not item or(item['bytes'],item['targetSha256'])!=(row['bytes'],row['targetSha256']):raise ValueError('Complete crypto extent differs')
 address=int(row['address'],0);native=image[address-0x21d7240:address-0x21d7240+row['bytes']]
 if hashlib.sha256(native).hexdigest()!=row['targetSha256']or item['canonicalInventoryRecord']not in inventory.splitlines():raise ValueError('Original caller entry/body differs')
 origin=address+rel['offset'];found=[s for s in item['originalRelocationRecords']if s.startswith('from:0x%08x '%origin)]
 if len(found)!=1 or found[0]not in records.splitlines():raise ValueError('Original crypto branch absent')
 match=re.fullmatch(r'from:0x[0-9a-f]+ kind:(thumb_call|thumb_call_arm) to:(0x[0-9a-f]+) module:(overlay\(6\)|main)',found[0])
 if not match:raise ValueError('Crypto original namespace absent')
 kind,target=match[1],int(match[2],0);module='main'if match[3]=='main'else'ov006';mode='arm'if kind=='thumb_call_arm'else'thumb'
 if(binding.get('program')or'',binding['processor'],binding['module'],binding['mode'],binding['kind'],int(binding['address'],0),int(rel['target'],0),rel['type'],rel['addend'])!=('','arm9',module,mode,'function',target,target,10,-4):raise ValueError('Original crypto typed branch binding differs')
 ins=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(native[rel['offset']:rel['offset']+4],origin));assert len(ins)==1
 if ins[0].mnemonic!=('blx'if mode=='arm'else'bl')or ins[0].op_str!='#'+hex(target):raise ValueError('Actual crypto native branch differs')
 if module=='main':
  if rel['symbol']!='_u32_div_f':raise ValueError('Unqualified compiler helper name')
  qualify(rel['symbol'],binding)
 else:
  sizes={0x21ed8fc:62,0x21ed99c:56}
  if target not in sizes or not any(re.fullmatch(r'\S+ kind:function\(thumb,size=0x%x\) addr:0x%08x'%(sizes[target],target),s)for s in inventory.splitlines()):raise ValueError('Original complete crypto callee absent')
 verify_binding(rel['symbol'],binding);return dict(originalRecord=found[0],originalNativeMnemonic=ins[0].mnemonic,target=hex(target),program='',processor='arm9',module=module,mode=mode,calleeSourceOrExecutionCredit=0)

def verify_original(row,bindings):
 value,image,inventory,records=inputs();return dict(allPassed=True,relocations=[validate(row,r,bindings[r['symbol']],value,image,inventory,records)for r in row['relocations']],providerSourceOrExecutionCredit=0)

def negative_controls(rows):
 value,image,inventory,records=inputs();rejected=[]
 for row in rows:
  for rel in row['relocations']:
   binding=row['nativeSymbolEntries'][rel['symbol']]
   for label,owner,key,wrong in [('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov001'),('mode','binding','mode','thumb'if binding['mode']=='arm'else'arm'),('interior','binding','address',hex(int(binding['address'],0)+4)),('origin','rel','offset',rel['offset']+2),('type','rel','type',2),('addend','rel','addend',0),('caller-mode','row','mode','arm')]:
    obj={k:copy.deepcopy(v)for k,v in[('row',row),('rel',rel),('binding',binding)]};obj[owner][key]=wrong
    try:validate(obj['row'],obj['rel'],obj['binding'],value,image,inventory,records)
    except(ValueError,KeyError)as error:rejected.append(dict(caller=row['address'],case=label,rejected=True,reason=str(error)))
    else:raise ValueError('Wrong crypto binding accepted')
 return dict(allPassed=True,cases=rejected,sourceOrExecutionCredit=0)
