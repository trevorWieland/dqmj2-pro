import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_main_sdk_heap_attribute424_20261101 as matcher
from project import ROOT,sha256,write_json

CONTROLS=ROOT/'evidence/verification/main-sdk-heap-attribute424-controls-20261101.json'
MATCHER_SHA='7e447dea6126f8d9e2271a92ae545540170b8c7522417e79cb62af145d7078ae'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:
        raise ValueError('Required current heap source/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pin=matcher.verify_inputs()
    names=[Path(matcher.__file__).name,'main_sdk_heap_attribute424_compile_20261101.py','main_sdk_heap_attribute424_native_20261101.py',
        'main_heap_commit_fixture_20261101.py',matcher.PROFILE.relative_to(ROOT).as_posix(),'evidence/research/20261101-main-heap-attribute424-sdk-reference.json',
        matcher.PINS.relative_to(ROOT).as_posix()]+[item['path']for item in json.loads(matcher.PINS.read_text())['files']]
    names=set(names)
    if {item['path']for item in report['generatorSources']}!=names or len(report['generatorSources'])!=len(names):
        raise ValueError('Complete heap source/runtime/reference closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    if report['generatorSha256']!=MATCHER_SHA or report['romSha256']!=matcher.ROM or report['pinnedGeneratorAndRuntimeDependencies']!=json.loads(matcher.PINS.read_text())['files']:
        raise ValueError('Frozen heap generator/build/runtime provenance differs')
    expected=dict(processor='arm9',program='',module='main',matchedInitializedBytes=424,matchedInstructionBytes=416,generatedLiteralBytes=8,
        newOrdinaryFunctionCount=1,newInitializedCoverageBytes=424,originalHelperDataExtentOrAssemblyCredit=0,initializedDenominatorDelta=0,
        wholeModuleLinked=False,sourceReconstructionComplete=False,supportedContext='bounded synthetic free/used heap list and all six original lower routines; no providers')
    if any(report.get(key)!=value for key,value in expected.items())or len(report['matches'])!=1:
        raise ValueError('Heap identity/ordinary-source/coverage scope differs')
    row=report['matches'][0]
    if any(row.get(key)!=value for key,value in pin.items()):raise ValueError('Heap source/compiler/qualified full boundary differs')
    for item in(row['nativeSymbols'],report['nativeSymbols']):
        if any(not isinstance(value,str)or value!=hex(int(value,0))for value in item.values()):
            raise ValueError('Main nativeSymbols require canonical hex strings')
    for path,key in[(row['source'],'sourceSha256'),(row['compiler'],'compilerSha256'),(row['object'],'objectSha256')]:checked(path,row[key])
    link=row['realMainLink']
    for path,key in[(link['linkedElf'],'linkedElfSha256'),(link['lcf'],'lcfSha256')]:checked(path,link[key])
    checked((matcher.WORK/'caller/genuine-link/caller.bin').as_posix(),row['targetSha256'])
    for probe in link['bindingOnlyProbes']:checked(probe['object'],probe['objectSha256'])
    trace=row['oracle']['trace'];data=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if data[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(data)).hexdigest()!=trace['rawSha256']:
        raise ValueError('Current native heap trace differs or is not mtime-zero gzip')
    if _FRESH is None:_FRESH=json.loads(json.dumps(matcher.proof()))
    current={key:value for key,value in report.items()if key not in('schemaVersion','generator','generatorSha256','generatorSources',
        'pinnedGeneratorAndRuntimeDependencies','romSha256','processor','program','module','originalFixtureGenerator','comparativeReference')}
    if current!=_FRESH:raise ValueError('Fresh genuine source link/full native model/CPU/memory evidence differs')
    if report['originalFixtureGenerator']!=dict(path='main_heap_commit_fixture_20261101.py',sha256=matcher.ORIGINAL_FIXTURE,untouched=True,
        instrumentedCopy='main_sdk_heap_attribute424_native_20261101.py'):
        raise ValueError('Original independent fixture provenance differs')
    reference=report['comparativeReference']
    if reference!=dict(path='evidence/research/20261101-main-heap-attribute424-sdk-reference.json',
        sha256=sha256(ROOT/'evidence/research/20261101-main-heap-attribute424-sdk-reference.json'),compilerInput=False,
        publicSdkRevisionEquivalenceProven=False,publicAllocatorThresholdAndFillPolicyAdopted=False):
        raise ValueError('Comparative SDK scope/provenance differs')
    return {('arm9','','main',row['address'],'arm'):row}


def wrong_sources(pin):
    text=(ROOT/pin['source']).read_text();results=[]
    changes=[('wrong-used-marker','0x5544','0x5545'),('wrong-group-bit','u32 newValue = group & maskBits;','u32 newValue = group & (maskBits ^ 1);'),
        ('wrong-fill-mode','if (flags & 1)','if (flags & 2)'),('wrong-free-split','< 20','< 24')]
    for label,old,new in changes:
        if old not in text:raise ValueError('Expected ordinary heap source control is absent')
        source=ROOT/'generated/main-sdk-heap-attribute424-negative-20261101'/label/'native_main_0202ae9c.c'
        source.parent.mkdir(parents=True,exist_ok=True);source.write_text(text.replace(old,new))
        bad=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),variant=label)
        entry,bindings,link,mismatch,code=matcher.compiler.build(bad,matcher.WORK/'wrong-source'/label,strict=False)
        if link is not None:raise ValueError('Wrong ordinary C unexpectedly linked to the original body')
        result=matcher.fixture.wrong_body(code,ROOT,matcher.WORK/'wrong-source'/label,label)
        result.update(source=bad['source'],sourceSha256=bad['sourceSha256'],compilerResult=entry,qualifiedBindings=bindings,
            genuineLinkMismatch={key:mismatch[key]for key in('caller','nativeBytes','linkedBytes','matchingBytes')})
        results.append(result)
    return results


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(label,keys,value):
        changed=copy.deepcopy(report);target=changed
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value
        try:validate(changed)
        except ValueError as error:controls.append(dict(name=label,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid heap source/evidence survived: '+label)
    changes=[('rom',('romSha256',),'0'*64),('processor',('processor',),'arm7'),('program',('program',),'child'),
        ('module',('module',),'itcm'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),
        ('runtime',('pinnedGeneratorAndRuntimeDependencies',),[]),('coverage',('newInitializedCoverageBytes',),848),
        ('helper-credit',('originalHelperDataExtentOrAssemblyCredit',),200),('module-claim',('wholeModuleLinked',),True),
        ('full-recovery',('sourceReconstructionComplete',),True),('denominator',('initializedDenominatorDelta',),424),
        ('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),
        ('flags',('matches',0,'compilerFlags'),[]),('blob',('matches',0,'originalObjectScaffolding'),True),
        ('exact',('matches',0,'exactAfterDeclaredRelocation'),False),('code-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),
        ('stack-argument',('matches',0,'sourceAbiContract','callerStackWords'),0),('arity',('matches',0,'sourceAbiContract','physicalArgumentWords'),4),
        ('direction-width',('matches',0,'sourceAbiContract','directionFormalBits'),32),('group-width',('matches',0,'sourceAbiContract','groupStoredBits'),16),
        ('model',('matches',0,'oracle','independentHeapModel'),False),('return-count',('matches',0,'oracle','actualOriginalAndCompiledReturns'),2240),
        ('scratch-unchecked',('matches',0,'oracle','allRawRegistersFlagsStackAndMappedMemoryCompared'),False),
        ('provider',('matches',0,'oracle','providerReplacements'),['heap']),('helper-source',('matches',0,'oracle','originalHelpersAdditionalSourceCredit'),1),
        ('historical-volatile',('matches',0,'sourceTypeHypothesis','originalHistoricalVolatileQualifierProven'),True),
        ('SDK-equivalence',('comparativeReference','publicSdkRevisionEquivalenceProven'),True),
        ('SDK-policy-adoption',('comparativeReference','publicAllocatorThresholdAndFillPolicyAdopted'),True),
        ('old-fixture-edit',('originalFixtureGenerator','untouched'),False),
        ('integer-symbol',('nativeSymbols','native_fn_0202ad78'),0x0202AD78),
        ('missing-object',('matches',0,'object'),'work/main-sdk-heap/absent-object.o'),
        ('missing-trace',('matches',0,'oracle','trace','path'),'work/main-sdk-heap/absent-trace.json.gz')]
    for label,keys,value in changes:reject(label,keys,value)
    negatives=wrong_sources(json.loads(matcher.PROFILE.read_text())['matches'][0])
    original=(ROOT/'extract/arm9/arm9.bin').read_bytes();body=(matcher.WORK/'caller/genuine-link/caller.bin').read_bytes()
    try:matcher.fixture.execute(original,body,0,budget=1)
    except AssertionError:controls.append(dict(name='exhausted-original-body-prefix',rejected=True,reason='Instruction cap reached without a normal return; post-state excluded'))
    else:raise ValueError('Exhausted native prefix acquired normal-return credit')
    validate(json.loads(matcher.REPORT.read_text()))
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,
        inputReportSha256=sha256(matcher.REPORT),metadataAndAvailabilityControls=controls,
        metadataAndAvailabilityControlCount=len(controls),compiledWrongSources=negatives,
        compiledWrongSourceControlCount=len(negatives),actualWrongSourceReturns=sum(row['actualWrongSourceReturns']for row in negatives),
        actualWrongSourceOriginalHelperReturnsSeparate=sum(row['actualOriginalHelperReturnsSeparate']for row in negatives),
        independentWrongSourceModelRejections=sum(row['independentModelRejections']for row in negatives),restoredPositive=True,
        currentSourceRebuiltBeforeValidation=True,staleObjectsOrOriginalCodeCompilerInputUsed=False,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),
        metadataControls=len(controls),wrongSourceControls=len(negatives),wrongSourceReturns=result['actualWrongSourceReturns'],
        independentRejections=result['independentWrongSourceModelRejections'])),flush=True)


if __name__=='__main__':main()
