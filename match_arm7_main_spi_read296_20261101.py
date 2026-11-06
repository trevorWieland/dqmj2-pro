import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_main_spi_read296_native_20261101 as native
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-spi-read296-final'
WORK=ROOT/'work/arm7-bulk-20261030/spi-read296-final'
REPORT=ROOT/'evidence/matches/arm7-main-spi-read296-20261101.json'
PINS=SOURCE/'generator-pins.json'
compile_unit=compiler.compile_unit

def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Complete read296 source/runtime/input missing or changed')
    if(native.BASE,native.STACK,native.OUTPUT,native.STOP)!=(compiler.native.BASE,compiler.native.STACK,compiler.native.OUTPUT,compiler.native.STOP):raise ValueError('Checked fixture/runtime constants differ')
    ownership=compiler.ownership();profile=json.loads((SOURCE/'profile.json').read_text())['units'];units=[compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:])for seed in profile];own,helper=units;original=(ROOT/profile[0]['binary']).read_bytes();original_own=original[native.ENTRY-native.BASE:native.ENTRY-native.BASE+260];original_helper=original[native.HELPER-native.BASE:native.HELPER-native.BASE+36];records=[];helper_records=[];own_visits=set();helper_visits=set()
    if own[2]!=original_own or helper[2]!=original_helper:raise ValueError('Complete freshly linked read/helper source chain differs')
    for index,case in enumerate(native.cases()):
        first=native.execute(original,original_own,original_helper,case,index);second=native.execute(original,own[2],helper[2],case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/source read full raw state/array/frame/halfword model differs')
        records.append(dict(case=case,execution=first));own_visits.update(first['visitedOwn']);helper_visits.update(first['visitedHelper'])
    for index,case in enumerate(native.helper_cases()):
        first=native.execute(original,original_own,original_helper,case,index,direct=True);second=native.execute(original,own[2],helper[2],case,index,direct=True)
        if first!=second or not first['modelPassed']:raise ValueError('Direct original/source helper raw state/constant model differs')
        helper_records.append(dict(case=case,execution=first));helper_visits.update(first['visitedHelper'])
    if len(records)!=445 or len(helper_records)!=81 or own_visits!=set(range(native.ENTRY,native.ENTRY+252,4))or helper_visits!=set(range(native.HELPER,native.HELPER+32,4)):raise ValueError('Complete read/helper matrix/instruction coverage differs')
    def trace(rows,name):
        raw=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode();p=WORK/name;p.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));return dict(path=p.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(p),gzipMtime=0)
    own_trace=trace(records,'read-records.json.gz');helper_trace=trace(helper_records,'helper-records.json.gz');unsupported=[];normal=next(case for case in native.cases()if case['count']==4)
    for phase in range(9):
        case=dict(normal,stuck=phase);first=native.execute(original,original_own,original_helper,case,0,budget=2000,allow_no_return=True);second=native.execute(original,own[2],helper[2],case,0,budget=2000,allow_no_return=True)
        if first!=second or first['actualOwnReturn']or not first['stuckPhaseReached']:raise ValueError('Specific permanent-busy read phase not observed without return')
        unsupported.append(dict(kind='permanent-busy',phase=phase,execution=first,supportedErrorPathCredit=0))
    for count in(0x7fffffff,0x80000000,0xffffffff):
        case=dict(normal,count=count);first=native.execute(original,original_own,original_helper,case,0,budget=2000,allow_no_return=True);second=native.execute(original,own[2],helper[2],case,0,budget=2000,allow_no_return=True)
        if first!=second or first['actualOwnReturn']:raise ValueError('Large unsigned count acquired completion/error credit')
        unsupported.append(dict(kind='large-count-bounded-prefix',count=count,execution=first,supportedErrorPathCredit=0))
    matches=[];symbols={}
    for i,(row,link,body)in enumerate(units):
        caller=i==0;local={k:hex(int(v['address'],0))for k,v in link['bindings'].items()};symbols.update(local);row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=local,nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
            sourceAbiContract=dict(physicalArgumentWords=3 if caller else 0,addressWordRemainsFullWidthAtZeroCount=caller,serializedAddressBits=24 if caller else 0,serializedHalfwordArrayElements=3 if caller else 0,outputStoreWidth=1 if caller else 0,countUnsigned32=caller,observedResult='incoming full address when count zero; last received unsigned halfword otherwise'if caller else'clear-busy unsigned halfword',historicalPublicMeaningProven=False),
            oracle=dict(vectors=445 if caller else 499,actualOriginalAndCompiledReturns=890 if caller else 998,directOwnReturns=890 if caller else 162,nestedSourceOwnReturns=0 if caller else 836,zeroCountCallerReturns=54 if caller else 0,allOwnInstructionsVisited=True,fullSourceLinkedReadAndDummyHelper=True,independentAddressByteOrderArrayStackFrameHalfwordAndOutputModel=True,rawRegistersFlagsStackAndMappedMemoryCompared=True,providerReplacements=[],physicalPeripheralExecution=False,unsupported=unsupported,maxInstructionsPerRun=5000,wholeSceneOrHardwareContextProven=False,readTrace=own_trace,directHelperTrace=helper_trace))
        matches.append(row)
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=matches,nativeSymbols=symbols,runtimeOwnership=ownership,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=2,matchedInitializedBytes=296,matchedCodeBytes=284,generatedLiteralBytes=12,initializedDenominatorDelta=0,totalActualOwnReturns=1888,callerOwnReturns=890,helperOwnReturns=998,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0)
    write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=1888)),flush=True)
if __name__=='__main__':main()
