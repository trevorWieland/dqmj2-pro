import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256

INPUT=ROOT/'evidence/lanes/parallel-wave20261104/main-command-forward/tail/fixture-helper-inputs.json'
INPUT_SHA='78b53af2ff3f202d1d1b0cef3ee055a58326e8da3fd7a26913091ef25c411ab4'


def frozen_inputs():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Immutable helper fixture contract changed')
    value=read_json(INPUT)
    for key in ['image','inventory','relocations']:
        pin=value[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable original helper input changed')
    return value


def validate(case,image,inventory,relocations):
    if (case['program'],case['processor'],case['module'],case['mode'],case['kind'])!=('','arm9','main','arm','function'):raise ValueError('Original fixture helper namespace/kind/mode differs')
    address=int(case['address'],0)
    if address not in (0x2063e38,0x205fb90) or case['bytes']!={0x2063e38:12,0x205fb90:36}[address]:raise ValueError('Original fixture helper entry/complete extent differs')
    record=case['canonicalInventoryRecord']
    if record not in inventory.splitlines() or not re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(case['bytes'],address),record):raise ValueError('Exact canonical ARM helper entry/extent absent')
    body=image[address-0x2000000:address-0x2000000+case['bytes']]
    if body.hex()!=case['nativeBytesHex'] or hashlib.sha256(body).hexdigest()!=case['nativeSha256']:raise ValueError('Complete original helper body changed')
    if address==0x2063e38:
        if body[:8].hex()!='00009fe51eff2fe1' or int(case['literalPool'],0)!=address+8:raise ValueError('Original provider is not exact measured literal getter')
        target=int(case['nativeTarget'],0)
        if body[8:].hex()!=case['literalWordHex'] or struct.unpack('<I',body[8:])[0]!=target or target!=0x21c0e68:raise ValueError('Original provider literal target differs')
        if case['originalLoadRecord']!='from:0x02063e40 kind:load to:0x021c0e68 module:main' or case['originalLoadRecord'] not in relocations.splitlines():raise ValueError('Original provider data-load record missing')
        if case['originalDataInventoryRecord'] not in inventory.splitlines() or not re.fullmatch(r'\S+ kind:(?:bss|data) addr:0x021c0e68',case['originalDataInventoryRecord']):raise ValueError('Original provider data point missing/nondata')
    else:
        if case['originalCallRecord']!='from:0x0205fb98 kind:arm_call to:0x02063e38 module:main' or case['originalCallRecord'] not in relocations.splitlines():raise ValueError('Original query-to-provider callsite differs')
        if sha256(ROOT/case['source'])!=case['sourceSha256']:raise ValueError('Frozen predecessor query source changed')
        for pin in case['sourceDependencies']:
            if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen predecessor query include changed')
    return dict(address=case['address'],bytes=case['bytes'],nativeSha256=case['nativeSha256'],canonicalInventoryRecord=case['canonicalInventoryRecord'],module='main',processor='arm9',program='',mode='arm',sourceAndExtentCredit=0)


def execute():
    value=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();relocs=(ROOT/value['relocations']['path']).read_text();positive=[validate(c,image,inventory,relocs) for c in value['cases']];negatives=[];provider=value['cases'][0]
    for name,key,wrong in [('program','program','dwc/utility.bin/move/child.srl'),('CPU','processor','arm7'),('module','module','ov000'),('mode','mode','thumb'),('kind','kind','data'),('interior-entry','address','0x2063e3c'),('extent','bytes',8),('target-address','nativeTarget','0x21c0e6c')]:
        changed=copy.deepcopy(provider);changed[key]=wrong
        try:validate(changed,image,inventory,relocs)
        except ValueError as error:negatives.append(dict(case=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid fixture helper accepted: '+name)
    changed=bytearray(image);changed[0x63e40]^=4
    tests=[('changed-native-literal',bytes(changed),inventory,relocs),('missing-canonical-entry',image,inventory.replace(provider['canonicalInventoryRecord'],''),relocs),('changed-data-kind',image,inventory.replace(provider['originalDataInventoryRecord'],provider['originalDataInventoryRecord'].replace('kind:bss','kind:function')),relocs),('missing-load-record',image,inventory,relocs.replace(provider['originalLoadRecord'],''))]
    for name,raw,inv,records in tests:
        try:validate(provider,raw,inv,records)
        except ValueError as error:negatives.append(dict(case=name,rejected=True,reason=str(error)))
        else:raise ValueError('Changed native fixture helper evidence accepted: '+name)
    return dict(status='passed',qualifiedHelpers=positive,negativeCases=negatives,sourceAndExtentCredit=0,originalProviderReconstructed=False)
