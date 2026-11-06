import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_main_spi_fast288_native_20261101 as native
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-spi-fast288-final'
WORK=ROOT/'work/arm7-bulk-20261030/spi-fast288-final'
REPORT=ROOT/'evidence/matches/arm7-main-spi-fast288-20261101.json'
PINS=SOURCE/'generator-pins.json'
compile_unit=compiler.compile_unit

def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        p=(ROOT/item['path']).resolve()
        if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=item['sha256']:raise ValueError('Complete fast-read source/runtime/input missing or changed')
    if(native.BASE,native.STACK,native.OUTPUT,native.STOP)!=(compiler.native.BASE,compiler.native.STACK,compiler.native.OUTPUT,compiler.native.STOP):raise ValueError('Checked fixture/runtime constants differ')
    ownership=compiler.ownership();profile=json.loads((SOURCE/'profile.json').read_text());seed=profile['newUnit'];dep=profile['existingSourceDependency'];row,link,body=compile_unit(seed,ROOT/seed['source'],WORK/'caller');old,old_link,helper=compile_unit(dep,ROOT/dep['source'],WORK/'helper');original=(ROOT/seed['binary']).read_bytes();own=original[native.ENTRY-native.BASE:native.ENTRY-native.BASE+288];original_helper=original[native.HELPER-native.BASE:native.HELPER-native.BASE+36];records=[];visited=set();helper_visited=set();helper_returns=0
    if body!=own or helper!=original_helper:raise ValueError('Fresh full fast-read/existing-helper source closure differs')
    for index,case in enumerate(native.cases()):
        first=native.execute(original,own,original_helper,case,index);second=native.execute(original,body,helper,case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/source fast-read full raw state/extra-transfer/frame model differs')
        records.append(dict(case=case,execution=first));visited.update(first['visitedOwn']);helper_visited.update(first['visitedHelper']);helper_returns+=2*first['actualNestedReturns']
    if len(records)!=445 or helper_returns!=836 or visited!=set(range(native.ENTRY,native.ENTRY+280,4))or helper_visited!=set(range(native.HELPER,native.HELPER+32,4)):raise ValueError('Complete fast-read/helper code or case/return coverage differs')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));unsupported=[];normal=next(case for case in native.cases()if case['count']==4)
    for phase in range(10):
        case=dict(normal,stuck=phase);first=native.execute(original,own,original_helper,case,0,budget=2000,allow_no_return=True);second=native.execute(original,body,helper,case,0,budget=2000,allow_no_return=True)
        if first!=second or first['actualOwnReturn']or not first['stuckPhaseReached']:raise ValueError('Busy fast-read phase not reached without return')
        unsupported.append(dict(kind='permanent-busy',phase=phase,execution=first,supportedErrorPathCredit=0))
    for count in(0x7fffffff,0x80000000,0xffffffff):
        case=dict(normal,count=count);first=native.execute(original,own,original_helper,case,0,budget=2000,allow_no_return=True);second=native.execute(original,body,helper,case,0,budget=2000,allow_no_return=True)
        if first!=second or first['actualOwnReturn']:raise ValueError('Large unsigned fast-read acquired completion/error credit')
        unsupported.append(dict(kind='large-count-bounded-prefix',count=count,execution=first,supportedErrorPathCredit=0))
    symbols={k:hex(int(v['address'],0))for k,v in link['bindings'].items()};row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=symbols,nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
        sourceAbiContract=dict(physicalArgumentWords=3,addressWordRemainsFullWidthAtZeroCount=True,serializedAddressBits=24,serializedHalfwordArrayElements=3,outputStoreWidth=1,countUnsigned32=True,fixedCommand=0xb,extraZeroTransferBeforeDataReads=True,observedResult='incoming full address when count zero; last received unsigned halfword otherwise',historicalPublicMeaningProven=False),
        oracle=dict(vectors=445,actualOriginalAndCompiledReturns=890,existingSourceHelperReturnsSeparateZeroCredit=helper_returns,zeroCountCallerReturns=54,allOwnAndHelperInstructionsVisited=True,fullSourceLinkedFastReadAndExistingHelper=True,independentExtraTransferAddressArrayStackFrameHalfwordAndOutputModel=True,rawRegistersFlagsStackAndMappedMemoryCompared=True,providerReplacements=[],physicalPeripheralExecution=False,unsupported=unsupported,maxInstructionsPerRun=5000,wholeSceneOrHardwareContextProven=False,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols=symbols,existingSourceDependency=dict(old,realLink=old_link,sourceCredit=0,byteCredit=0,existingSelectionUnchanged=True),runtimeOwnership=ownership,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=1,matchedInitializedBytes=288,matchedCodeBytes=280,generatedLiteralBytes=8,initializedDenominatorDelta=0,totalActualOwnReturns=890,totalExistingSourceHelperReturnsSeparateZeroCredit=836,existingSourceBytesSeparateZeroCredit=36,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=890,existingSourceHelperReturnsSeparate=836)),flush=True)
if __name__=='__main__':main()
