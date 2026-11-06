import hashlib
import subprocess
import sys
from unittest.mock import patch
from project import ROOT, read_json, write_json, write_text, sha256, configuration, now
import recovery_registry
import source_selection
from recovery_registry import register, verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources


PACKETS = [
    ('main-float-primitives-20261031', 'match_main_float_primitives_20261031.py', False),
    ('main-float-rounding-20261031', 'match_main_float_rounding_20261031.py', False),
    ('main-float-scale-wrapper-20261031', 'match_main_float_scale_wrapper_20261031.py', False),
    ('main-case-compare-20261031', 'match_main_case_compare_20261031.py', False),
    ('main-ascii-lower-data-20261031', 'match_main_ascii_lower_data_20261031.py', False),
    ('ov001-20261031-recruit373', 'match_ov001_recruit373_20261031.py', False),
    ('ov001-refresh-void-caller-20261031', 'adopt_ov001_refresh_void_caller_20261031.py', False),
    ('ov001-20261031-membership377', 'match_ov001_membership377_20261031.py', False),
    ('ov001-20261031-eligibility381', 'match_ov001_eligibility381_20261031.py', False),
    ('mechanics-save-20261031-lane-packed-input', 'match_mechanics_save_20261031_lane_packed_input.py', False),
    ('arm7-alarm-family572-20261031', 'match_arm7_alarm_family572_20261031.py', True),
]
MIGRATIONS = {
    ('ov001', 'arm', 0x02209AC0): ('typed-membership', 'Use the native-qualified membership source interface while preserving the previously matched140 bytes'),
    ('ov001', 'arm', 0x02209CC0): ('void-refresh-declaration', 'Declare the demonstrated actor-refresh call void; preserve caller instruction bytes'),
    ('arm7-wram', 'arm', 0x037FE5C0): ('complete-alarm-type', 'Replace the opaque44-byte alarm declaration with the connected measured full type'),
}
SUPERSEDED = 'evidence/matches/arm7-lane-alarm-registration156-20261031.json'
TRANSACTION = ROOT / 'work/integration/cohort95-recovery-transaction.json'
PREFERENCES = ROOT / 'work/integration/cohort95-preference-transaction.json'


def main():
    old = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-94.json')
    verify_sources()
    assert not old['linksPending'] and sha256(TRANSACTION) == old['sourceRegistrySha256']
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == 9053
    policy = read_json(ROOT / 'source-preferences.json')
    assert len(policy['preferences']) == 70
    fields = ['source', 'sourceSha256', 'object', 'objectSha256', 'size', 'targetSha256', 'report']
    write_json(ROOT / 'evidence/verification/cohort95-before-adoption-20261031.json', dict(
        registrySha256=sha256(TRANSACTION), preferencesSha256=sha256(ROOT / 'source-preferences.json'),
        selected=[dict(key=list(key), **{field: row[field] for field in fields if field in row}) for key, row in before.items()]))
    registry = read_json(TRANSACTION)
    removed = [row for row in registry['batches'] if row['report'] == SUPERSEDED]
    assert len(removed) == 1 and removed[0]['entries'] == 1
    registry['batches'] = [row for row in registry['batches'] if row['report'] != SUPERSEDED]
    write_json(TRANSACTION, registry)
    migrated, reports = set(), []
    for name, producer, raw in PACKETS:
        report = 'evidence/matches/' + name + '.json'
        if raw:
            register(report, [producer])
        else:
            seal_sources(report, [producer])
            register(report, ['seal_recovery_sources_20261031.py', report, producer])
        reports.append(report)
        for row in read_json(ROOT / report).get('matches', []):
            key = row['module'], row['mode'], int(row['address'], 0)
            if key not in MIGRATIONS:
                continue
            prior = before[key]
            assert row['bytes'] == prior['size'] and sha256(ROOT / prior['source']) == prior['sourceSha256']
            assert not prior.get('targetSha256') or row['targetSha256'] == prior['targetSha256']
            label, reason = MIGRATIONS[key]
            identity = dict(processor=row['processor'], module=row['module'], mode=row['mode'],
                address=row['address'], bytes=row['bytes'], targetSha256=row['targetSha256'])
            preferred = dict(source=row['source'], sourceSha256=row['sourceSha256'], report=report)
            evidence = f'evidence/abi/{row["module"]}-{key[2]:08x}-{label}-primary-migration-20261031.json'
            write_json(ROOT / evidence, dict(romSha256=configuration()['romSha256'], identity=identity,
                previous={field: prior[field] for field in ['source', 'sourceSha256', 'report']}, preferred=preferred,
                originalSourceUnchanged=True, nativeBytesUnchanged=True, newFunctionCredit=0, newByteCredit=0,
                sourceApiChange=reason, historicalObjectHashes=dict(previous=prior['objectSha256'], preferred=row['objectSha256']),
                behavioralProof=dict(report=report, reportSha256=sha256(ROOT / report), limitations=read_json(ROOT / report).get('limitations', ['Complete scope and unsupported paths are defined in the referenced native fixture report; no broader contract inferred']))))
            if row['processor'] == 'arm9':
                policy['preferences'].append(dict(**identity, **preferred, evidence=evidence, evidenceSha256=sha256(ROOT / evidence)))
            else:
                assert row['processor'] == 'arm7' and key == ('arm7-wram', 'arm', 0x037FE5C0)
                for original_source, original_hash in removed[0]['sourceHashes'].items():
                    assert sha256(ROOT / original_source) == original_hash
            migrated.add(key)
    assert migrated == set(MIGRATIONS) and len(policy['preferences']) == 72
    write_json(PREFERENCES, policy)
    verify_sources()
    original_preferences = source_selection.preferences
    with patch.object(source_selection, 'preferences', lambda namespace: original_preferences(namespace, path=PREFERENCES)):
        after, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    for key, row in before.items():
        if key not in migrated:
            assert all(after[key][field] == row[field] for field in ['source', 'sourceSha256', 'object', 'objectSha256'])
    added = set(after) - set(before)
    assert len(added) == 14 and sum(after[key]['size'] for key in added) == 2428
    registry = read_json(TRANSACTION)
    for script in ['compile_float_runtime_ports_20261031.py', 'verify_windows_float_runtime_20261031.py', 'prepare_float_runtime_android_20261031.py']:
        subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)
    oracles = {row['report']: row for row in registry['oracles']}
    for report, command in [
        ('evidence/verification/arm7-alarm-family572-controls-20261031.json', ['validate_arm7_alarm_family572_20261031.py']),
        ('evidence/portability/float-runtime-build-20261031.json', ['compile_float_runtime_ports_20261031.py']),
        ('evidence/portability/windows-float-runtime-execution-20261031.json', ['verify_windows_float_runtime_20261031.py']),
        ('evidence/portability/android-float-runtime-runner-20261031.json', ['prepare_float_runtime_android_20261031.py']),
    ]:
        assert (ROOT / report).is_file()
        oracles[report] = dict(report=report, reproduce=command)
    registry['oracles'] = list(oracles.values())
    write_json(TRANSACTION, registry)
    plan = {key: value for key, value in old.items() if key.startswith(('expectedInterpreted', 'expectedEmpty', 'expectedNonempty', 'expectedCopy'))}
    plan.update(schemaVersion=1, createdUtc=now(), reports=reports, interpretedReports=[],
        sourceRegistrySha256=sha256(TRANSACTION), sourcePreferenceSha256=sha256(PREFERENCES),
        interpretedRegistrySha256=sha256(ROOT / 'interpreted-recovery.json'), linksPending=True,
        newSourceFunctions=14, newOrdinaryCBytes=2428, newSourceBytes=2556, newMathematicalDataBytes=128,
        duplicateMigrationFunctions=3, duplicateMigrationBytes=1388, expectedSourceMatchedFunctions=9067,
        expectedSourceLinkedBytes=689765, preferredSourceInputsRequired=72, sourceReconstructionComplete=False,
        wholeRomMatchedFromSource=False, sourceOnlyRomProven=False, fullWindowsGameFromSourceProven=False,
        androidDeviceExecutionCount=0, previousAcceptedCohort=94, previousAcceptedFunctions=len(before),
        previousAcceptedBytes=old['sourceLinkedBytes'], allUnmigratedSourcesAndObjectsPreserved=True,
        supersededBatch=dict(previous=removed[0], replacement=reports[-1], oldSourceAndEvidencePreserved=True,
            migrationEvidence='evidence/abi/arm7-wram-037fe5c0-complete-alarm-type-primary-migration-20261031.json',
            sourcePreferenceGuardUnchanged=True),
        fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT / 'evidence/verification/cohort-2026-10-29-95.json', plan)
    print(dict(newFunctions=14, newFunctionBytes=2428, newDataBytes=128, zeroCreditMigrationBytes=1388, linksPending=True))


if __name__ == '__main__':
    current, preferences = ROOT / 'recovery.json', ROOT / 'source-preferences.json'
    original_registry, original_policy = current.read_bytes(), preferences.read_bytes()
    TRANSACTION.parent.mkdir(parents=True, exist_ok=True)
    TRANSACTION.write_bytes(original_registry)
    PREFERENCES.write_bytes(original_policy)
    recovery_registry.REGISTRY = TRANSACTION
    main()
    assert current.read_bytes() == original_registry and preferences.read_bytes() == original_policy
    write_text(preferences, PREFERENCES.read_text(encoding='utf-8-sig'))
    write_text(current, TRANSACTION.read_text(encoding='utf-8-sig'))
