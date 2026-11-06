import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_bitfields544_20261101 as matcher
from project import ROOT,sha256,write_json
MATCHER_SHA='5b25f598d744606e5fdb62801c12cf623097fc4e62aeaea3645bac91f7ccb44d'
CONTROLS=ROOT/'evidence/verification/arm7-main-bitfields544-controls-20261101.json'
_FRESH=None


def checked(name,digest):
    p=(ROOT/name).resolve()
    if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=digest:raise ValueError('Current bitfield source/product missing or changed')
    return p


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen bitfield closure differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Full bitfield source/input closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for row in report['matches']:
        for name,digest in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[name],row[digest])
        for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'linked.elf',link['linkedElfSha256']);checked(directory/'caller.bin',row['targetSha256']);trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
        if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Bitfield trace changed or nonzero gzip mtime')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only bitfield unit/default-link/full-word model differs')
    return {('arm7','','arm7-main',x['address'],'arm'):x for x in report['matches']}


def main():
    global _FRESH
    matcher.main();report=json.loads(matcher.REPORT.read_text());_FRESH=report;validate(report);controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False bitfield proof survived '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('functions',('newOrdinaryFunctionCount',),1),('bytes',('matchedInitializedBytes',),272),('code',('matchedCodeBytes',),400),('pool',('generatedLiteralBytes',),144),('denominator',('initializedDenominatorDelta',),544),('data',('originalDataAssemblyOrExtentCredit',),288),('module',('wholeModuleLinked',),True),('game',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),2560),('own-scope',('scope','eachCompleteNativeBytes'),268),('dispatch',('scope','jumpDispatchBranchesPerUnit'),35),('calls',('scope','externalCallsOrBindings'),1),('interior',('scope','callableInteriorOrSharedTailClaim'),True),('address',('matches',0,'address'),'0x27f6ca4'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('header',('matches',0,'sourceDependencies'),[]),('exact',('matches',0,'exactBytes'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('source-only',('matches',0,'sourceOnlyCompilerInput'),False),('argument',('matches',0,'sourceAbiContract','physicalArgumentWords'),0),('return',('matches',0,'sourceAbiContract','rawIncomingAddressWordReturned'),False),('layout-size',('matches',0,'sourceAbiContract','wordStorageView','bytes'),8),('layout-offset',('matches',0,'sourceAbiContract','wordStorageView','fields',1,'offsetBits'),9),('layout-width',('matches',0,'sourceAbiContract','wordStorageView','fields',1,'bits'),5),('full-object',('matches',0,'sourceAbiContract','wordStorageView','completeHistoricalObjectExtentClaim'),True),('unsigned',('matches',0,'sourceAbiContract','unsignedBitfieldArithmetic'),False),('historical-meaning',('matches',0,'sourceAbiContract','historicalPublicMeaningProven'),True),('android',('matches',0,'sourceAbiContract','platformIndependentBitfieldLayoutOrAndroidPointerModelProven'),True),('coverage',('matches',0,'oracle','allOwnInstructionsAndBranchTableSlotsVisited'),False),('code-flag',('matches',0,'oracle','codeFlagPairs'),64),('default-read',('matches',0,'oracle','distinctReadCounts'),[1]),('storeless',('matches',1,'oracle','distinctStoreCounts'),[1]),('model',('matches',0,'oracle','independentFullWordFieldPreservationAndReadStoreFlagsModel'),False),('raw-state',('matches',0,'oracle','fullRawCpuStackInputAndMappedRamCompared'),False),('provider',('matches',0,'oracle','providerReplacements'),['word']),('hardware',('matches',0,'oracle','hardwareContextProven'),True),('all-outcomes',('matches',0,'oracle','allLowByteValuesAndEveryCodeFlagOutcomeCovered'),False),('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/no-bitfield.o'),('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/no-bitfield.json.gz')]
    for name,path,value in changes:reject(name,path,value)
    profile=json.loads((matcher.SOURCE/'profile.json').read_text());original=(ROOT/profile['units'][0]['binary']).read_bytes();wrong=[]
    for index,(name,unit,old,new,layout)in enumerate([('wrong-clear',0,'p->flag=0; break;','p->flag=1; break;',False),('inverted-low-predicate',1,'if(p->flag) p->code+=18;','if(!p->flag) p->code+=18;',False),('shifted-word-layout',0,None,None,True)]):
        seed=copy.deepcopy(profile['units'][unit]);text=(ROOT/seed['source']).read_text();folder=ROOT/('generated/arm7-bitfields544-controls/'+name);folder.mkdir(parents=True,exist_ok=True);header=folder/'native_fields.h';header_text=(ROOT/seed['sourceDependencies'][0]['path']).read_text()
        if layout:header_text=header_text.replace('low:8','low:9').replace('high:17','high:16')
        else:
            if old not in text:raise ValueError('Wrong ordinary-C transformation absent')
            text=text.replace(old,new)
        header.write_text(header_text,encoding='utf-8');seed['sourceDependencies']=[dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header))];source=folder/'native.c';source.write_text(text,encoding='utf-8');row,comparison,body=matcher.compiler.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if len(body)!=272 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong bitfield source matched or escaped its complete scope')
        rejected=0;records=[]
        for j,case in enumerate(matcher.native.cases()):
            value=matcher.native.execute(original,int(seed['address'],0),body,case,j);records.append(value);rejected+=not value['modelPassed']
        if not rejected:raise ValueError('Wrong bitfield source survived its independent model')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,source=row,genuineLinkComparison=comparison,actualOwnReturns=len(records),independentModelRejections=rejected,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    for seed in profile['units']:
        entry=int(seed['address'],0);body=(matcher.WORK/seed['address'][2:]/'real-link/caller.bin').read_bytes();value=matcher.native.execute(original,entry,body,matcher.native.cases()[0],0,budget=1,allow_no_return=True)
        if value['actualOwnReturn']or value['actualNestedReturns']:raise ValueError('One-word-read prefix acquired a return')
        controls.append(dict(name='one-instruction-prefix-'+seed['address'],rejected=True,execution=value))
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=sum(x['actualOwnReturns']for x in wrong),independentWrongSourceRejections=sum(x['independentModelRejections']for x in wrong),sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=result['actualWrongOwnReturns'],modelRejections=result['independentWrongSourceRejections'])),flush=True)
if __name__=='__main__':main()
