import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi276_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='b2d826f8db14141f3c4e44574b7aa511c36e46a50863f5a5f1fc20a51d06852d'
CONTROLS=ROOT/'evidence/verification/arm7-main-spi276-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current initializer source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen main SPI source/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete main SPI source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for row in report['matches']:
        for key,hashkey in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[key],row[hashkey])
        for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=matcher.WORK/row['address'][2:]/'real-link';checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256']);trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
        if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Current main SPI trace differs or is not deterministic gzip')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh full source-only link/ROM mapping/native state evidence differs')
    return {('arm7','','arm7-main',row['address'],'arm'):row for row in report['matches']}


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(name,keys,value):
        bad=copy.deepcopy(report);target=bad
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Unqualified main SPI source evidence survived: '+name)
    for name,keys,value in [('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('count',('newOrdinaryFunctionCount',),5),('bytes',('matchedInitializedBytes',),312),('code',('matchedCodeBytes',),276),('literal',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),276),('duplicate-credit',('existingWramImplementationDuplicateByteCredit',),36),('data-credit',('originalDataAssemblyOrExtentCredit',),28),('module-credit',('wholeModuleLinked',),True),('complete-game',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),11356),('rom-offset',('runtimeOwnership','romArm7Offset'),0),('rom-size',('runtimeOwnership','romArm7Bytes'),160024),('main-map',('runtimeOwnership','modules',2,'runtimeBase'),'0x238f894'),('main-source',('runtimeOwnership','modules',2,'sourceImageOffset'),540),('duplicate-source',('runtimeOwnership','duplicateHelper','mainImageOffset'),52852),('duplicate-map',('runtimeOwnership','duplicateHelper','distinctRuntimeModules'),False),('stack-collision',('runtimeOwnership','fixtureStack'),'0x27f5400'),('output-collision',('runtimeOwnership','fixtureOutput'),'0x27e0000'),('stop-collision',('runtimeOwnership','fixtureStop'),'0x27f5554')]:reject(name,keys,value)
    for i in range(4):
        for name,keys,value in [('address',('address',),'0x27f54b4'),('mode',('mode',),'thumb'),('source',('sourceSha256',),'0'*64),('flags',('compilerFlags',),[]),('header',('sourceDependencies',),[]),('exact',('exactBytes',),False),('blob',('originalObjectScaffolding',),True),('arg-count',('sourceAbiContract','physicalArgumentWords'),4),('model',('oracle','independentRegisterHalfwordPollOutputByteAndUntouchedMemoryModel'),False),('raw-state',('oracle','rawRegistersFlagsStackAndMappedMemoryCompared'),False),('provider',('oracle','providerReplacements'),['poll']),('physical',('oracle','physicalPeripheralExecution'),True),('coverage',('oracle','allOwnInstructionsVisited'),False),('nested-credit',('oracle','actualNestedReturns'),1),('scene',('oracle','wholeSceneOrHardwareContextProven'),True),('missing-object',('object',),'work/arm7-bulk-20261030/absent-main-spi.o'),('missing-trace',('oracle','trace','path'),'work/arm7-bulk-20261030/absent-main-spi.json.gz')]:reject(str(i)+'-'+name,('matches',i)+keys,value)
    reject('word-return-compatibility',('matches',3,'sourceAbiContract','legacyCallerDeclarationCompatible'),False);reject('raw-word-view',('matches',3,'sourceAbiContract','outputRawAddressWordReturnView'),False);reject('historical-return-meaning',('matches',3,'sourceAbiContract','historicalPublicReturnMeaningProven'),True);reject('output-width',('matches',3,'sourceAbiContract','outputStoreWidth'),2)
    seeds=json.loads((matcher.SOURCE/'profile.json').read_text())['units'];original=(ROOT/seeds[0]['binary']).read_bytes();wrong=[]
    definitions=[('wrong-command-six',0,'[0] = 6;','[0] = 7;',81),('unmasked-transfer',1,'(u8)selector','(u16)selector',2331),('wrong-command-four',2,'[0] = 4;','[0] = 3;',81),('wrong-output-byte',3,'*((u8 *)destination) =','((u8 *)destination)[1] =',244)]
    for name,index,old,new,expected in definitions:
        seed=seeds[index];source_text=(ROOT/seed['source']).read_text();assert old in source_text;source=ROOT/('generated/arm7-main-spi276-controls-20261101/'+name+'/'+Path(seed['source']).name);source.parent.mkdir(parents=True,exist_ok=True);header=ROOT/seed['sourceDependencies'][0]['path'];(source.parent/header.name).write_bytes(header.read_bytes());source_text=source_text.replace(source_text.splitlines()[0],'#include "'+header.name+'"');source.write_text(source_text.replace(old,new),encoding='utf-8');row,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if comparison.get('exactLinkedBytes'):raise ValueError('Wrong main SPI C unexpectedly matched')
        records=[];rejections=0;entry=int(seed['address'],0)
        for n,case in enumerate(matcher.native.cases(entry)):
            if index==3 and n%6==5:continue
            value=matcher.native.execute(original,entry,body,case,n);records.append(value);rejections+=not value['modelPassed']
        if rejections!=expected:raise ValueError('Wrong main SPI independent rejection count differs '+name+':'+str(rejections))
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,compilerResult=row,genuineLinkComparison=comparison,actualOwnReturns=len(records),independentModelRejections=rejections,outputLastPageByteExcludedFromWrongPlusOneDomain=index==3,originalTailFallback=False,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    for row in report['matches']:
        entry=int(row['address'],0);body=(matcher.WORK/row['address'][2:]/'real-link/caller.bin').read_bytes();value=matcher.native.execute(original,entry,body,matcher.native.cases(entry)[0],0,budget=1,allow_no_return=True)
        if value['actualOwnReturn']:raise ValueError('Prefix gained return credit')
        controls.append(dict(name='prefix-'+row['address'],rejected=True,execution=value))
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=2791,independentWrongSourceRejections=2737,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=2791,modelRejections=2737)),flush=True)
if __name__=='__main__':main()
