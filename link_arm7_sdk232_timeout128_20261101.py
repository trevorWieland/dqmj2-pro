import json
from project import ROOT,sha256
import link_arm7_bulk_20261030 as base
BASE_SHA='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PROFILE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk232-timeout128-final/profile.json'
PROFILE_SHA='3904e2521048b023fe8f63203f3d6710d3737ee303f2ed95ab6a26d91a80933b'
IDENTITIES={('', 'arm7', 'arm7-main', 'arm', '0x27f0288', 128)}

def qualified(entry):
    if sha256(ROOT/'link_arm7_bulk_20261030.py')!=BASE_SHA or sha256(PROFILE)!=PROFILE_SHA:raise ValueError('Frozen base linker or exact caller profile changed')
    seeds=json.loads(PROFILE.read_text())['units']
    identity=tuple(entry.get(k,'')for k in('program','processor','module','mode','address','bytes'))
    if identity not in IDENTITIES:raise ValueError('Runtime-word rule is limited to the two exact settings callers')
    seed=next(row for row in seeds if row['address']==entry['address'])
    for key in('name','compiler','compilerSha256','compilerFlags','source','sourceSha256','sourceDependencies','targetSha256','inputModuleSha256','romSha256','runtimePointerQualification','nativeInterfaceContract'):
        if entry.get(key)!=seed[key]:raise ValueError('Exact caller/header/module/build/producer closure differs:'+key)
    for row in [dict(path=entry['source'],sha256=entry['sourceSha256']),*entry['sourceDependencies']]:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Current typed source/header changed')
    proof=entry['runtimePointerQualification'];path=ROOT/proof['report']
    if sha256(path)!=proof['sha256']:raise ValueError('Actual incoming-descriptor producer evidence changed')
    report=json.loads(path.read_text())
    if sha256(ROOT/report['generator'])!=report['generatorSha256']or report['storage']!='0x0380fff4'or report['storageBytes']!=4 or report['origin']!='incoming descriptor word0'or report['constructorReturnCredit']!=0 or report['moduleBssOwnership']is not False:raise ValueError('Measured runtime word producer scope differs')
    contract=entry['nativeInterfaceContract']
    if contract['physicalArgumentWords']!=1 or contract['unsigned16ClockInputsPreserved']is not True or sha256(ROOT/contract['sourceNativeModel'])!=contract['sourceNativeModelSha256']:raise ValueError('Complete TX caller and callback/priority source interface differs')
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
