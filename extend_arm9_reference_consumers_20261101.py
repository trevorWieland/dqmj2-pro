import argparse
import copy
import subprocess
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--proposal', required=True)
    options = parser.parse_args()
    prior = options.cohort - 1
    proof_path = f'evidence/verification/cohort{prior}-expanded-source-closure-20261101.json'
    blob = subprocess.run(['git', 'show', 'HEAD:' + proof_path], cwd=ROOT, capture_output=True, check=True).stdout
    assert blob == (ROOT / proof_path).read_bytes() and read_json(ROOT / proof_path)['passed']
    accepted = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{prior}.json')
    assert not accepted['linksPending'] and sha256(ROOT / 'recovery.json') == accepted['sourceRegistrySha256']
    ledger_path = 'provenance/arm9-reference-only-consumers-20261101.json'
    committed = subprocess.run(['git', 'show', 'HEAD:' + ledger_path], cwd=ROOT, capture_output=True, check=True).stdout
    import json
    original = json.loads(committed)
    updated = copy.deepcopy(original)
    proposal = read_json(ROOT / options.proposal)
    assert proposal['cohort'] == options.cohort and proposal['sourceCredit'] == 0
    prepared = read_json(ROOT / f'work/integration/cohort{options.cohort}-recovery-transaction.json')
    reports = {batch['report'] for batch in prepared['batches']}
    added = []
    for consumer in proposal['consumers']:
        assert consumer['processor'] == 'arm9' and consumer['program'] == ''
        assert consumer['module'] == 'main' and consumer['mode'] == 'arm'
        assert consumer['report'] in reports
        assert sha256(ROOT / consumer['producer']) == consumer['producerSha256']
        report = read_json(ROOT / consumer['report'])
        assert report['generatorSha256'] == consumer['producerSha256']
        assert {row['address']: row['bytes'] for row in report['matches']} == consumer['expectedRanges']
        for row in report['matches']:
            assert row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'main' and row['mode'] == 'arm'
            inputs = row['sourceOnlyCompilerInput']
            assert inputs['originalCodeCompilerInput'] is False
            assert inputs['source'] == row['source'] and sha256(ROOT / row['source']) == inputs['sha256'] == row['sourceSha256']
            assert row['exactAfterDeclaredRelocation']
            for header in inputs['includes']:
                assert sha256(ROOT / header['path']) == header['sha256']
        existing = [item for item in updated['consumers'] if item['report'] == consumer['report']]
        if existing:
            assert existing == [consumer]
        else:
            updated['consumers'].append(consumer)
            added.append(consumer['report'])
    current = read_json(ROOT / ledger_path)
    assert current == original or current == updated
    assert updated['consumers'][:len(original['consumers'])] == original['consumers']
    before = sha256(ROOT / ledger_path)
    write_json(ROOT / ledger_path, updated)
    write_json(ROOT / f'evidence/verification/cohort{options.cohort}-arm9-reference-consumer-update-20261101.json',
        dict(proposal=options.proposal, proposalSha256=sha256(ROOT / options.proposal),
            beforeSha256=before, afterSha256=sha256(ROOT / ledger_path), existingEntriesPreserved=True,
            addedReports=added, sourceOnlyCompilerInputRequired=True, originalBlobSourceCredit=0,
            defaultArm7NamespaceRulesChanged=False, sourceCredit=0))
    print(dict(cohort=options.cohort, explicitEvidenceConsumersAdded=len(added), sourceCredit=0))


if __name__ == '__main__':
    main()
