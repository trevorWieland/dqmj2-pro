import gzip
import hashlib
import json
from pathlib import Path
import compile_arm7_core117_state240_20261101 as compiler
import arm7_core117_state240_native_20261101 as native
import prove_arm7_lane_setting_producer_20261031 as pointer_producer
import prove_arm7_core117_gap52_20261101 as gap_producer
import audit_arm7_lane_scope107_20261101 as exclusion
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core117-state240-final'
WORK=ROOT/'work/arm7-bulk-20261030/core117-state240-final'
REPORT=ROOT/'evidence/matches/arm7-core117-state240-20261101.json'
PINS=SOURCE/'generator-pins.json'
SNAPSHOT='evidence/verification/lane-root108-connected-exclusion-observed-20261101.json'
POINTER_SHA='e372dd000041574275ca9852f7f5ca57a4fbe41acb4a1c0c4eed50ad8447c8f4'
GAP_SHA='37e8fa85c2fedccfc1366c2610531df72d2870f8dfe5b588584ad461557c2174'


def main():
    pointer_producer.main();gap_producer.main()
    if sha256(ROOT/'evidence/attempts/arm7-lane-setting-producer-20261031.json')!=POINTER_SHA or sha256(gap_producer.REPORT)!=GAP_SHA:raise ValueError('Fresh pointer-write/gap native qualification differs')
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Current state240 source/runtime/input closure differs')
    seeds=json.loads((SOURCE/'profile.json').read_text())['units'];selected=json.loads((ROOT/SNAPSHOT).read_text())['functions'];main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();matches=[];symbols={};total_helpers=0;overlap_events=0
    for seed in seeds:
        entry=int(seed['address'],0)
        if any(exclusion.overlaps(selected,('arm7','','arm7-main',mode,entry,seed['bytes']))for mode in('arm','thumb')):raise ValueError('State240 overlaps normalized historical selected source')
        row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:],strict=True);own=main[entry-native.MAIN:entry-native.MAIN+seed['bytes']];records=[];visited=set();helpers=0;overlaps=0;own_paths=set()
        if body!=own:raise ValueError('Full freshly compiled/linked state routine differs')
        for index,case in enumerate(native.cases(entry)):
            first=native.run(main,wram,entry,own,case,index);second=native.run(main,wram,entry,body,case,index)
            if first!=second or not first['modelPassed']:raise ValueError('Original/source descriptor/word/port/frame/helper/return model differs')
            records.append(dict(case=case,execution=first));visited.update(first['visited']);helpers+=2*first['scopedHelperReturnEvents'];overlaps+=2*first['overlappingTailHelperEvents'];own_paths.add(bool(case['value']!=0 and case['mode']!=1)if entry==0x27e9c58 else case['state']==2)
        code_bytes=native.TOPS[entry][1]
        if not set(range(entry,entry+code_bytes,4)).issubset(visited)or own_paths!={False,True}:raise ValueError('Full owned branch/instruction scope differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/seed['address'][2:]/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));native_symbols={name:hex(int(value['address'],0))for name,value in link['bindings'].items()};symbols.update(native_symbols);row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=native_symbols,nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceAbiContract=dict(physicalArgumentWords=1 if entry==0x27e9c58 else 0,rawReturnBits=32,fullInputWordPredicateAndLow16Store=entry==0x27e9c58,rawReturn=0 if entry==0x27e9c58 else 0x04808036,qualifiedSharedRuntimePointerWordBytes=4,pointerIsExternalDescriptorProducedStorageNotModuleBss=True,pointerOrPointeeSourceDataCredit=0,historicalPublicMeaningProven=False),oracle=dict(vectors=len(records),actualOriginalAndCompiledOwnReturns=2*len(records),actualProducerFillReturnsSeparateZeroCredit=2*len(records),constructorActualReturnCredit=0,originalHelperScopedReturnEventsSeparateZeroCredit=helpers,overlappingTailReturnEventsIncludedInScopedCount=overlaps,helperAndGapSourceCredit=0,allOwnInstructionsAndBranchesVisited=True,fullRawCpuFlagsFramesAllMappedMemoryAndOrderedReadsWritesCompared=True,independentStatePortStoreFlagAndOriginalHelperModel=True,realDescriptorPrefixAndContextClearBeforeEachEntry=True,syntheticOverridesDeclaredPerCase=True,providerReplacements=[],physicalHardwareOrSceneContextProven=False,maximumInstructionsPerEntry=250000,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)));matches.append(row);total_helpers+=helpers;overlap_events+=overlaps
    names={Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins};dependencies=[]
    for entry,(size,code)in native.FUNCTIONS.items():
        if entry in native.TOPS:continue
        base=native.MAIN if entry<0x037f8000 else native.WRAM;binary=main if base==native.MAIN else wram;dependencies.append(dict(processor='arm7',program='',module='arm7-main'if base==native.MAIN else'arm7-wram',mode='arm',address=hex(entry),bytes=size,codeBytes=code,spanSha256=hashlib.sha256(binary[entry-base:entry-base+size]).hexdigest(),sourceCredit=0,originalCodeScaffolding=True))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=matches,nativeSymbols=symbols,runtimePointerQualification=dict(report='evidence/attempts/arm7-lane-setting-producer-20261031.json',sha256=POINTER_SHA,storageBytes=4,sourceDataCredit=0),originalGapQualification=dict(report=gap_producer.REPORT.relative_to(ROOT).as_posix(),sha256=GAP_SHA,sourceCredit=0,configAndDenominatorUnchanged=True),originalHelperDependencies=dependencies,generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in sorted(names)],pinnedGeneratorAndRuntimeDependencies=pins,callerSpecificLinker=dict(path=Path(compiler.linker.__file__).name,sha256=sha256(compiler.linker.__file__),sourceIdentityAndSourceHashGated=True,baseAndEarlierPolicyUnchanged=True,sourceDataCredit=0),newOrdinaryFunctionCount=2,matchedInitializedBytes=240,matchedCodeBytes=200,generatedLiteralBytes=40,initializedDenominatorDelta=0,totalActualOwnReturns=sum(x['oracle']['actualOriginalAndCompiledOwnReturns']for x in matches),totalProducerFillReturnsSeparateZeroCredit=sum(x['oracle']['actualProducerFillReturnsSeparateZeroCredit']for x in matches),constructorActualReturnCredit=0,totalOriginalHelperScopedReturnEventsSeparateZeroCredit=total_helpers,overlappingTailReturnEventsIncluded=overlap_events,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),ownReturns=report['totalActualOwnReturns'],helperScopedEvents=total_helpers,producerFillReturns=report['totalProducerFillReturnsSeparateZeroCredit'])),flush=True)
if __name__=='__main__':main()
