import copy
import gzip
import json
from pathlib import Path
import match_main_sdk_dma_async152_20261101 as matcher
from project import write_json

ROOT=Path(__file__).resolve().parent
REPORT=matcher.REPORT
CONTROLS=ROOT/'evidence/verification/main-sdk-dma-async152-controls-20261101.json'
MATCHER_SHA='822a608726bfc7da212a3de09e00eb5aa45f9890b068a2a409c8df36f3f43d59'
_FRESH=None


def checked(name,sha):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or matcher.digest(path.read_bytes())!=sha:
        raise ValueError('Current DMA setup source/product missing or changed: '+str(name))
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=matcher.verify_inputs()
    names={Path(matcher.__file__).name,matcher.PROFILE.relative_to(ROOT).as_posix(),matcher.PINS.relative_to(ROOT).as_posix()}|{r['path']for r in pins}
    if {r['path']for r in report['generatorSources']}!=names or len(report['generatorSources'])!=len(names):
        raise ValueError('Complete DMA setup source/input/runtime closure differs')
    for row in report['generatorSources']:checked(row['path'],row['sha256'])
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins or report['romSha256']!=matcher.ROM:
        raise ValueError('Frozen DMA setup generator/runtime/build differs')
    expected={'processor':'arm9','program':'','module':'main','matchedInitializedBytes':152,'matchedInstructionBytes':152,
        'generatedLiteralBytes':0,'newOrdinaryFunctionCount':1,'newInitializedCoverageBytes':152,'originalHelperDataExtentOrAssemblyCredit':0,
        'initializedDenominatorDelta':0,'wholeModuleLinked':False,'sourceReconstructionComplete':False,
        'supportedContext':'idle channels0..3 register programming; sticky-busy and rejected-source bounded no-return separate'}
    if any(report.get(k)!=v for k,v in expected.items()):raise ValueError('Owned source/region/credit/context scope differs')
    if len(report['matches'])!=1:raise ValueError('One complete source unit required')
    if any(not isinstance(value,str)or value!=hex(int(value,0))for value in report['nativeSymbols'].values()):
        raise ValueError('Main nativeSymbols addresses must use canonical hex strings')
    row=report['matches'][0];pin=json.loads(matcher.PROFILE.read_text())['matches'][0]
    if any(row.get(k)!=v for k,v in pin.items()):raise ValueError('Current typed source/header/compiler identity differs')
    for n,k in[(row['source'],'sourceSha256'),(row['compiler'],'compilerSha256'),(row['object'],'objectSha256')]:checked(n,row[k])
    for item in row['sourceDependencies']:checked(item['path'],item['sha256'])
    link=row['realMainLink'];checked(link['linkedElf'],link['linkedElfSha256']);checked(link['lcf'],link['lcfSha256'])
    checked(str(matcher.WORK/'caller/genuine-link/caller.bin'),row['targetSha256'])
    for probe in link['bindingOnlyProbes']:checked(probe['object'],probe['objectSha256'])
    trace=row['oracle']['trace'];data=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if matcher.digest(gzip.decompress(data))!=trace['rawSha256']or data[4:8]!=bytes(4):
        raise ValueError('Fresh native trace changed or is not deterministic mtime-zero gzip')
    if _FRESH is None:_FRESH=json.loads(json.dumps(matcher.proof()))
    current={k:v for k,v in report.items()if k not in('schemaVersion','generator','generatorSha256','generatorSources',
        'pinnedGeneratorAndRuntimeDependencies','romSha256','processor','program','module')}
    if current!=_FRESH:raise ValueError('Fresh source/helper/return/state/no-return current-domain evidence differs')
    return {('arm9','','main',row['address'],'arm'):row}


def main():
    matcher.main();report=json.loads(REPORT.read_text());validate(report);controls=[]
    def reject(name,operation):
        try:operation()
        except Exception as error:controls.append({'name':name,'rejected':True,'exception':type(error).__name__,'reason':str(error)})
        else:raise ValueError('Invalid DMA setup source/proof accepted: '+name)
    changes=[('rom',('romSha256',),'0'*64),('processor',('processor',),'arm7'),('program',('program',),'child'),
        ('module',('module',),'itcm'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),
        ('runtime',('pinnedGeneratorAndRuntimeDependencies',),[]),('coverage-inflation',('newInitializedCoverageBytes',),500),
        ('helper-credit',('originalHelperDataExtentOrAssemblyCredit',),104),('module-link',('wholeModuleLinked',),True),
        ('full-recovery',('sourceReconstructionComplete',),True),('denominator',('initializedDenominatorDelta',),152),
        ('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),
        ('header',('matches',0,'sourceDependencies'),[]),('flags',('matches',0,'compilerFlags'),[]),
        ('blob',('matches',0,'originalObjectScaffolding'),True),('exact-gate',('matches',0,'exactAfterDeclaredRelocation'),False),
        ('code-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),
        ('arity',('matches',0,'sourceAbiContract','physicalArgumentWords'),4),
        ('caller-stack-erased',('matches',0,'sourceAbiContract','callerStackWords'),0),
        ('return-status-invented',('matches',0,'sourceAbiContract','return'),'u32-success-status'),
        ('bounds-guard-invented',('matches',0,'sourceAbiContract','nativeChannelBoundsGuardClaimed'),True),
        ('transfer-invented',('matches',0,'sourceAbiContract','registerShadowOnlyNoAutonomousTransfer'),False),
        ('callback-argument-erased',('matches',0,'sourceAbiContract','zeroLengthInvokesCallbackWithSixthWord'),False),
        ('immediate-nonzero-callback-invented',('matches',0,'sourceAbiContract','nonzeroLengthOnlyStoresCallback'),False),
        ('return-inflation',('matches',0,'oracle','actualOriginalAndCompiledReturns'),402),
        ('provider',('matches',0,'oracle','providerReplacements'),['dma']),
        ('budget-credit',('matches',0,'oracle','unsupportedReturnCredit'),1),
        ('busy-return-invented',('matches',0,'oracle','unsupportedControls',1,'actualReturn'),True),
        ('busy-post-state',('matches',0,'oracle','unsupportedControls',1,'postFaultOrBoundaryStateExcluded'),False),
        ('source-rejection-return-invented',('matches',0,'oracle','unsupportedControls',2,'actualReturn'),True),
        ('integer-address-publication',('nativeSymbols','native_fn_020088a4'),0x020088A4)]
    for name,keys,value in changes:
        changed=copy.deepcopy(report);target=changed
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value;reject(name,lambda changed=changed:validate(changed))
    row=report['matches'][0]
    for name,path in[('missing-object',ROOT/row['object']),('missing-linked-body',matcher.WORK/'caller/genuine-link/caller.bin'),
        ('missing-native-trace',ROOT/row['oracle']['trace']['path'])]:
        saved=path.read_bytes()
        try:path.unlink();reject(name,lambda:validate(report))
        finally:path.write_bytes(saved)
    pin=json.loads(matcher.PROFILE.read_text())['matches'][0]
    for name,before,after in [('wrong-zero-length-test','bytes == 0','bytes != 0'),
        ('wrong-count-shift','bytes >> 2','bytes >> 1'),
        ('callback-IRQ-removed','0xC4000000','0x84000000'),
        ('wrong-direct-callback-argument','callback(argument)','callback(0)'),
        ('source-destination-swapped','channel,source,destination,','channel,destination,(void *)source,')]:
        text=(ROOT/pin['source']).read_text()
        if before not in text:raise ValueError('Expected typed ordinary C expression absent')
        directory=matcher.WORK/'controls'/name;directory.mkdir(parents=True,exist_ok=True)
        header=directory/'native_dma_types.h';header.write_bytes((ROOT/pin['sourceDependencies'][0]['path']).read_bytes())
        source=directory/Path(pin['source']).name;source.write_text(text.replace(before,after))
        changed=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=matcher.digest(source.read_bytes()),
            sourceDependencies=[dict(path=header.relative_to(ROOT).as_posix(),sha256=matcher.digest(header.read_bytes()))])
        reject('fresh-C-'+name,lambda changed=changed:matcher.build(changed))
    reject('partial-body-execution',lambda:matcher.fixture.engine.setup({0x0200867C:b'1234'},0))
    matcher.build(pin);validate(report)
    result={'schemaVersion':1,'generator':Path(__file__).name,'generatorSha256':matcher.digest(Path(__file__).read_bytes()),
        'report':REPORT.relative_to(ROOT).as_posix(),'reportSha256':matcher.digest(REPORT.read_bytes()),'controls':controls,
        'allPassed':all(row['rejected']for row in controls),'newSourceBytes':152,'producerBeforeProductChecks':True,
        'oldSourcesAndSharedStateUnchanged':True}
    write_json(CONTROLS,result);print(json.dumps({'report':CONTROLS.relative_to(ROOT).as_posix(),'sha256':matcher.digest(CONTROLS.read_bytes()),
        'controls':len(controls),'allPassed':result['allPassed']}),flush=True)


if __name__=='__main__':main()
