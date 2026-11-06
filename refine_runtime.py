import argparse
import concurrent.futures
import json
import re
from pathlib import Path
import draft_runtime
import match_runtime as matcher
from project import ROOT, configuration, read_json, sha256, write_json


def hypotheses(text):
    from call_prototypes import recover_call_prototypes
    from decompiler_shapes import order_register_locals
    from narrow_increments import canonical_byte_increments
    from typed_global_fields import recover_global_records
    from refine_utility import variants
    from data_alignment_hypotheses import variants as alignment_variants
    from switch_default_shapes import variants as switch_variants
    from local_dereference_widths import variants as local_width_variants
    from scalar_array_widths import variants as array_width_variants
    transforms = [
        ('word-void-dereference', lambda value: value.replace('*(void *)', '*(s32 *)')),
        ('explicit-call-arity', lambda value: recover_call_prototypes(value)[0]),
        ('typed-global-records', lambda value: recover_global_records(value)[0]),
        ('direct-byte-increments', lambda value: canonical_byte_increments(value)[0]),
    ]
    name = re.search(r'\b(native_(?:main|ov00[0156])_[0-9a-f]+)\(', text)
    if name:
        transforms.append(('register-declaration-order', lambda value: order_register_locals(value, name[1])))
    seen = {text}
    for label, changed in variants(text):
        if changed not in seen:
            seen.add(changed)
            yield label, changed
    for label, changed in alignment_variants(text):
        if changed not in seen:
            seen.add(changed)
            yield label, changed
    for label, changed in switch_variants(text):
        if changed not in seen:
            seen.add(changed)
            yield label, changed
    for label, changed in local_width_variants(text):
        if changed not in seen:
            seen.add(changed)
            yield label, changed
    for label, changed in array_width_variants(text):
        if changed not in seen:
            seen.add(changed)
            yield label, changed
    accumulated = text
    for label, transform in transforms:
        for value, prefix in ((text, ''), (accumulated, 'combined-')):
            changed = transform(value)
            if changed not in seen:
                seen.add(changed)
                yield prefix + label, changed
        accumulated = transform(accumulated)


def recover(row, module, batch, compiler_override=None, hypothesis_prefix=None, optimization_override=None):
    original = ROOT / row['draftSource']
    text = original.read_text()
    previous = row['bestAttempt']
    if sha256(original) != previous['sourceSha256']:
        raise ValueError('Draft source changed since its measured comparison')
    work = ROOT / 'work/runtime-recovery/refinements' / batch
    work.mkdir(parents=True, exist_ok=True)
    result = {'nativeAlias': row['nativeAlias'], 'inputSource': text, 'inputSourceSha256': sha256(original), 'attempts': []}
    profiles = [(previous['compilerFlags'][0][2:], previous['compilerFlags'][previous['compilerFlags'].index('-inline') + 1], 'speed' in previous['compilerFlags'], previous.get('compilerPath'))]
    profiles.extend((optimization, 'off', speed, None) for optimization, speed in ((2, False), (2, True), (3, False), (3, True)))
    if compiler_override:
        profiles = [(optimization, inline, speed, compiler_override) for optimization, inline, speed, old_compiler in profiles]
    if optimization_override is not None:
        profiles = [(optimization_override, inline, speed, compiler) for optimization, inline, speed, compiler in profiles]
    profiles = list(dict.fromkeys(profiles))
    variants = [('independently-pinned-compiler', text)] if compiler_override else []
    variants.extend(hypotheses(text))
    if hypothesis_prefix:
        variants = [(label, changed) for label, changed in variants if label.startswith(hypothesis_prefix)]
    for hypothesis, changed in variants:
        if len(changed.splitlines()) > 500:
            continue
        source = work / (original.stem + '-' + matcher.sha(changed.encode())[:16] + '.c')
        source.write_text(changed)
        for optimization, inline, speed, compiler in profiles:
            rows, matches = matcher.compare(source, module, optimization, inline, speed, previous['mode'] == 'thumb', ROOT / compiler if compiler else None)
            result['attempts'].append({'hypothesis': hypothesis, 'comparisons': rows})
            if not matches:
                continue
            entry, code = next(iter(matches.values()))
            frozen = ROOT / 'src/runtime' / batch / (entry['name'] + '.c')
            if frozen.exists():
                raise ValueError('Refusing to overwrite frozen C source')
            frozen.parent.mkdir(parents=True, exist_ok=True)
            frozen.write_bytes(source.read_bytes())
            _, found = matcher.compare(frozen, module, optimization, inline, speed, previous['mode'] == 'thumb', ROOT / compiler if compiler else None)
            if entry['name'] not in found:
                raise ValueError('Frozen C did not retain its complete native match')
            accepted, code = found[entry['name']]
            binary_path, _, base = draft_runtime.module_paths(module)
            address = int(accepted['address'], 0)
            native = binary_path.read_bytes()[address - base:address - base + accepted['bytes']]
            try:
                if module == 'main':
                    accepted['oracle'] = matcher.oracle(accepted, code, native)
                else:
                    from reuse_overlay_c import bounded_oracle
                    accepted['oracle'] = bounded_oracle(accepted, code, native)
            except Exception as error:
                accepted['oracle'] = {'supported': False, 'failure': f'{type(error).__name__}: {error}', 'limitation': 'Complete native bytes and relocations match; platform execution remains unsupported'}
            accepted['sourceHypothesis'] = hypothesis
            result['match'] = accepted
            return result
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', choices=('main', 'ov000', 'ov001', 'ov005', 'ov006'), required=True)
    parser.add_argument('--batch', required=True)
    parser.add_argument('--input', action='append', default=[])
    parser.add_argument('--exclude', action='append', default=[])
    parser.add_argument('--compiler')
    parser.add_argument('--hypothesis-prefix')
    parser.add_argument('--optimization', type=int, choices=range(5))
    parser.add_argument('--limit', type=int, default=300)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--minimum-ratio', type=float, default=0.5)
    parser.add_argument('--workers', type=int, choices=(1, 2, 3), default=1)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', args.batch):
        raise ValueError('Invalid refinement batch name')
    path = ROOT / f'evidence/matches/{args.module}-{args.batch}.json'
    if args.verify:
        report = read_json(path)
        if report['module'] != args.module or report['romSha256'] != configuration()['romSha256']:
            raise ValueError('Refinement namespace differs')
        report['matches'] = draft_runtime.verify(report)
        report['nativeSymbols'] = {rel['symbol']: rel['target'] for entry in report['matches'] for rel in entry['relocations']}
        write_json(path, report)
        print({'verified': len(report['matches']), 'bytes': sum(row['bytes'] for row in report['matches'])})
        return
    if path.exists():
        raise ValueError('Choose a new source refinement batch')
    from ledger_state import collect_matches
    from recovery_ownership import reservation
    known, _ = collect_matches(configuration()['romSha256'])
    excluded = {(entry['module'], entry['mode'].lower(), int(entry['address'], 0)) for relative in args.exclude for entry in read_json(ROOT / relative).get('matches', [])}
    candidates = {}
    for relative in args.input:
        for row in read_json(ROOT / relative):
            if 'match' in row or not row.get('draftSource'):
                continue
            attempts = [entry for entry in row.get('attempts', []) if entry.get('bytes') and entry.get('module') == args.module and entry.get('sourceSha256')]
            if not attempts:
                continue
            best = max(attempts, key=lambda entry: entry['matchingBytes'] / max(entry['bytes'], entry['compiledBytes'], 1))
            address = int(best['address'], 0)
            if (args.module, best['mode'], address) in known or (args.module, best['mode'], address) in excluded or args.module == 'main' and reservation(address):
                continue
            ratio = best['matchingBytes'] / max(best['bytes'], best['compiledBytes'], 1)
            if ratio < args.minimum_ratio:
                continue
            candidate = {**row, 'bestAttempt': best, 'ratio': ratio}
            if row['nativeAlias'] not in candidates or ratio > candidates[row['nativeAlias']]['ratio']:
                candidates[row['nativeAlias']] = candidate
    selected = sorted(candidates.values(), key=lambda row: (-row['ratio'], row['nativeAlias']))[args.offset:args.offset + args.limit]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(lambda row: recover(row, args.module, args.batch, args.compiler, args.hypothesis_prefix, args.optimization), selected):
            results.append(result)
            print({'function': result['nativeAlias'], 'matched': 'match' in result, 'hypotheses': len(result['attempts'])}, flush=True)
    matches = [row['match'] for row in results if 'match' in row]
    report = {'schemaVersion': 1, 'romSha256': configuration()['romSha256'], 'module': args.module, 'moduleInputSha256': sha256(draft_runtime.module_paths(args.module)[0]), 'matches': matches,
              'nativeSymbols': {rel['symbol']: rel['target'] for entry in matches for rel in entry['relocations']}, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'limitations': ['C type and expression hypotheses require complete native bytes and genuine ELF relocation agreement', 'Unsupported execution contexts remain explicit; no original source-language or compiler-setting attribution is asserted']}
    write_json(ROOT / f'evidence/attempts/{args.module}-{args.batch}.json', results)
    write_json(path, report)
    print({'functions': len(matches), 'bytes': sum(row['bytes'] for row in matches)})


if __name__ == '__main__':
    main()
