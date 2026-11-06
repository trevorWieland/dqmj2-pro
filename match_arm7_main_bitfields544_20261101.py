import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_main_bitfields544_native_20261101 as native
import audit_arm7_lane_scope107_20261101 as exclusion
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-bitfields544-final'
WORK=ROOT/'work/arm7-bulk-20261030/bitfields544-final'
REPORT=ROOT/'evidence/matches/arm7-main-bitfields544-20261101.json'
PINS=SOURCE/'generator-pins.json'
EXCLUSION='evidence/verification/lane-root108-connected-exclusion-observed-20261101.json'


def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Current bitfield source/runtime/input closure differs')
    ownership=compiler.ownership();profile=json.loads((SOURCE/'profile.json').read_text());selected=json.loads((ROOT/EXCLUSION).read_text())['functions'];original=(ROOT/profile['units'][0]['binary']).read_bytes();matches=[]
    for seed in profile['units']:
        entry=int(seed['address'],0)
        if any(exclusion.overlaps(selected,('arm7','','arm7-main',mode,entry,272))for mode in('arm','thumb')):raise ValueError('Bitfield source overlaps normalized prior selected interval')
        row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:]);own=original[entry-native.BASE:entry-native.BASE+272];records=[];visited=set();branches=set();store_counts=set();reads=set()
        if body!=own:raise ValueError('Full bitfield source unit bytes differ')
        for index,case in enumerate(native.cases()):
            first=native.execute(original,entry,own,case,index);second=native.execute(original,entry,body,case,index)
            if first!=second or not first['modelPassed']:raise ValueError('Bitfield original/fresh-source full state or independent model differs')
            records.append(dict(case=case,execution=first));visited.update(first['visited']);branches.add((first['independentWordModel']['code'],first['independentWordModel']['flag']));store_counts.add(len(first['orderedWrites']));reads.add(len(first['orderedReads']))
        if visited!=set(range(entry,entry+272,4))or branches!={(code,flag)for code in range(64)for flag in(0,1)}or reads!={1,2}:raise ValueError('Full code/dispatch/flag/default-read coverage differs')
        if store_counts!=({1}if entry==native.ENTRIES[0]else{0,1}):raise ValueError('Store/no-store branch evidence differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/seed['address'][2:]/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols={},nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceAbiContract=dict(physicalArgumentWords=1,argumentKind='raw32 address of an aligned four-byte RAM view',rawIncomingAddressWordReturned=True,wordStorageView=profile['storageView'],unsignedBitfieldArithmetic=True,compilerTargetWordBits=32,historicalPublicMeaningProven=False,platformIndependentBitfieldLayoutOrAndroidPointerModelProven=False),oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),actualNestedReturns=0,allOwnInstructionsAndBranchTableSlotsVisited=True,codeFlagPairs=len(branches),distinctReadCounts=sorted(reads),distinctStoreCounts=sorted(store_counts),independentFullWordFieldPreservationAndReadStoreFlagsModel=True,fullRawCpuStackInputAndMappedRamCompared=True,providerReplacements=[],hardwareContextProven=False,allLowByteValuesAndEveryCodeFlagOutcomeCovered=True,maximumInstructionsPerRun=200,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)));matches.append(row)
    names={Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins};report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=matches,nativeSymbols={},runtimeOwnership=ownership,generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in sorted(names)],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=2,matchedInitializedBytes=544,matchedCodeBytes=544,generatedLiteralBytes=0,initializedDenominatorDelta=0,totalActualOwnReturns=sum(x['oracle']['actualOriginalAndCompiledReturns']for x in matches),wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0,scope=dict(eachCompleteNativeBytes=272,jumpDispatchBranchesPerUnit=36,tableKind='executed ARM branch instructions; zero data or literal bytes',externalCallsOrBindings=0,callableInteriorOrSharedTailClaim=False));write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=report['totalActualOwnReturns'])),flush=True)
if __name__=='__main__':main()
