import ast
import json
import subprocess
from pathlib import Path
from project import ROOT,sha256,write_json

def main():
    names={'arm7_sdk248_rates180_native_20261101.py','compile_arm7_sdk249_rates180_20261101.py','match_arm7_sdk249_rates180_20261101.py','arm7_sdk250_parameters_native_20261101.py','compile_arm7_sdk251_parameters_20261101.py','link_arm7_sdk251_parameters_20261101.py','match_arm7_sdk251_parameters_20261101.py','validate_arm7_sdk252_rates_parameters400_20261101.py','prove_arm7_sdk253_rates_parameters_cold_20261101.py','evidence/matches/arm7-sdk249-rates180-20261101.json','evidence/matches/arm7-sdk251-parameters220-20261101.json','evidence/verification/arm7-sdk252-rates-parameters400-controls-20261101.json','evidence/verification/arm7-sdk253-rates-parameters400-cold-20261101.json','evidence/attempts/arm7-sdk249-rate-table-extent-correction-20261101.json','provenance/arm7-sdk252-rates-parameters-reference-20261101.json','docs/2026-11-01-arm7-rates-and-parameters400.md',Path(__file__).name}
    pins={}
    for label in('249-rates180','251-parameters220'):
        folder=ROOT/('nonmatching/arm7-bulk/20261101/lane-sdk'+label+'-final')
        for name in('profile.json','generator-pins.json'):names.add((folder/name).relative_to(ROOT).as_posix())
        for row in json.loads((folder/'generator-pins.json').read_text())['files']:pins[row['path']]=row['sha256']
        for unit in json.loads((folder/'profile.json').read_text())['units']:
            names.add(unit['source']);names.update(row['path']for row in unit['sourceDependencies'])
    for pin,digest in pins.items():
        if sha256(ROOT/pin)!=digest:raise ValueError('Frozen generator closure changed')
    pending=list(name for name in names if name.endswith('.py'));visited=set()
    while pending:
        name=pending.pop()
        if name in visited:continue
        visited.add(name);tree=ast.parse((ROOT/name).read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            modules=[a.name for a in node.names]if isinstance(node,ast.Import)else[node.module]if isinstance(node,ast.ImportFrom)and node.module else[]
            for module in modules:
                candidate=module.split('.')[0]+'.py'
                if(ROOT/candidate).is_file():
                    if candidate not in names and candidate not in pins:pins[candidate]=sha256(ROOT/candidate)
                    pending.append(candidate)
    for name in list(pins):
        tracked=subprocess.run(['git','ls-files','--error-unmatch','--',name],cwd=ROOT,capture_output=True).returncode==0
        if not tracked:names.add(name)
    for name in list(names):pins.pop(name,None)
    for name in names:
        if name.startswith('work/')or not(ROOT/name).is_file():raise ValueError('Transport must contain explicit source/evidence only')
    controls=json.loads((ROOT/'evidence/verification/arm7-sdk252-rates-parameters400-controls-20261101.json').read_text());path=ROOT/'provenance/arm7-sdk252-rates-parameters400-handoff-20261101.json'
    report=dict(schemaVersion=1,command='python validate_arm7_sdk252_rates_parameters400_20261101.py',files=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted(names)],existingPins=[dict(path=name,sha256=digest)for name,digest in sorted(pins.items())],matchedInitializedBytes=400,matchedCodeBytes=368,generatedLiteralBytes=32,newOrdinaryFunctionCount=4,actualOwnReturns=4792,actualFocusedNativeHelperReturns=11136,actualSetupEntryReturns=0,actualDescriptorPrefixFillReturns=648,separateInvalidPeriodActualReturns=4,constructorReturnCredit=0,additionalCDefinitionOrCalleeCredit=0,metadataControls=controls['metadataControlCount'],policyControls=controls['directPolicyControlCount'],nativeControls=controls['nativeControlCount'],sourceOnlyColdReplay=True,noWorkInputsTransported=True,registryPreferencesConfigAndAcceptedInputsChanged=False,initializedDenominatorDelta=0,wholeModuleAcceptancePending=True)
    write_json(path,report);print(json.dumps(dict(manifest=path.relative_to(ROOT).as_posix(),sha256=sha256(path),files=len(names),existingPins=len(pins))),flush=True)

if __name__=='__main__':main()
