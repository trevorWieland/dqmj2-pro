import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
import arm7_sdk417_mp_key_native_20261102 as key_native
import arm7_sdk418_probe_response_native_20261102 as probe_native
import arm7_sdk419_beacon_native_20261102 as beacon_native
import compile_arm7_sdk422_beacon_probe_key_20261102 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import slice_arm7_sdk147_closed_v3_20261101 as slicer
from project import ROOT,sha256,write_json

WORK=ROOT/'work/arm7-bulk-20261030/sdk423-beacon-probe-key3016'
REPORT=ROOT/'evidence/matches/arm7-sdk423-beacon-probe-key3016-20261102.json'
FIELDS=['sizeof(WL_MAN)','sizeof(u16)','sizeof(u32)','sizeof(u64)','sizeof(void*)','sizeof(BEACON_FRAME)','sizeof(PRBRES_FRAME)','sizeof(ELEMENT_CHECKER)','sizeof(WlMlmeScanReq)','sizeof(WlBssDesc)','sizeof(WlMpKeyData)','sizeof(native_host_arm7_table_null_adrs_027f74c0)','(u32)&((WL_MAN*)0)->Counter.rx.beacon','(u32)&((WL_MAN*)0)->Work.BeaconPeriod','(u32)&((WL_MAN*)0)->MLME.State','(u32)&((WL_MAN*)0)->MLME.pReq','(u32)&((WL_MAN*)0)->MLME.pCfm','(u32)&((WL_MAN*)0)->TxCtrl.Mp.Busy','(u32)&((WL_MAN*)0)->TxCtrl.pMpEndInd','(u32)&((WlBssDesc*)0)->capaInfo','(u32)&((WlBssDesc*)0)->rateSet','(u32)&((WlBssDesc*)0)->channel','(u32)&((WlBssDesc*)0)->otherElement']
VALUES=[1684,2,4,8,4,112,112,44,84,68,12,6,1392,946,1028,1052,1056,1128,1212,44,46,54,64]
MODULES={'RxBeaconFrame':beacon_native,'RxProbeResFrame':probe_native,'RxKeyDataFrame':key_native}
MUTATIONS={'RxBeaconFrame':('->Counter.rx.beacon++;','->Counter.rx.beacon += 2;',1),'RxProbeResFrame':('pCfm->bssDescCount++;','pCfm->bssDescCount += 2;',1),'RxKeyDataFrame':('pTxCtrl->GetKeyMap |= bitmap;','pTxCtrl->GetKeyMap &= ~bitmap;',1)}

def packed(path,records):
    raw=json.dumps(records,sort_keys=True,separators=(',',':')).encode();path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(raw,mtime=0));return dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)

def layout(seed):
    indices=list(range(len(FIELDS)));fields=[FIELDS[i]for i in indices];expected=[VALUES[i]for i in indices];folder=WORK/'layout'/seed['name'];folder.mkdir(parents=True,exist_ok=True);source=folder/'layout.c';obj=folder/'layout.o';source.write_text('#include "ordinary_wireless.c"\nconst u32 sdk405_layout[]={'+','.join(fields)+'};\n',encoding='utf-8');argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-i',str((ROOT/seed['source']).parent),'-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    with obj.open('rb')as stream:
        e=ELFFile(stream);symbol=next(s for s in e.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk405_layout');raw=e.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
    values=list(struct.unpack('<'+str(len(fields))+'I',raw))
    if values!=expected:raise ValueError('Complete compatible native type/frame/alarm layout changed:'+str(values))
    return dict(expressions=fields,values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=argv,actualCwd=str(ROOT),sourceDataCredit=0)

def main():
    profile=compiler.linker.PROFILE;pinpath=profile.parent/'generator-pins.json';pins=json.loads(pinpath.read_text())['files']
    for r in pins:
        if sha256(ROOT/r['path'])!=r['sha256']:raise ValueError('Complete pinned source/runtime/compiler inputs changed:'+r['path'])
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();matches=[];own_returns=helper_returns=setup_returns=wrong_returns=wrong_rejections=0;symbols={};native_cases={};module_hashes={'main':hashlib.sha256(main).hexdigest(),'wram':hashlib.sha256(wram).hexdigest()}
    if module_hashes!={'main':'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416','wram':'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'}:raise ValueError('Both measured original ARM7 modules required')
    builds={};body_map={}
    for seed in json.loads(profile.read_text(encoding='utf-8'))['units']:
        row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['name']/'positive');builds[seed['name']]=(row,link,body);body_map[int(seed['address'],0)]=body
    all_layout=layout(json.loads(profile.read_text(encoding='utf-8'))['units'][0])
    for seed in json.loads(profile.read_text())['units']:
        module=MODULES[seed['name']];case_rows=list(enumerate(module.cases()));row,link,body=builds[seed['name']];records=[];branch=set();own=helpers_count=setup=0
        for index,case in case_rows:
            if index and index%1000==0:print(json.dumps(dict(phase='positive',name=seed['name'],vectorsCompleted=index)),flush=True)
            original=module.run(main,wram,case,index);compiled=module.run(main,wram,case,index,body=body,body_map=body_map);fields=('registers','cpsr','pc','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks','actualDeclaredHelperReturns');comparisons={k:original.get(k)==compiled.get(k)for k in fields}
            if not original['actualOwnReturn']or not compiled['actualOwnReturn']or not original['modelPassed']or not compiled['modelPassed']or not all(comparisons.values()):raise ValueError(dict(name=seed['name'],index=index,case=case,original=original.get('modelChecks',original),compiled=compiled.get('modelChecks',compiled),comparisons=comparisons))
            own+=2;helpers_count+=len(original['actualDeclaredHelperReturns'])+len(compiled['actualDeclaredHelperReturns']);setup+=len(original['actualSetupEntryReturns'])+len(compiled['actualSetupEntryReturns']);branch.update(original['visited']);records.append(dict(index=index,case=case,original=original,compiled=compiled,comparisons=comparisons))
        positive_trace=packed(WORK/seed['name']/'positive/native-records.json.gz',records);text=(ROOT/seed['source']).read_text();text=re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:((ROOT/seed['source']).parent/m[1]).read_text(),text);f=next(f for f in slicer.functions(text)if f['name']==seed['name']);fragment=text[f['start']:f['end']];old,new,count=MUTATIONS[seed['name']]
        if fragment.count(old)!=count:raise ValueError('Exact independently targeted wrong-C mutation missing:'+seed['name'])
        altered,wrong_build=diagnostic.build(dict(seed,address='0x2680000'),text[:f['start']]+fragment.replace(old,new)+text[f['end']:],WORK/seed['name']/'wrong-source',link['bindings']);bad=[];returned=rejected=0
        for index,case in case_rows:
            if index and index%1000==0:print(json.dumps(dict(phase='wrong-source',name=seed['name'],vectorsCompleted=index)),flush=True)
            result=module.run(main,wram,case,index,body=altered,virtual_address=0x02680000,body_map=body_map);returned+=int(result['actualOwnReturn']);rejected+=int(result.get('actualOwnReturn')and not result.get('modelPassed'));bad.append(dict(index=index,case=case,result=result))
        if returned!=len(case_rows)or not rejected:raise ValueError('All supported wrong-C entries must actually return, with independent state/model rejections:'+seed['name'])
        wrong_trace=packed(WORK/seed['name']/'wrong-source/native-records.json.gz',bad);native_symbols={k:v['address']for k,v in link['bindings'].items()}
        for k,v in native_symbols.items():
            if k in symbols and symbols[k]!=v:raise ValueError('Conflicting qualified source bindings')
            symbols[k]=v
        row.update(realLink=link,abiLayoutProof=all_layout,nativeSymbols=native_symbols,nativeSymbolEntries=link['bindings'],exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,oracle=dict(vectors=len(case_rows),actualOriginalAndCompiledReturns=own,actualDeclaredHelperReturns=helpers_count,actualSetupEntryReturns=setup,providerReplacements=[],prefixBoundaryNormalReturnCredit=0,trace=positive_trace,allRegistersCpsrStackRamAndOrderedWritesCompared=True,supportedFieldModelsPassed=True,sourceLinkedReceiveCallees=[dict(entry=hex(a),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),additionalCredit=0)for a,b in body_map.items()if a!=int(seed['address'],0)],sourceLinkedReceiveAdditionalCredit=0),wrongC=dict(mutation=[old,new],build=wrong_build,actualOwnReturns=returned,modelRejections=rejected,trace=wrong_trace),nativeExecutedOwnWords=len(branch),unvisitedOwnCodeAddresses=[hex(a)for a in range(int(seed['address'],0),int(seed['address'],0)+seed['codeBytes'],4)if a not in branch],unrecoveredCalleesAndExtraDefinitionsCredit=0)
        matches.append(row);own_returns+=own;helper_returns+=helpers_count;setup_returns+=setup;wrong_returns+=returned;wrong_rejections+=rejected;print(json.dumps(dict(name=seed['name'],ownReturns=own,helpers=helpers_count,setup=setup,wrongReturns=returned,wrongRejected=rejected)),flush=True)
    result=dict(processor='arm7',program='',romSha256=matches[0]['romSha256'],generator=Path(__file__).name,generatorSha256=sha256(__file__),matches=matches,nativeSymbols=symbols,matchedInitializedBytes=3016,newOrdinaryFunctionCount=3,totalActualOwnReturns=own_returns,totalActualDeclaredHelperReturns=helper_returns,totalActualSetupEntryReturns=setup_returns,totalWrongCActualReturns=wrong_returns,totalWrongCModelRejections=wrong_rejections,sourceReconstructionComplete=False,wholeModuleLinked=False,initializedDenominatorDelta=0,sourceInputsNoWorkCaches=True,originalCalleesAndAdditionalDefinitionsCredit=0,physicalRadioAndSceneAdmissionUnproved=True,sourceLinkedDefinitions=[dict(entry=hex(a),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())for a,b in body_map.items()],initializedNullTableSourceCredit=0,generatorSources=pins+[dict(path=pinpath.relative_to(ROOT).as_posix(),sha256=sha256(pinpath))]);write_json(REPORT,result);print(json.dumps(dict(reportSha256=sha256(REPORT),ownReturns=own_returns,helpers=helper_returns,setup=setup_returns,wrongReturns=wrong_returns,wrongRejected=wrong_rejections)),flush=True)

if __name__=='__main__':main()
