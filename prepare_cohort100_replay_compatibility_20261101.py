from project import ROOT, read_json, write_json, sha256
import recovery_registry
from recovery_registry import verify_sources
from ledger_state import collect_matches


def main():
    path = ROOT / 'work/integration/cohort100-recovery-transaction.json'
    plan_path = ROOT / 'evidence/verification/cohort-2026-10-29-100.json'
    plan = read_json(plan_path)
    assert plan['linksPending'] and sha256(path) == plan['sourceRegistrySha256']
    receipt_path = ROOT / 'evidence/verification/channel67-closure-compatibility-20261101.json'
    receipt = read_json(receipt_path)
    assert receipt['preparedOnly'] and receipt['allOriginalControlsPassed'] and receipt['negativeControls'] == 41
    assert receipt['generatorSha256'] == sha256(ROOT / receipt['generator'])
    report_name = 'evidence/matches/arm7-channel-parameters-20261030-67.json'
    control_name = 'evidence/verification/arm7-channel-parameters-controls-20261030-67.json'
    assert sha256(ROOT / report_name) == receipt['originalReportSha256']
    assert sha256(ROOT / receipt['report']) == receipt['reportSha256']
    assert sha256(ROOT / receipt['controls']) == receipt['controlsSha256']
    original, normalized = read_json(ROOT / report_name), read_json(ROOT / receipt['report'])
    assert len(original['matches']) == len(normalized['matches']) == 3
    identity_fields = ['address', 'bytes', 'source', 'sourceSha256', 'objectSha256', 'targetSha256']
    assert all(all(a[key] == b[key] for key in identity_fields) for a, b in zip(original['matches'], normalized['matches']))
    registry = read_json(path)
    batch = next(b for b in registry['batches'] if b['report'] == report_name)
    assert batch['reproduce'] == ['seal_recovery_evidence_20261031.py', report_name, 'match_arm7_channel_parameters_20261030_67.py']
    old_batch = dict(batch, sourceHashes=dict(batch['sourceHashes']))
    for item in receipt['supplementalReplaySources']:
        assert sha256(ROOT / item['path']) == item['sha256']
        assert item['path'] not in batch['sourceHashes'] or batch['sourceHashes'][item['path']] == item['sha256']
        batch['sourceHashes'][item['path']] = item['sha256']
    batch['reproduce'] = [receipt['generator']]
    assert all(batch['sourceHashes'][key] == value for key, value in old_batch['sourceHashes'].items())
    evidence = ROOT / 'evidence/verification/cohort100-channel67-replay-metadata-migration-20261101.json'
    write_json(evidence, dict(report=report_name, previousBatch=old_batch, preferredBatch=batch,
        preparationReceipt=receipt_path.relative_to(ROOT).as_posix(), preparationReceiptSha256=sha256(receipt_path),
        normalizedReport=receipt['report'], normalizedReportSha256=receipt['reportSha256'],
        normalizedControls=receipt['controls'], normalizedControlsSha256=receipt['controlsSha256'],
        previousReportSha256=sha256(ROOT / report_name), previousControlsSha256=sha256(ROOT / control_name),
        controlReport=control_name, originalSourceAndObjectIdentitiesPreserved=True,
        originalValidatorAndAll41ControlsUnchanged=True, newFunctionCredit=0, newByteCredit=0))
    write_json(path, registry)
    recovery_registry.REGISTRY = path
    verify_sources()
    selected, rejected = collect_matches(original['romSha256'])
    assert not rejected and len(selected) == plan['expectedSourceMatchedFunctions']
    plan.update(sourceRegistrySha256=sha256(path), replayMetadataMigrations=[dict(
        path=evidence.relative_to(ROOT).as_posix(), sha256=sha256(evidence))], previousSourcePinsPreserved=True)
    write_json(plan_path, plan)
    print(dict(preparedOnly=True, sourceFunctions=len(selected), oldSourcePins=len(old_batch['sourceHashes']),
               newSourcePins=len(batch['sourceHashes']), allOriginalControlsPassed=True, newByteCredit=0))


if __name__ == '__main__':
    main()
