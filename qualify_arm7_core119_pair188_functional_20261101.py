import gzip
import hashlib
import json
from pathlib import Path
import compile_arm7_core119_pair188_functional_20261101 as compiler88
import compile_arm7_core119_pair188_functional_20261101 as compiler100
import arm7_core119_pair188_native_20261101 as native
import prove_arm7_lane_setting_producer_20261031 as producer
from project import ROOT,sha256,write_json
WORK=ROOT/'work/arm7-bulk-20261030/core119-pair188-functional'
REPORT=ROOT/'evidence/attempts/arm7-core119-pair188-functional-20261101.json'


def relevant(value):
    helpers=[]
    for item in value['helpers']:
        helper=dict(entry=item['entry'],actualReturn=item['actualReturn'],result=item['result'],abiPreserved=item['abiPreserved'],incoming=item['incoming'][:2 if item['entry']=='0x3806e44'else 1])
        if item['entry']=='0x3806e44':helper['remainder']=item['secondaryResult']
        helpers.append(helper)
    return dict(rawResult=value['rawResult'],abiRegisters=[value['rawRegisters'][i]for i in [0,*range(4,12),13,14]],cpsr=value['cpsr'],orderedReads=value['orderedReads'],orderedWrites=value['orderedWrites'],helpers=helpers,dataRegions={k:v for k,v in value['regionHashes'].items()if k!=hex(native.MAIN)},modelChecks=value['modelChecks'],actualOwnReturn=value['actualOwnReturn'],providers=value['providers'])


def main():
    producer.main();pins=json.loads((ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core119-pair188-functional/generator-pins.json').read_text())['files']
    for item in pins:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Typed functional closure changed')
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();seed88=json.loads((ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core119-pair188/profile.json').read_text())['units'][0];seed100=json.loads((ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core119-pair188-unsigned/profile.json').read_text())['units'][1];compiled={};units=[]
    for seed,compiler in[(seed88,compiler88),(seed100,compiler100)]:
        row,comparison,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:],strict=False)
        if comparison!={'nativeBytes':seed['bytes'],'linkedBytes':seed['bytes'],'matchingBytes':83 if seed['bytes']==88 else 91}:raise ValueError('Bounded typed hypothesis linked byte differences changed')
        receipt_path=WORK/seed['address'][2:]/'real-link/functional-execution.json';receipt=json.loads(receipt_path.read_text())
        if receipt['exitCode']!=0 or receipt['sourceObjectSha256']!=row['objectSha256']or receipt['linkedBodySha256']!=hashlib.sha256(body).hexdigest():raise ValueError('Fresh real linker receipt/product differs')
        compiled[int(seed['address'],0)]=body;units.append(dict(source=row,genuineLinkComparison=comparison,genuineLinkExecution=receipt,sourceCredit=0,bytesMatchedCredit=0))
    linked_main=bytearray(main)
    for entry,body in compiled.items():linked_main[entry-native.MAIN:entry-native.MAIN+len(body)]=body
    results=[]
    for unit in units:
        entry=int(unit['source']['address'],0);size=unit['source']['bytes'];records=[];scratch=[];helper_events=0
        for i,case in enumerate(native.cases(entry)):
            first=native.run(main,wram,entry,main[entry-native.MAIN:entry-native.MAIN+size],case,i);second=native.run(bytes(linked_main),wram,entry,compiled[entry],case,i)
            if relevant(first)!=relevant(second)or not first['modelPassed']or not second['modelPassed']:raise ValueError(dict(address=hex(entry),case=case,originalModel=first['modelChecks'],compiledModel=second['modelChecks'],relevantEqual=relevant(first)==relevant(second)))
            differences=[index for index in(1,2,3,12)if first['rawRegisters'][index]!=second['rawRegisters'][index]];scratch.append(differences);helper_events+=first['scopedHelperReturnEvents']+second['scopedHelperReturnEvents'];records.append(dict(case=case,original=first,compiled=second,scratchRegisterDifferences= differences))
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/hex(entry)[2:]/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));results.append(dict(address=hex(entry),bytes=size,vectors=len(records),actualOriginalAndCompiledOwnReturns=2*len(records),actualProducerFillReturnsSeparate=2*len(records),constructorActualReturns=0,scopedNestedHelperReturnEventsSeparate=helper_events,scratchDifferenceCases=sum(bool(x)for x in scratch),completeScratchRegistersClaimedEquivalent=False,relevantRegisterFlagsFramesAllNoncodeMemoryAndOrderedReadsWritesEqual=True,compiled188SourceBodiesLoadedTogether=True,independentModelPassed=True,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),sourceCredit=0))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),units=units,results=results,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in sorted({x['path']for x in pins}|{Path(__file__).name,'nonmatching/arm7-bulk/20261101/lane-main-core119-pair188-functional/generator-pins.json'})],actualOriginalAndCompiledOwnReturns=sum(x['actualOriginalAndCompiledOwnReturns']for x in results),actualProducerFillReturnsSeparate=sum(x['actualProducerFillReturnsSeparate']for x in results),scopedNestedHelperReturnEventsSeparate=sum(x['scopedNestedHelperReturnEventsSeparate']for x in results),fullRawRegisterEquivalenceClaimed=False,onlyR0AndArmCalleeSavedSpLrAreDeclaredAbiOutputs=True,encodedCodeDifferencesExplicitAndExcludedFromDataEquivalenceOnly=True,physicalHardwareOrGameReachabilityProven=False,originalDivisionScopeFreshlyValidatedBeforeEachEntry=True,sourceAdmissionAccepted=False,matchedSourceOrDataOrDenominatorCredit=0,originalDefaultUnknownWordRefusalsUnchanged=True);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),ownReturns=report['actualOriginalAndCompiledOwnReturns'],nestedEvents=report['scopedNestedHelperReturnEventsSeparate'],sourceCredit=0)),flush=True)
if __name__=='__main__':main()
