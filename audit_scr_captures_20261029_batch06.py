import hashlib
import json
import struct
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/script-source/20261029/batch06'
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
import script_assets_20261029 as assets


def digest(data):
    return hashlib.sha256(data).hexdigest()


def references(data, slots):
    result = {slot: [] for slot in slots}
    bits = {struct.unpack('<I', struct.pack('<f', slot))[0]: slot for slot in slots}
    for row in data['instructions']:
        opcode, args = row['opcode'], row['argumentsRaw']
        pairs = []
        if opcode == 1045:
            pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read')]
        elif 1039 <= opcode <= 1044:
            pairs = [(args[1], args[2], 'read'), (args[3], args[4], 'read')]
        elif 1046 <= opcode <= 1053:
            pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read'), (args[5], args[6], 'read')]
        elif opcode == 1035:
            pairs = [(args[1], args[2], 'read')]
        for mode, value, access in pairs:
            if mode == 0 and value in bits:
                result[bits[value]].append({'pc': row['pc'], 'access': access})
    return result


def per_slot_dominance(data, cfg, slot, refs, capture_writes):
    records = {row['pc']: row for row in data['instructions']}
    nodes = {row['pc']: row for row in cfg['nodes']}
    roots = set(cfg['uniqueEntryRoots']) | {edge['targetPc'] for node in cfg['nodes'] for edge in node['successors']
             if edge['kind'] in ('call', 'possible-fork') and edge['targetPc'] is not None}
    writes = {row['pc'] for row in refs if row['access'] == 'write'}
    reads = {row['pc'] for row in refs if row['access'] == 'read'}
    outcomes = defaultdict(list)
    for root in sorted(roots):
        queue, seen = deque([(root, False)]), set()
        read_paths = defaultdict(set)
        while queue:
            pc, initialized = queue.popleft()
            if (pc, initialized) in seen:
                continue
            seen.add((pc, initialized))
            row = records.get(pc)
            if row is None or not row['known'] or pc not in nodes:
                continue
            opcode, args = row['opcode'], row['argumentsRaw']
            if pc in reads:
                read_paths[pc].add(initialized)
            if pc in writes:
                initialized = True
            if opcode == 1033:
                initialized |= slot in capture_writes.get(args[1], set())
                targets = [pc + row['bytes']]
            elif opcode == 1034:
                targets = [pc + row['bytes']]
            elif opcode in (1026, 1027):
                targets = []
            elif opcode == 1036:
                targets = [args[1]]
            elif opcode in (1037, 1038):
                targets = [args[1], pc + row['bytes']]
            elif opcode == 1035:
                targets = [edge['targetPc'] for edge in nodes[pc]['successors'] if edge['targetPc'] is not None]
            else:
                targets = [pc + row['bytes']]
            for target in targets:
                if 0 <= target < len(data['code']):
                    queue.append((target, initialized))
        for pc, states in read_paths.items():
            outcomes[pc].append({'rootPc': root, 'hasPathWithoutKnownInitialization': False in states})
    return {pc: {'knownRootPaths': outcomes.get(pc, []),
                 'allKnownReachingRootsInitializeBeforeRead': bool(outcomes.get(pc)) and
                    not any(row['hasPathWithoutKnownInitialization'] for row in outcomes.get(pc, []))}
            for pc in reads}


def audit():
    candidate_path = ROOT / 'evidence/encounter/scr-v4-candidates-20261029-batch06.json'
    candidates = json.loads(candidate_path.read_text())
    selected = [row for row in candidates if not any(api[0].startswith('set_') for api in row['apis'])]
    assert len(selected) == 117 and sum(row['bytes'] for row in selected) == 7712
    inventory_path = ROOT / 'evidence/encounter/scripts-inventory-20261029.json'
    inventory = json.loads(inventory_path.read_text())
    images = {image['scriptSha256']: image for image in inventory['images']}
    grouped = defaultdict(list)
    for row in selected:
        grouped[row['asset']].append(row)
    output = []
    for asset, rows in sorted(grouped.items()):
        data = assets.load(ROOT / asset)
        descriptor = images[data['scriptSha256']]
        cfg_path = ROOT / descriptor['cfg']['path']
        assert digest(cfg_path.read_bytes()) == descriptor['cfg']['sha256']
        cfg = json.loads(cfg_path.read_text())
        rows = [row for row in rows if not any(node['opcode'] in (1037, 1038)
                for node in data['instructions'] if row['startPc'] <= node['pc'] < row['endExclusivePc'])]
        all_slots = {slot for row in rows for slot in row['namedAllocation'].values()}
        refs = references(data, all_slots)
        capture_writes = {row['startPc']: set(row['namedAllocation'].values()) for row in rows}
        dominance = {slot: per_slot_dominance(data, cfg, slot, refs[slot], capture_writes) for slot in all_slots}
        for row in rows:
            selected_refs, unresolved = {}, []
            for slot in row['namedAllocation'].values():
                values = []
                for ref in refs[slot]:
                    inside = row['startPc'] <= ref['pc'] < row['endExclusivePc']
                    value = dict(ref, inside=inside)
                    if ref['access'] == 'read' and not inside:
                        value['outsideReadQualification'] = dominance[slot][ref['pc']]
                        if not value['outsideReadQualification']['allKnownReachingRootsInitializeBeforeRead']:
                            unresolved.append({'slot': slot, 'pc': ref['pc']})
                    values.append(value)
                inside_refs = [ref for ref in values if ref['inside']]
                assert len(inside_refs) == 1 and inside_refs[0]['access'] == 'write'
                selected_refs[slot] = values
            output.append(dict(row, slotReferences=selected_refs, unresolvedOutsideReads=unresolved,
                               cfgArtifact=descriptor['cfg'], sourceCredit=0))
    assert len(output) == 116 and sum(row['bytes'] for row in output) == 7496
    return {'schemaVersion': 1, 'generator': Path(__file__).relative_to(ROOT).as_posix(),
        'generatorSha256': digest(Path(__file__).read_bytes()), 'candidateIndexSha256': digest(candidate_path.read_bytes()),
        'inventorySha256': digest(inventory_path.read_bytes()), 'instances': output,
        'qualifiedBytesBeforeNativeProof': sum(row['bytes'] for row in output), 'sourceCredit': 0,
        'limits': ['Known decoded entry/direct-call/fork roots only; opaque native or computed slot access remains incomplete',
            'Call summaries credit only the guaranteed writes of complete straight capture functions; other callees are not assumed to initialize',
            'Dominance is syntactic conditional-on-reaching-read evidence; whole caller execution is not established',
            'Named fixed-slot ABI preserves VM storage after the C block returns; source output writes must be proved natively',
            'No inferred reentrancy/concurrency correctness, decision logic or gameplay meaning follows from input capture']}


if __name__ == '__main__':
    result = audit()
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / 'capture-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'instances': len(result['instances']), 'bytes': result['qualifiedBytesBeforeNativeProof'],
        'unresolvedUnits': [row['asset'] + ':' + str(row['startPc']) for row in result['instances'] if row['unresolvedOutsideReads']]}))
