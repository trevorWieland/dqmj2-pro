import argparse
from project import ROOT, read_json, sha256
from select_source_input_closure_v2_20261105 import select
import recovery_registry
from recovery_registry import verify_sources


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    options = parser.parse_args()
    cohort = options.cohort
    old = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort - 1}.json')
    plan = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json')
    specification = read_json(ROOT / plan['specification'])
    assert not specification.get('migrations')
    assert sha256(ROOT / plan['specification']) == plan['specificationSha256']
    registry = ROOT / 'recovery.json'
    policy = ROOT / 'source-preferences.json'
    prepared = ROOT / f'work/integration/cohort{cohort}-recovery-transaction.json'
    assert not old['linksPending'] and plan['linksPending']
    assert sha256(registry) == old['sourceRegistrySha256']
    assert sha256(policy) == old['sourcePreferenceSha256'] == plan['sourcePreferenceSha256']
    assert sha256(prepared) == plan['sourceRegistrySha256']
    expanded = read_json(ROOT / f'evidence/verification/cohort{cohort - 1}-expanded-source-closure-20261101.json')
    assert expanded['passed']
    for item in expanded['reports']:
        assert sha256(ROOT / item['path']) == item['sha256']
    relative_audit = select(expanded, cohort - 1)
    input_audit = relative_audit.rsplit('/', 1)[1]
    for name in [input_audit, f'cohort{cohort - 1}-captured-oracle-closure-verification-20261031.json']:
        proof = read_json(ROOT / 'evidence/verification' / name)
        assert proof.get('passed', proof.get('committedVerification', {}).get('passed'))
    recovery_registry.REGISTRY = prepared
    verify_sources()
    previous = registry.read_bytes()
    try:
        registry.write_bytes(prepared.read_bytes())
        assert sha256(registry) == plan['sourceRegistrySha256']
    except BaseException:
        registry.write_bytes(previous)
        raise
    print(dict(published=True, cohort=cohort, functionsPending=plan['newSourceFunctions'],
               bytesPending=plan['newSourceBytes'], preferencesUnchanged=True))


if __name__ == '__main__':
    main()
