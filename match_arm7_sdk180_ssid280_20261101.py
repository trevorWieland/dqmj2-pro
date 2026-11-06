import argparse
import gzip
import hashlib
import json
import os
import struct
import subprocess
import sys
from pathlib import Path
import match_runtime
import arm7_sdk157_ssid_native_20261101 as ssid
import arm7_sdk159_byte_helpers_native_20261101 as byte
import compile_arm7_sdk180_ssid280_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import match_arm7_main_spi276_20261101 as strict
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk180-ssid280-include-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk180-ssid280-include-final'
REPORT=ROOT/'evidence/matches/arm7-sdk180-ssid280-20261101.json'
def layout(seed):
    work=WORK/'layout';work.mkdir(parents=True,exist_ok=True);source=work/'layout.c';obj=work/'layout.o'
    fields=['Work.SSIDLength','Work.SSID','Work.SSIDMask','MLME.State']
    expressions=['sizeof(u32)','sizeof(s32)','sizeof(void*)','sizeof(WL_MAN)']+['(u32)&((WL_MAN*)0)->'+f for f in fields]
    source.write_text('#include "wl_complete_types.h"\nconst u32 sdk161_layout[] = {'+','.join(expressions)+'};\n',encoding='utf-8')
    command=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk161_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if not elf.little_endian or elf.elfclass!=32:raise ValueError('SSID compiler physical ABI differs')
    values=list(struct.unpack('<8I',raw))
    if values!=[4,4,4,0x694,0x362,0x364,0x384,0x404]:raise ValueError('SSID complete declaration layout differs')
    return dict(values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualCompilerArgv=command,actualCwd=str(ROOT),sourceDataCredit=0,originalAllocatedObjectExtentOrOwnershipUnproved=True)
def trace(path,records):
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(gzip.compress(raw,mtime=0));return dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)
def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen SSID source/header/native/tool closure differs')
    profile=json.loads((SOURCE/'profile.json').read_text());proof=layout(profile['units'][0]);units=[compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:])for seed in profile['units']];bodies={int(row['address'],0):body for row,link,body in units}
    main=(ROOT/profile['units'][0]['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();matches=[];total_own=total_nested=total_fill=0
    for row,link,body in units:
        entry=int(row['address'],0);code=204 if entry==ssid.TOP else len(body);records=[];visited=set();nested=fill=0
        if body!=main[entry-ssid.MAIN:entry-ssid.MAIN+len(body)]:raise ValueError('Complete freshly linked SSID/byte source differs')
        vectors=ssid.cases()if entry==ssid.TOP else byte.cases()
        for index,case in enumerate(vectors):
            if entry==ssid.TOP:
                original=ssid.run(main,wram,case,index);compiled=ssid.run(main,wram,case,index,bodies=bodies);nested+=original['actualHelperReturns']+compiled['actualHelperReturns'];fill+=2
            else:original=byte.run(main,wram,entry,case,index);compiled=byte.run(main,wram,entry,case,index,body=body)
            if original!=compiled or not original['modelPassed']:raise ValueError('SSID/byte fresh native/source/model differs')
            records.append(dict(original=original,compiled=compiled));visited.update(original['visited'])
        if not set(range(entry,entry+code,4))<=visited:raise ValueError('SSID/byte complete own code coverage absent')
        oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),scopedNestedReturns=nested,actualFillReturns=fill,constructorActualReturns=0,allOwnInstructionsVisited=True,allRawCpuFlagsStackRamReadsAndOrderedWritesCompared=True,independentMaskOrAlignedHalfwordModel=True,providerReplacements=[],physicalSceneConcurrencyAndBusSideEffectsUnproved=True,trace=trace(WORK/row['address'][2:]/'native-records.json.gz',records))
        abi=dict(physicalArgumentWords=2 if entry!=byte.READ else 1,declaredReturn='u32'if entry==ssid.TOP else'u8'if entry==byte.READ else'void',typedArgumentDomain=['zero-extended u16 length','readable aligned-halfword-backed bytes']if entry==ssid.TOP else['readable aligned-halfword-backed address']if entry==byte.READ else['writable aligned-halfword-backed address','zero-extended u8 data'],rawNonstandardUpperArgumentBitsNotQualified=True,allTargetPointersAndSdkLongBytes=4,sourceLinkedByteReader=entry==ssid.TOP,maximumPredicateLoopBytes=32 if entry==ssid.TOP else 0)
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:binding['address']for name,binding in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=abi,oracle=oracle)
        matches.append(row);total_own+=2*len(records);total_nested+=nested;total_fill+=fill
    wrong=[]
    for entry,old,new in[(ssid.TOP,'(ssid | mask) != (myss | mask)','(ssid & mask) != (myss & mask)'),(byte.READ,'>> 8','>> 7'),(byte.WRITE,'data << 8','data << 7')]:
        seed=next(r for r in profile['units']if int(r['address'],0)==entry);positive=next(r for r in matches if int(r['address'],0)==entry);text=(ROOT/seed['source']).read_text()
        if text.count(old)!=1:raise ValueError('SSID/byte wrong source mutation site differs')
        bad,build=diagnostic.build(seed,text.replace(old,new),WORK/('wrong-'+seed['address'][2:]),positive['realLink']['bindings']);altered=dict(bodies);altered[entry]=bad;returned=rejected=0
        for index,case in enumerate(ssid.cases()if entry==ssid.TOP else byte.cases()):
            execution=ssid.run(main,wram,case,index,bodies=altered)if entry==ssid.TOP else byte.run(main,wram,entry,case,index,body=bad);returned+=int(execution['actualOwnReturn']);rejected+=int(not execution['modelPassed'])
        if not rejected:raise ValueError('SSID/byte wrong source escaped independent model')
        wrong.append(dict(address=hex(entry),build=build,actualOwnReturns=returned,modelRejections=rejected))
    try:strict.compile_unit(profile['units'][0],ROOT/profile['units'][0]['source'],WORK/'original-default-word-refusal',strict=True)
    except ValueError as error:refusal=dict(errorType=type(error).__name__,error=str(error))
    else:raise ValueError('Original strict unknown-word refusal disappeared')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=profile['units'][0]['romSha256'],matches=matches,nativeSymbols={name:value for row in matches for name,value in row['nativeSymbols'].items()},matchedInitializedBytes=280,matchedCodeBytes=276,generatedLiteralBytes=4,newOrdinaryFunctionCount=3,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=total_own,totalScopedNestedReturns=total_nested,totalActualFillReturns=total_fill,constructorActualReturnCredit=0,wrongC=wrong,originalDefaultRefusal=refusal,abiLayoutProof=proof,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,excludedInexactSetterBytes=272,completeSharedHeadersAdditionalSourceCredit=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=280,ownReturns=total_own,nestedReturns=total_nested,wrong=[dict(address=r['address'],returns=r['actualOwnReturns'],rejects=r['modelRejections'])for r in wrong])),flush=True)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=480);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(process.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(process.stderr[-6000:])
    print(process.stdout.strip(),flush=True)
if __name__=='__main__':main()
