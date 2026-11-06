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
import arm7_sdk356_measure_task_native_20261102 as native
import prove_arm7_sdk369_unsigned_division_entry_abi_20261102 as helper_abi
import compile_arm7_sdk364_measure_task_20261102 as compiler
import compile_arm7_sdk350_mlme_tasks_timeouts_20261102 as callback_compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import slice_arm7_sdk147_closed_v3_20261101 as slicer
from project import ROOT,sha256,write_json

WORK=ROOT/'work/arm7-bulk-20261030/sdk365-measure-task624'
REPORT=ROOT/'evidence/matches/arm7-sdk365-measure-task624-20261102.json'

def packed(path,records):
    raw=json.dumps(records,sort_keys=True,separators=(',',':')).encode();path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(raw,mtime=0));return dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0)

def layout(seed):
    folder=WORK/'layout';folder.mkdir(parents=True,exist_ok=True);fields=['sizeof(WL_MAN)','sizeof(u16)','sizeof(u32)','sizeof(void*)','(u32)&((WL_MAN*)0)->MLME.Work.Measure.Counter','(u32)&((WL_MAN*)0)->MLME.Work.Measure.CCA','(u32)&((WL_MAN*)0)->MLME.Work.Measure.Channel','(u32)&((WL_MAN*)0)->MLME.Work.Measure.sts','(u32)&((WL_MAN*)0)->MLME.Work.Measure.bkPowerMode','(u32)&((WL_MAN*)0)->MLME.Work.Measure.bkCCAMode','(u32)&((WL_MAN*)0)->MLME.Work.Measure.bkEdTh','sizeof(WlMlmeMeasChanReq)','sizeof(WlMlmeMeasChanCfm)','(u32)&((WlMlmeMeasChanReq*)0)->ccaMode','(u32)&((WlMlmeMeasChanReq*)0)->edThreshold','(u32)&((WlMlmeMeasChanReq*)0)->measureTime','(u32)&((WlMlmeMeasChanReq*)0)->channelList','(u32)&((WlMlmeMeasChanCfm*)0)->ccaBusyInfo'];expected=[1684,2,4,4,0x408,0x40c,0x418,0x41a,0x410,0x412,0x414,40,40,18,20,22,24,8];source=folder/'layout.c';obj=folder/'layout.o';source.write_text('#include "ordinary_wireless.c"\nconst u32 sdk365_layout[]={'+','.join(fields)+'};\n',encoding='utf-8');argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-i',str((ROOT/seed['source']).parent),'-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    with obj.open('rb')as stream:
        e=ELFFile(stream);symbol=next(s for s in e.get_section_by_name('.symtab').iter_symbols()if s.name=='sdk365_layout');raw=e.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
    values=list(struct.unpack('<'+str(len(fields))+'I',raw))
    if values!=expected:raise ValueError('Full native measurement views changed:'+str(values))
    return dict(expressions=fields,values=values,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualArgv=argv,actualCwd=str(ROOT),sourceDataCredit=0)

def main():
    profile=compiler.linker.PROFILE;pins=json.loads((profile.parent/'generator-pins.json').read_text())['files']
    for r in pins:
        if sha256(ROOT/r['path'])!=r['sha256']:raise ValueError('Complete pinned source/runtime/compiler inputs changed:'+r['path'])
    helper_abi.main();native.main();native_path=ROOT/'evidence/attempts/arm7-sdk356-measure-task-native-20261102.json';baseline=json.loads(native_path.read_text());trace=baseline['nativeTrace'];originals=json.loads(gzip.decompress((ROOT/trace['path']).read_bytes()));cases=native.cases()
    if len(originals)!=1160 or baseline['actualOwnReturns']!=1112 or baseline['failedModels']or len(baseline['unsupported'])!=48:raise ValueError('Complete supported/unsupported original-context partition changed')
    seed=json.loads(profile.read_text())['units'][0];abi=layout(seed);row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'positive');row.update(realLink=link,abiLayoutProof=abi,nativeSymbols={k:v['address']for k,v in link['bindings'].items()},nativeSymbolEntries=link['bindings'])
    callback=next(r for r in json.loads(callback_compiler.linker.PROFILE.read_text())['units']if r['name']=='MLME_MeasChanTimeOut');crow,clink,cbody=callback_compiler.compile_unit(callback,ROOT/callback['source'],WORK/'source-callback');callback_proof=dict(row=crow,realLink=clink,bodyPath=(WORK/'source-callback/real-link/caller.bin').relative_to(ROOT).as_posix(),bodySha256=hashlib.sha256(cbody).hexdigest(),additionalSourceCredit=0,asynchronousCallbackDispatchUnproved=True)
    main=(ROOT/seed['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();records=[];helpers=setup=0;wanted=[]
    for index,(case,original)in enumerate(zip(cases,originals)):
        if case!=original['case']:raise ValueError('Original physical case order differs')
        if not original['actualOwnReturn']:continue
        compiled=native.run(main,wram,case,index,body=body,linked_callback=cbody);fields=('registers','cpsr','pc','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks','actualDeclaredHelperReturns');comparisons={k:original[k]==compiled[k]for k in fields}
        if not original['modelPassed']or not compiled.get('actualOwnReturn')or not compiled.get('modelPassed')or not all(comparisons.values()):raise ValueError(dict(case=case,checks=compiled.get('modelChecks',compiled),comparisons=comparisons))
        helpers+=len(original['actualDeclaredHelperReturns'])+len(compiled['actualDeclaredHelperReturns']);setup+=len(original['actualSetupEntryReturns'])+len(compiled['actualSetupEntryReturns']);records.append(dict(index=index,case=case,original=original,compiled=compiled,comparisons=comparisons));wanted.append((index,case))
    positive_trace=packed(WORK/'positive/native-records.json.gz',records);text=(ROOT/seed['source']).read_text();text=re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:((ROOT/seed['source']).parent/m[1]).read_text(),text);f=next(f for f in slicer.functions(text)if f['name']==seed['name']);fragment=text[f['start']:f['end']];old='ratio = 100;';new='ratio = 99;'
    if fragment.count(old)!=1:raise ValueError('Exact independent wrong-C saturation mutation missing')
    altered,wrong_build=diagnostic.build(dict(seed,address='0x2680000'),text[:f['start']]+fragment.replace(old,new)+text[f['end']:],WORK/'wrong-source',link['bindings']);bad=[];returned=rejected=0
    for index,case in wanted:
        result=native.run(main,wram,case,index,body=altered,virtual_address=0x02680000,linked_callback=cbody);returned+=int(result['actualOwnReturn']);rejected+=int(result.get('actualOwnReturn')and not result.get('modelPassed'));bad.append(dict(index=index,case=case,result=result))
    if returned!=1112 or not rejected:raise ValueError('All wrong-C supported entries must actually return with independent state rejections')
    wrong_trace=packed(WORK/'wrong-source/native-records.json.gz',bad);row.update(exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,oracle=dict(vectors=1112,actualOriginalAndCompiledReturns=2224,actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=setup,providerReplacements=[],prefixBoundaryNormalReturnCredit=0,trace=positive_trace,allRegistersCpsrStackRamAndOrderedWritesCompared=True,supportedFieldModelsPassed=True,unsupportedOriginalAttempts=48,unsupportedAttemptsSourceCredit=0,sourceLinkedCallbackProof=callback_proof,callbackSourceAndReturnCredit=0))
    result=dict(processor='arm7',program='',romSha256=seed['romSha256'],generator=Path(__file__).name,generatorSha256=sha256(__file__),matches=[row],nativeSymbols=row['nativeSymbols'],matchedInitializedBytes=624,newOrdinaryFunctionCount=1,totalActualOwnReturns=2224,totalActualDeclaredHelperReturns=helpers,totalActualSetupEntryReturns=setup,wrongC=dict(mutation=[old,new],build=wrong_build,actualOwnReturns=returned,modelRejections=rejected,trace=wrong_trace),originalContextReport=dict(path=native_path.relative_to(ROOT).as_posix(),sha256=sha256(native_path)),unsupportedOriginalAttempts=baseline['unsupported'],unsupportedSourceCredit=0,sourceReconstructionComplete=False,wholeModuleLinked=False,initializedDenominatorDelta=0,sourceInputsNoWorkCaches=True,originalCalleesAndAdditionalDefinitionsCredit=0,generatorSources=pins+[dict(path=(profile.parent/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(profile.parent/'generator-pins.json'))]);write_json(REPORT,result);print(json.dumps(dict(reportSha256=sha256(REPORT),ownReturns=2224,helpers=helpers,setup=setup,wrongReturns=returned,wrongRejected=rejected,unsupported=48)),flush=True)

if __name__=='__main__':main()
