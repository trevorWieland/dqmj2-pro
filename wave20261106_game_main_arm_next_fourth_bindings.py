import copy
import struct
from project import ROOT,sha256,read_json
from wave20261104_main_tail_bindings import verify_original as branch_verify
from wave20261104_main_command_forward_bindings import validate as original_data_validate

INPUT=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/fourth/data-inputs.json'
INPUT_SHA='c2763dd65c10b01d13186ff8b5b2faac2919dd58b66965ce888b7df1ba45b5c0'


def frozen_inputs():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Exact second data contract changed')
    value=read_json(INPUT)
    for key in ['image','inventory','relocations']:
        if sha256(ROOT/value[key]['path'])!=value[key]['sha256']:raise ValueError('Original data proof input changed')
    return value


def validate(case,row,relocation,binding,image,inventory,loads):
    proof=original_data_validate(case,row,relocation,binding,image,inventory,loads)
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
