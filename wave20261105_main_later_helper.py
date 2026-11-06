import copy
import hashlib
from project import ROOT,read_json,sha256

INPUT=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/fixture-helper-inputs.json'
INPUT_SHA='bd348b54c3de9dead3743f00bab950a82de098c956b55acf8aa72f0af39cd328'


def frozen_inputs():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Immutable original fill helper contract changed')
    value=read_json(INPUT)
    for key in ['image','inventory']:
        pin=value[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable helper image/inventory changed')
    return value


def validate(value,image,inventory):
    if (value['program'],value['processor'],value['module'],value['mode'],value['kind'])!=('','arm9','main','arm','function'):raise ValueError('Original fill helper namespace/kind/mode differs')
    if value['address']!='0x2008c14' or value['bytes']!=20:raise ValueError('Original helper entry/complete extent differs')
    if value['canonicalInventoryRecord']!='func_02008c14 kind:function(arm,size=0x14) addr:0x02008c14' or value['canonicalInventoryRecord'] not in inventory.splitlines():raise ValueError('Exact canonical ARM helper entry/extent absent')
    body=image[0x8c14:0x8c28]
    if body.hex()!=value['nativeBytesHex'] or hashlib.sha256(body).hexdigest()!=value['nativeSha256']:raise ValueError('Original complete fill helper changed')
    return dict(status='passed',program='',processor='arm9',module='main',mode='arm',address=value['address'],bytes=20,nativeSha256=value['nativeSha256'],helperCodeAndExtentCredit=0)


def execute():
    value=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();positive=validate(value,image,inventory);results=[]
    for label,key,wrong in [('program','program','dwc/utility.bin/move/child.srl'),('CPU','processor','arm7'),('module','module','ov000'),('mode','mode','thumb'),('kind','kind','data'),('interior-entry','address','0x2008c18'),('truncated-extent','bytes',16)]:
        changed=copy.deepcopy(value);changed[key]=wrong
        try:validate(changed,image,inventory)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid native helper accepted: '+label)
    changed=bytearray(image);changed[0x8c1c]^=4
    for label,raw,inv in [('changed-native-store',bytes(changed),inventory),('missing-canonical-entry',image,inventory.replace(value['canonicalInventoryRecord'],''))]:
        try:validate(value,raw,inv)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Changed native helper proof accepted: '+label)
    return dict(status='passed',positive=positive,negativeCases=results,helperCodeAndExtentCredit=0)
