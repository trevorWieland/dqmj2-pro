import hashlib
from project import ROOT, configuration, sha256, write_json
import prove_main_heap_sort_near_20261030 as compiler_support
import link_runtime_unit
from match_main_overlap_copy_20261030 import main_references
from main_string_reader_native_20261030 import oracle
from elftools.elf.elffile import ELFFile

SOURCE = 'src/runtime/20261030_string_reader/native_main_0201d618.c'
WORK = ROOT / 'work/main-string-reader-20261030'
NAME, ADDRESS, SIZE = 'native_main_0201d618', 0x0201D618, 132


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    compiler_support.WORK = WORK
    compiler = compiler_support.compiler.COMPILER
    assert sha256(compiler) == compiler_support.compiler.COMPILER_PINS[compiler.relative_to(ROOT).as_posix()]
    obj, body = compiler_support.build(ROOT / SOURCE, NAME, 'source')
    metadata, binary, config = link_runtime_unit.measured_module('main')
    offset = ADDRESS - int(metadata['base'], 0)
    original = binary[offset:offset + SIZE]
    assert len(body) == SIZE and body == original
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = elf.get_section_by_name('.symtab').get_symbol_by_name(NAME)[0]
        section, start = symbol['st_shndx'], symbol['st_value']
        for row in elf.iter_sections():
            if row['sh_type'] in ('SHT_REL', 'SHT_RELA') and row['sh_info'] == section:
                assert row.num_relocations() == 0
    entry = {'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'address': hex(ADDRESS),
             'name': NAME, 'bytes': SIZE, 'size': SIZE, 'targetSha256': hashlib.sha256(original).hexdigest(),
             'source': SOURCE, 'sourceSha256': sha256(ROOT / SOURCE), 'object': obj.relative_to(ROOT).as_posix(),
             'objectSha256': sha256(obj), 'sectionIndex': section, 'sectionOffset': start,
             'compiler': compiler.relative_to(ROOT).as_posix(), 'compilerSha256': sha256(compiler),
             'compilerFlags': compiler_support.FLAGS, 'relocations': [], 'sourceDependencies': [],
             'sourceLanguage': 'C', 'exactBytes': body == original, 'exactAfterDeclaredRelocation': body == original,
             'originalObjectScaffolding': False, 'ordinaryFunctionCredit': 1, 'wholeModuleLinked': False}
    entry['boundaries'] = main_references(entry, binary, config)
    directory = (WORK / 'real-main-link').resolve()
    assert directory.is_relative_to(WORK.resolve())
    for name in ['caller.bin', 'linked.elf']:
        path = directory / name
        if path.exists():
            path.unlink()
    entry['realMainLink'] = link_runtime_unit.validate(entry, {}, directory)
    rebuilt = (directory / 'caller.bin').read_bytes()
    assert rebuilt == body == original
    entry['oracle'] = oracle(original, rebuilt)
    files = ['match_main_string_reader_20261030.py', 'main_string_reader_native_20261030.py',
             'prove_main_heap_sort_near_20261030.py', 'match_main_overlap_copy_20261030.py',
             'link_runtime_unit.py', 'match_runtime.py']
    report = {'romSha256': configuration()['romSha256'], 'functionMatches': [entry], 'matchedFunctions': 1,
              'matchedBytes': SIZE, 'inputModuleSha256': metadata['sha256'],
              'generatorSources': [{'path': path, 'sha256': sha256(ROOT / path)} for path in files],
              'compiler': {'path': compiler.relative_to(ROOT).as_posix(), 'sha256': sha256(compiler), 'flags': compiler_support.FLAGS},
              'limitations': ['MSL callback identity is a reference-supported hypothesis; native behavior is separately modeled',
                  'No ordinary gameplay, source-only module or complete game claim is made']}
    path = ROOT / 'evidence/matches/main-string-reader-20261030.json'
    write_json(path, report)
    print({'functions': 1, 'bytes': SIZE, 'actualReturns': entry['oracle']['actualOriginalAndSourceReturns'],
           'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
