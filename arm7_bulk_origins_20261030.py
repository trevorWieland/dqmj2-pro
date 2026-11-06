import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
import arm7_bulk_source_policy_20261030 as source_policy
import utility_code
import reuse_utility_c
from recovery_registry import entries
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
MASKS = {1: 0xFF000000, 2: 0, 10: 0xF800F800, 15: 0xFE000000, 28: 0xFF000000, 29: 0xFF000000}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def origins():
    indexed = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    compiler_pins = utility_code.compiler_pins()
    source_cache, object_cache, seen = {}, {}, set()
    stats = defaultdict(int)
    for batch in json.loads((ROOT / 'recovery.json').read_text())['batches']:
        report = json.loads((ROOT / batch['report']).read_text())
        common = {key: report[key] for key in ('source', 'sourceSha256', 'compiler', 'compilerSha256', 'flags', 'compilerFlags', 'processor', 'mode', 'program', 'object', 'objectSha256') if key in report}
        for value in entries(report):
            row = dict(common, **value)
            source = ROOT / row.get('source', '')
            size = row.get('bytes', row.get('size'))
            if source.suffix != '.c' or not row.get('object') or not isinstance(size, int) or not 8 <= size <= 2048 or row.get('ordinaryFunctionCredit') == 0:
                continue
            if not row.get('sourceSha256') or not row.get('objectSha256'):
                continue
            if source not in source_cache:
                data = source.read_bytes()
                source_cache[source] = digest(data), data.decode('utf-8')
            source_hash, text = source_cache[source]
            if source_hash != row['sourceSha256']:
                raise ValueError('Canonical ordinary C source changed during bulk discovery')
            if not source_policy.inspect(text)['ordinarySourceCandidate']:
                stats['rejectedCommentOrStub'] += 1
                continue
            if '#include' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text) or len(text.splitlines()) > 500:
                stats['nonStandaloneOrNonOrdinarySource'] += 1
                continue
            flags = row.get('compilerFlags', row.get('flags'))
            compiler_hash = row.get('compilerSha256')
            compiler_names = [path for path, sha in compiler_pins.items() if sha == compiler_hash]
            if not flags or len(compiler_names) != 1:
                stats['unqualifiedCompilerProfile'] += 1
                continue
            obj = ROOT / row['object']
            if not obj.exists():
                stats['missingObjects'] += 1
                continue
            if obj not in object_cache:
                object_cache[obj] = digest(obj.read_bytes())
            if object_cache[obj] != row['objectSha256']:
                raise ValueError('Canonical compiled ordinary-C object changed during bulk discovery')
            with obj.open('rb') as stream:
                elf = ELFFile(stream)
                table = elf.get_section_by_name('.symtab')
                names = {row.get(key) for key in ('name', 'symbol', 'nativeAlias') if row.get(key)}
                symbols = [symbol for symbol in table.iter_symbols() if symbol.name in names and isinstance(symbol['st_shndx'], int)
                    and symbol['st_info']['type'] == 'STT_FUNC' and symbol['st_size'] == size]
                if len(symbols) != 1:
                    stats['unresolvedObjectSymbol'] += 1
                    continue
                symbol = symbols[0]
                identity = source, symbol.name, symbol['st_shndx'], symbol['st_value'] & ~1
                if identity in seen:
                    continue
                seen.add(identity)
                if not re.search(r'\b' + re.escape(symbol.name) + r'\s*\(', text):
                    stats['unresolvedAuthoredSymbol'] += 1
                    continue
                section, start = symbol['st_shndx'], symbol['st_value'] & ~1
                body = elf.get_section(section).data()[start:start + size]
                relocations = []
                invalid = False
                for rel_section in elf.iter_sections():
                    if rel_section['sh_type'] not in ('SHT_RELA', 'SHT_REL') or rel_section['sh_info'] != section:
                        continue
                    rel_table = elf.get_section(rel_section['sh_link'])
                    for relocation in rel_section.iter_relocations():
                        offset, kind = relocation['r_offset'] - start, relocation['r_info_type']
                        if not 0 <= offset < size:
                            continue
                        if kind not in MASKS or offset > size - 4 or rel_section['sh_type'] != 'SHT_RELA':
                            invalid = True
                            break
                        relocations.append({'offset': offset, 'type': kind, 'symbol': rel_table.get_symbol(relocation['r_info_sym']).name,
                            'addend': relocation['r_addend']})
                if invalid or len(body) != size:
                    stats['unsupportedRelocationOrExtent'] += 1
                    continue
            entry = dict(row, name=symbol.name, bytes=size, compiler=compiler_names[0], compilerFlags=flags,
                mode=row.get('mode', 'arm').lower(), sectionIndex=section, sectionOffset=start, relocations=relocations)
            offsets = tuple(sorted((rel['offset'], MASKS[rel['type']]) for rel in relocations))
            indexed[entry['mode'], size][offsets][reuse_utility_c.normalized(body, offsets)].append(entry)
            stats['qualifiedSourceFunctions'] += 1
    print(json.dumps({'canonicalStandaloneOriginInventory': dict(stats)}), flush=True)
    return indexed
