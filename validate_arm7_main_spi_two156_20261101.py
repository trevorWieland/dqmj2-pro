import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi_two156_20261101 as matcher
from project import ROOT,sha256,write_json
MATCHER_SHA='4c1187328544c3291054b59d0b0eeaad3ebcc5f813353c1e853a4dd3deaea461'
CONTROLS=ROOT/'evidence/verification/arm7-main-spi-two156-controls-20261101.json'
_FRESH=None


def checked(name,digest):
    p=(ROOT/name).resolve()
    if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=digest:raise ValueError('Current two-byte reader source/product missing or changed')
    return p


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen two-byte reader input closure differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Full two-byte reader source closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    row=report['matches'][0]
    for name,digest in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[name],row[digest])
    for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
    link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256']);trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Two-byte reader trace changed or nonzero mtime')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only two-byte reader/link/frame/full-state model differs')
    return {('arm7','','arm7-main','0x27f5bf4','arm'):row}


def main():
    global _FRESH
    matcher.main();report=json.loads(matcher.REPORT.read_text());_FRESH=report;validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False two-byte reader proof survived '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('functions',('newOrdinaryFunctionCount',),2),('bytes',('matchedInitializedBytes',),148),('code',('matchedCodeBytes',),156),('pool',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),156),('data',('originalDataAssemblyOrExtentCredit',),8),('module-match',('wholeModuleLinked',),True),('game-complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),795),('address',('matches',0,'address'),'0x27f5bf8'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('header',('matches',0,'sourceDependencies'),[]),('exact',('matches',0,'exactBytes'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('source-only',('matches',0,'sourceOnlyCompilerInput'),False),('argument',('matches',0,'sourceAbiContract','physicalArgumentWords'),2),('return-word',('matches',0,'sourceAbiContract','rawIncomingAddressWordReturned'),False),('command',('matches',0,'sourceAbiContract','fixedCommand'),3),('output-store',('matches',0,'sourceAbiContract','outputStoreWidth'),2),('output-bytes',('matches',0,'sourceAbiContract','outputBytes'),1),('receive-width',('matches',0,'sourceAbiContract','receivedHalfwordBits'),8),('frame-size',('matches',0,'sourceAbiContract','privateFrameBytes'),0),('r3-argument',('matches',0,'sourceAbiContract','preservedScratchR3IsPaddingNotASecondArgument'),False),('meaning',('matches',0,'sourceAbiContract','historicalPublicDeviceMeaningProven'),True),('coverage',('matches',0,'oracle','allOwnInstructionsVisited'),False),('model',('matches',0,'oracle','independentHalfwordReceiveTwoByteOutputAndR3LrFrameModel'),False),('raw-state',('matches',0,'oracle','fullRawRegistersFlagsAndMappedRamStackOutputIoCompared'),False),('read-order',('matches',0,'oracle','orderedAllReadsAndWritesCompared'),False),('providers',('matches',0,'oracle','providerReplacements'),['SPI']),('hardware',('matches',0,'oracle','physicalPeripheralExecution'),True),('scene',('matches',0,'oracle','hardwareOrSceneContextProven'),True),('busy-return',('matches',0,'oracle','unsupported',0,'execution','actualOwnReturn'),True),('busy-error',('matches',0,'oracle','unsupported',0,'supportedErrorPathCredit'),1),('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/no-two.o'),('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/no-two.json.gz')]
    for name,path,value in changes:reject(name,path,value)
    seed=json.loads((matcher.SOURCE/'profile.json').read_text())['unit'];original=(ROOT/seed['binary']).read_bytes();text=(ROOT/seed['source']).read_text();wrong=[]
    for name,old,new in [('wrong-command','[0]=0x9f;','[0]=0x9e;'),('wrong-final-control','[0]=0x8100;','[0]=0x8900;')]:
        if old not in text:raise ValueError('Wrong two-byte reader source mutation absent')
        folder=ROOT/('generated/arm7-two156-controls/'+name);folder.mkdir(parents=True,exist_ok=True);header=folder/'native_spi_types.h';header.write_bytes((ROOT/seed['sourceDependencies'][0]['path']).read_bytes());source=folder/'native.c';source.write_text(text.replace(old,new),encoding='utf-8');wrong_seed=dict(seed,sourceDependencies=[dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header))]);row,comparison,body=matcher.compiler.compile_unit(wrong_seed,source,matcher.WORK/name,strict=False)
        if len(body)!=156 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong reader matched or escaped complete extent')
        rejected=0;records=[]
        for index,case in enumerate(matcher.native.cases()):
            value=matcher.native.execute(original,body,case,index);records.append(value);rejected+=not value['modelPassed']
        if rejected!=795:raise ValueError('Wrong two-byte reader source effect rejection differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,source=row,genuineLinkComparison=comparison,actualOwnReturns=len(records),independentModelRejections=rejected,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    body=(matcher.WORK/'caller/real-link/caller.bin').read_bytes();value=matcher.native.execute(original,body,matcher.native.cases()[0],0,budget=1,allow_no_return=True)
    if value['actualOwnReturn']or value['actualNestedReturns']:raise ValueError('Frame-save prefix gained return credit')
    controls.append(dict(name='one-instruction-prefix',rejected=True,execution=value));validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=1590,independentWrongSourceRejections=1590,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=1590,modelRejections=1590)),flush=True)
if __name__=='__main__':main()
