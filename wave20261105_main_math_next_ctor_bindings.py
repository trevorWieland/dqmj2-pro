import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from link_runtime_unit import verify_binding

INPUT=ROOT/'evidence/lanes/parallel-wave20261105/main-math-next/ctor/literal-input.json'
INPUT_SHA='047189c7f7f0b4425a1b1292035a49bc4663587b7cec663487018e7e58ad65e1'


def frozen():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Immutable linker-constant witness changed')
    value=read_json(INPUT)
    for key in ['image','inventory','relocations']:
        item=value[key]
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Original linker-constant image/inventory/records changed')
    return value


def validate(value,row,rel,binding,image,inventory,records):
    if value['romSha256']!='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':raise ValueError('Original ROM identity differs')
    if (row.get('program') or '',row['processor'],row['module'],row['mode'],row['address'],row['bytes'])!=('','arm9','main','arm','0x2026a94',44):raise ValueError('Complete constructor caller namespace differs')
    if (value.get('program') or '',value['processor'],value['module'],value['mode'],value['caller'],value['bytes'])!=('','arm9','main','arm','0x2026a94',44):raise ValueError('Frozen constructor namespace differs')
    if (binding.get('program') or '',binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['address'])!=('','arm9','main','data','data','0x20dcb30'):raise ValueError('Exact linker constant binding differs')
    if (rel['symbol'],rel['offset'],rel['type'],rel['addend'],rel['target'])!=('native_data_020dcb30',40,2,0,'0x20dcb30'):raise ValueError('Original ABS32 symbol/origin/addend changed')
    if (value['literal'],value['literalWordHex'],value['originalRecord'],value['linkerSymbol'],value['target'],value['pointerWidth'],value['firstPointerBytes'])!=('0x2026abc','30cb0d02','from:0x02026abc kind:link_time_const(ARM9_CTOR_START)','ARM9_CTOR_START','0x20dcb30',4,'00000000'):raise ValueError('Original linker symbol/kind/literal/empty pointer contract differs')
    if value['originalRecord'] not in records.splitlines():raise ValueError('Original explicit linker-constant record absent')
    if any(re.search(r' addr:0x020dcb30$',line) for line in inventory.splitlines()):raise ValueError('Qualification does not invent or rebind a configured data entry')
    native=image[0x26a94:0x26ac0]
    if hashlib.sha256(native).hexdigest()!=value['callerSha256'] or row['targetSha256']!=value['callerSha256']:raise ValueError('Complete original constructor body changed')
    if image[0x26abc:0x26ac0].hex()!=value['literalWordHex'] or struct.unpack_from('<I',image,0x26abc)[0]!=0x20dcb30 or image[0xdcb30:0xdcb34].hex()!=value['firstPointerBytes']:raise ValueError('Original linker literal or first pointer word changed')
    if image[0x26aa0:0x26aa4].hex()!='30ff2fe1':raise ValueError('Original indirect interworking constructor call changed')
    verify_binding(rel['symbol'],binding)
    return dict(status='passed',origin='0x2026abc',target='0x20dcb30',originalRecord=value['originalRecord'],originalMetadataKind='link_time_const(ARM9_CTOR_START)',bindingRepresentation='zero-storage absolute data symbol',actualPointerWidth=4,firstObservedPointer=0,completeTableExtentUnproven=True,nonzeroCallbackNamespaceUnqualified=True,originalStorageExtentAuthorshipCredit=0,callbackSourceCredit=0)


def verify_original(row,bindings):
    value=frozen()
    if len(row['relocations'])!=1:raise ValueError('Constructor literal closure differs')
    rel=row['relocations'][0]
    return validate(value,row,rel,bindings[rel['symbol']],(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text())


def negative_controls(row):
    value=frozen();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();records=(ROOT/value['relocations']['path']).read_text();rel=row['relocations'][0];binding=row['nativeSymbolEntries'][rel['symbol']];negative=[]
    cases=[('ROM','value','romSha256','0'*64),('origin','rel','offset',44),('plus8','rel','addend',8),('kind','rel','type',1),('target','binding','address','0x20dcb34'),('function-kind','binding','kind','function'),('mode','binding','mode','arm'),('CPU','binding','processor','arm7'),('program','binding','program','child'),('module','binding','module','ov000'),('metadata-as-load','value','originalRecord','from:0x02026abc kind:load to:0x020dcb30 module:main'),('pointer-width','value','pointerWidth',8),('origin-value','value','literal','0x2026ab8'),('linker-symbol','value','linkerSymbol','ARM7_CTOR_START')]
    for label,owner,key,wrong_value in cases:
        objects={k:copy.deepcopy(x) for k,x in [('value',value),('row',row),('rel',rel),('binding',binding)]};objects[owner][key]=wrong_value
        try:validate(objects['value'],objects['row'],objects['rel'],objects['binding'],image,inventory,records)
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong constructor linker-constant witness admitted')
    for label,address in [('literal-byte',0x26abc),('first-pointer',0xdcb30),('indirect-call-instruction',0x26aa0)]:
        changed=bytearray(image);changed[address]^=1
        try:validate(value,row,rel,binding,bytes(changed),inventory,records)
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Changed original constructor bytes admitted')
    try:validate(value,row,rel,binding,image,inventory,records.replace(value['originalRecord'],''))
    except ValueError as error:negative.append(dict(case='missing-original-record',rejected=True,reason=str(error)))
    else:raise ValueError('Missing original linker record admitted')
    return dict(status='passed',cases=negative)
