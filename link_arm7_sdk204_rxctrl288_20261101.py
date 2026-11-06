import json
from project import ROOT,sha256
import link_arm7_bulk_20261030 as base
BASE_SHA='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PROFILE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk204-rxctrl288-final/profile.json'
PROFILE_SHA='bc58564003bbd421dedb99c575556a0ed0dd7dd361f7a94d4124f2d3a25003bb'
IDENTITY=('', 'arm7', 'arm7-wram', 'arm', '0x37fb1e0', 288)

def qualified(entry):
    if sha256(ROOT/'link_arm7_bulk_20261030.py')!=BASE_SHA or sha256(PROFILE)!=PROFILE_SHA:raise ValueError('Frozen base linker or exact caller profile changed')
    seed=json.loads(PROFILE.read_text())['units'][0]
    identity=tuple(entry.get(k,'')for k in('program','processor','module','mode','address','bytes'))
    if identity!=IDENTITY:raise ValueError('Runtime-word rule is limited to this exact host WRAM ARM288 receive initializer')
    for key in('name','compiler','compilerSha256','compilerFlags','source','sourceSha256','sourceDependencies','targetSha256','inputModuleSha256','romSha256','runtimePointerQualification','nativeModeDomain'):
        if entry.get(key)!=seed[key]:raise ValueError('Exact caller/header/module/build/producer closure differs:'+key)
    for row in [dict(path=entry['source'],sha256=entry['sourceSha256']),*entry['sourceDependencies']]:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Current typed source/header changed')
    proof=entry['runtimePointerQualification'];path=ROOT/proof['report']
    if sha256(path)!=proof['sha256']:raise ValueError('Actual incoming-descriptor producer evidence changed')
    report=json.loads(path.read_text())
    if sha256(ROOT/report['generator'])!=report['generatorSha256']or report['storage']!='0x0380fff4'or report['storageBytes']!=4 or report['origin']!='incoming descriptor word0'or report['constructorReturnCredit']!=0 or report['moduleBssOwnership']is not False:raise ValueError('Measured runtime word producer scope differs')
    domain=entry['nativeModeDomain']
    if domain['allowedGlobalModes']!=[0,1,2,3]or domain['outsideSourceDomainHasNoCredit']is not True or sha256(ROOT/domain['nativeModel'])!=domain['nativeModelSha256']:raise ValueError('RX supported native-produced mode domain differs')
    import hashlib
    raw=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    if hashlib.sha256(raw).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(raw[0x8f3c:0x8f3c+128]).hexdigest()!=domain['producerSha256']:raise ValueError('Current exact original supported-mode producer differs')
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
