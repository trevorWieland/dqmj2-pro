import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_main_sdk_lock_pair_20261101 as matcher
from project import write_json

ROOT=Path(__file__).resolve().parent
REPORT=matcher.REPORT
CONTROLS=ROOT/'evidence/verification/main-sdk-lock-pair-controls-20261101.json'
MATCHER_SHA='f67808f79bd84ca3db6f81ea82e2475f0a77cc077ee7ebfd3f4a503a26307fd7'
_FRESH=None


def checked(name,sha):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or matcher.digest(path.read_bytes())!=sha:
        raise ValueError('Current main SDK source/product missing or changed: '+str(name))
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=matcher.verify_inputs()
    names={Path(matcher.__file__).name,matcher.PROFILE.relative_to(ROOT).as_posix(),matcher.PINS.relative_to(ROOT).as_posix()}|{r['path']for r in pins}
    if {r['path']for r in report['generatorSources']}!=names or len(report['generatorSources'])!=len(names):
        raise ValueError('Complete current SDK source/generator/runtime closure differs')
    for row in report['generatorSources']:checked(row['path'],row['sha256'])
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins or report['romSha256']!=matcher.ROM:
        raise ValueError('Frozen main SDK generator/runtime/build identity differs')
    expected={'processor':'arm9','program':'','module':'main','matchedInitializedBytes':224,'matchedInstructionBytes':224,
        'generatedLiteralBytes':0,'newOrdinaryFunctionCount':2,'newInitializedCoverageBytes':224,'originalHelperOrCallbackSourceCredit':0,
        'originalDataOrExtentOrPaddingCredit':0,'ordinaryAssemblyOrBlobCredit':0,'wholeModuleLinked':False,
        'sourceReconstructionComplete':False,'initializedDenominatorDelta':0}
    if any(report.get(k)!=v for k,v in expected.items()):raise ValueError('Main SDK source/code/pool/credit scope differs')
    rows=report['matches'];profile=json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows)!=2:raise ValueError('Two complete independently owned lock source units required')
    for row,pin in zip(rows,profile):
        if any(row.get(k)!=v for k,v in pin.items()):raise ValueError('Main lock C/header/compiler/target identity differs')
        for n,k in[(row['source'],'sourceSha256'),(row['compiler'],'compilerSha256'),(row['object'],'objectSha256')]:checked(n,row[k])
        for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
        link=row['realMainLink'];checked(link['linkedElf'],link['linkedElfSha256']);checked(link['lcf'],link['lcfSha256'])
        checked(str(matcher.WORK/row['address']/'real-link/caller.bin'),row['targetSha256'])
        for probe in link['bindingOnlyProbes']:checked(probe['object'],probe['objectSha256'])
        if not row['oracle']['sharedSuiteCountsMustNotBeSummedPerRow']:
            raise ValueError('Two rows may not each claim the full shared-suite return count')
    trace=report['nativeStateModel']['trace'];data=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if matcher.digest(gzip.decompress(data))!=trace['rawSha256']or data[4:8]!=bytes(4):
        raise ValueError('Fresh raw/compressed native proof differs')
    if _FRESH is None:_FRESH=json.loads(json.dumps(matcher.proof()))
    current={k:v for k,v in report.items()if k not in('schemaVersion','generator','generatorSha256','generatorSources',
        'pinnedGeneratorAndRuntimeDependencies','romSha256','processor','program','module')}
    if current!=_FRESH:raise ValueError('Fresh exact C/native/helper/record/callback/mask proof differs')
    return {('arm9','','main',row['address'],'arm'):row for row in rows}


def main():
    matcher.main();report=json.loads(REPORT.read_text());validate(report);controls=[]
    def reject(name,operation):
        try:operation()
        except Exception as error:controls.append({'name':name,'rejected':True,'exception':type(error).__name__,'reason':str(error)})
        else:raise ValueError('Invalid main SDK source/proof accepted: '+name)
    changes=[('rom',('romSha256',),'0'*64),('processor',('processor',),'arm7'),('program',('program',),'child'),
        ('module',('module',),'itcm'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),
        ('runtime',('pinnedGeneratorAndRuntimeDependencies',),[]),('coverage-inflation',('newInitializedCoverageBytes',),500),
        ('callback-credit',('originalHelperOrCallbackSourceCredit',),8),('padding-credit',('originalDataOrExtentOrPaddingCredit',),2),
        ('assembly-credit',('ordinaryAssemblyOrBlobCredit',),8),('module-link-claim',('wholeModuleLinked',),True),
        ('full-recovery-claim',('sourceReconstructionComplete',),True),('denominator',('initializedDenominatorDelta',),224),
        ('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),
        ('header',('matches',0,'sourceDependencies'),[]),('flags',('matches',0,'compilerFlags'),[]),
        ('blob',('matches',0,'originalObjectScaffolding'),True),('exact-gate',('matches',0,'exactAfterDeclaredRelocation'),False),
        ('code-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),
        ('id-narrowing',('matches',0,'sourceAbiContract','idAndSwapWordBits'),16),
        ('owner-width',('matches',0,'sourceAbiContract','ownerStoreBits'),32),
        ('object-extent',('matches',0,'sourceAbiContract','originalObjectExtentOrPaddingClaimed'),True),
        ('callback-args-erased',('matches',0,'sourceAbiContract','callback'),'arbitrary callback ABI supported'),
        ('helper-patched',('matches',0,'nativeCalleeSourceCredit'),8),
        ('own-return-inflation',('matches',0,'oracle','actualOriginalAndCompiledReturns'),2376),
        ('shared-double-credit',('matches',0,'oracle','sharedSuiteCountsMustNotBeSummedPerRow'),False),
        ('model-return-inflation',('nativeStateModel','actualOriginalAndCompiledReturns'),4752),
        ('callback-FIQ-erased',('nativeStateModel','callbackCanRetainFiqDisableUnderIrqOnlyRestore'),False),
        ('provider',('nativeStateModel','providerReplacements'),['swap']),('budget-credit',('nativeStateModel','unsupportedReturnCredit'),1)]
    for name,keys,value in changes:
        changed=copy.deepcopy(report);target=changed
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value;reject(name,lambda changed=changed:validate(changed))
    products=[('missing-own-object',ROOT/report['matches'][0]['object']),
        ('missing-other-body',matcher.WORK/report['matches'][1]['address']/'real-link/caller.bin'),
        ('missing-trace',ROOT/report['nativeStateModel']['trace']['path'])]
    for name,path in products:
        saved=path.read_bytes()
        try:path.unlink();reject(name,lambda:validate(report))
        finally:path.write_bytes(saved)
    profile=json.loads(matcher.PROFILE.read_text())['matches']
    variants=[(0,'wrong-release-sentinel','0xFFFFFFFEU','0xFFFFFFFFU'),
        (0,'wrong-release-owner','record->owner = 0;','record->owner = 1;'),
        (0,'wrong-release-flag-value','    record->flag = 0;','    record->flag = 1;'),
        (1,'reverse-previous-flag-test','if (result == 0)','if (result != 0)'),
        (1,'wrong-owner-bits','(u16)identity','(u16)(identity >> 16)')]
    for index,name,before,after in variants:
        pin=profile[index];text=(ROOT/pin['source']).read_text()
        if before not in text:raise ValueError('Expected ordinary C lock expression absent')
        directory=matcher.WORK/'controls'/name;directory.mkdir(parents=True,exist_ok=True)
        original=ROOT/pin['sourceDependencies'][0]['path'];header=directory/original.name;header.write_bytes(original.read_bytes())
        source=directory/Path(pin['source']).name;source.write_text(text.replace(before,after))
        changed=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=matcher.digest(source.read_bytes()),
            sourceDependencies=[dict(path=header.relative_to(ROOT).as_posix(),sha256=matcher.digest(header.read_bytes()))])
        reject('fresh-C-'+name,lambda changed=changed:matcher.build(changed))
    reject('partial-source-body-installation',lambda:matcher.fixture.engine.setup({0x02005F08:b'1234'},0))
    for pin in profile:matcher.build(pin)
    validate(report)
    result={'schemaVersion':1,'generator':Path(__file__).name,'generatorSha256':matcher.digest(Path(__file__).read_bytes()),
        'report':REPORT.relative_to(ROOT).as_posix(),'reportSha256':matcher.digest(REPORT.read_bytes()),'controls':controls,
        'allPassed':all(row['rejected']for row in controls),'newFunctions':2,'newSourceBytes':224,
        'producerBeforeCurrentProductChecks':True,'allOldAcceptedSourcesAndSharedStateUnchanged':True}
    write_json(CONTROLS,result)
    print(json.dumps({'report':CONTROLS.relative_to(ROOT).as_posix(),'sha256':matcher.digest(CONTROLS.read_bytes()),
        'controls':len(controls),'allPassed':result['allPassed']}),flush=True)


if __name__=='__main__':
    main()
