import copy
import hashlib
import re
import struct
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_IMM,ARM_OP_MEM,ARM_OP_REG,ARM_SFT_LSL
from project import ROOT,read_json,sha256
from wave20261104_main_tail_bindings import verify_original as branch_verify
from link_runtime_unit import verify_binding

INPUT=ROOT/'evidence/lanes/parallel-wave20261104/main-command-forward/next/data-inputs.json'
INPUT_SHA='75bce5b821dcdeffa0f83ee66a59fe4c95195e369ec1d3afab72b354cfd09635'
MD=Cs(CS_ARCH_ARM,CS_MODE_ARM);MD.detail=True
MEMBERS={'Record11c':{'field0':(0,1),'field84':(0x84,12),'field90.words[0]':(0x90,4),'field90.words[1]':(0x94,4),'field90.words[2]':(0x98,4)},'Record8':{'field4':(4,2)}}


def frozen_inputs():
    if sha256(INPUT)!=INPUT_SHA:raise ValueError('Immutable original data contract changed')
    value=read_json(INPUT)
    for key in ['inventory','relocations','image']:
        pin=value[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable data inventory/image changed')
    return value


def instruction(image,proof):
    at=int(proof.get('instruction',proof.get('address')),0);body=image[at-0x2000000:at-0x2000000+4]
    if body.hex()!=proof.get('instructionBytesHex',proof.get('bytesHex')):raise ValueError('Original typed instruction changed')
    ins=list(MD.disasm(body,at))
    if len(ins)!=1 or ins[0].size!=4:raise ValueError('Typed instruction is not one measured ARM word')
    return ins[0]


def validate(case,row,relocation,binding,image,inventory,loads):
    ns=('', 'arm9','main','arm')
    if (row.get('program') or '',row.get('processor'),row['module'],row['mode'])!=ns or (case['program'],case['processor'],case['module'],case['mode'])!=ns:raise ValueError('Original data caller namespace differs')
    if (row['address'],row['bytes'],row['targetSha256'])!=(case['caller'],case['bytes'],case['callerSha256']):raise ValueError('Original complete caller contract differs')
    if (binding.get('program') or '',binding.get('processor'),binding['module'],binding['mode'],binding['kind'])!=('','arm9','main','data','data'):raise ValueError('Original data binding CPU/program/module/kind/mode differs')
    if (relocation['symbol'],relocation['offset'],relocation['type'],relocation['addend'])!=(case['symbol'],case['offset'],2,case['addend']):raise ValueError('Original ABS32 relocation/addend differs')
    origin=int(row['address'],0)+relocation['offset'];base=int(case['symbolAddress'],0);target=int(case['nativeTarget'],0)
    if int(relocation['target'],0)!=base or int(binding['address'],0)!=base or base+relocation['addend']!=target or origin!=int(case['literalPool'],0):raise ValueError('Original symbol/address/origin/addend differs')
    record=case['originalLoadRecord']
    if record not in loads.splitlines() or not re.fullmatch(r'from:0x%08x kind:load to:0x%08x module:main'%(origin,target),record):raise ValueError('Exact original kind:load record missing')
    for key,address in [('originalSymbolInventoryRecord',base),('originalTargetInventoryRecord',target)]:
        record=case[key]
        if record not in inventory.splitlines() or not re.fullmatch(r'\S+ kind:(?:bss|data) addr:0x%08x'%address,record):raise ValueError('Original data/nonfunction inventory point missing')
    native=image[int(row['address'],0)-0x2000000:int(row['address'],0)-0x2000000+row['bytes']]
    if len(native)!=row['bytes'] or hashlib.sha256(native).hexdigest()!=case['callerSha256']:raise ValueError('Original complete native body changed')
    literal=image[origin-0x2000000:origin-0x2000000+4]
    if literal.hex()!=case['literalWordHex'] or struct.unpack('<I',literal)[0]!=target:raise ValueError('Original literal/addend target differs')
    proofs=[case['strideInstruction'],*case['typedAccesses'],*[a['addressInstruction'] for a in case['typedAccesses'] if 'addressInstruction' in a]]
    for proof in proofs:
        at=int(proof.get('instruction',proof.get('address')),0)
        if not int(row['address'],0)<=at<at+4<=int(row['address'],0)+row['bytes']:raise ValueError('Typed instruction outside complete original caller')
    stride=instruction(image,case['strideInstruction'])
    operand=stride.operands[-1]
    actual_stride=operand.imm if stride.mnemonic=='mov' and operand.type==ARM_OP_IMM else 1<<operand.shift.value if stride.mnemonic=='lsl' and operand.type==ARM_OP_REG and operand.shift.type==ARM_SFT_LSL else None
    if actual_stride!=case['elementStride']:raise ValueError('Measured element stride differs')
    for access in case['typedAccesses']:
        ins=instruction(image,access)
        if (access['offset'],access['width'])!=MEMBERS.get(access['type'],{}).get(access['member']):raise ValueError('Compiler-witnessed typed field offset/width differs')
        if access['type']!=('Record8' if case['elementStride']==8 else 'Record11c'):raise ValueError('Typed record/stride differs')
        if ins.mnemonic!=access['mnemonic']:raise ValueError('Typed native operation differs')
        if ins.mnemonic=='ldmne':
            add=instruction(image,access['addressInstruction'])
            if access['width']!=4*(len(ins.operands)-1) or add.mnemonic!='add' or add.operands[-1].type!=ARM_OP_IMM or add.operands[-1].imm+case['addend']!=access['offset']:raise ValueError('Measured aggregate field address/width differs')
        else:
            mem=next((op.mem for op in ins.operands if op.type==ARM_OP_MEM),None)
            if mem is None or access['width']!={'ldrb':1,'ldrsh':2,'str':4}.get(ins.mnemonic) or mem.disp+case['addend']!=access['offset']:raise ValueError('Measured scalar field offset/width differs')
    verify_binding(relocation['symbol'],binding)
    return dict(symbol=case['symbol'],origin=hex(origin),symbolAddress=case['symbolAddress'],nativeTarget=case['nativeTarget'],originalAbs32Type=2,originalAddend=case['addend'],originalLoadRecord=case['originalLoadRecord'],typedAccesses=case['typedAccesses'],elementStride=case['elementStride'],externalStorageExtentAuthorshipCredit=0)


def verify_original(row,bindings):
    result=branch_verify(dict(row,relocations=[r for r in row['relocations'] if r['type']!=2]),bindings)
    data=[r for r in row['relocations'] if r['type']==2]
    if not data:return result
    value=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();witnesses=[]
    for relocation in data:
        case=next((c for c in value['cases'] if c['caller']==row['address'] and c['symbol']==relocation['symbol']),None)
        if case is None:raise ValueError('No immutable private data contract for caller/symbol')
        witnesses.append(validate(case,row,relocation,bindings[relocation['symbol']],image,inventory,loads))
    return dict(result,originalDataLoadWitnesses=witnesses,dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=INPUT_SHA),externalStorageExtentAuthorshipCredit=0)


def negative_controls(rows):
    value=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();results=[]
    for case in value['cases']:
        row=next(r for r in rows if r['address']==case['caller']);relocation=next(r for r in row['relocations'] if r['symbol']==case['symbol']);binding=row['nativeSymbolEntries'][case['symbol']]
        changes=[('origin','relocation','offset',case['offset']+4),('address','binding','address',hex(int(case['symbolAddress'],0)+4)),('plus8-addend','relocation','addend',case['addend']+8),('function-kind','binding','kind','function'),('function-mode','binding','mode','arm'),('CPU','binding','processor','arm7'),('program','binding','program','dwc/utility.bin/move/child.srl'),('module','binding','module','ov000'),('typed-offset','case','typedAccesses',[dict(case['typedAccesses'][0],offset=case['typedAccesses'][0]['offset']+1)]),('typed-width','case','typedAccesses',[dict(case['typedAccesses'][0],width=case['typedAccesses'][0]['width']+1)]),('record-stride','case','elementStride',case['elementStride']+4)]
        tests=[]
        for label,owner,key,wrong in changes:
            versions={name:copy.deepcopy(obj) for name,obj in [('case',case),('row',row),('relocation',relocation),('binding',binding)]};versions[owner][key]=wrong
            tests.append((label,versions['case'],versions['row'],versions['relocation'],versions['binding'],image,inventory,loads))
        changed=bytearray(image);changed[int(case['literalPool'],0)-0x2000000]^=4
        tests.extend([(label,case,row,relocation,binding,raw,inv,records) for label,raw,inv,records in [('literal',bytes(changed),inventory,loads),('symbol-inventory',image,inventory.replace(case['originalSymbolInventoryRecord'],''),loads),('load-record',image,inventory,loads.replace(case['originalLoadRecord'],''))]])
        for label,c,r,rel,b,raw,inv,records in tests:
            try:validate(c,r,rel,b,raw,inv,records)
            except ValueError as error:results.append(dict(caller=case['caller'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Invalid data qualification accepted: '+label)
    return dict(status='passed',negativeCases=results,ordinaryBranchVerifierUnchanged=True,externalStorageExtentAuthorshipCredit=0)
