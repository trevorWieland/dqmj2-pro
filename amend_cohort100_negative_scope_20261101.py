from project import ROOT, read_json, write_json, sha256, configuration
from recovery_registry import verify_sources
from recovery_order import order_batches
from ledger_state import collect_matches


def main():
    plan_path = ROOT / 'evidence/verification/cohort-2026-10-29-100.json'
    transaction = ROOT / 'work/integration/cohort100-recovery-transaction.json'
    registry_path = ROOT / 'recovery.json'
    plan = read_json(plan_path)
    assert plan['linksPending']
    assert sha256(registry_path) == sha256(transaction) == plan['sourceRegistrySha256']
    assert read_json(ROOT / 'evidence/verification/cohort100-validation-driver.json')['state'] == 'failed'
    previous = registry_path.read_bytes()
    previous_plan = plan_path.read_bytes()
    registry = read_json(registry_path)
    changed = []
    for family in ['reward437', 'clamp453']:
        receipt_path = ROOT / f'evidence/verification/{family}-negative-scope-20261101.json'
        receipt = read_json(receipt_path)
        assert receipt['fullOriginalExecutionAndControlChecksRerun']
        assert receipt['sourceAndObjectIdentitiesPreserved']
        report = read_json(ROOT / receipt['report'])
        assert sha256(ROOT / receipt['report']) == receipt['reportSha256']
        assert sha256(ROOT / receipt['generator']) == receipt['generatorSha256']
        batch = next(row for row in registry['batches'] if row['report'] == receipt['report'])
        old_pins = dict(batch['sourceHashes'])
        for row in report['generatorSources']:
            assert sha256(ROOT / row['path']) == row['sha256']
            assert row['path'] not in old_pins or old_pins[row['path']] == row['sha256']
            batch['sourceHashes'][row['path']] = row['sha256']
        batch['reproduce'] = [receipt['generator'], '--family', family]
        assert all(batch['sourceHashes'][name] == digest for name, digest in old_pins.items())
        changed.append(dict(family=family, report=receipt['report'], receipt=receipt_path.relative_to(ROOT).as_posix(),
            receiptSha256=sha256(receipt_path), oldPins=len(old_pins), currentPins=len(batch['sourceHashes'])))
    ordered = order_batches(registry['batches'], details=True)
    assert ordered['topologicalOrderVerified']
    try:
        write_json(transaction, registry)
        registry_path.write_bytes(transaction.read_bytes())
        verify_sources()
        selected, rejected = collect_matches(configuration()['romSha256'])
        assert not rejected
        assert len(selected) == plan['expectedSourceMatchedFunctions']
        plan['sourceRegistrySha256'] = sha256(registry_path)
        evidence_path = ROOT / 'evidence/verification/cohort100-negative-scope-replay-migration-20261101.json'
        write_json(evidence_path, dict(changed=changed, previousRegistrySha256=sha256_bytes(previous),
            currentRegistrySha256=sha256(registry_path), topologicalOrderVerified=True,
            originalSourceAndObjectIdentitiesPreserved=True, originalSourcePinsPreserved=True,
            negativeEvidencePreserved=True, globalDependencyGuardsUnmodified=True, newFunctionCredit=0, newByteCredit=0))
        plan.setdefault('replayMetadataMigrations', []).append(dict(path=evidence_path.relative_to(ROOT).as_posix(), sha256=sha256(evidence_path)))
        write_json(plan_path, plan)
    except BaseException:
        registry_path.write_bytes(previous)
        transaction.write_bytes(previous)
        plan_path.write_bytes(previous_plan)
        raise
    print(dict(topologicalOrderVerified=True, sourceFunctions=len(selected), newByteCredit=0))


def sha256_bytes(value):
    import hashlib
    return hashlib.sha256(value).hexdigest()


if __name__ == '__main__':
    main()
