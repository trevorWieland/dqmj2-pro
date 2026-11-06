import argparse
import subprocess
import sys
from unittest.mock import patch
import source_selection
from project import ROOT, configuration, read_json, write_json, sha256, now
import recovery_registry
from recovery_registry import register, verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    options = parser.parse_args()
    spec_path = ROOT / options.specification
    spec = read_json(spec_path)
    cohort, previous = spec['cohort'], spec['previousAcceptedCohort']
    assert cohort == previous + 1 and spec.get('migrations')
    current = ROOT / 'recovery.json'
    policy = ROOT / 'source-preferences.json'
    original_registry, original_policy = current.read_bytes(), policy.read_bytes()
    old = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{previous}.json')
    assert not old['linksPending'] and sha256(current) == old['sourceRegistrySha256']
    assert sha256(policy) == old['sourcePreferenceSha256']
    transaction = ROOT / f'work/integration/cohort{cohort}-recovery-transaction.json'
    transaction.parent.mkdir(parents=True, exist_ok=True)
    transaction.write_bytes(original_registry)
    preferences_path = ROOT / f'work/integration/cohort{cohort}-preference-transaction.json'
    preferences_path.write_bytes(original_policy)
    recovery_registry.REGISTRY = transaction
    verify_sources()
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == old['sourceMatchedFunctions']
    fields = ['source', 'sourceSha256', 'object', 'objectSha256', 'size', 'targetSha256', 'report']
    write_json(ROOT / f'evidence/verification/cohort{cohort}-before-adoption-20261101.json', dict(
        registrySha256=sha256(transaction), preferencesSha256=sha256(policy),
        selected=[dict(key=list(key), **{field: row.get(field) for field in fields}) for key, row in sorted(before.items())]))
    reports = []
    for packet in spec['packets']:
        report, producer = packet['report'], packet['producer']
        if packet.get('directProducer'):
            register(report, producer)
        else:
            seal_sources(report, producer)
            register(report, ['seal_recovery_sources_20261031.py', report, *producer])
        reports.append(report)
    for command in spec.get('postSealCommands', []):
        subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT, check=True)
    registry = read_json(transaction)
    oracles = {item['report']: item for item in registry['oracles']}
    for item in spec.get('oracles', []):
        assert (ROOT / item['report']).is_file()
        oracles[item['report']] = item
    registry['oracles'] = list(oracles.values())
    write_json(transaction, registry)
    migrated = set()
    proposed = {(item['module'], item['mode'], int(item['address'], 0)): item for item in spec['migrations']}
    policies = read_json(policy)
    migration_reports = []
    for report in reports:
        for row in read_json(ROOT / report).get('matches', []):
            key = row['module'], row['mode'], int(row['address'], 0)
            if key not in proposed:
                continue
            assert key not in migrated and row['processor'] == 'arm9' and not row.get('program')
            prior = before[key]
            assert row['bytes'] == prior['size'] == proposed[key]['bytes']
            assert row['targetSha256'] == prior['targetSha256']
            assert sha256(ROOT / prior['source']) == prior['sourceSha256']
            identity = dict(processor='arm9', module=row['module'], mode=row['mode'], address=row['address'], bytes=row['bytes'], targetSha256=row['targetSha256'])
            preferred = dict(source=row['source'], sourceSha256=row['sourceSha256'], report=report)
            evidence = f'evidence/abi/{row["module"]}-{key[2]:08x}-explicit-input-migration-20261101.json'
            write_json(ROOT / evidence, dict(romSha256=configuration()['romSha256'], identity=identity,
                previous={field: prior[field] for field in ['source', 'sourceSha256', 'report']}, preferred=preferred,
                originalSourceUnchanged=True, nativeBytesUnchanged=True, newFunctionCredit=0, newByteCredit=0,
                sourceApiChange=proposed[key]['reason'], originalFormalTypesProven=False,
                behavioralReport=report, behavioralReportSha256=sha256(ROOT / report)))
            policies['preferences'].append(dict(**identity, **preferred, evidence=evidence, evidenceSha256=sha256(ROOT / evidence)))
            migrated.add(key)
            migration_reports.append(evidence)
    assert migrated == set(proposed)
    write_json(preferences_path, policies)
    verify_sources()
    original_preferences = source_selection.preferences
    with patch.object(source_selection, 'preferences', lambda namespace: original_preferences(namespace, path=preferences_path)):
        after, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    for key, row in before.items():
        if key in migrated:
            continue
        assert all(after[key][field] == row[field] for field in ['source', 'sourceSha256', 'object', 'objectSha256'])
    added = set(after) - set(before)
    expected = {(item['module'], item['mode'], int(item['address'], 0)): item['bytes'] for item in spec['expectedAdditions']}
    assert added == set(expected)
    assert all(after[key]['size'] == expected[key] for key in added)
    delta = sum(after[key]['size'] for key in added)
    plan = {key: value for key, value in old.items() if key.startswith(('expectedInterpreted', 'expectedEmpty', 'expectedNonempty', 'expectedCopy'))}
    plan.update(schemaVersion=1, createdUtc=now(), reports=reports, interpretedReports=[],
        specification=options.specification, specificationSha256=sha256(spec_path), sourceRegistrySha256=sha256(transaction),
        sourcePreferenceSha256=sha256(preferences_path), interpretedRegistrySha256=sha256(ROOT / 'interpreted-recovery.json'),
        linksPending=True, newSourceFunctions=len(added), newOrdinaryCBytes=delta, newSourceBytes=delta,
        duplicateMigrationFunctions=len(migrated), duplicateMigrationBytes=sum(before[key]['size'] for key in migrated), migrationReports=migration_reports, expectedSourceMatchedFunctions=len(after),
        expectedSourceLinkedBytes=old['sourceLinkedBytes'] + delta,
        preferredSourceInputsRequired=len(policies['preferences']), sourceReconstructionComplete=False,
        wholeRomMatchedFromSource=False, sourceOnlyRomProven=False, fullWindowsGameFromSourceProven=False,
        androidDeviceExecutionCount=0, previousAcceptedCohort=previous, previousAcceptedFunctions=len(before),
        previousAcceptedBytes=old['sourceLinkedBytes'], allUnmigratedSourcesAndObjectsPreserved=True, originalMigratedSourcesPreserved=True,
        fullCleanReplayOfThisCohortProven=False, transactionPreparedOnly=True)
    write_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json', plan)
    assert current.read_bytes() == original_registry and policy.read_bytes() == original_policy
    print(dict(cohort=cohort, newFunctions=len(added), newBytes=delta, transactionPreparedOnly=True))


if __name__ == '__main__':
    main()
