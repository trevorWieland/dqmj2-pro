import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_main_spi_two156_native_20261101 as native
import audit_arm7_lane_scope107_20261101 as exclusion
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-spi-two156-final'
WORK=ROOT/'work/arm7-bulk-20261030/spi-two156-final'
REPORT=ROOT/'evidence/matches/arm7-main-spi-two156-20261101.json'
PINS=SOURCE/'generator-pins.json'
EXCLUSION='evidence/verification/lane-root108-connected-exclusion-observed-20261101.json'


def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Current two-byte reader source/input closure differs')
    ownership=compiler.ownership();seed=json.loads((SOURCE/'profile.json').read_text())['unit'];selected=json.loads((ROOT/EXCLUSION).read_text())['functions']
    if any(exclusion.overlaps(selected,('arm7','','arm7-main',mode,native.ENTRY,156))for mode in('arm','thumb')):raise ValueError('Two-byte reader overlaps selected historical source')
    row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'caller');original=(ROOT/seed['binary']).read_bytes();own=original[native.ENTRY-native.BASE:native.ENTRY-native.BASE+156];records=[];visited=set()
    if body!=own:raise ValueError('Full freshly linked two-byte reader differs')
    for index,case in enumerate(native.cases()):
        first=native.execute(original,own,case,index);second=native.execute(original,body,case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/source two-byte receive/frame/full CPU model differs')
        records.append(dict(case=case,execution=first));visited.update(first['visited'])
    if visited!=set(range(native.ENTRY,native.ENTRY+148,4)):raise ValueError('Complete two-byte reader instruction coverage differs')
    unsupported=[]
    for phase in range(4):
        case=dict(native.cases()[0],stuck=phase);first=native.execute(original,own,case,0,budget=300,allow_no_return=True);second=native.execute(original,body,case,0,budget=300,allow_no_return=True)
        if first!=second or first['actualOwnReturn']or not first['stuckPhaseReached']:raise ValueError('Unsupported busy phase acquired a return or was not reached')
        unsupported.append(dict(phase=phase,execution=first,supportedErrorPathCredit=0))
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'caller/native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols={},nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceAbiContract=dict(physicalArgumentWords=1,argumentKind='raw32 address of writable two-byte output',rawIncomingAddressWordReturned=True,fixedCommand=159,outputStoreWidth=1,outputBytes=2,receivedHalfwordBits=16,returnedOrStoredByteTruncationOnlyAtOutput=True,privateFrameBytes=8,preservedScratchR3IsPaddingNotASecondArgument=True,historicalPublicDeviceMeaningProven=False),oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),actualNestedReturns=0,allOwnInstructionsVisited=True,independentHalfwordReceiveTwoByteOutputAndR3LrFrameModel=True,fullRawRegistersFlagsAndMappedRamStackOutputIoCompared=True,orderedAllReadsAndWritesCompared=True,providerReplacements=[],physicalPeripheralExecution=False,hardwareOrSceneContextProven=False,unsupported=unsupported,outputOffsets=[0,1,64,255,511,4094],maximumInstructionsPerRun=2000,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)));names={Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins};report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols={},runtimeOwnership=ownership,generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in sorted(names)],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=1,matchedInitializedBytes=156,matchedCodeBytes=148,generatedLiteralBytes=8,initializedDenominatorDelta=0,totalActualOwnReturns=2*len(records),wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=report['totalActualOwnReturns'])),flush=True)
if __name__=='__main__':main()
