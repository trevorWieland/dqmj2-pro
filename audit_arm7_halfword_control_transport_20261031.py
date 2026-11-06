import ast
import json
import re
from pathlib import Path
from project import ROOT,sha256,write_json
PROFILE='nonmatching/arm7-bulk/20261031/lane-halfword-control80-final/closure.json'
PINS='nonmatching/arm7-bulk/20261031/lane-halfword-control80-final/generator-pins.json'
EXPLICIT=('match_arm7_lane_halfword_control_20261031.py','validate_arm7_lane_halfword_control_20261031.py',
    'evidence/matches/arm7-lane-halfword-control80-20261031.json','evidence/verification/arm7-lane-halfword-control80-controls-20261031.json',
    'evidence/verification/arm7-halfword-control80-replay-receipt-20261031.json','docs/2026-10-31-arm7-halfword-control80.md')


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
    draft=ROOT/'nonmatching/arm7-bulk/20261031/lane-halfword-frontier224'
    for name in ('native_arm7_main_027e9528.c','native_halfword_views.h'):add((draft/name).relative_to(ROOT).as_posix(),'historical-unaccepted-typed-hypothesis')
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
    files,python=collect();output=ROOT/'evidence/verification/arm7-halfword-control80-transport-audit-20261031.json'
    write_json(output,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),
        files=[dict(path=name,sha256=sha256(ROOT/name),bytes=(ROOT/name).stat().st_size,roles=sorted(roles)) for name,roles in sorted(files.items())],
        recursivePythonFiles=len(python),currentUnits=1,newCandidateBytes=80,zeroCoverageMigrationBytes=0,sourceCredit=0,allPassed=True,
        limitations=['Generated Work products must be freshly regenerated and validated','Private pinned original ROM/modules/compiler/runtime are explicit baseline prerequisites','Historical hypotheses are not compiler inputs or accepted source credit']))
    print(dict(report=output.relative_to(ROOT).as_posix(),sha256=sha256(output),files=len(files),allPassed=True))


if __name__=='__main__':main()
