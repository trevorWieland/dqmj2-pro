import json
import subprocess
from pathlib import Path
import utility_code
from wave20261102_host_arm7_sixth_index import candidates
from project import ROOT, write_json, read_json, sha256, now

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/host-arm7-sixth'
WORK = ROOT / 'work/parallel-wave20261102/host-arm7-sixth'
SOURCE = ROOT / 'src/utility/parallel_wave20261102/host-arm7-sixth'


def main():
    occupied, pins = [], []
    def add(row):
        if row.get('program') or row.get('processor') != 'arm7' or row.get('module') != 'arm7-main':
            return
        address = int(row['address'], 0)
        occupied.append((address, address + row.get('bytes', row.get('size', 0))))
    ledger = ROOT / 'ledger/functions.jsonl'
    for line in ledger.read_text().splitlines():
        row = json.loads(line)
        if row['states']['functionMatched']:
            add(row)
    pins.append(dict(path=ledger.relative_to(ROOT).as_posix(), sha256=sha256(ledger)))
    for path in sorted(ROOT.glob('cohort*-specification.json')):
        data = read_json(path)
        for row in data.get('expectedAdditions', []) + data.get('migrations', []):
            add(row)
    reports = {b['report'] for b in read_json(ROOT / 'recovery.json')['batches']}
    reports.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/matches').glob('*.json'))
    reports.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/lanes').rglob('packet-ready.json'))
    for name in sorted(reports):
        for row in read_json(ROOT / name).get('matches', []):
            add(row)
    for path in sorted((ROOT / 'evidence/lanes').rglob('claim.json')):
        data = read_json(path)
        for row in data.get('functions', []):
            add(dict({'program': data.get('program', ''), 'processor': data.get('processor'), 'module': data.get('module')}, **row))
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
    rows = []
    for spec in candidates():
        if spec['module'] != 'arm7-main' or spec['mode'] != 'arm' or not 0x027e0000 <= spec['address'] < 0x027e6000:
            continue
        if any(a < spec['address'] + spec['bytes'] and spec['address'] < b for a, b in occupied):
            continue
        raw = (ROOT / spec['binary']).read_bytes()
        at = spec['address'] - spec['base']
        rows.append(dict(**{k: v for k, v in spec.items() if k not in ['address', 'instructions', 'pools']},
            address=hex(spec['address']), end=hex(spec['address'] + spec['bytes']),
            targetSha256=utility_code.utility_runtime.sha(raw[at:at + spec['bytes']])))
    path = LANE / 'claim.json'
    if path.exists():
        raise ValueError('Fourth ownership claim already exists')
    write_json(path, dict(schemaVersion=1, owner='workflow_research', createdUtc=now(),
        baselineCommit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        romSha256=read_json(ROOT / 'project.json')['romSha256'], program='',
        processor='arm7', module='arm7-main', regionStart='0x027e0000', regionEndExclusive='0x027e6000',
        functions=rows, functionCount=len(rows), nativeOpportunityBytes=sum(r['bytes'] for r in rows),
        exclusiveSourceRoot=SOURCE.relative_to(ROOT).as_posix(), exclusiveWorkRoot=WORK.relative_to(ROOT).as_posix(),
        ownershipInputSnapshots=pins, selectionAndAllPreparedClaimsExcluded=True, sourceCreditGranted=0,
        wholeModuleLinked=False, arm9StartupAssociationReportRequired=False))
    print(dict(functions=len(rows), bytes=sum(r['bytes'] for r in rows)))


if __name__ == '__main__':
    main()
