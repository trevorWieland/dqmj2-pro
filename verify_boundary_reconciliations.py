import argparse
import copy
from project import ROOT, read_json, write_json
from boundary_reconciliations import reconcile


def main(policy_path):
    policy = read_json(ROOT / policy_path)
    modules = [dict(row, processor='arm9') for row in read_json(ROOT / 'provenance/seed-manifest.json')['modules']]
    rows = [dict(row, processor='arm9') for row in read_json(ROOT / 'provenance/seed-source-map.json')['functions']]
    original = copy.deepcopy(rows)
    merged = reconcile(rows, modules, [(policy_path, policy)])
    assert rows == original and len(merged) == len(rows) - 1
    target = [row for row in merged if row['module'] == 'main' and int(row['address'], 0) == 0x0201D470]
    assert len(target) == 1 and target[0]['size'] == 356
    assert not any(row['module'] == 'main' and int(row['address'], 0) == 0x0201D5CC for row in merged)
    assert sum(row.get('size') or 0 for row in merged) == sum(row.get('size') or 0 for row in rows)
    cases = []

    def rejected(label, candidate, current_rows=rows):
        try:
            reconcile(current_rows, modules, [(policy_path, candidate)])
        except ValueError:
            cases.append(label)
        else:
            raise AssertionError(label)

    changed = copy.deepcopy(policy)
    changed['romSha256'] = '0' * 64
    rejected('wrong-rom-namespace', changed)
    changed = copy.deepcopy(policy)
    changed['inputModuleSha256'] = '0' * 64
    rejected('wrong-module-hash', changed)
    changed = copy.deepcopy(policy)
    changed['inputBytesSha256'] = '0' * 64
    rejected('wrong-combined-native-bytes', changed)
    changed = copy.deepcopy(policy)
    changed['historicalReview']['sha256'] = '0' * 64
    rejected('changed-historical-review', changed)
    changed = copy.deepcopy(policy)
    changed['priorEntries'][1]['address'] = hex(0x0201D5D0)
    rejected('gap-in-prior-input-extents', changed)
    changed = copy.deepcopy(policy)
    changed['bytes'] += 4
    rejected('invented-additional-input-bytes', changed)
    missing = [row for row in rows if not (row['module'] == 'main' and int(row['address'], 0) == 0x0201D5CC)]
    rejected('missing-prior-fragment', policy, missing)
    overlap = rows + [dict(target[0], address=hex(0x0201D5C8), size=4)]
    rejected('unlisted-overlapping-candidate', policy, overlap)
    write_json(ROOT / 'evidence/verification/boundary-reconciliations-controls-20261030.json',
               {'policy': policy_path, 'validMergePassed': True, 'inputRowsUnchanged': rows == original,
                'retainedInputByteSum': True, 'removedIndependentFragmentCandidates': 1,
                'negativeControls': cases, 'sourceCredit': 0})
    print({'validMergePassed': True, 'negativeControls': len(cases), 'sourceCredit': 0})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--policy', default='evidence/regions/boundary-reconciliations/main-0201d470-20261030.json')
    main(parser.parse_args().policy)
