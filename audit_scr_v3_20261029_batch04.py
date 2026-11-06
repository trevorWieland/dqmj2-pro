import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / 'evidence/encounter/scripts-inventory-20261029.json'
OUTPUT = ROOT / 'work/script-source/20261029/batch04/v3-exhaustion-audit.json'
ALLOWED = {1036, 1045, 41, 42, 1038, 1039, 1040, 1026}
EXISTING = {('extract/files/s05e02.e', 57124), ('extract/files/s04e14.e', 118792),
            ('extract/files/s07e04.e', 77700)}
EXISTING_EMPTY = {('extract/files/s07e05.e', 53064), ('extract/files/s07e11.e', 53064)}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def audit():
    inventory = json.loads(INVENTORY.read_text())
    assert len(inventory['images']) == 297
    candidates, empty, roots_examined, images = [], [], 0, []
    for image in inventory['images']:
        path = ROOT / image['cfg']['path']
        assert digest(path.read_bytes()) == image['cfg']['sha256']
        cfg = json.loads(path.read_text())
        nodes = {row['pc']: row for row in cfg['nodes']}
        edges = [(row['pc'], edge['targetPc']) for row in cfg['nodes'] for edge in row['successors']
                 if edge['kind'] in ('call', 'possible-fork', 'jump-or-conditional') and edge['targetPc'] is not None]
        roots = set(cfg['uniqueEntryRoots']) | {edge['targetPc'] for row in cfg['nodes'] for edge in row['successors']
                 if edge['kind'] in ('call', 'possible-fork') and edge['targetPc'] is not None}
        asset = image['members'][0]['archive']
        images.append({'asset': asset, 'scriptSha256': image['scriptSha256'], 'cfg': image['cfg']})
        for root in sorted(roots):
            roots_examined += 1
            first = nodes.get(root)
            if not first or first['opcode'] != 1036 or first['successors'][0]['targetPc'] != root + 12:
                continue
            queue, seen, bad = [root], {}, False
            while queue:
                pc = queue.pop()
                if pc in seen:
                    continue
                row = nodes.get(pc)
                if row is None or row['opcode'] not in ALLOWED:
                    bad = True
                    break
                seen[pc] = row
                if row['opcode'] == 1026:
                    continue
                targets = [row['successors'][0]['targetPc']] if row['opcode'] == 1036 else (
                    [row['successors'][0]['targetPc'], pc + row['recordBytes']] if row['opcode'] == 1038
                    else [pc + row['recordBytes']])
                if any(target is None or target <= pc or target >= image['codeBytes'] for target in targets):
                    bad = True
                    break
                queue.extend(targets)
            if bad:
                continue
            spans = sorted((pc, pc + row['recordBytes']) for pc, row in seen.items())
            end = spans[-1][1]
            if any(left[1] != right[0] for left, right in zip(spans, spans[1:])):
                continue
            if sum(row['opcode'] == 1026 for row in seen.values()) != 1 or nodes[end - 4]['opcode'] != 1026:
                continue
            if any(root < target < end for target in cfg['uniqueEntryRoots']):
                continue
            if any(not root <= source < end and root < target < end for source, target in edges):
                continue
            row = {'asset': asset, 'scriptSha256': image['scriptSha256'], 'startPc': root,
                   'endExclusivePc': end, 'bytes': end - root,
                   'entryAliases': [slot for slot, pc in enumerate(cfg['entrySlots']) if pc == root],
                   'instructionRecords': len(seen), 'cfgArtifact': image['cfg'],
                   'externalInteriorEntries': 0, 'sharedReturnTailDetected': False}
            if end - root == 16 and len(seen) == 2:
                row['alreadyRecovered'] = (asset, root) in EXISTING_EMPTY
                empty.append(row)
            else:
                if not any(node['opcode'] in (41, 42) for node in seen.values()):
                    continue
                row['alreadyRecovered'] = (asset, root) in EXISTING
                candidates.append(row)
    assert len(candidates) == 3 and all(row['alreadyRecovered'] for row in candidates)
    new_empty = [row for row in empty if not row['alreadyRecovered']]
    assert len(new_empty) == 1109
    return {'schemaVersion': 1, 'evidenceClass': 'conservative-frozen-v3-known-root-exhaustion-audit',
            'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
            'inventory': {'path': INVENTORY.relative_to(ROOT).as_posix(), 'sha256': digest(INVENTORY.read_bytes())},
            'imagesAudited': len(images), 'knownRootsExamined': roots_examined, 'images': images,
            'nonemptyPrimitiveCandidates': candidates, 'additionalNonemptyCandidates': 0,
            'newEmptyFunctionInstances': new_empty, 'newEmptyInstanceCount': len(new_empty),
            'newEmptyQualifiedBytes': len(new_empty) * 16, 'previousEmptyInstancesExcluded': 2,
            'sourceOrByteCreditFromAuditAlone': 0,
            'limits': ['Known entry/direct-call/fork roots only; computed or opaque outside entry discovery remains incomplete',
                       'Frozen-v3 generated opcode family is overapproximated with forward complete private-return graphs',
                       'New empty instances still require exact source rebuilds and original/rebuilt native returns',
                       'No nonempty ordinary logic or whole-image completion follows from empty-hook discovery']}


if __name__ == '__main__':
    result = audit()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'images': result['imagesAudited'], 'roots': result['knownRootsExamined'],
                      'additionalNonempty': 0, 'newEmptyInstances': result['newEmptyInstanceCount']}))
