import argparse
from project import ROOT, read_json, write_json, sha256


def address(value):
    if isinstance(value, bool):
        raise ValueError('Boolean is not an executable address')
    number = int(value, 0) if isinstance(value, str) else int(value)
    if not 0 <= number <= 0xFFFFFFFF:
        raise ValueError('Address is outside the measured word namespace')
    return number


def identity(row):
    return row['processor'], row.get('program') or '', row['module'], row['mode'], address(row['address'])


def candidates(spec):
    entries = {}
    for packet in spec['packets']:
        report = read_json(ROOT / packet['report'])
        for row in report.get('matches', []):
            normalized = {**report, **row}
            key = row['module'], row['mode'], address(row['address'])
            if key in entries:
                raise ValueError('Ambiguous same-package module/mode/address')
            entries[key] = dict(processor=normalized['processor'], program=normalized.get('program') or '',
                module=normalized['module'], mode=normalized['mode'], address=address(row['address']),
                bytes=row['bytes'], source=row['source'], sourceSha256=row['sourceSha256'], report=packet['report'])
    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--specification', required=True)
    parser.add_argument('--accepted-cohort', type=int, required=True)
    parser.add_argument('--pending-specification')
    options = parser.parse_args()
    snapshot = f'evidence/verification/accepted-cohort{options.accepted_cohort}-identities-v2-20261101.json'
    accepted = read_json(ROOT / snapshot)['functions']
    assert address(0x0202B54C) == address('0x202b54c') == address('0X0202B54C')
    for invalid in [True, -1, 0x100000000]:
        try:
            address(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid address normalization passed')
    known = list(accepted)
    pending = []
    if options.pending_specification:
        previous = read_json(ROOT / options.pending_specification)
        proposed = candidates(previous)
        for item in previous['expectedAdditions']:
            pending.append(proposed[item['module'], item['mode'], address(item['address'])])
        known.extend(pending)
    specification = read_json(ROOT / options.specification)
    proposed = candidates(specification)
    exact = {identity(row): row for row in known}
    conflicts, additions, migrations = [], [], []
    for item in specification['expectedAdditions']:
        key = item['module'], item['mode'], address(item['address'])
        row = proposed[key]
        assert row['bytes'] == item['bytes']
        current = identity(row)
        collisions = [old for old in known if identity(old)[:3] == current[:3]
            and address(old['address']) < current[4] + row['bytes']
            and current[4] < address(old['address']) + old['bytes']]
        if collisions:
            conflicts.append(dict(proposed=row, overlaps=[dict(identity=list(identity(old)),
                bytes=old['bytes'], source=old['source']) for old in collisions]))
        additions.append(row)
    for item in specification.get('migrations', []):
        row = proposed[item['module'], item['mode'], address(item['address'])]
        current = identity(row)
        assert current in exact and exact[current]['bytes'] == row['bytes'] == item['bytes']
        migrations.append(dict(identity=list(current), bytes=row['bytes'], newByteCredit=0,
            previousSource=exact[current]['source'], proposedSource=row['source']))
    assert len({identity(row) for row in additions}) == len(additions)
    report = dict(generator=__file__.split(chr(92))[-1], generatorSha256=sha256(__file__),
        acceptedSnapshot=snapshot, acceptedSnapshotSha256=sha256(ROOT / snapshot),
        specification=options.specification, specificationSha256=sha256(ROOT / options.specification),
        acceptedRows=len(accepted), pendingRowsUsedOnlyForExclusion=len(pending),
        pendingSourceAcceptanceClaimed=False, newFunctionCandidates=len(additions),
        newByteCandidates=sum(row['bytes'] for row in additions), migrations=migrations,
        overlapConflicts=conflicts, passed=not conflicts, sourceCredit=0,
        limitations=['Current linked acceptance and original-source preservation remain separate gates',
            'Pending rows exclude duplicate work but never establish accepted coverage',
            'Interval collisions require explicit reconciliation; this audit cannot approve shared tails or ARM/Thumb interiors'])
    output = ROOT / f'evidence/verification/cohort{specification["cohort"]}-identity-preflight-20261101.json'
    write_json(output, report)
    print(dict(passed=not conflicts, candidates=len(additions), candidateBytes=report['newByteCandidates'],
        zeroCreditMigrations=len(migrations), overlaps=len(conflicts)))
    assert not conflicts


if __name__ == '__main__':
    main()
