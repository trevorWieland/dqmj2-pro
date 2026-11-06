import argparse
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
from recovery_order import order_batches

REPORT = 'evidence/matches/ov001-20261030-effect-queue01.json'
WRAPPER = 'reproduce_effect_queue_short_paths_v3_20261101.py'
FIELDS = ['source', 'sourceSha256', 'object', 'objectSha256', 'bytes', 'targetSha256']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    options = parser.parse_args()
    transaction = ROOT / f'work/integration/cohort{options.cohort}-recovery-transaction.json'
    registry = read_json(transaction)
    batch = next(row for row in registry['batches'] if row['report'] == REPORT)
    assert batch['reproduce'] == ['match_ov001_effect_queue_20261030.py']
    prior_pins = dict(batch['sourceHashes'])
    for path, digest in prior_pins.items():
        assert sha256(ROOT / path) == digest
    previous = read_json(ROOT / REPORT)
    subprocess.run([sys.executable, str(ROOT / WRAPPER), '--canonical'], cwd=ROOT, check=True)
    current = read_json(ROOT / REPORT)
    assert len(previous['matches']) == len(current['matches']) == 2
    for before, after in zip(previous['matches'], current['matches']):
        assert all(before.get(field) == after.get(field) for field in FIELDS)
        assert before['oracle']['executions'] == after['oracle']['executions']
    for path in code_closure([WRAPPER]):
        digest = sha256(ROOT / path)
        assert path not in prior_pins or prior_pins[path] == digest
        batch['sourceHashes'][path] = digest
    batch['sourceHashes'][WRAPPER] = sha256(ROOT / WRAPPER)
    assert all(batch['sourceHashes'][path] == digest for path, digest in prior_pins.items())
    batch['reproduce'] = [WRAPPER, '--canonical']
    assert order_batches(registry['batches'], details=True)['topologicalOrderVerified']
    write_json(transaction, registry)
    receipt = dict(cohort=options.cohort, generator=__file__.split(chr(92))[-1],
        generatorSha256=sha256(__file__), report=REPORT, reportSha256=sha256(ROOT / REPORT),
        previousPins=prior_pins, supplementalPins={p:h for p,h in batch['sourceHashes'].items() if p not in prior_pins},
        oldPinsPreserved=True, sourceAndObjectIdentitiesPreserved=True,
        actualReturns=sum(row['oracle']['executions'] for row in current['matches']),
        exactBytes=324, sourceCredit=0, acceptedBatchUnchangedExceptReplayTransport=True, passed=True)
    write_json(ROOT / f'evidence/verification/cohort{options.cohort}-effect-queue-replay-transport-20261101.json', receipt)
    print(dict(cohort=options.cohort, oldPinsPreserved=True, exactBytes=324, sourceCredit=0))


if __name__ == '__main__':
    main()
