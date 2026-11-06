import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import match_runtime
import link_arm7_bulk_20261030 as strict
from project import ROOT,sha256,configuration,write_json

IDENTITY=dict(processor='arm7',program='',module='arm7-main',mode='arm',address='0x27f0950',bytes=104,targetSha256='3bcd261fd23f5c6574f52dfc5819b8395e5de529144d76a68ccf5de685feb49d')
PINS=ROOT/'provenance/arm7-sdk291-pspoll-scope-pins-20261102.json'
SCOPE=ROOT/'evidence/attempts/arm7-sdk289-pspoll-callback104-scope-20261102.json'
INSTALL=ROOT/'evidence/attempts/arm7-sdk290-pspoll-installation-20261102.json'

def verify(entry,scope,install):
    if any(entry.get(k)!=v for k,v in IDENTITY.items()):raise ValueError('Only one measured ARM7 callback scope identity')
    if any(scope.get(k)!=v for k,v in IDENTITY.items()):raise ValueError('Native scope identity changed')
    if scope['instructionBytes']!=100 or scope['literalBytes']!=4 or scope['literal']!='f4ff8003'or scope['sourceCredit']!=0 or scope['denominatorByteIncrease']!=0:raise ValueError('Instruction/pool/zero-credit partition changed')
    if scope['configuredOverlaps']or not scope['defaultCanonicalEntryAbsent']or not scope['allPassed']or scope['actualOwnReturns']!=630 or len(scope['results'])!=630 or scope['actualPrerequisiteReturns']!=2520:raise ValueError('Complete scope/native-return evidence missing')
    if any(not r['actualOwnReturn']or not r['passed']or not all(r['checks'].values())or r['orderedStores']!=r['expectedOrderedStores']or any(not x['actualReturn']for x in r['nativePrerequisiteReturns'])or any(not 0x027f0950<=pc<0x027f09b4 for pc in r['visited'])for r in scope['results']):raise ValueError('Native state, return or owned execution evidence changed')
    if any(not r['insideOwnBody']and int(r['target'],0)!=0x027f0950 for r in scope['alignedArmBranchCandidates']):raise ValueError('Outside interior-reference candidate unresolved')
    if install['actualInitializerReturns']!=8 or install['realPspollInstallations']!=6 or len(install['rows'])!=8 or install['actualPrerequisiteReturns']!=24 or install['sourceCredit']!=0:raise ValueError('Real complete initializer evidence missing')
    for row in install['rows']:
        base=int(row['context'],0);stores=row['callbackStore']
        if row['beforePointer']!='0x0'or not row['actualInitializerReturn']['actualReturn']or len(stores)!=2 or int(stores[0]['value'],0)!=0 or any(s['width']!=4 or int(s['address'],0)!=base+0x464 for s in stores)or stores[-1]['value']!=row['installedPointer']:raise ValueError('Actual initializer zeroing/install effects changed')
        if row['pspollInstalled']!=(row['modeArgument']in(0,2,3))or row['pspollInstalled']and row['installedPointer']!='0x27f0950':raise ValueError('Installed pointer and raw mode evidence changed')
    loader=install['loaderModule']
    if loader['id']!='arm7-main'or loader['inputFileOffset']!=63636 or loader['bytes']!=96388 or install['callbackInputFileOffset']!=63636+0x10950:raise ValueError('Original loader ownership changed')
    return dict(IDENTITY,instructionBytes=100,literalBytes=4,sourceCredit=0,sharedNamespaceModified=False,canonicalAdmissionNotGranted=True)

def current():
    for row in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen scope producer/report changed:'+row['path'])
    scope=json.loads(SCOPE.read_text());install=json.loads(INSTALL.read_text())
    for path,expected in [('extract/arm7/runtime/arm7-main.bin',scope['inputMainSha256']),('extract/arm7/runtime/arm7-wram.bin',scope['inputWramSha256']),(scope['inventory'],scope['inventorySha256']),(scope['sourceReference'],scope['sourceReferenceSha256']),(install['loaderInput'],install['loaderInputSha256']),('arm7_runtime.py',install['loaderGeneratorSha256'])]:
        if sha256(ROOT/path)!=expected:raise ValueError('Current native/reference/loader input differs:'+path)
    if sha256(configuration()['rom'])!=scope['romSha256']:raise ValueError('Original whole ROM changed')
    raw=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()[0x10950:0x109b8]
    if hashlib.sha256(raw).hexdigest()!=IDENTITY['targetSha256']:raise ValueError('Complete callback bytes changed')
    if 0x027f0950 in strict.namespace('')[1]:raise ValueError('Original unknown-entry refusal changed')
    return scope,install

def main():
    pins=json.loads(PINS.read_text())['files'];producers=pins[:2]
    for row in producers:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen original producer changed')
        bootstrap='import runpy,sys;sys.path.insert(0,sys.argv[1]);runpy.run_path(sys.argv[2],run_name="__main__")'
        p=subprocess.run([sys.executable,'-I','-S','-c',bootstrap,str(ROOT),str(ROOT/row['path'])],cwd=ROOT.parent,capture_output=True,text=True,timeout=120)
        if p.returncode:raise ValueError(p.stdout+p.stderr)
    scope,install=current();positive=verify(IDENTITY,scope,install);controls=[]
    def reject(name,entry,a,b):
        try:verify(entry,a,b)
        except ValueError as error:controls.append(dict(name=name,rejected=True,error=str(error)));return
        raise ValueError('Scope mutation unexpectedly accepted:'+name)
    for key,value in [('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-wram'),('mode','thumb'),('address','0x27f0954'),('bytes',100),('targetSha256','0'*64)]:reject('wrong-qualified-'+key,dict(IDENTITY,**{key:value}),scope,install)
    for name,path,value in [('missing-own-return',('results',0,'actualOwnReturn'),False),('native-state-change',('results',0,'orderedStores'),[]),('pool-executed',('results',0,'visited'),[0x027f09b4]),('outside-interior-reference',('alignedArmBranchCandidates',),[dict(insideOwnBody=False,target='0x27f0954')]),('missing-all-cases',('actualOwnReturns',),629),('data-credit',('sourceCredit',),104)]:
        altered=copy.deepcopy(scope);target=altered
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value;reject(name,IDENTITY,altered,install)
    for name,key,value in [('no-real-installer','actualInitializerReturns',0),('wrong-loader-source','callbackInputFileOffset',0)]:reject(name,IDENTITY,scope,dict(install,**{key:value}))
    altered=copy.deepcopy(install);altered['rows'][0]['callbackStore'][-1]['value']='0x27f0954';reject('wrong-actual-install-word',IDENTITY,scope,altered)
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),pins=PINS.relative_to(ROOT).as_posix(),pinsSha256=sha256(PINS),scopeReportSha256=sha256(SCOPE),installationReportSha256=sha256(INSTALL),positive=positive,negativeControls=controls,negativeControlCount=len(controls),sourceCredit=0,defaultUnknownFunctionAndDataGuardsUnchanged=True);write_json(ROOT/'evidence/verification/arm7-sdk291-pspoll-scope-controls-20261102.json',report);print(json.dumps(dict(controls=len(controls),allRejected=True,sourceCredit=0)),flush=True)

if __name__=='__main__':main()
