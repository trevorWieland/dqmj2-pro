import re
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from goal_resume_resource_path_views import SOURCE,LANE,WORK,include
from goal_resume_resource_path_compile import compile_source,linker
from goal_resume_resource_path_contracts import dependencies

OLD_SOURCE=ROOT/'src/runtime/goal_resume20261107/resource_selection'
OLD_LANE=ROOT/'evidence/lanes/parallel-wave20261107/resource-selection-source1'
FUTURE_SOURCE=SOURCE/'future_resource_selection'
FUTURE_LANE=LANE/'future-resource-selection'
FUTURE_WORK=WORK/'future700'


def create():
    ready=LANE/'ready.json'
    if sha256(ready)!='9314ac7c0a84322f3863a1ebb132398a41fddf4b59900818e3902de1c45ae614':raise ValueError('Qualified canonical API dependency changed')
    if sha256(OLD_LANE/'claim.json')!='8cfabd4f47bb6ef3457da5a467c959444319ad89b0d73d4b8a79de15b4d9ded1'or sha256(OLD_LANE/'working.json')!='a572c801026d8e66e8429bc0b38e93c20a3aece9e3a0da71f7da8128d257cb89':raise ValueError('Frozen original700 claim/proof changed')
    if FUTURE_SOURCE.exists()or FUTURE_WORK.exists()or FUTURE_LANE.exists():raise ValueError('New additive future roots must be unused')
    FUTURE_SOURCE.mkdir(parents=True);FUTURE_LANE.mkdir(parents=True)
    header=(OLD_SOURCE/'resource_selection.h').read_text()
    for line in['extern u32 native_fn_0202a8e0(u32);\n','extern u32 native_fn_0203cc3c(u32,u32);\n']:
        if header.count(line)!=1:raise ValueError('Original top API declaration differs')
        header=header.replace(line,'')
    path=FUTURE_SOURCE/'resource_selection.h';path.write_text(include(path,SOURCE/'resource_path_api.h')+'\n'+header)
    changes=[]
    for address in[0x02061088,0x02061470]:
        old=OLD_SOURCE/f'{address:08x}.c';new=FUTURE_SOURCE/old.name;text=old.read_text();typed=text
        for name in['native_fn_0202a8e0','native_fn_0203cc3c']:
            typed=typed.replace(name+'((u32)path',name+'(path')
        restored=typed
        for name in['native_fn_0202a8e0','native_fn_0203cc3c']:restored=restored.replace(name+'(path',name+'((u32)path')
        if restored!=text:raise ValueError('Type-only path conversion changed original statement/control flow')
        new.write_text(typed);changes.append(dict(address=hex(address),previous=old.relative_to(ROOT).as_posix(),previousSha256=sha256(old),view=new.relative_to(ROOT).as_posix(),viewSha256=sha256(new),reverseTransformEqualsOriginalExactly=True))
    write_json(FUTURE_LANE/'claim.json',dict(status='authorized-single-canonical-API-compile',sourceCredit=0,originalBytes=700,canonicalDependency=dict(path=ready.relative_to(ROOT).as_posix(),sha256=sha256(ready)),originalClaim=dict(path=(OLD_LANE/'claim.json').relative_to(ROOT).as_posix(),sha256=sha256(OLD_LANE/'claim.json')),preservedWorkingProof=dict(path=(OLD_LANE/'working.json').relative_to(ROOT).as_posix(),sha256=sha256(OLD_LANE/'working.json')),changes=changes,rule='Only the two approved top-level API declarations and their obsolete integer casts on genuine path buffers change. Every original statement/control-flow structure and other boundary is preserved. One unchanged recipe per new source, no alternatives or searches. Shared adoption remains coordinator-owned.'))


def compile_once():
    results=[]
    originals=read_json(OLD_LANE/'working-report.json')['functions']
    for old in originals:
        address=int(old['address'],0);source=FUTURE_SOURCE/f'{address:08x}.c';folder=FUTURE_WORK/f'{address:08x}'
        ref=dict(old,compilerPath='tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe')
        row=compile_source(source,folder/'compile',ref);row.update(sourceDependencies=dependencies(source),sourceLanguage='C',sourceCredit=0)
        if row['compilerFlags']!=old['compilerFlags']or row['compilerSha256']!=old['compilerSha256']:raise ValueError('Original700 compiler recipe changed')
        bindings={r['symbol']:dict(program='',processor='arm9',module='main',mode='data'if r['type']==2 else'arm',kind='data'if r['type']==2 else'function',address=r['target'])for r in row['relocations']}
        try:real=linker.validate(row,bindings,folder/'link')
        except ValueError as error:
            if not error.args or not isinstance(error.args[0],dict):raise
            real=dict(exactCallerBytes=False,comparison=error.args[0])
        if linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(folder/'link/caller.o',row['name']):raise ValueError('Genuine source split changed raw relocations')
        row.update(realLink=real,nativeSymbolEntries=bindings,ordinaryCBytes=0,justifiedAssemblyBytes=0)
        results.append(row);write_json(FUTURE_LANE/f'{address:08x}-first-comparison.json',dict(view=row,previousCompiledBytes=old['compiledBytes'],sourceCredit=0,matchingWholeFunction=real['exactCallerBytes']and row['exactAfterDeclaredRelocation']))
        print(dict(address=row['address'],nativeBytes=row['bytes'],compiledBytes=row['compiledBytes'],matchingBytes=row['matchingBytes'],genuineNativeWholeMatch=real['exactCallerBytes']),flush=True)
    write_json(FUTURE_LANE/'first-compile.json',dict(status='single-approved-canonical-API-compile-complete',sourceCredit=0,functions=results,originalBytes=700,compiledBytes=sum(r['compiledBytes']for r in results),noSourceVariants=True))


def main():
    create();compile_once()


if __name__=='__main__':main()
