import hashlib
from project import ROOT, configuration, sha256, write_json
import prove_main_heap_sort_near_20261030 as support
import link_runtime_unit
from match_main_overlap_copy_20261030 import main_references
from main_string_routines_native_20261030 import oracle
from elftools.elf.elffile import ELFFile

WORK = ROOT / 'work/main-string-routines-20261030'


def main():
    support.FLAGS = list(support.compiler.FLAGS)
    assert support.FLAGS[0] == '-O2'
    support.FLAGS[0] = '-O3'
    support.FLAGS += ['-opt', 'speed']
    compiler = support.compiler.COMPILER
    assert sha256(compiler) == support.compiler.COMPILER_PINS[compiler.relative_to(ROOT).as_posix()]
    metadata, binary, config = link_runtime_unit.measured_module('main')
    entries = []
    for address, size, kind in [(0x0201D6B8, 200, 'copy'), (0x0201D800, 276, 'compare')]:
        directory = WORK / f'{address:08x}'
        directory.mkdir(parents=True, exist_ok=True)
        support.WORK = directory
        name = f'native_main_{address:08x}'
        source = 'src/runtime/20261030_strings/' + name + '.c'
        obj, body = support.build(ROOT / source, name, 'source')
        offset = address - int(metadata['base'], 0)
        original = binary[offset:offset + size]
        assert len(body) == size and body == original
        with obj.open('rb') as stream:
            elf = ELFFile(stream)
            symbol = elf.get_section_by_name('.symtab').get_symbol_by_name(name)[0]
            section, start = symbol['st_shndx'], symbol['st_value']
            for row in elf.iter_sections():
                if row['sh_type'] in ('SHT_REL', 'SHT_RELA') and row['sh_info'] == section:
                    assert row.num_relocations() == 0
        entry = {'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'address': hex(address),
                 'name': name, 'bytes': size, 'size': size, 'targetSha256': hashlib.sha256(original).hexdigest(),
                 'source': source, 'sourceSha256': sha256(ROOT / source), 'object': obj.relative_to(ROOT).as_posix(),
                 'objectSha256': sha256(obj), 'sectionIndex': section, 'sectionOffset': start,
                 'compiler': compiler.relative_to(ROOT).as_posix(), 'compilerSha256': sha256(compiler),
                 'compilerFlags': support.FLAGS, 'relocations': [], 'sourceDependencies': [], 'sourceLanguage': 'C',
                 'exactBytes': body == original, 'exactAfterDeclaredRelocation': body == original,
                 'originalObjectScaffolding': False, 'ordinaryFunctionCredit': 1, 'wholeModuleLinked': False}
        entry['boundaries'] = dict(main_references(entry, binary, config), generatedLiteralOrPaddingBytes=8,
                                   instructionBytes=size - 8, literalPoolBytes=8)
        link = (directory / 'real-main-link').resolve()
        assert link.is_relative_to(WORK.resolve())
        for filename in ['caller.bin', 'linked.elf']:
            path = link / filename
            if path.exists():
                path.unlink()
        entry['realMainLink'] = link_runtime_unit.validate(entry, {}, link)
        rebuilt = (link / 'caller.bin').read_bytes()
        assert rebuilt == body == original
        entry['oracle'] = oracle(original, rebuilt, address, kind)
        entries.append(entry)
        print({'function': name, 'bytes': size, 'actualReturns': entry['oracle']['actualOriginalAndSourceReturns']}, flush=True)
    files = ['match_main_string_routines_20261030.py', 'main_string_routines_native_20261030.py',
             'prove_main_heap_sort_near_20261030.py', 'match_main_overlap_copy_20261030.py',
             'link_runtime_unit.py', 'match_runtime.py']
    report = {'romSha256': configuration()['romSha256'], 'functionMatches': entries, 'matchedFunctions': len(entries),
              'matchedBytes': sum(row['bytes'] for row in entries), 'inputModuleSha256': metadata['sha256'],
              'generatorSources': [{'path': path, 'sha256': sha256(ROOT / path)} for path in files],
              'compiler': {'path': compiler.relative_to(ROOT).as_posix(), 'sha256': sha256(compiler), 'flags': support.FLAGS},
              'referenceEvidence': 'evidence/research/20261030-msl-reader-and-string-reference-source.json',
              'limitations': ['Sibling-project C is a reference hypothesis, not proof of the original library version',
                  'No assembly, fixed-register assignments or original executable inputs compile into these products',
                  'No source-only module or complete game claim is made']}
    path = ROOT / 'evidence/matches/main-string-routines-20261030.json'
    write_json(path, report)
    print({'functions': len(entries), 'bytes': report['matchedBytes'], 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
