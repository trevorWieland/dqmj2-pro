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
import arm7_sdk262_element804_native_20261101 as native
import compile_arm7_sdk263_element804_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk263-element804-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk263-element804-final'
REPORT=ROOT/'evidence/matches/arm7-sdk263-element804-20261101.json'

def layout(seed):
    directory=WORK/'layout';directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';expressions=['sizeof(WL_MAN)','sizeof(ELEMENT_CHECKER)','sizeof(WlMlmeJoinReq)','sizeof(CF_PARAM_ELEMENT)','(u32)&((WL_MAN*)0)->Work.SSIDLength','(u32)&((WL_MAN*)0)->Work.SSID','(u32)&((WL_MAN*)0)->Work.SSIDMask','(u32)&((WL_MAN*)0)->Work.RateSet','(u32)&((WL_MAN*)0)->Work.BSSID','(u32)&((WL_MAN*)0)->Work.CurrChannel','(u32)&((WL_MAN*)0)->Work.CapaInfo','(u32)&((WL_MAN*)0)->MLME.State','(u32)&((WL_MAN*)0)->MLME.pReq','(u32)&((WlMlmeJoinReq*)0)->bssDesc.channel']
    for field in('pElement','rxStatus','capability','bodyLength','matchFlag','foundFlag','channel','rateSet','otherElementCount','otherElementLength','pSSID','pCFP','pTIM','pGMIF'):expressions.append('(u32)&((ELEMENT_CHECKER*)0)->'+field)
    source.write_text('#include "ordinary_wireless.c"\nconst u32 sdk263_layout[]={'+','.join(expressions)+'};\n',encoding='utf-8');argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-i',str((ROOT/seed['source']).parent),'-c',str(source),'-o',str(obj)];result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:raise ValueError(result.stdout+result.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk263_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
    values=list(struct.unpack('<'+str(len(expressions))+'I',raw));expected=[0x694,44,88,8,866,868,900,932,936,958,960,1028,1052,74,0,4,6,8,10,12,18,20,24,26,28,32,36,40]
    if values!=expected:raise ValueError('Complete parser, work, and join declaration layouts differ')
    return dict(expressions=expressions,values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=argv,actualCwd=str(ROOT),sourceDataCredit=0)

def flattened(seed):
    path=ROOT/seed['source'];return re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:(path.parent/m[1]).read_text(),path.read_text())

def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Complete source/model/tool closure changed')
    seed=json.loads((SOURCE/'profile.json').read_text())['units'][0];proof=layout(seed);row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'positive');main=(ROOT/seed['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();vectors=[(i,c)for i,c in enumerate(native.cases())if native.source_compatible(c)];records=[];visited=set();helpers=fills=0
    if body!=main[native.TOP-native.MAIN:native.TOP-native.MAIN+804]:raise ValueError('Complete freshly linked804 C bytes differ')
    for index,case in vectors:
        original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
        if original!=compiled or not original['actualOwnReturn']or not original['modelPassed']:raise ValueError('Original/fresh-C parser state, raw CPU, stores, or helper returns differ')
        records.append(dict(original=original,compiled=compiled));visited.update(a for a in original['visited']if native.TOP<=a<native.TOP+800);helpers+=2*len(original['actualNativeHelperReturns']);fills+=2*len(original['actualPrefixFillReturns'])
    if visited!=set(range(native.TOP,native.TOP+800,4)):raise ValueError('All200 parser instructions must be visited inside source-compatible domains')
    path=WORK/'positive/native-records.json.gz';raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(gzip.compress(raw,mtime=0));trace=dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0);oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),actualOriginalHelperReturns=helpers,actualPrefixFillReturns=fills,constructorActualReturns=0,allOwnInstructionsVisited=True,ownInstructionCount=200,allRawCpuFlagsStackRamAndOrderedWritesCompared=True,independentFullNonstackMemoryAndOrderedStores=True,sourceCompatibleCfpAlignmentRequired=True,rateHelperTwoByteCapacityRequired=True,completeStreamLengthAtMost512=True,providerReplacements=[],sourceDataAndSceneCredit=0,trace=trace)
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=seed['nativeInterfaceContract'],oracle=oracle);text=flattened(seed);found=list(re.finditer(r'\bvoid\s+ElementChecker\s*\([^;{}]*\)\s*\{',text))
    if len(found)!=1:raise ValueError('Unique structured C parser definition missing')
    start=found[0].start();end=text.index('{',start)+1;depth=1
    while depth:
        if text[end]=='{':depth+=1
        elif text[end]=='}':depth-=1
        end+=1
    wrong=[]
    for number,(old,new,count)in enumerate([('p->channel ==','p->channel !=',1),('!= 0x09','!= 0x08',1),('0x01 << 4','0x01 << 5',2),('p->otherElementCount++','p->otherElementCount += 2',2)]):
        part=text[start:end]
        if part.count(old)!=count:raise ValueError('Target-only parser mutation site changed')
        altered,build=diagnostic.build(seed,text[:start]+part.replace(old,new)+text[end:],WORK/('wrong-'+str(number)),link['bindings']);returned=rejected=0
        for index,case in vectors:
            result=native.run(main,wram,case,index,body=altered);returned+=int(result['actualOwnReturn']);rejected+=int(not result['modelPassed'])
        if not rejected:raise ValueError('Returning wrong parser C survived independent model')
        wrong.append(dict(mutation=[old,new],build=build,actualOwnReturns=returned,modelRejections=rejected))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=seed['romSha256'],matches=[row],nativeSymbols=row['nativeSymbols'],matchedInitializedBytes=804,matchedCodeBytes=800,generatedLiteralBytes=4,newOrdinaryFunctionCount=1,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=2*len(records),totalActualHelperReturns=helpers,totalActualSetupEntryReturns=0,totalActualPrefixFillReturns=fills,constructorActualReturnCredit=0,calleeSourceCredit=0,wrongC=wrong,abiLayoutProof=proof,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,additionalCDefinitionsInTypedUnitHaveNoSourceCredit=True,rawNativeCasesExcludedFromSourceScope=len(native.cases())-len(vectors),excludedReason='Odd alignment of stored CF_PARAM_ELEMENT pointer: source type requires two-byte alignment; raw native behavior remains separate',originalSsidAndRateHelpersSourceCredit=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=804,ownReturns=2*len(records),helperReturns=helpers,prefixFillReturns=fills,excludedNativeContexts=report['rawNativeCasesExcludedFromSourceScope'],wrong=[dict(returns=r['actualOwnReturns'],rejects=r['modelRejections'])for r in wrong])),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=1200);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(result.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(result.stderr,encoding='utf-8')
    if result.returncode:raise ValueError(result.stderr[-7000:])
    print(result.stdout.strip(),flush=True)

if __name__=='__main__':main()
