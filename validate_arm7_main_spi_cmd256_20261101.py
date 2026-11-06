import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi_cmd256_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='e74ded16e70b4a5ac752e7543fdbc0a025b4aa6768fe6cec539bbb10fc292607'
CONTROLS=ROOT/'evidence/verification/arm7-main-spi-cmd256-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current initializer source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen fixed-command source/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete fixed-command source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for row in report['matches']:
        for key,hashkey in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[key],row[hashkey])
        for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=matcher.WORK/row['address'][2:]/'real-link';checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256']);trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
        if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Current fixed-command trace differs or is not deterministic gzip')
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
        else:raise ValueError('Unqualified fixed-command proof survived '+name)
    for name,path,value in [('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('count',('newOrdinaryFunctionCount',),8),('bytes',('matchedInitializedBytes',),512),('code',('matchedCodeBytes',),256),('literal',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),256),('family-novelty',('newImplementationFamilyNoveltyCredit',),4),('data-credit',('originalDataAssemblyOrExtentCredit',),32),('whole-module',('wholeModuleLinked',),True),('complete-game',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),1296),('main-source',('runtimeOwnership','modules',2,'sourceImageOffset'),540),('main-target',('runtimeOwnership','modules',2,'runtimeBase'),'0x37f8000'),('stack',('runtimeOwnership','fixtureStack'),'0x27f5b34')]:reject(name,path,value)
    for i in range(4):
        for name,path,value in [('address',('address',),'0x27f5b38'),('mode',('mode',),'thumb'),('source',('sourceSha256',),'0'*64),('flags',('compilerFlags',),[]),('header',('sourceDependencies',),[]),('exact',('exactBytes',),False),('blob',('originalObjectScaffolding',),True),('arguments',('sourceAbiContract','physicalArgumentWords'),1),('command',('sourceAbiContract','fixedCommand'),0),('control',('sourceAbiContract','controlWord'),0x8900),('meaning',('sourceAbiContract','historicalPublicMeaningProven'),True),('model',('oracle','independentHalfwordPollConstantCommandAndUntouchedMemoryModel'),False),('raw-state',('oracle','rawRegistersFlagsStackAndMappedMemoryCompared'),False),('coverage',('oracle','allOwnInstructionsVisited'),False),('nested-credit',('oracle','actualNestedReturns'),1),('providers',('oracle','providerReplacements'),['poll']),('physical',('oracle','physicalPeripheralExecution'),True),('scene',('oracle','wholeSceneOrHardwareContextProven'),True),('missing-object',('object',),'work/arm7-bulk-20261030/no-spi-cmd.o'),('missing-trace',('oracle','trace','path'),'work/arm7-bulk-20261030/no-spi-cmd.json.gz')]:reject(str(i)+'-'+name,('matches',i)+path,value)
    profile=json.loads((matcher.SOURCE/'profile.json').read_text())['units'];original=(ROOT/profile[0]['binary']).read_bytes();wrong=[]
    for seed in profile:
        command=seed['fixedCommand'];text=(ROOT/seed['source']).read_text();old='[0] = '+hex(command)+';';assert old in text;source=ROOT/('generated/arm7-spi-cmd256-controls/'+seed['address'][2:]+'/native.c');source.parent.mkdir(parents=True,exist_ok=True);header=ROOT/seed['sourceDependencies'][0]['path'];(source.parent/header.name).write_bytes(header.read_bytes());source.write_text(text.replace(old,'[0] = '+hex(command^1)+';'),encoding='utf-8');row,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/'wrong'/seed['address'][2:],strict=False)
        if len(body)!=64 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong command source matched or escaped extent')
        records=[];rejected=0;entry=int(seed['address'],0)
        for index,case in enumerate(matcher.native.cases(entry)):
            value=matcher.native.execute(original,entry,body,case,index);records.append(value);rejected+=not value['modelPassed']
        if len(records)!=81 or rejected!=81:raise ValueError('Wrong command source was not rejected independently')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/'wrong'/seed['address'][2:]/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(entry=seed['address'],originalCommand=command,wrongCommand=command^1,compilerResult=row,genuineLinkComparison=comparison,actualOwnReturns=81,independentModelRejections=81,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    for row in report['matches']:
        entry=int(row['address'],0);body=(matcher.WORK/row['address'][2:]/'real-link/caller.bin').read_bytes();value=matcher.native.execute(original,entry,body,matcher.native.cases(entry)[0],0,budget=1,allow_no_return=True)
        if value['actualOwnReturn']:raise ValueError('Prefix gained a return')
        controls.append(dict(name='prefix-'+row['address'],rejected=True,execution=value))
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=324,independentWrongSourceRejections=324,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=324,modelRejections=324)),flush=True)
if __name__=='__main__':main()
