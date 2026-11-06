import copy
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import match_arm7_sdk184_start952_20261101 as matcher
import link_arm7_sdk184_start952_20261101 as policy
import link_arm7_bulk_20261030 as base
import arm7_sdk176_start_explicit_model_20261101 as native
import arm7_sdk183_start_cases_20261101 as vectors
import source_dependencies
from unicorn import UcError
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk184-start952-controls-20261101.json'
_FRESH=None
def checked(path,digest):
    path=(ROOT/path).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Startup complete source/input/product missing or changed')
    return path
def fresh():
    global _FRESH
    if _FRESH is None:
        result=subprocess.run([sys.executable,str(Path(matcher.__file__).resolve())],cwd=Path.cwd(),capture_output=True,text=True,timeout=600)
        if result.returncode:raise ValueError(result.stderr[-7000:])
        _FRESH=json.loads(matcher.REPORT.read_text())
    return _FRESH
def validate(report):
    if report!=fresh():raise ValueError('Fresh full startup source/native/link/helper evidence differs')
    pins=json.loads((matcher.SOURCE/'generator-pins.json').read_text())['files'];complete=pins+[dict(path=(matcher.SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(matcher.SOURCE/'generator-pins.json'))]
    if report['generatorSha256']!=sha256(matcher.__file__)or report['generatorSources']!=complete or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Current complete startup closure differs')
    for pin in pins:checked(pin['path'],pin['sha256'])
    if len(report['matches'])!=1 or report['matchedInitializedBytes']!=952 or report['matchedCodeBytes']!=876 or report['generatedLiteralBytes']!=76 or report['initializedDenominatorDelta']!=0:raise ValueError('Complete startup code/literal/extent differs')
    row=report['matches'][0];policy.qualified(row)
    if not source_dependencies.dependencies_current(row):raise ValueError('Quoted source-parent include closure differs')
    for key,digest in [('source','sourceSha256'),('object','objectSha256'),('compiler','compilerSha256')]:checked(row[key],row[digest])
    for dep in row['sourceDependencies']:checked(dep['path'],dep['sha256'])
    link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'caller.bin',row['targetSha256']);checked(directory/'linked.elf',link['linkedElfSha256'])
    if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Full ordinary C/unchanged real-link proof missing')
    trace=row['oracle']['trace'];compressed=checked(trace['path'],trace['compressedSha256']).read_bytes();raw=gzip.decompress(compressed)
    if compressed[4:8]!=bytes(4)or hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic startup trace differs')
    records=json.loads(raw)
    if len(records)!=len(vectors.cases())or not all(r['original']==r['compiled']and r['original']['actualOwnReturn']and r['original']['modelPassed']for r in records):raise ValueError('Actual fresh startup return/own-effect/helper ABI proof absent')
    proof=report['abiLayoutProof'];checked(proof['source'],proof['sourceSha256']);checked(proof['object'],proof['objectSha256'])
    if proof['values']!=[4,8,4,0x694,12,0x3c0,0x356,0x350,0x352,0x3b2,0x3a8,0x30c,0x310,392,560]or proof['preambleBitfieldBytes']!=[[0x33a,4]]:raise ValueError('Startup real SDK/list/bitfield layout differs')
    helper=report['explicitU64HelperProof'];data=json.loads(checked(helper['path'],helper['sha256']).read_text())
    if data['actualOwnReturns']!=256 or data['zeroActualReturns']!=72 or data['sourceCredit']!=0:raise ValueError('Explicit original helper API qualification differs')
    return{('arm7','','arm7-wram','0x37f8de0','arm'):row}
def main():
    report=fresh();validate(report);metadata=[];direct=[];execution=[]
    def rejected(name,action,collection):
        try:action()
        except(ValueError,FileNotFoundError,KeyError,UcError)as error:collection.append(dict(name=name,rejected=True,error=str(error)))
        else:raise ValueError('Invalid startup proof survived:'+name)
    def changed(path,value):
        bad=copy.deepcopy(report);obj=bad
        for key in path[:-1]:obj=obj[key]
        obj[path[-1]]=value;validate(bad)
    for name,path,value in [('rom',('romSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-main'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),('bytes',('matchedInitializedBytes',),953),('code',('matchedCodeBytes',),952),('pools',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),952),('whole',('wholeModuleLinked',),True),('complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),0),('nested',('totalScopedDirectCalleeReturns',),0),('fill',('totalActualFillReturns',),0),('constructor',('constructorActualReturnCredit',),1),('wrong',('wrongC',),[]),('helper-credit',('explicitU64HelperProof','sourceCredit'),72),('helper-abi',('explicitU64HelperProof','sha256'),'0'*64),('layout',('abiLayoutProof','values'),[]),('bitfield',('abiLayoutProof','preambleBitfieldBytes'),[]),('address',('matches',0,'address'),'0x37f8de4'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('headers',('matches',0,'sourceDependencies'),[]),('flags',('matches',0,'compilerFlags'),[]),('exact',('matches',0,'exactBytes'),False),('source-only',('matches',0,'sourceOnlyCompilerInput'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('argument',('matches',0,'sourceAbiContract','physicalArgumentWords'),4),('return',('matches',0,'sourceAbiContract','declaredReturn'),'u64'),('zero-ub',('matches',0,'sourceAbiContract','zeroDivisionExpressionAbsent'),False),('providers',('matches',0,'oracle','providerReplacements'),['init']),('synthetic',('matches',0,'oracle','syntheticEmptyQueuePrerequisite'),False),('initializer-erased',('matches',0,'oracle','realEffectfulNativeInitializersAndCleanupRetained'),False),('raw-state',('matches',0,'oracle','fullRawCpuFlagsStackRamReadsAndWritesCompared'),False)]:rejected(name,lambda path=path,value=value:changed(path,value),metadata)
    row=report['matches'][0]
    for key,value in [('name','other'),('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-main'),('mode','thumb'),('address','0x37f8de4'),('bytes',876),('source','src/unowned.c'),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',[]),('compilerSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/no-producer.json')),('nativeHelperContracts',[]),('nativeHelperContracts',[dict(row['nativeHelperContracts'][0],sha256='0'*64)]),('nativeHelperContracts',[dict(row['nativeHelperContracts'][0],address='0x3806bfc')])]:
        bad=dict(row);bad[key]=value;rejected('caller-'+key,lambda bad=bad:policy.qualified(bad),direct)
    before=base.data_binding;policy.validate(row,matcher.WORK/'restoration-positive')
    if base.data_binding is not before:raise ValueError('Startup word rule leaked after success')
    rejected('default-word-refusal',lambda:base.validate(row,matcher.WORK/'default-refusal-control'),direct);rejected('output-escape',lambda:policy.validate(row,ROOT/'evidence'),direct)
    if base.data_binding is not before:raise ValueError('Startup word rule leaked after failure')
    modules,unused=base.namespace('')
    for address in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('neighbor-'+hex(address),lambda address=address:base.data_binding(row,address,modules),direct)
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();body=(matcher.WORK/'positive/real-link/caller.bin').read_bytes()
    def supported(case,budget,candidate,image=main,ram=wram):
        result=native.run(image,ram,case,0,body=candidate,budget=budget)
        if not result['actualOwnReturn']or not result.get('modelPassed'):raise ValueError('Native startup context unsupported; no return/effect credit')
    for name,case,budget in [('runtime-word',dict(vectors.cases()[0],wrongRuntimePointer=True),200000),('missing-empty-lists',dict(vectors.cases()[0],initializeLists=False),200000),('exhaustion',vectors.cases()[0],1)]:
        for label,candidate in [('original',None),('compiled',body)]:rejected(name+'-'+label,lambda case=case,budget=budget,candidate=candidate:supported(case,budget,candidate),execution)
    for name,image,ram in [('main',bytes([main[0]^1])+main[1:],wram),('wram',main,bytes([wram[0]^1])+wram[1:])]:rejected('current-input-'+name,lambda image=image,ram=ram:supported(vectors.cases()[0],200000,None,image,ram),execution)
    path=matcher.WORK/'positive/real-link/caller.bin';raw=path.read_bytes()
    try:path.write_bytes(bytes([raw[0]^1])+raw[1:]);rejected('changed-real-linked-body',lambda:validate(report),metadata)
    finally:path.write_bytes(raw)
    trace=ROOT/report['matches'][0]['oracle']['trace']['path'];held=trace.with_name('held-native-records.json.gz')
    try:trace.rename(held);rejected('missing-native-product',lambda:validate(report),metadata)
    finally:
        if held.is_file():held.rename(trace)
    validate(json.loads(matcher.REPORT.read_text()));write_json(REPORT,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReportSha256=sha256(matcher.REPORT),metadataControls=metadata,metadataControlCount=len(metadata),directPolicyControls=direct,directPolicyControlCount=len(direct),nativePrerequisiteControls=execution,nativeControlCount=len(execution),freshSourceOnlyBuildBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0))
    print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),metadata=len(metadata),policy=len(direct),native=len(execution))),flush=True)
if __name__=='__main__':main()
