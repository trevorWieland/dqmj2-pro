import copy,re,hashlib
import match_runtime
from project import ROOT,read_json,sha256
LANE=ROOT/'evidence/lanes/parallel-wave20261106/g3d-blendvis-next'

def verify_original(row,bindings):
 v=read_json(LANE/'native-inputs.json')
 for k in['image','inventory','relocations']:
  if sha256(ROOT/v[k]['path'])!=v[k]['sha256']:raise ValueError('Original BlendVis namespace changed')
 item=v['entries'][0]
 if(row.get('program')or'',row['processor'],row['module'],row['mode'],row['address'],row['bytes'],row['targetSha256'])!=('','arm9','main','arm','0x202e260',128,item['targetSha256']):raise ValueError('Whole BlendVis caller identity differs')
 if row['relocations']or bindings or item['originalRelocationRecords']:raise ValueError('BlendVis is not a no-relocation caller')
 if item['canonicalInventoryRecord']not in(ROOT/v['inventory']['path']).read_text().splitlines():raise ValueError('Original BlendVis entry absent')
 return dict(allPassed=True,wholeCanonicalArmCallerVerified=True,directRelocations=[],runtimeCallbackQualifiedSeparately=True,providerSourceOrExecutionCredit=0)

def callback(binding):
 v=read_json(LANE/'native-inputs.json');expected=v['callbackProvider']
 for k in['program','processor','module','mode','address','bytes','bodySha256']:
  if binding.get(k)!=expected[k]:raise ValueError('Real callback identity differs: '+k)
 image=(ROOT/v['image']['path']).read_bytes()
 if hashlib.sha256(image[0x34448:0x34480]).hexdigest()!=binding['bodySha256']or expected['canonicalInventoryRecord']not in(ROOT/v['inventory']['path']).read_text().splitlines():raise ValueError('Real callback entry/body absent')
 return dict(allPassed=True,actualWholeCanonicalArmCallback=expected,providerSourceOrExecutionCredit=0)

def negative_controls(rows):
 row,=rows;rejected=[]
 for key,value in[('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address','0x202e264'),('bytes',132),('targetSha256','0'*64)]:
  x=copy.deepcopy(row);x[key]=value
  try:verify_original(x,{})
  except ValueError as e:rejected.append(dict(kind='caller',field=key,rejected=True,reason=str(e)))
  else:raise ValueError('Wrong caller identity accepted')
 provider=read_json(LANE/'native-inputs.json')['callbackProvider'];callback(provider)
 for key,value in[('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address','0x203444c'),('bytes',60),('bodySha256','0'*64),('address','0x20343fc')]:
  x=copy.deepcopy(provider);x[key]=value
  try:callback(x)
  except ValueError as e:rejected.append(dict(kind='callback',field=key,rejected=True,reason=str(e)))
  else:raise ValueError('Wrong callback accepted')
 return dict(allPassed=True,cases=rejected,providerSourceOrExecutionCredit=0)
