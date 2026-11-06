import concurrent.futures
import hashlib
import json
import re
from pathlib import Path
import match_runtime
import compile_arm7_sdk435_intr_transmit_compiler_20261102 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
import slice_arm7_sdk428_attributes_20261102 as slicer
import audit_arm7_sdk440_intr_transmit_boundaries_20261102 as boundaries
import prove_arm7_sdk441_defined_transmit_source_20261102 as defined_source
from project import ROOT,sha256,write_json
WORK=ROOT/'work/arm7-bulk-20261030/sdk436-intr-transmit-compiler1236'
REPORT=ROOT/'evidence/matches/arm7-sdk436-intr-transmit-compiler1236-20261102.json'
MUTATIONS={'TxqEndData':('pCounter->tx.success++;','pCounter->tx.success += 2;'),'DeleteTxFrames':('i < 3','i < 2'),'SetSupRateSet':('return len;','return len + 1;'),'CheckKeyTxEndMain':('u32 ret = 0;','u32 ret = 4;'),'SetSSIDElement':('return len;','return len + 1;'),'IsExistManFrame':('return 0 ;','return 1 ;'),'MacBugTxMp':('i = 100;','i = 99;')}

def worker(seed):
    row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['name']/'positive');return row,link

def main():
    pins_path=compiler.linker.PROFILE.parent/'generator-pins.json';pins=json.loads(pins_path.read_text(encoding='utf-8'))['files']
    for pin in pins:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Current complete source/compiler/profile closure changed:'+pin['path'])
    defined_source.main();boundaries.main();boundary=ROOT/'evidence/attempts/arm7-sdk440-intr-transmit-boundaries-20261102.json';seeds=json.loads(compiler.linker.PROFILE.read_text(encoding='utf-8'))['units'];matches=[];symbols={}
    with concurrent.futures.ProcessPoolExecutor(max_workers=2)as pool:compiled=list(pool.map(worker,seeds))
    for seed,(row,link)in zip(seeds,compiled):
        target=(ROOT/seed['binary']).read_bytes()[int(seed['address'],0)-seed['base']:int(seed['address'],0)-seed['base']+seed['bytes']];text=(ROOT/seed['source']).read_text(encoding='utf-8');text=re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:((ROOT/seed['source']).parent/m[1]).read_text(encoding='utf-8'),text);f=next(f for f in slicer.functions(text)if f['name']==seed['name']);fragment=text[f['start']:f['end']];old,new=MUTATIONS[seed['name']]
        if fragment.count(old)!=1:raise ValueError('Exact ordinary-C negative mutation missing:'+seed['name']+':'+old)
        bad,proof=diagnostic.build(dict(seed,address='0x26a0000'),text[:f['start']]+fragment.replace(old,new)+text[f['end']:],WORK/seed['name']/'wrong-source',link['bindings'])
        if bad==target:raise ValueError('Wrong ordinary C passed complete original byte gate')
        native_symbols={k:v['address']for k,v in link['bindings'].items()}
        for name,value in native_symbols.items():
            if name in symbols and symbols[name]!=value:raise ValueError('Conflicting measured symbol identities')
            symbols[name]=value
        row.update(realLink=link,nativeSymbols=native_symbols,nativeSymbolEntries=link['bindings'],exactBytes=True,exactAfterDeclaredRelocation=True,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,compilerOnlyEvidence=True,evidenceClass='function-matched-compiler-linker-only',behavioralQualification='not performed',actualOwnReturns=0,oracle=dict(vectors=0,actualOriginalAndCompiledReturns=0,actualDeclaredHelperReturns=0,actualSetupEntryReturns=0,providerReplacements=[],behavioralReturnCredit=0),wrongC=dict(mutation=[old,new],build=proof,linkedBytes=len(bad),byteGateRejected=True,actualOwnReturns=0,behavioralReturnCredit=0),boundaryProof=dict(path=boundary.relative_to(ROOT).as_posix(),sha256=sha256(boundary)),unrecoveredCalleesAndExtraDefinitionsCredit=0)
        matches.append(row);print(json.dumps(dict(name=seed['name'],bytes=seed['bytes'],exact=True,wrongCRejected=True,behavioralReturns=0)),flush=True)
    result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',romSha256=seeds[0]['romSha256'],matches=matches,nativeSymbols=symbols,matchedInitializedBytes=1236,newOrdinaryFunctionCount=7,compilerOnlyEvidence=True,evidenceClass='function-matched-compiler-linker-only',totalActualOwnReturns=0,totalActualDeclaredHelperReturns=0,totalActualSetupEntryReturns=0,totalWrongCActualReturns=0,wrongCByteGateRejections=len(matches),sourceInputsNoWorkCaches=True,sourceReconstructionComplete=False,wholeModuleLinked=False,initializedDenominatorDelta=0,originalCalleesAndAdditionalDefinitionsCredit=0,initializedRateTableSourceCredit=0,behavioralAndHardwareQualification='not performed',generatorSources=pins+[dict(path=pins_path.relative_to(ROOT).as_posix(),sha256=sha256(pins_path))]);write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),bytes=1236,functions=7,actualBehavioralReturns=0)),flush=True)

if __name__=='__main__':main()
