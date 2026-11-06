from project import ROOT, read_json, write_json, sha256, configuration, now
from recovery_registry import register, verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS = [
    ('main-numeric-dispatch-20261031', 'match_main_numeric_dispatch_20261031.py', False),
    ('mechanics-save-20261031-lane-group-validation', 'match_mechanics_save_20261031_lane_group_validation.py', False),
    ('mechanics-save-20261031-lane-sequence-adapter', 'match_mechanics_save_20261031_lane_sequence_adapter.py', False),
]
REGISTRY_TARGET = ROOT / 'work/integration/cohort90-recovery-transaction.json'


def main():
    old = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-89.json')
    verify_sources()
    assert not old['linksPending']
    assert sha256(REGISTRY_TARGET) == old['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == old['sourcePreferenceSha256']
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == 9007
    fields = ['module', 'mode', 'address', 'size', 'source', 'sourceSha256',
              'object', 'objectSha256', 'targetSha256', 'report']
    write_json(ROOT / 'evidence/verification/cohort90-before-adoption-20261031.json', dict(
        sourceRegistrySha256=sha256(REGISTRY_TARGET), preferencesSha256=sha256(ROOT / 'source-preferences.json'),
        selected=[dict(key=list(key), **{field: row[field] for field in fields if field in row})
                  for key, row in before.items()]))
    reports = []
    for name, producer, raw in PACKETS:
        path = f'evidence/matches/{name}.json'
        if raw:
            register(path, [producer])
        else:
            seal_sources(path, [producer])
            register(path, ['seal_recovery_sources_20261031.py', path, producer])
        reports.append(path)
    registry = read_json(REGISTRY_TARGET)
    removed = {
        'evidence/verification/arm7-seq-main-proposed-controls-20261030.json',
        'evidence/verification/arm7-lane-child-counter-controls-20261031.json',
    }
    assert removed <= {row['report'] for row in registry['oracles']}
    oracles = {row['report']: row for row in registry['oracles'] if row['report'] not in removed}
    for report, producer in [
        ('evidence/verification/arm7-seq-main-proposed-clean-replay-20261031.json',
         'replay_arm7_seq_main_proposed_clean_20261031.py'),
        ('evidence/verification/arm7-child-counter-clean-replay-20261031.json',
         'replay_arm7_child_counter_clean_20261031.py'),
        ('evidence/portability/main-numeric-dispatch-windows32-20261031.json',
         'check_main_numeric_dispatch_windows32_20261031.py'),
        ('evidence/functional/mechanics-save-item-effect-chain-20261031.json',
         'prove_save_core_item_effect_chain_20261031.py'),
    ]:
        assert (ROOT / report).is_file(), report
        oracles[report] = dict(report=report, reproduce=[producer])
    registry['oracles'] = list(oracles.values())
    write_json(REGISTRY_TARGET, registry)
    verify_sources()
    after, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    for key, row in before.items():
        assert all(after[key][field] == row[field] for field in
                   ['source', 'sourceSha256', 'object', 'objectSha256', 'report'])
    added = set(after) - set(before)
    new_bytes = sum(after[key]['size'] for key in added)
    assert len(added) == 3 and new_bytes == 720, (len(added), new_bytes)
    plan = {key: value for key, value in old.items()
            if key.startswith(('expectedInterpreted', 'expectedEmpty', 'expectedNonempty', 'expectedCopy'))}
    plan.update(schemaVersion=1, createdUtc=now(), reports=reports, interpretedReports=[],
                sourceRegistrySha256=sha256(REGISTRY_TARGET),
                sourcePreferenceSha256=sha256(ROOT / 'source-preferences.json'),
                interpretedRegistrySha256=sha256(ROOT / 'interpreted-recovery.json'), linksPending=True,
                newSourceFunctions=3, newOrdinaryCBytes=720, newSourceBytes=720,
                newSymbolicInitializedDataBytes=0, newMathematicalDataBytes=0,
                duplicateMigrationFunctions=0, duplicateMigrationBytes=0,
                expectedSourceMatchedFunctions=9010, expectedSourceLinkedBytes=679219,
                preferredSourceInputsRequired=61, sourceReconstructionComplete=False,
                wholeRomMatchedFromSource=False, sourceOnlyRomProven=False,
                fullWindowsGameFromSourceProven=False, androidDeviceExecutionCount=0,
                previousAcceptedCohort=89, previousAcceptedFunctions=len(before),
                previousAcceptedBytes=old['sourceLinkedBytes'],
                zeroCreditOracleReplacements=sorted(removed),
                originalFrozenMatchersAndValidatorsUnchanged=True,
                allUnmigratedSourcesAndObjectsPreserved=True, fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT / 'evidence/verification/cohort-2026-10-29-90.json', plan)
    print(dict(newFunctions=len(added), newOrdinaryCBytes=new_bytes,
               allPriorSourcesAndObjectsPreserved=True, linksPending=True))


if __name__ == '__main__':
    import recovery_registry
    from project import write_text
    current = ROOT / 'recovery.json'
    before = current.read_bytes()
    before_sha = sha256(current)
    REGISTRY_TARGET.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_TARGET.write_bytes(before)
    recovery_registry.REGISTRY = REGISTRY_TARGET
    main()
    assert sha256(current) == before_sha, 'Concurrent registry change prevents publication'
    write_text(current, REGISTRY_TARGET.read_text(encoding='utf-8-sig'))
    assert sha256(current) == sha256(REGISTRY_TARGET)
    print(dict(registryPublishedAtomically=True))
