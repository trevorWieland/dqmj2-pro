from project import ROOT, read_json, sha256
import recovery_registry
from recovery_registry import verify_sources


def main():
    old = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-95.json')
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-96.json')
    registry = ROOT / 'recovery.json'
    policy = ROOT / 'source-preferences.json'
    prepared = ROOT / 'work/integration/cohort96-recovery-transaction.json'
    preferences = ROOT / 'work/integration/cohort96-preference-transaction.json'
    assert not old['linksPending'] and plan['linksPending']
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
