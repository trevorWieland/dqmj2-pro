import copy
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import match_arm7_sdk249_rates180_20261101 as rates
import match_arm7_sdk251_parameters_20261101 as parameters
import link_arm7_sdk251_parameters_20261101 as policy
import link_arm7_bulk_20261030 as base
import arm7_sdk248_rates180_native_20261101 as rate_native
import arm7_sdk250_parameters_native_20261101 as parameter_native
import source_dependencies
from unicorn import UcError
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk252-rates-parameters400-controls-20261101.json'
MATCHERS=(rates,parameters)
MODELS=(rate_native,parameter_native)
_FRESH={}

def checked(path,digest):
    path=(ROOT/path).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Current source/input/product missing or changed')
    return path

def fresh(index):
    if index not in _FRESH:
        matcher=MATCHERS[index];result=subprocess.run([sys.executable,str(Path(matcher.__file__).resolve())],cwd=Path.cwd(),capture_output=True,text=True,timeout=600)
        if result.returncode:raise ValueError(result.stderr[-7000:])
        _FRESH[index]=json.loads(matcher.REPORT.read_text())
    return _FRESH[index]

def validate(index,report):
    matcher=MATCHERS[index];native=MODELS[index]
    if report!=fresh(index):raise ValueError('Fresh source/native/link report differs')
    pins=json.loads((matcher.SOURCE/'generator-pins.json').read_text())['files'];complete=pins+[dict(path=(matcher.SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(matcher.SOURCE/'generator-pins.json'))]
    if report['generatorSha256']!=sha256(matcher.__file__)or report['generatorSources']!=complete or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Current source-only closure differs')
    for pin in pins:checked(pin['path'],pin['sha256'])
    expected=(1,180,176,4)if index==0 else(3,220,192,28)
    if tuple([len(report['matches'])]+[report[k]for k in('matchedInitializedBytes','matchedCodeBytes','generatedLiteralBytes')])!=expected or report['initializedDenominatorDelta']!=0:raise ValueError('Complete function/code/literal extents differ')
    output={};own=helpers=0
    for row in report['matches']:
        if index:policy.qualified(row)
        if not source_dependencies.dependencies_current(row):raise ValueError('Source-parent include closure differs')
        for key,digest in[('source','sourceSha256'),('object','objectSha256'),('compiler','compilerSha256')]:checked(row[key],row[digest])
        for dep in row['sourceDependencies']:checked(dep['path'],dep['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'caller.bin',row['targetSha256']);checked(directory/'linked.elf',link['linkedElfSha256'])
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Ordinary C unchanged genuine link evidence missing')
        trace=row['oracle']['trace'];compressed=checked(trace['path'],trace['compressedSha256']).read_bytes();raw=gzip.decompress(compressed)
        if compressed[4:8]!=bytes(4)or hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic full native trace changed')
        records=json.loads(raw);vectors=native.cases()if not index else[c for c in native.cases()if c['entry']==int(row['address'],0)]
        if len(records)!=len(vectors)or not all(r['original']==r['compiled']and r['original']['actualOwnReturn']and r['original']['modelPassed']for r in records):raise ValueError('Returning full-state source/native evidence missing')
        own+=2*len(records);helpers+=sum(2*len(r['original']['actualNativeHelperReturns'])for r in records);output[('arm7','','arm7-main',row['address'],'arm')]=row
    if own!=report['totalActualOwnReturns']or helpers!=report['totalActualHelperReturns']:raise ValueError('Own/helper return accounting differs')
    proof=report['abiLayoutProof'];checked(proof['source'],proof['sourceSha256']);checked(proof['object'],proof['objectSha256'])
    if proof['values']!=([1,2,4,4,4,4,1,2,0,2,240]if not index else[0x694,0x5f0,0x5f0,0x5f2,0x3a8,0x3b8]):raise ValueError('Typed complete storage layout changed')
    for wrong in report['wrongC']:
        build=wrong['build'];checked(build['source'],build['sourceSha256']);checked(build['object'],build['objectSha256'])
        if not wrong['actualOwnReturns']or not wrong['modelRejections']:raise ValueError('Wrong C did not actually return and fail the independent model')
    return output

def main():
    reports=[fresh(i)for i in range(2)];metadata=[];direct=[];execution=[];early_returns=[]
    for index,report in enumerate(reports):validate(index,report)
    exclusion=parameters.exclusion([row for report in reports for row in report['matches']])
    def rejected(name,action,collection):
        try:action()
        except(ValueError,FileNotFoundError,KeyError,UcError)as error:collection.append(dict(name=name,rejected=True,error=str(error)))
        else:raise ValueError('Invalid bundled proof survived:'+name)
    for index,report in enumerate(reports):
        def changed(path,value):
            bad=copy.deepcopy(report);obj=bad
            for key in path[:-1]:obj=obj[key]
            obj[path[-1]]=value;validate(index,bad)
        changes=[('rom',('romSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),('bytes',('matchedInitializedBytes',),0),('code',('matchedCodeBytes',),0),('pools',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),400),('whole',('wholeModuleLinked',),True),('complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),0),('nested',('totalActualHelperReturns',),0),('constructor',('constructorActualReturnCredit',),1),('wrong',('wrongC',),[]),('layout',('abiLayoutProof','values'),[]),('callee-credit',('calleeSourceCredit',),1)]
        for row_index,row in enumerate(report['matches']):
            for name,key,value in[('address','address','0x27e0000'),('mode','mode','thumb'),('source','sourceSha256','0'*64),('headers','sourceDependencies',[dict(path='src/missing.h',sha256='0'*64)]),('flags','compilerFlags',[]),('exact','exactBytes',False),('source-only','sourceOnlyCompilerInput',False),('blob','originalObjectScaffolding',True)]:changes.append((name+str(row_index),('matches',row_index,key),value))
        for name,path,value in changes:rejected(str(index)+'-'+name,lambda path=path,value=value:changed(path,value),metadata)
        row=report['matches'][0];path=ROOT/row['object'];raw=path.read_bytes()
        try:path.write_bytes(bytes([raw[0]^1])+raw[1:]);rejected(str(index)+'-changed-object',lambda:validate(index,report),metadata)
        finally:path.write_bytes(raw)
        path=ROOT/row['oracle']['trace']['path'];held=path.with_name('held-native-records.json.gz')
        try:path.rename(held);rejected(str(index)+'-missing-native-product',lambda:validate(index,report),metadata)
        finally:
            if held.is_file():held.rename(path)
    for row in reports[1]['matches']:
        for key,value in[('name','other'),('processor','arm9'),('program','child.srl'),('module','arm7-wram'),('mode','thumb'),('address',hex(int(row['address'],0)+4)),('bytes',row['bytes']+4),('source','src/unowned.c'),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',[]),('compilerSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],physicalArgumentWords=4)),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],sourceNativeModelSha256='0'*64)),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],completeWlContextBytes=12)),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/no-producer.json'))]:
            bad=dict(row);bad[key]=value;rejected(row['address']+'-'+key,lambda bad=bad:policy.qualified(bad),direct)
        before=base.data_binding;policy.validate(row,parameters.WORK/('restoration-'+row['address'][2:]))
        if base.data_binding is not before:raise ValueError('Runtime word policy leaked on success')
        rejected(row['address']+'-default-refusal',lambda row=row:base.validate(row,parameters.WORK/('default-refusal-'+row['address'][2:])),direct);rejected(row['address']+'-output-escape',lambda row=row:policy.validate(row,ROOT/'evidence'),direct)
        if base.data_binding is not before:raise ValueError('Runtime word policy leaked on error')
    modules,unused=base.namespace('')
    for address in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('neighbor-'+hex(address),lambda address=address:base.data_binding(reports[1]['matches'][0],address,modules),direct)
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    for index,report in enumerate(reports):
        native=MODELS[index]
        for row in report['matches']:
            case=native.cases()[0]if not index else next(c for c in native.cases()if c['entry']==int(row['address'],0));body=(ROOT/Path(row['realLink']['lcf']).parent/'caller.bin').read_bytes()
            if row['name']=='WSetDTIMPeriod':case=dict(case,period=1)
            def supported(case,budget,candidate,image=main,ram=wram):
                result=native.run(image,ram,case,0,body=candidate,budget=budget)
                if not result['actualOwnReturn']or not result.get('modelPassed'):raise ValueError('Unsupported prerequisite; zero post-fault/return credit')
            tests=[('bound',case,1)]
            if not index:tests.extend([('source',dict(case,nullSource=True),20000),('output',dict(case,nullOutput=True),20000),('source-capacity',dict(case,length=3),20000)])
            else:
                tests.append(('runtime-word',dict(case,wrongRuntimePointer=True),20000))
                if row['name']=='WSetBssid':tests.append(('source',dict(case,nullSource=True),20000))
                if row['name']=='WSetDTIMPeriod':tests.append(('producer-width',dict(case,period=65536),20000))
            for name,altered,budget in tests:
                for label,candidate in [('original',None),('compiled',body)]:rejected(row['name']+'-'+name+'-'+label,lambda altered=altered,budget=budget,candidate=candidate:supported(altered,budget,candidate),execution)
            for name,image,ram in[('main',bytes([main[0]^1])+main[1:],wram),('wram',main,bytes([wram[0]^1])+wram[1:])]:rejected(row['name']+'-current-'+name,lambda image=image,ram=ram:supported(case,20000,None,image,ram),execution)
            if row['name']=='WSetDTIMPeriod':
                for period in(0,65535):
                    invalid=dict(case,period=period,wrongRuntimePointer=True);original=native.run(main,wram,invalid,0);compiled=native.run(main,wram,invalid,0,body=body)
                    if original!=compiled or not original['actualOwnReturn']or not original['modelPassed']:raise ValueError('Invalid period must return5 before the runtime pointer is used')
                    early_returns.append(dict(original=original,compiled=compiled))
    for index,report in enumerate(reports):validate(index,json.loads(MATCHERS[index].REPORT.read_text()))
    write_json(REPORT,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReports=[dict(path=m.REPORT.relative_to(ROOT).as_posix(),sha256=sha256(m.REPORT))for m in MATCHERS],metadataControls=metadata,metadataControlCount=len(metadata),directPolicyControls=direct,directPolicyControlCount=len(direct),nativePrerequisiteControls=execution,nativeControlCount=len(execution),invalidPeriodBeforePointerUse=early_returns,separateInvalidPeriodActualReturns=2*len(early_returns),acceptedSnapshotExclusion=exclusion,freshSourceOnlyBuildBeforeValidation=True,restoredPositive=True,totalOwnBytes=400,totalOwnFunctions=4,additionalSourceCredit=0))
    print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),metadata=len(metadata),policy=len(direct),native=len(execution))),flush=True)

if __name__=='__main__':main()
