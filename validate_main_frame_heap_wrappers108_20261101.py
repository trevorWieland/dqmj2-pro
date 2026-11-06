import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_main_frame_heap_wrappers108_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='b98a6b9cfa76ca130fd66a709ac31e3753fbc6cad80f4b70afb81ab4f6144f9f'
CONTROLS=ROOT/'evidence/verification/main-frame-heap-wrappers108-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current frame source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files']
    names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frame generator/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete frame source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for row in report['matches']:
        checked(row['source'],row['sourceSha256']);checked(row['compiler'],row['compilerSha256']);checked(row['object'],row['objectSha256'])
        link=row['realMainLink'];checked(link['lcf'],link['lcfSha256']);checked(link['linkedElf'],link['linkedElfSha256'])
        checked(matcher.WORK/row['address']/'genuine-link/caller.bin',row['targetSha256'])
        for probe in link['bindingOnlyProbes']:checked(probe['object'],probe['objectSha256'])
        trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
        if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Current frame trace differs or is not deterministic gzip')
    if _FRESH is None:
        matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only main links/native models/stops/coverage differ')
    return {('arm9','','main',row['address'],'arm'):row for row in report['matches']}


def wrong_sources():
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();results=[]
    for pin in json.loads(matcher.PROFILE.read_text())['matches']:
        address=int(pin['address'],0);text=(ROOT/pin['source']).read_text()
        if address==matcher.native.CREATOR:
            changes=[('wrong-minimum52','< 0x30U','< 0x34U'),('wrong-start-rounding','(arg0 + 3) & ~3','arg0 & ~3')]
            indices=list(range(1200))+list(range(1330,1426))
        else:
            changes=[('wrong-round8','(var_r1 + 3) & ~3','(var_r1 + 7) & ~7'),
                ('wrong-zero-promotion','var_r1 = 1;','var_r1 = 0;')]
            indices=[];original=image[address-0x02000000:address-0x02000000+pin['bytes']]
            for index in range(1568):
                value=matcher.native.execute(image,address,original,index)
                if value['actualOwnReturn']and value['case']['modelDomain']:indices.append(index)
        for label,old,new in changes:
            if text.count(old)!=1:raise ValueError('Expected ordinary frame source control missing or ambiguous')
            source=ROOT/'generated/main-frame-heap-wrappers108-negative-20261101'/label/Path(pin['source']).name
            source.parent.mkdir(parents=True,exist_ok=True);source.write_text(text.replace(old,new));dependencies=[]
            for item in pin['sourceDependencies']:
                header=source.parent/Path(item['path']).name;header.write_bytes((ROOT/item['path']).read_bytes())
                dependencies.append(dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header)))
            bad=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=dependencies,variant=label)
            directory=matcher.WORK/'wrong-source'/label
            entry,bindings,link,mismatch,body=matcher.compiler.build(bad,directory,strict=False)
            if link is not None:raise ValueError('Wrong ordinary frame C matched the measured original')
            records=[];returns=stops=rejections=helpers=0
            for index in indices:
                value=matcher.native.execute(image,address,body,index);records.append(dict(index=index,result=value))
                if value['actualOwnReturn']:
                    returns+=1;rejections+=int(not value['modelPassed']);helpers+=len(value['actualOriginalHelperReturnsSeparate'])
                else:stops+=1
            if not rejections:raise ValueError('Wrong ordinary frame source survived independent memory/return model')
            raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=directory/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
            results.append(dict(name=label,compilerResult=entry,qualifiedBindings=bindings,genuineMainLinkMismatch=mismatch,
                actualWrongSourceReturns=returns,boundedNoReturnCases=stops,independentModelRejections=rejections,
                actualOriginalHelperReturnsSeparate=helpers,providerReplacements=[],completeGeneratedBodyOnly=True,
                trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    return results


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(label,keys,value):
        bad=copy.deepcopy(report);target=bad
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=label,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid frame source/evidence survived: '+label)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm7'),
        ('program',('program',),'child'),('module',('module',),'itcm'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),
        ('coverage',('matchedInitializedBytes',),216),('code',('matchedInstructionBytes',),100),('literal',('generatedLiteralBytes',),8),
        ('function-count',('newOrdinaryFunctionCount',),3),('callee-credit',('originalCalleeDataExtentOrAssemblyCredit',),324),
        ('denominator',('initializedDenominatorDelta',),108),('module-claim',('wholeModuleLinked',),True),('complete-source',('sourceReconstructionComplete',),True),
        ('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('mode',('matches',0,'mode'),'thumb'),
        ('size',('matches',0,'bytes'),52),('blob',('matches',0,'originalObjectScaffolding'),True),('exact',('matches',0,'exactAfterDeclaredRelocation'),False),
        ('code-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),('arity',('matches',0,'sourceAbiContract','physicalArgumentWords'),2),
        ('historical-types',('matches',0,'sourceAbiContract','originalHistoricalTypesProven'),True),
        ('return-count',('matches',0,'oracle','actualOwnSupportedReturns'),2852),('stops-counted-as-returns',('matches',0,'oracle','pairedBoundedNoReturnCases'),0),
        ('provider',('matches',1,'oracle','providerReplacements'),['allocator']),('callee-proof-credit',('matches',0,'oracle','originalCalleesAdditionalSourceCredit'),72),
        ('unchecked-state',('matches',1,'oracle','rawRegistersFlagsAllMappedRamStackOrderedMemoryAndNestedArgumentsCompared'),False),
        ('zero-return-semantics',('matches',1,'oracle','zeroReturnWithChangedHeadTailCases'),0),
        ('binding',('nativeSymbols','native_fn_0202b54c'),'0x202b550'),('missing-object',('matches',0,'object'),'work/main-sdk-heap/absent-frame.o'),
        ('missing-trace',('matches',1,'oracle','trace','path'),'work/main-sdk-heap/absent-frame.json.gz')]
    for label,keys,value in changes:reject(label,keys,value)
    negatives=wrong_sources();image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    body=(matcher.WORK/'0x202b740/genuine-link/caller.bin').read_bytes();value=matcher.native.execute(image,matcher.native.CREATOR,body,0,budget=1)
    if value['actualOwnReturn']or not value['postStateExcluded']:raise ValueError('Exhausted frame prefix acquired return/post-state credit')
    controls.append(dict(name='bounded-exhaustion',rejected=True,reason='Prefix did not return; post-state excluded'))
    validate(json.loads(matcher.REPORT.read_text()))
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),
        metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=negatives,compiledWrongSourceControlCount=len(negatives),
        actualWrongSourceReturns=sum(r['actualWrongSourceReturns']for r in negatives),independentWrongSourceModelRejections=sum(r['independentModelRejections']for r in negatives),
        restoredPositive=True,sourceOnlyFreshCompileBeforeValidation=True,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),metadataControls=len(controls),
        wrongSourceControls=len(negatives),wrongSourceReturns=result['actualWrongSourceReturns'],independentRejections=result['independentWrongSourceModelRejections'])),flush=True)


if __name__=='__main__':main()
