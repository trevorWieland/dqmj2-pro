from project import ROOT, read_json, sha256
import recovery_registry
from recovery_registry import verify_sources


def main():
    old = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-98.json')
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-99.json')
    registry = ROOT / 'recovery.json'
    policy = ROOT / 'source-preferences.json'
    prepared = ROOT / 'work/integration/cohort99-recovery-transaction.json'
    preferences = ROOT / 'work/integration/cohort99-preference-transaction.json'
    assert not old['linksPending'] and plan['linksPending']
    assert sha256(ROOT / plan['specification']) == plan['specificationSha256']
    proof = read_json(ROOT / 'evidence/verification/cohort98-expanded-source-closure-20261101.json')
    assert proof['passed'] and proof['cohort'] == 98
    for item in proof['reports']:
        assert sha256(ROOT / item['path']) == item['sha256']
    assert read_json(ROOT / 'evidence/verification/cohort98-committed-source-inputs-v3-20261031.json')['passed']
    assert read_json(ROOT / 'evidence/verification/cohort98-captured-oracle-closure-verification-20261031.json')['committedVerification']['passed']
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
    print(dict(published=True, functionsPending=plan['newSourceFunctions'], bytesPending=plan['newSourceBytes']))


if __name__ == '__main__':
    main()
