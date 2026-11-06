from project import ROOT, read_json, write_json, sha256, configuration, now
from recovery_registry import register, verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS = [
    ('arm7-lane-node-initialization216-20261031', 'match_arm7_lane_node_initialization216_20261031.py', True),
    ('mechanics-save-20261031-lane-initializer-query', 'match_mechanics_save_20261031_lane_initializer_query.py', False),
    ('mechanics-save-20261031-lane-mask-merge', 'match_mechanics_save_20261031_lane_mask_merge.py', False),
    ('ov005-20261031-callbacks300-linked', 'adapt_ov005_callbacks300_linked_20261031.py', False),
    ('main-word-stream-20261031', 'match_main_word_stream_20261031.py', False),
    ('main-list-operations-20261031', 'match_main_list_operations_20261031.py', False),
    ('main-context-installers-20261031', 'match_main_context_installers_20261031.py', False),
]
REGISTRY_TARGET = ROOT / 'work/integration/cohort88-recovery-transaction.json'


def main():
    old = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-87.json')
    verify_sources()
    assert not old['linksPending']
    assert sha256(REGISTRY_TARGET) == old['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == old['sourcePreferenceSha256']
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == 8984
    fields = ['module', 'mode', 'address', 'size', 'source', 'sourceSha256',
              'object', 'objectSha256', 'targetSha256', 'report']
    write_json(ROOT / 'evidence/verification/cohort88-before-adoption-20261031.json', dict(
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
    oracles = {row['report']: row for row in registry['oracles']}
    for report, producer in [
        ('evidence/verification/arm7-lane-node-initialization216-controls-20261031.json',
         'validate_arm7_lane_node_initialization216_20261031.py'),
        ('evidence/verification/main-pointer-clear299-20261031.json', 'probe_main_pointer_clear299_20261031.py'),
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
    assert len(added) == 14 and new_bytes == 1740, (len(added), new_bytes)
    plan = {key: value for key, value in old.items()
            if key.startswith(('expectedInterpreted', 'expectedEmpty', 'expectedNonempty', 'expectedCopy'))}
    plan.update(schemaVersion=1, createdUtc=now(), reports=reports, interpretedReports=[],
                sourceRegistrySha256=sha256(REGISTRY_TARGET),
                sourcePreferenceSha256=sha256(ROOT / 'source-preferences.json'),
                interpretedRegistrySha256=sha256(ROOT / 'interpreted-recovery.json'), linksPending=True,
                newSourceFunctions=14, newOrdinaryCBytes=1740, newSourceBytes=1740,
                newSymbolicInitializedDataBytes=0, newMathematicalDataBytes=0,
                duplicateMigrationFunctions=0, duplicateMigrationBytes=0,
                expectedSourceMatchedFunctions=8998, expectedSourceLinkedBytes=677763,
                preferredSourceInputsRequired=61, sourceReconstructionComplete=False,
                wholeRomMatchedFromSource=False, sourceOnlyRomProven=False,
                fullWindowsGameFromSourceProven=False, androidDeviceExecutionCount=0,
                previousAcceptedCohort=87, previousAcceptedFunctions=len(before),
                previousAcceptedBytes=old['sourceLinkedBytes'],
                allUnmigratedSourcesAndObjectsPreserved=True, fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT / 'evidence/verification/cohort-2026-10-29-88.json', plan)
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
