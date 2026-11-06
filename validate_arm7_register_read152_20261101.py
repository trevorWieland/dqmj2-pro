import copy
import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_register_read152_20261101 as matcher
from project import ROOT,sha256,write_json

MATCHER_SHA='b33e1c36cc071927faf5afce9f0d1c70be179d0747fee9f14a7556e2b45358a2'
CONTROLS=ROOT/'evidence/verification/arm7-register-read152-controls-20261101.json'
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
        for field in ('readerTrace','directHelperTrace'):
            trace=row['oracle'][field];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
            if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Register-read trace differs or has nonzero gzip mtime')
    if _FRESH is None:matcher.main();_FRESH=json.loads(matcher.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh source-only pair link/native/direct/bus/source evidence differs')
    return {('arm7','','arm7-wram',row['address'],'arm'):row for row in report['matches']}


def main():
    matcher.main();report=json.loads(matcher.REPORT.read_text());validate(report);controls=[]
    def reject(name,keys,value):
        bad=copy.deepcopy(report);target=bad
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value
        try:validate(bad)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid register-read source evidence survived: '+name)
    changes=[('rom',('romSha256',),'0'*64),('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-main'),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('count',('newOrdinaryFunctionCount',),1),('bytes',('matchedInitializedBytes',),304),('code',('matchedCodeBytes',),152),('literal',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),152),('data-credit',('originalDataHelperAssemblyOrExtentCredit',),4),('module-credit',('wholeModuleLinked',),True),('whole-source',('sourceReconstructionComplete',),True),('returns',('totalActualOwnedReturns',),8250),('helper-returns',('helperOwnReturns',),1160),('reader-returns',('readerOwnReturns',),580),('binding',('nativeSymbols','native_host_arm7_arm_03804c58'),'0x3804c7c')]
    for name,keys,value in changes:reject(name,keys,value)
    for i in range(2):
        prefix=('matches',i)
        for name,keys,value in [('address',('address',),'0x3804c5c'),('mode',('mode',),'thumb'),('source',('sourceSha256',),'0'*64),('flags',('compilerFlags',),[]),('header',('sourceDependencies',),[]),('original-blob',('originalObjectScaffolding',),True),('exact',('exactBytes',),False),('one-word-abi',('sourceAbiContract','physicalArgumentWords'),0),('historical-type',('sourceAbiContract','historicalTypesProven'),True),('model',('oracle','independentFullMemoryStackHalfwordStoreAndReturnModel'),False),('raw-state',('oracle','rawRegistersFlagsStackModeAndMappedMemoryCompared'),False),('providers',('oracle','providerReplacements'),['data']),('physical-peripheral',('oracle','syntheticReadBoundary','physicalPeripheralExecution'),True),('mmio-width',('oracle','fixedMmioAddressRoles','width'),4),('code-word-admission',('oracle','fixedMmioAddressRoles','noArbitraryCodeWordOrDataAdmission'),False),('callee-source',('oracle','sourceLinkedOwnedPair'),False),('missing-object',('object',),'work/arm7-bulk-20261030/absent-register-read.o'),('missing-trace',('oracle','readerTrace','path'),'work/arm7-bulk-20261030/absent-register-read.json.gz')]:reject(str(i)+'-'+name,prefix+keys,value)
    seeds=json.loads((matcher.SOURCE/'profile.json').read_text())['units'];original=(ROOT/seeds[0]['binary']).read_bytes();helper_body=(matcher.WORK/seeds[0]['address'][2:]/'real-link/caller.bin').read_bytes();reader_body=(matcher.WORK/seeds[1]['address'][2:]/'real-link/caller.bin').read_bytes();wrong=[]
    for name,index,old,new,expected in [('unmasked-helper',0,'(u8)selector','(u16)selector',2331),('wide-result',1,'return (u8)','return (u16)',399)]:
        seed=seeds[index];source_text=(ROOT/seed['source']).read_text();assert old in source_text;source=ROOT/('generated/arm7-register-read152-controls-20261101/'+name+'/'+Path(seed['source']).name);source.parent.mkdir(parents=True,exist_ok=True);source.write_text(source_text.replace(old,new),encoding='utf-8')
        header=ROOT/seed['sourceDependencies'][0]['path'];(source.parent/header.name).write_bytes(header.read_bytes());bad,comparison,body=matcher.compile_unit(seed,source,matcher.WORK/name,strict=False)
        if comparison.get('exactLinkedBytes'):raise ValueError('Wrong register C unexpectedly matched')
        rows=[];rejections=0
        if index==0:
            if bad['relocations']:raise ValueError('Position-independent wrong helper acquired external fixups')
            for n,case in enumerate(matcher.direct.cases()):
                value=matcher.direct.execute(original,body,case,n,virtual=True);rows.append(value);rejections+=not value['modelPassed']
        else:
            for n,case in enumerate(matcher.native.cases()):
                value=matcher.native.execute(original,body,helper_body,case,n);rows.append(value);rejections+=not value['modelPassed']
        if rejections!=expected:raise ValueError('Wrong register C model rejection count differs: '+name+':'+str(rejections))
        raw=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode();trace=matcher.WORK/name/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
        wrong.append(dict(name=name,compilerResult=bad,genuineLinkComparison=comparison,actualOwnReturns=len(rows),independentModelRejections=rejections,noOriginalTailOrHelperDelegation=True,positionIndependentWrongHelperVirtualExecution=index==0,virtualHelperJustification='Zero relocation leaf, sole PC-relative literal travels with source code, full code guard and halfword model'if index==0 else None,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    for name,case,budget in [('stuck-helper',dict(matcher.direct.cases()[0],stuck=True),300),('helper-prefix',matcher.direct.cases()[0],1)]:
        value=matcher.direct.execute(original,helper_body,case,0,budget=budget,allow_no_return=True)
        if value['actualReturn']:raise ValueError('Helper exhaustion acquired return credit')
        controls.append(dict(name=name,rejected=True,execution=value))
    validate(json.loads(matcher.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),matcherSha256=MATCHER_SHA,inputReportSha256=sha256(matcher.REPORT),metadataControls=controls,metadataControlCount=len(controls),compiledWrongSources=wrong,actualWrongOwnReturns=2965,independentWrongSourceRejections=2730,sourceOnlyFreshCompileBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0)
    write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),controls=len(controls),wrongReturns=2965,modelRejections=2730)),flush=True)
if __name__=='__main__':main()
