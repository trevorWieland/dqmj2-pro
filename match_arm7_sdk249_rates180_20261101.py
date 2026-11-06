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
import arm7_sdk248_rates180_native_20261101 as native
import compile_arm7_sdk249_rates180_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import match_arm7_main_spi276_20261101 as strict
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk249-rates180-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk249-rates180-final'
REPORT=ROOT/'evidence/matches/arm7-sdk249-rates180-20261101.json'

def layout(seed):
    directory=WORK/'layout';directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';expressions=['sizeof(u8)', 'sizeof(u16)', 'sizeof(u32)', 'sizeof(void*)', 'sizeof(SUP_RATE_ELEMENT)', 'sizeof(RATE_SET)', '(u32)&((SUP_RATE_ELEMENT*)0)->Length', '(u32)&((SUP_RATE_ELEMENT*)0)->SupportedRate', '(u32)&((RATE_SET*)0)->Basic', '(u32)&((RATE_SET*)0)->Support', 'sizeof(native_host_arm7_data_027f73c0)']
    source.write_text('#include "native_host_arm7_main_027ea4d0.c"\nconst u32 sdk249_layout[]={'+','.join(expressions)+'};\n',encoding='utf-8');command=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-i',str((ROOT/seed['source']).parent),'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk249_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if not elf.little_endian or elf.elfclass!=32:raise ValueError('Full typed TX compiler physical ABI differs')
    values=list(struct.unpack('<11I',raw))
    if values!=[1,2,4,4,4,4,1,2,0,2,240]:raise ValueError('Complete TX queue/frame/camera/OS queue offsets differ')
    return dict(values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=command,actualCwd=str(ROOT),sourceDataCredit=0)

def flattened(seed):
    source=ROOT/seed['source'];text=source.read_text()
    return re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:(source.parent/m[1]).read_text(),text)

def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Complete TX source/header/native/tool closure differs')
    seed=json.loads((SOURCE/'profile.json').read_text())['units'][0];proof=layout(seed);row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'positive');main=(ROOT/seed['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();records=[];visited=set();callbacks=setup_returns=0
    if body!=main[native.TOP-native.MAIN:native.TOP-native.MAIN+180]:raise ValueError('Whole freshly compiled TX function differs')
    for index,case in enumerate(native.cases()):
        original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
        if original!=compiled or not original['actualOwnReturn']or not original['modelPassed']:raise ValueError('TX original/fresh-C ABI/own fields/callback effects differ')
        records.append(dict(original=original,compiled=compiled));visited.update(a for a in original['visited']if native.TOP<=a<native.TOP+176);callbacks+=2*len(original['actualNativeHelperReturns']);setup_returns+=0
    if visited!=set(range(native.TOP,native.TOP+176,4)):raise ValueError('Complete91 own receive instructions not visited')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/'positive/native-records.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));trace=dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0);own=2*len(records)
    oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=own,actualOriginalHelperReturns=callbacks,actualNativeSetupEntryReturns=0,constructorActualReturns=0,allOwnInstructionsVisited=True,ownInstructionCount=44,allRawCpuFlagsStackRamAndOrderedWritesCompared=True,independentTwelveRateMapFullDataAndOrderedStoreModel=True,originalComplete120EntryLookupRetained=True,declaredTwoByteRateArrayDomain=True,providerReplacements=[],sourceAndOriginalDataCredit=0,trace=trace)
    abi=dict(physicalArgumentWords=2,declaredArguments=['complete4-byte rate element with length0..2','nonoverlapping halfword-aligned4-byte output'],declaredReturn='void',allSdkLongPointerAndTargetWordsBytes=4,sourceRateArrayCapacity=2,sourceLengthDomain=[0,2],completeOriginalTableEntries=120,completeOriginalTableBytes=240,opaqueCalleeSourceAndAssemblyCredit=0)
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=abi,oracle=oracle)
    text=flattened(seed);definition=re.search(r'\bvoid\s+WElement2RateSet\s*\([^)]*\)\s*\{',text)
    if definition is None:raise ValueError('Unique target C definition missing')
    start=definition.start();opening=text.index('{',start);depth=1;end=opening+1
    while depth:
        if text[end]=='{':depth+=1
        elif text[end]=='}':depth-=1
        end+=1
    wrong=[]
    for index,(old,new)in enumerate([('0x8000','0x4000'),('brate & 0x80','brate & 0x40')]):
        fragment=text[start:end]
        if fragment.count(old)!=2:raise ValueError('Target-only wrong TX source site differs')
        changed=text[:start]+fragment.replace(old,new)+text[end:];altered,build=diagnostic.build(seed,changed,WORK/('wrong-'+str(index)),link['bindings']);returned=rejected=0
        for vector,case in enumerate(native.cases()):
            result=native.run(main,wram,case,vector,body=altered);returned+=int(result['actualOwnReturn']);rejected+=int(not result['modelPassed'])
        if not rejected:raise ValueError('Returning wrong TX C escaped independent own/IRQ contract model')
        wrong.append(dict(mutation=[old,new],build=build,actualOwnReturns=returned,modelRejections=rejected))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=seed['romSha256'],matches=[row],nativeSymbols=row['nativeSymbols'],matchedInitializedBytes=180,matchedCodeBytes=176,generatedLiteralBytes=4,newOrdinaryFunctionCount=1,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=own,totalActualHelperReturns=callbacks,totalActualSetupEntryReturns=setup_returns,totalActualPrefixFillReturns=0,constructorActualReturnCredit=0,calleeSourceCredit=0,wrongC=wrong,abiLayoutProof=proof,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,additionalCDefinitionsInTypedUnitHaveNoSourceCredit=True)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=180,ownReturns=own,helperReturns=callbacks,setupReturns=setup_returns,wrong=[dict(returns=r['actualOwnReturns'],rejects=r['modelRejections'])for r in wrong])),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=600);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(process.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(process.stderr[-7000:])
    print(process.stdout.strip(),flush=True)
if __name__=='__main__':main()
