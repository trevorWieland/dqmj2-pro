import argparse
import gzip
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path
import match_runtime
import arm7_sdk221_tx544_native_20261101 as native
import compile_arm7_sdk222_tx544_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import match_arm7_main_spi276_20261101 as strict
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk222-tx544-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk222-tx544-final'
REPORT=ROOT/'evidence/matches/arm7-sdk222-tx544-20261101.json'

def layout(seed):
    directory=WORK/'layout';directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';expressions=['sizeof(u32)','sizeof(void*)','sizeof(WL_MAN)','sizeof(TXQ)','sizeof(HEAPBUF_MAN)','(u32)&((WL_MAN*)0)->TxCtrl.Txq[0]','(u32)&((WL_MAN*)0)->HeapMan.TxPri[0]','(u32)&((WL_MAN*)0)->HeapMan.TxPri[0].Count','(u32)&((WL_MAN*)0)->Work.PowerState','(u32)&((WL_MAN*)0)->CamMan.PowerState','(u32)&((WlMaDataReq*)0)->frame','(u32)&((TXFRM*)0)->Dot11Header.FrameCtrl.Data','sizeof(MAC_HEADER)','sizeof(DATA_HEADER)','sizeof(OSMessageQueue)','(u32)&((WL_MAN*)0)->pSendMsgQueue']
    source.write_text('#include "native_host_arm7_main_027eff00.c"\nconst u32 sdk222_layout[]={'+','.join(expressions)+'};\n',encoding='utf-8');command=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk222_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if not elf.little_endian or elf.elfclass!=32:raise ValueError('Full typed TX compiler physical ABI differs')
    values=list(struct.unpack('<16I',raw))
    if values!=[4,4,0x694,20,12,0x42c,0x194,0x19c,0x354,0x530,16,20,12,24,32,0x304]:raise ValueError('Complete TX queue/frame/camera/OS queue offsets differ')
    return dict(values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=command,actualCwd=str(ROOT),sourceDataCredit=0)

def flattened(seed):
    source=ROOT/seed['source'];text=source.read_text()
    return re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:(source.parent/m[1]).read_text(),text)

def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Complete TX source/header/native/tool closure differs')
    seed=json.loads((SOURCE/'profile.json').read_text())['units'][0];proof=layout(seed);row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'positive');main=(ROOT/seed['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();records=[];visited=set();callbacks=setup_returns=0
    if body!=main[native.TOP-native.MAIN:native.TOP-native.MAIN+544]:raise ValueError('Whole freshly compiled TX function differs')
    for index,case in enumerate(native.cases()):
        original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
        if original!=compiled or not original['actualOwnReturn']or not original['modelPassed']:raise ValueError('TX original/fresh-C ABI/own fields/callback effects differ')
        records.append(dict(original=original,compiled=compiled));visited.update(a for a in original['visited']if native.TOP<=a<native.TOP+532);callbacks+=2*len(original['actualCallbackReturns']);setup_returns+=2*len(original['actualSetupReturns'])
    if visited!=set(range(native.TOP,native.TOP+532,4)):raise ValueError('Complete133 own TX instructions not visited')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/'positive/native-records.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));trace=dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0);own=2*len(records)
    oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=own,actualNativeCallbackReturns=callbacks,actualNativeSetupEntryReturns=setup_returns,constructorActualReturns=0,allOwnInstructionsVisited=True,ownInstructionCount=133,allRawCpuFlagsStackRamAndOrderedWritesCompared=True,independentOwnStoresAndCallbackAbiModel=True,baselineQueueAndPositiveFrameCompleteNonstackModelSeparatelyDemonstrated=True,realModeQueueCamAndTxInitializersRetained=True,realPowerIrqTimeoutCopierAndCallbacksRetained=True,providerReplacements=[],syntheticCamStateActiveAndFrameCountOverridesExplicit=True,dmaMaxCountZeroCpuFallbackPrerequisite=True,physicalNetworkDmaConcurrencyAndSceneReachabilityUnproved=True,trace=trace)
    abi=dict(physicalArgumentWords=1,declaredArgument='SDK u32 priority0..2',declaredReturn='void',callbackArguments=['frame pointer',0],callbackReturnDeclared='void',allSdkLongPointerAndTargetWordsBytes=4,priorityOutside0To2AndInvalidPointersUnsupported=True,opaqueCallbackSourceAndAssemblyCredit=0)
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=abi,oracle=oracle)
    text=flattened(seed);definition=re.search(r'\bvoid\s+TxqPri\s*\(u32\s+pri\)\s*\{',text)
    if definition is None:raise ValueError('Unique target C definition missing')
    start=definition.start();opening=text.index('{',start);depth=1;end=opening+1
    while depth:
        if text[end]=='{':depth+=1
        elif text[end]=='}':depth-=1
        end+=1
    wrong=[]
    for index,(old,new)in enumerate([('pTxq->InCount++;','pTxq->InCount += 2;'),('OS_DisableIrqMask((1UL << 24) )','OS_DisableIrqMask((1UL << 23) )')]):
        fragment=text[start:end]
        if fragment.count(old)!=1:raise ValueError('Target-only wrong TX source site differs')
        changed=text[:start]+fragment.replace(old,new)+text[end:];altered,build=diagnostic.build(seed,changed,WORK/('wrong-'+str(index)),link['bindings']);returned=rejected=0
        for vector,case in enumerate(native.cases()):
            result=native.run(main,wram,case,vector,body=altered);returned+=int(result['actualOwnReturn']);rejected+=int(not result['modelPassed'])
        if not rejected:raise ValueError('Returning wrong TX C escaped independent own/IRQ contract model')
        wrong.append(dict(mutation=[old,new],build=build,actualOwnReturns=returned,modelRejections=rejected))
    try:strict.compile_unit(seed,ROOT/seed['source'],WORK/'original-default-word-refusal',strict=True)
    except ValueError as error:refusal=dict(errorType=type(error).__name__,error=str(error))
    else:raise ValueError('Frozen default TX data-word refusal disappeared')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=seed['romSha256'],matches=[row],nativeSymbols=row['nativeSymbols'],matchedInitializedBytes=544,matchedCodeBytes=532,generatedLiteralBytes=12,newOrdinaryFunctionCount=1,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=own,totalActualCallbackReturns=callbacks,totalActualSetupEntryReturns=setup_returns,totalActualPrefixFillReturns=own,constructorActualReturnCredit=0,calleeSourceCredit=0,wrongC=wrong,originalDefaultRefusal=refusal,abiLayoutProof=proof,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,additionalCDefinitionsInTypedUnitHaveNoSourceCredit=True)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=544,ownReturns=own,callbackReturns=callbacks,setupReturns=setup_returns,wrong=[dict(returns=r['actualOwnReturns'],rejects=r['modelRejections'])for r in wrong])),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=180);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(process.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(process.stderr[-7000:])
    print(process.stdout.strip(),flush=True)
if __name__=='__main__':main()
