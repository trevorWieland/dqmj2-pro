import copy
import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from wave20261104_main_tail_bindings import verify_original as branch_verify,native_relocations
from link_runtime_unit import verify_binding
from wave20261105_main_control_next_more_compiler import INPUT as IMPORTS,INPUT_SHA as IMPORTS_SHA

POINTERS=ROOT/'evidence/lanes/parallel-wave20261105/main-control-next/more/pointer-inputs.json'
POINTERS_SHA='364182f5e931f319f5738aa99f0aa6c3f1bde42f36e202c19e2696c24b1dd727'
HELPERS=()


def frozen_inputs():
    if sha256(POINTERS)!=POINTERS_SHA or sha256(IMPORTS)!=IMPORTS_SHA:raise ValueError('Immutable SDK pointer/helper contracts changed')
    value=read_json(POINTERS)
    for key in ['image','inventory','relocations']:
        pin=value[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable SDK native/reference pointer input changed')
    return value,read_json(IMPORTS)


def helper(entry,relocation,binding,imports,inventory):
    name=relocation['symbol']
    if name not in HELPERS or name not in imports['mapping']:raise ValueError('Unknown SDK compiler helper symbol')
    expected=imports['mapping'][name];origin=int(entry['address'],0)+relocation['offset'];original=native_relocations().get(origin)
    if (entry.get('program') or '',entry['processor'],entry['module'],entry['mode'])!=('','arm9','main','arm'):raise ValueError('SDK helper caller namespace differs')
    if (binding.get('program') or '',binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['address'])!=('','arm9','main','arm','function',expected['address']):raise ValueError('Exact measured SDK helper binding differs')
    if relocation['type'] not in (1,28,29) or relocation['addend']!=-8 or relocation['target']!=expected['address'] or not original or original['module']!='main' or int(original['address'],0)!=int(expected['address'],0):raise ValueError('Original SDK helper branch origin/target/relocation differs')
    if expected['canonicalInventoryRecord'] not in inventory.splitlines() or 'kind:function(arm,' not in expected['canonicalInventoryRecord']:raise ValueError('Canonical same-program ARM SDK helper entry missing')
    if entry.get('compilerSha256')!='89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca' or '-O4,p' not in entry['compilerFlags']:raise ValueError('SDK compiler helper emitted under different measured compiler/profile')
    verify_binding(name,binding)
    return dict(symbol=name,origin=hex(origin),target=expected['address'],module='main',mode='arm',originalRecord=original['record'],canonicalInventoryRecord=expected['canonicalInventoryRecord'],sourceAndCalleeCredit=0)


def validate(case,row,relocation,binding,image,inventory,loads,tables):
    if (row.get('program') or '',row['processor'],row['module'],row['mode'])!=('','arm9','main','arm') or (case['program'],case['processor'],case['module'],case['callerMode'])!=('','arm9','main','arm'):raise ValueError('SDK pointer caller namespace differs')
    if (row['address'],row['bytes'],row['targetSha256'])!=(case['caller'],case['bytes'],case['callerSha256']):raise ValueError('Complete original SDK caller contract differs')
    expected=('', 'arm9','main',case['bindingMode'],case['bindingKind'],case['symbolAddress'])
    if (binding.get('program') or '',binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['address'])!=expected:raise ValueError('SDK pointer binding CPU/program/module/kind/mode/address differs')
    if (relocation['symbol'],relocation['offset'],relocation['type'],relocation['addend'],relocation['target'])!=(case['symbol'],case['offset'],2,case['addend'],case['symbolAddress']):raise ValueError('Unchanged original ABS32/addend differs')
    base=int(case['symbolAddress'],0);target=int(case['nativeTarget'],0);origin=int(row['address'],0)+relocation['offset']
    if target!=base+case['addend'] or origin!=int(case['literalPool'],0):raise ValueError('Original SDK literal origin/addend target differs')
    if case['originalLoadRecord'] not in loads.splitlines() or not re.fullmatch(r'from:0x%08x kind:load to:0x%08x module:main'%(origin,target),case['originalLoadRecord']):raise ValueError('Exact original SDK pointer kind:load record absent')
    record=case['originalInventoryRecord']
    pattern=r'\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x%08x'%base if case['bindingKind']=='function' else r'\S+ kind:(?:bss|data(?:\(any\))?) addr:0x%08x'%base
    if record not in inventory.splitlines() or not re.fullmatch(pattern,record):raise ValueError('Exact original pointer function/data inventory kind absent')
    start=int(row['address'],0)-0x2000000;native=image[start:start+row['bytes']];literal=image[origin-0x2000000:origin-0x2000000+4]
    if len(native)!=row['bytes'] or hashlib.sha256(native).hexdigest()!=case['callerSha256'] or literal.hex()!=case['literalWordHex'] or struct.unpack('<I',literal)[0]!=target:raise ValueError('Original complete SDK caller/literal word changed')
    view=case['typedView']
    if case['bindingKind']=='function':
        if case['bindingMode']!='arm' or case['addend'] or target&1:raise ValueError('Measured ARM callback pointer changed mode/tag/addend')
    else:
        views={35415848: {'type': 'Selection-minimum-view', 'member': 'id-slot-pad', 'offsets': [0, 2, 3], 'widths': [2, 1, 1], 'minimumBytes': 4, 'alignment': 2}}
        if base not in views or view!=views[base] or case['addend']!=0 or 'kind:bss' not in record:raise ValueError('Exact original selection BSS minimum view differs')

    verify_binding(relocation['symbol'],binding)
    return dict(symbol=case['symbol'],origin=hex(origin),base=case['symbolAddress'],target=case['nativeTarget'],kind=case['bindingKind'],mode=case['bindingMode'],originalLoadRecord=case['originalLoadRecord'],originalInventoryRecord=record,originalAbs32Type=2,originalAddend=case['addend'],typedView=view,originalStorageExtentAuthorshipCredit=0)


def verify_original(row,bindings):
    pointers,imports=frozen_inputs();image=(ROOT/pointers['image']['path']).read_bytes();inventory=(ROOT/pointers['inventory']['path']).read_text();loads=(ROOT/pointers['relocations']['path']).read_text();regular=[r for r in row['relocations'] if r['type']!=2 and r['symbol'] not in HELPERS];result=branch_verify(dict(row,relocations=regular),bindings)
    helpers=[helper(row,r,bindings[r['symbol']],imports,inventory) for r in row['relocations'] if r['symbol'] in HELPERS];witnesses=[]
    for relocation in row['relocations']:
        if relocation['type']!=2:continue
        case=next((c for c in pointers['cases'] if c['caller']==row['address'] and c['symbol']==relocation['symbol'] and c['offset']==relocation['offset']),None)
        if case is None:raise ValueError('No private original SDK pointer contract')
        witnesses.append(validate(case,row,relocation,bindings[relocation['symbol']],image,inventory,loads,pointers['externalArrays']))
    return dict(result,qualifiedCompilerHelpers=helpers,originalPointerWitnesses=witnesses,originalStorageExtentAuthorshipCredit=0)


def negative_controls(rows):
    value,imports=frozen_inputs();image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();results=[]
    for case in value['cases']:
        row=next(r for r in rows if r['address']==case['caller']);rel=next(r for r in row['relocations'] if r['offset']==case['offset']);binding=row['nativeSymbolEntries'][rel['symbol']]
        changes=[('origin','rel','offset',rel['offset']+4),('address','binding','address',hex(int(binding['address'],0)+4)),('plus8-addend','rel','addend',rel['addend']+8),('kind','binding','kind','data' if case['bindingKind']=='function' else 'function'),('mode','binding','mode','thumb' if case['bindingKind']=='function' else 'arm'),('CPU','binding','processor','arm7'),('program','binding','program','dwc/utility.bin/move/child.srl'),('module','binding','module','ov000'),('view-width','case','typedView',dict(case['typedView'],widths=[4,1,1]))]
        for label,owner,key,wrong in changes:
            objects={k:copy.deepcopy(v) for k,v in [('case',case),('row',row),('rel',rel),('binding',binding)]};objects[owner][key]=wrong
            try:validate(objects['case'],objects['row'],objects['rel'],objects['binding'],image,inventory,loads,value['externalArrays'])
            except ValueError as error:results.append(dict(caller=case['caller'],origin=case['literalPool'],case=label,rejected=True,reason=str(error)))
            else:
                if case['bindingKind']=='function' and label=='view-width':continue
                raise ValueError('Invalid SDK pointer accepted:'+label)
        changed=bytearray(image);changed[int(case['literalPool'],0)-0x2000000]^=4
        for label,raw,inv,recs in [('native-literal',bytes(changed),inventory,loads),('inventory',image,inventory.replace(case['originalInventoryRecord'],''),loads),('load-record',image,inventory,loads.replace(case['originalLoadRecord'],''))]:
            try:validate(case,row,rel,binding,raw,inv,recs,value['externalArrays'])
            except ValueError as error:results.append(dict(caller=case['caller'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Changed SDK pointer evidence accepted:'+label)
    return dict(status='passed',negativeCases=results,ordinaryBranchVerifierUnchanged=True,originalStorageExtentAuthorshipCredit=0)
