import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi_read296_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='53a7dd6a27824fcfb92fc7db448d6b5ddcc23ff3ac863a63dc7511198852c771'
CONTROLS=ROOT/'evidence/verification/arm7-main-spi-read296-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current initializer source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA)
    pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen register-read generator/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete register-read source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for row in report['matches']:
        for key,hashkey in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[key],row[hashkey])
        for dep in row['sourceDependencies']:checked(dep['path'],dep['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=matcher.WORK/row['address'][2:]/'real-link'
        checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256'])
        for field in ('readTrace','directHelperTrace'):
            trace=row['oracle'][field];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
            if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Register-read trace differs or has nonzero gzip mtime')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only pair link/native/direct/bus/source evidence differs')
    return {('arm7','','arm7-main',row['address'],'arm'):row for row in report['matches']}


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid read296 proof survived '+name)
    for name,path,value in [('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('count',('newOrdinaryFunctionCount',),3),('bytes',('matchedInitializedBytes',),592),('code',('matchedCodeBytes',),296),('literal',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),296),('data-credit',('originalDataAssemblyOrExtentCredit',),12),('module-credit',('wholeModuleLinked',),True),('complete-game',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),2724),('helper-return-double',('helperOwnReturns',),1834),('caller-return-double',('callerOwnReturns',),1780),('source-map',('runtimeOwnership','modules',2,'sourceImageOffset'),540),('runtime-map',('runtimeOwnership','modules',2,'runtimeBase'),'0x37f8000'),('stack',('runtimeOwnership','fixtureStack'),'0x27f55c4')]:reject(name,path,value)
    for i in range(2):
        for name,path,value in [('address',('address',),'0x27f55c8'),('mode',('mode',),'thumb'),('source',('sourceSha256',),'0'*64),('flags',('compilerFlags',),[]),('header',('sourceDependencies',),[]),('exact',('exactBytes',),False),('blob',('originalObjectScaffolding',),True),('arguments',('sourceAbiContract','physicalArgumentWords'),4),('meaning',('sourceAbiContract','historicalPublicMeaningProven'),True),('model',('oracle','independentAddressByteOrderArrayStackFrameHalfwordAndOutputModel'),False),('raw-state',('oracle','rawRegistersFlagsStackAndMappedMemoryCompared'),False),('coverage',('oracle','allOwnInstructionsVisited'),False),('original-helper',('oracle','fullSourceLinkedReadAndDummyHelper'),False),('providers',('oracle','providerReplacements'),['dummy']),('physical',('oracle','physicalPeripheralExecution'),True),('scene',('oracle','wholeSceneOrHardwareContextProven'),True),('missing-object',('object',),'work/arm7-bulk-20261030/no-read296.o'),('missing-trace',('oracle','readTrace','path'),'work/arm7-bulk-20261030/no-read296.json.gz')]:reject(str(i)+'-'+name,('matches',i)+path,value)
    for name,path,value in [('zero-count-word',('matches',0,'sourceAbiContract','addressWordRemainsFullWidthAtZeroCount'),False),('24-bit-encoding',('matches',0,'sourceAbiContract','serializedAddressBits'),8),('array-extent',('matches',0,'sourceAbiContract','serializedHalfwordArrayElements'),1),('store-width',('matches',0,'sourceAbiContract','outputStoreWidth'),2),('unsigned-count',('matches',0,'sourceAbiContract','countUnsigned32'),False),('zero-count-returns',('matches',0,'oracle','zeroCountCallerReturns'),0),('busy-error',('matches',0,'oracle','unsupported',0,'supportedErrorPathCredit'),1),('large-count-error',('matches',0,'oracle','unsupported',9,'supportedErrorPathCredit'),1),('callee-binding',('nativeSymbols','native_host_arm7_arm_027f56c8'),'0x27f54f0')]:reject(name,path,value)
    profile=json.loads((matcher.SOURCE/'profile.json').read_text())['units'];original=(ROOT/profile[0]['binary']).read_bytes();own=(matcher.WORK/profile[0]['address'][2:]/'real-link/caller.bin').read_bytes();helper=(matcher.WORK/profile[1]['address'][2:]/'real-link/caller.bin').read_bytes();wrong=[]
    definitions=[('swapped-address-bytes',0,'(u16)((address & 0xff0000) >> 16), (u16)((address & 0xff00) >> 8)','(u16)((address & 0xff00) >> 8), (u16)((address & 0xff0000) >> 16)'),('wrong-read-command',0,'[0] = 3;','[0] = 2;'),('wrong-dummy',1,'[0] = 0;','[0] = 1;')]
    for name,index,old,new in definitions:
        seed=profile[index];text=(ROOT/seed['source']).read_text();assert old in text;source=ROOT/('generated/arm7-spi-read296-controls/'+name+'/native.c');source.parent.mkdir(parents=True,exist_ok=True);header=ROOT/seed['sourceDependencies'][0]['path'];(source.parent/header.name).write_bytes(header.read_bytes());source.write_text(text.replace(old,new),encoding='utf-8');row,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if len(body)!=seed['bytes']or comparison.get('exactLinkedBytes'):raise ValueError('Wrong read source matched or escaped its complete extent')
        records=[];rejects=0
        for n,case in enumerate(matcher.native.cases()):
            value=matcher.native.execute(original,body if index==0 else own,body if index==1 else helper,case,n);records.append(value);rejects+=not value['modelPassed']
        expected=324 if name=='swapped-address-bytes'else 418
        if rejects!=expected:raise ValueError('Wrong read independent rejection count differs '+name+':'+str(rejects))
        direct_records=[];direct_rejects=0
        if index==1:
            for n,case in enumerate(matcher.native.helper_cases()):
                value=matcher.native.execute(original,own,body,case,n,direct=True);direct_records.append(value);direct_rejects+=not value['modelPassed']
            if direct_rejects!=81:raise ValueError('Wrong direct dummy failed to reject')
        raw=(json.dumps(dict(caller=records,directHelper=direct_records),sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,compilerResult=row,genuineLinkComparison=comparison,actualCallerReturns=445,independentCallerModelRejections=rejects,actualDirectHelperReturns=len(direct_records),independentDirectHelperModelRejections=direct_rejects,zeroCountCallerPathsRemainValid=27,sourceChainFreshNoOriginalHelperDelegation=True,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    for direct in(False,True):
        case=matcher.native.helper_cases()[0]if direct else matcher.native.cases()[0];value=matcher.native.execute(original,own,helper,case,0,direct=direct,budget=1,allow_no_return=True)
        if value['actualOwnReturn']or value['actualNestedReturns']:raise ValueError('Prefix gained own or nested return')
        controls.append(dict(name='helper-prefix'if direct else'caller-prefix',rejected=True,execution=value))
    case=dict(matcher.native.helper_cases()[0],stuck=1);value=matcher.native.execute(original,own,helper,case,0,direct=True,budget=300,allow_no_return=True)
    if value['actualOwnReturn']or not value['stuckPhaseReached']:raise ValueError('Direct helper busy phase not observed')
    controls.append(dict(name='direct-helper-busy',rejected=True,execution=value));validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongCallerReturns=1335,actualWrongDirectHelperReturns=81,independentWrongSourceRejections=1241,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongCallerReturns=1335,wrongDirectReturns=81,modelRejections=1241)),flush=True)
if __name__=='__main__':main()
