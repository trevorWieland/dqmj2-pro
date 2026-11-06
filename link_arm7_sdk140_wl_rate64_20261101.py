import json
from project import ROOT,sha256
import link_arm7_bulk_20261030 as base
BASE_SHA='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PROFILE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk140-wl-pair192-final/profile.json'
PROFILE_SHA='b2a5efdfe380c1c542d531ccf107b0b3abcf4baa3c2557f14153459ab5bf518d'
IDENTITY=('', 'arm7', 'arm7-main', 'arm', '0x27e9b98', 64)

def qualified(entry):
    if sha256(ROOT/'link_arm7_bulk_20261030.py')!=BASE_SHA or sha256(PROFILE)!=PROFILE_SHA:raise ValueError('Frozen base linker or exact caller profile changed')
    seed=json.loads(PROFILE.read_text())['units'][0]
    identity=tuple(entry.get(k,'')for k in('program','processor','module','mode','address','bytes'))
    if identity!=IDENTITY:raise ValueError('Runtime-word rule is limited to this exact host main ARM64 caller')
    for key in('compiler','compilerSha256','compilerFlags','source','sourceSha256','sourceDependencies','targetSha256','inputModuleSha256','romSha256','runtimePointerQualification'):
        if entry.get(key)!=seed[key]:raise ValueError('Exact caller/header/module/build/producer closure differs:'+key)
    for row in [dict(path=entry['source'],sha256=entry['sourceSha256']),*entry['sourceDependencies']]:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Current typed source/header changed')
    proof=entry['runtimePointerQualification'];path=ROOT/proof['report']
    if sha256(path)!=proof['sha256']:raise ValueError('Actual incoming-descriptor producer evidence changed')
    report=json.loads(path.read_text())
    if sha256(ROOT/report['generator'])!=report['generatorSha256']or report['storage']!='0x0380fff4'or report['storageBytes']!=4 or report['origin']!='incoming descriptor word0'or report['constructorReturnCredit']!=0 or report['moduleBssOwnership']is not False:raise ValueError('Measured runtime word producer scope differs')
    return dict(program='',processor='arm7',module='external-arm7-runtime-pointer-word',kind='data',mode='data',address='0x380fff4',region='descriptor-produced-absolute-pointer-no-module-ownership',storageBytes=4,producerQualification=proof,sourceCredit=0)

def validate(entry,directory):
    binding=qualified(entry);original=base.data_binding
    def scoped(candidate,target,modules):
        if target==0x0380fff4:
            if candidate is not entry:raise ValueError('Runtime-word rule escaped its validated caller')
            return dict(binding)
        return original(candidate,target,modules)
    base.data_binding=scoped
    try:return base.validate(entry,directory)
    finally:base.data_binding=original
