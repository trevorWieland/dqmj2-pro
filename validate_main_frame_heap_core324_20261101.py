import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_main_frame_heap_core324_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='2353a78cdbd9b8fc080c79aff4c871f96c9f8035df875116bf82cc8997ed801a'
CONTROLS=ROOT/'evidence/verification/main-frame-heap-core324-controls-20261101.json'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:raise ValueError('Required current core source/closure/product missing or changed')
    return path


def link_products(entry,link,directory):
    checked(entry['object'],entry['objectSha256']);checked(link['lcf'],link['lcfSha256']);checked(link['linkedElf'],link['linkedElfSha256'])
    checked(directory/'genuine-link/caller.bin',entry['targetSha256'])
    for row in link['bindingOnlyProbes']:checked(row['object'],row['objectSha256'])


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files']
    names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{r['path']for r in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Frozen core generator/runtime identity differs')
    if len(report['generatorSources'])!=len(names)or{r['path']for r in report['generatorSources']}!=names:raise ValueError('Complete core source/source-linked closure differs')
    for row in report['generatorSources']:checked(row['path'],row['sha256'])
    for row in report['matches']:
        checked(row['source'],row['sourceSha256']);checked(row['compiler'],row['compilerSha256']);link_products(row,row['realMainLink'],matcher.WORK/row['address'])
    for row in report['sourceLinkedWrappers']:link_products(row['entry'],row['realMainLink'],matcher.WORK/'source-linked-wrappers'/row['entry']['address'])
    trace=report['sourceLinkedCoreEvidence']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Current core native trace differs or is not deterministic gzip')
    if _FRESH is None:
        matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh owned-source and source-linked native return/model/coverage evidence differs')
    return {('arm9','','main',row['address'],'arm'):row for row in report['matches']}


def wrong_sources():
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();rebuilt=bytearray(image)
    for pin in json.loads(matcher.PROFILE.read_text())['matches']:
        address=int(pin['address'],0);body=(matcher.WORK/pin['address']/'genuine-link/caller.bin').read_bytes()
        rebuilt[address-0x02000000:address-0x02000000+len(body)]=body
    wrappers={int(pin['address'],0):(matcher.WORK/'source-linked-wrappers'/pin['address']/'genuine-link/caller.bin').read_bytes()for pin in json.loads(matcher.WRAPPERS.read_text())['matches']}
    results=[]
    for pin in json.loads(matcher.PROFILE.read_text())['matches']:
        address=int(pin['address'],0);text=(ROOT/pin['source']).read_text()
        if address==0x0202B54C:
            changes=[('wrong-payload-start52','(u32)heap+48','(u32)heap+52'),('wrong-opaque-initial-state','heap->frame.opaqueState=0;','heap->frame.opaqueState=1;')]
            contexts=[(matcher.native.CREATOR,i)for i in list(range(1200))+list(range(1330,1426))]
        else:
            changes=[('wrong-head-state','frame->head=finish;','frame->head=aligned;')]if address==0x0202B594 else[('wrong-tail-field','frame->tail=aligned;','frame->head=aligned;')]
            contexts=[]
            for index in range(1568):
                spec=matcher.native.allocation_case(image,index)[-1]
                if (address==0x0202B614)==spec['backwards']and spec['modelDomain']:contexts.append((matcher.native.ALLOCATOR,index))
        for label,old,new in changes:
            if text.count(old)!=1:raise ValueError('Expected ordinary core source control missing or ambiguous')
            source=ROOT/'generated/main-frame-heap-core324-negative-20261101'/label/Path(pin['source']).name
            source.parent.mkdir(parents=True,exist_ok=True);source.write_text(text.replace(old,new));dependencies=[]
            for item in pin['sourceDependencies']:
                header=source.parent/Path(item['path']).name;header.write_bytes((ROOT/item['path']).read_bytes())
                dependencies.append(dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header)))
            bad=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=dependencies,variant=label)
            directory=matcher.WORK/'wrong-source'/label;entry,bindings,link,mismatch,body=matcher.compiler.build(bad,directory,strict=False)
            if link is not None or len(body)>pin['bytes']:raise ValueError('Wrong core source matched or exceeds its exclusive native slot')
            bad_image=bytearray(rebuilt);bad_image[address-0x02000000:address-0x02000000+len(body)]=body
            lengths=dict(matcher.native.CORE_CODE);lengths[address]=len(body)-(4 if address==0x0202B54C else 0)
            records=[];returns=owned=stops=rejections=0
            for wrapper,index in contexts:
                value=matcher.native.execute(bytes(bad_image),wrapper,wrappers[wrapper],index,core_code_lengths=lengths)
                records.append(dict(wrapper=hex(wrapper),index=index,result=value))
                if value['actualOwnReturn']:
                    returns+=1;owned+=sum(int(r['address'],0)==address for r in value['actualOwnedCoreReturns']);rejections+=int(not value['modelPassed'])
                else:stops+=1
            if not rejections or not owned:raise ValueError('Wrong core C survived model or lacks actual owned return evidence')
            raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=directory/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
            results.append(dict(name=label,address=pin['address'],compilerResult=entry,qualifiedBindings=bindings,genuineLinkMismatch=mismatch,
                actualWrongOwnedReturns=owned,actualOuterWrapperReturnsSeparate=returns,boundedNoReturnContexts=stops,independentModelRejections=rejections,
                originalTailOrLiteralExecutionRejected=True,completeGeneratedBodyOnly=True,providerReplacements=[],
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
        else:raise ValueError('Invalid core source/evidence survived: '+label)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm7'),('program',('program',),'child'),
        ('module',('module',),'itcm'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),
        ('coverage',('matchedInitializedBytes',),432),('code',('matchedInstructionBytes',),324),('literal',('generatedLiteralBytes',),0),
        ('functions',('newOrdinaryFunctionCount',),5),('denominator',('initializedDenominatorDelta',),324),('callee-credit',('additionalOtherCalleeDataOrAssemblyCredit',),160),
        ('module-linked',('wholeModuleLinked',),True),('full-source',('sourceReconstructionComplete',),True),
        ('mode',('matches',0,'mode'),'thumb'),('size',('matches',1,'bytes'),124),('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),
        ('blob',('matches',0,'originalObjectScaffolding'),True),('exact',('matches',1,'exactAfterDeclaredRelocation'),False),
        ('code-input',('matches',2,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),('arity',('matches',0,'sourceAbiContract','physicalArgumentWords'),4),
        ('object-extent',('matches',0,'sourceStorageView','originalTotalObjectExtentProven'),True),
        ('own-count',('matches',0,'oracle','actualOwnSourceAndNativeReturns'),5836),('duplicate-caller-credit',('sourceLinkedCoreEvidence','newWrapperSourceCredit'),108),
        ('other-callee-credit',('sourceLinkedCoreEvidence','otherOriginalCalleeDataOrAssemblyCredit'),160),('provider',('sourceLinkedCoreEvidence','providerReplacements'),['fill']),
        ('unsupported-return-credit',('sourceLinkedCoreEvidence','boundedStopPostStateCredit'),76),
        ('unchecked-owned-abi',('sourceLinkedCoreEvidence','ownedReturnCalleeSavedStackAndForwardedR0Verified'),False),
        ('unchecked-effects',('sourceLinkedCoreEvidence','fullRawRegistersFlagsMappedMemoryStackOrderedEffectsCompared'),False),
        ('missing-object',('matches',0,'object'),'work/main-sdk-heap/absent-core.o'),
        ('missing-source-linked-caller',('sourceLinkedWrappers',0,'entry','object'),'work/main-sdk-heap/absent-core-wrapper.o'),
        ('missing-trace',('sourceLinkedCoreEvidence','trace','path'),'work/main-sdk-heap/absent-core-trace.json.gz')]
    for label,keys,value in changes:reject(label,keys,value)
    negatives=wrong_sources();validate(json.loads(matcher.REPORT.read_text()))
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),
        metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=negatives,compiledWrongSourceControlCount=len(negatives),
        actualWrongOwnedReturns=sum(r['actualWrongOwnedReturns']for r in negatives),independentWrongSourceModelRejections=sum(r['independentModelRejections']for r in negatives),
        restoredPositive=True,sourceOnlyFreshOwnedAndCallerCompileBeforeValidation=True,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),metadataControls=len(controls),
        wrongSourceControls=len(negatives),wrongOwnedReturns=result['actualWrongOwnedReturns'],independentRejections=result['independentWrongSourceModelRejections'])),flush=True)


if __name__=='__main__':main()
