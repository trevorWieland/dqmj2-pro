import gzip
import hashlib
import json
from pathlib import Path
import main_sdk_heap_attribute424_compile_20261101 as compiler
import main_frame_heap_core324_native_20261101 as native
from project import ROOT,sha256,write_json

PROFILE=ROOT/'nonmatching/main-sdk-heap/20261101/lane-frame-core324-final/profile.json'
WRAPPERS=ROOT/'nonmatching/main-sdk-heap/20261101/lane-frame-wrappers108-final/profile.json'
WORK=ROOT/'work/main-sdk-heap/20261101/lane-frame-core324-final'
REPORT=ROOT/'evidence/matches/main-frame-heap-core324-20261101.json'
PINS=PROFILE.parent/'generator-pins.json'


def execute_pairs(image,rebuilt,wrappers):
    counts={a:0 for a in native.CORE};visited={a:set()for a in native.CORE};records=[];wrapper_returns=0;stops=0;other_returns=0
    for entry,size,vectors in[(native.CREATOR,56,1426),(native.ALLOCATOR,52,1568)]:
        original=image[entry-0x02000000:entry-0x02000000+size]
        for index in range(vectors):
            first=native.execute(image,entry,original,index);second=native.execute(rebuilt,entry,wrappers[entry],index)
            if first!=second:raise ValueError('Original/source-linked core own returns/registers/memory/stops differ')
            if first['actualOwnReturn']:
                if not first['case']['modelDomain']or not first['modelPassed']:raise ValueError('Independent core model unavailable or differs for returned context')
                wrapper_returns+=2
                for item in first['actualOwnedCoreReturns']:
                    address=int(item['address'],0);counts[address]+=2
                    if item['registers'][0]!=first['result']:raise ValueError('Outer wrapper did not forward actual owned core return')
                other_returns+=2*sum(a not in native.CORE for a in first['actualOriginalHelperReturnsSeparate'])
                for address,length in native.CORE_CODE.items():visited[address].update(pc for pc in first['visited']if address<=pc<address+length)
            else:stops+=1
            records.append(dict(wrapper=hex(entry),index=index,result=first))
        print(json.dumps(dict(wrapper=hex(entry),contexts=vectors,sourceCredit=0)),flush=True)
    for address,length in native.CORE_CODE.items():
        if visited[address]!=set(range(address,address+length,4))or counts[address]==0:raise ValueError('Owned core complete native code/actual return evidence missing')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'source-linked-native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(actualOwnedCoreReturns={hex(a):n for a,n in counts.items()},actualOwnSourceAndNativeReturns=sum(counts.values()),
        actualOuterWrapperReturnsSeparate=wrapper_returns,actualOtherOriginalHelperReturnsSeparate=other_returns,
        pairedBoundedNoReturnContexts=stops,boundedStopPostStateCredit=0,providerReplacements=[],
        completeCodeCoverage={hex(a):dict(codeBytes=n,visited=sorted(visited[a]),unvisited=[])for a,n in native.CORE_CODE.items()},
        ownedReturnCalleeSavedStackAndForwardedR0Verified=True,fullRawRegistersFlagsMappedMemoryStackOrderedEffectsCompared=True,
        trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),
        newWrapperSourceCredit=0,otherOriginalCalleeDataOrAssemblyCredit=0,maxInstructionsPerExecution=20000)


def main():
    for item in json.loads(PINS.read_text())['files']:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Required core/source-linked/runtime input missing or changed')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    if hashlib.sha256(image).hexdigest()!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('Measured main module differs')
    rebuilt=bytearray(image);rows=[]
    for pin in json.loads(PROFILE.read_text())['matches']:
        entry,bindings,link,unused,body=compiler.build(pin,WORK/pin['address'])
        address=int(pin['address'],0);rebuilt[address-0x02000000:address-0x02000000+len(body)]=body
        rows.append(dict(entry,realMainLink=link,nativeSymbolEntries=bindings,nativeSymbols={k:hex(int(v['address'],0))for k,v in bindings.items()},
            exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,matchingBytes=pin['bytes'],sourceOnlyCompilerInput=dict(source=pin['source'],sha256=pin['sourceSha256'],includes=pin['sourceDependencies'],originalCodeCompilerInput=False),
            originalObjectScaffolding=False,wholeModuleLinked=False,sourceAbiContract=dict(physicalArgumentWords=3,guestWordAndPointerBits=32,originalHistoricalTypesProven=False),
            sourceStorageView=dict(commonBytes=36,frameBytes=12,combinedPrefixBytes=48,originalTotalObjectExtentProven=False)))
    wrapper_code={};closure=[]
    for pin in json.loads(WRAPPERS.read_text())['matches']:
        entry,bindings,link,unused,body=compiler.build(pin,WORK/'source-linked-wrappers'/pin['address']);address=int(pin['address'],0)
        wrapper_code[address]=body;rebuilt[address-0x02000000:address-0x02000000+len(body)]=body
        closure.append(dict(entry=entry,bindings=bindings,realMainLink=link,additionalSourceCredit=0))
    if bytes(rebuilt)!=image:raise ValueError('Fresh compiled owned/source-linked ranges change original module bytes')
    evidence=execute_pairs(image,bytes(rebuilt),wrapper_code)
    for row in rows:row['oracle']=dict(actualOwnSourceAndNativeReturns=evidence['actualOwnedCoreReturns'][row['address']],measure='source-linked-wrapper-contexts',coreProofOwnsOnlyThisQualifiedIdentity=True)
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm9',program='',module='main',
        romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=rows,nativeSymbols={k:v for row in rows for k,v in row['nativeSymbols'].items()},
        sourceLinkedWrappers=closure,sourceLinkedCoreEvidence=evidence,matchedInitializedBytes=324,matchedInstructionBytes=320,generatedLiteralBytes=4,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in json.loads(PINS.read_text())['files']})],
        pinnedGeneratorAndRuntimeDependencies=json.loads(PINS.read_text())['files'],
        newOrdinaryFunctionCount=3,initializedDenominatorDelta=0,additionalOtherCalleeDataOrAssemblyCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnedCoreReturns=evidence['actualOwnedCoreReturns'])),flush=True)


if __name__=='__main__':main()
