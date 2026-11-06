from project import ROOT, read_json, write_json, sha256, configuration
from recovery_registry import verify_sources
from recovery_order import order_batches
from ledger_state import collect_matches


def main():
    plan_path = ROOT / 'evidence/verification/cohort-2026-10-29-102.json'
    registry_path = ROOT / 'recovery.json'
    transaction = ROOT / 'work/integration/cohort102-recovery-transaction.json'
    plan = read_json(plan_path)
    assert plan['linksPending']
    assert read_json(ROOT / 'evidence/verification/cohort102-validation-driver.json')['state'] == 'failed'
    assert sha256(registry_path) == sha256(transaction) == plan['sourceRegistrySha256']
    receipt_path = ROOT / 'evidence/verification/sdk-lock-pair-symbol-transport-20261101.json'
    receipt = read_json(receipt_path)
    assert receipt['preparedOnly'] and receipt['roundTripExact'] and receipt['allOriginalControlsPassed']
    assert receipt['originalControls'] == 41
    assert sha256(ROOT / receipt['generator']) == receipt['generatorSha256']
    report_path, control_path = ROOT / receipt['report'], ROOT / receipt['controls']
    assert sha256(report_path) == receipt['previousReportSha256']
    assert sha256(control_path) == receipt['previousControlsSha256']
    assert sha256(ROOT / receipt['normalizedReport']) == receipt['normalizedReportSha256']
    assert sha256(ROOT / receipt['normalizedControls']) == receipt['normalizedControlsSha256']
    saved = {path: path.read_bytes() for path in [plan_path, registry_path, transaction, report_path, control_path]}
    registry = read_json(registry_path)
    batch = next(row for row in registry['batches'] if row['report'] == receipt['report'])
    previous_pins = dict(batch['sourceHashes'])
    for row in receipt['supplementalReplaySources']:
        assert sha256(ROOT / row['path']) == row['sha256']
        assert row['path'] not in previous_pins or previous_pins[row['path']] == row['sha256']
        batch['sourceHashes'][row['path']] = row['sha256']
    batch['reproduce'] = [receipt['generator'], '--family', 'lock-pair']
    for oracle in registry['oracles']:
        if oracle['report'] == receipt['controls']:
            oracle['reproduce'] = list(batch['reproduce'])
    try:
        report_path.write_bytes((ROOT / receipt['normalizedReport']).read_bytes())
        control_path.write_bytes((ROOT / receipt['normalizedControls']).read_bytes())
        write_json(transaction, registry)
        registry_path.write_bytes(transaction.read_bytes())
        verify_sources()
        assert order_batches(registry['batches'], details=True)['topologicalOrderVerified']
        selected, rejected = collect_matches(configuration()['romSha256'])
        assert not rejected and len(selected) == plan['expectedSourceMatchedFunctions']
        evidence = ROOT / 'evidence/verification/cohort102-sdk-symbol-transport-migration-20261101.json'
        write_json(evidence, dict(preparationReceipt=receipt_path.relative_to(ROOT).as_posix(),
            preparationReceiptSha256=sha256(receipt_path), oldPins=len(previous_pins), currentPins=len(batch['sourceHashes']),
            allPreviousPinsPreserved=all(batch['sourceHashes'][name] == digest for name,digest in previous_pins.items()),
            originalSourceAndObjectIdentitiesPreserved=True, originalValidatorAndAll41ControlsUnchanged=True,
            originalBuilderUnmodified=True, reversibleAddressSerializationOnly=True, newFunctionCredit=0, newByteCredit=0))
        plan['sourceRegistrySha256'] = sha256(registry_path)
        plan.setdefault('replayMetadataMigrations', []).append(dict(path=evidence.relative_to(ROOT).as_posix(), sha256=sha256(evidence)))
        write_json(plan_path, plan)
    except BaseException:
        for path, data in saved.items():
            path.write_bytes(data)
        raise
    print(dict(sourceFunctions=len(selected), originalControls=41, reversibleSerialization=True, newByteCredit=0))


if __name__ == '__main__':
    main()
