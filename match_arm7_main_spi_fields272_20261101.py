import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_main_spi_fields272_native_20261101 as native
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-spi-fields272-final'
WORK=ROOT/'work/arm7-bulk-20261030/spi-fields272-final'
REPORT=ROOT/'evidence/matches/arm7-main-spi-fields272-20261101.json'
PINS=SOURCE/'generator-pins.json'
compile_unit=compiler.compile_unit

def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        p=(ROOT/item['path']).resolve()
        if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=item['sha256']:raise ValueError('Complete field caller/helper source/runtime differs')
    ownership=compiler.ownership();profile=json.loads((SOURCE/'profile.json').read_text());dep=profile['existingSourceDependency'];old,old_link,helper=compile_unit(dep,ROOT/dep['source'],WORK/'helper');original=(ROOT/dep['binary']).read_bytes();native_helper=original[native.HELPER-native.BASE:native.HELPER-native.BASE+36];matches=[];helper_returns=0;symbols={}
    if helper!=native_helper:raise ValueError('Fresh existing helper source differs')
    for seed in profile['units']:
        row,link,body=compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:]);entry=int(seed['address'],0);own=original[entry-native.BASE:entry-native.BASE+136];records=[];visited=set();helper_visited=set();local_returns=0
        if body!=own:raise ValueError('Fresh complete field caller source differs')
        for index,case in enumerate(native.cases()):
            first=native.execute(original,entry,own,native_helper,case,index);second=native.execute(original,entry,body,helper,case,index)
            if first!=second or not first['modelPassed']:raise ValueError('Original/source field raw ABI/arguments/byte-order/ports model differs')
            records.append(dict(case=case,execution=first));visited.update(first['visitedOwn']);helper_visited.update(first['visitedHelper']);local_returns+=2*first['actualNestedReturns']
        if len(records)!=283 or local_returns!=1698 or visited!=set(range(entry,entry+128,4))or helper_visited!=set(range(native.HELPER,native.HELPER+32,4)):raise ValueError('Full field/helper code or return coverage differs')
        helper_returns+=local_returns;raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/seed['address'][2:]/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));unsupported=[]
        for phase in range(5):
            case=dict(native.cases()[0],stuck=phase);first=native.execute(original,entry,own,native_helper,case,0,budget=2000,allow_no_return=True);second=native.execute(original,entry,body,helper,case,0,budget=2000,allow_no_return=True)
            if first!=second or first['actualOwnReturn']or not first['stuckPhaseReached']:raise ValueError('Busy field phase not reached without own return')
            unsupported.append(dict(phase=phase,execution=first,additionalNestedReturnCredit=0,supportedErrorPathCredit=0))
        local={k:hex(int(v['address'],0))for k,v in link['bindings'].items()};symbols.update(local);row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=local,nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
            sourceAbiContract=dict(physicalArgumentWords=1,serializedAddressBits=24,orderedHelperArguments='parameter bits16..23,8..15,0..7 as zero-extended words',fixedCommand=native.COMMANDS[entry],helperCalls=3,sourceWidths=dict(high=16,middle=16,low=8),observedResult='last clear-busy unsigned halfword',historicalPublicMeaningProven=False),
            oracle=dict(vectors=283,actualOriginalAndCompiledReturns=566,existingSourceHelperReturnsSeparateZeroCredit=1698,allOwnAndHelperInstructionsVisited=True,fullSourceLinkedFieldCallerAndExistingHelper=True,independentWordInputsShiftWidthsByteOrderSavedFrameAndHalfwordPortModel=True,rawRegistersFlagsStackAndMappedMemoryCompared=True,providerReplacements=[],physicalPeripheralExecution=False,unsupported=unsupported,maxInstructionsPerRun=5000,wholeSceneOrHardwareContextProven=False,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
        matches.append(row)
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=matches,nativeSymbols=symbols,existingSourceDependency=dict(old,realLink=old_link,sourceCredit=0,byteCredit=0,existingSelectionUnchanged=True),runtimeOwnership=ownership,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=2,matchedInitializedBytes=272,matchedCodeBytes=256,generatedLiteralBytes=16,initializedDenominatorDelta=0,totalActualOwnReturns=1132,totalExistingSourceHelperReturnsSeparateZeroCredit=helper_returns,existingSourceBytesSeparateZeroCredit=36,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=1132,existingHelperReturnsSeparate=3396)),flush=True)
if __name__=='__main__':main()
