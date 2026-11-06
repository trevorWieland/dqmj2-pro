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
import arm7_sdk273_frame_constructors_native_20261101 as native
import compile_arm7_sdk274_frame_builders_20261101 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk274-frame-builders1304-final'
WORK=ROOT/'work/arm7-bulk-20261030/sdk274-frame-builders1304-final'
REPORT=ROOT/'evidence/matches/arm7-sdk274-frame-builders1304-20261101.json'

def layout(seed):
    directory=WORK/'layout';directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';expressions=['sizeof(WL_MAN)','sizeof(WlMaDataReq)','(u32)&((WlMaDataReq*)0)->frame','sizeof(AUTH_FRAME)','(u32)&((AUTH_FRAME*)0)->FirmHeader.Length','(u32)&((AUTH_FRAME*)0)->MacHeader.Tx.MPDU','(u32)&((AUTH_FRAME*)0)->Dot11Header.FrameCtrl','(u32)&((AUTH_FRAME*)0)->Body','(u32)&((AUTH_FRAME*)0)->Body.ChallengeText.ID','(u32)&((AUTH_FRAME*)0)->Body.ChallengeText.Length','(u32)&((WL_MAN*)0)->Work.ListenInterval','(u32)&((WL_MAN*)0)->HeapMan.TxPri[1].Count','(u32)&((WL_MAN*)0)->CamMan.ConnectSta','sizeof(ASSREQ_FRAME)','sizeof(REASSREQ_FRAME)','sizeof(ASSRES_FRAME)','(u32)&((ASSREQ_FRAME*)0)->Body','(u32)&((ASSREQ_FRAME*)0)->Body.Buf','(u32)&((REASSREQ_FRAME*)0)->Body.CurrAPMacAdrs','(u32)&((REASSREQ_FRAME*)0)->Body.Buf','(u32)&((ASSRES_FRAME*)0)->Body','(u32)&((ASSRES_FRAME*)0)->Body.Buf','sizeof(WlCmdHeader)','sizeof(HEAPBUF_HEADER)','sizeof(CHALLENGE_ELEMENT)','sizeof(PRBREQ_FRAME)','sizeof(DISASS_FRAME)','sizeof(DEAUTH_FRAME)','sizeof(u32)','sizeof(void*)','sizeof(u16)']
    source.write_text('#include "ordinary_wireless.c"\nconst u32 sdk274_layout[]={'+','.join(expressions)+'};\n',encoding='utf-8');argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-i',str((ROOT/seed['source']).parent),'-c',str(source),'-o',str(obj)];result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:raise ValueError(result.stdout+result.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk274_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
    values=list(struct.unpack('<'+str(len(expressions))+'I',raw));expected=[0x694,64,16,306,6,18,20,44,50,51,948,424,1336,86,92,54,44,48,48,54,44,50,4,12,255,82,46,46,4,4,2]
    if values!=expected:raise ValueError('Complete frame/context/physical word type layouts differ')
    return dict(expressions=expressions,values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=argv,actualCwd=str(ROOT),sourceDataCredit=0,variableLengthPacketViewsAreNotProvenAndroidPortable=True)

def flattened(seed):
    source=ROOT/seed['source'];return re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:(source.parent/m[1]).read_text(),source.read_text())

def fragment(text,name):
    found=list(re.finditer(r'\b[A-Za-z_]\w*\s+'+re.escape(name)+r'\s*\([^;{}]*\)\s*\{',text))
    if len(found)!=1:raise ValueError('Unique ordinary frame builder definition missing')
    start=found[0].start();end=text.index('{',start)+1;depth=1
    while depth:
        if text[end]=='{':depth+=1
        elif text[end]=='}':depth-=1
        end+=1
    return start,end

def worker():
    pins=json.loads((SOURCE/'generator-pins.json').read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Complete frame/source/model/tool closure changed')
    seeds=json.loads((SOURCE/'profile.json').read_text())['units'];proof=layout(seeds[0]);main=(ROOT/seeds[0]['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();matches=[];wrong=[];own=helper=setup=prefix=0
    mutations={'MakeDisAssFrame':[('0x0A *','0x0B *')],'MakeAssReqFrame':[('0x00 * 0x0010','0x01 * 0x0010')],'MakeReAssReqFrame':[('0x02 *','0x03 *')],'MakeReAssResFrame':[('aid | 0xC000','aid | 0x8000')],'MakeProbeReqFrame':[('0x04 *','0x05 *')],'MakeAuthFrame':[('txtLen += 2','txtLen += 1'),('!IsEnableManagement()','IsEnableManagement()')],'MakeDeAuthFrame':[('0x0C *','0x0B *'),('!IsEnableManagement()','IsEnableManagement()')]}
    for seed in seeds:
        row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['name']/'positive');top=int(seed['address'],0);size=seed['bytes'];records=[];visited=set();nested=prerequisites=fills=0;vectors=[(i,c)for i,c in enumerate(native.cases())if c['entry']==top]
        if body!=main[top-native.MAIN:top-native.MAIN+size]:raise ValueError('Fresh complete frame function differs')
        for index,case in vectors:
            original=native.run(main,wram,case,index);compiled=native.run(main,wram,case,index,body=body)
            if original!=compiled or not original['actualOwnReturn']or not original['modelPassed']:raise ValueError('Original/fresh-C frame return, raw CPU/RAM, fields, native producers or helper effects differ')
            records.append(dict(original=original,compiled=compiled));visited.update(a for a in original['visited']if top<=a<top+size-8);nested+=2*len(original['actualNativeHelperReturns']);prerequisites+=2*len(original['actualSetupReturns']);fills+=2*len(original['actualPrefixFillReturns'])
        if visited!=set(range(top,top+size-8,4)):raise ValueError('Complete frame own instruction coverage differs:'+seed['name']+' '+str(sorted(set(range(top,top+size-8,4))-visited)))
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=WORK/seed['name']/'positive/native-records.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));trace=dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0);oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),actualOriginalHelperReturns=nested,actualNativeSetupEntryReturns=prerequisites,actualPrefixFillReturns=fills,constructorPrefixActualReturns=0,allOwnInstructionsVisited=True,ownInstructionCount=(size-8)//4,allRawCpuFlagsStackRamAndOrderedWritesCompared=True,independentAllocationArgumentAndCapacityModel=True,independentOwnedStoresAndPayloadFields=True,actualHeapQueueModeCamAndTxSetup=True,aidExhaustionUsesFifteenActualProducers=True if top==0x027f19fc else None,sourcePacketTypeAndroidPortabilityProven=False,providerReplacements=[],sourceDataAndSceneCredit=0,trace=trace)
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceAbiContract=seed['nativeInterfaceContract'],oracle=oracle);matches.append(row);own+=2*len(records);helper+=nested;setup+=prerequisites;prefix+=fills;text=flattened(seed);start,end=fragment(text,seed['name'])
        for number,(old,new)in enumerate(mutations[seed['name']]):
            part=text[start:end]
            if part.count(old)!=1:raise ValueError('Target-only wrong frame source site changed:'+old)
            altered,build=diagnostic.build(seed,text[:start]+part.replace(old,new)+text[end:],WORK/seed['name']/('wrong-'+str(number)),link['bindings']);returned=rejected=0
            for index,case in vectors:
                result=native.run(main,wram,case,index,body=altered);returned+=int(result['actualOwnReturn']);rejected+=int(not result['modelPassed'])
            if not rejected:raise ValueError('Returning wrong frame C survived independent own-field/allocation model')
            wrong.append(dict(name=seed['name'],mutation=[old,new],build=build,actualOwnReturns=returned,modelRejections=rejected))
    symbols={}
    for row in matches:
        for name,value in row['nativeSymbols'].items():
            if name in symbols and symbols[name]!=value:raise ValueError('One qualified frame symbol has conflicting native addresses')
            symbols[name]=value
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256=seeds[0]['romSha256'],matches=matches,nativeSymbols=symbols,matchedInitializedBytes=1304,matchedCodeBytes=1248,generatedLiteralBytes=56,newOrdinaryFunctionCount=7,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=own,totalActualHelperReturns=helper,totalActualSetupEntryReturns=setup,totalActualPrefixFillReturns=prefix,constructorPrefixActualReturnCredit=0,calleeSourceCredit=0,wrongC=wrong,abiLayoutProof=proof,pinnedGeneratorAndRuntimeDependencies=pins,generatorSources=pins+[dict(path=(SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'generator-pins.json'))],sourceInputsNoWorkCaches=True,originalDataAssemblyOrExtentCredit=0,additionalCDefinitionsInTypedUnitHaveNoSourceCredit=True,sourceSpecificPacketTypeAndroidPortabilityProven=False,actualFifteenAidProducerSequenceRatherThanSuppliedCalleeResult=True)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=1304,ownReturns=own,helperReturns=helper,setupReturns=setup,prefixFillReturns=prefix,wrong=[dict(name=r['name'],returns=r['actualOwnReturns'],rejects=r['modelRejections'])for r in wrong])),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if args.worker:worker();return
    result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],cwd=Path.cwd(),capture_output=True,text=True,timeout=1800);WORK.mkdir(parents=True,exist_ok=True);(WORK/'stdout.txt').write_text(result.stdout,encoding='utf-8');(WORK/'stderr.txt').write_text(result.stderr,encoding='utf-8')
    if result.returncode:raise ValueError(result.stderr[-7000:])
    print(result.stdout.strip(),flush=True)

if __name__=='__main__':main()
