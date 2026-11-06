import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_core126_state76_20261101 as matcher
import arm7_core117_wrong_c_20261101 as wrong_compiler
import link_arm7_bulk_20261030 as original_policy
import compile_arm7_core118_packet176_20261101 as previous_policy
from project import ROOT,sha256,write_json
MATCHER_SHA='15feb72c42fae8d2e076a32a549bceadb5dd51a423a558f10d5ed9fef7743d56'
WRONG_COMPILER_SHA='66ced44dca372cb3cd80d1199b09835020f603ab6251442535cdd0ff3346d386'
CONTROLS=ROOT/'evidence/verification/arm7-core126-state76-controls-20261101.json'
_FRESH=None


def checked(name,digest):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Current state76 input/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA)
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh state76 source-only native/link/input proof differs')
    pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins or {x['path']for x in report['generatorSources']}!=names or len(report['generatorSources'])!=len(names):raise ValueError('Getter full immutable source/input closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    row=report['matches'][0];matcher.compiler.linker.validate_caller_contract(row)
    for name,digest in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[name],row[digest])
    link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256']);trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('State76 deterministic native trace differs')
    return {('arm7','','arm7-main','0x27ea584','arm'):row}


def main():
    global _FRESH
    checked(Path(wrong_compiler.__file__).name,WRONG_COMPILER_SHA);matcher.main();report=json.loads(matcher.REPORT.read_text());_FRESH=report;validate(report);controls=[];policies=[];native_controls=[]
    def rejected(name,action,collection=controls):
        try:action()
        except(ValueError,FileNotFoundError)as error:collection.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False getter proof survived '+name)
    def changed(path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value;validate(bad)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('functions',('newOrdinaryFunctionCount',),2),('bytes',('matchedInitializedBytes',),72),('code',('matchedCodeBytes',),76),('pool',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),76),('data-credit',('originalDataAssemblyOrExtentCredit',),4),('module-match',('wholeModuleLinked',),True),('game-complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),176),('prefix-return',('constructorActualReturnCredit',),352),('pointer-width',('runtimePointerQualification','storageBytes'),8),('policy-disabled',('callerSpecificLinker','exactCallerSourceHashAndFullIdentityRequired'),False),('policy-code',('callerSpecificLinker','sha256'),'0'*64),('old-policy',('callerSpecificLinker','defaultAndEarlierPoliciesUnchanged'),False),('address',('matches',0,'address'),'0x27ea588'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('exact',('matches',0,'exactBytes'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('source-only',('matches',0,'sourceOnlyCompilerInput'),False),('argument',('matches',0,'sourceAbiContract','physicalArgumentWords'),1),('result',('matches',0,'sourceAbiContract','rawReturns'),[10]),('mask',('matches',0,'sourceAbiContract','fields','testedMask'),2),('field-width',('matches',0,'sourceAbiContract','fields','modeHalfwordOffset'),'0x332'),('writes',('matches',0,'sourceAbiContract','ownMemoryWrites'),1),('calls',('matches',0,'sourceAbiContract','ownCalls'),1),('meaning',('matches',0,'sourceAbiContract','historicalPublicMeaningProven'),True),('coverage',('matches',0,'oracle','allOwnInstructionsAndSupportedBranchesVisited'),False),('model',('matches',0,'oracle','independentProducedPointerHalfwordPredicateLeafRegisterAndFlagModel'),False),('raw-state',('matches',0,'oracle','fullRawRegistersFlagsAndAllMappedMemoryAndOrderedReadsCompared'),False),('providers',('matches',0,'oracle','providerReplacements'),['state']),('scene',('matches',0,'oracle','physicalHardwareOrSceneContextProven'),True),('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/no76.o'),('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/no76.json.gz')]
    for name,path,value in changes:rejected(name,lambda path=path,value=value:changed(path,value))
    row=report['matches'][0];modules,unused=matcher.compiler.linker.namespace('')
    for key,value in [('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-wram'),('mode','thumb'),('address','0x27ea588'),('bytes',72),('source','src/arm7/unowned.c'),('sourceSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],sha256='0'*64)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/missing-producer.json'))]:
        bad=copy.deepcopy(row);bad[key]=value;rejected('direct-'+key+'-'+str(value),lambda bad=bad:matcher.compiler.linker.validate(bad,matcher.WORK/'negative-policy'),policies)
    rejected('original-unknown-word-policy',lambda:original_policy.validate(row,matcher.WORK/'original-refusal'),policies);rejected('earlier176-policy',lambda:previous_policy.linker.validate(row,matcher.WORK/'176-refusal'),policies)
    for target in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('wrong-word-'+hex(target),lambda target=target:matcher.compiler.linker.data_binding(row,target,modules),policies)
    main_bytes=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();entry=0x027ea584;original=main_bytes[0xa584:0xa584+76];body=(matcher.WORK/'caller/real-link/caller.bin').read_bytes();case=matcher.native.cases()[0]
    for kind,code in [('original',original),('compiled',body)]:
        rejected(kind+'wrong-descriptor',lambda code=code:matcher.native.run(main_bytes,wram,entry,code,case,19,wrong_descriptor=True),native_controls);value=matcher.native.run(main_bytes,wram,entry,code,case,19,wrong_pointer=True)
        if not value['actualOwnReturn']or value['modelPassed']:raise ValueError('Corrupted pointer escaped immutable-state model')
        native_controls.append(dict(name=kind+'wrong-pointer',actualOwnReturn=True,rejected=True,modelChecks=value['modelChecks'],positiveReturnOrPostStateCredit=0));rejected(kind+'one-instruction-prefix',lambda code=code:matcher.native.run(main_bytes,wram,entry,code,case,19,budget=1),native_controls)
    seed=json.loads((matcher.SOURCE/'profile.json').read_text())['units'][0];text=(ROOT/seed['source']).read_text();wrong=[]
    for name,old,new in [('wrong-mode1-return','case 1:\n        return 10;','case 1:\n        return 11;'),('wrong-bit-mask','& 1) != 0','& 2) != 0')]:
        if old not in text:raise ValueError('Wrong getter source mutation absent')
        folder=matcher.WORK/name;wrong_body,build=wrong_compiler.build(seed,text.replace(old,new),folder,row['realLink']['bindings']);bad=dict(row,source=build['source'],sourceSha256=build['sourceSha256'],object=build['object'],objectSha256=build['objectSha256']);rejected(name+'source-admission',lambda bad=bad:matcher.compiler.linker.validate(bad,folder/'refused'),policies)
        if len(wrong_body)!=76:raise ValueError('Wrong getter escaped complete76-byte code/pool bound')
        records=[];rejects=0
        for index,test in enumerate(matcher.native.cases()):
            value=matcher.native.run(main_bytes,wram,entry,wrong_body,test,index);records.append(dict(case=test,execution=value));rejects+=not value['modelPassed']
        if rejects==0:raise ValueError('Wrong getter escaped independent model')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=folder/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,diagnosticFreshCompilerAndRealLink=build,actualWrongOwnReturns=len(records),independentModelRejections=rejects,sourceAdmissionRejected=True,sourceCredit=0,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),directSourceOwnershipProducerAndDefaultPolicyControls=policies,directPolicyControlCount=len(policies),nativeProducerPointerAndPrefixControls=native_controls,nativeControlCount=len(native_controls),compiledWrongSources=wrong,actualWrongOwnReturns=sum(x['actualWrongOwnReturns']for x in wrong),independentWrongSourceRejections=sum(x['independentModelRejections']for x in wrong),sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,sourceDataOrDenominatorCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),metadataControls=len(controls),policyControls=len(policies),nativeControls=len(native_controls),wrongReturns=result['actualWrongOwnReturns'],modelRejections=result['independentWrongSourceRejections'])),flush=True)
if __name__=='__main__':main()
