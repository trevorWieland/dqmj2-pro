import ast
import json
import subprocess
from pathlib import Path
from project import ROOT,sha256,write_json

def main():
    names={'arm7_sdk262_element804_native_20261101.py','prove_arm7_sdk262_element804_native_20261101.py','compile_arm7_sdk263_element804_20261101.py','link_arm7_sdk263_element804_20261101.py','match_arm7_sdk263_element804_20261101.py','validate_arm7_sdk265_element804_20261101.py','prove_arm7_sdk266_element804_cold_20261101.py','evidence/attempts/arm7-sdk262-element804-native-20261101.json','evidence/matches/arm7-sdk263-element804-20261101.json','evidence/verification/arm7-sdk265-element804-controls-20261101.json','evidence/verification/arm7-sdk266-element804-cold-20261101.json','docs/2026-11-01-arm7-element804.md',Path(__file__).name};folder=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk263-element804-final';pins={r['path']:r['sha256']for r in json.loads((folder/'generator-pins.json').read_text())['files']}
    names.add('provenance/arm7-sdk267-element-reference-20261101.json')
    for name in('profile.json','generator-pins.json'):names.add((folder/name).relative_to(ROOT).as_posix())
    for unit in json.loads((folder/'profile.json').read_text())['units']:
        names.add(unit['source']);names.update(row['path']for row in unit['sourceDependencies'])
    for pin,digest in pins.items():
        if sha256(ROOT/pin)!=digest:raise ValueError('Frozen current generator closure changed')
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
    for name in list(pins):
        if subprocess.run(['git','ls-files','--error-unmatch','--',name],cwd=ROOT,capture_output=True).returncode:names.add(name)
    for name in names:
        pins.pop(name,None)
        if name.startswith('work/')or not(ROOT/name).is_file():raise ValueError('Only explicit source/evidence may be transported')
    controls=json.loads((ROOT/'evidence/verification/arm7-sdk265-element804-controls-20261101.json').read_text());manifest=ROOT/'provenance/arm7-sdk267-element804-handoff-20261101.json';report=dict(schemaVersion=1,command='python validate_arm7_sdk265_element804_20261101.py',files=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted(names)],existingPins=[dict(path=name,sha256=digest)for name,digest in sorted(pins.items())],matchedInitializedBytes=804,matchedCodeBytes=800,generatedLiteralBytes=4,newOrdinaryFunctionCount=1,actualOwnReturns=5192,actualFocusedNativeHelperReturns=12360,actualSetupEntryReturns=0,actualDescriptorPrefixFillReturns=5192,constructorReturnCredit=0,additionalCDefinitionOrCalleeCredit=0,metadataControls=controls['metadataControlCount'],policyControls=controls['directPolicyControlCount'],nativeControls=controls['nativeControlCount'],sourceScopeControls=controls['sourceScopeControlCount'],oddCfpRawNativeContextsWithheldFromSourceScope=36,completeSupportedPathReconstruction=False,sourceOnlyColdReplay=True,noWorkInputsTransported=True,registryPreferencesConfigAndAcceptedInputsChanged=False,initializedDenominatorDelta=0,wholeModuleAcceptancePending=True);write_json(manifest,report);print(json.dumps(dict(manifest=manifest.relative_to(ROOT).as_posix(),sha256=sha256(manifest),files=len(names),existingPins=len(pins))),flush=True)

if __name__=='__main__':main()
