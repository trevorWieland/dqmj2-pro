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
import arm7_sdk250_parameters_native_20261101 as native
import compile_arm7_sdk251_parameters_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk251-parameters220-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk251-parameters220-final'
REPORT=ROOT/'evidence/matches/arm7-sdk251-parameters220-20261101.json'

def layout(seed):
    directory=WORK/'layout';directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';expressions=['sizeof(WL_MAN)','(u32)&((WL_MAN*)0)->Rand','(u32)&((WL_MAN*)0)->Rand.a','(u32)&((WL_MAN*)0)->Rand.b','(u32)&((WL_MAN*)0)->Work.BSSID','(u32)&((WL_MAN*)0)->Work.DTIMPeriod']
    source.write_text('#include "ordinary_wireless.c"\nconst u32 sdk251_layout[]={'+','.join(expressions)+'};\n',encoding='utf-8');command=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-i',str((ROOT/seed['source']).parent),'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk251_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if not elf.little_endian or elf.elfclass!=32:raise ValueError('Compiler word/pointer layout changed')
    values=list(struct.unpack('<6I',raw))
    if values!=[0x694,0x5f0,0x5f0,0x5f2,0x3a8,0x3b8]:raise ValueError('Complete WL context field offsets changed')
    return dict(expressions=expressions,values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=command,actualCwd=str(ROOT),sourceDataCredit=0)

def flattened(seed):
    source=ROOT/seed['source'];text=source.read_text()
    return re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:(source.parent/m[1]).read_text(),text)

def fragment(text,name):
    found=list(re.finditer(r'\b(?:void|u16)\s+'+name+r'\s*\([^;{}]*\)\s*\{',text))
    if len(found)!=1:raise ValueError('Unique ordinary parameter definition missing')
    start=found[0].start();end=text.index('{',start)+1;depth=1
    while depth:
        if text[end]=='{':depth+=1
        elif text[end]=='}':depth-=1
        end+=1
    return start,end

def exclusion(seeds):
    snapshot=ROOT/'evidence/verification/accepted-cohort129-identities-v2-20261101.json'
    if sha256(snapshot)!='ecb74fb8b8e85677badf2afc3caa35bf8d023c7ab500bac1d6a3c51efb185013':raise ValueError('Frozen normalized accepted snapshot changed')
    identities={(r['processor'],r.get('program',''),r['module'],r['mode'],int(r['address'],0)if isinstance(r['address'],str)else r['address'])for r in json.loads(snapshot.read_text())['functions']}
    for seed in seeds:
        if(seed['processor'],seed.get('program',''),seed['module'],seed['mode'],int(seed['address'],0))in identities:raise ValueError('Parameter identity already accepted')
    return dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot),qualifiedIdentityCount=len(identities),currentUnitsAbsent=True,numericHexAndIntegerAddressNormalization=True)

def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Source/model/linker/producer closure changed')
    seeds=json.loads((SOURCE/'profile.json').read_text())['units'];audit=exclusion(seeds);proof=layout(seeds[0]);main=(ROOT/seeds[0]['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();matches=[];wrong=[];own=helper=prefix=0
    changes={'WSetBssid':[('pBssid[0] & 0x0001','pBssid[0] & 0x0002'),('0x0001 << 10','0x0001 << 9')],'WSetDTIMPeriod':[('period > 255','period > 254'),('0x088','0x08A')],'RND_init':[('0xFFF8','0xFFF0'),('b | 1','b | 2')]}
    for seed in seeds:
        row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['name']/'positive');top=int(seed['address'],0);size=seed['bytes'];records=[];visited=set();helpers=fills=0;vectors=[(i,c)for i,c in enumerate(native.cases())if c['entry']==top]
        if body!=main[top-native.MAIN:top-native.MAIN+size]:raise ValueError('Fresh complete compiled parameter differs')
        for index,case in vectors:
            original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
            if original!=compiled or not original['actualOwnReturn']or not original['modelPassed']:raise ValueError('Original/fresh-C raw CPU/RAM/state/helper contracts differ')
            records.append(dict(original=original,compiled=compiled));visited.update(a for a in original['visited']if top<=a<top+native.CODES[top]);helpers+=2*len(original['actualNativeHelperReturns']);fills+=2*len(original['actualPrefixFillReturns'])
        if visited!=set(range(top,top+native.CODES[top],4)):raise ValueError('Complete parameter instructions not covered')
        path=WORK/seed['name']/'positive/native-records.json.gz';raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(gzip.compress(raw,mtime=0));trace=dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)
        oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),actualOriginalHelperReturns=helpers,actualPrefixFillReturns=fills,actualNativeSetupEntryReturns=0,constructorActualReturns=0,allOwnInstructionsVisited=True,ownInstructionCount=native.CODES[top]//4,allRawCpuFlagsStackRamAndOrderedWritesCompared=True,independentFullNonstackMemoryAndOrderedStores=True,providerReplacements=[],sourceDataAndSceneCredit=0,trace=trace)
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=seed['nativeInterfaceContract'],oracle=oracle);matches.append(row);own+=2*len(records);helper+=helpers;prefix+=fills;text=flattened(seed);start,end=fragment(text,seed['name'])
        for number,(old,new)in enumerate(changes[seed['name']]):
            part=text[start:end]
            if part.count(old)!=(2 if seed['name']=='WSetBssid'and number==1 else 1):raise ValueError('Target-only mutation site changed')
            changed=text[:start]+part.replace(old,new)+text[end:];altered,build=diagnostic.build(seed,changed,WORK/seed['name']/('wrong-'+str(number)),link['bindings']);returned=rejected=0
            for index,case in vectors:
                result=native.run(main,wram,case,index,body=altered);returned+=int(result['actualOwnReturn']);rejected+=int(not result['modelPassed'])
            if not rejected:raise ValueError('Returning wrong parameter C escaped independent model')
            wrong.append(dict(name=seed['name'],mutation=[old,new],build=build,actualOwnReturns=returned,modelRejections=rejected))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=seeds[0]['romSha256'],matches=matches,nativeSymbols={name:value for row in matches for name,value in row['nativeSymbols'].items()},matchedInitializedBytes=220,matchedCodeBytes=sum(native.CODES.values()),generatedLiteralBytes=220-sum(native.CODES.values()),newOrdinaryFunctionCount=3,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=own,totalActualHelperReturns=helper,totalActualSetupEntryReturns=0,totalActualPrefixFillReturns=prefix,constructorActualReturnCredit=0,calleeSourceCredit=0,wrongC=wrong,abiLayoutProof=proof,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,additionalCDefinitionsInTypedUnitHaveNoSourceCredit=True,acceptedSnapshotExclusion=audit)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=220,ownReturns=own,helperReturns=helper,prefixFillReturns=prefix,wrong=[dict(name=r['name'],returns=r['actualOwnReturns'],rejects=r['modelRejections'])for r in wrong])),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=600);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(process.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(process.stderr[-7000:])
    print(process.stdout.strip(),flush=True)

if __name__=='__main__':main()
