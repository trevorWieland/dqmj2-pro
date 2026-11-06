import ast
import json
import subprocess
from pathlib import Path
from project import ROOT,sha256,write_json

def main():
    profile=ROOT/'nonmatching/arm7-bulk/20261101/lane-sdk264-wireless-large-ready/profile.json';groups=json.loads(profile.read_text())['groups'];names={profile.relative_to(ROOT).as_posix(),'replay_arm7_sdk264_wireless_large_queue_20261101.py','validate_arm7_sdk264_wireless_large_queue_20261101.py','prove_arm7_sdk268_wireless_queue_cold_20261101.py','evidence/attempts/arm7-sdk264-wireless-large-ready-replay-20261101.json','evidence/verification/arm7-sdk264-wireless-large-queue-controls-20261101.json','evidence/verification/arm7-sdk268-wireless-large-cold-20261101.json','docs/2026-11-01-arm7-wireless-large-draft-queue.md',Path(__file__).name};pins={}
    for group in groups:
        for row in[dict(path=group['source'],sha256=group['sourceSha256']),*group['sourceDependencies']]:
            if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen compiler-ready source/include changed')
            names.add(row['path'])
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
        if subprocess.run(['git','ls-files','--error-unmatch','--',name],cwd=ROOT,capture_output=True).returncode:names.add(name)
    for name in names:
        pins.pop(name,None)
        if name.startswith('work/')or not(ROOT/name).is_file():raise ValueError('Only source/evidence/compiler profile may be transported')
    replay=json.loads((ROOT/'evidence/attempts/arm7-sdk264-wireless-large-ready-replay-20261101.json').read_text());path=ROOT/'provenance/arm7-sdk269-wireless-large-queue-handoff-20261101.json';report=dict(schemaVersion=1,command='python validate_arm7_sdk264_wireless_large_queue_20261101.py',files=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted(names)],existingPins=[dict(path=name,sha256=digest)for name,digest in sorted(pins.items())],closedSourceGroups=len(groups),sourceAndIncludeFiles=sum(1+len(g['sourceDependencies'])for g in groups),authoredDefinitionInstances=sum(g['selectedDefinitionCount']for g in groups),distinctDefinitionNames=len({name for g in groups for name in g['selectedDefinitionNames']}),candidateNativeRanges=replay['compileReadyTargetRanges'],candidateInitializedBytes=replay['qualifiedNativeBytes'],relocationMaskedEqualTargets=replay['relocationMaskedEqualTargets'],relocationMaskedEqualBytes=replay['relocationMaskedEqualBytes'],matchedInitializedBytes=0,newOrdinaryFunctionCount=0,sourceCredit=0,controlCount=9,sourceOnlyColdReplay=True,noWorkInputsTransported=True,registryPreferencesConfigAndAcceptedInputsChanged=False,allCompilerOutputsAreHypotheses=True,perFunctionAbiLinkNativeAndModuleGatesStillRequired=True);write_json(path,report);print(json.dumps(dict(manifest=path.relative_to(ROOT).as_posix(),sha256=sha256(path),files=len(names),pins=len(pins))),flush=True)

if __name__=='__main__':main()
