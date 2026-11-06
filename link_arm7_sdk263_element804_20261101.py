import json
from project import ROOT,sha256
import link_arm7_bulk_20261030 as base
BASE_SHA='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PROFILE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk263-element804-final/profile.json'
PROFILE_SHA='2b00a207e7b638bf4498507f06507b27700f3227b6e2bbb9fd1ecd5d4fbd39a0'
IDENTITIES={('', 'arm7', 'arm7-main', 'arm', '0x27f3c1c', 804)}

def qualified(entry):
    if sha256(ROOT/'link_arm7_bulk_20261030.py')!=BASE_SHA or sha256(PROFILE)!=PROFILE_SHA:raise ValueError('Frozen base linker or parameter profiles changed')
    identity=tuple(entry.get(k,'')for k in('program','processor','module','mode','address','bytes'))
    if identity not in IDENTITIES:raise ValueError('Runtime word rule limited to exact three parameter callers')
    seed=next(row for row in json.loads(PROFILE.read_text())['units']if row['address']==entry['address'])
    for key in('name','compiler','compilerSha256','compilerFlags','source','sourceSha256','sourceDependencies','targetSha256','inputModuleSha256','romSha256','runtimePointerQualification','nativeInterfaceContract'):
        if entry.get(key)!=seed[key]:raise ValueError('Exact caller/source/build/producer closure changed:'+key)
    for row in [dict(path=entry['source'],sha256=entry['sourceSha256']),*entry['sourceDependencies']]:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Current complete typed source changed')
    proof=entry['runtimePointerQualification'];path=ROOT/proof['report']
    if sha256(path)!=proof['sha256']:raise ValueError('Incoming descriptor producer changed')
    report=json.loads(path.read_text())
    if sha256(ROOT/report['generator'])!=report['generatorSha256']or report['storage']!='0x0380fff4'or report['storageBytes']!=4 or report['origin']!='incoming descriptor word0'or report['constructorReturnCredit']!=0 or report['moduleBssOwnership']is not False:raise ValueError('Runtime word producer scope changed')
    contract=entry['nativeInterfaceContract']
    if contract['completeWlContextBytes']!=0x694 or contract['descriptorProducedAbsoluteWord']!='0x380fff4'or sha256(ROOT/contract['sourceNativeModel'])!=contract['sourceNativeModelSha256']:raise ValueError('Typed parameter/native model changed')
    return dict(program='',processor='arm7',module='external-arm7-runtime-pointer-word',kind='data',mode='data',address='0x380fff4',region='descriptor-produced-absolute-pointer-no-module-ownership',storageBytes=4,producerQualification=proof,sourceCredit=0)

def validate(entry,directory):
    binding=qualified(entry);original=base.data_binding
    def scoped(candidate,target,modules):
        if target==0x0380fff4:
            if candidate is not entry:raise ValueError('Runtime word rule escaped validated parameter caller')
            return dict(binding)
        return original(candidate,target,modules)
    base.data_binding=scoped
    try:return base.validate(entry,directory)
    finally:base.data_binding=original
