import ast
import json
from pathlib import Path
import subprocess
from project import ROOT,sha256,write_json

def main():
    names={'arm7_sdk356_measure_task_native_20261102.py','compile_arm7_sdk364_measure_task_20261102.py','link_arm7_sdk363_measure_task_20261102.py','match_arm7_sdk365_measure_task_20261102.py','validate_arm7_sdk366_measure_task_20261102.py','prove_arm7_sdk367_measure_task_cold_20261102.py','prove_arm7_sdk369_unsigned_division_entry_abi_20261102.py','package_arm7_sdk368_measure_task_20261102.py','evidence/matches/arm7-sdk365-measure-task624-20261102.json','evidence/verification/arm7-sdk366-measure-task-controls-20261102.json','evidence/verification/arm7-sdk367-measure-task-cold-20261102.json','evidence/attempts/arm7-sdk356-measure-task-native-20261102.json','evidence/attempts/arm7-sdk369-unsigned-division-entry-abi-20261102.json','evidence/attempts/arm7-sdk368-accepted141-exclusion-audit-20261102.json','evidence/attempts/arm7-sdk368-development-refusals-20261102.json','docs/2026-11-02-arm7-channel-measurement624.md','provenance/arm7-sdk368-measure-task-reference-20261102.json'};folder=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk362-measure-task-final';pins={p['path']:p['sha256']for p in json.loads((folder/'generator-pins.json').read_text())['files']};profile=json.loads((folder/'profile.json').read_text())
    for name in('profile.json','generator-pins.json'):names.add((folder/name).relative_to(ROOT).as_posix())
    for unit in profile['units']:names.add(unit['source']);names.update(d['path']for d in unit['sourceDependencies']);names.add(unit['authoritativeExclusionSnapshot']['path'])
    audit=json.loads((ROOT/'evidence/attempts/arm7-sdk368-accepted141-exclusion-audit-20261102.json').read_text());names.add(audit['snapshot'])
    if audit['duplicates']:raise ValueError('Current accepted identity conflict')
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
    for row in json.loads((ROOT/'provenance/arm7-sdk368-measure-task-reference-20261102.json').read_text())['referenceFiles']:pins[row['path']]=row['sha256']
    positive=json.loads((ROOT/'evidence/matches/arm7-sdk365-measure-task624-20261102.json').read_text());controls=json.loads((ROOT/'evidence/verification/arm7-sdk366-measure-task-controls-20261102.json').read_text());cold=json.loads((ROOT/'evidence/verification/arm7-sdk367-measure-task-cold-20261102.json').read_text())
    if not cold['sameCanonicalAndControlBytes']or cold['canonicalReportSha256']!=sha256(ROOT/'evidence/matches/arm7-sdk365-measure-task624-20261102.json')or cold['controlsSha256']!=sha256(ROOT/'evidence/verification/arm7-sdk366-measure-task-controls-20261102.json'):raise ValueError('Terminal complete source-only unrelated-CWD replay required')
    manifest=ROOT/'provenance/arm7-sdk368-measure-task624-handoff-20261102.json';write_json(manifest,dict(schemaVersion=1,command='python validate_arm7_sdk366_measure_task_20261102.py',files=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted(names)],existingPins=[dict(path=name,sha256=digest)for name,digest in sorted(pins.items())],matchedInitializedBytes=624,newOrdinaryFunctionCount=1,actualOwnReturns=positive['totalActualOwnReturns'],actualDeclaredNativeHelperReturns=positive['totalActualDeclaredHelperReturns'],actualSetupEntryReturns=positive['totalActualSetupEntryReturns'],wrongReturns=positive['wrongC']['actualOwnReturns'],wrongModelRejections=positive['wrongC']['modelRejections'],negativeControls=controls['negativeControlCount'],sourceOnlyColdReplay=True,sourceInputWorkCaches=False,originalTablesAndAdditionalDefinitionsSourceCredit=0,initializedDenominatorDelta=0,unsupportedOriginalContexts=48,unsupportedSourceCredit=0,additionalCallbackAndArithmeticHelperCredit=0,generatedHelperAbiCharacterization='python prove_arm7_sdk369_unsigned_division_entry_abi_20261102.py',sharedRegistryPreferencesConfigAndAcceptedInputsChanged=False,wholeModuleAcceptancePending=True,radioAndAndroidPortabilityUnproved=True));print(json.dumps(dict(manifest=manifest.relative_to(ROOT).as_posix(),sha256=sha256(manifest),files=len(names),existingPins=len(pins))),flush=True)

if __name__=='__main__':main()
