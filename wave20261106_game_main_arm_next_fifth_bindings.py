import copy
import hashlib
import struct
from project import ROOT,sha256,read_json
from link_runtime_unit import verify_binding
from wave20261104_main_tail_bindings import verify_original as branch_verify

INPUT=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/fifth/data-inputs.json'
INPUT_SHA='2b24c6502d70a3c6aecd7351280f633e4d268bdadd0b357a3c8e8dcf8e3f83bb'


def frozen_inputs():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Exact resource-name input changed')
    value=read_json(INPUT)
    for key in ['image','inventory','relocations']:
        if sha256(ROOT/value[key]['path'])!=value[key]['sha256']:raise ValueError('Pinned original reference changed')
    return value


def validate(case,row,relocation,binding,image,inventory,loads):
    if tuple(row.get(k) or '' for k in ['program','processor','module','mode'])!=('','arm9','main','arm') or tuple(case.get(k) or '' for k in ['program','processor','module','mode'])!=('','arm9','main','arm'):raise ValueError('Original string caller namespace differs')
    if tuple(binding.get(k) or '' for k in ['program','processor','module','mode','kind'])!=('','arm9','main','data','data'):raise ValueError('Original string namespace/kind/mode differs')
    if (row['address'],row['bytes'],row['targetSha256'])!=(case['caller'],case['bytes'],case['callerSha256']) or (row['address'],row['bytes'],case['symbol'])!=('0x207154c',92,'native_data_020de394'):raise ValueError('String escaped its single measured caller')
    if (relocation['symbol'],relocation['offset'],relocation['type'],relocation['addend'])!=(case['symbol'],88,2,0) or case['offset']!=88:raise ValueError('Original string ABS32 origin/addend differs')
    target,origin=0x020de394,0x020715a4
    if any(int(v,0)!=target for v in [binding['address'],relocation['target'],case['target']]) or int(case['literalPool'],0)!=origin:raise ValueError('Original string literal/target differs')
    record='data_020de394 kind:data(any) addr:0x020de394';load='from:0x020715a4 kind:load to:0x020de394 module:main'
    if case['originalInventoryRecord']!=record or record not in inventory.splitlines() or case['originalLoadRecord']!=load or load not in loads.splitlines():raise ValueError('Original string inventory/load missing')
    native=image[0x7154c:0x715a8];literal=image[0x715a4:0x715a8];prefix=image[0xde394:0xde394+22]
    if len(native)!=92 or hashlib.sha256(native).hexdigest()!=case['callerSha256'] or literal!=struct.pack('<I',target) or literal.hex()!=case['literalWordHex']:raise ValueError('Original string caller/pool changed')
    if case['minimumInitializedPrefix']!=22 or case['encoding']!='nul-terminated-ascii' or prefix!=b'fld_up_menu_parts.cch\0' or hashlib.sha256(prefix).hexdigest()!=case['initializedPrefixSha256']:raise ValueError('Exact terminated resource name differs')
    instruction=struct.unpack_from('<I',native,16)[0]
    if case['instructionWords']!={'16':0xe59f1040} or instruction!=0xe59f1040 or 0x207155c+8+(instruction&4095)!=origin:raise ValueError('Original R1 PC-relative literal read differs')
    if case!=frozen_inputs()['cases'][0] or case['completeObjectExtent'] is not None or case['externalStorageCredit']!=0:raise ValueError('Frozen minimum string/storage contract differs')
    verify_binding(case['symbol'],binding)
    return dict(symbol=case['symbol'],origin=hex(origin),target=hex(target),minimumInitializedPrefix=22,initializedPrefixSha256=case['initializedPrefixSha256'],originalInventoryRecord=record,originalLoadRecord=load,completeObjectExtent=None,externalStorageCredit=0)


def verify_original(row,bindings):
    proof=branch_verify(dict(row,relocations=[r for r in row['relocations'] if r['type']!=2]),bindings);value=frozen_inputs();data=[r for r in row['relocations'] if r['type']==2]
    if len(data)!=1:raise ValueError('One exact original resource-name reference required')
    witness=validate(value['cases'][0],row,data[0],bindings[data[0]['symbol']],(ROOT/value['image']['path']).read_bytes(),(ROOT/value['inventory']['path']).read_text(),(ROOT/value['relocations']['path']).read_text())
    return dict(proof,originalDataLoadWitnesses=[witness],dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=INPUT_SHA),externalStorageCredit=0)


def negative_controls(rows):
    value=frozen_inputs();case=value['cases'][0];row=rows[0];relocation=next(r for r in row['relocations'] if r['type']==2);binding=row['nativeSymbolEntries'][case['symbol']];image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();results=[]
    changes=[('wrong-origin','relocation','offset',84),('nonzero-addend','relocation','addend',4),('same-text-wrong-symbol','binding','address','0x20de3ac'),('wrong-CPU','binding','processor','arm7'),('wrong-program','binding','program','child'),('wrong-overlay','binding','module','ov000'),('function-kind','binding','kind','function'),('function-mode','binding','mode','arm'),('missing-terminator-extent','case','minimumInitializedPrefix',21),('invented-object-extent','case','completeObjectExtent',22),('invented-storage-credit','case','externalStorageCredit',22)]
    for label,owner,key,wrong in changes:
        parts={k:copy.deepcopy(v) for k,v in [('case',case),('row',row),('relocation',relocation),('binding',binding)]};parts[owner][key]=wrong
        try:validate(parts['case'],parts['row'],parts['relocation'],parts['binding'],image,inventory,loads)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong initialized resource contract admitted')
    changed=bytearray(image);changed[0xde394]^=1;pool=bytearray(image);pool[0x715a4]^=4
    for label,raw,inv,records in [('changed-name',bytes(changed),inventory,loads),('changed-pool',bytes(pool),inventory,loads),('missing-inventory',image,inventory.replace(case['originalInventoryRecord'],''),loads),('missing-load',image,inventory,loads.replace(case['originalLoadRecord'],''))]:
        try:validate(case,row,relocation,binding,raw,inv,records)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Changed original string proof admitted')
    return dict(status='passed',sourceCredit=0,rejections=results)
