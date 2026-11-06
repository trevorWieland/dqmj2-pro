import ast
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import match_arm7
import utility_code
import utility_runtime
from recovery_registry import entries as registered_entries

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030'
MODULES = {'arm7-wram', 'arm7-main', 'utility-child-arm7-wram', 'utility-child-arm7-main'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(entry):
    return entry.get('program', ''), entry['module'], int(entry['address'], 0) if isinstance(entry['address'], str) else entry['address'], entry.get('mode', 'arm').lower()


def registered():
    ranges, origins = defaultdict(list), []
    for batch in json.loads((ROOT / 'recovery.json').read_text())['batches']:
        report = json.loads((ROOT / batch['report']).read_text())
        for value in registered_entries(report):
            entry = {**{key: report[key] for key in ('program', 'processor', 'mode', 'compilerFlags') if key in report}, **value}
            if entry.get('module') not in MODULES:
                continue
            if entry['module'].startswith('utility-'):
                entry.setdefault('program', utility_runtime.PROGRAM)
            key = identity(entry)
            size = entry.get('bytes', entry.get('size'))
            if type(size) is not int:
                raise ValueError('Registered ARM7 range lacks an explicit extent')
            ranges[key[:2]].append((key[2], key[2] + size))
            path = ROOT / entry.get('source', '')
            if path.is_file() and path.suffix == '.c':
                if digest(path.read_bytes()) != entry['sourceSha256']:
                    raise ValueError('Registered ARM7 C changed: ' + str(path))
                origins.append(entry)
    return ranges, origins


def specs():
    host = [dict(row, processor='arm7', mode='arm', program='', name='native_' + row['module'].replace('-', '_') + '_' + format(row['address'], '08x'))
        for row in match_arm7.candidates(1000000) if row['module'] in MODULES]
    child = [row for row in utility_code.candidates() if row['processor'] == 'arm7' and row['module'] in MODULES]
    return host + child


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    accepted, origins = registered()
    all_specs = specs()
    available = {identity(row): row for row in all_specs if not any(first < row['address'] + row['bytes'] and row['address'] < last
        for first, last in accepted[(row.get('program', ''), row['module'])])}
    attempts, source_rows = {}, defaultdict(dict)
    for prefix in ('arm7', 'utility'):
        for path in (ROOT / 'evidence/attempts').glob(prefix + '-*.json'):
            try:
                rows = json.loads(path.read_text())
            except (ValueError, UnicodeError):
                continue
            if not isinstance(rows, list):
                continue
            for result in rows:
                if not isinstance(result, dict) or result.get('module') not in MODULES:
                    continue
                key = (utility_runtime.PROGRAM if result['module'].startswith('utility-') else '', result['module'], int(result['address'], 0), result.get('mode', 'arm'))
                if key not in available:
                    continue
                for variant in result.get('variants', []):
                    for row in variant.get('attempts', []):
                        if not row.get('source') or not row.get('sourceSha256'):
                            continue
                        source = ROOT / row['source']
                        if not source.is_file() or digest(source.read_bytes()) != row['sourceSha256']:
                            continue
                        text = source.read_text()
                        if len(text.splitlines()) > 500 or any(token in text for token in ('__asm', 'asm(', 'INCBIN')):
                            continue
                        old = source_rows[key].get(row['sourceSha256'])
                        native_size = available[key]['bytes']
                        score = (abs(row.get('compiledBytes', native_size + 10000) - native_size), -row.get('matchingBytes', 0))
                        if old is None or score < tuple(old['score']):
                            source_rows[key][row['sourceSha256']] = {'source': row['source'], 'sourceSha256': row['sourceSha256'],
                                'score': list(score), 'historicalAttemptReport': path.relative_to(ROOT).as_posix(),
                                'historicalCompilerFlags': row.get('compilerFlags'), 'historicalCompiledBytes': row.get('compiledBytes'),
                                'historicalMatchingBytes': row.get('matchingBytes'), 'historicalObject': row.get('object'),
                                'historicalObjectSha256': row.get('objectSha256'), 'unresolvedSymbol': row.get('unresolvedNativeSymbol')}
    inventory = []
    for key, spec in sorted(available.items()):
        row = {name: value for name, value in spec.items() if name not in ('instructions', 'pools')}
        row['name'] = spec.get('name', 'native_' + spec['module'].replace('-', '_') + '_' + format(spec['address'], '08x'))
        row['address'] = hex(spec['address'])
        row['sourceDrafts'] = sorted(source_rows[key].values(), key=lambda item: item['score'])
        row['instructionCount'] = len(spec['instructions'])
        row['literalCount'] = len(spec['pools'])
        row['generatedDraftSourceCredit'] = 0
        inventory.append(row)
    report = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'romSha256': '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',
        'registeredCOriginCount': len(origins), 'heuristicCandidatesBeforeOverlapExclusion': len(all_specs),
        'remainingHeuristicCandidates': inventory, 'currentRegisteredRangesExcluded': True,
        'processorProgramModuleAddressModeIdentityRequired': True, 'heuristicBoundariesAreNotAccepted': True,
        'newSourceCredit': 0, 'compilerProfiles': {'SP1p5': 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'}}
    target = WORK / 'inventory.json'
    target.write_text(json.dumps(report, indent=2) + '\n')
    summary = defaultdict(lambda: {'candidates': 0, 'bytes': 0, 'withDrafts': 0, 'sameSizeDrafts': 0})
    for row in inventory:
        item = summary[row['module']]
        item['candidates'] += 1
        item['bytes'] += row['bytes']
        item['withDrafts'] += bool(row['sourceDrafts'])
        item['sameSizeDrafts'] += any(entry['score'][0] == 0 for entry in row['sourceDrafts'])
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
