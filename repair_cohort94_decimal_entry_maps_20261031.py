import shutil
from project import ROOT, configuration, read_json, write_json, write_text, sha256
from ledger_state import collect_matches
import recovery_registry
from recovery_registry import register, verify_sources
from seal_recovery_sources_20261031 import seal_sources


CHANGES = {f'evidence/matches/main-decimal-{name}-20261031.json':
    (f'evidence/matches/main-decimal-{name}-20261031-host-bindings.json', unit)
    for name, unit in [('pow2', 'pow2'), ('from-double', 'from-double')]}


def main():
    verify_sources()
    current = ROOT / 'recovery.json'
    before_sha = sha256(current)
    preference_sha = sha256(ROOT / 'source-preferences.json')
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == 9053
    archive = ROOT / 'evidence/verification/cohort94-first-entry-maps'
    archive.mkdir(parents=True, exist_ok=True)
    plan_path = ROOT / 'evidence/verification/cohort-2026-10-29-94.json'
    for path in [current, ROOT / 'source-preferences.json', plan_path,
                 ROOT / 'evidence/verification/cohort94-validation-driver.json']:
        target = archive / path.name
        assert not target.exists() or sha256(target) == sha256(path)
        if not target.exists():
            shutil.copyfile(path, target)
    registry = read_json(current)
    assert sum(row['report'] in CHANGES for row in registry['batches']) == 2
    registry['batches'] = [row for row in registry['batches'] if row['report'] not in CHANGES]
    transaction = ROOT / 'work/integration/cohort94-entry-map-repair-registry.json'
    write_json(transaction, registry)
    recovery_registry.REGISTRY = transaction
    for target, unit in CHANGES.values():
        command = ['adapt_main_decimal_host_entries_20261031.py', unit]
        seal_sources(target, command)
        register(target, ['seal_recovery_sources_20261031.py', target, *command])
    after, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and set(after) == set(before)
    for key, row in before.items():
        assert all(after[key].get(field) == row.get(field) for field in
            ['source', 'sourceSha256', 'object', 'objectSha256', 'size', 'targetSha256'])
    plan = read_json(plan_path)
    plan['reports'] = [CHANGES[path][0] if path in CHANGES else path for path in plan['reports']]
    plan.update(sourceRegistrySha256=sha256(transaction), entryMapMetadataRepair=dict(
        adapter='adapt_main_decimal_host_entries_20261031.py', repairedReports=2,
        frozenFrameworkModified=False, selectedSourcesAndObjectsPreserved=9053, sourceCredit=0))
    assert sha256(current) == before_sha and sha256(ROOT / 'source-preferences.json') == preference_sha
    write_text(current, transaction.read_text(encoding='utf-8-sig'))
    write_json(plan_path, plan)
    verify_sources()
    print(dict(preservedFunctions=9053, metadataReportsRepaired=2, linksPending=True))


if __name__ == '__main__':
    main()
