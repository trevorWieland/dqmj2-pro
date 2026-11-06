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
import compile_arm7_sdk310_task_command_20261102 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import slice_arm7_sdk147_closed_v3_20261101 as slicer
import arm7_sdk307_task_queue_native_20261102 as tasks
import arm7_sdk308_command_dispatch_native_20261102 as commands
from project import ROOT,sha256,write_json

PROFILE=compiler.linker.PROFILE
WORK=ROOT/'work/arm7-bulk-20261030/sdk312-task-command-family'
REPORT=ROOT/'evidence/matches/arm7-sdk312-task-command-family1224-20261102.json'
MUTATIONS={'InitializeTask':('pTaskMan->NextPri = 0;','pTaskMan->NextPri = 1;'),'AddTask':('pTaskTbl[nTaskID].Flag = 0x0001 ;','pTaskTbl[nTaskID].Flag = 0x0002 ;'),'DeleteTask':('pTaskTbl[nOfstTaskID].Flag = 0x0000 ;','pTaskTbl[nOfstTaskID].Flag = 0x0001 ;'),'LowestIdleTask':('AddTask(3 , 12 );','AddTask(3 , 13 );'),'RequestCmdTask':('pCfm->resultCode = 0x06 ;','pCfm->resultCode = 0x07 ;')}

def units():return json.loads(PROFILE.read_text())['units']

def layout(seed,directory):
    directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';fields=['sizeof(WL_MAN)','sizeof(TASK_MAN)','sizeof(TASK_TBL)','sizeof(u32)','sizeof(u16)','sizeof(void*)','(u32)&((WL_MAN*)0)->TaskMan.EnQ','(u32)&((WL_MAN*)0)->TaskMan.DeQ','(u32)&((WL_MAN*)0)->TaskMan.NextPri','(u32)&((WL_MAN*)0)->TaskMan.TaskPri','(u32)&((WL_MAN*)0)->TaskMan.CurrTaskID','(u32)&((WL_MAN*)0)->TaskMan.Thread','(u32)&((WL_MAN*)0)->TaskMan.TaskTbl','(u32)&((WL_MAN*)0)->pSendMsgQueue','(u32)&((WL_MAN*)0)->pRecvMsgQueue','(u32)&((WL_MAN*)0)->HeapMan.RequestCmd','(u32)&((WL_MAN*)0)->HeapMan.ToWM','(u32)&((WL_MAN*)0)->CmdIf.pCmd','(u32)&((WL_MAN*)0)->CmdIf.Busy','(u32)&((WL_MAN*)0)->Config.DiagResult','(u32)&((WL_MAN*)0)->Work.STA','sizeof(WlCmdReq)','(u32)&((WlCmdReq*)0)->header.code','(u32)&((WlCmdReq*)0)->header.length','sizeof(WlCmdCfm)','(u32)&((WlCmdCfm*)0)->resultCode','sizeof(WLLIB_CMD_TBL)','(u32)&((WL_MAN*)0)->Config.RetryLimit','(u32)&((WL_MAN*)0)->Config.Mode','(u32)&((WL_MAN*)0)->Config.EnableChannel','(u32)&((WL_MAN*)0)->Work.CurrChannel','sizeof(((WL_MAN*)0)->TaskMan.EnQ)/sizeof(u16)','sizeof(((WL_MAN*)0)->TaskMan.TaskTbl)/sizeof(TASK_TBL)'];expected=[1684,380,8,4,2,4,0,8,16,18,20,24,188,772,776,512,500,1060,1064,830,844,20,12,14,10,4,8,810,814,812,958,4,24];
    if seed['name']!='RequestCmdTask':
        position=fields.index('sizeof(WLLIB_CMD_TBL)');fields.pop(position);expected.pop(position)
    source.write_text('#include "ordinary_wireless.c"\nconst u32 sdk312_layout[]={'+','.join(fields)+'};\n');argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-i',str((ROOT/seed['source']).parent),'-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);s=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk312_layout');raw=elf.get_section(s['st_shndx']).data()[s['st_value']:s['st_value']+s['st_size']]
    values=list(struct.unpack('<'+str(len(fields))+'I',raw))
    if values!=expected:raise ValueError('Full typed context/task/command layout differs:'+str(values))
    return dict(expressions=fields,values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=argv,actualCwd=str(ROOT),nativeAllocationExtentBeyondObservedClearUnproved=True,sourceDataCredit=0)

def compile_worker(index):
    seed=units()[index];directory=WORK/seed['name'];abi=layout(seed,directory/'layout');row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],directory/'positive');row.update(abiLayoutProof=abi,realLink=link,nativeSymbols={k:v['address']for k,v in link['bindings'].items()},nativeSymbolEntries=link['bindings']);write_json(directory/'build.json',dict(row=row,bodyPath=(directory/'positive/real-link/caller.bin').relative_to(ROOT).as_posix(),bodySha256=hashlib.sha256(body).hexdigest()));print(seed['name']+' fresh source compile/real link passed',flush=True)

def source_bodies():
    bodies={}
    for seed in units():
        row=json.loads((WORK/seed['name']/'build.json').read_text());compiler.linker.qualified(row['row']);obj=ROOT/row['row']['object'];binary=ROOT/row['bodyPath']
        if sha256(obj)!=row['row']['objectSha256']or sha256(binary)!=row['bodySha256']:raise ValueError('Fresh source product changed before connected execution')
        bodies[int(seed['address'],0)]=binary.read_bytes()
    return bodies

def packed(path,records):
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(gzip.compress(raw,mtime=0));return dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)

def proof_worker(index):
    seed=units()[index];directory=WORK/seed['name'];built=json.loads((directory/'build.json').read_text());row=built['row'];bodies=source_bodies();top=int(seed['address'],0);native=commands if seed['name']=='RequestCmdTask'else tasks;vectors=list(enumerate(native.cases()))
    if native is tasks:vectors=[(i,c)for i,c in vectors if c['entry']==top]
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();records=[];visited=set();helpers=setup=0
    for number,case in vectors:
        original=native.run(main,wram,case,number);compiled=native.run(main,wram,case,number,bodies=bodies);comparisons={key:original.get(key)==compiled.get(key)for key in('registers','cpsr','pc','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks','actualDeclaredHelperReturns')}
        if not original.get('actualOwnReturn')or not compiled.get('actualOwnReturn')or not original.get('modelPassed')or not compiled.get('modelPassed')or not all(comparisons.values()):raise ValueError(dict(name=seed['name'],case=case,original=original.get('modelChecks',original),compiled=compiled.get('modelChecks',compiled),comparisons=comparisons))
        helpers+=len(original['actualDeclaredHelperReturns'])+len(compiled['actualDeclaredHelperReturns']);setup+=len(original['actualSetupEntryReturns'])+len(compiled['actualSetupEntryReturns']);visited.update(original['visited']);records.append(dict(case=case,original=original,compiled=compiled,comparisons=comparisons))
    trace=packed(directory/'positive/native-records.json.gz',records);text=(ROOT/seed['source']).read_text();text=re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:((ROOT/seed['source']).parent/m[1]).read_text(),text);function=next(r for r in slicer.functions(text)if r['name']==seed['name']);fragment=text[function['start']:function['end']];old,new=MUTATIONS[seed['name']]
    if fragment.count(old)!=1:raise ValueError('Exactly one target-only ordinary wrong-C mutation required:'+old)
    wrong=text[:function['start']]+fragment.replace(old,new)+text[function['end']:];altered,wrong_build=diagnostic.build(dict(seed,address='0x2680000'),wrong,directory/'wrong-source',row['realLink']['bindings']);wrong_records=[];returned=rejected=0
    for number,case in vectors:
        result=native.run(main,wram,case,number,bodies=bodies,body=altered,virtual_address=0x02680000);returned+=int(result['actualOwnReturn']);rejected+=int(result.get('actualOwnReturn')and not result.get('modelPassed'));wrong_records.append(dict(case=case,result=result))
    if returned!=len(vectors)or not rejected:raise ValueError('Every wrong-source supported case must actually return, with independent model rejections')
    wrong_trace=packed(directory/'wrong-source/native-records.json.gz',wrong_records);oracle=dict(vectors=len(vectors),actualOriginalAndCompiledReturns=2*len(vectors),actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=setup,prefixBoundaryNormalReturnCredit=0,providerReplacements=[],allSupportedFieldAndStateModelsPassed=True,allRegistersCpsrStackNonstackRamAndOrderedWritesCompared=True,ownedInstructionAddresses=sorted(visited),ownedInstructionCoverageIsMeasuredNotAssumedComplete=True,trace=trace,fiveFreshCompiledBodiesInstalledBeforeTaskAndCommandPrerequisites=True,originalUnreconstructedTableAndHandlerCredit=0,radioSceneAsyncSchedulerAndAndroidUnproved=True);row.update(exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,oracle=oracle);result=dict(match=row,wrongC=dict(name=seed['name'],mutation=[old,new],build=wrong_build,actualOwnReturns=returned,modelRejections=rejected,trace=wrong_trace));write_json(directory/'result.json',result);print(json.dumps(dict(name=seed['name'],bytes=seed['bytes'],returns=2*len(vectors),wrongReturns=returned,wrongRejected=rejected)),flush=True)

def invoke(args):
    bootstrap='import runpy,sys;r=sys.argv.pop(1);p=sys.argv.pop(1);sys.path.insert(0,r);runpy.run_path(p,run_name="__main__")';argv=[sys.executable,'-I','-S','-c',bootstrap,str(ROOT),str(Path(__file__).resolve()),*args];p=subprocess.run(argv,cwd=ROOT.parent,capture_output=True,text=True,timeout=300)
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    print(p.stdout.strip(),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--compile-worker',type=int);parser.add_argument('--proof-worker',type=int);args=parser.parse_args()
    if args.compile_worker is not None:compile_worker(args.compile_worker);return
    if args.proof_worker is not None:proof_worker(args.proof_worker);return
    pin_path=PROFILE.parent/'generator-pins.json';pins=json.loads(pin_path.read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Pinned source/runtime/tool closure changed:'+pin['path'])
    seeds=units();snapshot=seeds[0]['authoritativeExclusionSnapshot'];path=ROOT/snapshot['path']
    if sha256(path)!=snapshot['sha256']:raise ValueError('Authoritative normalized exclusion snapshot changed')
    accepted=json.loads(path.read_text())['functions'];identity=lambda r:(r['processor'],r.get('program',''),r['module'],r['mode'],int(r['address'],0)if isinstance(r['address'],str)else r['address'])
    if any(identity(s)==identity(r)for s in seeds for r in accepted):raise ValueError('Duplicate accepted identity cannot receive new source coverage')
    for phase in('--compile-worker','--proof-worker'):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:list(pool.map(invoke,[[phase,str(i)]for i in range(len(seeds))]))
    results=[json.loads((WORK/s['name']/'result.json').read_text())for s in seeds];matches=[r['match']for r in results];symbols={}
    for row in matches:
        for name,value in row['nativeSymbols'].items():
            if name in symbols and symbols[name]!=value:raise ValueError('Shared named dependency has conflicting qualified addresses')
            symbols[name]=value
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',romSha256=seeds[0]['romSha256'],matches=matches,nativeSymbols=symbols,matchedInitializedBytes=1224,newOrdinaryFunctionCount=5,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=sum(r['oracle']['actualOriginalAndCompiledReturns']for r in matches),totalActualDeclaredHelperReturns=sum(r['oracle']['actualDeclaredHelperReturns']for r in matches),totalActualSetupEntryReturns=sum(r['oracle']['actualSetupEntryReturns']for r in matches),wrongC=[r['wrongC']for r in results],originalTablesAndAdditionalDefinitionsSourceCredit=0,sourceInputsNoWorkCaches=True,sourceSpecificHardwareAndAndroidPortabilityProven=False,generatorSources=pins+[dict(path=pin_path.relative_to(ROOT).as_posix(),sha256=sha256(pin_path))],pinnedGeneratorAndRuntimeDependencies=pins);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=1224,ownReturns=report['totalActualOwnReturns'])),flush=True)

if __name__=='__main__':main()
