import copy
import struct
import hashlib
from project import ROOT,sha256,read_json
from link_runtime_unit import verify_binding
from wave20261104_main_tail_bindings import verify_original as branch_verify
from wave20261104_main_command_forward_bindings import validate as original_data_validate

INPUT=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/third/data-inputs.json'
INPUT_SHA='fc361183ebfad7107d9d25476fdc823a7ae078e2f25c31326ec899e2936b0862'


def frozen_inputs():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Exact second data contract changed')
    value=read_json(INPUT)
    for key in ['image','inventory','relocations']:
        if sha256(ROOT/value[key]['path'])!=value[key]['sha256']:raise ValueError('Original data proof input changed')
    return value


def initialized_table(case,row,relocation,binding,image,inventory,loads):
    if tuple(row.get(k) or '' for k in ['program','processor','module','mode'])!=('','arm9','main','arm') or tuple(case.get(k) or '' for k in ['program','processor','module','mode'])!=('','arm9','main','arm'):raise ValueError('Initialized lookup caller namespace differs')
    if tuple(binding.get(k) or '' for k in ['program','processor','module','mode','kind'])!=('','arm9','main','data','data'):raise ValueError('Initialized lookup is not exact ARM9 main data')
    if (row['address'],row['bytes'],row['targetSha256'])!=(case['caller'],case['bytes'],case['callerSha256']) or (row['address'],row['bytes'],case['symbol'])!=('0x2071b28',116,'native_data_020daf42'):raise ValueError('Initialized lookup escaped the one measured caller')
    if (relocation['symbol'],relocation['offset'],relocation['type'],relocation['addend'])!=(case['symbol'],112,2,0) or case['offset']!=112:raise ValueError('Initialized lookup original ABS32 origin/addend differs')
    target=0x020daf42;origin=0x02071b98
    if int(binding['address'],0)!=target or int(relocation['target'],0)!=target or int(case['target'],0)!=target or int(case['literalPool'],0)!=origin:raise ValueError('Initialized lookup target/literal differs')
    record='data_020daf42 kind:data(any) addr:0x020daf42';load='from:0x02071b98 kind:load to:0x020daf42 module:main'
    if case['originalInventoryRecord']!=record or record not in inventory.splitlines() or case['originalLoadRecord']!=load or load not in loads.splitlines():raise ValueError('Exact original initialized-data inventory/load missing')
    start=0x071b28;literal=image[origin-0x02000000:origin-0x02000000+4]
    if hashlib.sha256(image[start:start+116]).hexdigest()!=case['callerSha256'] or literal.hex()!=case['literalWordHex'] or literal!=struct.pack('<I',target):raise ValueError('Original initialized lookup caller/pool changed')
    if [case.get(k) for k in ['minimumInitializedPrefix','indexMinimum','indexMaximum','indexStride','elementWidth','signedElement']]!=[17,0,8,2,1,True]:raise ValueError('Bounded nine-element signed stride2 lookup differs')
    prefix=image[target-0x02000000:target-0x02000000+17]
    if len(prefix)!=17 or hashlib.sha256(prefix).hexdigest()!=case['initializedPrefixSha256']:raise ValueError('Measured initialized lookup prefix changed')
    words={60:0xe1a00086,64:0xe19500d0,96:0xe3560009}
    if {int(k):v for k,v in case['layoutInstructionWords'].items()}!=words or any(struct.unpack_from('<I',image,start+offset)[0]!=word for offset,word in words.items()):raise ValueError('Actual signed byte/index/loop instruction differs')
    verify_binding(relocation['symbol'],binding)
    return dict(symbol=case['symbol'],origin=hex(origin),target=hex(target),originalInventoryRecord=record,originalLoadRecord=load,minimumInitializedPrefix=17,initializedPrefixSha256=case['initializedPrefixSha256'],signedElement=True,indexStride=2,completeObjectExtent=None,originalDataStorageCredit=0)


def validate(case,row,relocation,binding,image,inventory,loads):
    proof=initialized_table(case,row,relocation,binding,image,inventory,loads) if case['symbol']=='native_data_020daf42' else original_data_validate(case,row,relocation,binding,image,inventory,loads)
    expected=next((c for c in frozen_inputs()['cases'] if (c['caller'],c['symbol'])==(case['caller'],case['symbol'])),None)
    if case!=expected or case['completeObjectExtent'] is not None or case['externalStorageCredit']!=0 or case['typedAccesses']:raise ValueError('Exact zero-credit column/word/coordinate contract differs')
    start=int(row['address'],0)-0x02000000;origin=int(case['literalPool'],0)
    for offset,word in case['instructionWords'].items():
        at=int(row['address'],0)+int(offset);actual=struct.unpack_from('<I',image,start+int(offset))[0]
        if actual!=word or actual&0x0f7f0000!=0x051f0000 or at+8+(1 if actual&0x00800000 else -1)*(actual&4095)!=origin:raise ValueError('Actual original ARM literal-read instruction differs')
    return dict(proof,layout=case['layout'],instructionWords=case['instructionWords'],completeObjectExtent=None)


def verify_original(row,bindings):
    proof=branch_verify(dict(row,relocations=[r for r in row['relocations'] if r['type']!=2]),bindings);value=frozen_inputs()
    image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();data=[r for r in row['relocations'] if r['type']==2];cases=[c for c in value['cases'] if c['caller']==row['address']]
    if len(data)!=len(cases):raise ValueError('Every original data literal is required')
    witnesses=[]
    for relocation in data:
        case=next((c for c in cases if c['symbol']==relocation['symbol']),None)
        if case is None:raise ValueError('Unqualified original storage symbol')
        witnesses.append(validate(case,row,relocation,bindings[relocation['symbol']],image,inventory,loads))
    return dict(proof,originalDataLoadWitnesses=witnesses,dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=INPUT_SHA),externalStorageCredit=0)


def negative_controls(rows):
    value=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();results=[]
    for case in value['cases']:
        row=next(r for r in rows if r['address']==case['caller']);relocation=next(r for r in row['relocations'] if r['symbol']==case['symbol']);binding=row['nativeSymbolEntries'][case['symbol']]
        changes=[('wrong-origin','relocation','offset',relocation['offset']-4),('wrong-addend','relocation','addend',4),('wrong-base','binding','address',hex(int(binding['address'],0)+4)),('wrong-CPU','binding','processor','arm7'),('wrong-program','binding','program','child'),('wrong-module','binding','module','ov000'),('function-kind','binding','kind','function'),('function-mode','binding','mode','arm'),('wrong-stride','case','layout',dict(case['layout'],stride=8)),('invented-extent','case','completeObjectExtent',100),('invented-storage-credit','case','externalStorageCredit',1)]
        for label,owner,key,wrong in changes:
            versions={k:copy.deepcopy(v) for k,v in [('case',case),('row',row),('relocation',relocation),('binding',binding)]};versions[owner][key]=wrong
            try:validate(versions['case'],versions['row'],versions['relocation'],versions['binding'],image,inventory,loads)
            except ValueError as error:results.append(dict(caller=row['address'],symbol=case['symbol'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Invalid original data contract admitted')
        changed=bytearray(image);changed[int(case['literalPool'],0)-0x02000000]^=4
        for label,raw,inv,records in [('changed-literal',bytes(changed),inventory,loads),('missing-inventory',image,inventory.replace(case['originalInventoryRecord'],''),loads),('missing-load-record',image,inventory,loads.replace(case['originalLoadRecord'],''))]:
            try:validate(case,row,relocation,binding,raw,inv,records)
            except ValueError as error:results.append(dict(caller=row['address'],symbol=case['symbol'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Changed original data proof admitted')
    return dict(status='passed',sourceCredit=0,rejections=results)
