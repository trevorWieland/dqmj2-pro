import argparse
import re
from pathlib import Path
import draft_runtime
import match_runtime as matcher
from project import ROOT, configuration, now, read_json, sha256, write_json


def recover(row, module, batch):
    origin = ROOT / row['draftSource']
    text = origin.read_text()
    source = ROOT / 'work/runtime-recovery/null-drafts' / batch / origin.name
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text('#define NULL ((void *)0)\n' + text)
    attempts = []
    name = row['nativeAlias']
    for optimization, inline, speed in [(2, 'off', False), (2, 'off', True), (3, 'off', False), (3, 'off', True), (2, 'on', False)]:
        try:
            records, found = matcher.compare(source, module, optimization, inline, speed, row['thumb'])
        except ValueError as error:
            attempts.append({'optimization': optimization, 'inline': inline, 'speed': speed, 'failure': str(error)})
            continue
        attempts.extend(records)
        if not found:
            continue
        if len(found) != 1:
            raise ValueError('NULL repair must produce exactly one function')
        function = next(iter(found))
        destination = ROOT / 'src/runtime' / batch / (function + '.c')
        if destination.exists() and destination.read_bytes() != source.read_bytes():
            raise ValueError('Refusing to overwrite changed source')
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            destination.write_bytes(source.read_bytes())
        unused, accepted = matcher.compare(destination, module, optimization, inline, speed, row['thumb'])
        entry, code = accepted[function]
        binary, unused, base = draft_runtime.module_paths(module)
        address = int(entry['address'], 0)
        native = binary.read_bytes()[address - base:address - base + entry['bytes']]
        try:
            if module == 'main':
                entry['oracle'] = matcher.oracle(entry, code, native)
            else:
                from reuse_overlay_c import bounded_oracle
                entry['oracle'] = bounded_oracle(entry, code, native)
        except Exception as error:
            entry['oracle'] = {'supported': False, 'failure': f'{type(error).__name__}: {error}', 'limitation': 'Complete byte and relocation match; behavioral context remains unsupported'}
        entry['draftOrigin'] = {'path': row['draftSource'], 'sha256': sha256(origin), 'transformation': 'Define standard C NULL as a void pointer constant'}
        return {'nativeAlias': name, 'match': entry, 'attempts': attempts}
    return {'nativeAlias': name, 'attempts': attempts}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', required=True, choices=('main', 'ov000', 'ov001', 'ov002', 'ov003', 'ov005', 'ov006', 'ov007'))
    parser.add_argument('--batch', required=True)
    parser.add_argument('--input', action='append', default=[])
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
        raise ValueError('Select a new unpublished batch')
    from ledger_state import collect_matches
    from recovery_ownership import reservation
    known, unused = collect_matches(configuration()['romSha256'])
    candidates = {}
    for relative in args.input:
        for row in read_json(ROOT / relative):
            if 'match' in row or not row.get('draftSource'):
                continue
            failed = [item for item in row.get('attempts', []) if item.get('compileFailed') and "undefined identifier 'NULL'" in item.get('stdout', '')]
            if not failed:
                continue
            text = (ROOT / row['draftSource']).read_text()
            if re.search(r'^\s*#\s*define\s+NULL\b', text, re.M) or len(text.splitlines()) >= 500:
                continue
            match = re.search(r'\bnative_' + args.module + r'_([0-9a-f]{8})\s*\(', text)
            if not match:
                continue
            address = int(match[1], 16)
            thumb = '-thumb' in failed[0]['flags']
            mode = 'thumb' if thumb else 'arm'
            if (args.module, mode, address) in known or args.module == 'main' and reservation(address):
                continue
            candidates[(mode, address)] = {**row, 'thumb': thumb}
    results = []
    for row in candidates.values():
        result = recover(row, args.module, args.batch)
        results.append(result)
        print({'function': row['nativeAlias'], 'matched': 'match' in result}, flush=True)
    matches = [item['match'] for item in results if 'match' in item]
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'], 'module': args.module, 'moduleInputSha256': sha256(draft_runtime.module_paths(args.module)[0]), 'matches': matches, 'nativeSymbols': {rel['symbol']: rel['target'] for item in matches for rel in item['relocations']}, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False, 'limitations': ['Standard NULL supplies a C pointer constant; it supplies no instruction, callee implementation or guessed type beyond the archived draft.', 'Only full native byte and relocation matches receive function credit; native behavior outside supported isolated contexts remains unresolved.']}
    write_json(ROOT / f'evidence/attempts/{args.module}-{args.batch}.json', results)
    write_json(target, report)
    print({'candidates': len(results), 'functions': len(matches), 'bytes': sum(item['bytes'] for item in matches)})


if __name__ == '__main__':
    main()
