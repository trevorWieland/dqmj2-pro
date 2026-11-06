import copy
import gzip
import hashlib
import json
from pathlib import Path
import qualify_arm7_core127_helper128_functional_20261101 as producer
from project import ROOT,sha256,write_json
PRODUCER_SHA='5a586e662bb984c8eb51506955b4f49224c47d9224a7228cc52512e18d936c2e'
CONTROLS=ROOT/'evidence/verification/arm7-core127-helper128-functional-controls-20261101.json'
_FRESH=None


def checked(name,digest):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Current helper128 functional input/product changed or unavailable')
    return path


def validate(report):
    global _FRESH
    checked(Path(producer.__file__).name,PRODUCER_SHA)
    if _FRESH is None:producer.main();_FRESH=json.loads(producer.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh virtual source/native/context/ABI/input proof differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    checked(report['source']['source'],report['source']['sourceSha256']);checked(report['source']['compiler'],report['source']['compilerSha256']);build=report['virtualBuild'];checked(build['object'],build['objectSha256']);folder=Path(build['object']).parent;checked(folder/'linked.elf',build['linkedElfSha256']);checked(folder/'caller.bin',build['linkedBodySha256']);getter=report['freshSourceGetter76'];checked(getter['source']['source'],getter['source']['sourceSha256']);checked(getter['source']['object'],getter['source']['objectSha256']);checked(getter['realLink']['lcf'],getter['realLink']['lcfSha256']);trace=report['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
    if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Helper128 deterministic trace differs')
    return dict(sourceDataOrDenominatorCredit=0)


def main():
    global _FRESH
    producer.main();report=json.loads(producer.REPORT.read_text());_FRESH=report;validate(report);controls=[];native_controls=[]
    def rejected(name,action,collection=controls):
        try:action()
        except(ValueError,FileNotFoundError)as error:collection.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False functional helper128 claim survived '+name)
    def changed(path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value;validate(bad)
    changes=[('generator',('generatorSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('original-entry',('originalAddress',),'0x27e9bdc'),('native-size',('nativeBytes',),136),('compiled-size',('compiledBytes',),128),('code',('compiledCodeBytes',),124),('pools',('compiledLiteralBytes',),12),('virtual',('virtualExecutionAddress',),'0x26d0004'),('source',('source','sourceSha256'),'0'*64),('compiler',('source','compilerSha256'),'0'*64),('flags',('source','compilerFlags'),[]),('link-argv',('virtualBuild','actualLinkerArgv'),[]),('source-admission',('sourceAdmissionAccepted',),True),('source-credit',('matchedSourceDataAndDenominatorCredit',),128),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('own-return',('actualOriginalAndCompiledOwnReturns',),384),('nested-as-top',('actualNestedHelperEventsSeparate',),0),('prefix-return',('constructorActualReturnCredit',),768),('raw-registers',('fullRawRegisterOrReadInterleavingEquivalenceClaimed',),True),('abi',('R0R3CalleeSavedSpLrFlagsAndAllNormalizedRamMatch',),False),('broad-normalization',('onlyActualTransferReturnLrStackSlotNormalized',),False),('write-model',('orderedWritesEquivalentAfterOnlyDeclaredLrNormalization',),False),('read-interleaving',('portReadOccursBeforePrivateSubtractionStoreInC',),False),('concurrency',('noAsynchronousPortOrConcurrencyEquivalenceClaimed',),False),('providers',('actualTransferByteGetterByteWriterAndStateGetterNoProviders',),False),('coverage',('allSupportedOwnedBranchAndInstructionCoverage',),False),('physical',('physicalHardwareOrGameReachabilityProven',),True),('getter-source',('freshSourceGetter76','source','sourceSha256'),'0'*64),('getter-credit',('freshSourceGetter76','additionalSourceCredit'),76),('missing-object',('virtualBuild','object'),'work/arm7-bulk-20261030/nohelper128.o'),('missing-trace',('trace','path'),'work/arm7-bulk-20261030/nohelper128.json.gz')]
    for name,path,value in changes:rejected(name,lambda path=path,value=value:changed(path,value))
    main_bytes=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();body=(producer.WORK/'virtual/caller.bin').read_bytes();case=producer.native.cases()[0]
    rejected('original-one-instruction-prefix',lambda:producer.native.run(main_bytes,wram,case,0,budget=1),native_controls);rejected('virtual-one-instruction-prefix',lambda:producer.native.run(main_bytes,wram,case,0,budget=1,body=body,entry=0x26d0000),native_controls)
    for key,value in [('mode',2),('flags',1),('sourceEnabled',1)]:
        bad=copy.deepcopy(report);bad[key]=value;rejected('undeclared-fixture-'+key,lambda bad=bad:validate(bad))
    text=(ROOT/report['source']['source']).read_text();wrong=[]
    for name,old,new in [('wrong-subtract-constant','(sp0 - 0x61) - 0x6100','(sp0 - 0x62) - 0x6100'),('wrong-getter-condition','() == 0x14','() == 0xA')]:
        if old not in text:raise ValueError('Wrong helper128 C mutation absent')
        folder=producer.WORK/name;wrong_body,build=producer.compiler.build(dict(report['source'],address='0x26d0000'),text.replace(old,new),folder,report['virtualBuild']['bindings'])
        if len(wrong_body)!=136:raise ValueError('Wrong virtual C escaped qualified136/116-code extent')
        records=[];rejects=0
        for index,test in enumerate(producer.native.cases()):
            result=producer.native.run(main_bytes,wram,test,index,body=wrong_body,entry=0x26d0000);records.append(dict(case=test,execution=result));rejects+=not result['modelPassed']
        if rejects==0:raise ValueError('Wrong helper128 C escaped independent private-word/port/flag model')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=folder/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wrong.append(dict(name=name,actualFreshSourceAndLink=build,actualWrongOwnReturns=len(records),independentModelRejections=rejects,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),sourceCredit=0))
    validate(json.loads(producer.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),producerSha256=PRODUCER_SHA,inputReportSha256=sha256(producer.REPORT),metadataControls=controls,metadataControlCount=len(controls),prefixAndDeclaredFixtureControls=native_controls,nativeControlCount=len(native_controls),compiledWrongSources=wrong,actualWrongOwnReturns=sum(x['actualWrongOwnReturns']for x in wrong),independentWrongSourceRejections=sum(x['independentModelRejections']for x in wrong),freshSourceOnlyDirectAndLinkedGetterBeforeValidation=True,restoredPositive=True,matchedSourceDataOrDenominatorCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),metadataControls=len(controls),nativeControls=len(native_controls),wrongReturns=result['actualWrongOwnReturns'],modelRejections=result['independentWrongSourceRejections'],sourceCredit=0)),flush=True)
if __name__=='__main__':main()
