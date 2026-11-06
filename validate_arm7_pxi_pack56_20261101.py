import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_pxi_pack56_20261101 as matcher
from project import ROOT,sha256,write_json
MATCHER_SHA='9a2892d859230beea94464eb13bcd111f122c40ef0864fc312e28d199a5c1b48'
CONTROLS=ROOT/'evidence/verification/arm7-pxi-pack56-controls-20261101.json'
_FRESH=None

def checked(name,expected):
    p=(ROOT/name).resolve()
    if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=expected:raise ValueError('Required PXI source/product missing or changed')
    return p

def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name,MATCHER_SHA);pins=json.loads(matcher.PINS.read_text())['files'];names={Path(matcher.__file__).name,matcher.PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins}
    if report['generatorSha256']!=MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies']!=pins or len(report['generatorSources'])!=len(names)or {x['path']for x in report['generatorSources']}!=names:raise ValueError('Complete frozen PXI source/runtime closure differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    row=report['matches'][0]
    for item,directory in[(row,matcher.WORK/'newUnit'),(report['sourceLinkedExistingDependency']['compilerResult'],matcher.WORK/'existingSelectedSourceDependency')]:
        checked(item['source'],item['sourceSha256']);checked(item['compiler'],item['compilerSha256']);checked(item['object'],item['objectSha256'])
        for dependency in item['sourceDependencies']:checked(dependency['path'],dependency['sha256'])
        link=item.get('realLink')or report['sourceLinkedExistingDependency']['realLink'];checked(link['lcf'],link['lcfSha256']);checked(directory/'real-link/linked.elf',link['linkedElfSha256']);checked(directory/'real-link/caller.bin',item['targetSha256'])
    trace=row['oracle']['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic complete PXI trace differs')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only compile/link/native/model evidence differs')
    return {('arm7','','arm7-wram','0x37fe410','arm'):row}

def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(name,keys,value):
        bad=copy.deepcopy(report);target=bad
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid PXI evidence survived: '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-main'),('mode',('matches',0,'mode'),'thumb'),('address',('matches',0,'address'),'0x37fe414'),('size',('matches',0,'bytes'),52),
        ('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('duplicate-count',('newOrdinaryFunctionCount',),2),('duplicate-bytes',('matchedInitializedBytes',),152),('code',('matchedCodeBytes',),152),('literal',('generatedLiteralBytes',),4),('denominator',('initializedDenominatorDelta',),96),('data-credit',('originalDataHelperAssemblyOrExtentCredit',),96),('module-credit',('wholeModuleLinked',),True),('full-source',('sourceReconstructionComplete',),True),
        ('source',('matches',0,'sourceSha256'),'0'*64),('flags',('matches',0,'compilerFlags'),[]),('header',('matches',0,'sourceDependencies'),[]),('blob',('matches',0,'originalObjectScaffolding'),True),('exact',('matches',0,'exactAfterDeclaredRelocation'),False),('fourth-arg',('matches',0,'sourceAbiContract','physicalArgumentWords'),4),('fourth-needed',('matches',0,'sourceAbiContract','semanticFourthArgumentRequired'),True),('field-init',('matches',0,'sourceAbiContract','fullyAssignedBitfieldsBeforeWordRead'),False),('compatible-word',('matches',0,'sourceAbiContract','compatibleWordMessageClosure'),False),('erase-scratch-read',('matches',0,'sourceAbiContract','nativeTransientScratchR3ReadRecorded'),False),
        ('model',('matches',0,'oracle','independentFullMappedMemoryStackOrderedEffectsAndPackedWordModel'),False),('machine',('matches',0,'oracle','rawRegistersFlagsStackModeAndMappedMemoryCompared'),False),('own-returns',('actualOuterReturns',),6144),('sender-credit',('sourceLinkedExistingDependency','additionalFunctionOrByteCredit'),96),('sender-selection',('sourceLinkedExistingDependency','existingSourceSelectionPreserved'),False),('sender-source',('sourceLinkedExistingDependency','compilerResult','sourceSha256'),'0'*64),('sender-flags',('sourceLinkedExistingDependency','compilerResult','compilerFlags'),[]),
        ('sender-source-linked',('matches',0,'oracle','sourceLinkedExistingSender'),False),('sender-returns',('actualExistingSourceSenderReturnsSeparateZeroCredit',),0),('irq-returns',('actualOriginalIrqReturnsSeparateZeroCredit',),0),('r3-groups',('matches',0,'oracle','incomingR3VariationGroups'),0),('r3-padding',('matches',0,'oracle','transientFirstPaddingWritePreservedButExcludedFromSemanticR3Invariance'),False),('providers',('matches',0,'oracle','providerReplacements'),['send']),('physical-hardware',('matches',0,'oracle','physicalPeripheralExecution'),True),('scene',('matches',0,'oracle','wholeSceneOrHardwareContextProven'),True),('result-paths',('matches',0,'oracle','allThreeSenderResults'),[0]),
        ('binding',('nativeSymbols','native_host_arm7_arm_037fe448'),'0x37fe44c'),('missing-object',('matches',0,'object'),'work/arm7-bulk-20261030/absent-pxi-pack56.o'),('missing-dependency-object',('sourceLinkedExistingDependency','compilerResult','object'),'work/arm7-bulk-20261030/absent-pxi-dependency96.o'),('missing-trace',('matches',0,'oracle','trace','path'),'work/arm7-bulk-20261030/absent-pxi-pack56.json.gz')]
    for name,keys,value in changes:reject(name,keys,value)
    profile=json.loads((matcher.SOURCE/'profile.json').read_text());seed=profile['newUnit'];text=(ROOT/seed['source']).read_text();header=ROOT/seed['sourceDependencies'][0]['path'];existing=(matcher.WORK/'existingSelectedSourceDependency/real-link/caller.bin').read_bytes();original=(ROOT/seed['binary']).read_bytes();wrong=[]
    definitions=[('payload-as-tag',text.replace('unk_00_0 = tag;','unk_00_0 = payload;'),lambda c:bool((c['tag']^c['payload'])&31)),('payload-as-error',text.replace('unk_00_5 = error;','unk_00_5 = payload;'),lambda c:bool((c['payload']^c['error'])&1))]
    for name,source_text,predicate in definitions:
        source=ROOT/('generated/arm7-pxi-pack56-controls-20261101/'+name+'/native_arm7_wram_037fe410.c');source.parent.mkdir(parents=True,exist_ok=True);source.write_text(source_text,encoding='utf-8');(source.parent/'native_pxi_types.h').write_bytes(header.read_bytes())
        bad,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if len(body)!=56 or comparison.get('exactLinkedBytes'):raise ValueError('Wrong packer matched or escaped its complete extent')
        records=[];rejections=0
        for case in matcher.native.cases():
            value=matcher.native.execute(original,body,existing,case);records.append(value);rejections+=not value['modelPassed']
        expected=sum(predicate(c)for c in matcher.native.cases())
        if rejections!=expected or not expected:raise ValueError('Wrong bitfield model rejection count differs')
        data=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
        wrong.append(dict(name=name,compilerResult=bad,genuineLinkComparison=comparison,actualOwnReturns=1536,existingSourceSenderReturnsSeparateZeroCredit=1536,originalIrqReturnsSeparateZeroCredit=2048,independentModelRejections=rejections,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(data).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    exhausted=matcher.native.execute(original,(matcher.WORK/'newUnit/real-link/caller.bin').read_bytes(),existing,matcher.native.cases()[0],budget=1,allow_no_return=True)
    if exhausted['actualOuterReturn']or exhausted['actualNestedReturns']:raise ValueError('Prefix acquired return credit')
    controls.append(dict(name='bounded-exhaustion',rejected=True,reason='Prefix did not return; post-state excluded'))
    validate(json.loads(matcher.REPORT.read_text()))
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=3072,existingSourceSenderReturnsSeparateZeroCredit=3072,originalIrqReturnsSeparateZeroCredit=4096,independentWrongSourceRejections=sum(x['independentModelRejections']for x in wrong),sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),metadataControls=len(controls),wrongOwnReturns=3072,modelRejections=result['independentWrongSourceRejections'])),flush=True)
if __name__=='__main__':main()
