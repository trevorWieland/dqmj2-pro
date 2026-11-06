import shutil
from project import ROOT, read_json, write_json, sha256, configuration
import match_ov005_callbacks296_20261031 as producer
from elftools.elf.elffile import ELFFile

RAW = 'evidence/matches/ov005-20261031-callbacks296-data.json'
OUTPUT = 'evidence/matches/ov005-20261031-callbacks296-source-data.json'


def main():
    producer.run()
    report = read_json(ROOT / RAW)
    assert report['romSha256'] == configuration()['romSha256']
    assert report['exactAfterGenuineDataLink'] and report['typedSourceDataBytes'] == 24
    assert report['authoredExecutableCodeBytes'] == 0 and not report['functionMatches']
    proof = report['proof']
    assert proof['nonExecutable'] and proof['calleeCodeBytes'] == 0
    assert all(anchor['initializedCalleeCodeBytes'] == 0 for anchor in proof['anchors'])
    obj = ROOT / proof['object']
    assert sha256(obj) == proof['objectSha256']
    frozen = ROOT / 'work/ov005-callbacks296-source-data-20261031/objects' / (sha256(obj) + '.o')
    frozen.parent.mkdir(parents=True, exist_ok=True)
    if frozen.exists() and frozen.read_bytes() != obj.read_bytes():
        raise ValueError('Frozen data object collision')
    shutil.copy2(obj, frozen)
    with frozen.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == producer.NAME)
        section = elf.get_section(symbol['st_shndx'])
        assert symbol['st_info']['type'] == 'STT_OBJECT' and symbol['st_size'] == 24
        assert not section['sh_flags'] & 4
        section_index, section_offset = symbol['st_shndx'], symbol['st_value'] - section['sh_addr']
        section_name = section.name
    relocations = []
    for entry in proof['relocations']:
        assert entry['type'] == 2 and entry.get('explicitAddend') in [None, 0]
        assert int.from_bytes(bytes.fromhex(entry['originalEncodedWord']), 'little') == 0
        binding = proof['bindings'][entry['symbol']]
        assert binding['kind'] == 'function' and binding['mode'] == 'arm' and binding['module'] == 'ov005'
        relocations.append(dict(offset=entry['offset'], type=2, symbol=entry['symbol'],
                                target=binding['address'], addend=0))
    assert len(relocations) == 3 and proof['linkedDataSha256'] == report['nativeSpanSha256']
    row = dict(name=producer.NAME, symbol=producer.NAME, module='ov005', processor='arm9', program='',
               address=hex(producer.ADDRESS), bytes=24, size=24, compiledBytes=24, kind='rodata',
               source=proof['source'], sourceSha256=proof['sourceSha256'],
               object=frozen.relative_to(ROOT).as_posix(), objectSha256=sha256(frozen),
               compilerSha256=proof['compilerSha256'], compilerFlags=proof['compilerFlags'],
               sectionIndex=section_index, sectionOffset=section_offset, section=section_name,
               targetSha256=report['nativeSpanSha256'], outputSha256=proof['linkedDataSha256'],
               exactAfterDeclaredRelocation=proof['linkedDataSha256'] == report['nativeSpanSha256'],
               exactAfterGenuineDataLink=True, nativeAlias='data_ov005_021e6ea4',
               relocations=relocations, nativeSymbolEntries=proof['bindings'],
               nativeInteriorSymbols={}, nonExecutable=True)
    write_json(ROOT / OUTPUT, dict(schemaVersion=1, romSha256=report['romSha256'],
        sourceReport=RAW, sourceReportSha256=sha256(ROOT / RAW), source=proof['source'],
        sourceSha256=proof['sourceSha256'], dataMatches=[row], matches=[], functionMatches=[],
        dataAliases={'data_ov005_021e6ea4': hex(producer.ADDRESS)},
        nativeSymbols={entry['symbol']: entry['target'] for entry in relocations},
        initializedDataBytes=24, authoredExecutableCodeBytes=0, functionMatched=0, moduleLinked=False,
        producerProof=proof, rawNegative=report['negative'],
        generator='adapt_ov005_callbacks296_data_20261031.py', generatorSha256=sha256(__file__),
        limitations=['Raw worker report remains unchanged; this adapter exposes fresh genuine source-data proof to existing builders',
            'Opaque function references are storage views, not original callback prototypes or reconstructed callee code',
            'No source credit is published until source registration and module/ROM comparison pass']))
    print(dict(initializedDataBytes=24, functionMatched=0, authoredExecutableCodeBytes=0))


if __name__ == '__main__':
    main()
