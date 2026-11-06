import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_main_spi_cmd256_native_20261101 as native
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-spi-cmd256-final'
WORK=ROOT/'work/arm7-bulk-20261030/spi-cmd256-final'
REPORT=ROOT/'evidence/matches/arm7-main-spi-cmd256-20261101.json'
PINS=SOURCE/'generator-pins.json'
compile_unit=compiler.compile_unit

def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Complete fixed-command source/runtime/input missing or changed')
    if(native.BASE,native.STACK,native.OUTPUT,native.STOP)!=(compiler.native.BASE,compiler.native.STACK,compiler.native.OUTPUT,compiler.native.STOP):raise ValueError('Actual checked runtime/fixture page constants differ')
    ownership=compiler.ownership();profile=json.loads((SOURCE/'profile.json').read_text())['units'];original=(ROOT/profile[0]['binary']).read_bytes();matches=[]
    for seed in profile:
        row,link,body=compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:]);entry=int(seed['address'],0);own=original[entry-native.BASE:entry-native.BASE+64];records=[];visited=set()
        if body!=own or native.SPECS[entry]!=(64,8,'command',seed['fixedCommand'])or own[-8:]!=bytes.fromhex('c0010004c2010004'):raise ValueError('Full native fixed-command code/literals/identity differ')
        for index,case in enumerate(native.cases(entry)):
            first=native.execute(original,entry,own,case,index);second=native.execute(original,entry,body,case,index)
            if first!=second or not first['modelPassed']:raise ValueError('Original/source fixed-command raw ABI/bus/full-memory model differs')
            records.append(dict(case=case,execution=first));visited.update(first['visited'])
        if len(records)!=81 or visited!=set(range(entry,entry+56,4)):raise ValueError('Fixed-command matrix/full instruction coverage differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/seed['address'][2:]/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));unsupported=[]
        for phase in(0,1):
            case=dict(native.cases(entry)[0],stuck=phase);first=native.execute(original,entry,own,case,0,budget=300,allow_no_return=True);second=native.execute(original,entry,body,case,0,budget=300,allow_no_return=True)
            if first!=second or first['actualOwnReturn']:raise ValueError('Fixed-command busy exhaustion acquired normal return')
            unsupported.append(dict(phase=phase,execution=first,supportedErrorPathCredit=0))
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols={},nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceAbiContract=dict(physicalArgumentWords=0,fixedCommand=seed['fixedCommand'],controlWord=0x8100,observedResult='last clear-busy unsigned halfword',historicalPublicMeaningProven=False),
            oracle=dict(vectors=81,actualOriginalAndCompiledReturns=162,actualNestedReturns=0,allOwnInstructionsVisited=True,independentHalfwordPollConstantCommandAndUntouchedMemoryModel=True,rawRegistersFlagsStackAndMappedMemoryCompared=True,providerReplacements=[],physicalPeripheralExecution=False,unsupported=unsupported,maxInstructionsPerRun=5000,wholeSceneOrHardwareContextProven=False,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
        matches.append(row)
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=matches,nativeSymbols={},runtimeOwnership=ownership,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=4,matchedInitializedBytes=256,matchedCodeBytes=224,generatedLiteralBytes=32,initializedDenominatorDelta=0,totalActualOwnReturns=648,implementationFamilies=1,newImplementationFamilyNoveltyCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0)
    write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=648)),flush=True)
if __name__=='__main__':main()
