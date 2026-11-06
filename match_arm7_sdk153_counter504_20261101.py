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
import arm7_sdk150_counter_native_20261101 as native
import compile_arm7_sdk153_counter504_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import match_arm7_main_spi276_20261101 as strict
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk153-counter504-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk153-counter504-final'
REPORT=ROOT/'evidence/matches/arm7-sdk153-counter504-20261101.json'
FIELDS=['rx.plcpErr','rx.lengthErr','rx.rateErr','rx.pathErr','rx.bufOvfErr','rx.fcsOk','rx.fcsErr','rx.fcErr','rx.rts','rx.wep','rx.icvErr','rx.duplicateErr','rx.mpDuplicateErr','tx.ackErr']+['multiPoll.keyResponseErr['+str(i)+']'for i in range(15)]

def layout(seed):
    work=WORK/'layout';work.mkdir(parents=True,exist_ok=True);source=work/'layout.c';obj=work/'layout.o'
    expressions=['sizeof(u32)','sizeof(s32)','sizeof(void*)','sizeof(WL_MAN)','sizeof(WlCounter)','(u32)&((WL_MAN*)0)->Counter']+['(u32)&((WL_MAN*)0)->Counter.'+name for name in FIELDS]
    source.write_text('#include "wl_complete_types.h"\nconst u32 sdk153_layout[] = {'+','.join(expressions)+'};\n',encoding='utf-8')
    command=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk153_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if not elf.little_endian or elf.elfclass!=32:raise ValueError('Counter compiler object ABI differs')
    values=list(struct.unpack('<'+'I'*(len(raw)//4),raw))
    if values!=[4,4,4,0x694,0xb4,0x53c]+[r[2]for r in native.UPDATES]:raise ValueError('Complete SDK view and29 independent native field offsets differ')
    return dict(source=source.relative_to(ROOT).as_posix(),object=obj.relative_to(ROOT).as_posix(),values=values,fieldOffsets=dict(zip(FIELDS,values[6:])),actualCompilerArgv=command,actualCwd=str(ROOT),sourceSha256=sha256(source),objectSha256=sha256(obj),viewSizeEqualsMeasuredPrefixClearBytes=True,allocatedObjectTotalExtentOrOwnershipUnproved=True,sourceDataCredit=0)

def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for item in pins:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Frozen counter source/native/tool closure changed')
    profile=json.loads((SOURCE/'profile.json').read_text());seed=profile['units'][0]
    for pin in [dict(path=seed['source'],sha256=seed['sourceSha256']),*seed['sourceDependencies']]:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Counter source/header closure changed')
    proof=layout(seed);row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'positive')
    main=(ROOT/seed['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if sha256(ROOT/seed['binary'])!=seed['inputModuleSha256']or body!=main[native.TOP-native.MAIN:native.TOP-native.MAIN+native.SIZE]:raise ValueError('Counter full native module or source-only linked bytes differ')
    records=[]
    for index,case in enumerate(native.cases()):
        original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
        if original!=compiled or not original['modelPassed']:raise ValueError('Counter original/source complete CPU/RAM/ordered memory/model differ')
        records.append(dict(original=original,compiled=compiled))
    trace=WORK/'native-records.json.gz';raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace.write_bytes(gzip.compress(raw,mtime=0));wrong=[]
    source=(ROOT/seed['source']).read_text()
    for index,(old,new)in enumerate([('pCounter->rx.plcpErr +=','pCounter->rx.plcpErr ^='),('pCounter->multiPoll.keyResponseErr[14] +=','pCounter->multiPoll.keyResponseErr[14] -=')]):
        if source.count(old)!=1:raise ValueError('Counter wrong-C site absent')
        altered,build=diagnostic.build(seed,source.replace(old,new),WORK/('wrong'+str(index)),link['bindings'])
        returned=rejected=0
        for number,case in enumerate(native.cases()):
            execution=native.run(main,wram,case,number,body=altered);returned+=int(execution['actualOwnReturn']);rejected+=int(not execution['modelPassed'])
        if not rejected:raise ValueError('Counter wrong source escaped field/wrap model')
        wrong.append(dict(actualOwnReturns=returned,independentModelRejections=rejected,build=build))
    try:strict.compile_unit(seed,ROOT/seed['source'],WORK/'original-default-refusal',strict=True)
    except ValueError as error:refusal=dict(errorType=type(error).__name__,error=str(error))
    else:raise ValueError('Frozen strict unknown-runtime-word guard disappeared')
    try:native.run(main,wram,native.cases()[0],0,body=body,budget=1)
    except ValueError as error:bounded=dict(error=str(error),actualOwnReturnCredit=0)
    else:raise ValueError('Counter exhaustion incorrectly returned')
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:binding['address']for name,binding in link['bindings'].items()},nativeSymbolEntries=link['bindings'],
        sourceAbiContract=dict(physicalArgumentWords=0,declaredReturn='void',incidentalRawR0='updated Counter.multiPoll.keyResponseErr[14]',sdkLongAndPointerBytes=4,externalPointerWordDeclaredUnsignedIntCompatibleWithExistingViews=True,allNativeRegistersCompared=True,androidLong64OrPhysicalHardwareNotQualified=True),
        oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),actualFillReturns=2*len(records),constructorActualReturns=0,scopedNestedTargetReturns=0,completeOwnCodeBytes=496,generatedLiteralBytes=8,allOwnInstructionsVisited=True,independent29FieldByteAndWrapModel=True,allRawCpuFlagsStackRamReadsAndOrderedWritesCompared=True,providerReplacements=[],physicalReadSideEffectsConcurrencyAndGameContextUnproved=True,trace=dict(path=trace.relative_to(ROOT).as_posix(),compressedSha256=sha256(trace),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=seed['romSha256'],matches=[row],nativeSymbols=row['nativeSymbols'],matchedInitializedBytes=504,matchedCodeBytes=496,generatedLiteralBytes=8,newOrdinaryFunctionCount=1,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=2*len(records),totalActualFillReturns=2*len(records),constructorActualReturnCredit=0,totalScopedNestedReturns=0,abiLayoutProof=proof,wrongC=wrong,originalDefaultRefusal=refusal,boundedExhaustion=bounded,sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,sdkReference=dict(revision=profile['referenceRevision'],matchingSdkRevisionUnproved=True,completeDeclarationViewBytes=0x694,originalAllocatedObjectTotalExtentUnproved=True,provisionalParsingHeadersAbsentFromClosedCompilerInput=True))
    report['pinnedGeneratorAndRuntimeDependencies']=pins
    report['generatorSources']=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))]
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=504,actualOwnReturns=2*len(records),wrong=wrong),default=str)[:1500],flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=240)
    WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(process.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(process.stderr[-6000:])
    print(process.stdout.strip(),flush=True)
if __name__=='__main__':main()
