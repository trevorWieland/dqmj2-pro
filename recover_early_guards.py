import argparse
import json
import re
from pathlib import Path
import draft_arm7
import draft_utility
import early_guards
import match_arm7
import match_lowlevel
import utility_code
import utility_runtime
import wireless_oracle
from match_utility_primitives import native_bindings

ROOT = Path(__file__).resolve().parent


def draft_records(value):
    if isinstance(value, dict):
        if all(key in value for key in ('source', 'name', 'module', 'address', 'bytes')):
            yield {'source': value['source'], 'module': value['module'], 'address': value['address'], 'attempt': value}
        for child in value.values():
            yield from draft_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from draft_records(child)


def validate(entry, target):
    source = ROOT / entry['source']
    if utility_runtime.sha(source.read_bytes()) != entry['sourceSha256']:
        raise ValueError('Frozen early-guard C source changed')
    flags = entry['compilerFlags']
    if target == 'arm7':
        spec = match_arm7.accepted_spec(entry)
        record, code = match_arm7.compare(source, spec, ROOT / entry['compiler'], entry['compilerSha256'],
                                          int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    else:
        spec = utility_code.accepted_spec(entry)
        record, code = utility_code.compile_compare(source, dict(spec, compilerPath=ROOT / entry['compiler']),
                                                    int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if code is None:
        raise ValueError('Frozen early-guard source stopped matching all native bytes and relocations')
    try:
        record['oracle'] = wireless_oracle.verify(code, spec)
    except Exception as error:
        record['oracle'] = {'supported': False, 'failure': f'{type(error).__name__}: {error}',
                            'limitation': 'Complete byte/relocation equality is proven; runtime inputs need a more specific isolated fixture'}
    record['sourceShapeEvidence'] = entry['sourceShapeEvidence']
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', choices=['arm7', 'utility'], required=True)
    parser.add_argument('--batch', required=True)
    parser.add_argument('--limit', type=int, default=600)
    parser.add_argument('--draft-report', type=Path)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    path = ROOT / f'evidence/matches/{args.target}-{args.batch}.json'
    if args.verify:
        report = json.loads(path.read_text())
        report['matches'] = [validate(entry, args.target) for entry in report['matches']]
        if args.target == 'utility':
            report['nativeSymbolBindings'] = native_bindings(report['matches'])
        path.write_text(json.dumps(report, indent=2) + '\n')
        print({'verifiedFunctions': len(report['matches']), 'bytes': sum(entry['bytes'] for entry in report['matches'])})
        return
    if path.exists():
        raise ValueError('Choose a new early-guard research batch')
    specs = match_arm7.candidates(10000) if args.target == 'arm7' else utility_code.candidates()
    specs = {(spec['module'], spec['address']): spec for spec in specs}
    accepted = {(entry['module'], int(entry['address'], 0)) for report in (ROOT / 'evidence/matches').glob(f'{args.target}-*.json')
                for entry in json.loads(report.read_text()).get('matches', [])}
    if args.draft_report:
        snapshots = list(draft_records(json.loads(args.draft_report.read_text())))
        unique = {(item['module'], item['address'], item['source']): item for item in snapshots}
        triage = list(unique.values())
    else:
        triage = json.loads((ROOT / f'work/lowlevel-recovery/{args.target}-near-matches.json').read_text())
    directory = ROOT / f'work/lowlevel-recovery/early-guards/{args.target}-{args.batch}'
    directory.mkdir(parents=True, exist_ok=True)
    compilers = match_arm7.tools()[:2]
    results, attempts = [], []
    for item in triage[:args.limit]:
        key = item['module'], int(item['address'], 0)
        if key in accepted or key not in specs:
            continue
        spec = specs[key]
        original = ROOT / item['source']
        if not original.exists():
            continue
        text = original.read_text()
        name = item['attempt']['name']
        hypothesis = re.sub(r'extern (?:u8|s8|u16|s16) (native_(?:arm7|utility_child_arm7)_data_0380fff4);', r'extern u32 \1;', text)
        changed = early_guards.variant(text, name)
        widened = early_guards.variant(hypothesis, name)
        variants = list(dict.fromkeys(value for value in (changed, widened) if value is not None))
        found = False
        for source_text in variants:
            source = directory / (name + '-' + utility_runtime.sha(source_text.encode())[:16] + '.c')
            source.write_text(source_text)
            for compiler, digest in compilers:
                for level, speed in ((2, False), (2, True), (3, True), (1, False)):
                    try:
                        if args.target == 'arm7':
                            record, code = match_arm7.compare(source, spec, compiler, digest, level, 'off', speed)
                        else:
                            record, code = utility_code.compile_compare(source, dict(spec, compilerPath=compiler), level, 'off', speed)
                    except match_lowlevel.UnresolvedNativeSymbol as error:
                        attempts.append(error.details)
                        continue
                    except utility_code.InterworkingRequiresLink as error:
                        attempts.append({'module': key[0], 'address': hex(key[1]), 'linkerRequired': str(error)})
                        continue
                    attempts.append(record)
                    if code is None:
                        continue
                    frozen = ROOT / f'src/{"arm7" if args.target == "arm7" else "utility"}/{args.batch}/{name}.c'
                    frozen.parent.mkdir(parents=True, exist_ok=True)
                    if frozen.exists():
                        raise ValueError('Refusing to overwrite recovered early-guard C')
                    frozen.write_text(source_text)
                    record.update(source=frozen.relative_to(ROOT).as_posix(), sourceSha256=utility_runtime.sha(frozen.read_bytes()),
                                  sourceShapeEvidence={'kind': 'invert-final-return-guard', 'generator': 'early_guards.py',
                                                       'generatorSha256': utility_runtime.sha((ROOT / 'early_guards.py').read_bytes()),
                                                       'originalDraftSha256': utility_runtime.sha(text.encode()), 'nativeSharedPointerWordRepair': hypothesis != text and source_text == widened,
                                                       'mutableDraftRequiredForReplay': False})
                    entry = validate(record, args.target)
                    results.append(entry)
                    accepted.add(key)
                    print({'module': key[0], 'address': hex(key[1]), 'bytes': entry['bytes'], 'oracle': entry['oracle'].get('vectors')}, flush=True)
                    found = True
                    break
                if found:
                    break
            if found:
                break
    report = {'schemaVersion': 1, 'romSha256': utility_runtime.audit_regions.ROM_HASH, 'runtimeMappingCanonical': True,
              'matches': results, 'nativeSymbols': {rel['symbol']: rel['target'] for entry in results for rel in entry['relocations']},
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'limitations': ['Only new ordinary C source hypotheses are generated; accepted source files remain immutable',
                              'Final guard inversion preserves block scope and one evaluation of the condition; only complete native byte/relocation matches are frozen',
                              'The shared pointer width repair applies only to the measured word pointer at0380FFF4, with full recompilation equality required',
                              'Replay uses frozen source, compiler flags and module hashes, without discovery drafts or old objects']}
    if args.target == 'utility':
        report.update(program=utility_runtime.PROGRAM, nativeSymbolBindings=native_bindings(results))
    else:
        report['processor'] = 'arm7'
    (ROOT / f'evidence/attempts/{args.target}-{args.batch}.json').write_text(json.dumps(attempts, indent=2) + '\n')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': len(results), 'bytes': sum(entry['bytes'] for entry in results), 'attempts': len(attempts)})


if __name__ == '__main__':
    main()
