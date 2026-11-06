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
import arm7_sdk295_transmit_family_native_20261102 as native
import compile_arm7_sdk294_transmit_family_20261102 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import slice_arm7_sdk147_closed_v3_20261101 as slicer
from project import ROOT,sha256,write_json

PROFILE=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk294-transmit-family-final/profile.json'
WORK=ROOT/'work/arm7-bulk-20261030/sdk296-transmit-family'
REPORT=ROOT/'evidence/matches/arm7-sdk296-transmit-family1600-20261102.json'
MUTATIONS={'InitTxCtrl':('sizeof(TX_CTRL)','(sizeof(TX_CTRL)-4)'),'ClearTxKeyData':('pTxCtrl->Key[0].Busy = 0','pTxCtrl->Key[0].Busy = 1'),'ClearQueuedPri':('pTxq->pFrm->MacHeader.Tx.Status = 2','pTxq->pFrm->MacHeader.Tx.Status = 3'),'ResetTxqPri':('native_host_arm7_priority_bits_027f787c[pri];','(native_host_arm7_priority_bits_027f787c[pri] ^ 1);'),'DeleteAllTxFrames':('pTxCtrl->Mp.InCount--;','pTxCtrl->Mp.InCount++;'),'TxPsPollFrame':('pTxq->InCount++;','pTxq->InCount += 2;'),'StartBeaconFrame':('pTxq->Busy = 1','pTxq->Busy = 2')}

def layout(seed,directory):
    directory.mkdir(parents=True,exist_ok=True);source=directory/'layout.c';obj=directory/'layout.o';fields=['sizeof(WL_MAN)','sizeof(TX_CTRL)','sizeof(TXQ)','sizeof(u32)','sizeof(u16)','sizeof(void*)','(u32)&((WL_MAN*)0)->TxCtrl','(u32)&((WL_MAN*)0)->TxCtrl.Txq[2].Busy','(u32)&((WL_MAN*)0)->TxCtrl.Txq[2].InCount','(u32)&((WL_MAN*)0)->TxCtrl.Txq[2].pMacFrm','(u32)&((WL_MAN*)0)->TxCtrl.Txq[2].pFrm','(u32)&((WL_MAN*)0)->TxCtrl.Txq[2].pEndFunc','(u32)&((WL_MAN*)0)->TxCtrl.Mp.Busy','(u32)&((WL_MAN*)0)->TxCtrl.Mp.InCount','(u32)&((WL_MAN*)0)->TxCtrl.Key[0].Busy','(u32)&((WL_MAN*)0)->TxCtrl.Key[1].Busy','(u32)&((WL_MAN*)0)->TxCtrl.Beacon.Busy','(u32)&((WL_MAN*)0)->TxCtrl.Beacon.pMacFrm','(u32)&((WL_MAN*)0)->TxCtrl.pMpEndInd','(u32)&((WL_MAN*)0)->TxCtrl.BkKeyIn','(u32)&((WL_MAN*)0)->TxCtrl.BkKeyOut','(u32)&((WL_MAN*)0)->Work.Mode','(u32)&((WL_MAN*)0)->Config.WepMode'];expected=[0x694,0xb0,20,4,2,4,0x42c,0x454,0x456,0x45c,0x460,0x464,0x468,0x46a,0x47c,0x490,0x4a4,0x4ac,0x4bc,0x4ce,0x4d0,0x350,0x334];source.write_text('#include "ordinary_wireless.c"\nconst u32 sdk296_layout[]={'+','.join(fields)+'};\n');argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-i',str((ROOT/seed['source']).parent),'-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk296_layout');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
    values=list(struct.unpack('<'+str(len(fields))+'I',raw))
    if values!=expected:raise ValueError('Full context/transmit/primitive layout changed:'+str(values))
    return dict(expressions=fields,values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=argv,actualCwd=str(ROOT),sourceDataCredit=0)

def worker(index):
    seed=json.loads(PROFILE.read_text())['units'][index];directory=WORK/seed['name'];abi=layout(seed,directory/'layout');row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],directory/'positive');main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();module=wram if seed['module']=='arm7-wram'else main;base=native.context.WRAM if seed['module']=='arm7-wram'else native.context.MAIN;top=int(seed['address'],0)
    if body!=module[top-base:top-base+seed['bytes']]:raise ValueError('Full freshly linked body differs')
    vectors=[(i,c)for i,c in enumerate(native.cases())if c['entry']==top];records=[];visited=set();helpers=setup=0
    for number,case in vectors:
        original=native.run(main,wram,case,number,link['bindings']);compiled=native.run(main,wram,case,number,link['bindings'],body=body);comparisons={key:original.get(key)==compiled.get(key)for key in('registers','cpsr','pc','relevantRegisters','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks')}
        if not original.get('actualOwnReturn')or not compiled.get('actualOwnReturn')or not original.get('modelPassed')or not compiled.get('modelPassed')or not all(comparisons.values()):raise ValueError(dict(name=seed['name'],case=case,original=original.get('modelChecks',original),compiled=compiled.get('modelChecks',compiled),comparisons=comparisons))
        helpers+=len(original['actualDeclaredHelperReturns'])+len(compiled['actualDeclaredHelperReturns']);setup+=len(original['actualSetupEntryReturns'])+len(compiled['actualSetupEntryReturns']);visited.update(original['visited']);records.append(dict(case=case,original=original,compiled=compiled,comparisons=comparisons))
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=directory/'positive/native-records.json.gz';trace.write_bytes(gzip.compress(raw,mtime=0));text=(ROOT/seed['source']).read_text();text=re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:((ROOT/seed['source']).parent/m[1]).read_text(),text);function=next(r for r in slicer.functions(text)if r['name']==seed['name']);fragment=text[function['start']:function['end']];old,new=MUTATIONS[seed['name']]
    if fragment.count(old)!=1:raise ValueError('Exactly one target-only ordinary wrong-C mutation expected:'+old)
    changed=text[:function['start']]+fragment.replace(old,new)+text[function['end']:];altered,wrong_build=diagnostic.build(dict(seed,address='0x2680000'),changed,directory/'wrong-source',link['bindings']);returned=rejected=0;wrong_records=[]
    for number,case in vectors:
        result=native.run(main,wram,case,number,link['bindings'],body=altered,virtual_address=0x02680000);returned+=int(result['actualOwnReturn']);rejected+=int(result.get('actualOwnReturn')and not result.get('modelPassed'));wrong_records.append(dict(case=case,result=result))
    if returned!=len(vectors)or not rejected:raise ValueError('Wrong source must actually return in every supported case and be rejected by the model')
    wrong_raw=(json.dumps(wrong_records,sort_keys=True,separators=(',',':'))+'\n').encode();wrong_trace=directory/'wrong-source/native-records.json.gz';wrong_trace.write_bytes(gzip.compress(wrong_raw,mtime=0));oracle=dict(vectors=len(vectors),actualOriginalAndCompiledReturns=2*len(vectors),actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=setup,prefixBoundaryNormalReturnCredit=0,providerReplacements=[],allSupportedFieldAndStateModelsPassed=True,allRelevantRegistersNonstackRamAndOrderedWritesCompared=True,ownedInstructionAddresses=sorted(visited),ownedInstructionCoverageIsMeasuredNotAssumedComplete=True,trace=dict(path=trace.relative_to(ROOT).as_posix(),compressedSha256=sha256(trace),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0),radioTimingSceneAndAndroidPortabilityUnproved=True)
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,nativeSymbols={name:b['address']for name,b in link['bindings'].items()},nativeSymbolEntries=link['bindings'],oracle=oracle,abiLayoutProof=abi);result=dict(match=row,wrongC=dict(name=seed['name'],mutation=[old,new],build=wrong_build,actualOwnReturns=returned,modelRejections=rejected,trace=dict(path=wrong_trace.relative_to(ROOT).as_posix(),compressedSha256=sha256(wrong_trace),rawSha256=hashlib.sha256(wrong_raw).hexdigest(),gzipMtime=0)));write_json(directory/'result.json',result);print(json.dumps(dict(name=seed['name'],bytes=seed['bytes'],returns=2*len(vectors),wrongReturns=returned,wrongRejected=rejected)),flush=True)

def invoke(index):
    bootstrap='import runpy,sys;r=sys.argv.pop(1);p=sys.argv.pop(1);sys.path.insert(0,r);runpy.run_path(p,run_name="__main__")';argv=[sys.executable,'-I','-S','-c',bootstrap,str(ROOT),str(Path(__file__).resolve()),'--worker',str(index)];p=subprocess.run(argv,cwd=ROOT.parent,capture_output=True,text=True,timeout=240)
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    print(p.stdout.strip(),flush=True);seed=json.loads(PROFILE.read_text())['units'][index];return json.loads((WORK/seed['name']/'result.json').read_text())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',type=int);args=parser.parse_args()
    if args.worker is not None:worker(args.worker);return
    pin_path=PROFILE.parent/'generator-pins.json';pins=json.loads(pin_path.read_text())['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Complete source/tool/model closure changed:'+pin['path'])
    if sha256(PROFILE)!=compiler.linker.PROFILE_SHA:raise ValueError('Exact family profile changed')
    p=subprocess.run([sys.executable,str(ROOT/'validate_arm7_sdk291_pspoll_scope_20261102.py')],cwd=ROOT.parent,capture_output=True,text=True,timeout=120)
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    units=json.loads(PROFILE.read_text())['units']
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:results=list(pool.map(invoke,range(len(units))))
    matches=[r['match']for r in results];symbols={}
    for row in matches:
        for name,value in row['nativeSymbols'].items():
            if name in symbols and symbols[name]!=value:raise ValueError('Shared named dependency has conflicting actual addresses')
            symbols[name]=value
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',romSha256=units[0]['romSha256'],matches=matches,nativeSymbols=symbols,matchedInitializedBytes=1600,newOrdinaryFunctionCount=7,initializedDenominatorDelta=0,wholeModuleLinked=False,sourceReconstructionComplete=False,totalActualOwnReturns=sum(r['oracle']['actualOriginalAndCompiledReturns']for r in matches),totalActualDeclaredHelperReturns=sum(r['oracle']['actualDeclaredHelperReturns']for r in matches),totalActualSetupEntryReturns=sum(r['oracle']['actualSetupEntryReturns']for r in matches),wrongC=[r['wrongC']for r in results],originalCallbackAndTableSourceCredit=0,additionalDefinitionsInUnitsHaveNoSourceCredit=True,sourceInputsNoWorkCaches=True,scopeWitness='evidence/attempts/arm7-sdk289-pspoll-callback104-scope-20261102.json',scopeWitnessSha256=sha256(ROOT/'evidence/attempts/arm7-sdk289-pspoll-callback104-scope-20261102.json'),sourceSpecificHardwareAndAndroidPortabilityProven=False,generatorSources=pins+[dict(path=pin_path.relative_to(ROOT).as_posix(),sha256=sha256(pin_path))],pinnedGeneratorAndRuntimeDependencies=pins);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=1600,ownReturns=report['totalActualOwnReturns'])),flush=True)

if __name__=='__main__':main()
