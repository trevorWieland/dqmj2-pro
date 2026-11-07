import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from wave20261106_ov001_large_controller_source_header_clean_paths import EVIDENCE

INPUT=EVIDENCE/'native-inputs.json'
INPUT_SHA='28202bfd5998b13bb0d70bf3f23b0f61bbad5cb031d52106c769e4bb935e7d1a'


def inputs():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Immutable overlay caller input changed')
    value=read_json(INPUT)
    for key in ['image','inventory','relocations','mainImage','mainInventory']:
        pin=value[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Original whole image/configuration changed')
    return value,(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text(),(ROOT/value['mainInventory']['path']).read_text()


def caller(row,value,image,inventory):
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','ov001','arm'):raise ValueError('Caller complete CPU/program/module/mode differs')
    e=next(v for v in value['entries']if v['address']==row['address']);a=int(row['address'],0);base=int(value['base'],0)
    if(row['bytes'],row['targetSha256'])!=(e['bytes'],e['targetSha256'])or hashlib.sha256(image[a-base:a-base+e['bytes']]).hexdigest()!=e['targetSha256']:raise ValueError('Original complete caller extent/body differs')
    if e['canonicalInventoryRecord']not in inventory.splitlines():raise ValueError('Original canonical caller boundary absent')
    return e


def validate(row,rel,binding,value,image,inventory,records,main_inventory):
    e=caller(row,value,image,inventory);origin=int(row['address'],0)+rel['offset'];found=[s for s in e['originalRelocationRecords']if s.startswith('from:0x'+format(origin,'08x')+' ')]
    if len(found)!=1 or found[0]not in records.splitlines():raise ValueError('Original relocation origin/record differs')
    m=re.fullmatch(r'from:0x[0-9a-f]+ kind:(arm_call|load) to:(0x[0-9a-f]+) module:(main|overlay\(1\))',found[0])
    if m is None:raise ValueError('Original singular overlay/main namespace absent')
    target=int(m[2],0);module='main'if m[3]=='main'else'ov001'
    expectedSymbol=('native_fn_'if module=='main'else'native_fn_ov001_')+format(target,'08x')if m[1]=='arm_call'else'native_data_'+format(target,'08x')
    if rel['symbol']!=expectedSymbol:raise ValueError('Exact packet-owned C import name/original namespace differs')
    if int(rel['target'],0)!=target or(binding.get('program')or'',binding['processor'],binding['module'],int(binding['address'],0))!=('','arm9',module,target):raise ValueError('Original relocation target CPU/program/module/address differs')
    word=image[origin-int(value['base'],0):origin-int(value['base'],0)+4]
    if m[1]=='arm_call':
        if(rel['type'],rel['addend'],binding['kind'],binding['mode'])!=(1,-8,'function','arm'):raise ValueError('Actual ARM branch type/addend/kind/mode differs')
        instruction=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(word,origin))
        if len(instruction)!=1 or instruction[0].mnemonic!='bl'or instruction[0].op_str!='#'+hex(target):raise ValueError('Original native BL word differs')
        canonical=next((s for s in(main_inventory if module=='main'else inventory).splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x%08x'%target,s)),None)
    else:
        if(rel['type'],rel['addend'],binding['kind'],binding['mode'])!=(2,0,'data','data')or struct.unpack('<I',word)[0]!=target:raise ValueError('Original data/BSS literal word/type/addend differs')
        if module=='ov001':pattern=r'\S+ kind:bss addr:0x%08x'%target;table=inventory
        elif target==0x020dbc18:pattern=r'\S+ kind:data\(any\) addr:0x020dbc18';table=main_inventory
        elif target==0x021c9698:pattern=r'\S+ kind:bss addr:0x021c9698';table=main_inventory
        else:raise ValueError('Unqualified initialized main data/BSS interface')
        canonical=next((s for s in table.splitlines()if re.fullmatch(pattern,s)),None)
    if canonical is None:raise ValueError('Actual configured function/BSS entry absent')
    verify_binding(rel['symbol'],binding)
    return dict(originalRecord=found[0],origin=hex(origin),target=hex(target),nativeWord=word.hex(),canonicalTargetRecord=canonical,calleeCodeCredit=0,storageCredit=0)


def verify_original(row,bindings):
    args=inputs();proof=[]
    for rel in row['relocations']:
        if rel['symbol']not in bindings:raise ValueError('Original import absent')
        proof.append(validate(row,rel,bindings[rel['symbol']],*args))
    return dict(witnesses=proof,completeNativeOriginalWordsAndNamespacesChecked=True,normalizersUnchanged=True,sourceOrStorageCredit=0)


def negative_controls(rows):
    args=inputs();negative=[]
    for row in rows:
        for rel in row['relocations']:
            binding=row['nativeSymbolEntries'][rel['symbol']]
            for label,owner,key,wrong in [('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('mode','binding','mode','thumb'),('interior-entry','binding','address',hex(int(binding['address'],0)+4)),('kind','binding','kind','data'if binding['kind']=='function'else'function'),('symbol-name','rel','symbol','native_fn_02049adc'),('target-word','rel','target',hex(int(rel['target'],0)+4)),('origin','rel','offset',rel['offset']+4),('addend','rel','addend',rel['addend']+8),('type','rel','type',10),('caller-mode','row','mode','thumb')]:
                objects={k:copy.deepcopy(v)for k,v in [('row',row),('rel',rel),('binding',binding)]};objects[owner][key]=wrong
                try:validate(objects['row'],objects['rel'],objects['binding'],*args)
                except(ValueError,KeyError)as error:negative.append(dict(case=label,caller=row['address'],origin=rel['offset'],rejected=True,reason=str(error)))
                else:raise ValueError('Invalid native overlay contract accepted:'+label)
    return dict(passed=True,negativeCases=negative,normalizersUnchanged=True)
