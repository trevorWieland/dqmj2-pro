import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_pxi_retry64_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='cd77dd2bc60f1f2c1b6f5bbd2ee53a9e209fc499ca15570929397c148984aa68'
CONTROLS=ROOT/'evidence/verification/arm7-main-pxi-retry64-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current initializer source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen retry source/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete retry source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for dependency,rows in [(False,report['matches']),(True,report['existingSourceDependencies'])]:
        for row in rows:
            for key,hashkey in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[key],row[hashkey])
            for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
            link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=(matcher.WORK/'dependencies'/row['address'][2:]if dependency else matcher.WORK/'caller')/'real-link';checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256'])
            if not dependency:
                trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
                if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Current retry trace differs or is not deterministic gzip')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only three-unit link/native/IRQ/retry evidence differs')
    return {('arm7','','arm7-main','0x27f6074','arm'):report['matches'][0]}


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Unqualified retry source proof survived '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('count',('newOrdinaryFunctionCount',),3),('bytes',('matchedInitializedBytes',),216),('code',('matchedCodeBytes',),216),('literal',('generatedLiteralBytes',),4),('denominator',('initializedDenominatorDelta',),64),('data-credit',('originalDataAssemblyOrExtentCredit',),4),('module-credit',('wholeModuleLinked',),True),('complete-game',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),7642),('dependency-credit',('existingSourceBytesSeparateZeroCredit',),0),('source-closure',('existingSourceDependencies',),[]),('address',('matches',0,'address'),'0x27f6078'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('exact',('matches',0,'exactBytes'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('arguments',('matches',0,'sourceAbiContract','physicalArgumentWords'),3),('packer-args',('matches',0,'sourceAbiContract','packerArgumentWords'),4),('tag',('matches',0,'sourceAbiContract','fixedTag'),4),('error',('matches',0,'sourceAbiContract','fixedError'),1),('signed-retry',('matches',0,'sourceAbiContract','retryWhileSignedResultNegative'),False),('public-meaning',('matches',0,'sourceAbiContract','historicalPublicMeaningProven'),True),('model',('matches',0,'oracle','independentWordPacketStackFramesRetryOrderAndPortModel'),False),('raw-state',('matches',0,'oracle','rawRegistersFlagsStackModeAndMappedMemoryCompared'),False),('source-chain',('matches',0,'oracle','fullFreshSourceCallerPackerSender'),False),('irq-chain',('matches',0,'oracle','actualNativeIrqCodeRetained'),False),('coverage',('matches',0,'oracle','completeOwnAndDependencyInstructionsVisited'),False),('packer-returns',('matches',0,'oracle','sourcePackerReturnsSeparateZeroCredit'),1322),('sender-returns',('matches',0,'oracle','sourceSenderReturnsSeparateZeroCredit'),1322),('irq-returns',('matches',0,'oracle','originalIrqReturnsSeparateZeroCredit'),0),('providers',('matches',0,'oracle','providerReplacements'),['irq']),('physical',('matches',0,'oracle','physicalPeripheralExecution'),True),('volatile-input-scope',('matches',0,'oracle','stableFifoStatusWithinEachAttempt'),False),('mode-scope',('matches',0,'oracle','privilegedSystemModeAndIrqFiqMasksTested'),False),('scene',('matches',0,'oracle','wholeSceneOrHardwareContextProven'),True),('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/absent-retry.o'),('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/absent-retry.json.gz'),('binding',('nativeSymbols','native_host_arm7_arm_037fe410'),'0x37fe448')]
    for name,path,value in changes:reject(name,path,value)
    for i in range(2):reject('callee-source-'+str(i),('existingSourceDependencies',i,'sourceSha256'),'0'*64);reject('callee-credit-'+str(i),('existingSourceDependencies',i,'sourceCredit'),1)
    profile=json.loads((matcher.SOURCE/'profile.json').read_text());seed=profile['newUnit'];main=(ROOT/seed['binary']).read_bytes();wram=(ROOT/profile['dependencies'][0]['binary']).read_bytes();pack=(matcher.WORK/'dependencies'/profile['dependencies'][0]['address'][2:]/'real-link/caller.bin').read_bytes();send=(matcher.WORK/'dependencies'/profile['dependencies'][1]['address'][2:]/'real-link/caller.bin').read_bytes();text=(ROOT/seed['source']).read_text();wrong=[]
    for name,old,new,expected in [('drop-selector-bit-six','0x7f00','0x3f00',308),('wrong-retry-sign','result < 0','result > 0',528)]:
        assert old in text;source=ROOT/('generated/arm7-pxi-retry64-controls/'+name+'/native.c');source.parent.mkdir(parents=True,exist_ok=True);source.write_text(text.replace(old,new),encoding='utf-8');row,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if len(body)!=64 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong retry source matched or escaped full extent')
        records=[];rejected=0
        for index,case in enumerate(matcher.native.cases()):
            value=matcher.native.execute(main,wram,body,pack,send,case,index);records.append(value);rejected+=not value['modelPassed']
        if rejected!=expected:raise ValueError('Wrong retry independent rejection count differs '+name+':'+str(rejected))
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,compilerResult=row,genuineLinkComparison=comparison,actualOwnReturns=661,independentModelRejections=rejected,freshSourcePackerSenderAndOriginalIrqRetained=True,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    own=(matcher.WORK/'caller/real-link/caller.bin').read_bytes();value=matcher.native.execute(main,wram,own,pack,send,matcher.native.cases()[0],0,budget=1,allow_no_return=True)
    if value['actualOwnReturn']or value['actualPackerReturns']or value['actualSenderReturns']or value['actualIrqReturns']:raise ValueError('Prefix gained a return')
    controls.append(dict(name='one-instruction-prefix',rejected=True,execution=value));validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=1322,independentWrongSourceRejections=836,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=1322,modelRejections=836)),flush=True)
if __name__=='__main__':main()
