import sys
from unittest.mock import patch
import source_selection
from project import ROOT, read_json, write_json, write_text, sha256, configuration, now
import recovery_registry
from recovery_registry import register, verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources


PACKETS = [
    ('ov000-20261031-birth395', 'match_ov000_birth395_20261031.py', False),
    ('mechanics-save-20261031-lane-historical-exact95', 'match_mechanics_save_20261031_lane_historical_exact95.py', False),
    ('arm7-child-alarm544-20261031', 'match_arm7_child_alarm544_20261031.py', True),
    ('main-state-dispatch-20261031', 'match_main_state_dispatch_20261031.py', False),
    ('ov000-20261031-birth388', 'match_ov000_birth388_20261031.py', False),
    ('arm7-oneshot112-20261031', 'match_arm7_alarm_oneshot112_20261031.py', True),
    ('arm7-valarm-insert164-20261031', 'match_arm7_valarm_insert164_20261031.py', True),
    ('mechanics-save-20261031-lane-input-state-family', 'match_mechanics_save_20261031_lane_input_state_family.py', False),
    ('mechanics-save-20261031-lane-array-initial-index', 'match_mechanics_save_20261031_lane_array_initial_index.py', False),
]
TRANSACTION = ROOT / 'work/integration/cohort96-recovery-transaction.json'
PREFERENCES = ROOT / 'work/integration/cohort96-preference-transaction.json'
MIGRATIONS = {('main', 'arm', address) for address in [0x02048A94, 0x02048A9C]}


def main():
    old = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-95.json')
    verify_sources()
    assert not old['linksPending'] and sha256(TRANSACTION) == old['sourceRegistrySha256']
    preference_hash = sha256(ROOT / 'source-preferences.json')
    policy = read_json(ROOT / 'source-preferences.json')
    assert len(policy['preferences']) == 72
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == old['sourceMatchedFunctions'] == 9067
    selected = [dict(key=list(key), **{field: row.get(field) for field in
        ['source', 'sourceSha256', 'object', 'objectSha256', 'size', 'targetSha256', 'report']}) for key, row in sorted(before.items())]
    write_json(ROOT / 'evidence/verification/cohort96-before-adoption-20261031.json',
        dict(registrySha256=sha256(TRANSACTION), preferencesSha256=preference_hash, selected=selected))
    reports = []
    for name, producer, direct in PACKETS:
        report = 'evidence/matches/' + name + '.json'
        if direct:
            register(report, [producer])
        else:
            seal_sources(report, [producer])
            register(report, ['seal_recovery_sources_20261031.py', report, producer])
        reports.append(report)
    registry = read_json(TRANSACTION)
    oracles = {row['report']: row for row in registry['oracles']}
    for report, command in [
        ('evidence/verification/arm7-child-alarm544-controls-20261031.json', ['validate_arm7_child_alarm544_20261031.py']),
        ('evidence/verification/arm7-oneshot112-controls-20261031.json', ['validate_arm7_alarm_oneshot112_20261031.py']),
        ('evidence/verification/arm7-valarm-insert164-controls-20261031.json', ['validate_arm7_valarm_insert164_20261031.py']),
    ]:
        assert (ROOT / report).is_file()
        oracles[report] = dict(report=report, reproduce=command)
    registry['oracles'] = list(oracles.values())
    write_json(TRANSACTION, registry)
    migrated = set()
    for report in reports:
        for row in read_json(ROOT / report).get('matches', []):
            key = row['module'], row['mode'], int(row['address'], 0)
            if key not in MIGRATIONS:
                continue
            previous = before[key]
            assert row['processor'] == 'arm9' and row['bytes'] == previous['size'] == 8
            assert row['targetSha256'] == previous['targetSha256']
            assert sha256(ROOT / previous['source']) == previous['sourceSha256']
            identity = dict(processor='arm9', module='main', mode='arm', address=row['address'], bytes=8, targetSha256=row['targetSha256'])
            preferred = dict(source=row['source'], sourceSha256=row['sourceSha256'], report=report)
            evidence = f'evidence/abi/main-{key[2]:08x}-word-receiver-primary-migration-20261031.json'
            write_json(ROOT / evidence, dict(romSha256=configuration()['romSha256'], identity=identity,
                previous={field: previous[field] for field in ['source', 'sourceSha256', 'report']}, preferred=preferred,
                originalSourceUnchanged=True, nativeBytesUnchanged=True, newFunctionCredit=0, newByteCredit=0,
                sourceApiChange='Coherent full-word caller input view; original low-byte stores and pointer returns preserved',
                originalFormalTypesProven=False, behavioralReport=report, behavioralReportSha256=sha256(ROOT / report)))
            policy['preferences'].append(dict(**identity, **preferred, evidence=evidence, evidenceSha256=sha256(ROOT / evidence)))
            migrated.add(key)
    assert migrated == MIGRATIONS and len(policy['preferences']) == 74
    write_json(PREFERENCES, policy)
    verify_sources()
    original_preferences = source_selection.preferences
    with patch.object(source_selection, 'preferences', lambda namespace: original_preferences(namespace, path=PREFERENCES)):
        after, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and sha256(ROOT / 'source-preferences.json') == preference_hash
    for key, row in before.items():
        if key not in migrated:
            assert all(after[key][field] == row[field] for field in ['source', 'sourceSha256', 'object', 'objectSha256'])
    added = set(after) - set(before)
    assert len(added) == 29 and sum(after[key]['size'] for key in added) == 5558
    plan = {key: value for key, value in old.items() if key.startswith(('expectedInterpreted', 'expectedEmpty', 'expectedNonempty', 'expectedCopy'))}
    plan.update(schemaVersion=1, createdUtc=now(), reports=reports, interpretedReports=[],
        sourceRegistrySha256=sha256(TRANSACTION), sourcePreferenceSha256=sha256(PREFERENCES),
        interpretedRegistrySha256=sha256(ROOT / 'interpreted-recovery.json'), linksPending=True,
        newSourceFunctions=len(added), newOrdinaryCBytes=sum(after[key]['size'] for key in added), newSourceBytes=sum(after[key]['size'] for key in added), duplicateMigrationFunctions=2, duplicateMigrationBytes=16,
        expectedSourceMatchedFunctions=len(after), expectedSourceLinkedBytes=old['sourceLinkedBytes'] + sum(after[key]['size'] for key in added), preferredSourceInputsRequired=74,
        sourceReconstructionComplete=False, wholeRomMatchedFromSource=False, sourceOnlyRomProven=False,
        fullWindowsGameFromSourceProven=False, androidDeviceExecutionCount=0, previousAcceptedCohort=95,
        previousAcceptedFunctions=len(before), previousAcceptedBytes=old['sourceLinkedBytes'],
        allUnmigratedSourcesAndObjectsPreserved=True, fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT / 'evidence/verification/cohort-2026-10-29-96.json', plan)
    print(dict(newFunctions=len(added), newFunctionBytes=sum(after[key]['size'] for key in added), linksPending=True))


if __name__ == '__main__':
    current = ROOT / 'recovery.json'
    original = current.read_bytes()
    preferences = ROOT / 'source-preferences.json'
    original_policy = preferences.read_bytes()
    PREFERENCES.write_bytes(original_policy)
    TRANSACTION.parent.mkdir(parents=True, exist_ok=True)
    TRANSACTION.write_bytes(original)
    recovery_registry.REGISTRY = TRANSACTION
    main()
    assert current.read_bytes() == original and preferences.read_bytes() == original_policy
    if '--defer-publication' in sys.argv:
        print(dict(preparedTransactionOnly=True, currentRegistryUnchanged=True))
        raise SystemExit(0)
    write_text(preferences, PREFERENCES.read_text(encoding='utf-8-sig'))
    write_text(current, TRANSACTION.read_text(encoding='utf-8-sig'))
