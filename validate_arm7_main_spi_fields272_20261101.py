import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi_fields272_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='aa0fb27b9dd34eb996181aea33168830dc2fd845475988d553cbf3acec01ec2b'
CONTROLS=ROOT/'evidence/verification/arm7-main-spi-fields272-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current initializer source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen field source/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete field source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for dependency,rows in[(False,report['matches']),(True,[report['existingSourceDependency']])]:
        for row in rows:
            for key,hashkey in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[key],row[hashkey])
            for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
            link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=(matcher.WORK/'helper'if dependency else matcher.WORK/row['address'][2:])/'real-link';checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256'])
            if not dependency:
                trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
                if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Field trace differs or is not deterministic gzip')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only two-field/existing-helper link/native evidence differs')
    return {('arm7','','arm7-main',row['address'],'arm'):row for row in report['matches']}


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid field proof survived '+name)
    for name,path,value in [('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('count',('newOrdinaryFunctionCount',),3),('bytes',('matchedInitializedBytes',),308),('code',('matchedCodeBytes',),272),('literal',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),272),('data-credit',('originalDataAssemblyOrExtentCredit',),16),('module-credit',('wholeModuleLinked',),True),('complete-game',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),4528),('helper-credit',('existingSourceDependency','sourceCredit'),1),('helper-byte-credit',('existingSourceDependency','byteCredit'),36),('helper-source',('existingSourceDependency','sourceSha256'),'0'*64),('binding',('nativeSymbols','native_host_arm7_arm_027f54f0'),'0x27f56c8')]:reject(name,path,value)
    for i in range(2):
        for name,path,value in [('address',('address',),'0x27f5a28'),('mode',('mode',),'thumb'),('source',('sourceSha256',),'0'*64),('flags',('compilerFlags',),[]),('header',('sourceDependencies',),[]),('exact',('exactBytes',),False),('blob',('originalObjectScaffolding',),True),('arguments',('sourceAbiContract','physicalArgumentWords'),0),('bits',('sourceAbiContract','serializedAddressBits'),8),('calls',('sourceAbiContract','helperCalls'),1),('command',('sourceAbiContract','fixedCommand'),0),('width',('sourceAbiContract','sourceWidths','high'),8),('meaning',('sourceAbiContract','historicalPublicMeaningProven'),True),('model',('oracle','independentWordInputsShiftWidthsByteOrderSavedFrameAndHalfwordPortModel'),False),('raw-state',('oracle','rawRegistersFlagsStackAndMappedMemoryCompared'),False),('coverage',('oracle','allOwnAndHelperInstructionsVisited'),False),('source-chain',('oracle','fullSourceLinkedFieldCallerAndExistingHelper'),False),('providers',('oracle','providerReplacements'),['byte']),('physical',('oracle','physicalPeripheralExecution'),True),('scene',('oracle','wholeSceneOrHardwareContextProven'),True),('nested-double',('oracle','existingSourceHelperReturnsSeparateZeroCredit'),3396),('missing-object',('object',),'work/arm7-bulk-20261030/absent-field.o'),('missing-trace',('oracle','trace','path'),'work/arm7-bulk-20261030/absent-field.json.gz')]:reject(str(i)+'-'+name,('matches',i)+path,value)
    profile=json.loads((matcher.SOURCE/'profile.json').read_text());original=(ROOT/profile['units'][0]['binary']).read_bytes();helper=(matcher.WORK/'helper/real-link/caller.bin').read_bytes();wrong=[]
    for seed in profile['units']:
        entry=int(seed['address'],0);text=(ROOT/seed['source']).read_text();command=matcher.native.COMMANDS[entry]
        definitions=[('high-bit-omitted','0xff0000','0xfe0000',134),('wrong-command','[0] = '+hex(command)+';','[0] = '+hex(command^1)+';',283),('wrong-final-control','[0] = 0x8100;','[0] = 0x8900;',283)]
        for name,old,new,expected in definitions:
            assert old in text;directory=matcher.WORK/'wrong'/seed['address'][2:]/name;source=ROOT/('generated/arm7-fields272-controls/'+seed['address'][2:]+'/'+name+'/native.c');source.parent.mkdir(parents=True,exist_ok=True);header=ROOT/seed['sourceDependencies'][0]['path'];(source.parent/header.name).write_bytes(header.read_bytes());source.write_text(text.replace(old,new),encoding='utf-8');row,comparison,body=matcher.compile_unit(seed,source,directory,strict=False)
            if len(body)!=136 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong field C matched or escaped extent')
            records=[];rejected=0
            for index,case in enumerate(matcher.native.cases()):
                value=matcher.native.execute(original,entry,body,helper,case,index);records.append(value);rejected+=not value['modelPassed']
            if rejected!=expected:raise ValueError('Wrong field model rejection count differs '+name+':'+str(rejected))
            raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=directory/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,entry=seed['address'],compilerResult=row,genuineLinkComparison=comparison,actualOwnReturns=283,independentModelRejections=rejected,existingHelperFreshlySourceCompiled=True,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    for seed in profile['units']:
        entry=int(seed['address'],0);body=(matcher.WORK/seed['address'][2:]/'real-link/caller.bin').read_bytes();value=matcher.native.execute(original,entry,body,helper,matcher.native.cases()[0],0,budget=1,allow_no_return=True)
        if value['actualOwnReturn']or value['actualNestedReturns']:raise ValueError('Field prefix gained a return')
        controls.append(dict(name='prefix-'+seed['address'],rejected=True,execution=value))
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=1698,independentWrongSourceRejections=1400,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=1698,modelRejections=1400)),flush=True)
if __name__=='__main__':main()
