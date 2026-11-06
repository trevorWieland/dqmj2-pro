import copy
import gzip
import hashlib
import json
from pathlib import Path
import qualify_arm7_core119_pair188_functional_20261101 as producer
import arm7_core117_wrong_c_20261101 as wrong_compiler
from project import ROOT,sha256,write_json
PRODUCER_SHA='20607a9757d5e6faa2eb8d3b3627b77cbb23d85c9ddff8a064bf336625a39ce6'
WRONG_COMPILER_SHA='66ced44dca372cb3cd80d1199b09835020f603ab6251442535cdd0ff3346d386'
CONTROLS=ROOT/'evidence/verification/arm7-core119-pair188-functional-controls-20261101.json'
_FRESH=None


def checked(name,digest):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Current typed functional input/product missing or changed')
    return path


def validate(report):
    global _FRESH
    checked(Path(producer.__file__).name,PRODUCER_SHA)
    if _FRESH is None:producer.main();_FRESH=json.loads(producer.REPORT.read_text())
    if report!=_FRESH:raise ValueError('Fresh typed source/direct/connected native proof differs')
    for item in report['generatorSources']:checked(item['path'],item['sha256'])
    for unit in report['units']:
        row=unit['source'];receipt=unit['genuineLinkExecution']
        for name,digest in [('source','sourceSha256'),('compiler','compilerSha256'),('object','objectSha256')]:checked(row[name],row[digest])
        checked(receipt['lcf'],receipt['lcfSha256']);checked(receipt['linkedElf'],receipt['linkedElfSha256']);checked(Path(receipt['lcf']).parent/'caller.bin',receipt['linkedBodySha256'])
    for unit in report['results']:
        trace=unit['trace'];raw=checked(trace['path'],trace['compressedSha256']).read_bytes()
        if raw[4:8]!=bytes(4)or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=trace['rawSha256']:raise ValueError('Typed functional trace changed')
    return dict(matchedSourceCredit=0,matchedDataCredit=0,denominatorDelta=0)


def main():
    global _FRESH
    checked(Path(wrong_compiler.__file__).name,WRONG_COMPILER_SHA);producer.main();report=json.loads(producer.REPORT.read_text());_FRESH=report;validate(report);controls=[];native_controls=[]
    def rejected(name,action,collection=controls):
        try:action()
        except(ValueError,FileNotFoundError)as error:collection.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('False typed functional claim survived '+name)
    def changed(path,value):
        bad=copy.deepcopy(report);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value;validate(bad)
    changes=[('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),('pins',('pinnedGeneratorAndRuntimeDependencies',),[]),('credit',('matchedSourceOrDataOrDenominatorCredit',),188),('admission',('sourceAdmissionAccepted',),True),('full-registers',('fullRawRegisterEquivalenceClaimed',),True),('abi',('onlyR0AndArmCalleeSavedSpLrAreDeclaredAbiOutputs',),False),('code-as-data',('encodedCodeDifferencesExplicitAndExcludedFromDataEquivalenceOnly',),False),('physical',('physicalHardwareOrGameReachabilityProven',),True),('division',('originalDivisionScopeFreshlyValidatedBeforeEachEntry',),False),('old-policy',('originalDefaultUnknownWordRefusalsUnchanged',),False),('own-returns',('actualOriginalAndCompiledOwnReturns',),322),('helpers-as-host',('scopedNestedHelperReturnEventsSeparate',),0)]
    for index in range(2):changes.extend([(str(index)+'source',('units',index,'source','sourceSha256'),'0'*64),(str(index)+'flags',('units',index,'source','compilerFlags'),[]),(str(index)+'exact',('units',index,'genuineLinkComparison','matchingBytes'),report['units'][index]['source']['bytes']),(str(index)+'data-credit',('units',index,'sourceCredit'),4),(str(index)+'link-argv',('units',index,'genuineLinkExecution','actualLinkerArgv'),[]),(str(index)+'missing-object',('units',index,'source','object'),'work/arm7-bulk-20261030/no188.o'),(str(index)+'model',('results',index,'independentModelPassed'),False),(str(index)+'prefix-credit',('results',index,'constructorActualReturns'),322),(str(index)+'source-credit',('results',index,'sourceCredit'),report['units'][index]['source']['bytes']),(str(index)+'full-scratch',('results',index,'completeScratchRegistersClaimedEquivalent'),True),(str(index)+'missing-trace',('results',index,'trace','path'),'work/arm7-bulk-20261030/no188.json.gz')])
    for name,path,value in changes:rejected(name,lambda path=path,value=value:changed(path,value))
    main_bytes=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    for unit in report['units']:
        seed=unit['source'];entry=int(seed['address'],0);size=seed['bytes'];case=next(x for x in producer.native.cases(entry)if x['value']==10);original=main_bytes[entry-producer.native.MAIN:entry-producer.native.MAIN+size]
        rejected(seed['address']+'wrong-descriptor',lambda entry=entry,size=size,case=case,original=original:producer.native.run(main_bytes,wram,entry,original,case,13,wrong_descriptor=True),native_controls);rejected(seed['address']+'one-instruction-prefix',lambda entry=entry,case=case,original=original:producer.native.run(main_bytes,wram,entry,original,case,13,budget=1),native_controls)
    unit=report['units'][1];seed=unit['source'];text=(ROOT/seed['source']).read_text();old='M2C_FIELD(temp_r4, u16 *, 0x8C) = temp_r0;'
    if old not in text:raise ValueError('Wrong output-field source mutation absent')
    body,build=wrong_compiler.build(seed,text.replace(old,'M2C_FIELD(temp_r4, u16 *, 0x8E) = temp_r0;'),producer.WORK/'wrong-output-offset',unit['genuineLinkExecution']['bindings']);records=[];rejects=0
    if len(body)!=100:raise ValueError('Wrong output field escaped complete100-byte bound')
    for index,case in enumerate(producer.native.cases(0x027e9e3c)):
        value=producer.native.run(main_bytes,wram,0x027e9e3c,body,case,index);records.append(dict(case=case,execution=value));rejects+=not value['modelPassed']
    if rejects==0:raise ValueError('Wrong output field escaped native state model')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=producer.WORK/'wrong-output-offset/native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));validate(json.loads(producer.REPORT.read_text()));result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),producerSha256=PRODUCER_SHA,inputReportSha256=sha256(producer.REPORT),metadataControls=controls,metadataControlCount=len(controls),nativePrefixAndProducerControls=native_controls,nativeControlCount=len(native_controls),compiledWrongSource=build,actualWrongOwnReturns=len(records),independentWrongSourceRejections=rejects,wrongTrace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),freshSourceOnlyDirectAndConnectedBuild=True,restoredPositive=True,sourceDataOrDenominatorCredit=0);write_json(CONTROLS,result);print(json.dumps(dict(report=CONTROLS.relative_to(ROOT).as_posix(),sha256=sha256(CONTROLS),metadataControls=len(controls),nativeControls=len(native_controls),wrongReturns=len(records),modelRejections=rejects,sourceCredit=0)),flush=True)
if __name__=='__main__':main()
