import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from goal_resume_resource_path_views import SOURCE,LANE,WORK,AUDIT,SDK,mirror,typedefs
import match_runtime as compiler
import link_runtime_unit as linker
sys.path.insert(0,str(ROOT/'public_tools'))
from public_tools.native_objects import object_contract


def normalized(value):
    return json.loads(json.dumps(value))


def reference(address):
    row=next(r for r in read_json(AUDIT)['minimumMigrationInventory']if int(r['address'],0)==address)
    report=read_json(ROOT/row['evidence']);entries=report.get('functionMatches',report.get('matches',[]))
    entry=next(e for e in entries if int(e['address'],0)==address)
    entry=dict(entry,compilerFlags=entry.get('compilerFlags',entry.get('flags')))
    if any(entry.get(k)!=row.get(v)for k,v in [('source','sourceUnit'),('sourceSha256','sourceSha256'),('object','object'),('objectSha256','objectSha256'),('compilerSha256','compilerSha256'),('compilerFlags','compilerFlags')]):raise ValueError('Frozen source/object/compiler recipe differs from admitted audit')
    if sha256(ROOT/entry['source'])!=entry['sourceSha256']or sha256(ROOT/entry['object'])!=entry['objectSha256']:raise ValueError('Selected canonical source/object changed')
    return entry


def compile_source(source,directory,ref):
    executable=ROOT/ref['compilerPath']
    if sha256(executable)!=ref['compilerSha256']:raise ValueError('Exact compiler changed')
    saved=compiler.WORK,compiler.FLAGS
    try:
        compiler.WORK=directory;compiler.FLAGS=ref['compilerFlags'][:]
        rows,unused=compiler.compare(source,ref['module'],ref['compilerFlags'][0][2:],ref['compilerFlags'][ref['compilerFlags'].index('-inline')+1],False,compiler=executable)
    finally:compiler.WORK,compiler.FLAGS=saved
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('Genuine pointer view compile failed',rows))
    if rows[0]['compilerFlags']!=ref['compilerFlags']:raise ValueError('Existing compiler recipe changed')
    return dict(rows[0],program='')


def geometry(ref):
    folder=WORK/'sdk-geometry';folder.mkdir(parents=True,exist_ok=True)
    source=folder/'geometry.c';obj=folder/'geometry.o'
    include=(SOURCE/'sdk_file.h').as_posix()
    checks=['sizeof(unsigned int)==4','sizeof(unsigned long)==4','sizeof(u32)==4','sizeof(FSFile)==72','sizeof(OSThreadQueue)==8','(unsigned int)&((FSFile*)0)->prop.file.top==36','(unsigned int)&((FSFile*)0)->prop.file.bottom==40']
    source.write_text('#include "'+include+'"\n'+'\n'.join('typedef char Verified'+str(i)+'[('+condition+')?1:-1];'for i,condition in enumerate(checks))+'\n')
    command=[str(ROOT/ref['compilerPath']),*ref['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(('Actual ARM32 SDK type geometry failed',process.stdout,process.stderr))
    originals=typedefs(SDK.read_text());copies=typedefs((SOURCE/'sdk_file.h').read_text())
    for name in read_json(LANE/'sdk-types.json')['completeTypedefs']:
        if originals[name]!=copies[name]:raise ValueError('A completed SDK dependency/tag type was changed')
    return dict(actualCompilerPassed=True,checks=checks,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),exactCompletedTypeDeclarations=True)


def qualify(address,source=None,label=None):
    ref=reference(address);source=source or mirror(ref['source']);folder=WORK/'providers'/(label or f'{address:08x}')
    row=compile_source(source,folder/'compile',ref)
    old=normalized(object_contract(ROOT/ref['object']));new=normalized(object_contract(ROOT/row['object']))
    raw=linker.relocation_rows(ROOT/ref['object'],ref['name']);fresh=linker.relocation_rows(ROOT/row['object'],row['name'])
    result=dict(previousSource=ref['source'],previousSourceSha256=ref['sourceSha256'],previousObject=ref['object'],previousObjectSha256=ref['objectSha256'],view=row,allocatedContractEqual=old==new,rawRelocationsEqual=raw==fresh,sourceCredit=0)
    output=label or f'{address:08x}'
    write_json(LANE/(output+'-comparison.json'if label else f'{address:08x}'+'-first-comparison.json'),result)
    if old!=new or raw!=fresh or not row['exactAfterDeclaredRelocation']or row['compiledBytes']!=ref['bytes']:
        raise ValueError(('Provider allocated/native contract changed; migration blocked without further attempts',hex(address),row['compiledBytes'],row['matchingBytes']))
    bindings={r['symbol']:dict(program='',processor='arm9',module='main',address=r['target'],mode='data'if r['type']==2 else'arm',kind='data'if r['type']==2 else'function')for r in row['relocations']}
    real=linker.validate(row,bindings,folder/'link')
    if linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(folder/'link/caller.o',row['name']):raise ValueError('Actual native link split altered source relocations')
    result.update(realLink=real,rawRelocations=raw)
    write_json(LANE/(output+'-qualified.json'),result)
    print(dict(provider=hex(address),bytes=row['bytes'],compiled=row['compiledBytes'],allocatedEqual=True,rawRelocationsEqual=True,realNativeLink=True),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--providers',action='store_true');group.add_argument('--faithful-size',action='store_true');group.add_argument('--load-provider',action='store_true');options=parser.parse_args()
    if options.faithful_size:
        diff=read_json(LANE/'faithful-structural-diff.json')
        if not diff['reverseTransformEqualsOriginalStatementControlFlowExactly']or sha256(ROOT/diff['newFaithfulView'])!=diff['newFaithfulSha256']:raise ValueError('Authorized faithful structural proof changed')
        qualify(0x0202a8e0,ROOT/diff['newFaithfulView'],'faithful-size')
        return
    if options.load_provider:
        if not read_json(LANE/'faithful-size-qualified.json')['allocatedContractEqual']:raise ValueError('Faithful size provider gate is not closed')
        qualify(0x0203cc3c)
        return
    ref=reference(0x0202a8e0);layout=geometry(ref)
    write_json(LANE/'sdk-geometry.json',layout)
    results=[qualify(address)for address in[0x0202a8e0,0x0203cc3c]]
    write_json(LANE/'providers-qualified.json',dict(status='providers-qualified-no-adoption',sourceCredit=0,results=results,sdkGeometry=layout))


if __name__=='__main__':main()
