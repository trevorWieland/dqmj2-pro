import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from wave20261106_ov006_resource_slot_source_second_paths import EVIDENCE


def inputs():
    value=read_json(EVIDENCE/'native-inputs.json');images={};inventories={};records={}
    for name,item in value['images'].items():
        for key in['image','inventory','relocations']:
            if sha256(ROOT/item[key]['path'])!=item[key]['sha256']:raise ValueError('Original whole image/configuration changed')
        images[name]=(ROOT/item['image']['path']).read_bytes();inventories[name]=(ROOT/item['inventory']['path']).read_text();records[name]=(ROOT/item['relocations']['path']).read_text()
    return value,images,inventories,records


def caller(row,value,images,inventories):
    if(row.get('program')or'',row['processor'],row['mode'])!=('','arm9','arm'):raise ValueError('Caller program/CPU/mode differs')
    entry=next((e for e in value['entries']if(e['module'],e['address'])==(row['module'],row['address'])),None)
    if entry is None:raise ValueError('Caller is outside exactly admitted two bodies')
    a=int(row['address'],0);base=int(value['images'][row['module']]['base'],0)
    if(row['bytes'],row['targetSha256'])!=(entry['bytes'],entry['targetSha256'])or hashlib.sha256(images[row['module']][a-base:a-base+entry['bytes']]).hexdigest()!=entry['targetSha256']:raise ValueError('Original whole caller extent/native payload changed')
    if entry['canonicalInventoryRecord']not in inventories[row['module']].splitlines():raise ValueError('Original complete canonical caller entry absent')
    return entry


def validate(row,rel,binding,value,images,inventories,records):
    entry=caller(row,value,images,inventories);origin=int(row['address'],0)+rel['offset'];found=[s for s in entry['originalRelocationRecords']if s.startswith('from:0x%08x '%origin)]
    if len(found)!=1 or found[0]not in records[row['module']].splitlines():raise ValueError('Exact original relocation origin/record differs')
    match=re.fullmatch(r'from:0x[0-9a-f]+ kind:(arm_call|load) to:(0x[0-9a-f]+) module:(main|overlay\([36]\))',found[0])
    if match is None:raise ValueError('Original singular overlay/main namespace absent')
    target=int(match[2],0);module='main'if match[3]=='main'else'ov%03d'%int(re.search(r'\d+',match[3])[0]);offset=origin-int(value['images'][row['module']]['base'],0);word=images[row['module']][offset:offset+4]
    if int(rel['target'],0)!=target or(binding.get('program')or'',binding['processor'],binding['module'],int(binding['address'],0))!=('','arm9',module,target):raise ValueError('Original target program/CPU/module/address differs')
    if match[1]=='arm_call':
        if(rel['type'],rel['addend'],binding['kind'],binding['mode'])!=(1,-8,'function','arm'):raise ValueError('Actual ARM branch type/addend/kind/mode differs')
        instruction=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(word,origin))
        if len(instruction)!=1 or instruction[0].mnemonic!='bl'or instruction[0].op_str!='#'+hex(target):raise ValueError('Original native BL word differs')
        canonical=next((s for s in inventories[module].splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x%08x'%target,s)),None)
    else:
        if(rel['type'],rel['addend'],binding['kind'],binding['mode'],module,target)!=(2,0,'data','data',module,target)or struct.unpack('<I',word)[0]!=target:raise ValueError('Actual external data literal/type/addend/kind differs')
        canonical=next((s for s in inventories[module].splitlines()if re.fullmatch(r'\S+ kind:(?:data\([^)]*\)|bss) addr:0x%08x'%target,s)),None)
    if canonical is None:raise ValueError('Actual configured function/data entry absent')
    verify_binding(rel['symbol'],binding)
    return dict(originalRecord=found[0],origin=hex(origin),target=hex(target),nativeWord=word.hex(),canonicalTargetRecord=canonical,calleeCodeCredit=0,storageCredit=0,externalDataWidthOrExtentCredit=0)


def verify_original(row,bindings):
    args=inputs()
    if len(row['relocations'])!=len(caller(row,*args[:3])['originalRelocationRecords']):raise ValueError('Original complete14 relocation contract differs')
    proof=[validate(row,rel,bindings[rel['symbol']],*args)for rel in row['relocations']]
    return dict(witnesses=proof,completeNativeOriginalWordsAndNamespacesChecked=True,normalizersUnchanged=True,sourceOrStorageCredit=0)


def negative_controls(rows):
    args=inputs();negative=[]
    for row in rows:
        for rel in row['relocations']:
            binding=row['nativeSymbolEntries'][rel['symbol']]
            for label,owner,key,wrong in[('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov001'),('mode','binding','mode','thumb'),('interior-entry','binding','address',hex(int(binding['address'],0)+4)),('kind','binding','kind','data'if binding['kind']=='function'else'function'),('origin','rel','offset',rel['offset']+4),('addend','rel','addend',rel['addend']+8),('type','rel','type',10),('caller-mode','row','mode','thumb')]:
                objects={k:copy.deepcopy(v)for k,v in[('row',row),('rel',rel),('binding',binding)]};objects[owner][key]=wrong
                try:validate(objects['row'],objects['rel'],objects['binding'],*args)
                except(ValueError,KeyError)as error:negative.append(dict(case=label,caller=row['address'],origin=rel['offset'],rejected=True,reason=str(error)))
                else:raise ValueError('Wrong native overlay contract passed:'+label)
    return dict(passed=True,negativeCases=negative,normalizersUnchanged=True)
