import argparse
import json
import os
import re
import subprocess
from collections import defaultdict
from pathlib import Path
import draft_utility
import match_lowlevel
import reuse_utility_c as reuse
import utility_bridges
import utility_code
import utility_runtime
from elftools.elf.elffile import ELFFile
from match_utility_primitives import native_bindings

ROOT = Path(__file__).resolve().parent
MASKS = {1: 0xff000000, 2: 0, 10: 0xe800f800, 15: 0xfe000000, 28: 0xff000000, 29: 0xff000000}


def sources(processor):
    accepted = json.loads((ROOT / 'recovery.json').read_text())['batches']
    result, identities = [], set()
    for batch in accepted:
        for entry in json.loads((ROOT / batch['report']).read_text()).get('matches', []):
            path = ROOT / entry.get('source', '')
            if path.suffix != '.c' or not entry.get('sourceSha256') or not entry.get('name'):
                continue
            if not 16 <= entry.get('bytes', entry.get('size', 0)) <= 600 or entry.get('module') not in ('main', 'itcm', 'arm7-main', 'arm7-wram'):
                continue
            payload = path.read_bytes()
            if utility_runtime.sha(payload) != entry['sourceSha256']:
                raise ValueError('Published origin C source changed')
            text = payload.decode()
            if '#include' in text or re.search(r'\b(?:asm|__asm|INCBIN)\b', text):
                continue
            names = {}
            def token(match):
                name = match[0]
                if name not in names:
                    names[name] = 'relocated_' + str(len(names))
                return names[name]
            normalized = re.sub(r'\b[A-Za-z_][A-Za-z_0-9]*_[0-9a-f]{8}\b', token, text)
            identity = utility_runtime.sha(re.sub(r'\s+', ' ', normalized).encode())
            if identity in identities:
                continue
            identities.add(identity)
            result.append(entry)
    return sorted(result, key=lambda item: (item.get('processor', 'arm9') != processor, len(item.get('relocations', [])), item.get('bytes', item.get('size', 0)), item['source']))


def compile_origin(origin, compiler, flags, directory):
    source = ROOT / origin['source']
    key = utility_runtime.sha((origin['sourceSha256'] + json.dumps(flags) + str(compiler)).encode())[:20]
    output = directory / (key + '.o')
    command = [str(compiler), *flags, '-c', str(source), '-o', str(output)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30,
                            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:
        return {'source': origin['source'], 'command': command, 'compileFailed': True, 'stdout': result.stdout, 'stderr': result.stderr}, None
    with output.open('rb') as stream:
        elf = ELFFile(stream)
        table = elf.get_section_by_name('.symtab')
        symbol = next((symbol for symbol in table.iter_symbols() if symbol.name == origin['name']), None)
        if symbol is None or not isinstance(symbol['st_shndx'], int):
            return {'source': origin['source'], 'functionSymbolMissing': True}, None
        start, size = symbol['st_value'] & ~1, symbol['st_size']
        payload = elf.get_section(symbol['st_shndx']).data()[start:start + size]
        relocations = []
        for section in elf.iter_sections():
            if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != symbol['st_shndx']:
                continue
            symbols = elf.get_section(section['sh_link'])
            for relocation in section.iter_relocations():
                offset, kind = relocation['r_offset'] - start, relocation['r_info_type']
                if not 0 <= offset < size:
                    continue
                if kind not in MASKS or offset + 4 > size or section['sh_type'] != 'SHT_RELA':
                    return {'source': origin['source'], 'unsupportedRelocation': kind}, None
                relocations.append({'offset': offset, 'type': kind, 'symbol': symbols.get_symbol(relocation['r_info_sym']).name, 'addend': relocation['r_addend']})
        offsets = tuple(sorted((rel['offset'], MASKS[rel['type']]) for rel in relocations))
    entry = {**origin, 'bytes': size, 'relocations': relocations, 'compilerFlags': flags,
             'compiler': compiler.relative_to(ROOT).as_posix(), 'compilerSha256': utility_runtime.sha(compiler.read_bytes()),
             'probeObject': output.relative_to(ROOT).as_posix(), 'probeObjectSha256': utility_runtime.sha(output.read_bytes())}
    return {'source': origin['source'], 'compiledBytes': size, 'relocations': relocations,
            'probeObject': entry['probeObject'], 'probeObjectSha256': entry['probeObjectSha256']}, (entry, offsets, payload)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', required=True)
    parser.add_argument('--processor', choices=['arm9', 'arm7'], default='arm9')
    parser.add_argument('--mode', choices=['arm', 'thumb'], default='thumb')
    parser.add_argument('--compiler', default='1.2/base')
    parser.add_argument('--limit', type=int, default=300)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--speed', action='store_true')
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    report_path = ROOT / f'evidence/matches/utility-{args.batch}.json'
    if args.verify:
        report = json.loads(report_path.read_text())
        results = []
        for entry in report['matches']:
            provenance = entry['sourceReuseProvenance']
            for path, digest in ((entry['source'], entry['sourceSha256']), (provenance['source'], provenance['sourceSha256'])):
                if utility_runtime.sha((ROOT / path).read_bytes()) != digest:
                    raise ValueError('Frozen cross-compiler C source or provenance changed')
            result = draft_utility.validate(entry, utility_code.accepted_spec(entry))
            result['sourceReuseProvenance'] = provenance
            results.append(result)
        report.update(matches=results, nativeSymbolBindings=native_bindings(results))
        report_path.write_text(json.dumps(report, indent=2) + '\n')
        print({'verified': len(results), 'bytes': sum(entry['bytes'] for entry in results)})
        return
    if report_path.exists():
        raise ValueError('Choose a new cross-compiler C batch')
    compiler = ROOT / f'tools/mwccarm/mwccarm/{args.compiler}/mwccarm.exe'
    if utility_runtime.sha(compiler.read_bytes()) != utility_code.compiler_pins().get(compiler.relative_to(ROOT).as_posix()):
        raise ValueError('Cross-compiler probe identity changed')
    flags = match_lowlevel.FLAGS[:]
    flags[flags.index('-proc') + 1] = 'arm946e' if args.processor == 'arm9' else 'arm7tdmi'
    if args.mode == 'thumb':
        flags.append('-thumb')
    if args.speed:
        flags.extend(['-opt', 'speed'])
    accepted = defaultdict(list)
    for path in (ROOT / 'evidence/matches').glob('utility-*.json'):
        for entry in json.loads(path.read_text()).get('matches', []):
            start = int(entry['address'], 0)
            accepted[entry['module']].append((start, start + entry['bytes']))
    for entry in utility_bridges.derive()['bridges']:
        start = int(entry['address'], 0)
        accepted[entry['module']].append((start, start + 12))
    layout, files = utility_runtime.derive()
    candidates = [spec for spec in utility_code.candidates() if spec['processor'] == args.processor and spec['mode'] == args.mode and
                  not any(start < spec['address'] + spec['bytes'] and spec['address'] < end for start, end in accepted[spec['module']])]
    by_size = defaultdict(list)
    for spec in candidates:
        by_size[spec['bytes']].append(spec)
    directory = ROOT / f'work/lowlevel-recovery/crossreuse/{args.batch}'
    directory.mkdir(parents=True, exist_ok=True)
    attempts, matches = [], []
    selected = sources(args.processor)[args.offset:args.offset + args.limit]
    for index, origin in enumerate(selected):
        attempt, compiled = compile_origin(origin, compiler, flags, directory)
        attempts.append(attempt)
        if compiled is None:
            continue
        derived, offsets, payload = compiled
        digest = reuse.normalized(payload, offsets)
        for spec in by_size.get(len(payload), []):
            if any(start < spec['address'] + spec['bytes'] and spec['address'] < end for start, end in accepted[spec['module']]):
                continue
            native = bytes(files[ROOT / spec['binary']][spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']])
            if reuse.normalized(native, offsets) != digest:
                continue
            text = (ROOT / origin['source']).read_text()
            rename = reuse.replacements(derived, spec, native, layout['modules'], text)
            if rename is None:
                continue
            text = re.sub(r'\b(?:' + '|'.join(map(re.escape, rename)) + r')\b', lambda match: rename[match[0]], text)
            source = directory / (spec['name'] + '.c')
            source.write_text(text)
            try:
                entry, code = utility_code.compile_compare(source, dict(spec, compilerPath=compiler), 2, 'off', args.speed)
            except match_lowlevel.UnresolvedNativeSymbol as error:
                attempt.setdefault('rejectedTargets', []).append(error.details)
                continue
            except utility_code.InterworkingRequiresLink as error:
                attempt.setdefault('rejectedTargets', []).append({'module': spec['module'], 'address': hex(spec['address']), 'linkerRequired': str(error)})
                continue
            if code is None:
                attempt.setdefault('rejectedTargets', []).append(entry)
                continue
            frozen = ROOT / f'src/utility/{args.batch}/{spec["name"]}.c'
            frozen.parent.mkdir(parents=True, exist_ok=True)
            if frozen.exists() or len(text.splitlines()) > 500:
                raise ValueError('Refusing to overwrite C or exceed source line bound')
            frozen.write_text(text)
            entry.update(source=frozen.relative_to(ROOT).as_posix(), sourceSha256=utility_runtime.sha(frozen.read_bytes()))
            validated = draft_utility.validate(entry, spec)
            validated['sourceReuseProvenance'] = {key: origin[key] for key in ('source', 'sourceSha256', 'address', 'module')}
            validated['sourceReuseProvenance'].update(originalName=origin['name'], rename=rename, ordinaryCOnly=True,
                                                       discoveryCompiler=derived['compiler'], discoveryCompilerFlags=flags)
            matches.append(validated)
            accepted[spec['module']].append((spec['address'], spec['address'] + spec['bytes']))
            print({'matched': spec['module'], 'address': hex(spec['address']), 'bytes': spec['bytes'], 'origin': origin['source']}, flush=True)
        if index % 50 == 0:
            print({'originsCompiled': index + 1, 'matches': len(matches)}, flush=True)
    report = {'schemaVersion': 1, 'romSha256': utility_runtime.audit_regions.ROM_HASH, 'program': utility_runtime.PROGRAM,
              'runtimeMappingCanonical': True, 'matches': matches, 'nativeSymbols': {rel['symbol']: rel['target'] for entry in matches for rel in entry['relocations']},
              'nativeSymbolBindings': native_bindings(matches), 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'limitations': ['Published ordinary C is compiled for a new pinned processor/mode/compiler configuration before candidate selection',
                              'Native bytes select full-span candidates but never become C or object input; each renamed target is freshly recompiled and compared',
                              'Origin source hashes remain required for provenance; replay never requires original probe or accepted origin objects',
                              'Behavioral limitations are attached per function, and whole-module linking remains separately required']}
    (ROOT / f'evidence/attempts/utility-{args.batch}.json').write_text(json.dumps(attempts, indent=2) + '\n')
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print({'origins': len(selected), 'functions': len(matches), 'bytes': sum(entry['bytes'] for entry in matches)})


if __name__ == '__main__':
    main()
