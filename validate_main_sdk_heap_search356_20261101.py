import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_main_sdk_heap_search356_20261101 as matcher
from project import ROOT,sha256,write_json

CONTROLS=ROOT/'evidence/verification/main-sdk-heap-search356-controls-20261101.json'
MATCHER_SHA='e1c989eaa24844c237226ba3015c1a1b3beb1011e8f1c65945b41ad865793207'
_FRESH=None


def checked(name,expected):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=expected:
        raise ValueError('Required current search source/product missing or changed')
    return path


def check_link(row,directory):
    checked(row['object'],row['objectSha256']);link=row['realMainLink']
    checked(link['linkedElf'],link['linkedElfSha256']);checked(link['lcf'],link['lcfSha256'])
    checked(directory/'genuine-link/caller.bin',row['targetSha256'])
    for probe in link['bindingOnlyProbes']:checked(probe['object'],probe['objectSha256'])


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=matcher.verify_inputs()
    names={Path(matcher.__file__).name,'main_sdk_heap_attribute424_compile_20261101.py',
        'main_sdk_heap_search356_native_20261101.py',matcher.PROFILE.relative_to(ROOT).as_posix(),matcher.PINS.relative_to(ROOT).as_posix()}
    names.update(item['path']for item in json.loads(matcher.PINS.read_text())['files'])
    if {item['path']for item in report['generatorSources']}!=names or len(report['generatorSources'])!=len(names):
        raise ValueError('Complete search source/runtime/reference closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    if report['generatorSha256']!=MATCHER_SHA or report['romSha256']!=matcher.ROM or report['pinnedGeneratorAndRuntimeDependencies']!=json.loads(matcher.PINS.read_text())['files']:
        raise ValueError('Frozen search generator/build/runtime provenance differs')
    expected=dict(processor='arm9',program='',module='main',matchedInitializedBytes=356,matchedInstructionBytes=356,
        generatedLiteralBytes=0,newOrdinaryFunctionCount=2,newInitializedCoverageBytes=356,originalHelperDataExtentOrAssemblyCredit=0,
        initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False)
    if any(report.get(key)!=value for key,value in expected.items())or len(report['matches'])!=2:
        raise ValueError('Search identity/ordinary-source/coverage scope differs')
    for row,pin in zip(report['matches'],pins):
        if any(row.get(key)!=value for key,value in pin.items()):raise ValueError('Search source/compiler/qualified boundary differs')
        for path,key in[(row['source'],'sourceSha256'),(row['compiler'],'compilerSha256')]:checked(path,row[key])
        check_link(row,matcher.WORK/pin['address'])
        for item in(row['nativeSymbols'],report['nativeSymbols']):
            if any(not isinstance(value,str)or value!=hex(int(value,0))for value in item.values()):
                raise ValueError('Main nativeSymbols require canonical hex strings')
        trace=row['oracle']['trace'];data=checked(trace['path'],trace['compressedSha256']).read_bytes()
        if data[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(data)).hexdigest()!=trace['rawSha256']:
            raise ValueError('Current native search trace differs or is not mtime-zero gzip')
    dep=report['sourceLinkedCommit424'];check_link(dict(dep['entry'],realMainLink=dep['realMainLink']),matcher.WORK/'source-linked-commit424')
    if _FRESH is None:_FRESH=json.loads(json.dumps(matcher.proof()))
    current={key:value for key,value in report.items()if key not in('schemaVersion','generator','generatorSha256','generatorSources',
        'pinnedGeneratorAndRuntimeDependencies','romSha256','processor','program','module')}
    if current!=_FRESH:raise ValueError('Fresh source-only links/full native model/CPU/memory evidence differ')
    return {('arm9','','main',row['address'],'arm'):row for row in report['matches']}


def wrong_sources(pins):
    results=[];commit=(matcher.WORK/'source-linked-commit424/genuine-link/caller.bin').read_bytes()
    for pin in pins:
        text=(ROOT/pin['source']).read_text();address=int(pin['address'],0);direction=int(address==0x0202B0F8)
        changes=[('wrong-first-best-mode','heap_mode(exp) == 0','heap_mode(exp) != 0'),
            ('wrong-direction',f',bytes,{direction});',f',bytes,{1-direction});')]
        for name,old,new in changes:
            label=pin['address']+'-'+name
            if text.count(old)!=1:raise ValueError('Expected ordinary search source control absent or ambiguous')
            source=ROOT/'generated/main-sdk-heap-search356-negative-20261101'/label/Path(pin['source']).name
            source.parent.mkdir(parents=True,exist_ok=True);source.write_text(text.replace(old,new))
            dependencies=[]
            for item in pin['sourceDependencies']:
                header=source.parent/Path(item['path']).name;header.write_bytes((ROOT/item['path']).read_bytes())
                dependencies.append(dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header)))
            bad=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=dependencies,variant=label)
            directory=matcher.WORK/'wrong-source'/label
            entry,bindings,link,mismatch,code=matcher.compiler.build(bad,directory,strict=False)
            if link is not None:raise ValueError('Wrong ordinary search C unexpectedly matched the original')
            result=matcher.fixture.wrong_body(ROOT,directory,address,code,commit,label)
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
        else:raise ValueError('Invalid search source/evidence survived: '+label)
    changes=[('rom',('romSha256',),'0'*64),('processor',('processor',),'arm7'),('program',('program',),'child'),
        ('module',('module',),'itcm'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),
        ('runtime',('pinnedGeneratorAndRuntimeDependencies',),[]),('coverage',('newInitializedCoverageBytes',),780),
        ('helper-credit',('originalHelperDataExtentOrAssemblyCredit',),424),('module-claim',('wholeModuleLinked',),True),
        ('full-recovery',('sourceReconstructionComplete',),True),('denominator',('initializedDenominatorDelta',),356),
        ('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),
        ('flags',('matches',0,'compilerFlags'),[]),('blob',('matches',0,'originalObjectScaffolding'),True),
        ('exact',('matches',0,'exactAfterDeclaredRelocation'),False),('code-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),
        ('arity',('matches',0,'sourceAbiContract','physicalArgumentWords'),5),
        ('signed-alignment',('matches',0,'sourceAbiContract','alignmentFormalSigned'),False),
        ('alignment-domain',('matches',0,'sourceAbiContract','formalZeroNegativeOrNonPowerAlignmentProven'),True),
        ('object-extent',('matches',0,'sourceTypeHypothesis','originalTotalHeapObjectExtentProven'),True),
        ('model',('matches',0,'oracle','independentMultiBlockHeapModel'),False),
        ('return-count',('matches',1,'oracle','actualOriginalAndCompiledReturns'),2240),
        ('unchecked-state',('matches',1,'oracle','fullRawRegistersFlagsStackMemoryReadsWritesAndFifthWordCompared'),False),
        ('provider',('matches',0,'oracle','providerReplacements'),['commit']),
        ('callee-credit',('sourceLinkedCommit424','additionalSourceCredit'),424),
        ('callee-source',('sourceLinkedCommit424','entry','sourceSha256'),'0'*64),
        ('nonfirst-selection',('matches',0,'oracle','selectedBeyondFirstTraversalNodeCases'),0),
        ('integer-symbol',('nativeSymbols','native_fn_0202ae9c'),0x0202AE9C),
        ('missing-object',('matches',0,'object'),'work/main-sdk-heap/absent-search-object.o'),
        ('missing-linked-callee',('sourceLinkedCommit424','entry','object'),'work/main-sdk-heap/absent-commit-object.o'),
        ('missing-trace',('matches',1,'oracle','trace','path'),'work/main-sdk-heap/absent-search-trace.json.gz')]
    for label,keys,value in changes:reject(label,keys,value)
    negatives=wrong_sources(json.loads(matcher.PROFILE.read_text())['matches'])
    original=(ROOT/'extract/arm9/arm9.bin').read_bytes();body=(matcher.WORK/'0x202b044/genuine-link/caller.bin').read_bytes()
    commit=(matcher.WORK/'source-linked-commit424/genuine-link/caller.bin').read_bytes()
    try:matcher.fixture.execute(original,0x0202B044,body,commit,1,budget=1)
    except ValueError:controls.append(dict(name='exhausted-original-body-prefix',rejected=True,reason='Instruction cap reached without normal return; post-state excluded'))
    else:raise ValueError('Exhausted native prefix acquired normal-return credit')
    validate(json.loads(matcher.REPORT.read_text()))
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,
        inputReportSha256=sha256(matcher.REPORT),metadataAndAvailabilityControls=controls,metadataAndAvailabilityControlCount=len(controls),
        compiledWrongSources=negatives,compiledWrongSourceControlCount=len(negatives),
        actualWrongSourceReturns=sum(row['actualWrongSourceReturns']for row in negatives),
        independentWrongSourceModelRejections=sum(row['independentModelRejections']for row in negatives),
        restoredPositive=True,currentSourcesAndLinkedCalleeRebuiltBeforeValidation=True,staleObjectsOrOriginalCodeCompilerInputUsed=False,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),
        metadataControls=len(controls),wrongSourceControls=len(negatives),wrongSourceReturns=result['actualWrongSourceReturns'],
        independentRejections=result['independentWrongSourceModelRejections'])),flush=True)


if __name__=='__main__':main()
