import copy
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import match_arm7_sdk140_wl_pair192_20261101 as matcher
import link_arm7_sdk140_wl_rate64_20261101 as policy
import link_arm7_bulk_20261030 as original_policy
import arm7_sdk140_rate64_native_20261101 as native
from unicorn import UcError
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk140-wl-pair192-controls-20261101.json'
_FRESH=None

def checked(path,digest):
    path=(ROOT/path).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('WL complete source/input/product missing or changed')
    return path

def fresh():
    global _FRESH
    if _FRESH is None:
        call=subprocess.run([sys.executable,str(Path(matcher.__file__).resolve())],cwd=Path.cwd(),capture_output=True,text=True,timeout=300)
        if call.returncode:raise ValueError(call.stderr[-8000:])
        _FRESH=json.loads(matcher.REPORT.read_text())
    return _FRESH

def validate(report):
    if report!=fresh():raise ValueError('Fresh full WL source/link/native/input evidence differs')
    pins=json.loads((matcher.SOURCE/'generator-pins.json').read_text())['files']
    complete=pins+[dict(path=(matcher.SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(matcher.SOURCE/'generator-pins.json'))]
    if report['generatorSha256']!=sha256(matcher.__file__)or report['generatorSources']!=complete or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Complete current replay closure differs')
    for item in pins:checked(item['path'],item['sha256'])
    if len(report['matches'])!=2 or report['matchedInitializedBytes']!=192 or report['matchedCodeBytes']!=176 or report['generatedLiteralBytes']!=16 or report['initializedDenominatorDelta']!=0:raise ValueError('Qualified full ranges or byte classifications differ')
    result={}
    for row in report['matches']:
        for pathkey,digestkey in [('source','sourceSha256'),('object','objectSha256'),('compiler','compilerSha256')]:checked(row[pathkey],row[digestkey])
        for dep in row['sourceDependencies']:checked(dep['path'],dep['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'caller.bin',row['targetSha256']);checked(directory/'linked.elf',link['linkedElfSha256'])
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Full ordinary-C/unaltered real-link match missing')
        trace=row['oracle']['trace'];compressed=checked(trace['path'],trace['compressedSha256']).read_bytes();raw=gzip.decompress(compressed)
        if compressed[4:8]!=bytes(4)or hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic raw native proof differs')
        records=json.loads(raw)
        if row['oracle']['actualOriginalAndCompiledReturns']!=2*len(records)or not all(r[k]['actualOwnReturn']and r[k]['modelPassed']for r in records for k in('original','compiled')):raise ValueError('Actual entry returns/independent model absent')
        if int(row['address'],0)==native.TOP:policy.qualified(row)
        result[('arm7','','arm7-main',row['address'],'arm')]=row
    proof=report['abiLayoutProof'];checked(proof['source'],proof['sourceSha256']);checked(proof['object'],proof['objectSha256'])
    if proof['measuredValues']!=[4,4,4,4,980,932,946,952,976,824]or not proof['originalObjectTotalExtentNotClaimed']or proof['sourceDataCredit']!=0:raise ValueError('Measured physical ABI/prefix offsets differ')
    return result

def main():
    report=fresh();validate(report);controls=[];direct=[];native_controls=[]
    def rejected(name,action,collection):
        try:action()
        except(ValueError,FileNotFoundError,KeyError,UcError)as error:collection.append(dict(name=name,rejected=True,error=str(error)))
        else:raise ValueError('Invalid WL source evidence survived:'+name)
    def changed(path,value):
        bad=copy.deepcopy(report);obj=bad
        for key in path[:-1]:obj=obj[key]
        obj[path[-1]]=value;validate(bad)
    for name,path,value in [('build',('romSha256',),'0'*64),('cpu',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),('count',('newOrdinaryFunctionCount',),3),('bytes',('matchedInitializedBytes',),193),('code',('matchedCodeBytes',),192),('pools',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),192),('whole-module',('wholeModuleLinked',),True),('complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),3841),('nested',('totalScopedNestedReturns',),3840),('wrong-source',('wrongC',),[]),('policy-disabled',('callerSpecificLinker','exactCallerSourceHeaderCompilerAndFullIdentityRequired'),False),('word-width',('callerSpecificLinker','wordBytes'),8),('policy-global',('callerSpecificLinker','defaultAndEarlierPoliciesUnchanged'),False),('layout-long-width',('abiLayoutProof','measuredValues'),[4,8,4,4,980,932,946,952,976,824]),('layout-full-object',('abiLayoutProof','originalObjectTotalExtentNotClaimed'),False),('getter-new-credit',('existingGetter76SourceClosure','additionalSourceCredit'),76),('address',('matches',0,'address'),'0x27e9b9c'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('header',('matches',0,'sourceDependencies'),[]),('compiler-flags',('matches',0,'compilerFlags'),[]),('exact',('matches',0,'exactBytes'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('source-only',('matches',0,'sourceOnlyCompilerInput'),False),('argument',('matches',0,'sourceAbiContract','physicalArgumentWords'),0),('whole-object-extent',('matches',0,'sourceAbiContract','completeOriginalWlManObjectExtentClaimed'),True),('raw-state',('matches',0,'oracle','fullRawCpuFlagsStackRamReadsAndOrderedWritesCompared'),False),('providers',('matches',0,'oracle','providerReplacements'),['memory']),('scene',('matches',0,'oracle','wholeSceneOrPhysicalHardwareContextProven'),True)]:rejected(name,lambda path=path,value=value:changed(path,value),controls)
    row=report['matches'][0]
    for key,value in [('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-wram'),('mode','thumb'),('address','0x27e9b9c'),('bytes',60),('source','src/unowned.c'),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',[]),('compilerSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/no-producer.json'))]:
        bad=dict(row);bad[key]=value;rejected('caller-'+key,lambda bad=bad:policy.qualified(bad),direct)
    before=original_policy.data_binding;policy.validate(row,matcher.WORK/'restoration-positive')
    if original_policy.data_binding is not before:raise ValueError('Scoped word rule leaked after success')
    rejected('default-word-refusal',lambda:original_policy.validate(row,matcher.WORK/'default-refusal-control'),direct)
    rejected('output-escape',lambda:policy.validate(row,ROOT/'evidence'),direct)
    if original_policy.data_binding is not before:raise ValueError('Scoped word rule leaked after failure')
    modules,unused=original_policy.namespace('')
    for address in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('neighbor-word-'+hex(address),lambda address=address:original_policy.data_binding(row,address,modules),direct)
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();bodies={int(r['address'],0):(matcher.WORK/r['address'][2:]/'real-link/caller.bin').read_bytes()for r in report['matches']}
    for name,case,budget in [('changed-descriptor',dict(native.cases()[0],wrongDescriptor=True),200000),('changed-runtime-word',dict(native.cases()[0],wrongRuntimePointer=True),200000),('exhaustion',native.cases()[0],1)]:
        for label,candidate in [('original',None),('compiled',bodies)]:rejected(name+'-'+label,lambda case=case,budget=budget,candidate=candidate:native.run(main,wram,case,0,budget=budget,compiledBodies=candidate),native_controls)
    path=matcher.WORK/'27e9b98/real-link/caller.bin';content=path.read_bytes()
    try:
        path.write_bytes(bytes([content[0]^1])+content[1:]);rejected('changed-actual-linked-body',lambda:validate(report),controls)
    finally:path.write_bytes(content)
    trace=ROOT/report['matches'][0]['oracle']['trace']['path'];held=trace.with_name('held-native-records.json.gz')
    try:
        trace.rename(held);rejected('missing-actual-native-product',lambda:validate(report),controls)
    finally:
        if held.is_file():held.rename(trace)
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),directPolicyControls=direct,directPolicyControlCount=len(direct),nativePrerequisiteControls=native_controls,nativeControlCount=len(native_controls),freshSourceOnlyBuildBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0)
    write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),metadata=len(controls),policy=len(direct),native=len(native_controls))),flush=True)
if __name__=='__main__':main()
