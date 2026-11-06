import argparse
from project import ROOT, read_json, sha256
import recovery_registry
from recovery_registry import verify_sources


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    options = parser.parse_args()
    cohort = options.cohort
    old = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort - 1}.json')
    plan = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json')
    registry = ROOT / 'recovery.json'
    policy = ROOT / 'source-preferences.json'
    prepared = ROOT / f'work/integration/cohort{cohort}-recovery-transaction.json'
    preferences = ROOT / f'work/integration/cohort{cohort}-preference-transaction.json'
    assert not old['linksPending'] and plan['linksPending']
    assert plan['previousAcceptedCohort'] == cohort - 1
    assert sha256(ROOT / plan['specification']) == plan['specificationSha256']
    assert read_json(ROOT / plan['specification'])['migrations']
    proof = read_json(ROOT / f'evidence/verification/cohort{cohort - 1}-expanded-source-closure-20261101.json')
    assert proof['passed'] and proof['cohort'] == cohort - 1
    for item in proof['reports']:
        assert sha256(ROOT / item['path']) == item['sha256']
    from select_committed_migration_predecessor_audit_v7_20261106 import select
    audit = select(cohort - 1, proof)
    assert any(item['path'] == audit.relative_to(ROOT).as_posix() and item['sha256'] == sha256(audit) for item in proof['reports'])
    assert read_json(audit)['passed']
    assert read_json(ROOT / f'evidence/verification/cohort{cohort - 1}-captured-oracle-closure-verification-20261031.json')['committedVerification']['passed']
    assert sha256(registry) == old['sourceRegistrySha256']
    assert sha256(policy) == old['sourcePreferenceSha256']
    assert sha256(prepared) == plan['sourceRegistrySha256']
    assert sha256(preferences) == plan['sourcePreferenceSha256']
    recovery_registry.REGISTRY = prepared
    verify_sources()
    previous_registry, previous_policy = registry.read_bytes(), policy.read_bytes()
    try:
        policy.write_bytes(preferences.read_bytes())
        registry.write_bytes(prepared.read_bytes())
        assert sha256(registry) == plan['sourceRegistrySha256']
        assert sha256(policy) == plan['sourcePreferenceSha256']
    except BaseException:
        registry.write_bytes(previous_registry)
        policy.write_bytes(previous_policy)
        raise
    print(dict(published=True, cohort=cohort, functionsPending=plan['newSourceFunctions'], bytesPending=plan['newSourceBytes']))


if __name__ == '__main__':
    main()
