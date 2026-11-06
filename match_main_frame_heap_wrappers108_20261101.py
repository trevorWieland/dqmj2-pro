import gzip
import hashlib
import json
from pathlib import Path
import main_sdk_heap_attribute424_compile_20261101 as compiler
import main_frame_heap_wrappers108_native_20261101 as native
from project import ROOT,sha256,write_json

PROFILE=ROOT/'nonmatching/main-sdk-heap/20261101/lane-frame-wrappers108-final/profile.json'
WORK=ROOT/'work/main-sdk-heap/20261101/lane-frame-wrappers108-final'
REPORT=ROOT/'evidence/matches/main-frame-heap-wrappers108-20261101.json'
PINS=PROFILE.parent/'generator-pins.json'


def oracle(image,entry,body):
    size=56 if entry==native.CREATOR else 52;original=image[entry-0x02000000:entry-0x02000000+size]
    vectors=1426 if entry==native.CREATOR else 1568
    records=[];supported=0;stops=0;unsupported_returns=0;helpers=0;visited=set();zero_changed=0
    for index in range(vectors):
        first=native.execute(image,entry,original,index);second=native.execute(image,entry,body,index)
        if first!=second:raise ValueError('Original/fresh compiled frame wrapper state/return/stop differs at '+str(index))
        if first['actualOwnReturn']and first['case']['modelDomain']:
            if not first['modelPassed']:raise ValueError('Independent frame model differs at '+str(index))
            if entry==native.ALLOCATOR and first['result']==0:
                spec=first['case'];zero_changed+=int(spec['oldHead']!=spec['resultingHead']or spec['oldTail']!=spec['resultingTail'])
            supported+=1;helpers+=2*len(first['actualOriginalHelperReturnsSeparate']);visited.update(a for a in first['visited']if entry<=a<entry+size)
        elif first['actualOwnReturn']:unsupported_returns+=1
        else:stops+=1
        records.append(first)
    missing=sorted(set(range(entry,entry+size,4))-visited)
    if missing:raise ValueError('Complete frame wrapper instruction coverage missing')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/(f'{entry:08x}-native-records.json.gz');path.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(vectors=vectors,supportedOriginalAndCompiledPairs=supported,actualOwnSupportedReturns=2*supported,
        actualOriginalHelperReturnsSeparate=helpers,zeroReturnWithChangedHeadTailCases=zero_changed,pairedBoundedNoReturnCases=stops,pairedReturnedOutsideIndependentModel=unsupported_returns,
        completeCodeBytes=size,unvisited=missing,providerReplacements=[],originalCalleesAdditionalSourceCredit=0,
        rawRegistersFlagsAllMappedRamStackOrderedMemoryAndNestedArgumentsCompared=True,
        trace=dict(path=path.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(path),gzipMtime=0),
        limitations=['Stable disposable heap/list context on original32-bit guest ABI only',
            'Constructor global hierarchy and actual allocator/fill paths execute natively; no supplied outcomes',
            'Creator guard-pass low/unmapped buffers and any payload access beyond disposable backing are bounded stops with post-state excluded',
            'Zero return does not imply unchanged state or valid-allocation failure; wrapped arithmetic and signed fill-helper address tests are measured',
            'No physical ownership, scene feasibility, concurrency or native64-bit/Android pointer portability claim'])


def main():
    for item in json.loads(PINS.read_text())['files']:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Required frame source/runtime/reference pin missing or changed')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    if hashlib.sha256(image).hexdigest()!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('Measured main image differs')
    rows=[]
    for pin in json.loads(PROFILE.read_text())['matches']:
        entry,bindings,link,unused,body=compiler.build(pin,WORK/pin['address'])
        address=int(pin['address'],0);record=oracle(image,address,body)
        row=dict(entry,realMainLink=link,nativeSymbolEntries=bindings,nativeSymbols={k:hex(int(v['address'],0))for k,v in bindings.items()},
            exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,matchingBytes=pin['bytes'],oracle=record,
            originalObjectScaffolding=False,sourceOnlyCompilerInput=dict(source=pin['source'],sha256=pin['sourceSha256'],includes=pin['sourceDependencies'],originalCodeCompilerInput=False),
            wholeModuleLinked=False,sourceAbiContract=dict(physicalArgumentWords=3,unsignedWordArithmetic=True,originalHistoricalTypesProven=False))
        rows.append(row);print(json.dumps(dict(address=pin['address'],supportedPairs=record['supportedOriginalAndCompiledPairs'],stoppedPairs=record['pairedBoundedNoReturnCases'])),flush=True)
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm9',program='',module='main',
        romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=rows,
        nativeSymbols={k:v for row in rows for k,v in row['nativeSymbols'].items()},matchedInitializedBytes=108,matchedInstructionBytes=108,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in json.loads(PINS.read_text())['files']})],
        pinnedGeneratorAndRuntimeDependencies=json.loads(PINS.read_text())['files'],
        generatedLiteralBytes=0,newOrdinaryFunctionCount=2,originalCalleeDataExtentOrAssemblyCredit=0,initializedDenominatorDelta=0,
        wholeModuleLinked=False,sourceReconstructionComplete=False)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),
        actualOwnSupportedReturns=sum(r['oracle']['actualOwnSupportedReturns']for r in rows))),flush=True)


if __name__=='__main__':main()
