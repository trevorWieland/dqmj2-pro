import copy
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import match_arm7_sdk263_element804_20261101 as matcher
import link_arm7_sdk263_element804_20261101 as policy
import link_arm7_bulk_20261030 as base
import arm7_sdk262_element804_native_20261101 as native
import source_dependencies
from unicorn import UcError
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk265-element804-controls-20261101.json'
_FRESH=None

def checked(path,digest):
    path=(ROOT/path).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Current source/input/product missing or changed')
    return path

def fresh():
    global _FRESH
    if _FRESH is None:
        result=subprocess.run([sys.executable,str(Path(matcher.__file__).resolve())],cwd=Path.cwd(),capture_output=True,text=True,timeout=1200)
        if result.returncode:raise ValueError(result.stderr[-7000:])
        _FRESH=json.loads(matcher.REPORT.read_text())
    return _FRESH

def validate(report):
    if report!=fresh():raise ValueError('Fresh parser source/native/link report differs')
    pins=json.loads((matcher.SOURCE/'generator-pins.json').read_text())['files'];complete=pins+[dict(path=(matcher.SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(matcher.SOURCE/'generator-pins.json'))]
    if report['generatorSha256']!=sha256(matcher.__file__)or report['generatorSources']!=complete or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Current source-only closure differs')
    for pin in pins:checked(pin['path'],pin['sha256'])
    if len(report['matches'])!=1 or [report[k]for k in('matchedInitializedBytes','matchedCodeBytes','generatedLiteralBytes','initializedDenominatorDelta')]!=[804,800,4,0]:raise ValueError('Complete parser extents differ')
    row=report['matches'][0];policy.qualified(row)
    if not source_dependencies.dependencies_current(row):raise ValueError('Exact quoted source-parent include closure differs')
    for key,digest in[('source','sourceSha256'),('object','objectSha256'),('compiler','compilerSha256')]:checked(row[key],row[digest])
    for dep in row['sourceDependencies']:checked(dep['path'],dep['sha256'])
    link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'caller.bin',row['targetSha256']);checked(directory/'linked.elf',link['linkedElfSha256'])
    if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Complete ordinary C and genuine unchanged linked bytes missing')
    trace=row['oracle']['trace'];compressed=checked(trace['path'],trace['compressedSha256']).read_bytes();raw=gzip.decompress(compressed)
    if compressed[4:8]!=bytes(4)or hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic native trace changed')
    records=json.loads(raw);vectors=[c for c in native.cases()if native.source_compatible(c)]
    if len(records)!=len(vectors)or not all(r['original']==r['compiled']and r['original']['actualOwnReturn']and r['original']['modelPassed']and native.source_compatible(r['original']['case'])for r in records):raise ValueError('Actual source-compatible parser returns/state evidence missing')
    if report['totalActualOwnReturns']!=2*len(records)or report['rawNativeCasesExcludedFromSourceScope']!=36:raise ValueError('Owned return or source-boundary accounting differs')
    proof=report['abiLayoutProof'];checked(proof['source'],proof['sourceSha256']);checked(proof['object'],proof['objectSha256'])
    if proof['values']!=[0x694,44,88,8,866,868,900,932,936,958,960,1028,1052,74,0,4,6,8,10,12,18,20,24,26,28,32,36,40]:raise ValueError('Complete parser and native context layouts differ')
    for wrong in report['wrongC']:
        build=wrong['build'];checked(build['source'],build['sourceSha256']);checked(build['object'],build['objectSha256'])
        if wrong['actualOwnReturns']!=len(records)or not wrong['modelRejections']:raise ValueError('Wrong parser C did not return and fail independent model')
    return {('arm7','','arm7-main',row['address'],'arm'):row}

def main():
    report=fresh();validate(report);metadata=[];direct=[];execution=[];scopes=[]
    def rejected(name,action,collection):
        try:action()
        except(ValueError,FileNotFoundError,KeyError,UcError)as error:collection.append(dict(name=name,rejected=True,error=str(error)))
        else:raise ValueError('Invalid parser evidence survived:'+name)
    def changed(path,value):
        bad=copy.deepcopy(report);obj=bad
        for key in path[:-1]:obj=obj[key]
        obj[path[-1]]=value;validate(bad)
    changes=[('rom',('romSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),('bytes',('matchedInitializedBytes',),800),('code',('matchedCodeBytes',),804),('pools',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),804),('whole',('wholeModuleLinked',),True),('complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),0),('nested',('totalActualHelperReturns',),0),('prefix',('totalActualPrefixFillReturns',),0),('constructor',('constructorActualReturnCredit',),1),('wrong',('wrongC',),[]),('layout',('abiLayoutProof','values'),[]),('scope-exclusion',('rawNativeCasesExcludedFromSourceScope',),0),('callback-credit',('calleeSourceCredit',),1),('cfp-alignment',('matches',0,'sourceAbiContract','storedCfpPointerAlignmentBytes'),1),('rate-capacity',('matches',0,'sourceAbiContract','supportedRateLengthDomain'),[0,255]),('stream-extent',('matches',0,'sourceAbiContract','sourceStreamMaximumBytes'),65535)]
    for name,key,value in[('address','address','0x27f3c20'),('mode','mode','thumb'),('source','sourceSha256','0'*64),('headers','sourceDependencies',[]),('flags','compilerFlags',[]),('exact','exactBytes',False),('source-only','sourceOnlyCompilerInput',False),('blob','originalObjectScaffolding',True)]:changes.append((name,('matches',0,key),value))
    for name,path,value in changes:rejected(name,lambda path=path,value=value:changed(path,value),metadata)
    row=report['matches'][0]
    for key,value in[('name','other'),('processor','arm9'),('program','child.srl'),('module','arm7-wram'),('mode','thumb'),('address','0x27f3c20'),('bytes',800),('source','src/unowned.c'),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',[]),('compilerSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],physicalArgumentWords=4)),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],sourceNativeModelSha256='0'*64)),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],checkerBytes=40)),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/no-producer.json'))]:
        bad=dict(row);bad[key]=value;rejected(key,lambda bad=bad:policy.qualified(bad),direct)
    before=base.data_binding;policy.validate(row,matcher.WORK/'policy-restoration')
    if base.data_binding is not before:raise ValueError('Runtime word rule leaked on success')
    rejected('default-refusal',lambda:base.validate(row,matcher.WORK/'default-refusal'),direct);rejected('output-escape',lambda:policy.validate(row,ROOT/'evidence'),direct)
    if base.data_binding is not before:raise ValueError('Runtime word rule leaked on error')
    modules,unused=base.namespace('')
    for address in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('neighbor-'+hex(address),lambda address=address:base.data_binding(row,address,modules),direct)
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();body=(matcher.WORK/'positive/real-link/caller.bin').read_bytes();case=next(c for c in native.cases()if c['elements']==[[3,[6]]]and native.source_compatible(c))
    def supported(case,budget,candidate,image=main,ram=wram):
        if candidate is not None and not native.source_compatible(case):raise ValueError('Typed CFP alignment is outside supported C; no C return claim')
        result=native.run(image,ram,case,0,body=candidate,budget=budget)
        if not result['actualOwnReturn']or not result.get('modelPassed'):raise ValueError('Prerequisite unsupported; zero post-fault/return credit')
    for name,altered,budget in[('runtime-word',dict(case,wrongRuntimePointer=True),100000),('checker',dict(case,nullChecker=True),100000),('join',dict(case,nullJoin=True),100000),('exhaustion',case,1)]:
        for label,candidate in [('original',None),('compiled',body)]:rejected(name+'-'+label,lambda altered=altered,budget=budget,candidate=candidate:supported(altered,budget,candidate),execution)
    for name,image,ram in[('main',bytes([main[0]^1])+main[1:],wram),('wram',main,bytes([wram[0]^1])+wram[1:])]:rejected('current-'+name,lambda image=image,ram=ram:supported(case,100000,None,image,ram),execution)
    odd=next(c for c in native.cases()if not native.source_compatible(c));raw_native=native.run(main,wram,odd,0)
    if not raw_native['actualOwnReturn']or not raw_native['modelPassed']:raise ValueError('Odd CFP raw native characterization failed')
    rejected('odd-cfp-source-domain',lambda:supported(odd,100000,body),scopes)
    excessive=dict(case,elements=[[1,[2,4,11]]]);rejected('rate-source-capacity',lambda:supported(excessive,100000,body),scopes)
    excessive=dict(case,elements=[[7,[1]*255],[7,[1]*255]]);rejected('stream-source-capacity',lambda:supported(excessive,100000,body),scopes)
    path=matcher.WORK/'positive/real-link/caller.bin';raw=path.read_bytes()
    try:path.write_bytes(bytes([raw[0]^1])+raw[1:]);rejected('changed-linked-product',lambda:validate(report),metadata)
    finally:path.write_bytes(raw)
    trace=ROOT/row['oracle']['trace']['path'];held=trace.with_name('held-native-records.json.gz')
    try:trace.rename(held);rejected('missing-native-product',lambda:validate(report),metadata)
    finally:
        if held.is_file():held.rename(trace)
    validate(json.loads(matcher.REPORT.read_text()));write_json(REPORT,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReportSha256=sha256(matcher.REPORT),metadataControls=metadata,metadataControlCount=len(metadata),directPolicyControls=direct,directPolicyControlCount=len(direct),nativePrerequisiteControls=execution,nativeControlCount=len(execution),sourceScopeControls=scopes,sourceScopeControlCount=len(scopes),oddAlignedCfpOriginalNativeOnly=raw_native,oddAlignedCfpCSourceCredit=0,freshSourceOnlyBuildBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0));print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),metadata=len(metadata),policy=len(direct),native=len(execution),sourceScope=len(scopes))),flush=True)

if __name__=='__main__':main()
