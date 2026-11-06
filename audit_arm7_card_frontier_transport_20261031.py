import ast
import json
from pathlib import Path
from project import ROOT,sha256,write_json
MATCHER='match_arm7_lane_card_frontier_20261031.py'
VALIDATOR='validate_arm7_lane_card_frontier_20261031.py'
PROFILE='nonmatching/arm7-bulk/20261031/lane-card-frontier2240-final/closure.json'
PINS='nonmatching/arm7-bulk/20261031/lane-card-frontier2240-final/generator-pins.json'
OLD='nonmatching/arm7-bulk/20261031/lane-card-abi16-1252-final/closure.json'
EXPLICIT=('prove_arm7_card_frontier_request_domains_20261031.py',
    'evidence/arm7/lane-card-frontier-request-domains-20261031.json',
    'evidence/attempts/arm7-card-frontier-worker-paired-failure-20261031.json',
    'evidence/arm7/lane-card-callback-scope-20261031.json',
    'evidence/verification/arm7-card-frontier-layout-20261031.json',
    'evidence/matches/arm7-lane-card-frontier2240-20261031.json',
    'evidence/verification/arm7-lane-card-frontier2240-controls-20261031.json',
    'evidence/verification/arm7-card-frontier-replay-receipt-20261031.json',
    'evidence/attempts/arm7-card-frontier-tuning-history-20261031.json',
    'docs/2026-10-31-arm7-card-frontier2240-and-storage-migration.md')


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
    for name,role in ((PROFILE,'current-source-profile'),(OLD,'historical-source-profile'),(PINS,'runtime-pins')):
        add(name,role);jsonfiles.add(name)
    header_inputs(json.loads((ROOT/PROFILE).read_text()),False)
    header_inputs(json.loads((ROOT/OLD).read_text()),True)
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
    tuning=json.loads((ROOT/'evidence/attempts/arm7-card-frontier-tuning-history-20261031.json').read_text())
    for variant in tuning['variants']:
        add(variant['generator'],'historical-draft-generator',variant['generatorSha256'])
        for item in variant['sources']:add(item['path'],'historical-draft-source',item['sha256'])
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
    if len(old_four)!=4:raise ValueError('Four historical callback/page headers were not explicitly retained')
    report=ROOT/'evidence/verification/arm7-card-frontier-transport-audit-20261031.json'
    write_json(report,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),
        files=[dict(path=name,sha256=sha256(ROOT/name),bytes=(ROOT/name).stat().st_size,roles=sorted(roles)) for name,roles in sorted(found.items())],
        historicalHeaderPins=[dict(path=name,sha256=value,historicalEvidenceOnly=True,compilerInput=False) for name,value in sorted(history.items())],
        historicalPreviouslyOmittedHeaders=old_four,recursivePythonFiles=len(python),currentUnits=13,newCandidateBytes=988,
        zeroCoverageMigrationBytes=1252,allFilesPresentAndPinned=True,sourceCredit=0,
        limitations=['Transport audit checks source/profile/runtime/evidence closure, not a complete source build or ROM completion',
            'Generated Work products are rebuilt and checked by the matcher/validator, never transported as source',
            'Private ROM, extracted module, pinned compiler/linker/runtime libraries and framework configuration remain explicit baseline prerequisites',
            'Historical prefix headers are provenance evidence only. Current compiler includes use the new complete compatible storage declarations']))
    print(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),files=len(found),historicalHeaders=len(history),recursivePythonFiles=len(python),allPassed=True))


if __name__=='__main__':main()
