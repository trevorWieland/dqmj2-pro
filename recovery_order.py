import argparse
import ast
import hashlib
import heapq
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MATCHES = 'evidence/matches/'
COMPOSED = ('record-update', 'features', 'feature-bonus', 'skill-observe')
COMPOSED_CONSUMERS = ('action-banks', 'projection', 'skill-prepare', 'derived-refresh', 'roster-mutation')
SUPPORT = {
    'features': ('library',),
    'feature-bonus': ('inventory', 'features'),
    'skill-observe': ('library',),
    'native-name': ('features',),
    'runtime-view': ('roster', 'features', 'action-banks', 'projection'),
    'runtime-refresh': ('roster', 'features', 'action-banks', 'projection', 'runtime-view', 'native-name'),
    'reserve-refresh': ('runtime-refresh',),
    'enemy-initialize': ('runtime-view', 'runtime-refresh', 'native-name', 'runtime-rng', 'battle-skill-pointer', 'feature-bonus'),
}
for consumer in COMPOSED_CONSUMERS:
    SUPPORT[consumer] = COMPOSED

class RecoveryOrderError(ValueError):
    pass

def normalized(value):
    return str(value).replace('\\', '/').casefold()

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def match_entries(document):
    result = []
    for key in ('matches', 'functionMatches', 'functions', 'dataMatches', 'containerMatches', 'linkageMatches'):
        for row in document.get(key, []):
            if isinstance(row, dict):
                result.append({**document, **row})
    return result

def references(value):
    if isinstance(value, dict):
        if isinstance(value.get('source'), str) and isinstance(value.get('object'), str) and value.get('objectSha256'):
            yield value
        for child in value.values():
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)

def local_oracle_sources(root, starting):
    pending = [root / starting] if starting else []
    visited = set()
    while pending:
        path = pending.pop()
        if path in visited or not path.is_file():
            continue
        visited.add(path)
        tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        yield path, tree
        for node in ast.walk(tree):
            names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.module else []
            for name in names:
                if name.startswith('mechanics_save_') and name.endswith('_oracle') or name == 'verify_record_features' or name.startswith('save_') and name.endswith('_oracle'):
                    pending.append(root / (name + '.py'))

def literal_wanted_addresses(tree):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not any(isinstance(target, ast.Name) and target.id in ('wanted', 'addresses') for target in node.targets):
            continue
        if not isinstance(node.value, (ast.Set, ast.List, ast.Tuple)):
            continue
        for child in node.value.elts:
            if isinstance(child, ast.Constant) and isinstance(child.value, int) and 0x02000000 <= child.value < 0x02100000:
                yield child.value

def priority(report):
    name = Path(report).name
    return 2 if name.startswith('mechanics-save-') else 1 if name.startswith('save-') or name == 'save-write.json' else 0

def dependency_graph(items, root=ROOT):
    root = Path(root)
    batches = {normalized(batch['report']): batch for batch in items}
    if len(batches) != len(items):
        raise RecoveryOrderError('Duplicate registered report paths')
    documents = {key: read_json(root / batch['report']) for key, batch in batches.items()}
    edges = {key: set() for key in batches}
    reasons = {}
    object_producers = {}
    identity_producers = {}
    address_producers = {}
    for key, document in documents.items():
        for row in match_entries(document):
            if isinstance(row.get('object'), str) and row.get('objectSha256'):
                artifact = normalized(row['object']), row['objectSha256']
                object_producers.setdefault(artifact, set()).add(key)
            if row.get('source') and row.get('name') and row.get('address'):
                identity = normalized(row['source']), row['name'], str(row['address']).lower()
                identity_producers.setdefault(identity, set()).add(key)
            if row.get('address') and row.get('module') in ('main', 'arm9') and row.get('name'):
                address_producers.setdefault(int(row['address'], 16), set()).add(key)

    def add(consumer, producer, reason):
        if producer == consumer:
            return
        edges[consumer].add(producer)
        reasons.setdefault((consumer, producer), set()).add(reason)

    for key, document in documents.items():
        for declared in (batches[key].get('replayRequires', []), document.get('replayRequires', [])):
            if not isinstance(declared, list) or not all(isinstance(value, str) for value in declared):
                raise RecoveryOrderError('Replay prerequisites must be a list of registered report paths')
            for required in declared:
                producer = normalized(required)
                if producer not in batches:
                    raise RecoveryOrderError('Missing registered replay prerequisite for ' + batches[key]['report'] + ': ' + required)
                if producer == key:
                    raise RecoveryOrderError('Self replay prerequisite: ' + required)
                if not document.get('romSha256') or documents[producer].get('romSha256') != document['romSha256']:
                    raise RecoveryOrderError('Replay prerequisite build namespace differs: ' + required)
                add(key, producer, 'declared generated-evidence prerequisite: ' + required)
        for reference in references(document.get('oracle', {})):
            artifact = normalized(reference['object']), reference['objectSha256']
            providers = object_producers.get(artifact, set())
            if reference.get('name') and reference.get('address'):
                identity = normalized(reference['source']), reference['name'], str(reference['address']).lower()
                qualified = identity_producers.get(identity, set())
                if qualified:
                    providers = qualified
            if not providers:
                raise RecoveryOrderError('No registered producer for ' + batches[key]['report'] + ': ' + reference['source'] + ' / ' + reference['object'])
            if key in providers:
                continue
            if len(providers) != 1:
                if artifact not in object_producers or object_producers[artifact] != providers:
                    raise RecoveryOrderError('Ambiguous source identity for ' + batches[key]['report'] + ': ' + reference['source'])
            producer = sorted(providers)[0]
            add(key, producer, 'oracle object identity: ' + reference['source'] + ' / ' + reference.get('name', reference['object']))
        oracle = document.get('oracleSource')
        for source, tree in local_oracle_sources(root, oracle):
            for address in literal_wanted_addresses(tree):
                for producer in address_producers.get(address, ()):
                    add(key, producer, 'oracle wanted-address loader: ' + source.relative_to(root).as_posix() + ':' + hex(address))
        filename = Path(batches[key]['report']).name
        if filename.startswith('mechanics-save-'):
            suffix = filename[len('mechanics-save-'):-len('.json')]
            for support in SUPPORT.get(suffix, ()):
                producer = normalized(MATCHES + 'mechanics-save-' + support + '.json')
                if producer not in batches:
                    raise RecoveryOrderError('Missing registered support report for ' + batches[key]['report'] + ': ' + producer)
                add(key, producer, 'explicit connected-loader report: ' + support)
    return batches, documents, edges, reasons

def order_batches(items=None, root=ROOT, details=False):
    root = Path(root)
    if items is None:
        items = read_json(root / 'recovery.json')['batches']
    batches, documents, edges, reasons = dependency_graph(items, root)
    counts = {key: len(values) for key, values in edges.items()}
    followers = {key: set() for key in batches}
    for consumer, producers in edges.items():
        for producer in producers:
            followers[producer].add(consumer)
    ready = [(priority(key), key) for key, count in counts.items() if count == 0]
    heapq.heapify(ready)
    ordered = []
    while ready:
        unused, key = heapq.heappop(ready)
        ordered.append(key)
        for consumer in sorted(followers[key]):
            counts[consumer] -= 1
            if counts[consumer] == 0:
                heapq.heappush(ready, (priority(consumer), consumer))
    if len(ordered) != len(batches):
        remaining = {batches[key]['report']: [batches[dependency]['report'] for dependency in sorted(edges[key]) if counts[dependency]] for key, count in counts.items() if count}
        raise RecoveryOrderError('Recovery dependency cycle: ' + json.dumps(remaining, sort_keys=True))
    positions = {key: index for index, key in enumerate(ordered)}
    if any(positions[producer] >= positions[consumer] for consumer, producers in edges.items() for producer in producers):
        raise RecoveryOrderError('Recovery topological verification failed')
    result = [batches[key] for key in ordered]
    if not details:
        return result
    return {'schemaVersion': 1, 'registrySha256': hashlib.sha256((root / 'recovery.json').read_bytes()).hexdigest(), 'batches': result, 'edges': [{'consumer': batches[consumer]['report'], 'producer': batches[producer]['report'], 'reasons': sorted(reasons[consumer, producer])} for consumer in sorted(edges) for producer in sorted(edges[consumer])], 'topologicalOrderVerified': True, 'objectsReadOrCopied': False, 'compilerAndOracleChecksSkipped': False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = order_batches(root=args.root, details=True)
    text = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    else:
        print(text)

if __name__ == '__main__':
    main()
