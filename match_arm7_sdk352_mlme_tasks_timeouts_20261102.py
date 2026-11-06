import argparse
import concurrent.futures
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import match_runtime
from elftools.elf.elffile import ELFFile
import compile_arm7_sdk350_mlme_tasks_timeouts_20261102 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import slice_arm7_sdk147_closed_v3_20261101 as slicer
import arm7_sdk351_mlme_family_native_20261102 as native
from project import ROOT,sha256,write_json

PROFILE=compiler.linker.PROFILE
WORK=ROOT/'work/arm7-bulk-20261030/sdk352-mlme-tasks-timeouts'
REPORT=ROOT/'evidence/matches/arm7-sdk352-mlme-tasks-timeouts860-20261102.json'
MUTATIONS={'MLME_ScanTask':('pMLME->State = (0x03 | 0x10) ;','pMLME->State = (0x04 | 0x10) ;'),'MLME_JoinTask':('pMLME->Work.Join.Result = 0 ;','pMLME->Work.Join.Result = 1 ;'),'MLME_ScanTimeOut':('pMLME->State = (0x01 | 0x10) ;','pMLME->State = (0x02 | 0x10) ;'),'MLME_JoinTimeOut':('pMLME->Work.Join.Result = 0x07 ;','pMLME->Work.Join.Result = 0x08 ;'),'MLME_MeasChanTimeOut':('(0x03 | 0x80) ;','(0x04 | 0x80) ;')}

def units():return json.loads(PROFILE.read_text())['units']

def layout(seed,directory):
    directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';fields=['sizeof(WL_MAN)','sizeof(u16)','sizeof(u32)','sizeof(void*)'];expected=[1684,2,4,4]
    fields+=['(u32)&((WL_MAN*)0)->MLME.State','(u32)&((WL_MAN*)0)->MLME.Work.Scan.ChannelCount','(u32)&((WL_MAN*)0)->MLME.Work.Scan.ElapseTime','(u32)&((WL_MAN*)0)->MLME.Work.Scan.TxPeriod','(u32)&((WL_MAN*)0)->MLME.pReq','(u32)&((WL_MAN*)0)->MLME.pCfm','(u32)&((WL_MAN*)0)->Config.Mode','(u32)&((WL_MAN*)0)->Work.STA','(u32)&((WL_MAN*)0)->Work.Mode','(u32)&((WL_MAN*)0)->Alarm','(u32)&((WlMlmeScanReq*)0)->scanType','(u32)&((WlMlmeScanReq*)0)->channelList','(u32)&((WlMlmeScanReq*)0)->maxChannelTime','(u32)&((WlMlmeJoinReq*)0)->timeOut','(u32)&((WlMlmeJoinCfm*)0)->resultCode','(u32)&((WlMlmeJoinCfm*)0)->statusCode'];expected+=[0x404,0x40a,0x40e,0x410,0x41c,0x420,0x32e,0x34c,0x350,0x634,0x38,0x3a,0x4a,0x10,4,6]
    source.write_text('#include "ordinary_wireless.c"\nconst u32 sdk352_layout[]={'+','.join(fields)+'};\n');argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-i',str((ROOT/seed['source']).parent),'-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(v for v in elf.get_section_by_name('.symtab').iter_symbols()if v.name=='sdk352_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
    values=list(struct.unpack('<'+str(len(fields))+'I',raw))
    if values!=expected:raise ValueError('Full measured context/parameter/key layout changed:'+str(values))
    return dict(expressions=fields,values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=argv,actualCwd=str(ROOT),sourceDataCredit=0)

def compile_worker(index):
    seed=units()[index];directory=WORK/seed['name'];abi=layout(seed,directory/'layout');row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],directory/'positive');row.update(abiLayoutProof=abi,realLink=link,nativeSymbols={k:v['address']for k,v in link['bindings'].items()},nativeSymbolEntries=link['bindings']);write_json(directory/'build.json',dict(row=row,bodyPath=(directory/'positive/real-link/caller.bin').relative_to(ROOT).as_posix(),bodySha256=hashlib.sha256(body).hexdigest()));print(seed['name']+' fresh source compile/real link passed',flush=True)


def packed(path,records):
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(gzip.compress(raw,mtime=0));return dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)

def proof_worker(index):
    seed=units()[index];directory=WORK/seed['name'];built=json.loads((directory/'build.json').read_text());row=built['row'];linked_bodies={}
    for selected in units():
        source_product=json.loads((WORK/selected['name']/'build.json').read_text());p=ROOT/source_product['bodyPath']
        if sha256(p)!=source_product['bodySha256']:raise ValueError('Fresh complete selected source body missing or changed')
        linked_bodies[int(selected['address'],0)]=p.read_bytes()
    top=int(seed['address'],0);body=(ROOT/built['bodyPath']).read_bytes();vectors=[(i,c)for i,c in enumerate(native.cases())if c['entry']==top]
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();records=[];visited=set();helpers=setup=independent=0
    for number,case in vectors:
        original=native.run(main,wram,case,number);compiled=native.run(main,wram,case,number,body=body,linked_bodies=linked_bodies);comparisons={key:original.get(key)==compiled.get(key)for key in('registers','cpsr','pc','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks','actualDeclaredHelperReturns')}
        if not original.get('actualOwnReturn')or not compiled.get('actualOwnReturn')or not original.get('modelPassed')or not compiled.get('modelPassed')or not all(comparisons.values()):raise ValueError(dict(name=seed['name'],case=case,original=original.get('modelChecks',original),compiled=compiled.get('modelChecks',compiled),comparisons=comparisons))
        independent+=sum(len(r['independentOriginalApiModel']['actualIndependentApiReturns'])if r.get('independentOriginalApiModel')else 0 for r in(original,compiled));helpers+=len(original['actualDeclaredHelperReturns'])+len(compiled['actualDeclaredHelperReturns']);setup+=len(original['actualSetupEntryReturns'])+len(compiled['actualSetupEntryReturns']);visited.update(original['visited']);records.append(dict(case=case,original=original,compiled=compiled,comparisons=comparisons))
    trace=packed(directory/'positive/native-records.json.gz',records);text=(ROOT/seed['source']).read_text();text=re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:((ROOT/seed['source']).parent/m[1]).read_text(),text);function=next(r for r in slicer.functions(text)if r['name']==seed['name']);fragment=text[function['start']:function['end']];old,new=MUTATIONS[seed['name']]
    if fragment.count(old)<1:raise ValueError('Target-only ordinary wrong-C mutation missing:'+old)
    wrong=text[:function['start']]+fragment.replace(old,new,1)+text[function['end']:];altered,wrong_build=diagnostic.build(dict(seed,address='0x2680000'),wrong,directory/'wrong-source',row['realLink']['bindings']);wrong_records=[];returned=rejected=0
    for number,case in vectors:
        result=native.run(main,wram,case,number,body=altered,virtual_address=0x02680000,linked_bodies=linked_bodies);returned+=int(result['actualOwnReturn']);rejected+=int(result.get('actualOwnReturn')and not result.get('modelPassed'));wrong_records.append(dict(case=case,result=result))
    if returned!=len(vectors)or not rejected:raise ValueError('Every wrong-source supported case must actually return, with independent model rejections')
    wrong_trace=packed(directory/'wrong-source/native-records.json.gz',wrong_records);oracle=dict(vectors=len(vectors),actualOriginalAndCompiledReturns=2*len(vectors),actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=setup,actualIndependentOriginalApiReturns=independent,sourceLinkedSelectedBodies=[dict(address=hex(a),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())for a,b in sorted(linked_bodies.items())],prefixBoundaryNormalReturnCredit=0,providerReplacements=[],allSupportedFieldAndStateModelsPassed=True,allRegistersCpsrStackNonstackRamAndOrderedWritesCompared=True,ownedInstructionAddresses=sorted(visited),ownedInstructionCoverageIsMeasuredNotAssumedComplete=True,trace=trace,freshOwnCompiledBodyInstalledBeforeEntryAndOriginalLowerApisHaveZeroAdditionalCredit=True,originalUnreconstructedTableAndHandlerCredit=0,radioSceneAsyncSchedulerAndAndroidUnproved=True);row.update(exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,oracle=oracle);result=dict(match=row,wrongC=dict(name=seed['name'],mutation=[old,new],build=wrong_build,actualOwnReturns=returned,modelRejections=rejected,trace=wrong_trace));write_json(directory/'result.json',result);print(json.dumps(dict(name=seed['name'],bytes=seed['bytes'],returns=2*len(vectors),wrongReturns=returned,wrongRejected=rejected)),flush=True)

def invoke(args):
    bootstrap='import runpy,sys;r=sys.argv.pop(1);p=sys.argv.pop(1);sys.path.insert(0,r);runpy.run_path(p,run_name="__main__")';argv=[sys.executable,'-I','-S','-c',bootstrap,str(ROOT),str(Path(__file__).resolve()),*args];p=subprocess.run(argv,cwd=ROOT.parent,capture_output=True,text=True,timeout=300)
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    print(p.stdout.strip(),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--compile-worker',type=int);parser.add_argument('--compile-all',action='store_true');parser.add_argument('--proof-worker',type=int);args=parser.parse_args()
    if args.compile_all:
        for index in range(len(units())):compile_worker(index)
        return
    if args.compile_worker is not None:compile_worker(args.compile_worker);return
    if args.proof_worker is not None:proof_worker(args.proof_worker);return
    pin_path=PROFILE.parent/'generator-pins.json';pins=json.loads(pin_path.read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Pinned source/runtime/tool closure changed:'+pin['path'])
    seeds=units();snapshot=seeds[0]['authoritativeExclusionSnapshot'];path=ROOT/snapshot['path']
    if sha256(path)!=snapshot['sha256']:raise ValueError('Authoritative normalized exclusion snapshot changed')
    accepted=json.loads(path.read_text())['functions'];identity=lambda r:(r['processor'],r.get('program',''),r['module'],r['mode'],int(r['address'],0)if isinstance(r['address'],str)else r['address'])
    if any(identity(s)==identity(r)for s in seeds for r in accepted):raise ValueError('Duplicate accepted identity cannot receive new source coverage')
    invoke(['--compile-all'])
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:list(pool.map(invoke,[['--proof-worker',str(i)]for i in range(len(seeds))]))
    results=[json.loads((WORK/s['name']/'result.json').read_text())for s in seeds];matches=[r['match']for r in results];symbols={}
    for row in matches:
        for name,value in row['nativeSymbols'].items():
            if name in symbols and symbols[name]!=value:raise ValueError('Shared named dependency has conflicting qualified addresses')
            symbols[name]=value
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',romSha256=seeds[0]['romSha256'],matches=matches,nativeSymbols=symbols,matchedInitializedBytes=860,newOrdinaryFunctionCount=5,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=sum(r['oracle']['actualOriginalAndCompiledReturns']for r in matches),totalActualDeclaredHelperReturns=sum(r['oracle']['actualDeclaredHelperReturns']for r in matches),totalActualSetupEntryReturns=sum(r['oracle']['actualSetupEntryReturns']for r in matches),totalActualIndependentOriginalApiReturns=sum(r['oracle']['actualIndependentOriginalApiReturns']for r in matches),wrongC=[r['wrongC']for r in results],originalTablesAndAdditionalDefinitionsSourceCredit=0,sourceInputsNoWorkCaches=True,sourceSpecificHardwareAndAndroidPortabilityProven=False,generatorSources=pins+[dict(path=pin_path.relative_to(ROOT).as_posix(),sha256=sha256(pin_path))],pinnedGeneratorAndRuntimeDependencies=pins);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=860,ownReturns=report['totalActualOwnReturns'])),flush=True)

if __name__=='__main__':main()
