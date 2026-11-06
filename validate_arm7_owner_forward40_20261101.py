import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_owner_forward40_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='51836c6f0769ef3e9d562d78eb2592a00d557e1137778b81970dd7a74ff4eef3'
CONTROLS=ROOT/'evidence/verification/arm7-owner-forward40-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current initializer source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA)
    pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen initializer generator/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete initializer source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    row=report['matches'][0]
    checked(row['source'],row['sourceSha256']);checked(row['compiler'],row['compilerSha256']);checked(row['object'],row['objectSha256'])
    link=row['realLink'];checked(link['lcf'],link['lcfSha256'])
    checked(matcher.WORK/'caller/real-link/linked.elf',link['linkedElfSha256'])
    checked(matcher.WORK/'caller/real-link/caller.bin',row['targetSha256'])
    trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Current initializer trace differs or is not deterministic gzip')
    if _FRESH is None:
        matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only link/native execution/coverage/effect evidence differs')
    return {('arm7','','arm7-wram','0x3806390','arm'):row}


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(name,keys,value):
        bad=copy.deepcopy(report);target=bad
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid owner-forward evidence survived: '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-main'),('address',('matches',0,'address'),'0x3806394'),('mode',('matches',0,'mode'),'thumb'),('size',('matches',0,'bytes'),36),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('count',('newOrdinaryFunctionCount',),2),('bytes',('matchedInitializedBytes',),80),('code',('matchedCodeBytes',),36),('literal',('generatedLiteralBytes',),4),('denominator',('initializedDenominatorDelta',),40),('helper-credit',('originalDataHelperAssemblyOrExtentCredit',),124),('module-credit',('wholeModuleLinked',),True),('whole-source',('sourceReconstructionComplete',),True),('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('blob',('matches',0,'originalObjectScaffolding'),True),('exact',('matches',0,'exactAfterDeclaredRelocation'),False),
        ('owner-arg-erased',('matches',0,'sourceAbiContract','physicalArgumentWords'),1),('owner-not-forwarded',('matches',0,'sourceAbiContract','firstWordForwardedToQualifiedTailChain'),False),('prefix',('matches',0,'sourceAbiContract','contextPrefixBytes'),32),('ordinary-volatile',('matches',0,'sourceAbiContract','ordinaryRamNotVolatile'),False),
        ('model',('matches',0,'oracle','independentSharedPageOwnerCompareAndOrderedLockStoreModel'),False),('unchecked-machine',('matches',0,'oracle','rawRegistersFlagsStackModeAndMappedMemoryCompared'),False),('returns',('matches',0,'oracle','actualOriginalAndCompiledReturns'),3360),('tail-returns',('matches',0,'oracle','actualTailChainReturnsSeparateZeroCredit'),1680),('irq-returns',('matches',0,'oracle','actualOriginalIrqReturnsSeparateZeroCredit'),0),('callback-returns',('matches',0,'oracle','actualOriginalCallbackReturnsSeparateZeroCredit'),0),('providers',('matches',0,'oracle','providerReplacements'),['unlock']),('native-chain',('matches',0,'oracle','allNativeTailCallbackAndIrqCodeRetained'),False),
        ('tail-entry',('matches',0,'oracle','tailWitness','qualifyingEntry'),'0x37fbb7c'),('tail-forward',('matches',0,'oracle','tailWitness','forwardingEntry'),'0x37fbb84'),('common-entry',('matches',0,'oracle','tailWitness','actualCommonEntry'),'0x37fba1c'),('callback',('matches',0,'oracle','tailWitness','fixedCallback'),'0x37fbba4'),('fixed-flag',('matches',0,'oracle','tailWitness','fixedFlag'),0),('owner-offset',('matches',0,'oracle','tailWitness','ownerFieldOffset'),0),('owner-width',('matches',0,'oracle','tailWitness','ownerFieldReadWidth'),4),('owner-narrowing',('matches',0,'oracle','tailWitness','callerWordComparedWithoutNarrowing'),False),('data-credit',('matches',0,'oracle','tailWitness','calleeSourceDataOrExtentCredit'),8),('unexecuted-helper-branch',('matches',0,'oracle','tailWitness','completeCommonHelperOtherBranchesProven'),True),('scene',('matches',0,'oracle','wholeSceneOrHardwareContextProven'),True),('binding',('nativeSymbols','native_host_arm7_arm_037fbb78'),'0x37fbb58'),('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/absent-owner.o'),('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/absent-owner.json.gz')]
    for name,keys,value in changes:reject(name,keys,value)
    seed=json.loads((matcher.SOURCE/'seed.json').read_text());text=(ROOT/seed['source']).read_text();original=(ROOT/seed['binary']).read_bytes();wrong=[]
    definitions=[('erased-owner',text.replace('native_host_arm7_arm_037fbb78(u32);','native_host_arm7_arm_037fbb78(void);').replace('native_host_arm7_arm_037fbb78(owner);','native_host_arm7_arm_037fbb78();'),240),('inverted-state',text.replace('context->state == 0','context->state != 0'),840)]
    for name,source_text,expected in definitions:
        source=ROOT/('generated/arm7-owner-forward40-controls-20261101/'+name+'/native_arm7_wram_03806390.c');source.parent.mkdir(parents=True,exist_ok=True);source.write_text(source_text,encoding='utf-8')
        bad,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if len(body)!=40 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong owner caller matched or escaped full extent')
        records=[];rejections=0
        for index,case in enumerate(matcher.native.cases()):
            value=matcher.native.execute(original,body,case,index);records.append(value);rejections+=not value['modelPassed']
        if rejections!=expected:raise ValueError('Wrong owner caller independent rejection count differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
        wrong.append(dict(name=name,compilerResult=bad,genuineLinkComparison=comparison,actualOwnReturns=840,independentModelRejections=rejections,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    value=matcher.native.execute(original,(matcher.WORK/'caller/real-link/caller.bin').read_bytes(),matcher.native.cases()[0],0,budget=1,allow_no_return=True)
    if value['actualOwnReturn']or value['actualIrqReturns']or value['actualTailChainReturns']:raise ValueError('Prefix acquired a return')
    controls.append(dict(name='bounded-exhaustion',rejected=True,reason='Prefix did not return; post-state excluded'));validate(json.loads(matcher.REPORT.read_text()))
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=1680,independentWrongSourceRejections=1080,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),metadataControls=len(controls),wrongOwnReturns=1680,modelRejections=1080)),flush=True)
if __name__=='__main__':main()
