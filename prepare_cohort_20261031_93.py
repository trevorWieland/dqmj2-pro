from project import ROOT, read_json, write_json, write_text, sha256, configuration, now
from recovery_registry import register, verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources


PACKETS = [
    ('evidence/matches/main-decimal-subtract-20261031.json', 'match_main_decimal_subtract_20261031.py'),
    ('evidence/matches/main-decimal-family-20261031.json', 'match_main_decimal_family_20261031.py'),
    ('evidence/matches/main-decimal-round-direction-20261031.json', 'match_main_decimal_round_direction_20261031.py'),
    ('evidence/matches/mechanics-save-20261031-lane-thread-commands.json', 'match_mechanics_save_20261031_lane_thread_commands.py'),
    ('evidence/matches/mechanics-save-20261031-lane-roster-actions.json', 'match_mechanics_save_20261031_lane_roster_actions.py'),
    ('evidence/matches/ov001-20261031-recruit353.json', 'match_ov001_recruit353_20261031.py'),
    ('evidence/matches/ov001-20261031-recruit360.json', 'match_ov001_recruit360_20261031.py'),
    ('evidence/matches/arm7-child-crc-table32-integrated-20261031.json', 'adapt_arm7_crc_table32_report_20261031.py'),
]
ORACLES = [
    ('evidence/verification/arm7-crc-table32-controls-20261031.json', 'validate_arm7_crc_table32_20261031.py'),
    ('evidence/verification/signed-division341-compiler-20261031.json', 'probe_signed_division341_20261031.py'),
    ('evidence/verification/main-row43-347-native-20261031.json', 'probe_main_row43_347_20261031.py'),
    ('evidence/application/ov001-template349-functional-20261031.json', 'prove_ov001_template349_20261031.py'),
]
TRANSACTION = ROOT / 'work/integration/cohort93-recovery-transaction.json'


def main():
    old = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-92.json')
    verify_sources()
    assert not old['linksPending'] and sha256(TRANSACTION) == old['sourceRegistrySha256']
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == 9032
    preferences_sha = sha256(ROOT / 'source-preferences.json')
    assert len(read_json(ROOT / 'source-preferences.json')['preferences']) == 68
    fields = ['module', 'mode', 'address', 'size', 'source', 'sourceSha256', 'object', 'objectSha256', 'targetSha256', 'report']
    write_json(ROOT / 'evidence/verification/cohort93-before-adoption-20261031.json', dict(
        sourceRegistrySha256=sha256(TRANSACTION), sourcePreferencesSha256=preferences_sha,
        selected=[dict(key=list(key), **{field: row[field] for field in fields if field in row}) for key, row in before.items()]))
    for report, producer in PACKETS:
        seal_sources(report, [producer])
        register(report, ['seal_recovery_sources_20261031.py', report, producer])
    registry = read_json(TRANSACTION)
    oracles = {row['report']: row for row in registry['oracles']}
    for report, producer in ORACLES:
        assert (ROOT / report).is_file()
        oracles[report] = dict(report=report, reproduce=[producer])
    registry['oracles'] = sorted(oracles.values(), key=lambda row: row['report'])
    write_json(TRANSACTION, registry)
    verify_sources()
    after, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and sha256(ROOT / 'source-preferences.json') == preferences_sha
    for key, row in before.items():
        assert all(after[key][field] == row[field] for field in ['source', 'sourceSha256', 'object', 'objectSha256'])
    added = set(after) - set(before)
    code_bytes = sum(after[key]['size'] for key in added)
    assert len(added) == 11 and code_bytes == 3360
    data = read_json(ROOT / PACKETS[-1][0])['dataMatches']
    assert len(data) == 1 and data[0]['bytes'] == 32 and data[0]['mode'] == 'data'
    assert data[0]['ordinaryFunctionCredit'] == 0 and data[0]['kind'] == 'data'
    plan = {key: value for key, value in old.items() if key.startswith(('expectedInterpreted', 'expectedEmpty', 'expectedNonempty', 'expectedCopy'))}
    plan.update(schemaVersion=1, createdUtc=now(), reports=[row[0] for row in PACKETS], interpretedReports=[],
        sourceRegistrySha256=sha256(TRANSACTION), sourcePreferenceSha256=preferences_sha,
        interpretedRegistrySha256=sha256(ROOT / 'interpreted-recovery.json'), linksPending=True,
        newSourceFunctions=11, newOrdinaryCBytes=3360, newSourceBytes=3392, newMathematicalDataBytes=32,
        duplicateMigrationFunctions=0, duplicateMigrationBytes=0, expectedSourceMatchedFunctions=9043,
        expectedSourceLinkedBytes=684333, preferredSourceInputsRequired=68, sourceReconstructionComplete=False,
        wholeRomMatchedFromSource=False, sourceOnlyRomProven=False, fullWindowsGameFromSourceProven=False,
        androidDeviceExecutionCount=0, previousAcceptedCohort=92, previousAcceptedFunctions=len(before),
        previousAcceptedBytes=old['sourceLinkedBytes'], allUnmigratedSourcesAndObjectsPreserved=True,
        fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT / 'evidence/verification/cohort-2026-10-29-93.json', plan)
    print(dict(newFunctions=len(added), newOrdinaryCBytes=code_bytes, newDataBytes=32, linksPending=True))


if __name__ == '__main__':
    import recovery_registry
    current = ROOT / 'recovery.json'
    before = current.read_bytes()
    before_sha = sha256(current)
    TRANSACTION.parent.mkdir(parents=True, exist_ok=True)
    TRANSACTION.write_bytes(before)
    recovery_registry.REGISTRY = TRANSACTION
    main()
    assert sha256(current) == before_sha, 'Concurrent registry change prevents publication'
    write_text(current, TRANSACTION.read_text(encoding='utf-8-sig'))
    assert sha256(current) == sha256(TRANSACTION)
