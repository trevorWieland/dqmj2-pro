import argparse
import json
import re
from pathlib import Path
import match_lowlevel as matcher
import utility_code
from decompiler_shapes import order_register_locals

ROOT = Path(__file__).resolve().parent
BASE_FLAGS = matcher.FLAGS[:]


def compile_entry(source, compiler, flags):
    key = compiler.relative_to(ROOT).as_posix()
    if matcher.sha(compiler.read_bytes()) != utility_code.compiler_pins().get(key):
        raise ValueError('ITCM C compiler identity changed')
    previous_tool, previous_flags = matcher.COMPILER, matcher.FLAGS
    try:
        matcher.COMPILER, matcher.FLAGS = compiler, flags[:]
        records, matches = matcher.compare(source, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1])
        for entry in records:
            entry['compiler'] = key
        return records, matches
    finally:
        matcher.COMPILER, matcher.FLAGS = previous_tool, previous_flags


def validate(entry):
    source = ROOT / entry['source']
    if matcher.sha(source.read_bytes()) != entry['sourceSha256']:
        raise ValueError('Frozen refined ITCM C changed')
    records, matches = compile_entry(source, ROOT / entry['compiler'], entry['compilerFlags'])
    if entry['name'] not in matches:
        raise ValueError('Refined ITCM C no longer matches its full native span')
    result, code = matches[entry['name']]
    native = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    offset = int(result['address'], 0) - 0x01FF8000
    try:
        result['oracle'] = matcher.oracle(result, code, native[offset:offset + result['bytes']])
    except Exception as error:
        result['oracle'] = {'supported': False, 'failure': f'{type(error).__name__}: {error}', 'limitation': 'Complete native bytes and ELF relocations match; unavailable runtime state remains explicit'}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', required=True)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    report_path = ROOT / f'evidence/matches/itcm-{args.batch}.json'
    if args.verify:
        report = json.loads(report_path.read_text())
        report['matches'] = [validate(entry) for entry in report['matches']]
        report_path.write_text(json.dumps(report, indent=2) + '\n')
        print({'verifiedFunctions': len(report['matches']), 'bytes': sum(entry['bytes'] for entry in report['matches'])})
        return
    if report_path.exists():
        raise ValueError('Choose a new ITCM C refinement batch')
    previous = json.loads((ROOT / 'evidence/attempts/itcm-translated32-drafts.json').read_text())
    accepted = {entry.get('nativeAlias', entry.get('originalSymbol')) for report in (ROOT / 'evidence/matches').glob('*.json') for entry in json.loads(report.read_text()).get('matches', []) if entry.get('module') == 'itcm'}
    work = ROOT / 'work/lowlevel-recovery/itcm-refinements' / args.batch
    work.mkdir(parents=True, exist_ok=True)
    tools = [ROOT / f'tools/mwccarm/mwccarm/{version}/mwccarm.exe' for version in ('2.0/base', '1.2/base', '2.0/sp1p5')]
    configurations = [(level, []) for level in (1, 2, 3, 4)] + [(level, ['-opt', 'speed']) for level in (2, 3, 4)] + [(2, ['-opt', mode]) for mode in ('nocse', 'noprop', 'nolifetimes')]
    matches, attempts = [], []
    for item in previous:
        if item['nativeAlias'] in accepted or 'draftSource' not in item:
            continue
        original = ROOT / item['draftSource']
        text = original.read_text()
        name = 'native_itcm_' + item['nativeAlias'].rsplit('_', 1)[-1]
        variants = list(dict.fromkeys([text, order_register_locals(text, name)]))
        journal = {'nativeAlias': item['nativeAlias'], 'attempts': []}
        found = False
        for text in variants:
            source = work / (name + '-' + matcher.sha(text.encode())[:16] + '.c')
            source.write_text(text)
            for compiler in tools:
                for level, extras in configurations:
                    flags = BASE_FLAGS[:]
                    flags[0] = '-O' + str(level)
                    flags.extend(extras)
                    records, compiled = compile_entry(source, compiler, flags)
                    journal['attempts'].extend(records)
                    if name not in compiled:
                        continue
                    entry, code = compiled[name]
                    frozen = ROOT / f'src/itcm/{args.batch}' / (name + '.c')
                    frozen.parent.mkdir(parents=True, exist_ok=True)
                    if frozen.exists():
                        raise ValueError('Refusing to overwrite accepted ITCM C')
                    frozen.write_bytes(source.read_bytes())
                    entry.update(source=frozen.relative_to(ROOT).as_posix(), sourceSha256=matcher.sha(frozen.read_bytes()))
                    matches.append(validate(entry))
                    found = True
                    break
                if found:
                    break
            if found:
                break
        attempts.append(journal)
        (work / (name + '.json')).write_text(json.dumps(journal, indent=2) + '\n')
        print({'nativeAlias': item['nativeAlias'], 'matched': found, 'attempts': len(journal['attempts'])}, flush=True)
    report = {'schemaVersion': 1, 'romSha256': matcher.sha((ROOT / 'inputs/game.nds').read_bytes()), 'module': 'itcm',
              'moduleInputSha256': matcher.sha((ROOT / 'extract/arm9/itcm.bin').read_bytes()), 'matches': matches,
              'nativeSymbols': {rel['symbol']: rel['target'] for entry in matches for rel in entry['relocations']},
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'limitations': ['Only ordinary C and full-span native ELF relocation agreement are accepted', 'Compiler/optimization variants are explicitly pinned per unit without historical compiler attribution', 'Unavailable native effects remain explicit']}
    (ROOT / f'evidence/attempts/itcm-{args.batch}.json').write_text(json.dumps(attempts, indent=2) + '\n')
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': len(matches), 'bytes': sum(entry['bytes'] for entry in matches)})


if __name__ == '__main__':
    main()
