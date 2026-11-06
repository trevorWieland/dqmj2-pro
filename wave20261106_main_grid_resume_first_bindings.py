import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM


NATIVE=ROOT/'evidence/lanes/parallel-wave20261106/main-grid-resume-next/first/native-inputs.json'
NATIVE_SHA='9c5684eeac423734fd14c3c195e7afc5781ec3602bb70060f72b92b6500fd10d'


def inputs():
    if sha256(NATIVE)!=NATIVE_SHA:raise ValueError('Exact original grid input contract changed')
    value=read_json(NATIVE)
    for name in ['image','inventory','relocations']:
        pin=value[name]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Original image/inventory input changed')
    return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text()


def caller(row,value,image,inventory):
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','arm'):raise ValueError('Actual grid CPU/program/module/mode differs')
    expected=value['entry'];a=int(row['address'],0)
    if(row['address'],row['bytes'],row['targetSha256'])!=(expected['address'],292,expected['targetSha256']):raise ValueError('Actual complete grid identity differs')
    if hashlib.sha256(image[a-0x2000000:a-0x2000000+292]).hexdigest()!=row['targetSha256']or expected['canonicalInventoryRecord']not in inventory.splitlines():raise ValueError('Actual full original body/boundary changed')


def validate(row,rel,binding,value,image,inventory,records):
    caller(row,value,image,inventory);origin=int(row['address'],0)+rel['offset'];found=[line for line in value['entry']['originalRelocationRecords']if line.startswith('from:0x'+format(origin,'08x')+' ')]
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
        if(rel['type'],rel['addend'],binding['kind'],binding['mode'],target)!=(2,0,'data','data',0x021d6b5c)or struct.unpack('<I',word)[0]!=target:raise ValueError('Actual original grid BSS literal/addend/kind differs')
        canonical=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:bss addr:0x021d6b5c',line)),None)
        if canonical is None:raise ValueError('Actual configured page BSS boundary absent')
    verify_binding(rel['symbol'],binding)
    return dict(originalRecord=record,origin=hex(origin),target=hex(target),nativeWord=word.hex(),canonicalTargetRecord=canonical,calleeCodeCredit=0,storageCredit=0)


def field(row,access,value,image,inventory,records):
    caller(row,value,image,inventory);roles={'page':(0x020d0b14,1,1,'ldrb','r1, [r1, #1]'),'first-id':(0x020d0b38,20,4,'ldr','r0, [r0, #0x14]'),'second-id':(0x020d0b98,20,4,'ldr','r0, [r0, #0x14]')}
    expected=roles.get(access['role']);actual=(int(access['address'],0),access['fieldOffset'],access['width'],access['mnemonic'],access['operands'])
    if actual!=expected:raise ValueError('Exact original page/id role/origin/width/offset differs')
    pc=actual[0];word=image[pc-0x2000000:pc-0x2000000+4]
    if word.hex()!=access['nativeWord']:raise ValueError('Actual original consumed field instruction changed')
    decoded=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(word,pc))
    if len(decoded)!=1 or(decoded[0].mnemonic,decoded[0].op_str)!=actual[3:]:raise ValueError('Original field disassembly differs')
    if access['pointerRecord']not in records.splitlines()or access['pointerRecord']not in value['entry']['originalRelocationRecords']:raise ValueError('Actual original field pointer-provider record absent')
    expected_record={'page':'from:0x020d0bf8 kind:load to:0x021d6b5c module:main','first-id':'from:0x020d0b34 kind:arm_call to:0x02062a50 module:main','second-id':'from:0x020d0b94 kind:arm_call to:0x02062a88 module:main'}[access['role']]
    if access['pointerRecord']!=expected_record:raise ValueError('Actual original field pointer source differs')
    return dict(access,sourceCredit=0,wholeStorageExtentCredit=0)


def verify_original(row,bindings):
    value,image,inventory,records=inputs();fields=[field(row,item,value,image,inventory,records)for item in value['fieldAccesses']];witnesses=[]
    for rel in row['relocations']:
        if rel['symbol']not in bindings:raise ValueError('Actual grid import binding missing')
        witnesses.append(validate(row,rel,bindings[rel['symbol']],value,image,inventory,records))
    return dict(witnesses=witnesses,fields=fields,actualOriginalArmWordsEntriesAndFieldsChecked=True,oldNormalizerUnchanged=True,sourceOrStorageCredit=0)


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
        for access in value['fieldAccesses']:
            for label,key,wrong in [('field-offset','fieldOffset',access['fieldOffset']+4),('field-width','width',2),('field-origin','address',hex(int(access['address'],0)+4)),('field-word','nativeWord','00000000'),('field-pointer-record','pointerRecord',access['pointerRecord'].replace('module:main','module:overlay(0,6)'))]:
                bad=copy.deepcopy(access);bad[key]=wrong
                try:field(row,bad,value,image,inventory,records)
                except ValueError as error:field_negative.append(dict(role=access['role'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Bad original consumed grid field accepted')
    return dict(status='passed',negativeCases=negative,fieldLoadNegatives=field_negative,oldCompilerNormalizerUnchanged=True,sourceCredit=0)
