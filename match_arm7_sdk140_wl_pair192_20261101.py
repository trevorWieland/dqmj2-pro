import argparse
import gzip
import hashlib
import json
import os
import struct
import subprocess
import sys
from collections import Counter
from pathlib import Path
import match_runtime
import arm7_sdk140_rate64_native_20261101 as rate
import arm7_core124_helper128_native_20261101 as timestamp
import compile_arm7_sdk140_wl_pair192_20261101 as compiler
import compile_arm7_core126_state76_20261101 as getter_compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import match_arm7_main_spi276_20261101 as original_compiler
from project import ROOT,sha256,write_json
from elftools.elf.elffile import ELFFile

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk140-wl-pair192-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk140-wl-pair192-final'
REPORT=ROOT/'evidence/matches/arm7-sdk140-wl-pair192-20261101.json'

def measure_layout(seed):
    directory=WORK/'layout';directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o'
    text='#include "wl_measured_views.h"\n#define OF(t,f) ((u32)&((t *)0)->f)\nconst u32 native_wl_view_layout[] = {sizeof(u32),sizeof(unsigned long),sizeof(void *),sizeof(NativeRateSet),sizeof(NativeWlView),OF(NativeWlView,Work.RateSet),OF(NativeWlView,Work.BeaconPeriod),OF(NativeWlView,Work.DTIMPeriod),OF(NativeWlView,Work.FrameLifeTime),OF(NativeWlView,Config.FrameLifeTimePerBeacon)};\n'
    source.write_text(text,encoding='utf-8');argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(source),'-o',str(obj)];process=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='native_wl_view_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if not elf.little_endian or elf.elfclass!=32 or len(raw)!=40:raise ValueError('Measured ARM32 layout data shape differs')
    values=list(struct.unpack('<10I',raw))
    if values!=[4,4,4,4,0x3d4,0x3a4,0x3b2,0x3b8,0x3d0,0x338]:raise ValueError('Measured prefix/ABI offsets disagree with original native field widths/offsets')
    return dict(measuredValues=values,actualCompilerArgv=argv,actualCompilerCwd=str(ROOT),source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),originalObjectTotalExtentNotClaimed=True,sourceDataCredit=0)

def worker():
    for item in json.loads((SOURCE/'generator-pins.json').read_text())['files']:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Frozen source/native/header/tool/model input changed')
    profile=json.loads((SOURCE/'profile.json').read_text());layout=measure_layout(profile['units'][0]);units=[]
    for seed in profile['units']:units.append(compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:]))
    getter_seed=json.loads((ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core126-state76-final/profile.json').read_text())['units'][0]
    getter=getter_compiler.compile_unit(getter_seed,ROOT/getter_seed['source'],WORK/'existing-getter76-source-closure')
    main=(ROOT/profile['units'][0]['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();bodies={int(row['address'],0):body for row,link,body in units};bodies[0x027ea584]=getter[2]
    for address,body in bodies.items():
        if main[address-timestamp.MAIN:address-timestamp.MAIN+len(body)]!=body:raise ValueError('Fresh compiled closure differs from complete original bytes')
    rebuilt=bytearray(main)
    for address,body in bodies.items():rebuilt[address-timestamp.MAIN:address-timestamp.MAIN+len(body)]=body
    rebuilt=bytes(rebuilt);matches=[];total_helpers=0;total_returns=0
    for row,link,body in units:
        entry=int(row['address'],0);vectors=rate.cases()if entry==rate.TOP else timestamp.cases();records=[];visited=set();helper_counts=Counter()
        for index,case in enumerate(vectors):
            if entry==rate.TOP:
                original=rate.run(main,wram,case,index);compiled=rate.run(main,wram,case,index,compiledBodies=bodies);first={k:v for k,v in original.items()if k!='executedSourceRegions'};second={k:v for k,v in compiled.items()if k!='executedSourceRegions'}
                if first!=second:raise ValueError('Connected original/rebuilt full CPU/RAM/reads/stores differ')
            else:
                original=timestamp.run(main,wram,case,index);compiled=timestamp.run(rebuilt,wram,case,index)
                if original!=compiled:raise ValueError('Direct timestamp original/rebuilt complete execution differs')
            if not original['modelPassed']or not compiled['modelPassed']:raise ValueError('Independent raw rate/alias/timestamp/frame model failed')
            records.append(dict(case=case,original=original,compiled=compiled,compiledSourceBodySha256={hex(k):hashlib.sha256(v).hexdigest()for k,v in bodies.items()}));visited.update(original['visited'])
            helper_counts.update(h['entry']for h in original['helpers']);helper_counts.update(h['entry']for h in compiled['helpers'])
        own_code=60 if entry==rate.TOP else 116
        if not set(range(entry,entry+own_code,4))<=visited:raise ValueError('Complete owned ARM instruction coverage missing')
        trace=WORK/row['address'][2:]/'native-records.json.gz';raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace.write_bytes(gzip.compress(raw,mtime=0));abi=dict(physicalArgumentWords=1 if entry==rate.TOP else 0,rawWordAddressInput=entry==rate.TOP,rawWordReturn=0 if entry==rate.TOP else'0x04808140',compatibleExistingWordCalleeDeclarations=True,localSdkUnsignedLongBytes=4,completeOriginalWlManObjectExtentClaimed=False,boundedViewMaxOffset='0x3d3',originalInitializerClearBytes=0x694)
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols={name:binding['address']for name,binding in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceAbiContract=abi,
            oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),scopedNestedReturns=sum(helper_counts.values()),nestedReturnsByQualifiedEntry=dict(helper_counts),actualFillReturns=2*len(records),constructorActualReturns=0,allOwnInstructionsVisited=True,fullRawCpuFlagsStackRamReadsAndOrderedWritesCompared=True,independentRawFieldAliasAndArithmeticModel=True,providerReplacements=[],wholeSceneOrPhysicalHardwareContextProven=False,trace=dict(path=trace.relative_to(ROOT).as_posix(),compressedSha256=sha256(trace),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)))
        matches.append(row);total_helpers+=sum(helper_counts.values());total_returns+=2*len(records)
    wrong=[]
    for entry,old,new in [(rate.TOP,'pRateSet->Support | pRateSet->Basic','pRateSet->Support & pRateSet->Basic'),(timestamp.TOP,'97 + 97 * 0x100','98 + 98 * 0x100')]:
        seed=next(r for r in profile['units']if int(r['address'],0)==entry);positive=next(r for r in matches if int(r['address'],0)==entry);text=(ROOT/seed['source']).read_text()
        if text.count(old)!=1:raise ValueError('Independent wrong-C mutation site absent')
        bad,build=diagnostic.build(seed,text.replace(old,new),WORK/('wrong-'+seed['address'][2:]),positive['realLink']['bindings']);bad_bodies=dict(bodies);bad_bodies[entry]=bad;returned=rejected=0;vectors=rate.cases()if entry==rate.TOP else timestamp.cases()
        for index,case in enumerate(vectors):
            if entry==rate.TOP:execution=rate.run(main,wram,case,index,compiledBodies=bad_bodies)
            else:
                altered=bytearray(main)
                for address,own in bad_bodies.items():altered[address-timestamp.MAIN:address-timestamp.MAIN+len(own)]=own
                execution=timestamp.run(bytes(altered),wram,case,index)
            returned+=int(execution['actualOwnReturn']);rejected+=int(not execution['modelPassed'])
        if not rejected:raise ValueError('Wrong source escaped independent native field/arithmetic checks')
        wrong.append(dict(address=hex(entry),actualOwnReturns=returned,independentModelRejections=rejected,build=build))
    try:original_compiler.compile_unit(profile['units'][0],ROOT/profile['units'][0]['source'],WORK/'original-unchanged-word-refusal',strict=True)
    except ValueError as error:refusal=dict(errorType=type(error).__name__,error=str(error))
    else:raise ValueError('Default unknown-runtime-word refusal disappeared')
    symbols={name:binding['address']for row in matches for name,binding in row['realLink']['bindings'].items()}
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=profile['units'][0]['romSha256'],matches=matches,nativeSymbols=symbols,totalActualOwnReturns=total_returns,totalScopedNestedReturns=total_helpers,matchedInitializedBytes=sum(row['bytes']for row in matches),matchedCodeBytes=176,generatedLiteralBytes=16,newOrdinaryFunctionCount=len(matches),initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,wrongC=wrong,originalDefaultRefusal=refusal,existingGetter76SourceClosure=dict(source=getter[0]['source'],sourceSha256=getter[0]['sourceSha256'],sourceOnlyBuild=getter[1],compiledBytes=len(getter[2]),additionalSourceCredit=0),sdkReference=json.loads((ROOT/profile['reference']).read_text()),generatorSources=json.loads((SOURCE/'generator-pins.json').read_text())['files'],sourceInputsNoWorkCaches=True)
    report['abiLayoutProof']=layout
    report['callerSpecificLinker']=dict(path='link_arm7_sdk140_wl_rate64_20261101.py',sha256=sha256(ROOT/'link_arm7_sdk140_wl_rate64_20261101.py'),exactCallerSourceHeaderCompilerAndFullIdentityRequired=True,wordAddress='0x0380fff4',wordBytes=4,defaultAndEarlierPoliciesUnchanged=True,sourceDataOrDenominatorCredit=0)
    report['pinnedGeneratorAndRuntimeDependencies']=report['generatorSources']
    report['generatorSources']=report['generatorSources']+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))]
    report['originalDataAssemblyOrExtentCredit']=0
    report['constructorActualReturnCredit']=0
    report['totalActualFillReturns']=sum(row['oracle']['actualFillReturns']for row in matches)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),ownReturns=total_returns,nestedReturns=total_helpers,bytes=192)),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=240);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(process.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(process.stderr[-8000:])
    print(process.stdout.strip(),flush=True)
if __name__=='__main__':main()
