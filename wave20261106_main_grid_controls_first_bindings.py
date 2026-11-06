import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM


NATIVE=ROOT/'evidence/lanes/parallel-wave20261106/main-grid-controls-next/first/native-inputs.json'
NATIVE_SHA='13a9c3d7234e840951e1329a382a0be80e9bf48fb601376e93e0f681f8360dd7'


def inputs():
    if sha256(NATIVE)!=NATIVE_SHA:raise ValueError('Exact original grid input contract changed')
    value=read_json(NATIVE)
    for name in ['image','inventory','relocations']:
        pin=value[name]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Original image/inventory input changed')
    return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text()


def caller(row,value,image,inventory):
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','arm'):raise ValueError('Actual grid CPU/program/module/mode differs')
    expected=next(e for e in value['entries']if e['address']==row['address']);a=int(row['address'],0)
    if(row['address'],row['bytes'],row['targetSha256'])!=(expected['address'],expected['bytes'],expected['targetSha256']):raise ValueError('Actual complete grid identity differs')
    if hashlib.sha256(image[a-0x2000000:a-0x2000000+expected['bytes']]).hexdigest()!=row['targetSha256']or expected['canonicalInventoryRecord']not in inventory.splitlines():raise ValueError('Actual full original body/boundary changed')


def validate(row,rel,binding,value,image,inventory,records):
    caller(row,value,image,inventory);origin=int(row['address'],0)+rel['offset'];found=[line for line in next(e for e in value['entries']if e['address']==row['address'])['originalRelocationRecords']if line.startswith('from:0x'+format(origin,'08x')+' ')]
    if len(found)!=1 or found[0]not in records.splitlines():raise ValueError('Exact original grid relocation origin absent')
    record=found[0];m=re.fullmatch(r'from:0x[0-9a-f]+ kind:(arm_call|load) to:(0x[0-9a-f]+) module:main',record)
    if m is None:raise ValueError('Original grid relocation module/kind differs')
    target=int(m[2],0)
    if int(rel['target'],0)!=target or(binding.get('program')or'',binding['processor'],binding['module'],int(binding['address'],0))!=('','arm9','main',target):raise ValueError('Actual original grid target namespace/address differs')
    word=image[origin-0x2000000:origin-0x2000000+4]
    if m[1]=='arm_call':
        if(rel['type'],rel['addend'],binding['kind'],binding['mode'])!=(1,-8,'function','arm'):raise ValueError('Actual original ARM call type/addend/kind/mode differs')
        decoded=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(word,origin))
        if len(decoded)!=1 or decoded[0].mnemonic!='bl'or decoded[0].op_str!='#'+hex(target):raise ValueError('Actual original ARM BL target/opcode differs')
        canonical=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x%08x'%target,line)),None)
        if canonical is None:raise ValueError('Actual original target lacks canonical ARM entry')
    else:
        if(rel['type'],rel['addend'],binding['kind'],binding['mode'],target)!=(2,0,'data','data',target)or target not in [0x021d6b5c,0x021d6b64]or struct.unpack('<I',word)[0]!=target:raise ValueError('Actual original grid BSS literal/addend/kind differs')
        canonical=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:bss addr:0x%08x'%target,line)),None)
        if canonical is None:raise ValueError('Actual configured page BSS boundary absent')
    verify_binding(rel['symbol'],binding)
    return dict(originalRecord=record,origin=hex(origin),target=hex(target),nativeWord=word.hex(),canonicalTargetRecord=canonical,calleeCodeCredit=0,storageCredit=0)


def field(row,access,value,image,inventory,records):
    caller(row,value,image,inventory)
    expected=next((v for v in value['fieldAccesses']if v['caller']==row['address']and v['role']==access['role']),None)
    if access!=expected:raise ValueError('Original consumed field origin/width/offset/pointer evidence differs')
    pc=int(access['address'],0);word=image[pc-0x2000000:pc-0x2000000+4]
    decoded=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(word,pc))
    if word.hex()!=access['nativeWord']or len(decoded)!=1 or(decoded[0].mnemonic,decoded[0].op_str)!=(access['mnemonic'],access['operands']):raise ValueError('Actual consumed field opcode differs')
    return dict(access,sourceCredit=0,wholeStorageExtentCredit=0)



def dimension_arguments(row,value,image,records):
    proof=[]
    for item in value['dimensionArguments']:
        origin=int(item['origin'],0)
        if not int(row['address'],0)<=origin<int(row['address'],0)+row['bytes']:continue
        if item['target']not in['0x020d0208','0x020d0210']or not item['argumentInstructions']or item['argumentInstructions'][0]['nativeWord']!='0400a0e1':raise ValueError('Actual full record-count R0 argument differs')
        for instruction in item['argumentInstructions']:
            pc=int(instruction['address'],0)
            if image[pc-0x02000000:pc-0x02000000+4].hex()!=instruction['nativeWord']:raise ValueError('Actual full record-count argument instruction changed')
        record='from:0x%08x kind:arm_call to:%s module:main'%(origin,item['target'])
        if record not in records.splitlines():raise ValueError('Dimension argument original caller target differs')
        proof.append(dict(item,providerParameterUniquenessNotClaimed=True,sourceCredit=0))
    return proof


def verify_original(row,bindings):
    value,image,inventory,records=inputs();fields=[field(row,item,value,image,inventory,records)for item in value['fieldAccesses']if item['caller']==row['address']];witnesses=[]
    for rel in row['relocations']:
        if rel['symbol']not in bindings:raise ValueError('Actual grid import binding missing')
        witnesses.append(validate(row,rel,bindings[rel['symbol']],value,image,inventory,records))
    return dict(witnesses=witnesses,fields=fields,dimensionArguments=dimension_arguments(row,value,image,records),actualOriginalArmWordsEntriesAndFieldsChecked=True,oldNormalizerUnchanged=True,sourceOrStorageCredit=0)


def negative_controls(rows):
    value,image,inventory,records=inputs();negative=[];field_negative=[]
    for row in rows:
        for rel in row['relocations']:
            binding=row['nativeSymbolEntries'][rel['symbol']]
            cases=[('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('mode','binding','mode','thumb'),('interior-entry','binding','address',hex(int(binding['address'],0)+4)),('kind','binding','kind','function'if binding['kind']=='data'else'data'),('origin','rel','offset',rel['offset']+4),('addend-plus8','rel','addend',rel['addend']+8),('type','rel','type',10),('caller-mode','row','mode','thumb')]
            for label,owner,key,wrong in cases:
                objects={k:copy.deepcopy(v)for k,v in [('row',row),('rel',rel),('binding',binding)]};objects[owner][key]=wrong
                try:validate(objects['row'],objects['rel'],objects['binding'],value,image,inventory,records)
                except(ValueError,KeyError)as error:negative.append(dict(case=label,origin=rel['offset'],rejected=True,reason=str(error)))
                else:raise ValueError('Bad grid native binding accepted:'+label)
            changed=bytearray(image);changed[int(row['address'],0)-0x2000000+rel['offset']]^=1;origin=int(row['address'],0)+rel['offset'];record=next(line for line in records.splitlines()if line.startswith('from:0x'+format(origin,'08x')+' '))
            for label,raw,recs in [('native-word',bytes(changed),records),('original-record',image,records.replace(record,''))]:
                try:validate(row,rel,binding,value,raw,inventory,recs)
                except ValueError as error:negative.append(dict(case=label,origin=rel['offset'],rejected=True,reason=str(error)))
                else:raise ValueError('Changed grid original evidence accepted')
        for access in [v for v in value['fieldAccesses']if v['caller']==row['address']]:
            for label,key,wrong in [('field-offset','fieldOffset',access['fieldOffset']+4),('field-width','width',2),('field-origin','address',hex(int(access['address'],0)+4)),('field-word','nativeWord','00000000'),('field-pointer-origin','pointerOrigin','unqualified')]:
                bad=copy.deepcopy(access);bad[key]=wrong
                try:field(row,bad,value,image,inventory,records)
                except ValueError as error:field_negative.append(dict(role=access['role'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Bad original consumed grid field accepted')
    return dict(status='passed',negativeCases=negative,fieldLoadNegatives=field_negative,oldCompilerNormalizerUnchanged=True,sourceCredit=0)
