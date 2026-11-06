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
import arm7_sdk188_settings_native_20261101 as native
import compile_arm7_sdk190_security328_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import match_arm7_main_spi276_20261101 as strict
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk190-security328-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk190-security328-final'
REPORT=ROOT/'evidence/matches/arm7-sdk190-security328-20261101.json'
SNAPSHOT=ROOT/'evidence/verification/accepted-cohort123-identities-v2-20261101.json'

def layout(seed):
    work=WORK/'layout';work.mkdir(parents=True,exist_ok=True);source=work/'layout.c';obj=work/'layout.o'
    fields=['TxCtrl.Beacon.pMacFrm','Config.WepMode','Work.STA','Work.CapaInfo','Work.FrameCtrl','Config.Mode','Config.Rate','Work.RateSet','Config']
    expressions=['sizeof(u32)','sizeof(s32)','sizeof(void*)','sizeof(WL_MAN)','sizeof(CAPA_INFO)','sizeof(BEACON_BODY)','(u32)&((BEACON_BODY*)0)->CapaInfo','(u32)&((TXFRM_MAC*)0)->Body']+['(u32)&((WL_MAN*)0)->'+f for f in fields]
    source.write_text('#include "beacon_types.h"\nconst u32 sdk190_layout[] = {'+','.join(expressions)+'};\nconst WL_MAN sdk190_preamble={.Config.PreambleType=1};\n',encoding='utf-8')
    command=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbols=elf.get_section_by_name('.symtab');symbol=next(s for s in symbols.iter_symbols()if s.name=='sdk190_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']];symbol=next(s for s in symbols.iter_symbols()if s.name=='sdk190_preamble');bits=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
        if not elf.little_endian or elf.elfclass!=32:raise ValueError('SDK190 compiler physical ABI differs')
    values=list(struct.unpack('<17I',raw));bitfield=[[i,b]for i,b in enumerate(bits)if b]
    if values!=[4,4,4,0x694,2,68,10,36,0x4ac,0x334,0x34c,0x3c0,0x3ce,0x32e,0x330,0x3a4,0x31c]or bitfield!=[[0x33a,4]]:raise ValueError('SDK190 complete declaration/beacon/bitfield offsets differ:'+str((values,bitfield)))
    return dict(values=values,preambleBitfieldBytes=bitfield,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualCompilerArgv=command,actualCwd=str(ROOT),sourceDataCredit=0,frameBackingAndOriginalAllocatedExtentUnproved=True)

def trace(path,records):
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(gzip.compress(raw,mtime=0));return dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)

def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen settings source/header/native/tool closure differs')
    profile=json.loads((SOURCE/'profile.json').read_text());snapshot=json.loads(SNAPSHOT.read_text());proof=layout(profile['units'][0]);units=[]
    for seed in profile['units']:
        if any(r['processor']=='arm7'and r.get('program','')==''and r['module']=='arm7-main'and r['mode']=='arm'and int(r['address'])==int(seed['address'],0)for r in snapshot['functions']):raise ValueError('Settings candidate already accepted in123')
        units.append(compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:]))
    bodies={int(row['address'],0):body for row,link,body in units};main=(ROOT/profile['units'][0]['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();matches=[];total_own=total_nested=total_fill=0
    for row,link,body in units:
        entry=int(row['address'],0);extent,code=native.FUNCTIONS[entry];records=[];visited=set();nested=0
        if body!=main[entry-native.MAIN:entry-native.MAIN+extent]:raise ValueError('Complete freshly compiled settings body differs')
        for index,case in enumerate(native.cases(entry)):
            original=native.run(main,wram,entry,case,index);compiled=native.run(main,wram,entry,case,index,bodies=bodies)
            if original!=compiled or not original['modelPassed']:raise ValueError('Settings independent native/source/field/port model differs')
            records.append(dict(original=original,compiled=compiled));visited.update(original['visited']);nested+=original['actualNativeHelperReturns']+compiled['actualNativeHelperReturns']
        if not set(range(entry,entry+code,4))<=visited:raise ValueError('Settings complete own code instruction coverage absent')
        oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),scopedNestedReturns=nested,actualFillReturns=2*len(records),constructorActualReturns=0,allOwnInstructionsVisited=True,allRawCpuFlagsStackRamReadsAndOrderedWritesCompared=True,independentFieldPortTimestampModel=True,providerReplacements=[],syntheticReadableBeaconBackingAndStaticRegisterPage=True,physicalFrameOwnershipHardwareConcurrencyAndSceneReachabilityUnproved=True,trace=trace(WORK/row['address'][2:]/'native-records.json.gz',records))
        abi=dict(physicalArgumentWords=1,typedArgumentDomain='zero-extended u16',declaredReturn='u16 status0or5',allTargetPointersAndSdkLongBytes=4,nonstandardUpperArgumentBitsNotQualified=True,rawNestedTimestampResultIgnored=True,declaredTimestampHelperReturn='unsigned int compatible with accepted128 u32 view')
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=abi,oracle=oracle);matches.append(row);total_own+=2*len(records);total_nested+=nested;total_fill+=2*len(records)
    wrong=[]
    for entry,old,new,count in[(native.WEP,'pWork->CapaInfo |= (0x01 << 4)','pWork->CapaInfo |= (0x01 << 3)',1),(native.PREAMBLE,'((0x0001 << 1) | (0x0001 << 2) )','((0x0001 << 0) | (0x0001 << 2) )',2),(native.PREAMBLE,'native_arm7_main_027e9bd8();\n    return 0;','native_arm7_main_027e9bd8();\n    return 1;',1)]:
        seed=next(r for r in profile['units']if int(r['address'],0)==entry);positive=next(r for r in matches if int(r['address'],0)==entry);text=(ROOT/seed['source']).read_text()
        if text.count(old)!=count:raise ValueError('Settings wrong-C source site differs')
        bad,build=diagnostic.build(seed,text.replace(old,new),WORK/('wrong-'+seed['address'][2:]+'-'+str(len(wrong))),positive['realLink']['bindings']);altered=dict(bodies);altered[entry]=bad;returned=rejected=0
        for index,case in enumerate(native.cases(entry)):
            result=native.run(main,wram,entry,case,index,bodies=altered);returned+=int(result['actualOwnReturn']);rejected+=int(not result['modelPassed'])
        if not rejected:raise ValueError('Settings wrong source escaped independent model')
        wrong.append(dict(address=hex(entry),mutation=[old,new],build=build,actualOwnReturns=returned,modelRejections=rejected))
    refusals=[]
    for seed in profile['units']:
        try:strict.compile_unit(seed,ROOT/seed['source'],WORK/('original-default-refusal-'+seed['address'][2:]),strict=True)
        except ValueError as error:refusals.append(dict(address=seed['address'],errorType=type(error).__name__,error=str(error)))
        else:raise ValueError('Default settings external-word refusal disappeared')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=profile['units'][0]['romSha256'],matches=matches,nativeSymbols={name:value for row in matches for name,value in row['nativeSymbols'].items()},matchedInitializedBytes=328,matchedCodeBytes=308,generatedLiteralBytes=20,newOrdinaryFunctionCount=2,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=total_own,totalScopedNestedReturns=total_nested,totalActualFillReturns=total_fill,constructorActualReturnCredit=0,wrongC=wrong,originalDefaultRefusals=refusals,abiLayoutProof=proof,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,completeSharedHeadersAdditionalSourceCredit=0,accepted123SnapshotSha256=sha256(SNAPSHOT),unacceptedDraftCampaign=dict(compilableFunctions=4,compilableNativeBytes=668,exactThisPacketBytes=328,inexactMode=[121,128],inexactDiversity=[197,212],additionalSourceCredit=0))
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=328,ownReturns=total_own,nestedReturns=total_nested,wrong=[dict(address=r['address'],returns=r['actualOwnReturns'],rejects=r['modelRejections'])for r in wrong])),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=480);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(process.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError(process.stderr[-7000:])
    print(process.stdout.strip(),flush=True)
if __name__=='__main__':main()
