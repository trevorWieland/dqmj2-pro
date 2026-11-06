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
import arm7_sdk176_start_explicit_model_20261101 as native
import arm7_sdk183_start_cases_20261101 as vectors
import prove_arm7_sdk179_unsigned_quotient_abi_20261101 as helper
import compile_arm7_sdk184_start952_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import match_arm7_main_spi276_20261101 as strict
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk184-start952-explicit-include-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk184-start952-explicit-include-final'
REPORT=ROOT/'evidence/matches/arm7-sdk184-start952-20261101.json'
def layout(seed):
    work=WORK/'layout';work.mkdir(parents=True,exist_ok=True);source=work/'layout.c';obj=work/'layout.o'
    fields=['Work.CapaInfo','Work.bSynchro','Work.Mode','Work.PowerMgtMode','Work.BeaconPeriod','Work.BSSID','DmaChannel','DmaMaxCount','HeapMan.TmpBuf','HeapMan.man_rsv[3]']
    expressions=['sizeof(u32)','sizeof(u64)','sizeof(void*)','sizeof(WL_MAN)','sizeof(HEAPBUF_MAN)']+['(u32)&((WL_MAN*)0)->'+f for f in fields]
    source.write_text('#include "wl_complete_types.h"\nconst u32 sdk184_layout[] = {'+','.join(expressions)+'};\nconst WL_MAN sdk184_short_preamble = {.Config.PreambleType=1};\n',encoding='utf-8')
    argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(source),'-o',str(obj)];run=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if run.returncode:raise ValueError(run.stdout+run.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbols={s.name:s for s in elf.get_section_by_name('.symtab').iter_symbols()}
        def data(name):
            sym=symbols[name];return elf.get_section(sym['st_shndx']).data()[sym['st_value']:sym['st_value']+sym['st_size']]
        raw=data('sdk184_layout');bitfield=data('sdk184_short_preamble')
    values=list(struct.unpack('<15I',raw));bits=[(i,v)for i,v in enumerate(bitfield)if v]
    if values!=[4,8,4,0x694,12,0x3c0,0x356,0x350,0x352,0x3b2,0x3a8,0x30c,0x310,392,560]or bits!=[(0x33a,4)]:raise ValueError('Complete startup SDK/bitfield/list ABI layout differs')
    return dict(values=values,preambleBitfieldBytes=bits,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualCompilerArgv=argv,actualCwd=str(ROOT),sourceDataCredit=0,allocatedObjectTotalExtentUnproved=True)
def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen startup C/header/native/proof/tool input changed')
    helper_proof=helper.measure();profile=json.loads((SOURCE/'profile.json').read_text());seed=profile['units'][0];abi=layout(seed)
    if sha256(helper.REPORT)!=seed['nativeHelperContracts'][0]['sha256']:raise ValueError('Fresh explicit u64 helper ABI proof differs')
    row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'positive');main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/seed['binary']).read_bytes()
    if body!=wram[native.TOP-native.WRAM:native.TOP-native.WRAM+native.SIZE]:raise ValueError('Whole freshly linked startup C differs')
    records=[];visited=set();nested=0
    for index,case in enumerate(vectors.cases()):
        original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
        if not original['actualOwnReturn']or not compiled['actualOwnReturn']:raise ValueError('Startup supported fixture did not actually return:'+str(index))
        if original!=compiled or not original['modelPassed']:raise ValueError('Startup raw state/own MMIO/field/direct-ABI independent model failed:'+str(index)+str(original['modelChecks']))
        records.append(dict(original=original,compiled=compiled));visited.update(pc for pc in original['visited']if native.TOP<=pc<native.TOP+native.CODE);nested+=len(original['directNativeReturns'])+len(compiled['directNativeReturns'])
    if visited!=set(range(native.TOP,native.TOP+native.CODE,4)):raise ValueError('Full startup own ARM code coverage missing')
    trace=WORK/'native-records.json.gz';raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace.write_bytes(gzip.compress(raw,mtime=0))
    source=(ROOT/seed['source']).read_text();wrong=[]
    for number,(old,new)in enumerate([('pWork->CapaInfo = (0x01 << 0)','pWork->CapaInfo = (0x01 << 1)'),('WlOperation & 0x00000008','WlOperation & 0x00000004'),('lltsf++;','lltsf--;')]):
        if source.count(old)!=1:raise ValueError('Startup independently wrong C site absent')
        bad,build=diagnostic.build(seed,source.replace(old,new),WORK/('wrong'+str(number)),link['bindings']);returned=rejected=0
        for index,case in enumerate(vectors.cases()):
            result=native.run(main,wram,case,index,body=bad)
            if not result['actualOwnReturn']:raise ValueError('Wrong C fixture unexpectedly failed instead of returning')
            returned+=1;rejected+=int(not result['modelPassed'])
        if not rejected:raise ValueError('Wrong startup C escaped the independent own-effect model')
        wrong.append(dict(build=build,actualOwnReturns=returned,independentModelRejections=rejected))
    try:strict.compile_unit(seed,ROOT/seed['source'],WORK/'original-default-word-refusal',strict=True)
    except ValueError as error:refusal=dict(errorType=type(error).__name__,error=str(error))
    else:raise ValueError('Default unknown runtime-word refusal disappeared')
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=dict(physicalArgumentWords=0,declaredReturn='void',descriptorPointerBytes=4,explicitUnsignedQuotientCallee='native_host_arm7_wram_03806bf0',u64ArgumentsAndReturnMeasured=True,zeroDivisionExpressionAbsent=True,zeroPeriodCDefinedByMeasuredExternalFunction=True,originalCalleeSourceCredit=0,globalModeProducerValidityUnproved=True),
        oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),scopedDirectNativeCalleeReturns=nested,actualFillReturns=2*len(records),constructorActualReturns=0,allOwnInstructionsVisited=True,ownCodeBytes=876,generatedLiteralBytes=76,independentOwnMmioFieldAndDirectCallAbiModel=True,fullRawCpuFlagsStackRamReadsAndWritesCompared=True,providerReplacements=[],realEffectfulNativeInitializersAndCleanupRetained=True,syntheticEmptyQueuePrerequisite=True,physicalMacDmaPhyConcurrencyAndSceneContextUnproved=True,rawModeEdgeCases=sum(c.get('rawModeProducerValidityUnproved',False)for c in vectors.cases()),trace=dict(path=trace.relative_to(ROOT).as_posix(),compressedSha256=sha256(trace),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',romSha256=seed['romSha256'],matches=[row],nativeSymbols=row['nativeSymbols'],matchedInitializedBytes=952,matchedCodeBytes=876,generatedLiteralBytes=76,newOrdinaryFunctionCount=1,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=2*len(records),totalScopedDirectCalleeReturns=nested,totalActualFillReturns=2*len(records),constructorActualReturnCredit=0,abiLayoutProof=abi,explicitU64HelperProof=dict(path=helper.REPORT.relative_to(ROOT).as_posix(),sha256=sha256(helper.REPORT),actualOwnReturns=helper_proof['actualOwnReturns'],sourceCredit=0),wrongC=wrong,originalDefaultRefusal=refusal,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],originalDataAssemblyCalleeOrExtentCredit=0,sourceInputsNoWorkCaches=True,sharedHeaderAdditionalCredit=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=952,ownReturns=2*len(records),directCalleeReturns=nested,wrong=[dict(returns=r['actualOwnReturns'],rejected=r['independentModelRejections'])for r in wrong])),flush=True)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    run=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=480);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(run.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(run.stderr,encoding='utf-8')
    if run.returncode:raise ValueError(run.stderr[-7000:])
    print(run.stdout.strip(),flush=True)
if __name__=='__main__':main()
