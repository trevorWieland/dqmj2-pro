import argparse
from unittest.mock import patch
import recovery_registry
from project import ROOT, read_json, sha256
from select_source_input_closure_v3_20261105 import select

def closed_binding(cohort):
    old = read_json(ROOT/f'evidence/verification/cohort-2026-10-29-{cohort}.json')
    if old['linksPending']:
        raise ValueError('Previous source cohort is still pending')
    expanded = read_json(ROOT/f'evidence/verification/cohort{cohort}-expanded-source-closure-20261101.json')
    if not expanded['passed'] or expanded['cohort'] != cohort:
        raise ValueError('Previous expanded source closure failed or belongs to another cohort')
    for item in expanded['reports']:
        if sha256(ROOT/item['path']) != item['sha256']:
            raise ValueError('Closed source proof changed: '+item['path'])
    audit_name = select(expanded,cohort)
    oracle = read_json(ROOT/f'evidence/verification/cohort{cohort}-captured-oracle-closure-verification-20261031.json')
    committed = oracle['committedVerification']
    if not committed['passed'] or committed['commit'] != expanded['sourceCommit']:
        raise ValueError('Committed source/oracle closures disagree')
    if oracle['sourceRegistrySha256'] != old['sourceRegistrySha256']:
        raise ValueError('Closed source/oracle registry bindings disagree')
    return dict(plan=old,inputAudit=audit_name,sourceCommit=expanded['sourceCommit'])

def check_data(plan):
    if not plan.get('newInitializedDataBytes'):
        return
    proof = plan['mathematicalDataQualification']
    if not proof['passed'] or proof['newInitializedDataBytes'] != plan['newInitializedDataBytes'] or proof['newInitializedDataObjects'] != plan['newInitializedDataObjects']:
        raise ValueError('Typed data qualification/accounting differs')
    if sha256(ROOT/plan['typedDataQualifier']) != plan['typedDataQualifierSha256']:
        raise ValueError('Typed data qualifier implementation changed')
    for item in proof['proofs']:
        row = item['fresh']
        for field in ('source','object','compiler','linkedElf','linkedDataBinary'):
            if sha256(ROOT/row[field]) != row[field+'Sha256']:
                raise ValueError('Fresh qualified data artifact changed: '+row[field])
        if 'lcf' in row and sha256(ROOT/row['lcf']) != row['lcfSha256']:
            raise ValueError('Declared fresh data linker layout changed')
        if not all(row['realLink'].get(field) for field in ('exactDataBytes','exactDataAddress','objectUnmodified')):
            raise ValueError('Fresh qualified data placement is incomplete')

def publish(cohort):
    binding = closed_binding(cohort-1)
    old = binding['plan']
    plan = read_json(ROOT/f'evidence/verification/cohort-2026-10-29-{cohort}.json')
    spec = read_json(ROOT/plan['specification'])
    if not plan['linksPending'] or not plan['transactionPreparedOnly'] or plan['previousAcceptedCohort'] != cohort-1 or spec['cohort'] != cohort:
        raise ValueError('Matching adjacent prepared source transaction required')
    if sha256(ROOT/plan['specification']) != plan['specificationSha256'] or not spec['migrations']:
        raise ValueError('Reviewed migration specification changed or is empty')
    registry, policy = ROOT/'recovery.json', ROOT/'source-preferences.json'
    prepared = ROOT/f'work/integration/cohort{cohort}-recovery-transaction.json'
    preferences = ROOT/f'work/integration/cohort{cohort}-preference-transaction.json'
    for path,expected in ((registry,old['sourceRegistrySha256']),(policy,old['sourcePreferenceSha256']),
            (prepared,plan['sourceRegistrySha256']),(preferences,plan['sourcePreferenceSha256'])):
        if sha256(path) != expected:
            raise ValueError('Source transaction binding changed: '+str(path))
    check_data(plan)
    with patch.object(recovery_registry,'REGISTRY',prepared):
        recovery_registry.verify_sources()
    previous_registry, previous_policy = registry.read_bytes(), policy.read_bytes()
    try:
        policy.write_bytes(preferences.read_bytes())
        registry.write_bytes(prepared.read_bytes())
        if sha256(registry) != plan['sourceRegistrySha256'] or sha256(policy) != plan['sourcePreferenceSha256']:
            raise ValueError('Published source transaction differs')
    except BaseException:
        registry.write_bytes(previous_registry)
        policy.write_bytes(previous_policy)
        raise
    return dict(cohort=cohort,registryPublished=True,sourceCreditPendingValidation=True,
        previousInputAudit=binding['inputAudit'],previousSourceCommit=binding['sourceCommit'],
        functionsPending=plan['newSourceFunctions'],initializedBytesPending=plan['newSourceBytes'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort',type=int,required=True)
    args = parser.parse_args()
    print(publish(args.cohort))

if __name__ == '__main__':
    main()
