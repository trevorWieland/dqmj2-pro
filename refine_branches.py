import argparse
import re
import draft_runtime
import match_runtime as matcher
from conditional_shapes import variants
from project import ROOT, configuration, now, read_json, sha256, write_json


def recover(row, module, batch):
    origin = ROOT / row['source']
    text = origin.read_text()
    if sha256(origin) != row['sourceSha256']:
        raise ValueError('Measured draft changed')
    settings = row['compilerFlags']
    profiles = [(settings[0][2:], settings[settings.index('-inline') + 1], 'speed' in settings)]
    profiles.extend((str(level), 'off', speed) for level, speed in [(2, False), (2, True), (3, False), (3, True)])
    profiles = list(dict.fromkeys(profiles))
    compiler = ROOT / row['compilerPath'] if row.get('compilerPath') else None
    results = []
    for label, changed in variants(text):
        if len(changed.splitlines()) > 500:
            continue
        source = ROOT / 'work/runtime-recovery/branch-shapes' / batch / (row['name'] + '-' + matcher.sha(changed.encode())[:12] + '.c')
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(changed)
        for optimization, inline, speed in profiles:
            try:
                records, found = matcher.compare(source, module, optimization, inline, speed, row['mode'] == 'thumb', compiler)
            except ValueError as error:
                results.append({'shape': label, 'failure': str(error)})
                continue
            results.append({'shape': label, 'comparisons': records})
            if row['name'] not in found:
                continue
            destination = ROOT / 'src/runtime' / batch / (row['name'] + '.c')
            if destination.exists() and destination.read_bytes() != source.read_bytes():
                raise ValueError('Refusing to overwrite source')
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                destination.write_bytes(source.read_bytes())
            unused, accepted = matcher.compare(destination, module, optimization, inline, speed, row['mode'] == 'thumb', compiler)
            entry, code = accepted[row['name']]
            binary, unused, base = draft_runtime.module_paths(module)
            offset = int(entry['address'], 0) - base
            native = binary.read_bytes()[offset:offset + entry['bytes']]
            try:
                if module == 'main':
                    entry['oracle'] = matcher.oracle(entry, code, native)
                else:
                    from reuse_overlay_c import bounded_oracle
                    entry['oracle'] = bounded_oracle(entry, code, native)
            except Exception as error:
                entry['oracle'] = {'supported': False, 'failure': f'{type(error).__name__}: {error}', 'limitation': 'Full native bytes and relocations match; broader caller context is unsupported'}
            entry['sourceHypothesis'] = label
            return {'nativeAlias': row['nativeAlias'], 'match': entry, 'attempts': results}
    return {'nativeAlias': row['nativeAlias'], 'attempts': results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', required=True, choices=('main', 'ov000', 'ov001', 'ov002', 'ov003', 'ov005', 'ov006', 'ov007'))
    parser.add_argument('--batch', required=True)
    parser.add_argument('--input', action='append', default=[])
    parser.add_argument('--minimum-ratio', type=float, default=0.85)
    parser.add_argument('--limit', type=int, default=100)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    target = ROOT / f'evidence/matches/{args.module}-{args.batch}.json'
    if args.verify:
        report = read_json(target)
        report['matches'] = draft_runtime.verify(report)
        write_json(target, report)
        print({'verifiedFunctions': len(report['matches']), 'bytes': sum(item['bytes'] for item in report['matches'])})
        return
    if target.exists():
        raise ValueError('Choose a new unpublished batch')
    from ledger_state import collect_matches
    from recovery_ownership import reservation
    known, unused = collect_matches(configuration()['romSha256'])
    selected = {}
    for relative in args.input:
        for row in read_json(ROOT / relative):
            if 'match' in row:
                continue
            for attempt in row.get('attempts', []):
                if not attempt.get('bytes') or not attempt.get('sourceSha256') or attempt.get('module') != args.module:
                    continue
                address = int(attempt['address'], 0)
                key = (args.module, attempt['mode'], address)
                ratio = attempt['matchingBytes'] / max(attempt['bytes'], attempt['compiledBytes'], 1)
                if key in known or ratio < args.minimum_ratio or args.module == 'main' and reservation(address, attempt['bytes']):
                    continue
                if key not in selected or selected[key]['ratio'] < ratio:
                    selected[key] = {**attempt, 'nativeAlias': row['nativeAlias'], 'ratio': ratio}
    ordered = sorted(selected.values(), key=lambda item: (-item['ratio'], int(item['address'], 0)))[:args.limit]
    results = []
    for row in ordered:
        result = recover(row, args.module, args.batch)
        results.append(result)
        print({'function': row['nativeAlias'], 'matched': 'match' in result, 'variants': len(result['attempts'])}, flush=True)
        write_json(ROOT / f'evidence/attempts/{args.module}-{args.batch}.json', results)
    matches = [item['match'] for item in results if 'match' in item]
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'], 'module': args.module, 'moduleInputSha256': sha256(draft_runtime.module_paths(args.module)[0]), 'matches': matches, 'nativeSymbols': {rel['symbol']: rel['target'] for item in matches for rel in item['relocations']}, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False, 'limitations': ['Equivalent if/else arm ordering changes compiler control layout without adding instructions or callee implementations.', 'Only full native byte and relocation agreement is accepted; original source spelling and compiler history remain unknown.']}
    write_json(target, report)
    print({'candidates': len(ordered), 'functions': len(matches), 'bytes': sum(item['bytes'] for item in matches)})


if __name__ == '__main__':
    main()
