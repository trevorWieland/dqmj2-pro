import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi_fast288_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='a56fcce10c3f0fc15311979cd4ec7de41b82d344b09ca22829de02ace3d5d1ff'
CONTROLS=ROOT/'evidence/verification/arm7-main-spi-fast288-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current initializer source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen fast-read source/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete fast-read source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for name,row in [('caller',report['matches'][0]),('helper',report['existingSourceDependency'])]:
        for key,hashkey in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[key],row[hashkey])
        for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=matcher.WORK/name/'real-link';checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256'])
    trace=report['matches'][0]['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Fast-read trace changed or has nonzero gzip mtime')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only fast-read/helper link/native frame/extra-transfer proof differs')
    return {('arm7','','arm7-main','0x27f56ec','arm'):report['matches'][0]}


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid fast-read proof survived '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('count',('newOrdinaryFunctionCount',),2),('bytes',('matchedInitializedBytes',),324),('code',('matchedCodeBytes',),288),('literal',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),288),('data-credit',('originalDataAssemblyOrExtentCredit',),8),('module-credit',('wholeModuleLinked',),True),('complete-game',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),1726),('helper-credit',('existingSourceDependency','sourceCredit'),1),('helper-byte-credit',('existingSourceDependency','byteCredit'),36),('helper-source',('existingSourceDependency','sourceSha256'),'0'*64),('address',('matches',0,'address'),'0x27f56f0'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('header',('matches',0,'sourceDependencies'),[]),('exact',('matches',0,'exactBytes'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('args',('matches',0,'sourceAbiContract','physicalArgumentWords'),4),('word',('matches',0,'sourceAbiContract','addressWordRemainsFullWidthAtZeroCount'),False),('width',('matches',0,'sourceAbiContract','serializedAddressBits'),8),('array',('matches',0,'sourceAbiContract','serializedHalfwordArrayElements'),1),('store',('matches',0,'sourceAbiContract','outputStoreWidth'),2),('count-sign',('matches',0,'sourceAbiContract','countUnsigned32'),False),('command',('matches',0,'sourceAbiContract','fixedCommand'),3),('extra-transfer',('matches',0,'sourceAbiContract','extraZeroTransferBeforeDataReads'),False),('meaning',('matches',0,'sourceAbiContract','historicalPublicMeaningProven'),True),('model',('matches',0,'oracle','independentExtraTransferAddressArrayStackFrameHalfwordAndOutputModel'),False),('raw-state',('matches',0,'oracle','rawRegistersFlagsStackAndMappedMemoryCompared'),False),('source-chain',('matches',0,'oracle','fullSourceLinkedFastReadAndExistingHelper'),False),('coverage',('matches',0,'oracle','allOwnAndHelperInstructionsVisited'),False),('helper-returns',('matches',0,'oracle','existingSourceHelperReturnsSeparateZeroCredit'),1672),('providers',('matches',0,'oracle','providerReplacements'),['dummy']),('physical',('matches',0,'oracle','physicalPeripheralExecution'),True),('scene',('matches',0,'oracle','wholeSceneOrHardwareContextProven'),True),('busy-error',('matches',0,'oracle','unsupported',0,'supportedErrorPathCredit'),1),('count-error',('matches',0,'oracle','unsupported',10,'supportedErrorPathCredit'),1),('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/no-fast.o'),('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/no-fast.json.gz'),('binding',('nativeSymbols','native_host_arm7_arm_027f56c8'),'0x27f54f0')]
    for name,path,value in changes:reject(name,path,value)
    profile=json.loads((matcher.SOURCE/'profile.json').read_text());seed=profile['newUnit'];original=(ROOT/seed['binary']).read_bytes();helper=(matcher.WORK/'helper/real-link/caller.bin').read_bytes();text=(ROOT/seed['source']).read_text();wrong=[]
    for name,old,new,expected in [('swapped-address-bytes','(u16)((address & 0xff0000) >> 16), (u16)((address & 0xff00) >> 8)','(u16)((address & 0xff00) >> 8), (u16)((address & 0xff0000) >> 16)',324),('wrong-fast-command','[0] = 0xb;','[0] = 0xa;',418)]:
        assert old in text;source=ROOT/('generated/arm7-fast288-controls/'+name+'/native.c');source.parent.mkdir(parents=True,exist_ok=True);header=ROOT/seed['sourceDependencies'][0]['path'];(source.parent/header.name).write_bytes(header.read_bytes());source.write_text(text.replace(old,new),encoding='utf-8');row,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if len(body)!=288 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong fast-read source matched or escaped extent')
        records=[];rejected=0
        for index,case in enumerate(matcher.native.cases()):
            value=matcher.native.execute(original,body,helper,case,index);records.append(value);rejected+=not value['modelPassed']
        if rejected!=expected:raise ValueError('Wrong fast-read model rejection count differs '+name+':'+str(rejected))
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,compilerResult=row,genuineLinkComparison=comparison,actualOwnReturns=445,independentModelRejections=rejected,zeroCountCallerPathsRemainValid=27,existingHelperFreshlySourceCompiled=True,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    own=(matcher.WORK/'caller/real-link/caller.bin').read_bytes();value=matcher.native.execute(original,own,helper,matcher.native.cases()[0],0,budget=1,allow_no_return=True)
    if value['actualOwnReturn']or value['actualNestedReturns']:raise ValueError('Prefix acquired a return')
    controls.append(dict(name='one-instruction-prefix',rejected=True,execution=value));validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=890,independentWrongSourceRejections=742,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=890,modelRejections=742)),flush=True)
if __name__=='__main__':main()
