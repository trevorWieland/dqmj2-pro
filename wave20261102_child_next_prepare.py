import json
import subprocess
import utility_code
import utility_bridges
from project import ROOT, sha256, write_json, now

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/utility-child-next'
WORK = ROOT / 'work/parallel-wave20261102/utility-child-next'
SOURCE = ROOT / 'src/utility/parallel_wave20261102/next'


def main():
    reports = {b['report'] for b in json.loads((ROOT / 'recovery.json').read_text())['batches']}
    for pattern in ['*utility*.json', '*child*.json']:
        reports.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/matches').glob(pattern))
    reports.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/lanes/parallel-wave20261102').glob('*/packet-ready.json'))
    occupied = []
    for report in sorted(reports):
        for row in json.loads((ROOT / report).read_text()).get('matches', []):
            if row.get('module') == 'utility-child-arm9-main':
                first = int(row['address'], 0)
                occupied.append((first, first + row.get('bytes', row.get('size', 0))))
    for row in utility_bridges.derive()['bridges']:
        if row['module'] == 'utility-child-arm9-main':
            first = int(row['address'], 0)
            occupied.append((first, first + row['bytes']))
    rows = []
    for spec in utility_code.candidates():
        if spec['module'] != 'utility-child-arm9-main' or not 0x020074c4 <= spec['address'] < 0x0200b104:
            continue
        if any(a < spec['address'] + spec['bytes'] and spec['address'] < b for a, b in occupied):
            continue
        raw = (ROOT / spec['binary']).read_bytes()
        offset = spec['address'] - spec['base']
        rows.append({**{k: v for k, v in spec.items() if k not in ('instructions', 'pools')},
            'address': hex(spec['address']), 'end': hex(spec['address'] + spec['bytes']),
            'targetSha256': utility_code.utility_runtime.sha(raw[offset:offset + spec['bytes']])})
    path = LANE / 'claim.json'
    if path.exists():
        raise ValueError('Claim exists')
    write_json(path, dict(schemaVersion=1, owner='workflow_research', createdUtc=now(),
        baselineCommit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        romSha256=json.loads((ROOT / 'project.json').read_text())['romSha256'],
        program='dwc/utility.bin/move/child.srl', processor='arm9', module='utility-child-arm9-main',
        regionStart='0x020074c4', regionEndExclusive='0x0200b104', functions=rows,
        functionCount=len(rows), nativeOpportunityBytes=sum(r['bytes'] for r in rows),
        exclusiveSourceRoot=SOURCE.relative_to(ROOT).as_posix(), exclusiveWorkRoot=WORK.relative_to(ROOT).as_posix(),
        priorPacketUntouched='evidence/lanes/parallel-wave20261102/utility-child/packet-ready.json',
        priorClaimExcluded=True, exclusionMethod='all accepted and prepared utility/child reports, ready wave packets, and bridges',
        sourceCreditGranted=0, wholeModuleLinked=False))
    print(dict(functions=len(rows), bytes=sum(r['bytes'] for r in rows)))


if __name__ == '__main__':
    main()
