import hashlib
import json
import os
import re
import struct
import sys
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,configuration
from goal_resume_resource_path_compile import normalized,object_contract,compile_source,linker
from goal_resume_resource_path_callers import bindings

SOURCE=ROOT/'src/runtime/goal_resume20261107/material_mask_pivot'
LANE=ROOT/'evidence/lanes/parallel-wave20261107/material-mask-pivot-source1'
WORK=ROOT/'work/goal-resume-20261107/material-mask-pivot-source1'
AUDIT=ROOT/'evidence/lanes/parallel-wave20261107/material-mask-pivot-frontier-source1'


def common():
    return '''#ifndef DQM_MATERIAL_PIVOT_H
#define DQM_MATERIAL_PIVOT_H
typedef struct NativeMaterialPivot {
    const unsigned long masks[8];
    const unsigned char pivots[9][4];
} NativeMaterialPivot;
extern const NativeMaterialPivot native_data_main_020d9068;
typedef char MaterialSDKWordWidth[sizeof(unsigned long)==4?1:-1];
typedef char MaterialPivotBytes[sizeof(NativeMaterialPivot)==68?1:-1];
#endif
'''


def render():
    body=r'''#define MATERIAL_MASK(i) (((i)&1?0x7fffUL:0)|((i)&2?0x7fff0000UL:0)|((i)&4?0x8000UL:0))
#define REMAIN_FIRST(i) ((i)==0?1:0)
#define REMAIN_SECOND(i) ((i)==2?1:2)
#define MATRIX_INDEX(r,c) (3*(r)+(c))
#define PIVOT_ROW(p) { \
    MATRIX_INDEX(REMAIN_FIRST((p)/3),REMAIN_FIRST((p)%3)), \
    MATRIX_INDEX(REMAIN_FIRST((p)/3),REMAIN_SECOND((p)%3)), \
    MATRIX_INDEX(REMAIN_SECOND((p)/3),REMAIN_FIRST((p)%3)), \
    MATRIX_INDEX(REMAIN_SECOND((p)/3),REMAIN_SECOND((p)%3)) }
const NativeMaterialPivot native_data_main_020d9068 = {
    { MATERIAL_MASK(0), MATERIAL_MASK(1), MATERIAL_MASK(2), MATERIAL_MASK(3),
      MATERIAL_MASK(4), MATERIAL_MASK(5), MATERIAL_MASK(6), MATERIAL_MASK(7) },
    { PIVOT_ROW(0), PIVOT_ROW(1), PIVOT_ROW(2),
      PIVOT_ROW(3), PIVOT_ROW(4), PIVOT_ROW(5),
      PIVOT_ROW(6), PIVOT_ROW(7), PIVOT_ROW(8) }
};
'''
    payload=struct.pack('<8I',*((0x7fff if i&1 else 0)|(0x7fff0000 if i&2 else 0)|(0x8000 if i&4 else 0)for i in range(8)))+bytes(3*r+c for p in range(9)for r in range(3)if r!=p//3 for c in range(3)if c!=p%3)
    return common()+body,payload


def guarded_render():
    original=Path.open;blocked=[]
    def source_only(path,*args,**kwargs):
        if any(path.resolve().is_relative_to(ROOT/p)for p in['inputs','extract','deps/reference']):raise PermissionError('Target inputs are blocked during independent material/pivot generation')
        return original(path,*args,**kwargs)
    with patch.object(Path,'open',source_only):
        code,payload=render()
        for path in[ROOT/'extract/arm9/arm9.bin',configuration()['rom']]:
            try:path.read_bytes()
            except PermissionError:blocked.append(path.relative_to(ROOT).as_posix())
            else:raise ValueError('Independent generation guard failed')
    return code,payload,blocked


def create():
    if SOURCE.exists()or LANE.exists()or WORK.exists():raise ValueError('New material/pivot roots must be unused')
    if sha256(AUDIT/'audit.json')!='e5c8611199744b3494a4a928b5a7b8006c9da0ea219eb355e6c85ea7557dc082'or sha256(AUDIT/'seal.json')!='c2532cd81735b894af2bf62b1470f0f20975176204322f53703e05a87020b67e':raise ValueError('Reviewed68B scope changed')
    for pin in read_json(AUDIT/'seal.json')['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Focused audit input changed')
    ledger=[json.loads(line)for line in(ROOT/'ledger/functions.jsonl').read_text().splitlines()];references=[]
    for address in[0x0202fde0,0x0203048c]:
        selected=next(r for r in ledger if r['module']=='main'and r['processor']=='arm9'and int(r['address'],0)==address);report=read_json(ROOT/selected['evidence']);entry=next(r for r in report['matches']if int(r['address'],0)==address)
        if sha256(ROOT/entry['source'])!=entry['sourceSha256']or sha256(ROOT/entry['object'])!=entry['objectSha256']:raise ValueError('Accepted source/object changed')
        entry=dict(entry,program='',admittedIdentity=selected['id'],allocatedContract=normalized(object_contract(ROOT/entry['object'])),rawRelocations=linker.relocation_rows(ROOT/entry['object'],entry['name']))
        qualified=dict(entry,relocations=[dict(r,target=r.get('targetAddress',r['target']))for r in entry['relocations']]);entry['nativeSymbolEntries']=bindings(qualified);references.append(entry)
    code,payload,blocked=guarded_render();LANE.mkdir(parents=True)
    data=dict(program='',processor='arm9',module='main',mode='data',kind='data',section='.rodata',address='0x020d9068',bytes=68,targetSha256=hashlib.sha256(payload).hexdigest(),source=(SOURCE/'data.c').relative_to(ROOT).as_posix())
    write_json(LANE/'claim.json',dict(status='coordinator-admitted-material-pivot-bounded-view-and-two-migrations',sourceCredit=0,claimedStorage=[data],migrationFunctions=[{k:r.get(k)for k in('admittedIdentity','program','processor','module','mode','address','bytes','source','sourceSha256','object','objectSha256','compilerPath','compilerSha256','compilerFlags','sourceDependencies')}for r in references],zeroCreditMigrationFunctions=2,zeroCreditMigrationBytes=2280,newFunctionCredit=0,newInitializedDataCandidateBytes=68,validPivotDomain='0..8 only;9..15 remain unsupported and are never executed against C or given an invented runtime guard.',dataCompilerRecipe=dict(compiler='tools/mwccarm/mwccarm/2.0/base/mwccarm.exe',sha256='7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880',flags=['-O3','-opt','speed','-proc','arm946e','-sym','on','-nolink']),sourceRoot=SOURCE.relative_to(ROOT).as_posix(),workRoot=WORK.relative_to(ROOT).as_posix(),frozenAudit=dict(path=(AUDIT/'seal.json').relative_to(ROOT).as_posix(),sha256=sha256(AUDIT/'seal.json')),limits=['Bounded68B view only; no original enclosing-object size or declaration-alignment claim.','No source/header/object/producers or shared selection are changed.']))
    write_json(LANE/'reference-contracts.json',dict(entries=references));SOURCE.mkdir(parents=True);(SOURCE/'material_pivot.h').write_text(common());(SOURCE/'data.c').write_text(code);views=[]
    for ref in references:
        address=int(ref['address'],0);directory=SOURCE/'consumers'/f'{address:08x}';directory.mkdir(parents=True);old=ROOT/ref['source'];new=directory/old.name;original=old.read_text();text=original.replace('.field_0000[','.masks[').replace('.field_0020[','.pivots[')
        if text.replace('.masks[','.field_0000[').replace('.pivots[','.field_0020[')!=original:raise ValueError('Necessary typed field names alter statement/control flow')
        new.write_text(text);header=old.with_name('context_00.h');body=header.read_text();pattern=r'typedef struct \{\n[^{}]*\} NativeStorage_020d9068;\nextern[^;]*native_data_main_020d9068;\n';matches=list(re.finditer(pattern,body))
        if len(matches)!=1:raise ValueError('Original storage declaration is ambiguous')
        include='#include "'+os.path.relpath(SOURCE/'material_pivot.h',directory).replace('\\','/')+'"\n';new_header=directory/header.name;new_header.write_text(body[:matches[0].start()]+include+body[matches[0].end():])
        views.append(dict(address=ref['address'],previousSource=ref['source'],previousSourceSha256=ref['sourceSha256'],previousHeader=header.relative_to(ROOT).as_posix(),previousHeaderSha256=sha256(header),view=new.relative_to(ROOT).as_posix(),viewSha256=sha256(new),viewHeader=new_header.relative_to(ROOT).as_posix(),viewHeaderSha256=sha256(new_header),statementsReverseExactly=True))
    write_json(LANE/'views.json',dict(status='additive-canonical-typed-views-created',sourceCredit=0,views=views,blockedOriginalGenerationReads=blocked,commonHeader=dict(path=(SOURCE/'material_pivot.h').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'material_pivot.h'))))
    print(dict(claim=(LANE/'claim.json').relative_to(ROOT).as_posix(),dataBytes=68,migrations=2,migrationBytes=2280),flush=True)


def qualify_consumers():
    results=[]
    for ref in read_json(LANE/'reference-contracts.json')['entries']:
        address=int(ref['address'],0);source=SOURCE/'consumers'/f'{address:08x}'/Path(ref['source']).name;folder=WORK/'contracts'/f'{address:08x}';pair=[]
        for kind,path in[('previous',ROOT/ref['source']),('view',source)]:
            row=compile_source(path,folder/kind/'c',ref);actual=normalized(object_contract(ROOT/row['object']));raw=linker.relocation_rows(ROOT/row['object'],row['name'])
            proof=dict(row=row,allocatedEqual=actual==ref['allocatedContract'],rawRelocationsEqual=raw==ref['rawRelocations'])
            write_json(LANE/f'{address:08x}-{kind}-comparison.json',proof)
            if actual!=ref['allocatedContract']or raw!=ref['rawRelocations']or row['compiledBytes']!=ref['bytes']:raise ValueError(('Atomic material/pivot migration contract changed; stop without source/profile alternatives',hex(address),kind))
            proof['realLink']=linker.validate(row,ref['nativeSymbolEntries'],folder/kind/'l')
            row.update(genericMatcherDiagnostic=dict(exact=row['exactAfterDeclaredRelocation'],matchingBytes=row['matchingBytes'],outputSha256=row['outputSha256']),exactAfterDeclaredRelocation=True,manualRelocationComparison=True,exactAfterDeclaredRelocationBasis='Complete native caller extent, unchanged compiler object relocations/addends and genuine pinned MW linker equality',matchingBytesScope='Generic matcher diagnostic only; realLink proves the full original span')
            pair.append(proof)
        results.append(dict(address=ref['address'],previous=pair[0],view=pair[1]))
    write_json(LANE/'consumers-qualified.json',dict(status='both-old-new-whole-native-contracts-qualified',functions=2,bytes=2280,sourceCredit=0,results=results));print(dict(functions=2,bytes=2280,oldAndNewNativeLinks=4),flush=True)


if __name__=='__main__':
    if sys.argv[1:]==['--create']:create()
    elif sys.argv[1:]==['--qualify-consumers']:qualify_consumers()
    else:raise ValueError('Choose--create or--qualify-consumers')
