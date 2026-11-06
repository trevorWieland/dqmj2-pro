import copy
import hashlib
import re
import struct
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_MEM,ARM_SFT_LSL
from project import ROOT,read_json,sha256
from wave20261104_main_tail_bindings import verify_original as branch_verify
from link_runtime_unit import verify_binding

INPUT=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/next/data-inputs.json'
INPUT_SHA='e4c7f77f49463936dbf4e706959745249389e73f419940de4ba9d396bcebc137'
MD=Cs(CS_ARCH_ARM,CS_MODE_ARM);MD.detail=True
MEMBERS={'Allocator12':{'base':(0,4),'limit':(4,4),'used':(8,4)},'GlobalSlot10':{'key':(0,4)},'ModeState':{'field4':(4,4)}}


def frozen_inputs():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Immutable original data contract changed')
    value=read_json(INPUT)
    for key in ['image','inventory','relocations']:
        pin=value[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable original data input changed')
    return value


def validate(case,row,relocation,binding,image,inventory,loads):
    ns=('', 'arm9','main','arm')
    if (row.get('program') or '',row.get('processor'),row['module'],row['mode'])!=ns or (case['program'],case['processor'],case['module'],case['mode'])!=ns:raise ValueError('Original data caller namespace differs')
    if (row['address'],row['bytes'],row['targetSha256'])!=(case['caller'],case['bytes'],case['callerSha256']):raise ValueError('Original complete caller contract differs')
    if (binding.get('program') or '',binding.get('processor'),binding['module'],binding['mode'],binding['kind'])!=('','arm9','main','data','data'):raise ValueError('Original data binding CPU/program/module/kind/mode differs')
    if (relocation['symbol'],relocation['offset'],relocation['type'],relocation['addend'])!=(case['symbol'],case['offset'],2,0):raise ValueError('Original unchanged ABS32 zero-addend differs')
    origin=int(row['address'],0)+relocation['offset'];base=int(case['symbolAddress'],0)
    if int(relocation['target'],0)!=base or int(binding['address'],0)!=base or int(case['nativeTarget'],0)!=base or origin!=int(case['literalPool'],0):raise ValueError('Original symbol/address/origin differs')
    if case['originalLoadRecord'] not in loads.splitlines() or not re.fullmatch(r'from:0x%08x kind:load to:0x%08x module:main'%(origin,base),case['originalLoadRecord']):raise ValueError('Exact original kind:load record missing')
    if case['originalInventoryRecord'] not in inventory.splitlines() or not re.fullmatch(r'\S+ kind:(?:bss|data) addr:0x%08x'%base,case['originalInventoryRecord']):raise ValueError('Original exact data/nonfunction point missing')
    start=int(row['address'],0)-0x2000000;native=image[start:start+row['bytes']]
    if len(native)!=row['bytes'] or hashlib.sha256(native).hexdigest()!=case['callerSha256']:raise ValueError('Original complete caller changed')
    literal=image[origin-0x2000000:origin-0x2000000+4]
    if literal.hex()!=case['literalWordHex'] or struct.unpack('<I',literal)[0]!=base:raise ValueError('Original literal word differs')
    if not case['typedAccesses'] and not (case['opaqueAddressOnly'] and case['caller']=='0x203a7cc'):raise ValueError('Unqualified opaque-only address use')
    for access in case['typedAccesses']:
        at=int(access['instruction'],0);body=image[at-0x2000000:at-0x2000000+4]
        if not int(row['address'],0)<=at<at+4<=int(row['address'],0)+row['bytes'] or body.hex()!=access['instructionBytesHex']:raise ValueError('Typed access outside original caller or changed')
        ins=list(MD.disasm(body,at))
        if len(ins)!=1 or ins[0].mnemonic!=access['mnemonic'] or access['mnemonic'] not in ('ldr','ldrlo','str','strlo','strne'):raise ValueError('Original typed word operation differs')
        if (access['offset'],access['width'])!=MEMBERS.get(access['type'],{}).get(access['member']):raise ValueError('Actual compiler-witnessed field offset/width differs')
        op=next((op for op in ins[0].operands if op.type==ARM_OP_MEM),None)
        if op is None or op.mem.disp!=access['offset'] or access['width']!=4:raise ValueError('Measured native field displacement/width differs')
        stride=case['indexedElementStride']
        if stride is not None and (stride!=16 or op.shift.type!=ARM_SFT_LSL or op.shift.value!=4):raise ValueError('Measured original indexed element stride differs')
    verify_binding(relocation['symbol'],binding)
    return dict(symbol=case['symbol'],origin=hex(origin),target=case['symbolAddress'],originalLoadRecord=case['originalLoadRecord'],originalInventoryRecord=case['originalInventoryRecord'],originalAbs32Type=2,originalAddend=0,typedAccesses=case['typedAccesses'],opaqueAddressOnly=case['opaqueAddressOnly'],originalStorageExtentAuthorshipCredit=0)


def verify_original(row,bindings):
    result=branch_verify(dict(row,relocations=[r for r in row['relocations'] if r['type']!=2]),bindings);data=[r for r in row['relocations'] if r['type']==2]
    if not data:return result
    value=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();witnesses=[]
    for relocation in data:
        case=next((c for c in value['cases'] if c['caller']==row['address'] and c['symbol']==relocation['symbol']),None)
        if case is None:raise ValueError('No private original caller/data qualification')
        witnesses.append(validate(case,row,relocation,bindings[relocation['symbol']],image,inventory,loads))
    return dict(result,originalDataLoadWitnesses=witnesses,dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=INPUT_SHA),originalStorageExtentAuthorshipCredit=0)


def negative_controls(rows):
    value=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();results=[]
    for case in value['cases']:
        row=next(r for r in rows if r['address']==case['caller']);relocation=next(r for r in row['relocations'] if r['symbol']==case['symbol']);binding=row['nativeSymbolEntries'][case['symbol']]
        changes=[('origin','relocation','offset',case['offset']+4),('address','binding','address',hex(int(case['symbolAddress'],0)+4)),('plus8-addend','relocation','addend',8),('kind','binding','kind','function'),('mode','binding','mode','arm'),('CPU','binding','processor','arm7'),('program','binding','program','dwc/utility.bin/move/child.srl'),('module','binding','module','ov000')]
        if case['typedAccesses']:changes.extend([('typed-offset','case','typedAccesses',[dict(case['typedAccesses'][0],offset=case['typedAccesses'][0]['offset']+1)]),('typed-width','case','typedAccesses',[dict(case['typedAccesses'][0],width=2)])])
        tests=[]
        for label,owner,key,wrong in changes:
            versions={name:copy.deepcopy(obj) for name,obj in [('case',case),('row',row),('relocation',relocation),('binding',binding)]};versions[owner][key]=wrong;tests.append((label,versions['case'],versions['row'],versions['relocation'],versions['binding'],image,inventory,loads))
        changed=bytearray(image);changed[int(case['literalPool'],0)-0x2000000]^=4
        tests.extend([(label,case,row,relocation,binding,raw,inv,records) for label,raw,inv,records in [('native-literal',bytes(changed),inventory,loads),('inventory',image,inventory.replace(case['originalInventoryRecord'],''),loads),('load-record',image,inventory,loads.replace(case['originalLoadRecord'],''))]])
        for label,c,r,rel,b,raw,inv,records in tests:
            try:validate(c,r,rel,b,raw,inv,records)
            except ValueError as error:results.append(dict(caller=case['caller'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Invalid original data qualification accepted: '+label)
    return dict(status='passed',negativeCases=results,branchVerifierUnchanged=True,originalStorageExtentAuthorshipCredit=0)
