import argparse
import json
import re
from pathlib import Path
import utility_code
import utility_runtime
import draft_utility
from match_utility_primitives import native_bindings

ROOT = Path(__file__).resolve().parent


def variants(text):
    result = []
    pointers = {match[2]: int(match[1][1:]) // 8 for match in re.finditer(r'\b(u16|u32)\s*\*\s*(\w+)', text)}
    for name, width in pointers.items():
        for match in re.finditer(r'\b' + re.escape(name) + r'\s*\+=\s*(0x[0-9A-Fa-f]+|[0-9]+);', text):
            amount = int(match[1], 0)
            if amount and amount % width == 0:
                changed = text[:match.start()] + name + ' += ' + hex(amount // width) + ';' + text[match.end():]
                result.append(('byte-extent-pointer-increment-' + name, changed))
        for match in re.finditer(r'\b' + re.escape(name) + r'\s*\+\s*(0x[0-9A-Fa-f]+|[0-9]+)\b', text):
            changed = text[:match.start()] + '(u8 *)' + name + ' + ' + match[1] + text[match.end():]
            result.append(('byte-offset-pointer-add-' + name, changed))
    for match in re.finditer(r'extern (u32|u16) (native_(?:utility|arm7)_\w+);', text):
        for kind in ('u8', 'u16'):
            if kind != match[1]:
                result.append(('scalar-' + match[2] + '-' + kind, text[:match.start()] + f'extern {kind} {match[2]};' + text[match.end():]))
    for match in re.finditer(r'extern u8 (native_(?:utility|arm7)_\w+)\[\];', text):
        for kind in ('u32', 'u16'):
            result.append(('global-' + match[1] + '-' + kind, text[:match.start()] + f'extern {kind} {match[1]}[];' + text[match.end():]))
    unsigned = re.sub(r's16 \*,([^\n]+)\) = (0x[89A-Fa-f][0-9A-Fa-f]{3});', r'u16 *,\1) = \2;', text)
    result.append(('unsigned-halfword-constants', unsigned))
    result.append(('unsigned-promotions', re.sub(r'\b(arg\d+) >>', r'(u32) \1 >>', text)))
    promoted = text
    for match in list(re.finditer(r'\(u16\) M2C_FIELD\(', text))[::-1]:
        opening = text.index('(', match.start() + len('(u16) M2C_FIELD'))
        depth, cursor = 1, opening + 1
        while cursor < len(text) and depth:
            depth += (text[cursor] == '(') - (text[cursor] == ')')
            cursor += 1
        if not depth and re.match(r'\s*>>', text[cursor:]):
            promoted = promoted[:match.start()] + '(u32) ' + promoted[match.start():]
    result.append(('unsigned-field-promotions', promoted))
    result.append(('stack-halfword-order', text.replace('u16 sp2;\n    u16 sp0;', 'u16 sp0;\n    u16 sp2;')))
    result.append(('pointer-base-addition', re.sub(r'\b(var_\w+) \+= (arg\d+);', r'\1 = (u32)((u8 *)\2 + \1);', text)))
    for match in re.finditer(r'\bu16 (arg\d+)\b', text):
        result.append(('word-argument-' + match[1], text[:match.start()] + 'u32 ' + match[1] + text[match.end():]))
    unique = set()
    for name, value in result:
        if value != text and value not in unique:
            unique.add(value)
            yield name, value


def stack_buffer_variant(text, spec):
    frames = [int(match[1], 0) for instruction in spec['instructions'] if instruction.mnemonic == 'sub'
              for match in [re.fullmatch(r'sp, sp, #(0x[0-9a-f]+|[0-9]+)', instruction.op_str)] if match]
    declaration = re.search(r'\b(?:s32|u32) sp0;', text)
    if len(frames) != 1 or not 8 <= frames[0] <= 4096 or declaration is None:
        return []
    remainder = text[:declaration.start()] + text[declaration.end():]
    if '&sp0' not in remainder or re.search(r'\bsp0\b', remainder.replace('&sp0', '')):
        return []
    return [('address-only-measured-frame-buffer', text[:declaration.start()] + f'u8 sp0[{frames[0]}];' + text[declaration.end():])]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', required=True)
    parser.add_argument('--limit', type=int, default=120)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    report_path = ROOT / f'evidence/matches/utility-{args.batch}.json'
    if args.verify:
        report = json.loads(report_path.read_text())
        matches = []
        for entry in report['matches']:
            if utility_runtime.sha((ROOT / entry['source']).read_bytes()) != entry['sourceSha256']:
                raise ValueError('Frozen utility C refinement source changed')
            matches.append(draft_utility.validate(entry, utility_code.accepted_spec(entry)))
        report.update(matches=matches, nativeSymbolBindings=native_bindings(matches))
        report_path.write_text(json.dumps(report, indent=2) + '\n')
        print({'verified': len(matches), 'bytes': sum(entry['bytes'] for entry in matches)})
        return
    if report_path.exists():
        raise ValueError('Choose a new C refinement batch')
    accepted = {(entry['module'], int(entry['address'], 0)) for path in (ROOT / 'evidence/matches').glob('utility-*.json') for entry in json.loads(path.read_text()).get('matches', [])}
    specs = {(spec['module'], spec['address']): spec for spec in utility_code.candidates()}
    rows = json.loads((ROOT / 'work/lowlevel-recovery/utility-near-matches.json').read_text())
    selected = [row for row in rows if (row['module'], int(row['address'], 0)) not in accepted][args.offset:args.offset + args.limit]
    work = ROOT / 'work/lowlevel-recovery/utility-refinements' / args.batch
    work.mkdir(parents=True, exist_ok=True)
    matches, attempts = [], []
    for row in selected:
        spec = specs[row['module'], int(row['address'], 0)]
        text = (ROOT / row['source']).read_text()
        flags = row['attempt']['compilerFlags']
        settings = dict(spec, compilerPath=ROOT / row['attempt']['compiler'], compilerProc=flags[flags.index('-proc') + 1])
        result = {'module': spec['module'], 'address': hex(spec['address']), 'attempts': []}
        for hypothesis, changed in [*variants(text), *stack_buffer_variant(text, spec)]:
            source = work / (spec['name'] + '-' + utility_runtime.sha(changed.encode())[:16] + '.c')
            source.write_text(changed)
            entry, compiled = utility_code.compile_compare(source, settings, int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
            entry['sourceHypothesis'] = hypothesis
            result['attempts'].append(entry)
            if compiled is None:
                continue
            frozen = ROOT / f'src/utility/{args.batch}' / (spec['name'] + '.c')
            frozen.parent.mkdir(parents=True, exist_ok=True)
            if frozen.exists():
                raise ValueError('Refusing to overwrite accepted C')
            frozen.write_bytes(source.read_bytes())
            entry.update(source=frozen.relative_to(ROOT).as_posix(), sourceSha256=utility_runtime.sha(frozen.read_bytes()))
            matches.append(draft_utility.validate(entry, spec))
            result['accepted'] = True
            break
        attempts.append(result)
        (work / (spec['name'] + '.json')).write_text(json.dumps(result, indent=2) + '\n')
        print({'module': spec['module'], 'address': hex(spec['address']), 'matched': result.get('accepted', False), 'attempts': len(result['attempts'])}, flush=True)
    report = {'schemaVersion': 1, 'romSha256': utility_runtime.audit_regions.ROM_HASH, 'program': utility_runtime.PROGRAM,
              'runtimeMappingCanonical': True, 'matches': matches,
              'nativeSymbols': {rel['symbol']: rel['target'] for entry in matches for rel in entry['relocations']},
              'nativeSymbolBindings': native_bindings(matches), 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'limitations': ['C width, promotion, stack-local and pointer arithmetic hypotheses are accepted only after complete native byte and real ELF relocation agreement', 'Unsupported native effects remain explicit; no source-language or original compiler attribution is asserted']}
    (ROOT / f'evidence/attempts/utility-{args.batch}.json').write_text(json.dumps(attempts, indent=2) + '\n')
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': len(matches), 'bytes': sum(entry['bytes'] for entry in matches)})


if __name__ == '__main__':
    main()
