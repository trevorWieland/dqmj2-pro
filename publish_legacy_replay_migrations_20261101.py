import argparse
import subprocess
import sys
from project import ROOT, read_json, sha256
from recovery_order import order_batches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    options = parser.parse_args()
    evidence_path = ROOT / f'evidence/verification/cohort{options.cohort}-legacy-replay-migrations-20261101.json'
    evidence = read_json(evidence_path)
    plan_path = ROOT / f'evidence/verification/cohort-2026-10-29-{options.cohort}.json'
    plan = read_json(plan_path)
    assert plan['linksPending']
    assert any(row['path'] == evidence_path.relative_to(ROOT).as_posix() and row['sha256'] == sha256(evidence_path)
               for row in plan['replayMetadataMigrations'])
    backups = {path: path.read_bytes() for path in [ROOT / 'recovery.json', ROOT / 'source-preferences.json', plan_path]}
    publications = []
    for row in evidence['migrations']:
        assert sha256(ROOT / row['preparationReceipt']) == row['preparationReceiptSha256']
        for target, candidate, old_hash, new_hash in [
            (row['report'], row['normalizedReport'], row['previousReportSha256'], row['normalizedReportSha256']),
            (row['controlReport'], row['normalizedControls'], row['previousControlsSha256'], row['normalizedControlsSha256'])]:
            path = ROOT / target
            assert sha256(path) == old_hash and sha256(ROOT / candidate) == new_hash
            backups[path] = path.read_bytes()
            publications.append((path, (ROOT / candidate).read_bytes()))
    for row in evidence.get('reportOnlyMigrations', []):
        assert sha256(ROOT / row['preparationReceipt']) == row['preparationReceiptSha256']
        path = ROOT / row['report']
        assert sha256(path) == row['previousReportSha256']
        assert sha256(ROOT / row['normalizedReport']) == row['normalizedReportSha256']
        backups[path] = path.read_bytes()
        publications.append((path, (ROOT / row['normalizedReport']).read_bytes()))
    try:
        for path, data in publications:
            path.write_bytes(data)
        transaction = ROOT / f'work/integration/cohort{options.cohort}-recovery-transaction.json'
        assert order_batches(read_json(transaction)['batches'], details=True)['topologicalOrderVerified']
        specification = read_json(ROOT / plan['specification'])
        publisher = 'publish_prepared_source_migrations_20261101.py' if specification.get('migrations') else 'publish_source_cohort_20261101.py'
        subprocess.run([sys.executable, str(ROOT / publisher), '--cohort', str(options.cohort)], cwd=ROOT, check=True)
    except BaseException:
        for path, data in backups.items():
            path.write_bytes(data)
        raise
    print(dict(cohort=options.cohort, migratedFamilies=len(evidence['migrations']),
        originalControls=evidence['totalOriginalControls'], newByteCredit=0))


if __name__ == '__main__':
    main()
