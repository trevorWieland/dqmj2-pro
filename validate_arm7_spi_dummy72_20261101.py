import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_spi_dummy72_20261101 as matcher
from project import ROOT,sha256,write_json
MATCHER_SHA='6474412b7e286ee96e27209bf825ac7f8fea2d480e7a560b32ec9af8b57082d1'
CONTROLS=ROOT/'evidence/verification/arm7-spi-dummy72-controls-20261101.json'
_FRESH=None


def checked(name,digest):
    p=(ROOT/name).resolve()
    if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=digest:raise ValueError('Required current dummy-pair source/product missing or changed')
    return p


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen dummy-pair inputs differ')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Full current dummy-pair closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for row in report['matches']:
        for name,digest in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[name],row[digest])
        for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256']);trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
        if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Dummy-pair trace changed or nonzero gzip mtime')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only complete-unit link/native model differs')
    return {('arm7','','arm7-wram',x['address'],'arm'):x for x in report['matches']}


def main():
    global _FRESH
    matcher.main();report=json.loads(matcher.REPORT.read_text());_FRESH=report;validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid dummy-pair claim survived '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-main'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('functions',('newOrdinaryFunctionCount',),1),('bytes',('matchedInitializedBytes',),36),('code',('matchedCodeBytes',),72),('pool',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),72),('data',('originalDataAssemblyOrExtentCredit',),8),('module-match',('wholeModuleLinked',),True),('game-complete',('sourceReconstructionComplete',),True),('family-novelty',('newImplementationFamilyCount',),2),('return-count',('totalActualOwnReturns',),3178),('ownership',('runtimeOwnership','romArm7Offset'),0),('address',('matches',0,'address'),'0x3803e40'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('header',('matches',0,'sourceDependencies'),[]),('exact',('matches',0,'exactBytes'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('source-only',('matches',0,'sourceOnlyCompilerInput'),False),('args',('matches',0,'sourceAbiContract','physicalArgumentWords'),1),('return-width',('matches',0,'sourceAbiContract','rawReturnBits'),8),('zero-extension',('matches',0,'sourceAbiContract','zeroExtendedControlHalfword'),False),('ports',('matches',0,'sourceAbiContract','volatileHalfwordPorts'),[]),('busy-bit',('matches',0,'sourceAbiContract','busyBit'),64),('meaning',('matches',0,'sourceAbiContract','historicalPublicDevicePolicyMeaningProven'),True),('stored-offset',('matches',0,'physicalSource','inputImageOffset'),0),('stored-rom-offset',('matches',0,'physicalSource','romOffset'),0),('stored-module',('matches',0,'physicalSource','module'),'arm7-main'),('model',('matches',0,'oracle','independentFullHalfwordPollModel'),False),('coverage',('matches',0,'oracle','allOwnInstructionsVisited'),False),('raw-state',('matches',0,'oracle','rawRegistersFlagsStackAndMappedMemoryCompared'),False),('providers',('matches',0,'oracle','providerReplacements'),['SPI']),('physical-hardware',('matches',0,'oracle','physicalPeripheralExecution'),True),('hardware-context',('matches',0,'oracle','wholeHardwareContextProven'),True),('busy-return',('matches',0,'oracle','unsupported',0,'execution','actualOwnReturn'),True),('busy-error',('matches',0,'oracle','unsupported',0,'supportedErrorPathCredit'),1),('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/no-dummy.o'),('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/no-dummy.json.gz')]
    for name,path,value in changes:reject(name,path,value)
    profile=json.loads((matcher.SOURCE/'profile.json').read_text());original=(ROOT/profile['units'][0]['binary']).read_bytes();wrong=[]
    for seed in profile['units']:
        name='wrong-zero-'+seed['address'][2:];text=(ROOT/seed['source']).read_text();old='[0] = 0;';new='[0] = 1;'
        if old not in text:raise ValueError('Wrong dummy source mutation absent')
        source=ROOT/('generated/arm7-dummy72-controls/'+name+'/native.c');source.parent.mkdir(parents=True,exist_ok=True);header=ROOT/seed['sourceDependencies'][0]['path'];(source.parent/header.name).write_bytes(header.read_bytes());source.write_text(text.replace(old,new),encoding='utf-8');row,comparison,body=matcher.compiler.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if len(body)!=36 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong zero transfer matched or escaped complete extent')
        rejected=0;records=[]
        for index,case in enumerate(matcher.native.cases()):
            value=matcher.native.execute(original,int(seed['address'],0),body,case,index);records.append(value);rejected+=not value['modelPassed']
        if rejected!=795:raise ValueError('Wrong dummy source effect rejection count differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,source=row,genuineLinkComparison=comparison,actualOwnReturns=len(records),independentModelRejections=rejected,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    for seed in profile['units']:
        address=int(seed['address'],0);body=(matcher.WORK/seed['address'][2:]/'real-link/caller.bin').read_bytes();value=matcher.native.execute(original,address,body,matcher.native.cases()[0],0,budget=1,allow_no_return=True)
        if value['actualOwnReturn']or value['actualNestedReturns']:raise ValueError('Dummy prefix gained a return')
        controls.append(dict(name='one-instruction-prefix-'+seed['address'],rejected=True,execution=value))
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=1590,independentWrongSourceRejections=1590,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=1590,modelRejections=1590)),flush=True)
if __name__=='__main__':main()
