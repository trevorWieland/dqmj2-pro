import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_core117_state240_20261101 as matcher
import arm7_core117_wrong_c_20261101 as wrong_compiler
import link_arm7_bulk_20261030 as original_policy
from project import ROOT,sha256,write_json
MATCHER_SHA='9c2eabf441ef31081ddd0de5b6159f69b839ada5be5dfae5e93157a71fbe857d'
WRONG_COMPILER_SHA='66ced44dca372cb3cd80d1199b09835020f603ab6251442535cdd0ff3346d386'
CONTROLS=ROOT/'evidence/verification/arm7-core117-state240-controls-20261101.json'
_FRESH=None


def checked(name,digest):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Current state240 source/product is unavailable or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA)
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only state240/provenance/native-model proof differs')
    pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins or {x['path']for x in report['generatorSources']}!=names or len(report['generatorSources'])!=len(names):raise ValueError('State240 full generator/source closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for row in report['matches']:
        matcher.compiler.linker.validate_caller_contract(row)
        for name,digest in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[name],row[digest])
        for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256']);trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
        if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('State240 native records or deterministic timestamp changed')
    return {('arm7','','arm7-main',row['address'],'arm'):row for row in report['matches']}


def main():
    global _FRESH
    checked(Path(wrong_compiler.__file__).name,WRONG_COMPILER_SHA);matcher.main();report=json.loads(matcher.REPORT.read_text());_FRESH=report;validate(report);controls=[];policies=[];native_controls=[]
    def rejected(name,action,collection=controls):
        try:action()
        except(ValueError,FileNotFoundError)as error:collection.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False state240 qualification survived '+name)
    def changed(path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value;validate(bad)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('functions',('newOrdinaryFunctionCount',),3),('bytes',('matchedInitializedBytes',),292),('code',('matchedCodeBytes',),240),('pool',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),52),('pointer-data-credit',('originalDataAssemblyOrExtentCredit',),4),('module-match',('wholeModuleLinked',),True),('game-complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),1528),('prefix-return',('constructorActualReturnCredit',),976),('helper-overlap',('overlappingTailReturnEventsIncluded',),0),('helper-source',('originalHelperDependencies',0,'sourceCredit'),176),('scope-credit',('originalGapQualification','sourceCredit'),52),('scope-config',('originalGapQualification','configAndDenominatorUnchanged'),False),('pointer-width',('runtimePointerQualification','storageBytes'),8),('source-guard-disabled',('callerSpecificLinker','sourceIdentityAndSourceHashGated'),False),('linker-guard-code',('callerSpecificLinker','sha256'),'0'*64)]
    for index in range(2):
        changes.extend([(str(index)+'address',('matches',index,'address'),'0x27e9c5c'),(str(index)+'mode',('matches',index,'mode'),'thumb'),(str(index)+'source',('matches',index,'sourceSha256'),'0'*64),(str(index)+'flags',('matches',index,'compilerFlags'),[]),(str(index)+'exact',('matches',index,'exactBytes'),False),(str(index)+'blob',('matches',index,'originalObjectScaffolding'),True),(str(index)+'source-only',('matches',index,'sourceOnlyCompilerInput'),False),(str(index)+'bss-ownership',('matches',index,'sourceAbiContract','pointerIsExternalDescriptorProducedStorageNotModuleBss'),False),(str(index)+'argument',('matches',index,'sourceAbiContract','physicalArgumentWords'),2),(str(index)+'coverage',('matches',index,'oracle','allOwnInstructionsAndBranchesVisited'),False),(str(index)+'model',('matches',index,'oracle','independentStatePortStoreFlagAndOriginalHelperModel'),False),(str(index)+'raw-state',('matches',index,'oracle','fullRawCpuFlagsFramesAllMappedMemoryAndOrderedReadsWritesCompared'),False),(str(index)+'providers',('matches',index,'oracle','providerReplacements'),['hardware']),(str(index)+'meaning',('matches',index,'sourceAbiContract','historicalPublicMeaningProven'),True),(str(index)+'scene',('matches',index,'oracle','physicalHardwareOrSceneContextProven'),True),(str(index)+'missing-object',('matches',index,'object'),'work/arm7-bulk-20261030/no-state.o'),(str(index)+'missing-trace',('matches',index,'oracle','trace','path'),'work/arm7-bulk-20261030/no-state.json.gz')])
    for name,path,value in changes:rejected(name,lambda path=path,value=value:changed(path,value))
    modules,functions=matcher.compiler.linker.namespace('')
    for index,row in enumerate(report['matches']):
        for key,value in [('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-wram'),('mode','thumb'),('address',hex(int(row['address'],0)+4)),('bytes',row['bytes']-4),('source','src/arm7/unknown.c'),('sourceSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],sha256='0'*64)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/no-pointer.json'))]:
            bad=copy.deepcopy(row);bad[key]=value;rejected(str(index)+'direct-policy-'+key+'-'+str(value),lambda bad=bad:matcher.compiler.linker.validate(bad,matcher.WORK/'negative-policy'),policies)
        rejected(str(index)+'original-unqualified-data-refusal',lambda row=row:original_policy.validate(row,matcher.WORK/('original-refusal-'+str(index))),policies)
        for target in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected(str(index)+'wrong-runtime-word-'+hex(target),lambda target=target,row=row:matcher.compiler.linker.data_binding(row,target,modules),policies)
    main_bytes=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();seed=json.loads((matcher.SOURCE/'profile.json').read_text())['units'][0];entry=int(seed['address'],0);original=main_bytes[entry-matcher.native.MAIN:entry-matcher.native.MAIN+104];case=next(c for c in matcher.native.cases(entry)if c['value']==1 and c['mode']==0)
    for kind in('original','compiled'):
        body=original if kind=='original'else(matcher.WORK/seed['address'][2:]/'real-link/caller.bin').read_bytes()
        rejected(kind+'wrong-incoming-descriptor',lambda body=body:matcher.native.run(main_bytes,wram,entry,body,case,71,wrong_descriptor=True),native_controls)
        value=matcher.native.run(main_bytes,wram,entry,body,case,71,wrong_pointer=True)
        if not value['actualOwnReturn']or value['modelPassed']:raise ValueError('Corrupted produced pointer escaped independent state/write model')
        native_controls.append(dict(name=kind+'returning-wrong-pointer',actualOwnReturn=True,rejected=True,modelChecks=value['modelChecks'],returnCredit=0,positivePostStateCredit=0))
    for row in report['matches']:
        address=int(row['address'],0);body=(matcher.WORK/row['address'][2:]/'real-link/caller.bin').read_bytes();test=matcher.native.cases(address)[0]
        for kind,code in [('original',main_bytes[address-matcher.native.MAIN:address-matcher.native.MAIN+row['bytes']]),('compiled',body)]:
            rejected(row['address']+'-'+kind+'one-owned-instruction-prefix',lambda address=address,code=code,test=test:matcher.native.run(main_bytes,wram,address,code,test,0,budget=1),native_controls)
    text=(ROOT/seed['source']).read_text();wrong=[]
    for name,old,new in [('inverted-value-predicate','(arg0 != 0)','(arg0 == 0)'),('removed-value-guard','(arg0 != 0)','(1)'),('wrong-set-mask','|= 0x40;','|= 0x20;'),('wrong-mode-predicate','u16 *, 0x12) != 1','u16 *, 0x12) != 2')]:
        if old not in text:raise ValueError('Wrong-C guard mutation absent')
        folder=matcher.WORK/name;body,build=wrong_compiler.build(seed,text.replace(old,new),folder,report['matches'][0]['realLink']['bindings']);bad=dict(report['matches'][0],source=build['source'],sourceSha256=build['sourceSha256'],object=build['object'],objectSha256=build['objectSha256']);rejected(name+'source-admission',lambda bad=bad:matcher.compiler.linker.validate(bad,folder/'refused'),policies);record=dict(name=name,diagnosticFreshCompilerAndRealLink=build,sourceAdmissionRejected=True,sourceCredit=0)
        if len(body)==104:
            records=[];rejects=0
            for index,test in enumerate(matcher.native.cases(entry)):
                value=matcher.native.run(main_bytes,wram,entry,body,test,index);records.append(dict(case=test,execution=value));rejects+=not value['modelPassed']
            if rejects==0:raise ValueError('Wrong predicate escaped independent model')
            raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=folder/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));record.update(actualWrongOwnReturns=len(records),independentModelRejections=rejects,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0))
        else:record.update(actualWrongOwnReturns=0,supportedWrongExecutionCredit=0,reason='Different complete generated extent retained as diagnostic; original code/pool boundaries are not relaxed')
        wrong.append(record)
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,wrongCompilerSha256=WRONG_COMPILER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),directOwnershipSourceProducerAndOriginalPolicyControls=policies,directPolicyControlCount=len(policies),nativeProducerAndPointerControls=native_controls,nativeControlCount=len(native_controls),compiledWrongSources=wrong,actualWrongOwnReturns=sum(x['actualWrongOwnReturns']for x in wrong),independentWrongSourceRejections=sum(x.get('independentModelRejections',0)for x in wrong),sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceDataOrExtentCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),metadataControls=len(controls),policyControls=len(policies),nativeControls=len(native_controls),wrongReturns=result['actualWrongOwnReturns'],modelRejections=result['independentWrongSourceRejections'])),flush=True)
if __name__=='__main__':main()
