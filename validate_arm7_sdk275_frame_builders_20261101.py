import copy
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import match_arm7_sdk274_frame_builders_20261101 as matcher
import link_arm7_sdk274_frame_builders_20261101 as policy
import link_arm7_bulk_20261030 as base
import arm7_sdk273_frame_constructors_native_20261101 as native
import source_dependencies
from unicorn import UcError
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk275-frame-builders1304-controls-20261101.json'
_FRESH=None

def checked(path,digest):
    path=(ROOT/path).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Current frame source/input/product missing or changed')
    return path

def fresh():
    global _FRESH
    if _FRESH is None:
        result=subprocess.run([sys.executable,str(Path(matcher.__file__).resolve())],cwd=Path.cwd(),capture_output=True,text=True,timeout=1800)
        if result.returncode:raise ValueError(result.stderr[-7000:])
        _FRESH=json.loads(matcher.REPORT.read_text())
    return _FRESH

def exclusion(report):
    path=ROOT/'evidence/verification/accepted-cohort131-identities-v2-20261101.json';checked(path,'603f6c630bdf9dbb17e924ba14959f60d2d1463355a25738a75a2e2f2ed6152a');accepted=json.loads(path.read_text())['functions'];identities={(r['processor'],r.get('program',''),r['module'],r['mode'],int(r['address'],0)if isinstance(r['address'],str)else r['address'])for r in accepted}
    if any((r['processor'],r.get('program',''),r['module'],r['mode'],int(r['address'],0))in identities for r in report['matches']):raise ValueError('Frame identity was already accepted at this proof epoch')
    return dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path),allSevenQualifiedIdentitiesAbsent=True,numericAddressNormalization=True)

def validate(report):
    if report!=fresh():raise ValueError('Fresh frame source/native/link report differs')
    pins=json.loads((matcher.SOURCE/'generator-pins.json').read_text())['files'];complete=pins+[dict(path=(matcher.SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(matcher.SOURCE/'generator-pins.json'))]
    if report['generatorSha256']!=sha256(matcher.__file__)or report['generatorSources']!=complete or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Current source-only frame closure differs')
    for pin in pins:checked(pin['path'],pin['sha256'])
    if len(report['matches'])!=7 or [report[k]for k in('matchedInitializedBytes','matchedCodeBytes','generatedLiteralBytes','initializedDenominatorDelta')]!=[1304,1248,56,0]:raise ValueError('Complete frame/code/literal extents differ')
    exclusion(report);output={};own=helpers=setup=fills=0
    for row in report['matches']:
        policy.qualified(row)
        if not source_dependencies.dependencies_current(row):raise ValueError('Source-parent frame includes differ')
        for key,digest in[('source','sourceSha256'),('object','objectSha256'),('compiler','compilerSha256')]:checked(row[key],row[digest])
        for dep in row['sourceDependencies']:checked(dep['path'],dep['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'caller.bin',row['targetSha256']);checked(directory/'linked.elf',link['linkedElfSha256'])
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Complete ordinary frame C/genuine linked bytes absent')
        trace=row['oracle']['trace'];compressed=checked(trace['path'],trace['compressedSha256']).read_bytes();raw=gzip.decompress(compressed)
        if compressed[4:8]!=bytes(4)or hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic frame native trace changed')
        records=json.loads(raw);vectors=[c for c in native.cases()if c['entry']==int(row['address'],0)]
        if len(records)!=len(vectors)or not all(r['original']==r['compiled']and r['original']['actualOwnReturn']and r['original']['modelPassed']for r in records):raise ValueError('Actual fresh-C/native frame/state/producer returns missing')
        own+=2*len(records);helpers+=sum(2*len(r['original']['actualNativeHelperReturns'])for r in records);setup+=sum(2*len(r['original']['actualSetupReturns'])for r in records);fills+=sum(2*len(r['original']['actualPrefixFillReturns'])for r in records);output[('arm7','','arm7-main',row['address'],'arm')]=row
    if [own,helpers,setup,fills]!=[report[k]for k in('totalActualOwnReturns','totalActualHelperReturns','totalActualSetupEntryReturns','totalActualPrefixFillReturns')]:raise ValueError('Owned/helper/setup/prefix return counts differ')
    proof=report['abiLayoutProof'];checked(proof['source'],proof['sourceSha256']);checked(proof['object'],proof['objectSha256'])
    if proof['values']!=[0x694,64,16,306,6,18,20,44,50,51,948,424,1336,86,92,54,44,48,48,54,44,50,4,12,255,82,46,46,4,4,2]:raise ValueError('Complete physical frame and packet-view layouts differ')
    for wrong in report['wrongC']:
        build=wrong['build'];checked(build['source'],build['sourceSha256']);checked(build['object'],build['objectSha256'])
        if not wrong['actualOwnReturns']or not wrong['modelRejections']:raise ValueError('Wrong frame C did not return and fail independent model')
    return output

def main():
    report=fresh();validate(report);metadata=[];direct=[];execution=[];scopes=[]
    def rejected(name,action,collection):
        try:action()
        except(ValueError,FileNotFoundError,KeyError,UcError)as error:collection.append(dict(name=name,rejected=True,error=str(error)))
        else:raise ValueError('Invalid frame proof survived:'+name)
    def changed(path,value):
        bad=copy.deepcopy(report);obj=bad
        for key in path[:-1]:obj=obj[key]
        obj[path[-1]]=value;validate(bad)
    changes=[('rom',('romSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),('bytes',('matchedInitializedBytes',),1308),('code',('matchedCodeBytes',),1304),('pools',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),1304),('whole',('wholeModuleLinked',),True),('complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),0),('nested',('totalActualHelperReturns',),0),('setup',('totalActualSetupEntryReturns',),0),('prefix',('totalActualPrefixFillReturns',),0),('constructor',('constructorPrefixActualReturnCredit',),1),('wrong',('wrongC',),[]),('layout',('abiLayoutProof','values'),[]),('callees',('calleeSourceCredit',),1),('portable-packets',('sourceSpecificPacketTypeAndroidPortabilityProven',),True),('aid-producers',('actualFifteenAidProducerSequenceRatherThanSuppliedCalleeResult',),False)]
    for i,row in enumerate(report['matches']):
        for name,key,value in[('address','address',hex(int(row['address'],0)+4)),('mode','mode','thumb'),('source','sourceSha256','0'*64),('headers','sourceDependencies',[]),('flags','compilerFlags',[]),('exact','exactBytes',False),('source-only','sourceOnlyCompilerInput',False),('blob','originalObjectScaffolding',True)]:changes.append((name+str(i),('matches',i,key),value))
    for name,path,value in changes:rejected(name,lambda path=path,value=value:changed(path,value),metadata)
    for row in report['matches']:
        for key,value in[('name','other'),('processor','arm9'),('program','child.srl'),('module','arm7-wram'),('mode','thumb'),('address',hex(int(row['address'],0)+4)),('bytes',row['bytes']+4),('source','src/unowned.c'),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',[]),('compilerSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],physicalArgumentWords=4)),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],sourceNativeModelSha256='0'*64)),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],ordinaryCSourceVisibilityPromotionOnly=False)),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/no-frame-producer.json'))]:
            bad=dict(row);bad[key]=value;rejected(row['address']+'-'+key,lambda bad=bad:policy.qualified(bad),direct)
        before=base.data_binding;policy.validate(row,matcher.WORK/('restoration-'+row['address'][2:]))
        if base.data_binding is not before:raise ValueError('Frame runtime word rule leaked after success')
        rejected(row['address']+'-default-refusal',lambda row=row:base.validate(row,matcher.WORK/('default-refusal-'+row['address'][2:])),direct);rejected(row['address']+'-output-escape',lambda row=row:policy.validate(row,ROOT/'evidence'),direct)
        if base.data_binding is not before:raise ValueError('Frame runtime word rule leaked after error')
    modules,unused=base.namespace('')
    for address in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('neighbor-'+hex(address),lambda address=address:base.data_binding(report['matches'][0],address,modules),direct)
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    for row in report['matches']:
        case=next(c for c in native.cases()if c['entry']==int(row['address'],0)and not c['heapFailure']and c['check']==0);body=(ROOT/Path(row['realLink']['lcf']).parent/'caller.bin').read_bytes()
        def supported(case,budget,candidate,image=main,ram=wram):
            result=native.run(image,ram,case,0,body=candidate,budget=budget)
            if not result['actualOwnReturn']or not result.get('modelPassed'):raise ValueError('Frame prerequisite unsupported; zero post-fault/return credit')
        tests=[('runtime-word',dict(case,wrongRuntimePointer=True),100000),('instruction-bound',case,1)]
        tests.append(('cam-storage',dict(case,camIndex=65535),100000)if row['name']=='MakeReAssResFrame'else('mac-backing',dict(case,nullDestination=True),100000))
        for name,altered,budget in tests:
            for label,candidate in [('original',None),('compiled',body)]:rejected(row['address']+'-'+name+'-'+label,lambda altered=altered,budget=budget,candidate=candidate:supported(altered,budget,candidate),execution)
        for name,image,ram in[('main',bytes([main[0]^1])+main[1:],wram),('wram',main,bytes([wram[0]^1])+wram[1:])]:rejected(row['address']+'-current-'+name,lambda image=image,ram=ram:supported(case,100000,None,image,ram),execution)
        if row['sourceAbiContract']['physicalArgumentWords']>=2:rejected(row['address']+'-word-width',lambda:supported(dict(case,word=65536),100000,body),scopes)
        if row['name']in('MakeAssReqFrame','MakeReAssReqFrame','MakeProbeReqFrame','MakeReAssResFrame'):rejected(row['address']+'-ssid-backing',lambda:supported(dict(case,ssidLength=33),100000,body),scopes)
    row=report['matches'][0];path=ROOT/Path(row['realLink']['lcf']).parent/'caller.bin';raw=path.read_bytes()
    try:path.write_bytes(bytes([raw[0]^1])+raw[1:]);rejected('changed-linked-product',lambda:validate(report),metadata)
    finally:path.write_bytes(raw)
    trace=ROOT/row['oracle']['trace']['path'];held=trace.with_name('held-frame-native.json.gz')
    try:trace.rename(held);rejected('missing-native-product',lambda:validate(report),metadata)
    finally:
        if held.is_file():held.rename(trace)
    validate(json.loads(matcher.REPORT.read_text()));write_json(REPORT,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReportSha256=sha256(matcher.REPORT),metadataControls=metadata,metadataControlCount=len(metadata),directPolicyControls=direct,directPolicyControlCount=len(direct),nativePrerequisiteControls=execution,nativeControlCount=len(execution),sourceScopeControls=scopes,sourceScopeControlCount=len(scopes),acceptedEpochExclusion=exclusion(report),freshSourceOnlyBuildBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0));print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),metadata=len(metadata),policy=len(direct),native=len(execution),sourceScope=len(scopes))),flush=True)

if __name__=='__main__':main()
