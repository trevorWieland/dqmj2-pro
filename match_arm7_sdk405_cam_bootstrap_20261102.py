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
import arm7_sdk401_cam_bootstrap_native_20261102 as receive
import compile_arm7_sdk386_receive_data_20261102 as helper_compiler
import compile_arm7_sdk404_cam_bootstrap_20261102 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import slice_arm7_sdk147_closed_v3_20261101 as slicer
from project import ROOT,sha256,write_json

WORK=ROOT/'work/arm7-bulk-20261030/sdk405-cam-bootstrap292'
REPORT=ROOT/'evidence/matches/arm7-sdk405-cam-bootstrap292-20261102.json'
FIELDS=['sizeof(WL_MAN)', 'sizeof(u16)', 'sizeof(u32)', 'sizeof(void*)', 'sizeof(CAM_ELEMENT)', 'sizeof(CAM_MAN)', 'sizeof(BC_ADRS)', '(u32)&((WL_MAN*)0)->Config.pCAM', '(u32)&((WL_MAN*)0)->Config.MaxStaNum', '(u32)&((WL_MAN*)0)->CamMan', '(u32)&((CAM_ELEMENT*)0)->maxLifeTime', '(u32)&((CAM_MAN*)0)->dmm']
VALUES=[1684, 2, 4, 4, 28, 16, 6, 796, 802, 1324, 26, 10]
MUTATIONS={'InitializeCAM': ('CAM_SetStaState(0, 0x40 );', 'CAM_SetStaState(0, 0x30 );', 1), 'InitCAM': ('pCamMan->NotClass3 = 0xFFFE;', 'pCamMan->NotClass3 = 0xFFFF;', 1)}

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
    helper_seed=next(r for r in json.loads(helper_compiler.linker.PROFILE.read_text())['units']if r['name']=='CAM_InitElement');helper_row,helper_link,helper_body=helper_compiler.compile_unit(helper_seed,ROOT/helper_seed['source'],WORK/'source-helper');helper_proof=dict(row=helper_row,realLink=helper_link,bodyPath=(WORK/'source-helper/real-link/caller.bin').relative_to(ROOT).as_posix(),sha256=hashlib.sha256(helper_body).hexdigest(),additionalCredit=0)
    for seed in json.loads(profile.read_text())['units']:
        module=receive;case_rows=[(i,c)for i,c in enumerate(module.cases())if c['entry']==int(seed['address'],0)];row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['name']/'positive');records=[];branch=set();own=helpers_count=setup=0
        for index,case in case_rows:
            original=module.run(main,wram,case,index);compiled=module.run(main,wram,case,index,body=body,compiled_helper=helper_body);fields=('registers','cpsr','pc','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks','actualDeclaredHelperReturns');comparisons={k:original.get(k)==compiled.get(k)for k in fields}
            if not original['actualOwnReturn']or not compiled['actualOwnReturn']or not original['modelPassed']or not compiled['modelPassed']or not all(comparisons.values()):raise ValueError(dict(name=seed['name'],index=index,case=case,original=original.get('modelChecks',original),compiled=compiled.get('modelChecks',compiled),comparisons=comparisons))
            own+=2;helpers_count+=len(original['actualDeclaredHelperReturns'])+len(compiled['actualDeclaredHelperReturns']);setup+=len(original['actualSetupEntryReturns'])+len(compiled['actualSetupEntryReturns']);branch.update(original['visited']);records.append(dict(index=index,case=case,original=original,compiled=compiled,comparisons=comparisons))
        positive_trace=packed(WORK/seed['name']/'positive/native-records.json.gz',records);text=(ROOT/seed['source']).read_text();text=re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:((ROOT/seed['source']).parent/m[1]).read_text(),text);f=next(f for f in slicer.functions(text)if f['name']==seed['name']);fragment=text[f['start']:f['end']];old,new,count=MUTATIONS[seed['name']]
        if fragment.count(old)!=count:raise ValueError('Exact independently targeted wrong-C mutation missing:'+seed['name'])
        altered,wrong_build=diagnostic.build(dict(seed,address='0x2680000'),text[:f['start']]+fragment.replace(old,new)+text[f['end']:],WORK/seed['name']/'wrong-source',link['bindings']);bad=[];returned=rejected=0
        for index,case in case_rows:
            result=module.run(main,wram,case,index,body=altered,virtual_address=0x02680000,compiled_helper=helper_body);returned+=int(result['actualOwnReturn']);rejected+=int(result.get('actualOwnReturn')and not result.get('modelPassed'));bad.append(dict(index=index,case=case,result=result))
        if returned!=len(case_rows)or not rejected:raise ValueError('All supported wrong-C entries must actually return, with independent state/model rejections:'+seed['name'])
        wrong_trace=packed(WORK/seed['name']/'wrong-source/native-records.json.gz',bad);native_symbols={k:v['address']for k,v in link['bindings'].items()}
        for k,v in native_symbols.items():
            if k in symbols and symbols[k]!=v:raise ValueError('Conflicting qualified source bindings')
            symbols[k]=v
        row.update(realLink=link,abiLayoutProof=layout(seed),nativeSymbols=native_symbols,nativeSymbolEntries=link['bindings'],exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,oracle=dict(vectors=len(case_rows),actualOriginalAndCompiledReturns=own,actualDeclaredHelperReturns=helpers_count,actualSetupEntryReturns=setup,providerReplacements=[],prefixBoundaryNormalReturnCredit=0,trace=positive_trace,allRegistersCpsrStackRamAndOrderedWritesCompared=True,supportedFieldModelsPassed=True,sourceLinkedInitializerProof=helper_proof,sourceLinkedInitializerAdditionalCredit=0),wrongC=dict(mutation=[old,new],build=wrong_build,actualOwnReturns=returned,modelRejections=rejected,trace=wrong_trace),nativeExecutedOwnWords=len(branch),unvisitedOwnCodeAddresses=[hex(a)for a in range(int(seed['address'],0),int(seed['address'],0)+seed['codeBytes'],4)if a not in branch],unrecoveredCalleesAndExtraDefinitionsCredit=0)
        matches.append(row);own_returns+=own;helper_returns+=helpers_count;setup_returns+=setup;wrong_returns+=returned;wrong_rejections+=rejected;print(json.dumps(dict(name=seed['name'],ownReturns=own,helpers=helpers_count,setup=setup,wrongReturns=returned,wrongRejected=rejected)),flush=True)
    result=dict(processor='arm7',program='',romSha256=matches[0]['romSha256'],generator=Path(__file__).name,generatorSha256=sha256(__file__),matches=matches,nativeSymbols=symbols,matchedInitializedBytes=292,newOrdinaryFunctionCount=2,totalActualOwnReturns=own_returns,totalActualDeclaredHelperReturns=helper_returns,totalActualSetupEntryReturns=setup_returns,totalWrongCActualReturns=wrong_returns,totalWrongCModelRejections=wrong_rejections,sourceReconstructionComplete=False,wholeModuleLinked=False,initializedDenominatorDelta=0,sourceInputsNoWorkCaches=True,originalCalleesAndAdditionalDefinitionsCredit=0,physicalRadioAndSceneAdmissionUnproved=True,sourceLinkedInitializerDefinition=helper_proof,initializedBroadcastTableSourceCredit=0,generatorSources=pins+[dict(path=pinpath.relative_to(ROOT).as_posix(),sha256=sha256(pinpath))]);write_json(REPORT,result);print(json.dumps(dict(reportSha256=sha256(REPORT),ownReturns=own_returns,helpers=helper_returns,setup=setup_returns,wrongReturns=wrong_returns,wrongRejected=wrong_rejections)),flush=True)

if __name__=='__main__':main()
