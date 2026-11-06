"""Remove one inactive consumer after an exact, registered packet replacement.

This repairs integration metadata only. It never changes source, reports,
compiler inputs, qualification code, or acceptance credit.
"""
import argparse
import copy
import gzip
import subprocess

from project import ROOT, now, read_json, sha256, write_json
from recovery_registry import batches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    options = parser.parse_args()
    assert options.cohort == 172
    ledger_name = 'provenance/arm9-thumb-reference-only-consumers-20261105.json'
    old_name = 'evidence/matches/cohort172-parallel-wave20261105-q-gp-core-first-0.json'
    new_name = 'evidence/matches/cohort172-parallel-wave20261105-q-gp-core-unsigned-repair-0.json'
    ledger = read_json(ROOT / ledger_name)
    active = {b['report']: b for b in batches()}
    inactive = [c for c in ledger['consumers'] if c['report'] not in active]
    assert len(inactive) == 1 and inactive[0]['report'] == old_name
    old = inactive[0]
    replacements = [c for c in ledger['consumers'] if c['report'] == new_name]
    assert len(replacements) == 1 and new_name in active
    replacement = replacements[0]
    expected = {'0x20aa9b4': 444, '0x20aced4': 44, '0x20acf00': 580}
    for consumer in (old, replacement):
        assert consumer['expectedRanges'] == expected
        assert (consumer.get('program') or '', consumer['processor'], consumer['module'], consumer['mode']) == ('', 'arm9', 'main', 'thumb')
        assert sha256(ROOT / consumer['producer']) == consumer['producerSha256']
        report = read_json(ROOT / consumer['report'])
        assert {r['address']: r['bytes'] for r in report['matches']} == expected
    report = read_json(ROOT / new_name)
    assert report['allPassed']
    selected = active[new_name]
    assert selected['sourceHashes']
    for name, digest in selected['sourceHashes'].items():
        assert sha256(ROOT / name) == digest
    failure = ROOT / 'evidence/verification/cohort172-sealing-resume-v3-20261106.json'
    failed = read_json(failure)
    assert failed['state'] == 'failed' and failed['exitCode'] == 1
    assert sha256(ROOT / failed['log']) == failed['logSha256']
    audit = ROOT / 'logs/integration/cohort172-source-input-audit-20261101.txt'
    assert "assert {p['report'] for p in proofs} == set(consumers)" in audit.read_text(encoding='utf-8')
    folder = ROOT / 'evidence/attempts/cohort172-inactive-reference-consumer-20261106'
    assert not folder.exists()
    folder.mkdir()
    files = []
    for index, source in enumerate((ROOT / ledger_name, failure, ROOT / failed['log'], audit,
                                  ROOT / 'evidence/verification/cohort172-captured-oracle-closure-20261031.json')):
        destination = folder / f'{index}.gz'
        destination.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
        assert gzip.decompress(destination.read_bytes()) == source.read_bytes()
        files.append(dict(path=source.relative_to(ROOT).as_posix(), sha256=sha256(source),
                          archive=destination.relative_to(ROOT).as_posix(), archiveSha256=sha256(destination)))
    before = {name: sha256(ROOT / name) for name in ('recovery.json', 'source-preferences.json', 'ledger/functions.jsonl', old_name, new_name)}
    repaired = copy.deepcopy(ledger)
    repaired['consumers'] = [c for c in ledger['consumers'] if c['report'] != old_name]
    assert len(repaired['consumers']) == len(ledger['consumers']) - 1
    assert all(c == next(x for x in ledger['consumers'] if x['report'] == c['report']) for c in repaired['consumers'])
    assert {c['report'] for c in repaired['consumers']} <= set(active)
    write_json(ROOT / ledger_name, repaired)
    assert before == {name: sha256(ROOT / name) for name in before}
    proof = dict(passed=True, createdUtc=now(), sourceCredit=0, previousFailurePreserved=True,
                 sourceCommitBeforeRepair=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                 removedInactiveConsumer=old, retainedReplacementConsumer=replacement,
                 sourceRegistrySourcesPreferencesIdentityLedgerAndReportsUnchanged=before,
                 originalQualifiersAndBothCommittedAuditsUnmodified=True,
                 newClosureCollectionAndBothCommittedAuditsRequired=True,
                 repairedConsumerLedger=ledger_name, repairedConsumerLedgerSha256=sha256(ROOT / ledger_name), files=files)
    write_json(folder / 'manifest.json', proof)
    subprocess.run(['git', 'add', '--', ledger_name, __file__, folder.relative_to(ROOT).as_posix()], cwd=ROOT, check=True)
    print(dict(passed=True, removedInactiveConsumers=1, retainedConsumers=len(repaired['consumers']), sourceCredit=0))


if __name__ == '__main__':
    main()
