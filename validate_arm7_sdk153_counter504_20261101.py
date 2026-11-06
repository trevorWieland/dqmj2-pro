import copy
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import match_arm7_sdk153_counter504_20261101 as matcher
import link_arm7_sdk153_counter504_20261101 as policy
import link_arm7_bulk_20261030 as base
import arm7_sdk150_counter_native_20261101 as native
from unicorn import UcError
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk153-counter504-controls-20261101.json'
_FRESH=None
def checked(path,digest):
    path=(ROOT/path).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Counter complete source/input/product missing or changed')
    return path
def fresh():
    global _FRESH
    if _FRESH is None:
        call=subprocess.run([sys.executable,str(Path(matcher.__file__).resolve())],cwd=Path.cwd(),capture_output=True,text=True,timeout=300)
        if call.returncode:raise ValueError(call.stderr[-6000:])
        _FRESH=json.loads(matcher.REPORT.read_text())
    return _FRESH
def validate(report):
    if report!=fresh():raise ValueError('Fresh full counter source/link/native/input evidence differs')
    if report['generatorSha256']!=sha256(matcher.__file__):raise ValueError('Counter generator differs')
    pins=json.loads((matcher.SOURCE/'generator-pins.json').read_text())['files']
    complete=pins+[dict(path=(matcher.SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(matcher.SOURCE/'generator-pins.json'))]
    if report['generatorSources']!=complete or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Current counter replay closure differs')
    for item in pins:checked(item['path'],item['sha256'])
    if len(report['matches'])!=1 or report['matchedInitializedBytes']!=504 or report['matchedCodeBytes']!=496 or report['generatedLiteralBytes']!=8 or report['initializedDenominatorDelta']!=0:raise ValueError('Full counter range/classification differs')
    row=report['matches'][0];policy.qualified(row)
    for key,digest in [('source','sourceSha256'),('object','objectSha256'),('compiler','compilerSha256')]:checked(row[key],row[digest])
    for dep in row['sourceDependencies']:checked(dep['path'],dep['sha256'])
    link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'caller.bin',row['targetSha256']);checked(directory/'linked.elf',link['linkedElfSha256'])
    if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Full ordinary C/unaltered real-link proof absent')
    trace=row['oracle']['trace'];compressed=checked(trace['path'],trace['compressedSha256']).read_bytes();raw=gzip.decompress(compressed)
    if compressed[4:8]!=bytes(4)or hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic counter trace differs')
    records=json.loads(raw)
    if len(records)!=1024 or not all(r['original']==r['compiled']and r['original']['actualOwnReturn']and r['original']['modelPassed']for r in records):raise ValueError('Actual counter returns/model/source equivalence absent')
    proof=report['abiLayoutProof'];checked(proof['source'],proof['sourceSha256']);checked(proof['object'],proof['objectSha256'])
    if proof['values']!=[4,4,4,0x694,0xb4,0x53c]+[r[2]for r in native.UPDATES]:raise ValueError('Compiler source declaration layout differs')
    return{('arm7','','arm7-main','0x27ea1b8','arm'):row}
def main():
    report=fresh();validate(report);metadata=[];direct=[];execution=[]
    def rejected(name,action,collection):
        try:action()
        except(ValueError,FileNotFoundError,KeyError,UcError)as error:collection.append(dict(name=name,rejected=True,error=str(error)))
        else:raise ValueError('Counter invalid evidence survived:'+name)
    def changed(path,value):
        bad=copy.deepcopy(report);obj=bad
        for key in path[:-1]:obj=obj[key]
        obj[path[-1]]=value;validate(bad)
    for name,path,value in [('rom',('romSha256',),'0'*64),('processor',('processor',),'arm9'),('module',('module',),'arm7-wram'),('program',('program',),'child.srl'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),('count',('newOrdinaryFunctionCount',),2),('bytes',('matchedInitializedBytes',),505),('code',('matchedCodeBytes',),504),('pools',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),504),('whole',('wholeModuleLinked',),True),('complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),2049),('fill',('totalActualFillReturns',),0),('constructor',('constructorActualReturnCredit',),2048),('nested',('totalScopedNestedReturns',),2048),('wrong',('wrongC',),[]),('layout',('abiLayoutProof','values'),[]),('address',('matches',0,'address'),'0x27ea1bc'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('headers',('matches',0,'sourceDependencies'),[]),('flags',('matches',0,'compilerFlags'),[]),('exact',('matches',0,'exactBytes'),False),('source-only',('matches',0,'sourceOnlyCompilerInput'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('argument',('matches',0,'sourceAbiContract','physicalArgumentWords'),1),('return',('matches',0,'sourceAbiContract','declaredReturn'),'u32'),('providers',('matches',0,'oracle','providerReplacements'),['port']),('raw-state',('matches',0,'oracle','allRawCpuFlagsStackRamReadsAndOrderedWritesCompared'),False)]:rejected(name,lambda path=path,value=value:changed(path,value),metadata)
    row=report['matches'][0]
    for key,value in [('name','other'),('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-wram'),('mode','thumb'),('address','0x27ea1bc'),('bytes',500),('source','src/unowned.c'),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',[]),('compilerSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/no-producer.json'))]:
        bad=dict(row);bad[key]=value;rejected('caller-'+key,lambda bad=bad:policy.qualified(bad),direct)
    before=base.data_binding;policy.validate(row,matcher.WORK/'restoration-positive')
    if base.data_binding is not before:raise ValueError('Counter word rule leaked after success')
    rejected('default-word-refusal',lambda:base.validate(row,matcher.WORK/'default-refusal-control'),direct)
    rejected('output-escape',lambda:policy.validate(row,ROOT/'evidence'),direct)
    if base.data_binding is not before:raise ValueError('Counter word rule leaked after failure')
    modules,unused=base.namespace('')
    for address in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('neighbor-'+hex(address),lambda address=address:base.data_binding(row,address,modules),direct)
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();body=(matcher.WORK/'positive/real-link/caller.bin').read_bytes()
    for name,case,budget in [('runtime-word',dict(native.cases()[0],wrongRuntimePointer=True),1000),('exhaustion',native.cases()[0],1)]:
        for label,candidate in [('original',None),('compiled',body)]:rejected(name+'-'+label,lambda case=case,budget=budget,candidate=candidate:native.run(main,wram,case,0,budget=budget,body=candidate),execution)
    path=matcher.WORK/'positive/real-link/caller.bin';content=path.read_bytes()
    try:path.write_bytes(bytes([content[0]^1])+content[1:]);rejected('changed-linked-body',lambda:validate(report),metadata)
    finally:path.write_bytes(content)
    trace=ROOT/report['matches'][0]['oracle']['trace']['path'];held=trace.with_name('held-native-records.json.gz')
    try:trace.rename(held);rejected('missing-native-product',lambda:validate(report),metadata)
    finally:
        if held.is_file():held.rename(trace)
    validate(json.loads(matcher.REPORT.read_text()))
    write_json(REPORT,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReportSha256=sha256(matcher.REPORT),metadataControls=metadata,metadataControlCount=len(metadata),directPolicyControls=direct,directPolicyControlCount=len(direct),nativePrerequisiteControls=execution,nativeControlCount=len(execution),freshSourceOnlyBuildBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0))
    print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),metadata=len(metadata),policy=len(direct),native=len(execution))),flush=True)
if __name__=='__main__':main()
