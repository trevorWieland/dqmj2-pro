import hashlib
from project import ROOT, configuration, sha256, write_json
import prove_main_heap_sort_near_20261030 as native
from elftools.elf.elffile import ELFFile

SOURCE = 'src/runtime/20261030_heap_sort/native_main_0201d470.c'
POLICY = 'evidence/regions/boundary-reconciliations/main-0201d470-20261030.json'
WORK = ROOT / 'work/main-heap-sort-20261030'
NAME, ADDRESS, SIZE = 'native_main_0201d470', 0x0201D470, 356


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    native.WORK = WORK
    compiler = native.compiler.COMPILER
    assert sha256(compiler) == native.compiler.COMPILER_PINS[compiler.relative_to(ROOT).as_posix()]
    metadata, binary, config = native.linker.measured_module('main')
    offset = ADDRESS - int(metadata['base'], 0)
    original = binary[offset:offset + SIZE]
    obj, body = native.build(ROOT / SOURCE, NAME, 'source')
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
             'compilerFlags': native.FLAGS, 'relocations': [], 'sourceDependencies': [],
             'sourceLanguage': 'C', 'exactBytes': body == original, 'exactAfterDeclaredRelocation': body == original,
             'originalObjectScaffolding': False, 'ordinaryFunctionCredit': 1, 'wholeModuleLinked': False,
             'boundaryReconciliation': POLICY, 'generatedLiteralOrPaddingBytes': 0,
             'tailFragmentIndependentFunctionCredit': 0}
    link_directory = (WORK / 'real-main-link').resolve()
    assert link_directory.is_relative_to(WORK.resolve())
    for name in ['caller.bin', 'linked.elf']:
        target = link_directory / name
        if target.exists():
            target.unlink()
    entry['realMainLink'] = native.linker.validate(entry, {}, link_directory)
    rebuilt = (WORK / 'real-main-link/caller.bin').read_bytes()
    assert rebuilt == body == original
    callback_source = WORK / 'synthetic_comparator.c'
    callback_source.write_text('int synthetic_comparator(const signed char *a, const signed char *b) { return (*a > *b) - (*a < *b); }\n', encoding='utf-8')
    callback_obj, callback = native.build(callback_source, 'synthetic_comparator', 'comparator')
    vectors = []
    for count in [0, 1, 2, 3, 5, 8, 17]:
        for width in [0, 1, 2, 4, 7]:
            for pattern in range(5):
                payload = bytes(((i * [0, 1, 255, 17, 113][pattern] + pattern * 63) & 255) for i in range(count * width))
                vectors.append((count, width, payload))
    vectors += [(16, 1, bytes(range(start, start + 16))) for start in range(0, 256, 16)]
    records = []
    for count, width, payload in vectors:
        before = native.execute(original, callback, payload, count, width)
        after = native.execute(rebuilt, callback, payload, count, width)
        assert before == after
        records.append({'count': count, 'width': width, 'inputSha256': hashlib.sha256(payload).hexdigest(),
                        'stateSha256': hashlib.sha256(repr(before).encode()).hexdigest(),
                        'syntheticComparatorReturns': before['syntheticComparatorReturns'] * 2})
    entry['oracle'] = {'cases': len(records), 'actualOriginalAndSourceReturns': len(records) * 2,
                       'hostProviders': 0, 'syntheticComparatorGameSourceCredit': 0, 'records': records,
                       'syntheticComparatorSourceSha256': sha256(callback_source),
                       'syntheticComparatorObjectSha256': sha256(callback_obj)}
    files = ['match_main_heap_sort_20261030.py', 'prove_main_heap_sort_near_20261030.py',
             'link_runtime_unit.py', 'match_runtime.py', 'boundary_reconciliations.py', POLICY]
    report = {'romSha256': configuration()['romSha256'], 'functionMatches': [entry], 'matchedFunctions': 1,
              'matchedBytes': SIZE, 'inputModuleSha256': metadata['sha256'],
              'generatorSources': [{'path': path, 'sha256': sha256(ROOT / path)} for path in files],
              'compiler': {'path': compiler.relative_to(ROOT).as_posix(), 'sha256': sha256(compiler), 'flags': native.FLAGS},
              'limitations': ['Synthetic comparator context is not an original game callback',
                  'Arbitrary callback effects, invalid pointers and overflowing extents are unsupported',
                  'The tail is retained within the complete compiler function and receives no separate function credit',
                  'No source-only module, full Windows game or whole-ROM completion is claimed']}
    write_json(ROOT / 'evidence/matches/main-heap-sort-20261030.json', report)
    print({'functions': 1, 'bytes': SIZE, 'actualReturns': len(records) * 2,
           'reportSha256': sha256(ROOT / 'evidence/matches/main-heap-sort-20261030.json')})


if __name__ == '__main__':
    main()
