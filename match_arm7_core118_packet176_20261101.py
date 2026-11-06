import gzip
import hashlib
import json
from pathlib import Path
import compile_arm7_core118_packet176_20261101 as compiler
import arm7_core118_packet176_native_20261101 as native
import compile_arm7_core117_state240_20261101 as caller_compiler
import arm7_core117_state240_native_20261101 as caller_native
import prove_arm7_lane_setting_producer_20261031 as pointer_producer
import audit_arm7_lane_scope107_20261101 as exclusion
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core118-packet176-final'
WORK=ROOT/'work/arm7-bulk-20261030/core118-packet176-final'
REPORT=ROOT/'evidence/matches/arm7-core118-packet176-20261101.json'
PINS=SOURCE/'generator-pins.json'
SNAPSHOT='evidence/verification/lane-root108-connected-exclusion-observed-20261101.json'
POINTER_SHA='e372dd000041574275ca9852f7f5ca57a4fbe41acb4a1c0c4eed50ad8447c8f4'


def save_trace(records,path):
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));return dict(path=path.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(path),gzipMtime=0)


def main():
    pointer_producer.main()
    if sha256(ROOT/'evidence/attempts/arm7-lane-setting-producer-20261031.json')!=POINTER_SHA:raise ValueError('Fresh descriptor pointer producer qualification changed')
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Current packet176 source/runtime/input closure differs')
    seed=json.loads((SOURCE/'profile.json').read_text())['units'][0];entry=int(seed['address'],0);selected=json.loads((ROOT/SNAPSHOT).read_text())['functions']
    if any(exclusion.overlaps(selected,('arm7','','arm7-main',mode,entry,176))for mode in('arm','thumb')):raise ValueError('Helper overlaps normalized historical selected C source')
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();original=main[entry-native.MAIN:entry-native.MAIN+176];row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'caller',strict=True)
    if body!=original:raise ValueError('Fresh complete C/helper link differs')
    records=[];visited=set();helpers=0;outcomes=set();raw_results=set()
    for index,case in enumerate(native.cases()):
        first=native.run(main,wram,entry,original,case,index);second=native.run(main,wram,entry,body,case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/C raw ABI/halfword/packet/frame model differs')
        records.append(dict(case=case,execution=first));visited.update(first['visited']);helpers+=2*first['scopedHelperReturnEvents'];raw_results.add(first['rawResult']);outcomes.add((case['value']<10,case['writePort']!=0,case['active']!=0,case['selector']==1))
    if not set(range(entry,entry+168,4)).issubset(visited)or len(outcomes)!=16 or raw_results!={0,5}:raise ValueError('Full direct supported branch/result/instruction domains differ')
    caller_seed=json.loads((ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core117-state240-final/profile.json').read_text())['units'][0];caller_row,caller_link,caller_body=caller_compiler.compile_unit(caller_seed,ROOT/caller_seed['source'],WORK/'connected104',strict=True);linked_main=bytearray(main);linked_main[0x91bc:0x91bc+176]=body;linked_main[0x9c58:0x9c58+104]=caller_body;connected=[];linked_returns=0;original_byte_returns=0
    for index,case in enumerate(caller_native.cases(0x027e9c58)):
        first=caller_native.run(main,wram,0x027e9c58,main[0x9c58:0x9c58+104],case,index);second=caller_native.run(bytes(linked_main),wram,0x027e9c58,caller_body,case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Fresh compiled104->compiled176 source closure state/return differs')
        connected.append(dict(case=case,execution=second));linked_returns+=2*sum(x['entry']=='0x27e91bc'for x in second['helpers']);original_byte_returns+=2*sum(x['entry']=='0x27ead30'for x in second['helpers'])
    symbols={name:hex(int(binding['address'],0))for name,binding in link['bindings'].items()};row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=symbols,nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceAbiContract=dict(physicalArgumentWords=2,rawUnsigned32ArgumentTypesCompatibleWithFrozen104=True,fullValueThresholdAndFullSecondArgumentZeroPredicate=True,low16ContextAndOptionalVolatilePortStores=True,byteHalfwordReadModifyWriteHelperOriginal=True,rawReturns=[0,5],historicalPublicMeaningProven=False,pointerOrPointeeSourceDataCredit=0),oracle=dict(vectors=len(records),actualOriginalAndCompiledOwnReturns=2*len(records),actualProducerFillReturnsSeparateZeroCredit=2*len(records),constructorActualReturnCredit=0,originalByteHelperReturnsSeparateZeroCredit=helpers,allOwnInstructionsAndSupportedBranchesVisited=True,fullRawCpuFlagsFramesMappedMemoryAndOrderedReadsWritesCompared=True,independentDescriptorInitializationHalfwordPacketAndFlagModel=True,syntheticOverridesDeclaredPerCase=True,providerReplacements=[],physicalHardwareOrSceneContextProven=False,maximumInstructionsPerEntry=250000,trace=save_trace(records,WORK/'direct-native-records.json.gz')))
    names={Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins};report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols=symbols,runtimePointerQualification=dict(report='evidence/attempts/arm7-lane-setting-producer-20261031.json',sha256=POINTER_SHA,storageBytes=4,sourceDataCredit=0),callerSpecificLinker=dict(path=Path(compiler.linker.__file__).name,sha256=sha256(compiler.linker.__file__),exactCallerSourceHashAndFullIdentityRequired=True,defaultAndState240PoliciesUnchanged=True,sourceDataCredit=0),connectedSourceClosure=dict(caller=caller_row,realLink=caller_link,sourceLinkedCallee=row['source'],freshOriginalAndCompiledCallerReturnsZeroAdditionalCredit=2*len(connected),freshCompiled176ScopedReturnsWithOriginalCounterpartZeroAdditionalCredit=linked_returns,originalByteHelperScopedReturnsZeroAdditionalCredit=original_byte_returns,actualFillReturnsSeparateZeroCredit=2*len(connected),constructorActualReturns=0,additionalSourceCredit=0,trace=save_trace(connected,WORK/'connected104-native-records.json.gz')),originalHelperDependencies=[dict(processor='arm7',program='',module='arm7-main',mode='arm',address='0x27ead30',bytes=44,spanSha256=hashlib.sha256(main[0xad30:0xad30+44]).hexdigest(),sourceCredit=0,originalCodeScaffolding=True)],generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in sorted(names)],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=1,matchedInitializedBytes=176,matchedCodeBytes=168,generatedLiteralBytes=8,initializedDenominatorDelta=0,totalActualOwnReturns=2*len(records),totalProducerFillReturnsSeparateZeroCredit=2*len(records),constructorActualReturnCredit=0,totalOriginalByteHelperReturnEventsSeparateZeroCredit=helpers,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),ownReturns=report['totalActualOwnReturns'],byteHelperReturns=helpers,connectedCallerReturns=2*len(connected),connected176ScopedReturns=linked_returns)),flush=True)
if __name__=='__main__':main()
