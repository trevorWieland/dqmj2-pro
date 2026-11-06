import copy
import shutil
from unittest.mock import patch
from project import ROOT, read_json, write_json, write_text, sha256, configuration
import recovery_registry
import source_selection
from recovery_registry import register, verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

CHANGES = {
    'evidence/matches/mechanics-save-20261031-lane-packed-classify.json':
        'evidence/matches/mechanics-save-20261031-lane-packed-classify-host-bindings.json',
    'evidence/matches/mechanics-save-20261031-lane-packed-pointer-abi.json':
        'evidence/matches/mechanics-save-20261031-lane-packed-pointer-abi-host-bindings.json',
}


def main():
    verify_sources()
    registry_path, policy_path = ROOT / 'recovery.json', ROOT / 'source-preferences.json'
    registry_sha, policy_sha = sha256(registry_path), sha256(policy_path)
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == 9018
    original_policy = read_json(policy_path)
    assert len(original_policy['preferences']) == 67
    archive = ROOT / 'evidence/verification/cohort91-first-bindings'
    archive.mkdir(parents=True, exist_ok=True)
    for path in [registry_path, policy_path, ROOT / 'evidence/verification/cohort-2026-10-29-91.json']:
        target = archive / path.name
        if target.exists():
            assert sha256(target) == sha256(path)
        else:
            shutil.copy2(path, target)
    transaction = ROOT / 'work/integration/cohort91-binding-repair-registry.json'
    preference = ROOT / 'work/integration/cohort91-binding-repair-preferences.json'
    registry = read_json(registry_path)
    assert sum(batch['report'] in CHANGES for batch in registry['batches']) == 2
    registry['batches'] = [batch for batch in registry['batches'] if batch['report'] not in CHANGES]
    write_json(transaction, registry)
    recovery_registry.REGISTRY = transaction
    for new in CHANGES.values():
        seal_sources(new, ['adapt_packed_pointer_host_bindings_20261031.py'])
        register(new, ['seal_recovery_sources_20261031.py', new, 'adapt_packed_pointer_host_bindings_20261031.py'])
    policy = copy.deepcopy(original_policy)
    count = 0
    for row in policy['preferences']:
        if row['report'] not in CHANGES:
            continue
        audit_path = ROOT / row['evidence']
        prior_copy = archive / audit_path.name
        if prior_copy.exists():
            assert sha256(prior_copy) == sha256(audit_path)
        else:
            shutil.copy2(audit_path, prior_copy)
        audit = read_json(audit_path)
        row['report'] = CHANGES[row['report']]
        audit['preferred']['report'] = row['report']
        audit['integrationBindingRepair'] = dict(adapter='adapt_packed_pointer_host_bindings_20261031.py',
            sourceAndObjectUnchanged=True, additionalSourceCredit=0)
        new_audit = audit_path.with_name(audit_path.stem + '-host-bindings.json')
        write_json(new_audit, audit)
        row['evidence'] = new_audit.relative_to(ROOT).as_posix()
        row['evidenceSha256'] = sha256(new_audit)
        count += 1
    assert count == 6
    write_json(preference, policy)
    original_preferences = source_selection.preferences
    with patch.object(source_selection, 'preferences', lambda namespace: original_preferences(namespace, path=preference)):
        after, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and set(after) == set(before)
    for key, old in before.items():
        assert all(after[key].get(field) == old.get(field) for field in ['source', 'sourceSha256', 'object', 'objectSha256', 'size', 'targetSha256'])
    plan_path = ROOT / 'evidence/verification/cohort-2026-10-29-91.json'
    plan = read_json(plan_path)
    plan['reports'] = [CHANGES.get(path, path) for path in plan['reports']]
    plan.update(sourceRegistrySha256=sha256(transaction), sourcePreferenceSha256=sha256(preference),
                hostBindingRepair=dict(adapter='adapt_packed_pointer_host_bindings_20261031.py',
                    frameworkModified=False, scopeKeysAligned=7, unchangedSelectedFunctions=len(after), sourceCredit=0))
    assert sha256(registry_path) == registry_sha and sha256(policy_path) == policy_sha
    write_text(policy_path, preference.read_text(encoding='utf-8-sig'))
    write_text(registry_path, transaction.read_text(encoding='utf-8-sig'))
    write_json(plan_path, plan)
    verify_sources()
    print(dict(selectedFunctionsPreserved=len(after), unchangedSourceAndObjectBytes=True, scopeKeysAligned=7, linksPending=True))


if __name__ == '__main__':
    main()
