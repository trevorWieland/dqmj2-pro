import argparse
from project import ROOT, read_json, write_json, sha256
from recovery_order import order_batches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--receipt', action='append', required=True)
    options = parser.parse_args()
    transaction = ROOT / f'work/integration/cohort{options.cohort}-recovery-transaction.json'
    plan_path = ROOT / f'evidence/verification/cohort-2026-10-29-{options.cohort}.json'
    plan = read_json(plan_path)
    assert plan['linksPending'] and sha256(transaction) == plan['sourceRegistrySha256']
    registry = read_json(transaction)
    changes = []
    for name in options.receipt:
        receipt = read_json(ROOT / name)
        assert receipt['roundTripExact'] and receipt['allOriginalControlsPassed']
        assert sha256(ROOT / receipt['generator']) == receipt['generatorSha256']
        assert sha256(ROOT / receipt['report']) == receipt['normalizedReportSha256']
        assert sha256(ROOT / receipt['controls']) == receipt['normalizedControlsSha256']
        batch = next(row for row in registry['batches'] if row['report'] == receipt['report'])
        assert batch['reproduce'] == [receipt['generator'], '--family', receipt['family']]
        previous = dict(batch['sourceHashes'])
        for row in receipt['supplementalReplaySources']:
            assert sha256(ROOT / row['path']) == row['sha256']
            assert row['path'] not in previous or previous[row['path']] == row['sha256']
            batch['sourceHashes'][row['path']] = row['sha256']
        assert all(batch['sourceHashes'][path] == digest for path,digest in previous.items())
        changes.append(dict(receipt=name, receiptSha256=sha256(ROOT / name), report=receipt['report'],
            previousPins=len(previous), currentPins=len(batch['sourceHashes']), oldPinsPreserved=True,
            originalControls=receipt['originalControls'], sourceAndObjectIdentitiesPreserved=True,
            newFunctionCredit=0, newByteCredit=0))
    assert order_batches(registry['batches'], details=True)['topologicalOrderVerified']
    evidence = ROOT / f'evidence/verification/cohort{options.cohort}-prepared-replay-transports-20261101.json'
    write_json(evidence, dict(changes=changes, registryOnlySourcePinAugmentation=True, newByteCredit=0))
    write_json(transaction, registry)
    plan['sourceRegistrySha256'] = sha256(transaction)
    plan.setdefault('replayMetadataMigrations', []).append(dict(path=evidence.relative_to(ROOT).as_posix(), sha256=sha256(evidence)))
    write_json(plan_path, plan)
    print(dict(cohort=options.cohort, transports=len(changes), newByteCredit=0))


if __name__ == '__main__':
    main()
