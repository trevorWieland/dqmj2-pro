import ast
import json
from pathlib import Path
import subprocess
from project import ROOT,sha256,write_json


def main():
    folder=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk420-beacon-probe-key-final';pins={p['path']:p['sha256']for p in json.loads((folder/'generator-pins.json').read_text())['files']};profile=json.loads((folder/'profile.json').read_text());names={'arm7_sdk417_mp_key_native_20261102.py','arm7_sdk418_probe_response_native_20261102.py','arm7_sdk419_beacon_native_20261102.py','link_arm7_sdk421_beacon_probe_key_20261102.py','compile_arm7_sdk422_beacon_probe_key_20261102.py','match_arm7_sdk423_beacon_probe_key_20261102.py','validate_arm7_sdk424_beacon_probe_key_20261102.py','prove_arm7_sdk425_beacon_probe_key_cold_20261102.py','package_arm7_sdk426_beacon_probe_key_20261102.py','provenance/arm7-sdk426-beacon-probe-key-reference-20261102.json','docs/2026-11-02-arm7-beacon-probe-key3016.md','evidence/matches/arm7-sdk423-beacon-probe-key3016-20261102.json','evidence/verification/arm7-sdk424-beacon-probe-key-controls-20261102.json','evidence/verification/arm7-sdk425-beacon-probe-key-cold-20261102.json'}
    names.add('evidence/attempts/arm7-sdk426-frozen-eof-transport-20261102.json')
    names.update({'prove_arm7_sdk426_failed_models_20261102.py','provenance/arm7-sdk426-failed-models-20261102.json','evidence/attempts/arm7-sdk426-failed-model-replay-20261102.json','nonmatching/arm7-bulk/20261102/lane-sdk426-historical-models/failed_floor_model.py.gz','nonmatching/arm7-bulk/20261102/lane-sdk426-historical-models/failed_span180_model.py.gz','evidence/attempts/arm7-sdk417-mp-key-model-correction-20261102.json','evidence/attempts/arm7-sdk417-mp-key-output-span-correction-20261102.json'})
    names.update((folder/n).relative_to(ROOT).as_posix()for n in('profile.json','generator-pins.json'))
    for unit in profile['units']:names.add(unit['source']);names.update(d['path']for d in unit['sourceDependencies']);names.add(unit['authoritativeExclusionSnapshot']['path'])
    snapshot=ROOT/profile['units'][0]['authoritativeExclusionSnapshot']['path'];accepted=json.loads(snapshot.read_text())['functions'];number=lambda v:int(v,0)if isinstance(v,str)else v;identity=lambda r:(r['processor'],r.get('program',''),r['module'],r['mode'],number(r['address']));selected={identity(r)for r in accepted}
    if any(identity(r)in selected for r in profile['units']):raise ValueError('Current accepted qualified identity conflict')
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
        if sha256(ROOT/name)!=digest:raise ValueError('Complete source/runtime/compiler input changed:'+name)
        if not name.startswith(('tools/','inputs/','extract/','deps/'))and subprocess.run(['git','cat-file','-e','HEAD:'+name],cwd=ROOT,capture_output=True).returncode:names.add(name)
    for name in names:
        pins.pop(name,None)
        if name.startswith('work/')or not(ROOT/name).is_file():raise ValueError('Only source/profile/provenance/evidence transport allowed')
    for row in json.loads((ROOT/'provenance/arm7-sdk426-beacon-probe-key-reference-20261102.json').read_text())['referenceFiles']:pins[row['path']]=row['sha256']
    report=ROOT/'evidence/matches/arm7-sdk423-beacon-probe-key3016-20261102.json';controls=ROOT/'evidence/verification/arm7-sdk424-beacon-probe-key-controls-20261102.json';positive=json.loads(report.read_text());negative=json.loads(controls.read_text());cold=json.loads((ROOT/'evidence/verification/arm7-sdk425-beacon-probe-key-cold-20261102.json').read_text())
    if not cold['sameCanonicalAndControlBytes']or cold['canonicalReportSha256']!=sha256(report)or cold['controlsSha256']!=sha256(controls):raise ValueError('Terminal empty-WORK unrelated-CWD source-only proof required')
    manifest=ROOT/'provenance/arm7-sdk426-beacon-probe-key3016-handoff-20261102.json';write_json(manifest,dict(schemaVersion=1,command='python validate_arm7_sdk424_beacon_probe_key_20261102.py',files=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted(names)],existingPins=[dict(path=name,sha256=digest)for name,digest in sorted(pins.items())],matchedInitializedBytes=3016,newOrdinaryFunctionCount=3,actualOwnReturns=positive['totalActualOwnReturns'],actualDeclaredNativeHelperReturns=positive['totalActualDeclaredHelperReturns'],actualSetupEntryReturns=positive['totalActualSetupEntryReturns'],wrongReturns=positive['totalWrongCActualReturns'],wrongModelRejections=positive['totalWrongCModelRejections'],negativeControls=negative['negativeControlCount'],sourceOnlyColdReplay=True,sourceInputWorkCaches=False,originalCalleesAndAdditionalDefinitionsCredit=0,initializedDenominatorDelta=0,unsupportedSourceCredit=0,sharedRegistryPreferencesConfigAndAcceptedInputsChanged=False,wholeModuleAcceptancePending=True,physicalRadioTimerDispatchAndAndroidUnproved=True));print(json.dumps(dict(manifest=manifest.relative_to(ROOT).as_posix(),sha256=sha256(manifest),files=len(names),existingPins=len(pins))),flush=True)

if __name__=='__main__':main()
