import json
import subprocess
from pathlib import Path
import utility_code
import utility_bridges
from project import ROOT, sha256, write_json, now

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/utility-child'
WORK = ROOT / 'work/parallel-wave20261102/utility-child'
SOURCE = ROOT / 'src/utility/parallel_wave20261102'


def prepare():
    specs = utility_code.candidates()
    used = []
    recovery = json.loads((ROOT / 'recovery.json').read_text())
    reports = {item['report'] for item in recovery['batches']}
    reports.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/matches').glob('*utility*.json'))
    reports.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/matches').glob('*child*.json'))
    for path in sorted(reports):
        for row in json.loads((ROOT / path).read_text()).get('matches', []):
            if row.get('module') == 'utility-child-arm9-main':
                size = row.get('bytes', row.get('size', 0))
                first = int(row['address'], 0)
                used.append((first, first + size, path))
    for row in utility_bridges.derive()['bridges']:
        if row['module'] == 'utility-child-arm9-main':
            first = int(row['address'], 0)
            used.append((first, first + row['bytes'], 'utility-bridge'))
    chosen = [s for s in specs if s['module'] == 'utility-child-arm9-main'
              and 0x020035bc <= s['address'] < 0x020074c4
              and not any(a < s['address'] + s['bytes'] and s['address'] < b for a, b, p in used)]
    rows = []
    for spec in chosen:
        body = (ROOT / spec['binary']).read_bytes()
        offset = spec['address'] - spec['base']
        rows.append({**{k: v for k, v in spec.items() if k not in ('instructions', 'pools')},
                     'address': hex(spec['address']), 'end': hex(spec['address'] + spec['bytes']),
                     'targetSha256': utility_code.utility_runtime.sha(body[offset:offset + spec['bytes']])})
    claim = dict(schemaVersion=1, owner='workflow_research', createdUtc=now(), state='claimed-research',
                 baselineCommit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                 romSha256=json.loads((ROOT / 'project.json').read_text())['romSha256'],
                 program='dwc/utility.bin/move/child.srl', processor='arm9', module='utility-child-arm9-main',
                 regionStart='0x020035bc', regionEndExclusive='0x020074c4', functionCount=len(rows),
                 nativeOpportunityBytes=sum(r['bytes'] for r in rows), functions=rows,
                 exclusiveSourceRoot=SOURCE.relative_to(ROOT).as_posix(),
                 exclusiveWorkRoot=WORK.relative_to(ROOT).as_posix(),
                 sharedMutationsForbidden=['recovery.json', 'manifest.json', 'source-map.json', 'ledger/', 'README.md'],
                 sourceCreditGranted=0, wholeModuleLinked=False,
                 exclusionMethod='all accepted recovery reports plus existing utility/child prepared match reports and bridges',
                 inputs=[dict(path='recovery.json', sha256=sha256(ROOT / 'recovery.json'))])
    LANE.mkdir(parents=True, exist_ok=True)
    path = LANE / 'claim.json'
    if path.exists():
        raise ValueError('Claim exists; refusing replacement')
    write_json(path, claim)
    print(dict(claim=path.relative_to(ROOT).as_posix(), functions=len(rows), bytes=claim['nativeOpportunityBytes']))


if __name__ == '__main__':
    prepare()
