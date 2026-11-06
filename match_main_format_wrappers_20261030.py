import hashlib
from project import ROOT, configuration, sha256, write_json
import prove_main_heap_sort_near_20261030 as support
import link_runtime_unit as linker
from match_main_overlap_copy_20261030 import main_references
from main_format_wrappers_native_20261030 import oracle
from elftools.elf.elffile import ELFFile

WORK = ROOT / 'work/main-format-wrappers-20261030'
BINDINGS = {name: {'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'kind': 'function', 'address': hex(address)}
            for name, address in [('format_write', 0x0201D398), ('format_core', 0x0201CB74), ('format_buffer', 0x0201D3DC)]}


def main():
    assert sha256(support.compiler.COMPILER) == support.compiler.COMPILER_PINS[support.compiler.COMPILER.relative_to(ROOT).as_posix()]
    metadata, binary, config = linker.measured_module('main')
    rebuilt, entries = bytearray(binary), []
    for address, size, pool in [(0x0201D3DC, 104, 4), (0x0201D444, 44, 0)]:
        directory = WORK / f'{address:08x}'
        directory.mkdir(parents=True, exist_ok=True)
        support.WORK = directory
        name = f'native_main_{address:08x}'
        source = 'src/runtime/20261030_format/' + name + '.c'
        obj, body = support.build(ROOT / source, name, 'source')
        offset = address - int(metadata['base'], 0)
        original = binary[offset:offset + size]
        assert len(body) == size
        with obj.open('rb') as stream:
            elf = ELFFile(stream)
            symbol = elf.get_section_by_name('.symtab').get_symbol_by_name(name)[0]
            section, start = symbol['st_shndx'], symbol['st_value']
        entry = {'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'address': hex(address),
                 'name': name, 'bytes': size, 'size': size, 'targetSha256': hashlib.sha256(original).hexdigest(),
                 'source': source, 'sourceSha256': sha256(ROOT / source), 'object': obj.relative_to(ROOT).as_posix(),
                 'objectSha256': sha256(obj), 'sectionIndex': section, 'sectionOffset': start,
                 'compiler': support.compiler.COMPILER.relative_to(ROOT).as_posix(), 'compilerSha256': sha256(support.compiler.COMPILER),
                 'compilerFlags': support.FLAGS, 'sourceDependencies': [], 'sourceLanguage': 'C',
                 'originalObjectScaffolding': False, 'ordinaryFunctionCredit': 1, 'wholeModuleLinked': False,
                 'nativeSymbolEntries': BINDINGS}
        link = (directory / 'real-main-link').resolve()
        assert link.is_relative_to(WORK.resolve())
        for filename in ['caller.bin', 'linked.elf']:
            path = link / filename
            if path.exists():
                path.unlink()
        entry['realMainLink'] = linker.validate(entry, BINDINGS, link)
        entry['relocations'] = [{**row, 'target': row['symbol'],
                                  'targetAddress': BINDINGS[row['symbol']]['address'],
                                  'targetMode': BINDINGS[row['symbol']]['mode'], 'targetModule': 'main',
                                  'addend': row['explicitAddend']} for row in entry['realMainLink']['originalRelocations']]
        linked = (link / 'caller.bin').read_bytes()
        assert linked == original
        entry.update(exactBytes=False, exactAfterDeclaredRelocation=linked == original)
        entry['boundaries'] = dict(main_references(entry, binary, config), generatedLiteralOrPaddingBytes=pool,
                                   instructionBytes=size - pool, literalPoolBytes=pool)
        rebuilt[offset:offset + size] = linked
        entries.append(entry)
    proof = oracle(binary, bytes(rebuilt))
    files = ['match_main_format_wrappers_20261030.py', 'main_format_wrappers_native_20261030.py',
             'prove_main_heap_sort_near_20261030.py', 'match_main_overlap_copy_20261030.py', 'link_runtime_unit.py', 'match_runtime.py']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main', 'matches': entries,
              'matchedFunctions': 2, 'matchedBytes': 148, 'nativeSymbolEntries': BINDINGS,
              'nativeSymbols': {name: row['address'] for name, row in BINDINGS.items()},
              'nativeSymbolModules': {name: row['module'] for name, row in BINDINGS.items()},
              'generatorSources': [{'path': path, 'sha256': sha256(ROOT / path)} for path in files],
              'oracle': proof, 'originalHelperCodeAndSourceCredit': 0,
              'limitations': proof['limitations']}
    path = ROOT / 'evidence/matches/main-format-wrappers-20261030.json'
    write_json(path, report)
    print({'functions': 2, 'bytes': 148, 'actualReturns': proof['actualOriginalAndSourceReturns'], 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
