import ast
import json
from pathlib import Path
import subprocess
from project import ROOT,sha256,write_json

def main():
    names={'link_arm7_sdk294_transmit_family_20261102.py','compile_arm7_sdk294_transmit_family_20261102.py','arm7_sdk295_transmit_family_native_20261102.py','match_arm7_sdk296_transmit_family_20261102.py','validate_arm7_sdk297_transmit_family_20261102.py','prove_arm7_sdk298_transmit_family_cold_20261102.py',Path(__file__).name,'evidence/matches/arm7-sdk296-transmit-family1600-20261102.json','evidence/verification/arm7-sdk297-transmit-family-controls-20261102.json','evidence/verification/arm7-sdk298-transmit-family-cold-20261102.json','docs/2026-11-02-arm7-transmit-family1600.md','provenance/arm7-sdk299-transmit-reference-20261102.json','evidence/verification/accepted-cohort133-identities-v2-20261102.json'};folder=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk294-transmit-family-final'
    names={p for p in names if p not in('evidence/verification/accepted-cohort133-identities-v2-20261102.json',)or(ROOT/p).exists()}
    if not any('accepted-cohort133' in p for p in names):names.add('evidence/verification/accepted-cohort133-identities-v2-20261101.json')
    pins={r['path']:r['sha256']for r in json.loads((folder/'generator-pins.json').read_text())['files']}
    for name in('profile.json','generator-pins.json'):names.add((folder/name).relative_to(ROOT).as_posix())
    for unit in json.loads((folder/'profile.json').read_text())['units']:names.add(unit['source']);names.update(d['path']for d in unit['sourceDependencies'])
    pending=[name for name in names if name.endswith('.py')];seen=set()
    while pending:
        name=pending.pop()
        if name in seen:continue
        seen.add(name)
        for node in ast.walk(ast.parse((ROOT/name).read_text(encoding='utf-8-sig'))):
            modules=[a.name for a in node.names]if isinstance(node,ast.Import)else[node.module]if isinstance(node,ast.ImportFrom)and node.module else[]
            for module in modules:
                candidate=module.split('.')[0]+'.py'
                if(ROOT/candidate).is_file():
                    if candidate not in names and candidate not in pins:pins[candidate]=sha256(ROOT/candidate)
                    pending.append(candidate)
    for name in list(pins):
        if sha256(ROOT/name)!=pins[name]:raise ValueError('Frozen runtime/source closure changed:'+name)
        if subprocess.run(['git','cat-file','-e','HEAD:'+name],cwd=ROOT,capture_output=True).returncode:names.add(name)
    for name in names:
        pins.pop(name,None)
        if name.startswith('work/')or not(ROOT/name).is_file():raise ValueError('Only direct source/profile/evidence files may be transported')
    for name in('evidence/attempts/arm7-sdk289-pspoll-callback104-scope-20261102.json','evidence/attempts/arm7-sdk290-pspoll-installation-20261102.json','evidence/verification/arm7-sdk291-pspoll-scope-controls-20261102.json','evidence/attempts/arm7-lane-setting-producer-20261031.json','extract/arm7/arm7.bin','extract/arm7/runtime/arm7-main.bin','extract/arm7/runtime/arm7-wram.bin','evidence/arm7/ghidra-runtime-inventory.json','inputs/game.nds','provenance/arm7-sdk142-full-parse-inputs-20261101.json'):pins[name]=sha256(ROOT/name)
    for row in json.loads((ROOT/'provenance/arm7-sdk299-transmit-reference-20261102.json').read_text())['referenceFiles']:pins[row['path']]=row['sha256']
    for unit in json.loads((folder/'profile.json').read_text())['units']:pins[unit['compiler']]=unit['compilerSha256']
    for name in('tools/mwccarm/mwccarm/2.0/base/mwldarm.exe','tools/mwccarm/mwccarm/license.dat'):pins[name]=sha256(ROOT/name)
    positive=json.loads((ROOT/'evidence/matches/arm7-sdk296-transmit-family1600-20261102.json').read_text());controls=json.loads((ROOT/'evidence/verification/arm7-sdk297-transmit-family-controls-20261102.json').read_text());cold=json.loads((ROOT/'evidence/verification/arm7-sdk298-transmit-family-cold-20261102.json').read_text())
    if not cold['sameCanonicalAndControlBytes']or cold['canonicalReportSha256']!=sha256(ROOT/'evidence/matches/arm7-sdk296-transmit-family1600-20261102.json'):raise ValueError('Complete unrelated-CWD source-only replay required')
    manifest=ROOT/'provenance/arm7-sdk299-transmit-family1600-handoff-20261102.json';write_json(manifest,dict(schemaVersion=1,command='python validate_arm7_sdk297_transmit_family_20261102.py',files=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted(names)],existingPins=[dict(path=name,sha256=digest)for name,digest in sorted(pins.items())],matchedInitializedBytes=1600,newOrdinaryFunctionCount=7,actualOwnReturns=positive['totalActualOwnReturns'],actualDeclaredNativeHelperReturns=positive['totalActualDeclaredHelperReturns'],actualSetupEntryReturns=positive['totalActualSetupEntryReturns'],wrongReturns=sum(r['actualOwnReturns']for r in positive['wrongC']),wrongModelRejections=sum(r['modelRejections']for r in positive['wrongC']),negativeControls=controls['negativeControlCount'],sourceOnlyColdReplay=True,sourceInputWorkCaches=False,originalCallbackAndTableSourceCredit=0,additionalCDefinitionsSourceCredit=0,initializedDenominatorDelta=0,sharedRegistryPreferencesConfigAndAcceptedInputsChanged=False,wholeModuleAcceptancePending=True,radioAndAndroidPortabilityUnproved=True));print(json.dumps(dict(manifest=manifest.relative_to(ROOT).as_posix(),sha256=sha256(manifest),files=len(names),existingPins=len(pins))),flush=True)

if __name__=='__main__':main()
