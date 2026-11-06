import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_core118_packet176_20261101 as matcher
import arm7_core117_wrong_c_20261101 as wrong_compiler
import link_arm7_bulk_20261030 as original_policy
from project import ROOT,sha256,write_json
MATCHER_SHA='c2da35eed8540724f6d99e8fa9abf385788a4e5ce4a872601e1eb6dbc866531e'
WRONG_COMPILER_SHA='66ced44dca372cb3cd80d1199b09835020f603ab6251442535cdd0ff3346d386'
CONTROLS=ROOT/'evidence/verification/arm7-core118-packet176-controls-20261101.json'
_FRESH=None


def checked(name,digest):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Current packet176 input/product is unavailable or changed')
    return path


def check_products(row,link,trace):
    for name,digest in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[name],row[digest])
    for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
    checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256']);raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Packet176 deterministic trace differs')


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA)
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh packet176 source-only/direct/composed proof differs')
    pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins or {x['path']for x in report['generatorSources']}!=names or len(report['generatorSources'])!=len(names):raise ValueError('Packet176 full immutable input closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    row=report['matches'][0];matcher.compiler.linker.validate_caller_contract(row);check_products(row,row['realLink'],row['oracle']['trace']);connected=report['connectedSourceClosure'];matcher.caller_compiler.linker.validate_caller_contract(connected['caller']);check_products(connected['caller'],connected['realLink'],connected['trace'])
    return {('arm7','','arm7-main','0x27e91bc','arm'):row}


def main():
    global _FRESH
    checked(Path(wrong_compiler.__file__).name,WRONG_COMPILER_SHA);matcher.main();report=json.loads(matcher.REPORT.read_text());_FRESH=report;validate(report);controls=[];policies=[];native_controls=[]
    def rejected(name,action,collection=controls):
        try:action()
        except(ValueError,FileNotFoundError)as error:collection.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False packet176 qualification survived '+name)
    def changed(path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value;validate(bad)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('functions',('newOrdinaryFunctionCount',),2),('bytes',('matchedInitializedBytes',),280),('code',('matchedCodeBytes',),176),('pool',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),176),('data-credit',('originalDataAssemblyOrExtentCredit',),4),('module-match',('wholeModuleLinked',),True),('game-complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),648),('prefix-return',('constructorActualReturnCredit',),1296),('helper-source',('originalHelperDependencies',0,'sourceCredit'),44),('pointer-width',('runtimePointerQualification','storageBytes'),8),('policy-disabled',('callerSpecificLinker','exactCallerSourceHashAndFullIdentityRequired'),False),('policy-code',('callerSpecificLinker','sha256'),'0'*64),('old-policy-modified',('callerSpecificLinker','defaultAndState240PoliciesUnchanged'),False),('address',('matches',0,'address'),'0x27e91c0'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('exact',('matches',0,'exactBytes'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('source-only',('matches',0,'sourceOnlyCompilerInput'),False),('argument',('matches',0,'sourceAbiContract','physicalArgumentWords'),1),('shared-prototype',('matches',0,'sourceAbiContract','rawUnsigned32ArgumentTypesCompatibleWithFrozen104'),False),('full-width',('matches',0,'sourceAbiContract','fullValueThresholdAndFullSecondArgumentZeroPredicate'),False),('raw-results',('matches',0,'sourceAbiContract','rawReturns'),[0]),('meaning',('matches',0,'sourceAbiContract','historicalPublicMeaningProven'),True),('coverage',('matches',0,'oracle','allOwnInstructionsAndSupportedBranchesVisited'),False),('model',('matches',0,'oracle','independentDescriptorInitializationHalfwordPacketAndFlagModel'),False),('raw-state',('matches',0,'oracle','fullRawCpuFlagsFramesMappedMemoryAndOrderedReadsWritesCompared'),False),('providers',('matches',0,'oracle','providerReplacements'),['packet']),('scene',('matches',0,'oracle','physicalHardwareOrSceneContextProven'),True),('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/no176.o'),('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/no176.json.gz'),('connected-source',('connectedSourceClosure','caller','sourceSha256'),'0'*64),('connected-object',('connectedSourceClosure','caller','object'),'work/arm7-bulk-20261030/no104.o'),('connected-trace',('connectedSourceClosure','trace','path'),'work/arm7-bulk-20261030/no104.json.gz'),('connected-credit',('connectedSourceClosure','additionalSourceCredit'),104),('connected-returns',('connectedSourceClosure','freshOriginalAndCompiledCallerReturnsZeroAdditionalCredit'),0),('connected-callee-returns',('connectedSourceClosure','freshCompiled176ScopedReturnsWithOriginalCounterpartZeroAdditionalCredit'),0),('connected-constructor',('connectedSourceClosure','constructorActualReturns'),640)]
    for name,path,value in changes:rejected(name,lambda path=path,value=value:changed(path,value))
    row=report['matches'][0];modules,unused=matcher.compiler.linker.namespace('')
    for key,value in [('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-wram'),('mode','thumb'),('address','0x27e91c0'),('bytes',172),('source','src/arm7/unowned.c'),('sourceSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],sha256='0'*64)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/missing-producer.json'))]:
        bad=copy.deepcopy(row);bad[key]=value;rejected('direct-'+key+'-'+str(value),lambda bad=bad:matcher.compiler.linker.validate(bad,matcher.WORK/'negative-policy'),policies)
    rejected('original-unknown-word-guard',lambda:original_policy.validate(row,matcher.WORK/'original-refusal'),policies);rejected('frozen240-caller-policy-still-refuses176',lambda:matcher.caller_compiler.linker.validate(row,matcher.WORK/'240-refusal'),policies)
    for target in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('outside-qualified-word-'+hex(target),lambda target=target:matcher.compiler.linker.data_binding(row,target,modules),policies)
    main_bytes=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();entry=0x027e91bc;original=main_bytes[0x91bc:0x91bc+176];case=next(c for c in matcher.native.cases()if c['value']==10 and c['writePort']==0 and c['active']==1 and c['selector']==1);body=(matcher.WORK/'caller/real-link/caller.bin').read_bytes()
    for kind,code in [('original',original),('compiled',body)]:
        rejected(kind+'wrong-descriptor',lambda code=code:matcher.native.run(main_bytes,wram,entry,code,case,17,wrong_descriptor=True),native_controls);value=matcher.native.run(main_bytes,wram,entry,code,case,17,wrong_pointer=True)
        if not value['actualOwnReturn']or value['modelPassed']:raise ValueError('Returning wrong pointer escaped packet176 state model')
        native_controls.append(dict(name=kind+'wrong-pointer',actualOwnReturn=True,rejected=True,modelChecks=value['modelChecks'],positiveReturnAndPostStateCredit=0));rejected(kind+'one-owned-instruction-prefix',lambda code=code:matcher.native.run(main_bytes,wram,entry,code,case,17,budget=1),native_controls)
    seed=json.loads((matcher.SOURCE/'profile.json').read_text())['units'][0];text=(ROOT/seed['source']).read_text();wrong=[]
    for name,old,new in [('wrong-threshold','arg0 < 0xAU','arg0 < 0xBU'),('wrong-port-predicate','arg1 != 0','arg1 == 0'),('removed-value-guard','arg0 < 0xAU','0')]:
        if old not in text:raise ValueError('Wrong packet176 source mutation absent')
        folder=matcher.WORK/name;wrong_body,build=wrong_compiler.build(seed,text.replace(old,new),folder,row['realLink']['bindings']);bad=dict(row,source=build['source'],sourceSha256=build['sourceSha256'],object=build['object'],objectSha256=build['objectSha256']);rejected(name+'source-admission',lambda bad=bad:matcher.compiler.linker.validate(bad,folder/'refused'),policies);record=dict(name=name,diagnosticFreshCompilerAndRealLink=build,sourceAdmissionRejected=True,sourceCredit=0)
        if len(wrong_body)==176:
            records=[];rejects=0
            for index,test in enumerate(matcher.native.cases()):
                value=matcher.native.run(main_bytes,wram,entry,wrong_body,test,index);records.append(dict(case=test,execution=value));rejects+=not value['modelPassed']
            if rejects==0:raise ValueError('Wrong packet176 C escaped independent model')
            record.update(actualWrongOwnReturns=len(records),independentModelRejections=rejects,trace=matcher.save_trace(records,folder/'native-records.json.gz'))
        else:record.update(actualWrongOwnReturns=0,supportedWrongExecutionCredit=0,reason='Different full generated extent retained; original code/pool guards are not relaxed')
        wrong.append(record)
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,wrongCompilerSha256=WRONG_COMPILER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),directSourceOwnershipProducerAndDefaultPolicyControls=policies,directPolicyControlCount=len(policies),nativeProducerPointerAndPrefixControls=native_controls,nativeControlCount=len(native_controls),compiledWrongSources=wrong,actualWrongOwnReturns=sum(x['actualWrongOwnReturns']for x in wrong),independentWrongSourceRejections=sum(x.get('independentModelRejections',0)for x in wrong),sourceOnlyFreshDirectAndConnectedCompilationBeforeValidation=True,restoredPositive=True,additionalSourceDataOrExtentCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),metadataControls=len(controls),policyControls=len(policies),nativeControls=len(native_controls),wrongReturns=result['actualWrongOwnReturns'],modelRejections=result['independentWrongSourceRejections'])),flush=True)
if __name__=='__main__':main()
