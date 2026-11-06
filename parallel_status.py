import argparse
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
DISPATCH = 'evidence/lanes/parallel-wave20261102/dispatch.json'


def committed(name):
    return subprocess.run(['git', 'show', 'HEAD:' + name], cwd=ROOT,
        check=True, capture_output=True).stdout.decode('utf-8')


def number(value):
    return int(value, 0) if isinstance(value, str) else int(value)


def interval(row, defaults=None):
    defaults = defaults or {}
    module = row.get('module', defaults.get('module'))
    processor = row.get('processor', defaults.get('processor'))
    if processor is None:
        processor = 'arm7' if 'arm7' in module else 'arm9'
    program = row.get('program') or defaults.get('program') or ''
    if module.startswith('utility-child-'):
        program = 'dwc/utility.bin/move/child.srl'
    address = number(row['address'])
    size = row.get('bytes', row.get('size'))
    if size is None:
        size = number(row['end']) - address
    if number(size) <= 0 or row['mode'] not in ('arm', 'thumb'):
        raise ValueError('Invalid claimed function extent or mode')
    alignment = 4 if row['mode'] == 'arm' else 2
    if address % alignment:
        raise ValueError('Claimed function alignment differs')
    return (program, processor, module), address, address + number(size), row['mode']


def collisions(owned, reserved):
    findings = []
    for index, (owner, current) in enumerate(owned):
        for other, candidate in owned[:index] + reserved:
            if current[0] == candidate[0] and current[1] < candidate[2] and candidate[1] < current[2]:
                findings.append(dict(owner=owner, conflictsWith=other, module=current[0][2],
                    start=hex(max(current[1], candidate[1])), endExclusive=hex(min(current[2], candidate[2]))))
    return findings


def finalized(receipt, closure):
    return (receipt.get('linksPending') is False and bool(receipt.get('acceptedBuildCreatedUtc')) and
        receipt.get('sourceMatchedFunctions') == receipt.get('expectedSourceMatchedFunctions') and
        receipt.get('sourceLinkedBytes') == receipt.get('expectedSourceLinkedBytes') and
        receipt.get('moduleComparisonsExact') == 20 and closure.get('passed') is True)


def snapshot():
    board = json.loads((ROOT / DISPATCH).read_text(encoding='utf-8'))
    readme = committed('README.md')
    cohort = int(re.search(r'^Latest accepted source cohort (\d+):', readme, re.M)[1])
    receipt_path = 'evidence/verification/cohort-2026-10-29-' + str(cohort) + '.json'
    receipt = json.loads(committed(receipt_path))
    closure = json.loads(committed('evidence/verification/cohort' + str(cohort) + '-expanded-source-closure-20261101.json'))
    if not finalized(receipt, closure):
        raise ValueError('Committed README points to an unaccepted cohort')
    ledger = [json.loads(line) for line in committed('ledger/functions.jsonl').splitlines() if line]
    accepted = [('accepted-' + str(cohort), interval(row)) for row in ledger if row['states']['functionMatched']]
    reserved = list(accepted)
    pending = []
    for candidate in board['pendingAcceptedCohorts']:
        if candidate <= cohort:
            continue
        specified = board.get('pendingSpecifications', {}).get(str(candidate))
        names = [ROOT / specified] if specified else list(ROOT.glob('cohort' + str(candidate) + '-*-specification.json'))
        if len(names) != 1:
            raise ValueError('Pending cohort specification is missing or ambiguous: ' + str(candidate))
        specification = json.loads(names[0].read_text(encoding='utf-8'))
        additions = specification['expectedAdditions']
        pending.append(dict(cohort=candidate, functions=len(additions), bytes=sum(number(row['bytes']) for row in additions),
            specification=names[0].name))
        for row in additions + specification['migrations']:
            reserved.append(('prepared-' + str(candidate), interval(row)))
    owned, lanes, missing_claims = [], [], []
    for lane in board['active']:
        summary = dict(id=lane['id'], owner=lane['owner'], state=lane['state'])
        if lane.get('claim'):
            path = ROOT / lane['claim']
            if not path.is_file():
                missing_claims.append(lane['claim'])
                summary['state'] = 'claim-unavailable-in-this-checkout'
                lanes.append(summary)
                continue
            claim = json.loads(path.read_text(encoding='utf-8'))
            rows = claim.get('claimedFunctions', claim.get('functions', []))
            values = [interval(row, claim) for row in rows]
            handed_off = set()
            for report in lane.get('handedOffReports', []):
                packet = json.loads((ROOT / report).read_text(encoding='utf-8'))
                handed_off.update(interval(row, packet) for row in packet['matches'])
            owned.extend((lane['id'], value) for value in values if value not in handed_off)
            summary.update(functions=len(values), opportunityBytes=sum(value[2] - value[1] for value in values), claim=lane['claim'])
            summary['handedOffFunctions'] = sum(value in handed_off for value in values)
        lanes.append(summary)
    manifest = json.loads(committed('manifest.json'))
    functions = receipt['sourceMatchedFunctions']
    source_bytes = receipt['sourceLinkedBytes']
    if manifest['functionMatched'] != functions or manifest['sourceLinkedBytes'] != source_bytes:
        raise ValueError('Committed manifest differs from finalized acceptance receipt')
    denominator = board['initializedModuleByteDenominator']
    return dict(acceptedCohort=cohort, acceptedFunctions=functions, acceptedInitializedSourceBytes=source_bytes,
        initializedModuleByteDenominator=denominator, acceptedInitializedPercentage=source_bytes * 100 / denominator,
        acceptedReceipt=receipt_path, pending=pending, lanes=lanes, conflicts=collisions(owned, reserved), missingClaims=missing_claims,
        queuedLanes=[row['id'] for row in board['nextDisjointQueues']],
        sourceOnlyRomProven=False, overallGamePercentage=None, dispatch=DISPATCH)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--check', action='store_true')
    options = parser.parse_args()
    result = snapshot()
    if options.json:
        print(json.dumps(result, indent=2))
    else:
        print('Accepted cohort {acceptedCohort}: {acceptedFunctions:,} functions / {acceptedInitializedSourceBytes:,} bytes ({acceptedInitializedPercentage:.6f}%)'.format(**result))
        print('Prepared: ' + ', '.join(str(row['cohort']) + '=' + str(row['bytes']) + 'B' for row in result['pending']))
        for lane in result['lanes']:
            print(lane['id'] + ': ' + lane['owner'] + ' / ' + lane['state'] +
                (' / ' + str(lane['functions']) + ' functions, ' + str(lane['opportunityBytes']) + 'B opportunity' if 'functions' in lane else ''))
        print('Ownership conflicts: ' + str(len(result['conflicts'])))
        if result['missingClaims']:
            print('Unverified ownership claims: ' + ', '.join(result['missingClaims']))
        print('Queued: ' + ', '.join(result['queuedLanes']))
    if options.check and (result['conflicts'] or result['missingClaims']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
