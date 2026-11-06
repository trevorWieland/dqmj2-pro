import copy,re,hashlib,struct
import match_runtime
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-md5-next'
NATIVE=LANE/'native-inputs.json'
IMPORTS=LANE/'original-imports.json'

def inputs():
 if sha256(NATIVE)!='47e2f341d15eef00fa0a09bd563083688d96e62820ff252c1e179cda5031b560'or sha256(IMPORTS)!='711cd45b5f7bb8d9c747dc48b98feeadff65a2ef9a5b2a2166662c5997d685ac':raise ValueError('Frozen MD5 native/import contract changed')
 value=read_json(NATIVE)
 for key in ['image','inventory','relocations']:
  pin=value[key]
  if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Original MD5 namespace changed')
 return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text(),read_json(IMPORTS)

def validate(row,rel,binding,value,image,inventory,records,imports):
 if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','ov006','thumb'):raise ValueError('MD5 caller namespace differs')
 item=next((x for x in value['entries']if x['address']==row['address']),None)
 if not item or(item['bytes'],item['targetSha256'])!=(row['bytes'],row['targetSha256']):raise ValueError('Whole MD5 extent differs')
 address=int(row['address'],0);native=image[address-0x21d7240:address-0x21d7240+row['bytes']]
 if hashlib.sha256(native).hexdigest()!=row['targetSha256']or item['canonicalInventoryRecord']not in inventory.splitlines():raise ValueError('Original MD5 body/entry differs')
 origin=address+rel['offset'];found=[s for s in item['originalRelocationRecords']if s.startswith('from:0x%08x '%origin)]
 if len(found)!=1 or found[0]not in records.splitlines():raise ValueError('Unique original MD5 relocation absent')
 record=found[0];match=re.fullmatch(r'from:0x[0-9a-f]+ kind:(load|thumb_call) to:(0x[0-9a-f]+) module:overlay\(6\)',record)
 if not match:raise ValueError('Original explicit overlay6 target absent')
 kind,target=match[1],int(match[2],0)
 if(binding.get('program')or'',binding['processor'],binding['module'],int(binding['address'],0))!=('','arm9','ov006',target)or int(rel['target'],0)!=target:raise ValueError('Original MD5 target namespace/entry differs')
 word=image[origin-0x21d7240:origin-0x21d7240+4]
 if kind=='load':
  view=imports['dataViews'].get(hex(target))
  if not view or(binding['kind'],binding['mode'])!=('data','data')or rel['type']!=2 or rel['addend']!=0 or struct.unpack('<I',word)[0]!=target:raise ValueError('Original MD5 data ABS32 differs')
  if view['elements']!=64 or view['elementBytes']!=1 or view['extentBytes']!=64:raise ValueError('Complete MD5 data view differs')
  raw=image[target-0x21d7240:target-0x21d7240+view['extentBytes']]
  if hashlib.sha256(raw).hexdigest()!=view['sha256']:raise ValueError('Native full MD5 table/rcon bytes differ')
  canonical=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:data(?:\(any\))? addr:0x%08x'%target,s)),None)
  if canonical is None:raise ValueError('Existing original table symbol absent')
  witness=dict(originalRecord=record,origin=hex(origin),target=hex(target),canonicalInventoryRecord=canonical,dataView=view,fullNativeDataSpanHashChecked=True,storageSourceCredit=0)
 else:
  sizes={0x21f152c:118,0x21f15f8:2120,0x21f1e40:44,0x21f1e6c:42,0x21f1e98:22,0x21f1eb0:22}
  if target not in sizes or(binding['kind'],binding['mode'],rel['type'],rel['addend'])!=('function','thumb',10,-4):raise ValueError('MD5 code provider differs')
  decoded=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(word,origin));assert len(decoded)==1
  if decoded[0].mnemonic!='bl'or decoded[0].op_str!='#'+hex(target):raise ValueError('Original MD5 branch differs')
  canonical=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(thumb,size=0x%x\) addr:0x%08x'%(sizes[target],target),s)),None)
  if canonical is None:raise ValueError('MD5 original complete helper boundary absent')
  witness=dict(originalRecord=record,origin=hex(origin),target=hex(target),canonicalInventoryRecord=canonical,selectedSamePacketCodeProvider=target in[0x21f152c,0x21f15f8],extraProviderCredit=0)

 verify_binding(rel['symbol'],binding);return witness

def arithmetic_literal(row):
 if row['address']!='0x21f15f8':return dict(notApplicable=True)
 from wave20261106_ov006_md5_next_prototypes import function_bytes
 data=function_bytes(ROOT/row['object'],row['name']);offset=0x21f1dcc-0x21f15f8;assert data[offset:offset+4]==struct.pack('<I',(-0xfde5380c)&0xffffffff)
 assert not any(r['offset']==offset or int(r['target'],0)==0x21ac7f4 for r in row['relocations'])
 native=(ROOT/'extract/arm9_overlays/ov006.bin').read_bytes();consumer=native[0x21f1ab6-0x21d7240:0x21f1ac4-0x21d7240];instructions=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(consumer,0x21f1ab6));assert[(x.mnemonic,x.op_str)for x in instructions[:2]]==[('ldr','r2, [pc, #0x314]'),('subs','r2, r5, r2')]
 source=(ROOT/row['source']).read_text();assert re.search(r'HH\s*\(\s*b, c, d, a, x\[14\], S34, 0xfde5380c\)',source)
 return dict(originalConfiguredRecordPreserved='from:0x021f1dcc kind:load to:0x021ac7f4 module:main',pool='0x21f1dcc',sourceObjectLiteralOffset=offset,sourceObjectScalarWord='0x021ac7f4',primaryRound36Constant='0xfde5380c',consumer='0x21f1ab6',entryReachableImmediateSubtract='0x21f1ab8',rotateLeftBits=23,sourceObjectHasNoPointerRelocationAtLiteral=True,noMainPointerAliasOrBinding=True,sourceStorageCredit=0)

def verify_original(row,bindings):
 value,image,inventory,records,imports=inputs();return dict(witnesses=[validate(row,r,bindings[r['symbol']],value,image,inventory,records,imports)for r in row['relocations']],arithmeticLiteral=arithmetic_literal(row),allActualRelocationsExplicitOv006OriginalReferences=True,importedStorageSourceCredit=0)


def negative_controls(rows):
 value,image,inventory,records,imports=inputs();rejected=[]
 for row in rows:
  for rel in row['relocations']:
   binding=row['nativeSymbolEntries'][rel['symbol']]
   for label,owner,key,wrong in [('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('main','binding','module','main'),('mode','binding','mode','arm'),('interior','binding','address',hex(int(binding['address'],0)+4)),('origin','rel','offset',rel['offset']+2),('addend','rel','addend',rel['addend']+4),('type','rel','type',1),('caller-mode','row','mode','arm')]:
    obj={k:copy.deepcopy(v)for k,v in [('row',row),('rel',rel),('binding',binding)]};obj[owner][key]=wrong
    try:validate(obj['row'],obj['rel'],obj['binding'],value,image,inventory,records,imports)
    except(ValueError,KeyError)as error:rejected.append(dict(caller=row['address'],case=label,rejected=True,reason=str(error)))
    else:raise ValueError('Wrong MD5 binding accepted:'+label)
   if binding['kind']=='data':
    changed=bytearray(image);changed[int(binding['address'],0)-0x21d7240]^=1
    try:validate(row,rel,binding,value,bytes(changed),inventory,records,imports)
    except ValueError as error:rejected.append(dict(caller=row['address'],case='altered-native-table-word',rejected=True,reason=str(error)))
    else:raise ValueError('Altered original MD5 table accepted')
 row=next(r for r in rows if r['address']=='0x21f15f8');fake=dict(offset=0x21f1dcc-0x21f15f8,type=2,addend=0,target='0x21ac7f4',symbol='native_data_main_021ac7f4');binding=dict(program='',processor='arm9',module='main',mode='data',kind='data',address='0x21ac7f4')
 try:validate(row,fake,binding,value,image,inventory,records,imports)
 except ValueError as error:rejected.append(dict(caller=row['address'],case='arithmetic-literal-invented-main-pointer',rejected=True,reason=str(error)))
 else:raise ValueError('MD5 scalar accepted as fabricated pointer binding')
 return dict(allPassed=True,cases=rejected,sourceCredit=0)
