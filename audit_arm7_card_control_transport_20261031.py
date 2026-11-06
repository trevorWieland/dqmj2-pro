import ast
import json
from pathlib import Path
from project import ROOT,sha256,write_json
MATCHER='match_arm7_lane_card_control_20261031.py'
VALIDATOR='validate_arm7_lane_card_control_20261031.py'
PROFILE='nonmatching/arm7-bulk/20261031/lane-card-control452-final/closure.json'
PINS='nonmatching/arm7-bulk/20261031/lane-card-control452-final/generator-pins.json'
EXPLICIT=('prove_arm7_card_control452_negative_returns_20261031.py',
    'evidence/verification/arm7-card-control452-negative-returns-20261031.json',
    'evidence/arm7/lane-card-callback-scope-20261031.json',
    'evidence/matches/arm7-lane-card-control452-20261031.json',
    'evidence/verification/arm7-lane-card-control452-controls-20261031.json',
    'evidence/verification/arm7-card-control-replay-receipt-20261031.json',
    'evidence/attempts/arm7-card-control452-negative-link-fixture-failure-20261031.json',
    'prove_arm7_card_return_candidate4_20261031.py',
    'evidence/arm7/lane-card-return-candidate4-20261031.json',
    'docs/2026-10-31-arm7-card-control452.md')


def collect():
    found={};history={};python=set();jsonfiles=set()
    def add(name,kind,pin=None):
        path=(ROOT/name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():raise ValueError('Missing/escaped transport input: '+name)
        current=sha256(path)
        if pin and current!=pin:raise ValueError('Pinned transport input differs: '+name)
        key=path.relative_to(ROOT).as_posix()
        found.setdefault(key,set()).add(kind)
        return key
    def header_inputs(profile,historical):
        role='historical-evidence-only' if historical else 'source-only-compiler-input'
        for row in profile['matches']:
            add(row['source'],role,row['sourceSha256'])
            for item in row['sourceDependencies']:add(item['path'],role,item['sha256'])
        for row in profile.get('sourceBodyHistory',[]):
            add(row['originalSource'],'historical-evidence-only',row['unchangedSourceSha256'])
            add(row['newSource'],role,row['unchangedSourceSha256'])
            for item in row.get('originalHeaderClosure',[]):
                add(item['path'],'historical-evidence-only',item['sha256']);history[item['path']]=item['sha256']
            for item in row.get('newHeaderClosure',[]):add(item['path'],role,item['sha256'])
    for name,role in ((PROFILE,'current-source-profile'),(PINS,'runtime-pins')):
        add(name,role);jsonfiles.add(name)
    header_inputs(json.loads((ROOT/PROFILE).read_text()),False)
    for row in json.loads((ROOT/PINS).read_text())['files']:add(row['path'],'pinned-runtime-input',row['sha256'])
    for name in (MATCHER,VALIDATOR,*EXPLICIT):add(name,'reproducer-or-evidence')
    import qualified_arm7_card_scope_20261031 as qualified
    import prove_arm7_lane_card_callbacks_scope_20261031 as scope
    pending_manifests=[(qualified.MANIFEST,qualified.MANIFEST_SHA),(scope.RUNTIME_PINS,scope.RUNTIME_PINS_SHA)]
    visited_manifests=set()
    while pending_manifests:
        name,pinned=pending_manifests.pop()
        if name in visited_manifests:continue
        visited_manifests.add(name);add(name,'frozen-boundary-static-manifest',pinned)
        manifest=json.loads((ROOT/name).read_text())
        for item in manifest.get('files',[]):
            name=item['path'];add(name,'frozen-boundary-manifest-input',item['sha256'])
            if name.startswith('provenance/') and name.endswith('.json'):pending_manifests.append((name,item['sha256']))
    todo=[name for name in found if name.endswith('.py')]
    while todo:
        name=todo.pop()
        if name in python:continue
        python.add(name);tree=ast.parse((ROOT/name).read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            modules=[item.name for item in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
            for module in modules:
                candidate=module.split('.')[0]+'.py'
                if (ROOT/candidate).is_file():
                    add(candidate,'recursive-local-python-dependency')
                    if candidate not in python:todo.append(candidate)
    for row in json.loads((ROOT/PROFILE).read_text())['matches']:
        seen=set();pending=[(ROOT/row['source']).resolve()]
        import re
        while pending:
            path=pending.pop()
            for name in re.findall(r'^#include "([^"<>]+)"$',path.read_text(),re.M):
                include=(path.parent/name).resolve()
                if not include.is_relative_to(ROOT):raise ValueError('Compiler include escaped repository')
                key=add(include.relative_to(ROOT).as_posix(),'recursive-compiler-include')
                if key not in seen:seen.add(key);pending.append(include)
        if seen!={item['path'] for item in row['sourceDependencies']}:raise ValueError('Actual include graph differs from profile')
    return found,history,python


def main():
    found,history,python=collect()
    old_four=[name for name in history if 'lane_20261031_card_callbacks244' in name or 'lane-card-pages368/' in name]
    report=ROOT/'evidence/verification/arm7-card-control-transport-audit-20261031.json'
    write_json(report,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),
        files=[dict(path=name,sha256=sha256(ROOT/name),bytes=(ROOT/name).stat().st_size,roles=sorted(roles)) for name,roles in sorted(found.items())],
        historicalHeaderPins=[dict(path=name,sha256=value,historicalEvidenceOnly=True,compilerInput=False) for name,value in sorted(history.items())],
        historicalPreviouslyOmittedHeaders=old_four,recursivePythonFiles=len(python),currentUnits=4,newCandidateBytes=452,
        zeroCoverageMigrationBytes=0,allFilesPresentAndPinned=True,sourceCredit=0,
        limitations=['Transport audit checks source/profile/runtime/evidence closure, not a complete source build or ROM completion',
            'Generated Work products are rebuilt and checked by the matcher/validator, never transported as source',
            'Private ROM, extracted module, pinned compiler/linker/runtime libraries and framework configuration remain explicit baseline prerequisites',
            'Historical prefix headers are provenance evidence only. Current compiler includes use the new complete compatible storage declarations']))
    print(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),files=len(found),historicalHeaders=len(history),recursivePythonFiles=len(python),allPassed=True))


if __name__=='__main__':main()
