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
import arm7_sdk202_rxctrl_native_20261101 as native
import compile_arm7_sdk204_rxctrl288_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import match_arm7_main_spi276_20261101 as strict
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk204-rxctrl288-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk204-rxctrl288-final'
REPORT=ROOT/'evidence/matches/arm7-sdk204-rxctrl288-20261101.json'

def layout(seed):
    directory=WORK/'layout';directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';fields=['RxCtrl','RxCtrl.wlCurr','RxCtrl.LastMpSeq','Work.Ofst.RxBuf.Size','Work.Mode','Config.Mode']
    expressions=['sizeof(u32)','sizeof(s32)','sizeof(void*)','sizeof(WL_MAN)','sizeof(RX_CTRL)']+['(u32)&((WL_MAN*)0)->'+field for field in fields]
    source.write_text('#include "../20261101_wl_counter504/wl_complete_types.h"\nconst u32 sdk204_layout[]={'+','.join(expressions)+'};\n',encoding='utf-8');command=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk204_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if not elf.little_endian or elf.elfclass!=32:raise ValueError('Receive compiler ABI differs')
    values=list(struct.unpack('<11I',raw))
    if values!=[4,4,4,0x694,80,0x4dc,0x4e0,0x4dc,0x3de,0x350,0x32e]:raise ValueError('Receive full SDK field/layout differs:'+str(values))
    return dict(values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=command,actualCwd=str(ROOT),sourceDataCredit=0)

def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Complete RX caller/model/source/tool input closure differs')
    seed=json.loads((SOURCE/'profile.json').read_text())['units'][0];proof=layout(seed);row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'positive');main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/seed['binary']).read_bytes();records=[];visited=set();producer_helpers=0
    if body!=wram[native.TOP-native.WRAM:native.TOP-native.WRAM+288]:raise ValueError('Complete freshly compiled RX source differs')
    for index,case in enumerate(native.cases()):
        original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
        if original!=compiled or not original['modelPassed']:raise ValueError('RX original/fresh-C independent field/port/producer proof differs')
        records.append(dict(original=original,compiled=compiled));visited.update(original['visited']);producer_helpers+=2*len(original['producer']['modeSetterHelpers'])
    expected=set(range(native.TOP,native.TOP+248,4));excluded={0x037fb22c}
    if expected-set(visited)!=excluded:raise ValueError('RX bounded-mode own coverage differs; no uninitialized-domain execution permitted')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/'positive/native-records.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));trace=dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0);own=2*len(records)
    oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=own,actualNestedFillReturns=own,actualPrefixFillReturns=own,actualModeSetterReturns=own,actualProducerNestedHelperReturns=producer_helpers,constructorActualReturns=0,allSupportedModeBranchesCovered=True,visitedOwnInstructions=61,totalOwnInstructions=62,excludedUndefinedDomainInstruction='0x37fb22c',uninitializedSourceModeOutside0To3Unsupported=True,originalModeSetterRetained=True,allRawCpuFlagsStackRamReadsAndOrderedWritesCompared=True,independentClearAndOrderedPortsModel=True,providerReplacements=[],trace=trace,physicalHardwareFrameOwnershipAndSceneReachabilityUnproved=True)
    abi=dict(physicalArgumentWords=0,declaredReturn='void',rawIncidentalR0='0x04805f70',sourceGlobalPrecondition='Work.Mode produced by original WSetMode with input0..3',unsupportedGlobalDomainHasNoCredit=True,originalClearCallWords=[0,'context+0x4dc',80],allTargetSdkLongAndPointerBytes=4)
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=abi,oracle=oracle)
    wrong=[];text=(ROOT/seed['source']).read_text()
    for index,(old,new,count)in enumerate([('sizeof(RX_CTRL)','sizeof(RX_CTRL)-4',1),('0x1F60','0x1F64',3)]):
        if text.count(old)!=count:raise ValueError('RX wrong source site/count differs:'+old+str(text.count(old)))
        altered,build=diagnostic.build(seed,text.replace(old,new),WORK/('wrong-'+str(index)),link['bindings']);returned=rejected=0
        for vector,case in enumerate(native.cases()):
            result=native.run(main,wram,case,vector,body=altered);returned+=int(result['actualOwnReturn']);rejected+=int(not result['modelPassed'])
        if not rejected:raise ValueError('RX wrong C escaped independent effects/ABI model')
        wrong.append(dict(mutation=[old,new],build=build,actualOwnReturns=returned,modelRejections=rejected))
    try:strict.compile_unit(seed,ROOT/seed['source'],WORK/'original-default-word-refusal',strict=True)
    except ValueError as error:refusal=dict(errorType=type(error).__name__,error=str(error))
    else:raise ValueError('Default RX unknown-word guard disappeared')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',romSha256=seed['romSha256'],matches=[row],nativeSymbols=row['nativeSymbols'],matchedInitializedBytes=288,matchedCodeBytes=248,generatedLiteralBytes=40,newOrdinaryFunctionCount=1,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=own,totalScopedNestedReturns=own,totalActualFillReturns=own,totalActualModeSetterReturns=own,totalActualProducerNestedHelperReturns=producer_helpers,constructorActualReturnCredit=0,wrongC=wrong,originalDefaultRefusal=refusal,abiLayoutProof=proof,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,completeSharedHeadersAdditionalSourceCredit=0)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=288,ownReturns=own,modeReturns=own,producerHelperReturns=producer_helpers,wrong=[dict(returns=r['actualOwnReturns'],rejects=r['modelRejections'])for r in wrong])),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=120);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(process.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(process.stderr[-7000:])
    print(process.stdout.strip(),flush=True)
if __name__=='__main__':main()
