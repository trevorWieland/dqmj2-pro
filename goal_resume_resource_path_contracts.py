import copy
import hashlib
import json
import re
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from goal_resume_resource_path_views import SOURCE,LANE,WORK,mirror
from goal_resume_resource_path_compile import reference,compile_source,normalized,object_contract,linker
from goal_resume_resource_path_callers import inventory,bindings


def snapshot():
    destination=LANE/'reference-contracts.json'
    if destination.exists():raise ValueError('Frozen original contracts already exist')
    entries=[]
    for selected in inventory():
        old=reference(int(selected['address'],0));qualified=dict(old,relocations=[dict(r,target=r.get('targetAddress',r['target']))for r in old['relocations']])
        old.update(program='',allocatedContract=normalized(object_contract(ROOT/old['object'])),rawRelocations=linker.relocation_rows(ROOT/old['object'],old['name']),nativeSymbolEntries=bindings(qualified),sourceDependencies=selected.get('sourceDependencies')or[],admittedIdentity=selected['id'])
        entries.append(old)
    write_json(destination,dict(schemaVersion=1,status='frozen-actual-original-allocated-contracts',functions=27,bytes=4812,entries=entries,sourceCredit=0,rule='Contracts were measured from hash-verified immutable original compiler objects. Independent replay recompiles both old source and new views against these contracts; no historical object is required as a runtime input.'))


def recipes():
    return read_json(LANE/'reference-contracts.json')['entries']


def recipe(address):
    return next(r for r in recipes()if int(r['address'],0)==address)


def view(ref):
    if int(ref['address'],0)==0x0202a8e0:return SOURCE/'faithful/runtime/20261031_overlay_file_size250/file_size.c'
    return mirror(ref['source'])


def dependencies(source):
    found=set()
    def visit(path):
        for name in re.findall(r'^\s*#include\s+"([^"]+)"',path.read_text(),re.M):
            dependency=(path.parent/name).resolve()
            dependency.relative_to(ROOT)
            if dependency not in found:
                found.add(dependency);visit(dependency)
    visit(source)
    return [dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in sorted(found)]


def identity(row,ref):
    fields=lambda r:((r.get('program')or''),r['processor'],r['module'],r['mode'],int(r['address'],0),r['bytes'],r['targetSha256'],r['name'])
    if fields(row)!=fields(ref):raise ValueError('Closed full physical identity or original extent changed')


def contract(row,ref):
    identity(row,ref)
    actual=normalized(object_contract(ROOT/row['object']));raw=linker.relocation_rows(ROOT/row['object'],row['name'])
    if actual!=ref['allocatedContract']or raw!=ref['rawRelocations']or not row['exactAfterDeclaredRelocation']or row['compiledBytes']!=ref['bytes']:raise ValueError('Frozen allocated/raw/native contract changed')
    return hashlib.sha256(json.dumps(actual,separators=(',',':')).encode()).hexdigest()


def build(source,directory,ref,negative=False):
    row=compile_source(source,directory/'compile',ref);identity(row,ref)
    row['sourceDependencies']=dependencies(source)
    if not negative:row['allocatedContractSha256']=contract(row,ref)
    native_bindings=copy.deepcopy(ref['nativeSymbolEntries'])
    try:real=linker.validate(row,native_bindings,directory/'link')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0],dict):raise
        real=dict(exactCallerBytes=False,comparison=error.args[0])
    if negative and real['exactCallerBytes']:raise ValueError('Wrong C unexpectedly retained complete original bytes')
    if linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(directory/'link/caller.o',row['name']):raise ValueError('Real linker split changed raw relocations')
    row.update(realLink=real,nativeSymbolEntries=native_bindings,sourceLanguage='C',ordinaryCBytes=0 if negative else row['bytes'],justifiedAssemblyBytes=0)
    return row,(directory/'link/caller.bin').read_bytes()


def negative_source(source,folder,before,after):
    text=source.read_text()
    if text.count(before)!=1:raise ValueError('Wrong-C control is ambiguous')
    text=text.replace(before,after)
    text=re.sub(r'(^\s*#include\s+)"([^"]+)"',lambda m:m[1]+'"'+(source.parent/m[2]).resolve().as_posix()+'"',text,flags=re.M)
    folder.mkdir(parents=True,exist_ok=True);path=folder/source.name;path.write_text(text)
    return path


def replay_builds():
    results=[]
    for ref in recipes():
        address=int(ref['address'],0);folder=WORK/'replay-builds'/f'{address:08x}'
        old=ROOT/ref['source']
        if sha256(old)!=ref['sourceSha256']:raise ValueError('Frozen previous source changed')
        for dependency in ref['sourceDependencies']:
            if sha256(ROOT/dependency['path'])!=dependency['sha256']:raise ValueError('Frozen previous source dependency changed')
        prior,unused=build(old,folder/'previous',ref);fresh,body=build(view(ref),folder/'view',ref)
        result=dict(identity=ref['admittedIdentity'],bytes=ref['bytes'],previous=prior,view=fresh,allocatedContractEqual=True,rawRelocationsEqual=True,sourceCredit=0)
        results.append(result)
        print(dict(module=ref['module'],address=ref['address'],previousAndViewNativeExact=True),flush=True)
    return results


if __name__=='__main__':snapshot()
