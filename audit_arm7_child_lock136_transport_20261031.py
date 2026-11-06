import ast
import json
import re
from pathlib import Path
from project import ROOT,sha256,write_json
PROFILE='nonmatching/arm7-bulk/20261031/lane-child-lock-initializer136-final/closure.json'
PINS='nonmatching/arm7-bulk/20261031/lane-child-lock-initializer136-final/generator-pins.json'
EXPLICIT=('match_arm7_child_lock_initializer136_20261031.py','validate_arm7_child_lock_initializer136_20261031.py',
    'evidence/matches/arm7-child-lock-initializer136-20261031.json','evidence/verification/arm7-child-lock-initializer136-controls-20261031.json',
    'evidence/verification/arm7-child-lock136-replay-receipt-20261031.json','docs/2026-10-31-arm7-child-lock-initializer136.md')


def collect():
    found={};python=set()
    def add(name,role,pin=None):
        path=(ROOT/name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():raise ValueError('Missing/escaped priority transport input: '+str(name))
        if pin and sha256(path)!=pin:raise ValueError('Changed priority transport input: '+str(name))
        found.setdefault(path.relative_to(ROOT).as_posix(),set()).add(role)
    add(PROFILE,'source-profile');add(PINS,'runtime-pins')
    profile=json.loads((ROOT/PROFILE).read_text())
    for row in profile['matches']:
        add(row['source'],'source-only-compiler-input',row['sourceSha256'])
        for item in row['sourceDependencies']:add(item['path'],'source-only-compiler-input',item['sha256'])
    history=(
        'nonmatching/arm7-bulk/20261031/lane-lock-bitmaps692-v1/utility-child-arm7-wram/native_utility_child_arm7_wram_037fc0b8.c',
        'nonmatching/arm7-bulk/20261031/lane-lock-bitmaps692-v1/native_lock_types.h',
        'nonmatching/arm7-bulk/20261031/lane-lock-initializers252-context-v2/utility-child-arm7-wram/native_utility_child_arm7_wram_037fc0b8-split-bitmap-words.c',
        'nonmatching/arm7-bulk/20261031/lane-lock-initializers252-context-v2/native_lock_types.h',
        'nonmatching/arm7-bulk/20261031/lane-lock-child-init136-order-v3/utility-child-arm7-wram/native_utility_child_arm7_wram_037fc0b8-direct-first-extension.c',
        'nonmatching/arm7-bulk/20261031/lane-lock-child-init136-order-v3/native_lock_types.h',
        'nonmatching/arm7-bulk/20261031/lane-lock-initializers252-static-v4/utility-child-arm7-wram/native_utility_child_arm7_wram_037fc0b8-extern-original.c',
        'nonmatching/arm7-bulk/20261031/lane-lock-initializers252-static-v4/native_lock_types.h',
        'evidence/attempts/arm7-constructor-lock-id-correction-20261031.json',
        'evidence/attempts/arm7-lock-region-v2-import-order-20261031.json',
        'evidence/attempts/arm7-lock-doc-encoding-failure-20261031.json',
        'evidence/attempts/arm7-child-lock136-ignored-reference-packaging-20261031.json')
    for name in history:add(name,'historical-unaccepted-zero-credit-hypothesis')
    reference='evidence/research/20261031-arm7-lane-os-reference-source.json';add(reference,'reference-only-git-manifest')
    manifest=json.loads((ROOT/reference).read_text());add(manifest['generator'],'reference-only-fetcher',manifest['generatorSha256'])
    import hashlib
    for item in manifest['files']:
        add(item['localPath'],'unmodified-third-party-reference-not-compiler-input',item['sha256']);data=(ROOT/item['localPath']).read_bytes()
        if len(data)!=item['bytes'] or hashlib.sha1(b'blob '+str(len(data)).encode()+bytes(1)+data).hexdigest()!=item['gitBlobSha1']:raise ValueError('Reference Git blob/length verification differs')
    for item in json.loads((ROOT/PINS).read_text())['files']:add(item['path'],'pinned-runtime-input',item['sha256'])
    for name in EXPLICIT:add(name,'reproducer-or-evidence')
    pending=[name for name in found if name.endswith('.py')]
    while pending:
        name=pending.pop()
        if name in python:continue
        python.add(name)
        for node in ast.walk(ast.parse((ROOT/name).read_text(encoding='utf-8-sig'))):
            modules=[x.name for x in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
            for module in modules:
                child=module.split('.')[0]+'.py'
                if (ROOT/child).is_file():
                    add(child,'recursive-python-dependency')
                    if child not in python:pending.append(child)
    for row in profile['matches']:
        seen=set();pending=[ROOT/row['source']]
        while pending:
            path=pending.pop()
            for name in re.findall(r'^#include "([^"<>]+)"$',path.read_text(),re.M):
                include=(path.parent/name).resolve();key=include.relative_to(ROOT).as_posix();add(key,'recursive-compiler-include')
                if key not in seen:seen.add(key);pending.append(include)
        if seen!={p['path'] for p in row['sourceDependencies']}:raise ValueError('Priority include graph differs')
    return found,python


def main():
    files,python=collect();output=ROOT/'evidence/verification/arm7-child-lock136-transport-audit-20261031.json'
    write_json(output,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),
        files=[dict(path=name,sha256=sha256(ROOT/name),bytes=(ROOT/name).stat().st_size,roles=sorted(roles)) for name,roles in sorted(files.items())],
        recursivePythonFiles=len(python),currentUnits=1,newCandidateBytes=136,zeroCoverageMigrationBytes=0,sourceCredit=0,allPassed=True,
        limitations=['Generated Work products must be freshly regenerated and validated','Private pinned original ROM/modules/compiler/runtime are explicit baseline prerequisites','Historical hypotheses are not compiler inputs or accepted source credit']))
    print(dict(report=output.relative_to(ROOT).as_posix(),sha256=sha256(output),files=len(files),allPassed=True))


if __name__=='__main__':main()
