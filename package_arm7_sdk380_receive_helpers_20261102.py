import ast
import json
from pathlib import Path
import subprocess
from project import ROOT,sha256,write_json


def main():
    folder=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk373-receive-helpers-final';pins={p['path']:p['sha256']for p in json.loads((folder/'generator-pins.json').read_text())['files']};profile=json.loads((folder/'profile.json').read_text());names={'arm7_sdk371_receive_native_20261102.py','arm7_sdk372_receive_helpers_native_20261102.py','link_arm7_sdk374_receive_helpers_20261102.py','compile_arm7_sdk375_receive_helpers_20261102.py','match_arm7_sdk376_receive_helpers_20261102.py','validate_arm7_sdk377_receive_helpers_20261102.py','prove_arm7_sdk378_receive_helpers_cold_20261102.py','package_arm7_sdk380_receive_helpers_20261102.py','evidence/matches/arm7-sdk376-receive-helpers1092-20261102.json','evidence/verification/arm7-sdk377-receive-helpers-controls-20261102.json','evidence/verification/arm7-sdk378-receive-helpers-cold-20261102.json','evidence/attempts/arm7-sdk371-ssid-model-correction-20261102.json','docs/2026-11-02-arm7-receive-helpers1092.md','provenance/arm7-sdk380-receive-helpers-reference-20261102.json'}
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
    for row in json.loads((ROOT/'provenance/arm7-sdk380-receive-helpers-reference-20261102.json').read_text())['referenceFiles']:pins[row['path']]=row['sha256']
    report=ROOT/'evidence/matches/arm7-sdk376-receive-helpers1092-20261102.json';controls=ROOT/'evidence/verification/arm7-sdk377-receive-helpers-controls-20261102.json';positive=json.loads(report.read_text());negative=json.loads(controls.read_text());cold=json.loads((ROOT/'evidence/verification/arm7-sdk378-receive-helpers-cold-20261102.json').read_text())
    if not cold['sameCanonicalAndControlBytes']or cold['canonicalReportSha256']!=sha256(report)or cold['controlsSha256']!=sha256(controls):raise ValueError('Terminal empty-WORK unrelated-CWD source-only proof required')
    manifest=ROOT/'provenance/arm7-sdk380-receive-helpers1092-handoff-20261102.json';write_json(manifest,dict(schemaVersion=1,command='python validate_arm7_sdk377_receive_helpers_20261102.py',files=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted(names)],existingPins=[dict(path=name,sha256=digest)for name,digest in sorted(pins.items())],matchedInitializedBytes=1092,newOrdinaryFunctionCount=5,actualOwnReturns=positive['totalActualOwnReturns'],actualDeclaredNativeHelperReturns=positive['totalActualDeclaredHelperReturns'],actualSetupEntryReturns=positive['totalActualSetupEntryReturns'],wrongReturns=positive['totalWrongCActualReturns'],wrongModelRejections=positive['totalWrongCModelRejections'],negativeControls=negative['negativeControlCount'],sourceOnlyColdReplay=True,sourceInputWorkCaches=False,originalCalleesAndAdditionalDefinitionsCredit=0,initializedDenominatorDelta=0,unsupportedSourceCredit=0,sharedRegistryPreferencesConfigAndAcceptedInputsChanged=False,wholeModuleAcceptancePending=True,physicalRadioTimerDispatchAndAndroidUnproved=True));print(json.dumps(dict(manifest=manifest.relative_to(ROOT).as_posix(),sha256=sha256(manifest),files=len(names),existingPins=len(pins))),flush=True)

if __name__=='__main__':main()
