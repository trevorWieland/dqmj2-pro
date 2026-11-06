from unittest.mock import patch
from project import ROOT, read_json, write_json, write_text, sha256, configuration, now
from recovery_registry import register, verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources
import source_selection

REGISTRY_TARGET = ROOT / 'work/integration/cohort84-recovery-transaction.json'
PREFERENCE_TARGET = ROOT / 'work/integration/cohort84-preference-transaction.json'
OLD_CARD = 'evidence/matches/arm7-lane-card-abi16-1252-20261031.json'
NEW_CARD = 'evidence/matches/arm7-lane-card-frontier2240-20261031.json'
PACKETS = [
    (NEW_CARD, 'match_arm7_lane_card_frontier_20261031.py', True),
    ('evidence/matches/ov001-20261031-phases257.json', 'match_ov001_phases257_20261031.py', False),
    ('evidence/matches/ov001-20261031-phases259.json', 'match_ov001_phases259_20261031.py', False),
    ('evidence/matches/ov001-20261031-query265.json', 'match_ov001_query265_20261031.py', False),
    ('evidence/matches/main-forwarded-interfaces-20261031.json', 'match_forwarded_interfaces_20261031.py', False),
    ('evidence/matches/mechanics-save-20261031-lane-creation-level-abi.json', 'match_mechanics_save_20261031_lane_creation_level_abi.py', False),
]


def identity(row, address):
    return dict(processor=row.get('processor', 'arm9'), module=row['module'], mode=row['mode'],
        address=hex(address), bytes=row.get('size', row.get('bytes')), targetSha256=row['targetSha256'])


def main():
    old = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-83.json')
    assert not old['linksPending'] and sha256(REGISTRY_TARGET) == old['sourceRegistrySha256']
    verify_sources()
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == 8945
    policies = read_json(ROOT / 'source-preferences.json')
    assert len(policies['preferences']) == 30
    registry = read_json(REGISTRY_TARGET)
    historical = [row for row in registry['batches'] if row['report'] == OLD_CARD]
    assert len(historical) == 1
    historical = historical[0]
    old_card = read_json(ROOT / OLD_CARD)
    assert len(old_card['matches']) == 9 and old_card['matchedInitializedBytes'] == 1252
    old_card_keys = {(row['module'], row['mode'], int(row['address'], 0)) for row in old_card['matches']}
    write_json(ROOT / 'evidence/verification/cohort84-before-adoption-20261031.json', dict(
        sourceRegistrySha256=sha256(REGISTRY_TARGET), preferencesSha256=sha256(ROOT / 'source-preferences.json'),
        selected=[dict(key=list(key), **{field: row[field] for field in
            ['name', 'module', 'mode', 'address', 'size', 'source', 'sourceSha256', 'object', 'objectSha256', 'targetSha256', 'report'] if field in row})
            for key, row in before.items()], historicalCardBatch=historical))
    main_migrations = set()
    for path, producer, raw in PACKETS:
        if raw:
            register(path, [producer])
        else:
            seal_sources(path, [producer])
            register(path, ['seal_recovery_sources_20261031.py', path, producer])
        if path not in ['evidence/matches/main-forwarded-interfaces-20261031.json',
            'evidence/matches/mechanics-save-20261031-lane-creation-level-abi.json']:
            continue
        for row in read_json(ROOT / path)['matches']:
            address = int(row['address'], 0)
            key = 'main', row['mode'], address
            prior = before[key]
            assert row['bytes'] == prior['size'] and row['targetSha256'] == prior['targetSha256']
            audit_path = f'evidence/abi/main-{address:08x}-explicit-forwarding-migration-20261031.json'
            preferred = {field: row[field] for field in ['source', 'sourceSha256']}
            preferred['report'] = path
            audit = dict(romSha256=configuration()['romSha256'], identity=identity(prior, address),
                previous={field: prior[field] for field in ['source', 'sourceSha256', 'report']}, preferred=preferred,
                originalSourceUnchanged=sha256(ROOT / prior['source']) == prior['sourceSha256'], nativeBytesUnchanged=True,
                newFunctionCredit=0, newByteCredit=0, sourceApiChange=row.get('interfaceMigration',
                    dict(qualifiedSignature=row.get('signature'), proofReport=path, historicalPrototypeProven=False)),
                historicalObjectHashes=dict(previous=prior['objectSha256'], preferred=row['objectSha256']))
            assert audit['originalSourceUnchanged']
            write_json(ROOT / audit_path, audit)
            policies['preferences'].append(dict(**audit['identity'], **preferred,
                evidence=audit_path, evidenceSha256=sha256(ROOT / audit_path)))
            main_migrations.add(key)
    assert len(main_migrations) == 31 and len(policies['preferences']) == 61
    registry = read_json(REGISTRY_TARGET)
    registry['batches'] = [row for row in registry['batches'] if row['report'] != OLD_CARD]
    assert not any(row['report'] == OLD_CARD for row in registry['oracles'])
    controls = 'evidence/verification/arm7-lane-card-abi16-1252-controls-20261031.json'
    insert = next(index for index, row in enumerate(registry['oracles']) if row['report'] == controls)
    registry['oracles'].insert(insert, dict(report=OLD_CARD, reproduce=historical['reproduce']))
    registry['oracles'].append(dict(report='evidence/verification/arm7-lane-card-frontier2240-controls-20261031.json',
        reproduce=['validate_arm7_lane_card_frontier_20261031.py']))
    write_json(REGISTRY_TARGET, registry)
    write_json(PREFERENCE_TARGET, policies)
    verify_sources()
    prior_preferences = source_selection.preferences
    with patch.object(source_selection, 'preferences', lambda namespace: prior_preferences(namespace, path=PREFERENCE_TARGET)):
        after, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    migrated = main_migrations | old_card_keys
    superseded = []
    for key, prior in before.items():
        current = after[key]
        assert sha256(ROOT / prior['source']) == prior['sourceSha256']
        assert sha256(ROOT / prior['object']) == prior['objectSha256']
        assert prior['size'] == current['size'] and prior.get('targetSha256') == current.get('targetSha256')
        if key not in migrated:
            assert all(prior[field] == current[field] for field in ['source', 'sourceSha256', 'object', 'objectSha256'])
        elif key in old_card_keys:
            assert (ROOT / prior['source']).read_bytes() == (ROOT / current['source']).read_bytes()
            superseded.append(dict(identity=identity(prior, key[2]),
                previous={field: prior[field] for field in ['source', 'sourceSha256', 'object', 'objectSha256', 'report']},
                preferred={field: current[field] for field in ['source', 'sourceSha256', 'object', 'objectSha256', 'report']},
                cBodyBytesUnchanged=True, newFunctionCredit=0, newByteCredit=0))
    assert len(superseded) == 9
    write_json(ROOT / 'evidence/abi/arm7-card-storage-batch-supersession-20261031.json', dict(
        romSha256=configuration()['romSha256'], previousSourceBatch=historical, previousReport=OLD_CARD,
        preferredReport=NEW_CARD, migrations=superseded, previousProducerRetainedAsOracleBeforeControls=True,
        oldSourcesObjectsAndMatchEvidencePreserved=True, frozenSelectionAndLinkEnginesChanged=False,
        newFunctionCredit=0, newByteCredit=0))
    added = set(after) - set(before)
    new_bytes = sum(after[key]['size'] for key in added)
    assert len(added) == 11 and new_bytes == 2564
    plan = {key: value for key, value in old.items() if key.startswith(('expectedInterpreted', 'expectedEmpty', 'expectedNonempty', 'expectedCopy'))}
    plan.update(schemaVersion=1, createdUtc=now(), reports=[path for path, _, _ in PACKETS], interpretedReports=[],
        sourceRegistrySha256=sha256(REGISTRY_TARGET), sourcePreferenceSha256=sha256(PREFERENCE_TARGET),
        interpretedRegistrySha256=sha256(ROOT / 'interpreted-recovery.json'), linksPending=True,
        newSourceFunctions=11, newOrdinaryCBytes=2564, newSourceBytes=2564, newMathematicalDataBytes=0,
        duplicateMigrationFunctions=40, duplicateMigrationBytes=1724, arm7RegistrySupersessionFunctions=9,
        expectedSourceMatchedFunctions=8956, expectedSourceLinkedBytes=671873, preferredSourceInputsRequired=61,
        sourceReconstructionComplete=False, wholeRomMatchedFromSource=False, sourceOnlyRomProven=False,
        fullWindowsGameFromSourceProven=False, androidDeviceExecutionCount=0, previousAcceptedCohort=83,
        previousAcceptedFunctions=len(before), previousAcceptedBytes=old['sourceLinkedBytes'],
        allUnmigratedSourcesAndObjectsPreserved=True, fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT / 'evidence/verification/cohort-2026-10-29-84.json', plan)
    print(dict(newFunctions=11, newOrdinaryCBytes=2564, zeroCoverageMigrations=40, preferences=61, linksPending=True))


if __name__ == '__main__':
    import recovery_registry
    current = ROOT / 'recovery.json'
    preferences = ROOT / 'source-preferences.json'
    original_registry, original_preferences = current.read_bytes(), preferences.read_bytes()
    REGISTRY_TARGET.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_TARGET.write_bytes(original_registry)
    recovery_registry.REGISTRY = REGISTRY_TARGET
    main()
    assert current.read_bytes() == original_registry and preferences.read_bytes() == original_preferences
    write_text(current, REGISTRY_TARGET.read_text(encoding='utf-8-sig'))
    write_text(preferences, PREFERENCE_TARGET.read_text(encoding='utf-8-sig'))
    print(dict(registryAndPreferencesPublished=True))
