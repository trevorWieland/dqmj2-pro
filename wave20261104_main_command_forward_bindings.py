import copy
import re
import struct
from project import ROOT,read_json,sha256
from wave20261104_main_tail_bindings import verify_original as branch_verify,native_relocations
from link_runtime_unit import verify_binding

INPUT=ROOT/'evidence/lanes/parallel-wave20261104/main-command-forward/data-inputs.json'
INPUT_SHA='fe7e9f56114fde7539d5470afd6216d9c183e348a0599aa7b84735d38777581a'


def frozen_inputs():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Immutable original data-load contract changed')
    value=read_json(INPUT)
    for key in ['inventory','relocations','image']:
        pin=value[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable native data inventory/image changed')
    return value


def validate(case,row,relocation,binding,image,inventory,loads):
    expected=('', 'arm9','main','arm')
    if (row.get('program') or '',row.get('processor'),row['module'],row['mode'])!=expected:raise ValueError('Data caller CPU/program/module/mode differs')
    if (case['program'],case['processor'],case['module'],case['mode'])!=expected:raise ValueError('Frozen data caller namespace differs')
    if (row['address'],row['bytes'],row['targetSha256'])!=(case['caller'],case['bytes'],case['callerSha256']):raise ValueError('Data load is outside its exact original caller contract')
    if (binding.get('program') or '',binding.get('processor'),binding['module'],binding['mode'],binding['kind'])!=('','arm9','main','data','data'):raise ValueError('Original data binding changed namespace/kind/mode')
    if (relocation['symbol'],relocation['offset'],relocation['type'],relocation['addend'])!=(case['symbol'],case['offset'],2,0):raise ValueError('Original ABS32 relocation or zero addend differs')
    target=int(case['target'],0);origin=int(row['address'],0)+relocation['offset']
    if int(relocation['target'],0)!=target or int(binding['address'],0)!=target or origin!=int(case['literalPool'],0):raise ValueError('Original literal origin or data address differs')
    if case['originalLoadRecord'] not in loads.splitlines() or not re.fullmatch(r'from:0x%08x kind:load to:0x%08x module:main'%(origin,target),case['originalLoadRecord']):raise ValueError('Exact original kind:load namespace record missing')
    if case['originalInventoryRecord'] not in inventory.splitlines() or not re.fullmatch(r'\S+ kind:(?:bss|data) addr:0x%08x'%target,case['originalInventoryRecord']):raise ValueError('Target lacks exact original non-function storage entry')
    start=int(row['address'],0)-0x02000000;native=image[start:start+row['bytes']]
    if len(native)!=row['bytes'] or __import__('hashlib').sha256(native).hexdigest()!=case['callerSha256']:raise ValueError('Complete original caller changed')
    literal=image[origin-0x02000000:origin-0x02000000+4]
    if literal.hex()!=case['literalWordHex'] or struct.unpack('<I',literal)[0]!=target:raise ValueError('Original literal word differs')
    for access in case['typedAccesses']:
        at=int(access['instruction'],0);body=image[at-0x02000000:at-0x02000000+4];word=struct.unpack('<I',body)[0]
        if body.hex()!=access['instructionBytesHex'] or access['operation']!='unsigned-byte-read' or access['width']!=1 or word&0xfffff000!=0xe5d00000 or word&0xfff!=access['offset']:raise ValueError('Measured original field offset/width/instruction differs')
    verify_binding(relocation['symbol'],binding)
    return dict(symbol=case['symbol'],origin=hex(origin),target=case['target'],module='main',mode='data',originalLoadRecord=case['originalLoadRecord'],originalInventoryRecord=case['originalInventoryRecord'],originalAbs32Type=2,originalAddend=0,typedAccesses=case['typedAccesses'],originalDataStorageCredit=0,originalObjectExtentOrAuthorshipCredit=0)


def verify_original(row,bindings):
    data=[r for r in row['relocations'] if r['type']==2]
    branch_row=dict(row,relocations=[r for r in row['relocations'] if r['type']!=2])
    result=branch_verify(branch_row,bindings)
    if not data:return result
    value=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();witnesses=[]
    for relocation in data:
        case=next((c for c in value['cases'] if c['caller']==row['address'] and c['symbol']==relocation['symbol']),None)
        if case is None:raise ValueError('No private original data-load qualification for caller/symbol')
        witnesses.append(validate(case,row,relocation,bindings[relocation['symbol']],image,inventory,loads))
    return dict(result,originalDataLoadWitnesses=witnesses,dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=INPUT_SHA),externalStorageCredit=0)


def negative_controls(rows):
    value=frozen_inputs();case=value['cases'][0];row=next(r for r in rows if r['address']==case['caller']);relocation=next(r for r in row['relocations'] if r['symbol']==case['symbol']);binding=row['nativeSymbolEntries'][case['symbol']]
    image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();results=[]
    changes=[('wrong-origin','relocation','offset',8),('wrong-address','binding','address',hex(int(case['target'],0)+4)),('nonzero-plus-eight-addend','relocation','addend',8),('function-kind','binding','kind','function'),('function-mode','binding','mode','arm'),('wrong-CPU','binding','processor','arm7'),('wrong-program','binding','program','dwc/utility.bin/move/child.srl'),('wrong-module','binding','module','ov000'),('wrong-offset','case','typedAccesses', [dict(case['typedAccesses'][0],offset=7)]),('wrong-width','case','typedAccesses',[dict(case['typedAccesses'][0],width=2)])]
    for label,owner,key,wrong in changes:
        versions={name:copy.deepcopy(obj) for name,obj in [('case',case),('row',row),('relocation',relocation),('binding',binding)]};versions[owner][key]=wrong
        try:validate(versions['case'],versions['row'],versions['relocation'],versions['binding'],image,inventory,loads)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid data-load binding accepted: '+label)
    changed=bytearray(image);changed[int(case['literalPool'],0)-0x02000000]^=4
    for label,raw,inv,records in [('changed-literal',bytes(changed),inventory,loads),('changed-inventory',image,inventory.replace(case['originalInventoryRecord'],''),loads),('changed-load-record',image,inventory,loads.replace(case['originalLoadRecord'],''))]:
        try:validate(case,row,relocation,binding,raw,inv,records)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Changed original data evidence accepted: '+label)
    return dict(status='passed',negativeCases=results,sourceOrDataStorageCredit=0,ordinaryBranchVerifierUnchanged=True)
