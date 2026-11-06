import gzip
import hashlib
import json
from pathlib import Path
import compile_arm7_core126_state76_20261101 as compiler
import arm7_core126_state76_native_20261101 as native
import prove_arm7_lane_setting_producer_20261031 as pointer_producer
import audit_arm7_lane_scope107_20261101 as exclusion
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core126-state76-final'
WORK=ROOT/'work/arm7-bulk-20261030/core126-state76-final'
REPORT=ROOT/'evidence/matches/arm7-core126-state76-20261101.json'
PINS=SOURCE/'generator-pins.json'
POINTER_SHA='e372dd000041574275ca9852f7f5ca57a4fbe41acb4a1c0c4eed50ad8447c8f4'


def main():
    pointer_producer.main()
    if sha256(ROOT/'evidence/attempts/arm7-lane-setting-producer-20261031.json')!=POINTER_SHA:raise ValueError('Fresh descriptor-pointer producer qualification differs')
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Current state76 source/runtime/input closure differs')
    seed=json.loads((SOURCE/'profile.json').read_text())['units'][0];entry=int(seed['address'],0);selected=json.loads((ROOT/'evidence/verification/lane-root108-connected-exclusion-observed-20261101.json').read_text())['functions']
    if any(exclusion.overlaps(selected,('arm7','','arm7-main',mode,entry,76))for mode in('arm','thumb')):raise ValueError('Pure getter overlaps normalized historical selected source')
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();original=main[0xa584:0xa584+76];row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'caller',strict=True)
    if body!=original:raise ValueError('Complete freshly compiled getter differs')
    records=[];visited=set();outcomes=set()
    for index,case in enumerate(native.cases()):
        first=native.run(main,wram,entry,original,case,index);second=native.run(main,wram,entry,body,case,index)
        if first!=second or not first['modelPassed']or first['orderedWrites']or first['scopedHelperReturnEvents']:raise ValueError('Pure getter original/C return/flag/read/register/immutable-memory model differs')
        records.append(dict(case=case,execution=first));visited.update(first['visited']);outcomes.add((0 if case['mode']==0 else 1 if case['mode']==1 else 2,bool(case['flags']&1)))
    if not set(range(entry,entry+72,4)).issubset(visited)or len(outcomes)!=6:raise ValueError('Complete getter code/domain coverage differs')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));symbols={name:hex(int(value['address'],0))for name,value in link['bindings'].items()};row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=symbols,nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceAbiContract=dict(physicalArgumentWords=0,rawReturnBits=32,rawReturns=[10,20],fields=dict(modeHalfwordOffset='0x330',flagsHalfwordOffset='0x3a4',testedMask=1),ownMemoryWrites=0,ownCalls=0,compatibleWithExistingUnsignedWordCallerView=True,historicalPublicMeaningProven=False,pointerOrPointeeSourceDataCredit=0),oracle=dict(vectors=len(records),actualOriginalAndCompiledOwnReturns=2*len(records),actualProducerFillReturnsSeparateZeroCredit=2*len(records),constructorActualReturnCredit=0,allOwnInstructionsAndSupportedBranchesVisited=True,fullRawRegistersFlagsAndAllMappedMemoryAndOrderedReadsCompared=True,independentProducedPointerHalfwordPredicateLeafRegisterAndFlagModel=True,allOwnMemoryWritesAndCallsZero=True,syntheticOverridesDeclaredPerCase=True,providerReplacements=[],physicalHardwareOrSceneContextProven=False,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    names={Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins};report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols=symbols,runtimePointerQualification=dict(report='evidence/attempts/arm7-lane-setting-producer-20261031.json',sha256=POINTER_SHA,storageBytes=4,sourceDataCredit=0),callerSpecificLinker=dict(path=Path(compiler.linker.__file__).name,sha256=sha256(compiler.linker.__file__),exactCallerSourceHashAndFullIdentityRequired=True,defaultAndEarlierPoliciesUnchanged=True,sourceDataCredit=0),generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in sorted(names)],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=1,matchedInitializedBytes=76,matchedCodeBytes=72,generatedLiteralBytes=4,initializedDenominatorDelta=0,totalActualOwnReturns=2*len(records),totalProducerFillReturnsSeparateZeroCredit=2*len(records),constructorActualReturnCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),ownReturns=report['totalActualOwnReturns'],producerFillReturns=report['totalProducerFillReturnsSeparateZeroCredit'],ownWritesAndCalls=0)),flush=True)
if __name__=='__main__':main()
