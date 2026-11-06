import hashlib
import match_runtime
from project import ROOT,read_json,sha256
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-md5-helper-next'

def verify_original(row,bindings):
 native=read_json(LANE/'native-inputs.json')
 for k in['image','inventory','relocations']:
  if sha256(ROOT/native[k]['path'])!=native[k]['sha256']:raise ValueError('Original MD5 helper namespace changed')
 if bindings or row['relocations']or(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','ov006','thumb'):raise ValueError('Unexpected leaf helper namespace/relocation')
 item=next((x for x in native['entries']if x['address']==row['address']),None)
 if not item or(item['bytes'],item['targetSha256'])!=(row['bytes'],row['targetSha256']):raise ValueError('Whole original MD5 helper extent differs')
 inventory=(ROOT/native['inventory']['path']).read_text();record='func_ov006_%08x kind:function(thumb,size=0x%x) addr:0x%08x'%(int(row['address'],0),row['bytes'],int(row['address'],0))
 if record not in inventory.splitlines():raise ValueError('Original MD5 helper canonical entry absent')
 image=(ROOT/native['image']['path']).read_bytes();a=int(row['address'],0)-0x21d7240
 if hashlib.sha256(image[a:a+row['bytes']]).hexdigest()!=row['targetSha256']:raise ValueError('Native helper body differs')
 return dict(canonicalInventoryRecord=record,exactNativeWholeExtentSha256=row['targetSha256'],noRelocations=True,importedCodeOrStorageCredit=0)

def negative_controls(rows):
 import copy
 rejected=[]
 for row in rows:
  for k,v in[('program','child'),('processor','arm7'),('module','main'),('mode','arm'),('address',hex(int(row['address'],0)+2)),('bytes',row['bytes']-2),('targetSha256','0'*64)]:
   bad=copy.deepcopy(row);bad[k]=v
   try:verify_original(bad,{})
   except ValueError as error:rejected.append(dict(caller=row['address'],field=k,rejected=True,reason=str(error)))
   else:raise ValueError('Bad leaf helper identity accepted')
 return dict(allPassed=True,cases=rejected,sourceOrExecutionCredit=0)
