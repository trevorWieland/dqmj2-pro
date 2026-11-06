import re
from pathlib import Path
from project import ROOT, read_json, sha256


WITNESS = 'evidence/lanes/parallel-wave20261105/weak-source-export-scope/proven-weak-exports-v2.json'
APPROVED = {'native_main_02000800': (0x02000800, 316), 'native_main_02008430': (0x02008430, 16), 'native_main_0201a670': (0x0201a670, 2300)}


def source_weak_export(unit, elf):
    name = unit.get('function') or unit.get('symbol')
    if name not in APPROVED:
        return None
    evidence = read_json(ROOT / WITNESS)
    constituents = []
    for pin in evidence['constituentWitnesses']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
        constituents.extend(read_json(ROOT / pin['path'])['exports'])
    assert evidence['exports'] == constituents
    assert evidence['scope'] == 'generated-canonical-source-export-records-only'
    assert evidence['requiredCompilerBinding'] == 14 and evidence['sourceByteCredit'] == 0
    assert {r['name'] for r in evidence['exports']} == set(APPROVED)
    row = next(r for r in evidence['exports'] if r['name'] == name)
    start, size = APPROVED[name]
    assert unit['module'] == 'main' and int(unit['start'], 0) == start and int(unit['end'], 0) == start + size
    assert int(row['address'], 0) == start and row['bytes'] == size
    source = (ROOT / unit['source']).resolve()
    assert source == (ROOT / row['source']).resolve() and source.is_relative_to(ROOT / 'src')
    assert sha256(source) == row['sourceSha256'] == unit['sourceSha256']
    published = (ROOT / row['publishedSource']).resolve()
    assert published.is_relative_to(ROOT / 'deps/reference') and sha256(published) == row['publishedSourceSha256']
    assert row['publishedWeakDeclaration'] in re.sub(r'\s+', ' ', published.read_text(encoding='utf-8'))
    result_type = 'int' if name == 'native_main_0201a670' else 'void'
    assert re.search(r'__declspec\(weak\)\s+(?:asm\s+)?' + result_type + r'\s+' + re.escape(name) + r'\s*\(', source.read_text(encoding='utf-8'))
    table = elf.get_section_by_name('.symtab')
    symbols = [(i, s) for i, s in enumerate(table.iter_symbols()) if s.name == name]
    assert len(symbols) == 1 and elf.elfclass == 32 and elf.little_endian
    index, symbol = symbols[0]
    assert isinstance(symbol['st_shndx'], int) and symbol['st_size'] == size
    elf.stream.seek(table['sh_offset'] + index * table['sh_entsize'] + 12)
    info = elf.stream.read(1)[0]
    assert info >> 4 == 14 and info & 15 == 2
    aliases = [old for old, new in unit.get('symbols', {}).items() if new == name]
    assert len(aliases) == 1
    return dict(name=name, originalName=aliases[0], address=hex(start), bytes=size,
        compilerBinding=14, generatedScope='weak', source=row['source'], sourceSha256=row['sourceSha256'],
        publishedSource=row['publishedSource'], publishedSourceSha256=row['publishedSourceSha256'],
        witness=WITNESS, witnessSha256=sha256(ROOT / WITNESS), sourceCredit=0)


def weak_record(rest):
    assert not re.search(r'(?:^|\s)local(?:\s|$)', rest)
    if re.search(r'(?:^|\s)weak(?:\s|$)', rest):
        return rest
    newline = '\n' if rest.endswith('\n') else ''
    return rest.rstrip('\r\n') + ' weak' + newline
