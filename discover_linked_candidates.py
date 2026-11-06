import argparse
import re
from project import ROOT, configuration, now, read_json, sha256, write_json
from ledger_state import collect_matches


def entries(value):
    if isinstance(value, list):
        for row in value:
            yield from entries(row)
    elif isinstance(value, dict):
        required = {'bytes', 'matchingBytes', 'compiledBytes', 'source', 'sourceSha256', 'object', 'objectSha256', 'address', 'module', 'mode', 'relocations', 'compilerFlags'}
        if required <= value.keys():
            yield value
        else:
            for row in value.values():
                if isinstance(row, (list, dict)):
                    yield from entries(row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', choices=['main', 'ov006'], required=True)
    parser.add_argument('--batch', required=True)
    options = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', options.batch):
        raise ValueError('Invalid evidence batch name')
    known, rejected = collect_matches(configuration()['romSha256'])
    spans = [(address, address + row['size']) for (module, mode, address), row in known.items() if module == options.module]
    found, skipped, scanned = {}, 0, []
    for path in sorted((ROOT / 'evidence/attempts').glob(options.module + '-*.json')):
        if not any(word in path.name for word in ('draft', 'null', 'runtime')):
            continue
        scanned.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha256(path)})
        for entry in entries(read_json(path)):
            if entry['module'] != options.module or entry['compiledBytes'] != entry['bytes'] or entry['matchingBytes'] == entry['bytes'] or not entry['relocations']:
                continue
            start = int(entry['address'], 0)
            if any(start < end and begin < start + entry['bytes'] for begin, end in spans):
                continue
            if entry['bytes'] - entry['matchingBytes'] > max(4, min(16, len(entry['relocations']) * 2)):
                continue
            source = ROOT / entry['source']
            if not source.is_file() or sha256(source) != entry['sourceSha256']:
                skipped += 1
                continue
            key = (entry['mode'], entry['address'], entry['objectSha256'])
            found.setdefault(key, {'input': path.relative_to(ROOT).as_posix(), 'nativeAlias': entry.get('nativeAlias'), 'entry': entry})
    rows = sorted(found.values(), key=lambda row: (row['entry']['address'], -row['entry']['matchingBytes']))
    target = ROOT / f'evidence/attempts/{options.module}-{options.batch}-candidates.json'
    write_json(target, {'createdUtc': now(), 'romSha256': configuration()['romSha256'], 'candidates': rows,
                        'scannedReports': scanned, 'staleSourceAttemptsSkipped': skipped, 'sourceCredit': 0,
                        'selection': 'Same-size compiled C hypotheses with small unresolved differences; acceptance requires fresh genuine linking'})
    print({'module': options.module, 'candidates': len(rows), 'scannedReports': len(scanned), 'staleAttemptsSkipped': skipped})


if __name__ == '__main__':
    main()
