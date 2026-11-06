import copy,re,hashlib,struct
import match_runtime
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-aes-next'
NATIVE=LANE/'native-inputs.json'
IMPORTS=LANE/'original-imports.json'

def inputs():
 if sha256(NATIVE)!='c315b1852adfc3e0b3152529a55abd232759a4251decb1a8dfe3b5475106fe63'or sha256(IMPORTS)!='824d84ee85ae9d91245d77f7fdc17159ca66deaa64db0282740deb7e75233628':raise ValueError('Frozen AES native/import contract changed')
 value=read_json(NATIVE)
 for key in ['image','inventory','relocations']:
  pin=value[key]
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Original AES namespace changed')
 return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text(),read_json(IMPORTS)

def validate(row,rel,binding,value,image,inventory,records,imports):
 if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','ov006','thumb'):raise ValueError('AES caller namespace differs')
 item=next((x for x in value['entries']if x['address']==row['address']),None)
 if not item or(item['bytes'],item['targetSha256'])!=(row['bytes'],row['targetSha256']):raise ValueError('Whole AES extent differs')
 address=int(row['address'],0);native=image[address-0x21d7240:address-0x21d7240+row['bytes']]
 if hashlib.sha256(native).hexdigest()!=row['targetSha256']or item['canonicalInventoryRecord']not in inventory.splitlines():raise ValueError('Original AES body/entry differs')
 origin=address+rel['offset'];found=[s for s in item['originalRelocationRecords']if s.startswith('from:0x%08x '%origin)]
 if len(found)!=1 or found[0]not in records.splitlines():raise ValueError('Unique original AES relocation absent')
 record=found[0];match=re.fullmatch(r'from:0x[0-9a-f]+ kind:(load|thumb_call) to:(0x[0-9a-f]+) module:overlay\(6\)',record)
 if not match:raise ValueError('Original explicit overlay6 target absent')
 kind,target=match[1],int(match[2],0)
 if(binding.get('program')or'',binding['processor'],binding['module'],int(binding['address'],0))!=('','arm9','ov006',target)or int(rel['target'],0)!=target:raise ValueError('Original AES target namespace/entry differs')
 word=image[origin-0x21d7240:origin-0x21d7240+4]
 if kind=='load':
  view=imports['dataViews'].get(hex(target))
  if not view or(binding['kind'],binding['mode'])!=('data','data')or rel['type']!=2 or rel['addend']!=0 or struct.unpack('<I',word)[0]!=target:raise ValueError('Original AES data ABS32 differs')
  if view['elements']not in[10,256]or view['elementBytes']!=4 or view['extentBytes']!=view['elements']*4:raise ValueError('Complete AES data view differs')
  raw=image[target-0x21d7240:target-0x21d7240+view['extentBytes']]
  if hashlib.sha256(raw).hexdigest()!=view['sha256']:raise ValueError('Native full AES table/rcon bytes differ')
  canonical=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:data(?:\(any\))? addr:0x%08x'%target,s)),None)
  if canonical is None:raise ValueError('Existing original table symbol absent')
  witness=dict(originalRecord=record,origin=hex(origin),target=hex(target),canonicalInventoryRecord=canonical,dataView=view,fullNativeDataSpanHashChecked=True,storageSourceCredit=0)
 else:
  if(target,binding['kind'],binding['mode'],rel['type'],rel['addend'])!=(0x21f0944,'function','thumb',10,-4)or address!=0x21f0bfc:raise ValueError('AES code provider differs')
  decoded=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(word,origin));assert len(decoded)==1
  if decoded[0].mnemonic!='bl'or decoded[0].op_str!='#'+hex(target):raise ValueError('Original AES branch differs')
  canonical=next(s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(thumb,size=0x2b8\) addr:0x021f0944',s))
  witness=dict(originalRecord=record,origin=hex(origin),target=hex(target),canonicalInventoryRecord=canonical,selectedSamePacketCodeProvider=True,extraProviderCredit=0)
 verify_binding(rel['symbol'],binding);return witness

def verify_original(row,bindings):
 value,image,inventory,records,imports=inputs();return dict(witnesses=[validate(row,r,bindings[r['symbol']],value,image,inventory,records,imports)for r in row['relocations']],allExplicitOv006OriginalReferences=True,importedStorageSourceCredit=0)

def negative_controls(rows):
 value,image,inventory,records,imports=inputs();rejected=[]
 for row in rows:
  for rel in row['relocations']:
   binding=row['nativeSymbolEntries'][rel['symbol']]
   for label,owner,key,wrong in [('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('main','binding','module','main'),('mode','binding','mode','arm'),('interior','binding','address',hex(int(binding['address'],0)+4)),('origin','rel','offset',rel['offset']+2),('addend','rel','addend',rel['addend']+4),('type','rel','type',1),('caller-mode','row','mode','arm')]:
    obj={k:copy.deepcopy(v)for k,v in [('row',row),('rel',rel),('binding',binding)]};obj[owner][key]=wrong
    try:validate(obj['row'],obj['rel'],obj['binding'],value,image,inventory,records,imports)
    except(ValueError,KeyError)as error:rejected.append(dict(caller=row['address'],case=label,rejected=True,reason=str(error)))
    else:raise ValueError('Wrong AES binding accepted:'+label)
   if binding['kind']=='data':
    changed=bytearray(image);changed[int(binding['address'],0)-0x21d7240]^=1
    try:validate(row,rel,binding,value,bytes(changed),inventory,records,imports)
    except ValueError as error:rejected.append(dict(caller=row['address'],case='altered-native-table-word',rejected=True,reason=str(error)))
    else:raise ValueError('Altered original AES table accepted')
 return dict(allPassed=True,cases=rejected,sourceCredit=0)
