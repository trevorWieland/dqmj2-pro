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
import arm7_sdk243_mlme_indications_native_20261101 as native
import compile_arm7_sdk244_mlme484_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import match_arm7_main_spi276_20261101 as strict
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk244-mlme484-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk244-mlme484-final'
REPORT=ROOT/'evidence/matches/arm7-sdk244-mlme484-20261101.json'

def layout(seed):
    directory=WORK/'layout';directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';expressions=['sizeof(u32)', 'sizeof(void*)', 'sizeof(WL_MAN)', 'sizeof(WlMlmeAssInd)', 'sizeof(WlMlmeReAssInd)', '(u32)&((WL_MAN*)0)->HeapMan.HeapInfo', '(u32)&((WL_MAN*)0)->HeapMan.HeapInfo.heapType', '(u32)&((WL_MAN*)0)->HeapMan.HeapInfo.func.os.id', '(u32)&((WL_MAN*)0)->HeapMan.HeapInfo.func.os.heapHandle', '(u32)&((WL_MAN*)0)->HeapMan.TmpBuf', '(u32)&((WlMlmeAssInd*)0)->header.code', '(u32)&((WlMlmeAssInd*)0)->header.length', '(u32)&((WlMlmeAssInd*)0)->peerMacAdrs', '(u32)&((WlMlmeAssInd*)0)->aid', '(u32)&((WlMlmeAssInd*)0)->ssidLength', '(u32)&((WlMlmeAssInd*)0)->ssid', '(u32)&((SSID_ELEMENT*)0)->Length', '(u32)&((SSID_ELEMENT*)0)->SSID', 'sizeof(SSID_ELEMENT)', '(u32)&((WL_MAN*)0)->Work.FatalErr', 'sizeof(((WL_MAN*)0)->Work.FatalErr)']
    source.write_text('#include "ordinary_wireless.c"\nconst u32 sdk244_layout[]={'+','.join(expressions)+'};\n',encoding='utf-8');command=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk244_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if not elf.little_endian or elf.elfclass!=32:raise ValueError('Full typed TX compiler physical ABI differs')
    values=list(struct.unpack('<21I',raw))
    if values!=[4,4,0x694,58,58,380,380,384,388,392,12,14,16,22,24,26,1,2,34,1012,2]:raise ValueError('Complete TX queue/frame/camera/OS queue offsets differ')
    return dict(values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=command,actualCwd=str(ROOT),sourceDataCredit=0)

def flattened(seed):
    source=ROOT/seed['source'];text=source.read_text()
    return re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:(source.parent/m[1]).read_text(),text)

def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Complete MLME source/type/native/tool closure differs')
    seeds=json.loads((SOURCE/'profile.json').read_text())['units'];proof=layout(seeds[0]);main=(ROOT/seeds[0]['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();rows=[];wrongs=[];symbols={};own_total=helper_total=setup_total=0
    for seed in seeds:
        address=int(seed['address'],0);size=seed['bytes'];code=native.CODES[address];directory=WORK/seed['address'][2:];row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],directory/'positive');records=[];visited=set();helpers=setup=0;cases=[c for c in native.cases()if c['entry']==address]
        if body!=main[address-native.MAIN:address-native.MAIN+size]:raise ValueError('Entire freshly linked MLME C body differs')
        for index,case in enumerate(cases):
            original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
            if original!=compiled or not original['actualOwnReturn']or not original['modelPassed']:raise ValueError('MLME fresh original/source model, CPU, RAM or stores differ')
            if not all(r['actualReturn']and r['calleeSavedPreserved']for r in original['actualNativeHelperReturns']):raise ValueError('Focused native helper did not return with its register contract')
            records.append(dict(original=original,compiled=compiled));visited.update(a for a in original['visited']if address<=a<address+code);helpers+=2*len(original['actualNativeHelperReturns']);setup+=2*len(original['actualSetupReturns'])
        if visited!=set(range(address,address+code,4)):raise ValueError('Complete MLME own code not visited')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=directory/'positive/native-records.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));trace=dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0);own=2*len(records)
        oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=own,actualOriginalHelperReturns=helpers,actualNativeSetupEntryReturns=setup,constructorActualReturns=0,allOwnInstructionsVisited=True,ownInstructionCount=code//4,allRawCpuFlagsStackRamAndOrderedWritesCompared=True,independentIndicationHeaderAidSsidAndOwnStoresModel=True,originalOsHeapAndQueueActuallyInitialized=True,allocationFailureAndOriginalFatalEffects=True,fullUnsignedByteSsidLengthWithCopyCap32=True,providerReplacements=[],sceneNetworkConcurrencyAndRealProducerUnproved=True,trace=trace)
        abi=dict(physicalArgumentWords=3,declaredArguments=['halfword-aligned6-byte MAC backing','u16 AID','readable34-byte SSID element with byte alignment'],declaredReturn='u32 success boolean',allSdkLongPointerAndTargetWordsBytes=4,ssidLengthRawUnsignedByte=True,ssidPayloadCopyBound=32,originalOsHeapAndQueueRequired=True,opaqueCalleeSourceAndAssemblyCredit=0)
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=abi,oracle=oracle);rows.append(row)
        for name,value in row['nativeSymbols'].items():
            if name in symbols and symbols[name]!=value:raise ValueError('MLME symbol identities conflict')
            symbols[name]=value
        text=flattened(seed);definition=re.search(r'\bu32\s+'+seed['name']+r'\s*\([^)]*\)\s*\{',text)
        if definition is None:raise ValueError('Target MLME ordinary C definition missing')
        start=definition.start();opening=text.index('{',start);depth=1;end=opening+1
        while depth:
            if text[end]=='{':depth+=1
            elif text[end]=='}':depth-=1
            end+=1
        mutations=[('aid & 0x0FFF','aid & 0x07FF')]if address==0x027edc6c else[('0x87','0x86')]
        mutations+=[('WL_WriteByte(&pInd->ssid[i], 0);','WL_WriteByte(&pInd->ssid[i], 255);'),('return 0 ;','return 1 ;')]
        for index,(old,new)in enumerate(mutations):
            fragment=text[start:end]
            if fragment.count(old)!=1:raise ValueError('Unique target-only wrong MLME C site missing:'+old)
            changed=text[:start]+fragment.replace(old,new)+text[end:];altered,build=diagnostic.build(seed,changed,directory/('wrong-'+str(index)),link['bindings']);returned=rejected=0
            for vector,case in enumerate(cases):
                result=native.run(main,wram,case,vector,body=altered);returned+=int(result['actualOwnReturn']);rejected+=int(not result.get('modelPassed',False))
            if not rejected:raise ValueError('Wrong MLME C survived independent return/field model')
            wrongs.append(dict(address=seed['address'],mutation=[old,new],build=build,actualOwnReturns=returned,modelRejections=rejected))
        try:strict.compile_unit(seed,ROOT/seed['source'],directory/'original-default-word-refusal',strict=True)
        except ValueError as error:row['originalDefaultRefusal']=dict(errorType=type(error).__name__,error=str(error))
        else:raise ValueError('Frozen default unknown-word refusal disappeared')
        own_total+=own;helper_total+=helpers;setup_total+=setup
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=seeds[0]['romSha256'],matches=rows,nativeSymbols=symbols,matchedInitializedBytes=484,matchedCodeBytes=472,generatedLiteralBytes=12,newOrdinaryFunctionCount=2,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=own_total,totalActualHelperReturns=helper_total,totalActualSetupEntryReturns=setup_total,totalActualPrefixFillReturns=own_total,constructorActualReturnCredit=0,calleeSourceCredit=0,wrongC=wrongs,abiLayoutProof=proof,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,additionalCDefinitionsInTypedUnitHaveNoSourceCredit=True)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=484,ownReturns=own_total,helperReturns=helper_total,setupReturns=setup_total,wrong=[dict(returns=r['actualOwnReturns'],rejects=r['modelRejections'])for r in wrongs])),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=180);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(process.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(process.stderr[-7000:])
    print(process.stdout.strip(),flush=True)
if __name__=='__main__':main()
