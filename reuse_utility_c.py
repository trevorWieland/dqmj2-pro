import argparse
import json
import re
import struct
from collections import defaultdict
from pathlib import Path
import utility_code
import utility_runtime
import draft_utility
import utility_bridges
from match_utility_primitives import native_bindings
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent


def normalized(payload, offsets):
    result = bytearray(payload)
    for offset, mask in offsets:
        value = struct.unpack_from('<I', result, offset)[0]
        struct.pack_into('<I', result, offset, value & mask)
    return utility_runtime.sha(result)


def origins():
    indexed = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    batches = json.loads((ROOT / 'recovery.json').read_text())['batches']
    seen = set()
    for batch in batches:
        for entry in json.loads((ROOT / batch['report']).read_text()).get('matches', []):
            source = ROOT / entry.get('source', '')
            identity = (source, entry.get('name', entry.get('symbol')), entry.get('sectionIndex'), entry.get('sectionOffset', 0))
            if source.suffix != '.c' or identity in seen or not entry.get('object'):
                continue
            seen.add(identity)
            if 'sourceSha256' not in entry or 'objectSha256' not in entry:
                continue
            if utility_runtime.sha(source.read_bytes()) != entry['sourceSha256']:
                raise ValueError('Origin published C identity changed')
            obj = ROOT / entry['object']
            if not obj.exists():
                continue
            if utility_runtime.sha(obj.read_bytes()) != entry['objectSha256']:
                raise ValueError('Origin immutable C object changed')
            size = entry.get('bytes', entry.get('size'))
            masks = {1: 0xFF000000, 2: 0, 10: 0xF800F800, 15: 0xFE000000, 28: 0xFF000000, 29: 0xFF000000}
            if any(rel['type'] not in masks for rel in entry.get('relocations', [])):
                continue
            offsets = tuple(sorted((rel['offset'], masks[rel['type']]) for rel in entry.get('relocations', [])))
            if any(offset < 0 or offset + 4 > size for offset, mask in offsets):
                continue
            with obj.open('rb') as stream:
                elf = ELFFile(stream)
                if 'sectionIndex' not in entry:
                    continue
                section = elf.get_section(entry['sectionIndex'])
                offset = entry.get('sectionOffset', 0)
                payload = section.data()[offset:offset + size]
            if len(payload) == size:
                indexed[entry.get('mode', 'arm').lower(), size][offsets][normalized(payload, offsets)].append(entry)
    return indexed


def replacements(entry, spec, payload, modules, source_text):
    result = {entry.get('name', entry.get('symbol')): spec['name']}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if spec['mode'] == 'thumb' else CS_MODE_ARM)
    decoder.detail = True
    for relocation in entry.get('relocations', []):
        at, kind = relocation['offset'], relocation['type']
        if kind == 2:
            literal = struct.unpack_from('<I', payload, at)[0]
            addend = relocation.get('addend', 0)
            target = (literal - addend) & 0xFFFFFFFF
            old_name = relocation['symbol']
            function = relocation.get('targetMode') in ('arm', 'thumb') or old_name.startswith(('native_fn_', 'func_')) or re.search(r'\b' + re.escape(old_name) + r'\s*\(', source_text)
            if function and addend:
                return None
            mode = ('thumb' if target & 1 else 'arm') if function else 'data'
        elif kind in (1, 10, 15, 28, 29):
            instruction = next(decoder.disasm(payload[at:at + 4], spec['address'] + at), None)
            if instruction is None or not instruction.operands or instruction.operands[0].type != 2 or not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)):
                return None
            target = instruction.operands[0].imm & 0xFFFFFFFF
            mode = ('thumb' if spec['mode'] == 'arm' else 'arm') if instruction.mnemonic == 'blx' else spec['mode']
        else:
            return None
        if mode != 'data' and not any(module['processor'] == spec['processor'] and int(module['base'], 0) <= (target & ~1) < int(module['base'], 0) + module['bytes'] for module in modules):
            return None
        label = f"native_utility_child_{spec['processor']}_{mode}_{target:08x}"
        old = relocation['symbol']
        if old in result and result[old] != label:
            return None
        result[old] = label
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', default='reuse01')
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    path = ROOT / f'evidence/matches/utility-{args.batch}.json'
    if args.verify:
        report = json.loads(path.read_text())
        matches = []
        for entry in report['matches']:
            if utility_runtime.sha((ROOT / entry['source']).read_bytes()) != entry['sourceSha256']:
                raise ValueError('Frozen utility reuse C changed')
            provenance = entry['sourceReuseProvenance']
            if utility_runtime.sha((ROOT / provenance['source']).read_bytes()) != provenance['sourceSha256']:
                raise ValueError('Original recovered C provenance changed')
            result = draft_utility.validate(entry, utility_code.accepted_spec(entry))
            result['sourceReuseProvenance'] = provenance
            matches.append(result)
        report.update(matches=matches, nativeSymbolBindings=native_bindings(matches))
        path.write_text(json.dumps(report, indent=2) + '\n')
        print({'verified': len(matches), 'bytes': sum(entry['bytes'] for entry in matches)})
        return
    if path.exists():
        raise ValueError('Choose a new C reuse batch')
    indexed = origins()
    layout, files = utility_runtime.derive()
    accepted = defaultdict(list)
    for report in (ROOT / 'evidence/matches').glob('utility-*.json'):
        for entry in json.loads(report.read_text()).get('matches', []):
            start = int(entry['address'], 0)
            accepted[entry['module']].append((start, start + entry['bytes']))
    for bridge in utility_bridges.derive()['bridges']:
        start = int(bridge['address'], 0)
        accepted[bridge['module']].append((start, start + 12))
    work = ROOT / 'work/lowlevel-recovery/utility-reuse' / args.batch
    work.mkdir(parents=True, exist_ok=True)
    matches, attempts, eligible = [], [], 0
    for spec in utility_code.candidates():
        if any(first < spec['address'] + spec['bytes'] and spec['address'] < last for first, last in accepted[spec['module']]):
            continue
        native = bytes(files[ROOT / spec['binary']][spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']])
        found = False
        for offsets, digests in indexed.get((spec['mode'], spec['bytes']), {}).items():
            for origin in digests.get(normalized(native, offsets), []):
                text = (ROOT / origin['source']).read_text()
                rename = replacements(origin, spec, native, layout['modules'], text)
                if rename is None:
                    continue
                eligible += 1
                text = re.sub(r'\b(?:' + '|'.join(map(re.escape, rename)) + r')\b', lambda match: rename[match[0]], text)
                if len(text.splitlines()) > 500 or '#include' in text:
                    continue
                source = work / (spec['name'] + '-' + utility_runtime.sha(text.encode())[:16] + '.c')
                source.write_text(text)
                flags = origin['compilerFlags']
                compiler = origin.get('compiler', origin.get('compilerPath', utility_code.COMPILER.relative_to(ROOT).as_posix()))
                if utility_runtime.sha((ROOT / compiler).read_bytes()) != origin['compilerSha256']:
                    raise ValueError('Origin C compiler identity cannot be reproduced')
                settings = dict(spec, compilerPath=ROOT / compiler, interworking='-nointerworking' not in flags)
                try:
                    optimization = re.fullmatch(r'-O(\d+)(?:,[a-z]+)?', flags[0])
                    if optimization is None:
                        raise ValueError('Unsupported original C optimization flag')
                    entry, code = utility_code.compile_compare(source, settings, int(optimization[1]), flags[flags.index('-inline') + 1] if '-inline' in flags else 'off', 'speed' in flags or ',p' in flags[0])
                except utility_code.match_lowlevel.UnresolvedNativeSymbol as error:
                    attempts.append({**error.details, 'module': spec['module'], 'address': hex(spec['address']), 'source': source.relative_to(ROOT).as_posix(),
                                     'sourceSha256': utility_runtime.sha(source.read_bytes()), 'originSource': origin['source']})
                    continue
                attempts.append(entry)
                if code is None:
                    continue
                frozen = ROOT / f'src/utility/{args.batch}' / (spec['name'] + '.c')
                frozen.parent.mkdir(parents=True, exist_ok=True)
                if frozen.exists():
                    raise ValueError('Refusing to overwrite reused C source')
                frozen.write_bytes(source.read_bytes())
                entry.update(source=frozen.relative_to(ROOT).as_posix(), sourceSha256=utility_runtime.sha(frozen.read_bytes()))
                result = draft_utility.validate(entry, spec)
                result['sourceReuseProvenance'] = {key: origin[key] for key in ('source', 'sourceSha256', 'address', 'module')}
                result['sourceReuseProvenance'].update(originalName=origin.get('name', origin.get('symbol')), rename=rename, ordinaryCOnly=True)
                matches.append(result)
                accepted[spec['module']].append((spec['address'], spec['address'] + spec['bytes']))
                print({'module': spec['module'], 'address': hex(spec['address']), 'bytes': spec['bytes'], 'origin': origin['source']}, flush=True)
                found = True
                break
            if found:
                break
    report = {'schemaVersion': 1, 'romSha256': utility_runtime.audit_regions.ROM_HASH, 'program': utility_runtime.PROGRAM,
              'runtimeMappingCanonical': True, 'matches': matches,
              'nativeSymbols': {rel['symbol']: rel['target'] for entry in matches for rel in entry['relocations']},
              'nativeSymbolBindings': native_bindings(matches), 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'limitations': ['Only ordinary recovered C is cloned; native bytes select candidates but are never source/object input', 'Entry and extern symbol renaming is accepted only after actual recompilation and complete native ELF-relocation agreement', 'Each utility module/processor and nonoverlap range is independently checked; unsupported behavioral paths remain explicit']}
    (ROOT / f'evidence/attempts/utility-{args.batch}.json').write_text(json.dumps(attempts, indent=2) + '\n')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print({'eligiblePairs': eligible, 'functions': len(matches), 'bytes': sum(entry['bytes'] for entry in matches)})


if __name__ == '__main__':
    main()
