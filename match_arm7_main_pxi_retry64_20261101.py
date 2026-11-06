import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_main_pxi_retry64_native_20261101 as native
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-pxi-retry64-final'
WORK=ROOT/'work/arm7-bulk-20261030/pxi-retry64-final'
REPORT=ROOT/'evidence/matches/arm7-main-pxi-retry64-20261101.json'
PINS=SOURCE/'generator-pins.json'
compile_unit=compiler.compile_unit

def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        p=(ROOT/item['path']).resolve()
        if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=item['sha256']:raise ValueError('Complete retry caller/typed sender/source runtime differs')
    ownership=compiler.ownership();profile=json.loads((SOURCE/'profile.json').read_text());row,link,body=compile_unit(profile['newUnit'],ROOT/profile['newUnit']['source'],WORK/'caller');dependencies=[compile_unit(seed,ROOT/seed['source'],WORK/'dependencies'/seed['address'][2:])for seed in profile['dependencies']];pack=dependencies[0][2];send=dependencies[1][2];main=(ROOT/row['binary']).read_bytes();wram=(ROOT/profile['dependencies'][0]['binary']).read_bytes();own=main[native.ENTRY-native.MAIN:native.ENTRY-native.MAIN+64];old_pack=wram[native.PACKER-native.WRAM:native.PACKER-native.WRAM+56];old_send=wram[native.SENDER-native.WRAM:native.SENDER-native.WRAM+96];records=[];visits={};pack_returns=send_returns=irq_returns=0
    if body!=own or pack!=old_pack or send!=old_send:raise ValueError('Entire fresh caller/packer/sender source bytes differ')
    for index,case in enumerate(native.cases()):
        first=native.execute(main,wram,own,old_pack,old_send,case,index);second=native.execute(main,wram,body,pack,send,case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/source retry full raw ABI/frames/status/packet model differs')
        records.append(dict(case=case,execution=first));pack_returns+=2*first['actualPackerReturns'];send_returns+=2*first['actualSenderReturns'];irq_returns+=2*first['actualIrqReturns']
        for name,items in first['visits'].items():visits.setdefault(name,set()).update(items)
    expected={hex(native.ENTRY):set(range(native.ENTRY,native.ENTRY+64,4)),hex(native.PACKER):set(range(native.PACKER,native.PACKER+56,4)),hex(native.SENDER):set(range(native.SENDER,native.SENDER+92,4)),hex(native.DISABLE):set(range(native.DISABLE,native.DISABLE+20,4)),hex(native.RESTORE):set(range(native.RESTORE,native.RESTORE+24,4))}
    if visits!=expected or len(records)!=661 or(pack_returns,send_returns,irq_returns)!=(3170,3170,4756):raise ValueError('Whole caller/dependency/branch/retry coverage or actual return accounting differs')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));unsupported=[]
    for status in(2,0x4000):
        case=dict(native.cases()[0],statuses=[status],repeatLast=True);first=native.execute(main,wram,own,old_pack,old_send,case,0,budget=2000,allow_no_return=True);second=native.execute(main,wram,body,pack,send,case,0,budget=2000,allow_no_return=True)
        if first!=second or first['actualOwnReturn']or first['attemptsStarted']<2:raise ValueError('Persistent FIFO failure acquired own return or was not retried')
        unsupported.append(dict(status=status,execution=first,additionalNestedReturnCredit=0,supportedErrorPathCredit=0))
    symbols={k:hex(int(v['address'],0))for k,v in link['bindings'].items()};closure=[]
    for old,old_link,old_body in dependencies:
        symbols.update({k:hex(int(v['address'],0))for k,v in old_link['bindings'].items()});closure.append(dict(old,realLink=old_link,sourceCredit=0,byteCredit=0,existingSelectionUnchanged=True))
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols={k:hex(int(v['address'],0))for k,v in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
        sourceAbiContract=dict(physicalArgumentWords=2,payload='0x8000 | ((selector << 8) & 0x7f00) | (value & 255)',packerArgumentWords=3,fixedTag=5,fixedError=0,retryWhileSignedResultNegative=True,measuredSuccessfulResult=0,historicalPublicMeaningProven=False),
        oracle=dict(vectors=661,actualOriginalAndCompiledReturns=1322,sourcePackerReturnsSeparateZeroCredit=pack_returns,sourceSenderReturnsSeparateZeroCredit=send_returns,originalIrqReturnsSeparateZeroCredit=irq_returns,fullFreshSourceCallerPackerSender=True,actualNativeIrqCodeRetained=True,independentWordPacketStackFramesRetryOrderAndPortModel=True,rawRegistersFlagsStackModeAndMappedMemoryCompared=True,providerReplacements=[],physicalPeripheralExecution=False,stableFifoStatusWithinEachAttempt=True,finiteStatusSequences=[list(x)for x in native.SEQUENCES],privilegedSystemModeAndIrqFiqMasksTested=True,completeOwnAndDependencyInstructionsVisited=True,unsupported=unsupported,maxInstructionsPerRun=10000,wholeSceneOrHardwareContextProven=False,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols=symbols,existingSourceDependencies=closure,runtimeOwnership=ownership,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=1,matchedInitializedBytes=64,matchedCodeBytes=64,generatedLiteralBytes=0,initializedDenominatorDelta=0,existingSourceBytesSeparateZeroCredit=152,totalActualOwnReturns=1322,totalExistingSourcePackerReturnsSeparateZeroCredit=3170,totalExistingSourceSenderReturnsSeparateZeroCredit=3170,totalOriginalIrqReturnsSeparateZeroCredit=4756,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=1322,sourcePackerAndSenderSeparate=[3170,3170],originalIrqSeparate=4756)),flush=True)
if __name__=='__main__':main()
