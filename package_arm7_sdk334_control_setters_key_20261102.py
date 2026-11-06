import ast
import json
from pathlib import Path
import subprocess
from project import ROOT,sha256,write_json

def main():
    names={'arm7_sdk327_control_setters_key_native_20261102.py','compile_arm7_sdk329_control_setters_key_20261102.py','link_arm7_sdk330_control_setters_key_20261102.py','match_arm7_sdk331_control_setters_key_20261102.py','validate_arm7_sdk332_control_setters_key_20261102.py','prove_arm7_sdk333_control_setters_key_cold_20261102.py','package_arm7_sdk334_control_setters_key_20261102.py','probe_arm7_sdk335_device_radio_context_limits_20261102.py','evidence/matches/arm7-sdk331-control-setters-key484-20261102.json','evidence/verification/arm7-sdk332-control-setters-key-controls-20261102.json','evidence/verification/arm7-sdk333-control-setters-key-cold-20261102.json','evidence/attempts/arm7-sdk335-device-radio-context-limits-20261102.json','evidence/attempts/arm7-sdk334-development-refusals-20261102.json','docs/2026-11-02-arm7-control-setters-key484.md','provenance/arm7-sdk334-control-setters-reference-20261102.json'};folder=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk328-control-setters-key-final';pins={p['path']:p['sha256']for p in json.loads((folder/'generator-pins.json').read_text())['files']};profile=json.loads((folder/'profile.json').read_text())
    for name in('profile.json','generator-pins.json'):names.add((folder/name).relative_to(ROOT).as_posix())
    for unit in profile['units']:names.add(unit['source']);names.update(d['path']for d in unit['sourceDependencies']);names.add(unit['authoritativeExclusionSnapshot']['path'])
    pending=[n for n in names if n.endswith('.py')];seen=set()
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
    for name,digest in list(pins.items()):
        if sha256(ROOT/name)!=digest:raise ValueError('Current complete source/runtime input differs:'+name)
        if name.endswith('.py')and subprocess.run(['git','cat-file','-e','HEAD:'+name],cwd=ROOT,capture_output=True).returncode:names.add(name)
    for name in names:
        pins.pop(name,None)
        if name.startswith('work/')or not(ROOT/name).is_file():raise ValueError('Only source/profile/provenance/evidence files may be transported')
    for row in json.loads((ROOT/'provenance/arm7-sdk334-control-setters-reference-20261102.json').read_text())['referenceFiles']:pins[row['path']]=row['sha256']
    positive=json.loads((ROOT/'evidence/matches/arm7-sdk331-control-setters-key484-20261102.json').read_text());controls=json.loads((ROOT/'evidence/verification/arm7-sdk332-control-setters-key-controls-20261102.json').read_text());cold=json.loads((ROOT/'evidence/verification/arm7-sdk333-control-setters-key-cold-20261102.json').read_text())
    if not cold['sameCanonicalAndControlBytes']or cold['canonicalReportSha256']!=sha256(ROOT/'evidence/matches/arm7-sdk331-control-setters-key484-20261102.json')or cold['controlsSha256']!=sha256(ROOT/'evidence/verification/arm7-sdk332-control-setters-key-controls-20261102.json'):raise ValueError('Terminal complete source-only unrelated-CWD replay required')
    manifest=ROOT/'provenance/arm7-sdk334-control-setters-key484-handoff-20261102.json';write_json(manifest,dict(schemaVersion=1,command='python validate_arm7_sdk332_control_setters_key_20261102.py',files=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted(names)],existingPins=[dict(path=name,sha256=digest)for name,digest in sorted(pins.items())],matchedInitializedBytes=484,newOrdinaryFunctionCount=3,actualOwnReturns=positive['totalActualOwnReturns'],actualDeclaredNativeHelperReturns=positive['totalActualDeclaredHelperReturns'],actualSetupEntryReturns=positive['totalActualSetupEntryReturns'],wrongReturns=sum(r['actualOwnReturns']for r in positive['wrongC']),wrongModelRejections=sum(r['modelRejections']for r in positive['wrongC']),negativeControls=controls['negativeControlCount'],sourceOnlyColdReplay=True,sourceInputWorkCaches=False,originalTablesAndAdditionalDefinitionsSourceCredit=0,initializedDenominatorDelta=0,originalOnlyDeviceProbe='python probe_arm7_sdk335_device_radio_context_limits_20261102.py',originalOnlyDeviceProbeSourceCredit=0,sharedRegistryPreferencesConfigAndAcceptedInputsChanged=False,wholeModuleAcceptancePending=True,radioAndAndroidPortabilityUnproved=True));print(json.dumps(dict(manifest=manifest.relative_to(ROOT).as_posix(),sha256=sha256(manifest),files=len(names),existingPins=len(pins))),flush=True)

if __name__=='__main__':main()
