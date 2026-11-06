import argparse
from project import ROOT, read_json, write_json, sha256

FAMILIES = {'driver-leaves': '20261030', 'timing': '20261031', 'setting': '20261031',
            'initializer': '20261031', 'alarm-selector': '20261031'}


def identity(document):
    fields = ['address', 'bytes', 'source', 'sourceSha256', 'object', 'objectSha256', 'targetSha256']
    return [{key: row.get(key) for key in fields} for row in document['matches']]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    options = parser.parse_args()
    plan_path = ROOT / f'evidence/verification/cohort-2026-10-29-{options.cohort}.json'
    transaction = ROOT / f'work/integration/cohort{options.cohort}-recovery-transaction.json'
    plan = read_json(plan_path)
    assert plan['linksPending'] and sha256(transaction) == plan['sourceRegistrySha256']
    registry = read_json(transaction)
    migrations = []
    entries = [(family, f'evidence/matches/arm7-lane-{family}-{date}.json',
        f'evidence/verification/arm7-lane-{family}-controls-{date}.json',
        f'evidence/verification/legacy-arm7-{family}-closure-compatibility-20261101.json')
        for family, date in FAMILIES.items()]
    entries.append(('channel67', 'evidence/matches/arm7-channel-parameters-20261030-67.json',
        'evidence/verification/arm7-channel-parameters-controls-20261030-67.json',
        'evidence/verification/channel67-closure-v2-compatibility-20261101.json'))
    for family, report_name, control_name, receipt_name in entries:
        receipt_path = ROOT / receipt_name
        receipt = read_json(receipt_path)
        assert receipt.get('family', family) == family and receipt['preparedOnly']
        assert receipt['allOriginalControlsPassed'] and receipt['unchangedOriginalValidator']
        assert sha256(ROOT / receipt['generator']) == receipt['generatorSha256']
        assert sha256(ROOT / report_name) == receipt['originalReportSha256']
        assert sha256(ROOT / receipt['report']) == receipt['reportSha256']
        assert sha256(ROOT / receipt['controls']) == receipt['controlsSha256']
        assert identity(read_json(ROOT / report_name)) == identity(read_json(ROOT / receipt['report']))
        controls = read_json(ROOT / receipt['controls'])
        assert controls['report'] == report_name and controls['reportSha256'] == receipt['reportSha256']
        assert len(controls['controls']) == receipt['negativeControls']
        assert all(row['rejected'] for row in controls['controls'])
        batch = next(row for row in registry['batches'] if row['report'] == report_name)
        old_pins = dict(batch['sourceHashes'])
        previous_command = list(batch['reproduce'])
        for row in receipt['supplementalReplaySources']:
            assert sha256(ROOT / row['path']) == row['sha256']
            assert row['path'] not in old_pins or old_pins[row['path']] == row['sha256']
            batch['sourceHashes'][row['path']] = row['sha256']
        batch['reproduce'] = [receipt['generator']] if family == 'channel67' else [receipt['generator'], '--family', family]
        assert all(batch['sourceHashes'][name] == digest for name, digest in old_pins.items())
        migrations.append(dict(family=family, report=report_name, controlReport=control_name,
            previousReportSha256=sha256(ROOT / report_name), previousControlsSha256=sha256(ROOT / control_name),
            normalizedReport=receipt['report'], normalizedReportSha256=receipt['reportSha256'],
            normalizedControls=receipt['controls'], normalizedControlsSha256=receipt['controlsSha256'],
            preparationReceipt=receipt_path.relative_to(ROOT).as_posix(), preparationReceiptSha256=sha256(receipt_path),
            previousCommand=previous_command, preferredCommand=batch['reproduce'],
            previousSourcePins=len(old_pins), currentSourcePins=len(batch['sourceHashes']),
            originalSourceAndObjectIdentitiesPreserved=True, originalSourcePinsPreserved=True,
            unchangedOriginalValidator=True, allOriginalControlsPassed=True, negativeControls=receipt['negativeControls'],
            newFunctionCredit=0, newByteCredit=0))
    report_only = []
    for family in ['reward437', 'clamp453']:
        receipt_path = ROOT / f'evidence/verification/{family}-negative-scope-v2-20261101.json'
        receipt = read_json(receipt_path)
        assert receipt['preparedOnly'] and receipt['fullOriginalExecutionAndControlChecksRerun']
        assert receipt['sourceAndObjectIdentitiesPreserved']
        assert sha256(ROOT / receipt['generator']) == receipt['generatorSha256']
        assert sha256(ROOT / receipt['report']) == receipt['previousReportSha256']
        assert sha256(ROOT / receipt['normalizedReport']) == receipt['reportSha256']
        normalized = read_json(ROOT / receipt['normalizedReport'])
        assert identity(read_json(ROOT / receipt['report'])) == identity(normalized)
        batch = next(row for row in registry['batches'] if row['report'] == receipt['report'])
        old_pins = dict(batch['sourceHashes'])
        for row in normalized['generatorSources']:
            assert sha256(ROOT / row['path']) == row['sha256']
            assert row['path'] not in old_pins or old_pins[row['path']] == row['sha256']
            batch['sourceHashes'][row['path']] = row['sha256']
        batch['reproduce'] = [receipt['generator'], '--family', family]
        assert all(batch['sourceHashes'][name] == digest for name, digest in old_pins.items())
        report_only.append(dict(family=family, report=receipt['report'], previousReportSha256=receipt['previousReportSha256'],
            normalizedReport=receipt['normalizedReport'], normalizedReportSha256=receipt['reportSha256'],
            preparationReceipt=receipt_path.relative_to(ROOT).as_posix(), preparationReceiptSha256=sha256(receipt_path),
            oldPins=len(old_pins), currentPins=len(batch['sourceHashes']), allOriginalControlsRerun=True,
            originalSourceAndObjectIdentitiesPreserved=True, oldSourcePinsPreserved=True, newByteCredit=0))
    evidence_path = ROOT / f'evidence/verification/cohort{options.cohort}-legacy-replay-migrations-20261101.json'
    write_json(evidence_path, dict(cohort=options.cohort, migrations=migrations, reportOnlyMigrations=report_only, preparedOnly=True,
        totalOriginalControls=sum(row['negativeControls'] for row in migrations), newFunctionCredit=0, newByteCredit=0))
    write_json(transaction, registry)
    plan['sourceRegistrySha256'] = sha256(transaction)
    plan.setdefault('replayMetadataMigrations', []).append(dict(path=evidence_path.relative_to(ROOT).as_posix(), sha256=sha256(evidence_path)))
    write_json(plan_path, plan)
    print(dict(cohort=options.cohort, families=len(migrations), controls=sum(row['negativeControls'] for row in migrations), newByteCredit=0))


if __name__ == '__main__':
    main()
