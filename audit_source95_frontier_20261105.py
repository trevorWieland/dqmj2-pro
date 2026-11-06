import argparse
import hashlib
import json
import subprocess
from collections import Counter
from project import ROOT, read_json, write_json, sha256


def identity(row):
    return row.get('program') or '', row['processor'], row.get('module', row.get('name'))


def number(value):
    return int(value, 0) if isinstance(value, str) else int(value)


def mark(modules, row, flag, rejected):
    key = identity(row)
    module = modules.get(key)
    size = row.get('bytes') or 0
    if module is None or size <= 0:
        rejected.append(dict(identity=list(key), address=row.get('address'), bytes=size))
        return
    offset = number(row['address']) - module['base']
    if not 0 <= offset < offset + size <= module['bytes']:
        rejected.append(dict(identity=list(key), address=row['address'], bytes=size))
        return
    data = module['mask']
    for index in range(offset, offset + size):
        data[index] |= flag


def runs(module, predicate):
    result, start = [], None
    for index, value in enumerate(module['mask']):
        selected = predicate(value)
        if selected and start is None:
            start = index
        if not selected and start is not None:
            result.append((start, index))
            start = None
    if start is not None:
        result.append((start, module['bytes']))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision', required=True)
    parser.add_argument('--atlas', default='work/parallel-wave20261102/atlas/atlas.json')
    parser.add_argument('--output', required=True)
    options = parser.parse_args()
    revision = subprocess.check_output(['git', 'rev-parse', options.revision], cwd=ROOT, text=True).strip()
    atlas = read_json(ROOT / options.atlas)
    assert atlas['sourceCommit'] == revision
    plan_name = f'evidence/verification/cohort-2026-10-29-{atlas["acceptedCohort"]}.json'
    closure_name = f'evidence/verification/cohort{atlas["acceptedCohort"]}-expanded-source-closure-20261101.json'
    def committed(name):
        return subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
    assert json.loads(committed(closure_name))['passed']
    plan = json.loads(committed(plan_name))
    ledger_bytes = committed('ledger/functions.jsonl')
    ledger = [json.loads(line) for line in ledger_bytes.decode('utf-8').splitlines()]
    board_name = 'evidence/lanes/parallel-wave20261102/dispatch.json'
    backlog_name = 'evidence/lanes/parallel-wave20261102/native-backlog/partition.json'
    boundary_name = 'evidence/lanes/parallel-wave20261102/native-backlog/boundary-work.json'
    pins = {name: sha256(ROOT / name) for name in [options.atlas, board_name, backlog_name, boundary_name]}
    modules = {}
    for row in atlas['modules']:
        module = dict(row, mask=bytearray(row['bytes']))
        key = identity(row)
        assert key not in modules
        modules[key] = module
        for offset, size, category in row['regions']:
            flag = 1 if category in [1, 2, 3, 4] else 2 if category == 5 else 0
            if flag:
                module['mask'][offset:offset + size] = bytes([flag]) * size
    accepted = sum(sum(bool(v & 1) for v in m['mask']) for m in modules.values())
    denominator = sum(m['bytes'] for m in modules.values())
    assert accepted == plan['sourceLinkedBytes'] == atlas['metrics']['acceptedBytes']
    assert denominator == atlas['metrics']['bytes'] == 2512636
    rejected, unknown, boundary_confidence = [], [], Counter()
    for row in ledger:
        if (row.get('bytes') or 0) > 0:
            mark(modules, row, 4, rejected)
            if not row['states']['functionMatched']:
                boundary_confidence[row['boundaryConfidence']] += 1
        else:
            unknown.append(dict(identity=list(identity(row)), address=row['address'], mode=row['mode']))
    for chunk in read_json(ROOT / backlog_name)['chunks']:
        for row in chunk['functionIdentities']:
            mark(modules, row, 8, rejected)
    ambiguous_fragments = []
    for group in read_json(ROOT / boundary_name)['groups']:
        for entry in group['entries']:
            for fragment in entry['ghidraBodyRanges']:
                owners = fragment['physicalOwningModules']
                if len(owners) != 1:
                    ambiguous_fragments.append(dict(entry=entry['id'], fragment=fragment))
                    continue
                row = dict(group, module=owners[0], address=fragment['start'], bytes=fragment['bytes'])
                mark(modules, row, 32, rejected)
    unparsed_claims = []
    for lane in read_json(ROOT / board_name)['active']:
        name = lane.get('claim')
        if not name:
            continue
        pins[name] = sha256(ROOT / name)
        claim = read_json(ROOT / name)
        rows = claim.get('claimedFunctions', claim.get('functions'))
        if not isinstance(rows, list) or not all(isinstance(r, dict) and 'address' in r for r in rows):
            unparsed_claims.append(name)
            continue
        for row in rows:
            mark(modules, row, 16, rejected)
    summaries, holes, investigations = [], [], []
    for key, module in modules.items():
        values = module['mask']
        remaining = [v for v in values if not v & 3]
        row = dict(program=key[0], processor=key[1], module=key[2], bytes=module['bytes'],
            acceptedBytes=sum(bool(v & 1) for v in values), regeneratedLinkageBytes=sum(bool(v & 2) for v in values),
            unresolvedBytes=len(remaining), positiveFunctionExtentBytes=sum(bool(v & 4) for v in remaining),
            existingBacklogBytes=sum(bool(v & 8) for v in remaining),
            parsedReservationBytes=sum(bool(v & 16) for v in remaining),
            outsideBacklogAndParsedReservations=sum(not v & 24 for v in remaining),
            withoutPositiveFunctionExtent=sum(not v & 4 for v in remaining),
            ghidraBodyBytesOutsidePositiveExtent=sum(not v & 4 and bool(v & 32) for v in remaining),
            withoutExtentOrGhidraBody=sum(not v & 36 for v in remaining))
        assert row['acceptedBytes'] + row['regeneratedLinkageBytes'] + row['unresolvedBytes'] == row['bytes']
        summaries.append(row)
        for start, end in runs(module, lambda v: not v & 7):
            holes.append(dict(program=key[0], processor=key[1], module=key[2],
                address=hex(module['base'] + start), endExclusive=hex(module['base'] + end), bytes=end - start))
        for start, end in runs(module, lambda v: not v & 23):
            for offset in range(start, end, 16384):
                finish = min(end, offset + 16384)
                if finish - offset < 256:
                    continue
                investigations.append(dict(program=key[0], processor=key[1], module=key[2],
                    address=hex(module['base'] + offset), endExclusive=hex(module['base'] + finish),
                    bytes=finish - offset, sourceCredit=0, ownershipGranted=False,
                    knownGhidraBodyBytes=sum(bool(v & 32) for v in values[offset:finish]),
                    status='read-only-boundary-or-initialized-data-investigation-proposal'))
    assert pins == {name: sha256(ROOT / name) for name in pins}
    totals = {key: sum(row[key] for row in summaries) for key in summaries[0] if key.endswith('Bytes') or key in ['outsideBacklogAndParsedReservations', 'withoutPositiveFunctionExtent', 'ghidraBodyBytesOutsidePositiveExtent', 'withoutExtentOrGhidraBody']}
    write_json(ROOT / options.output, dict(passed=True, sourceCredit=0, productionInputsChanged=False,
        sourceRevision=revision, acceptedCohort=atlas['acceptedCohort'], sourceBytes=accepted,
        initializedDenominator=denominator, source95TargetBytes=(denominator * 95 + 99) // 100,
        additionalValidatedBytesRequired=(denominator * 95 + 99) // 100 - accepted,
        minimumRecoveryOutsideCurrentPositiveExtents=max(0, (denominator * 95 + 99) // 100 - accepted - totals['positiveFunctionExtentBytes']),
        committedLedgerSha256=hashlib.sha256(ledger_bytes).hexdigest(), inputPins=pins,
        totals=totals, modules=sorted(summaries, key=lambda r: -r['unresolvedBytes']),
        unresolvedPositiveBoundaryConfidence=dict(boundary_confidence), entriesWithoutPositiveExtent=len(unknown),
        largestRegionsWithoutPositiveExtent=sorted(holes, key=lambda r: -r['bytes'])[:60],
        investigationProposals=sorted(investigations, key=lambda r: (-r['bytes'], -r['knownGhidraBodyBytes'])),
        unparsedClaimSchemas=unparsed_claims, excludedOrOutOfModuleRows=rejected, ambiguousGhidraFragments=ambiguous_fragments,
        limitations=['Positive function extents retain their existing boundary confidence; none are promoted to accepted code.',
            'Regions without a positive extent may be executable code, initialized data, pools or padding; classification requires original evidence.',
            'Ghidra body fragments retain unknown fragment mode/literal suffix/complete extent and grant no ownership or source credit.',
            'Unparsed historical claim schemas remain reserved and cannot be treated as unowned.',
            'Investigation proposals exclude parsed function reservations only; original data/literal/storage protections must be audited before any source ownership is granted.',
            'Backlog and reservation columns overlap and must not be added as disjoint source coverage.',
            'This read-only inventory creates no claims and proves neither source-only ROM nor native Windows execution.']))
    print(dict(passed=True, sourceBytes=accepted, additionalBytesRequired=(denominator * 95 + 99) // 100 - accepted,
        totals=totals, unparsedClaimSchemas=len(unparsed_claims), excludedRows=len(rejected)))


if __name__ == '__main__':
    main()
