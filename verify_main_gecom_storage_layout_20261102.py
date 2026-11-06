import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT, read_json, write_json, sha256


def main():
    report = 'evidence/attempts/main-gecom-declaration-closure-v2-20261102.json'
    rows = []
    for item in read_json(ROOT / report)['results']:
        path = ROOT / item['object']
        assert sha256(path) == item['objectSha256']
        with path.open('rb') as stream:
            elf = ELFFile(stream)
            objects = {s.name: (s['st_value'], s['st_size'])
                for s in elf.get_section_by_name('.symtab').iter_symbols()
                if isinstance(s['st_shndx'], int) and elf.get_section(s['st_shndx']).name == '.bss'
                and s['st_info']['type'] == 'STT_OBJECT'}
        assert objects['NNS_G3dGeBuffer'] == (0, 4)
        if item['identity']['address'] != '0x202e2e0':
            assert objects['NNS_G3dFlagGXDmaAsync'] == (4, 4)
        rows.append(dict(identity=item['identity'], originalCompilerObjectSha256=sha256(path),
            objectOffsetsAndWidths={key: list(value) for key, value in objects.items()},
            rawPreprocessedDeclarationSha256=item['originalExpandedSourceSha256']))
    write_json(ROOT / 'evidence/abi/main-gecom352-original-storage-layout-20261102.json',
        dict(passed=True, sourceCredit=0, originalCompilationReport=report,
            originalCompilationReportSha256=sha256(ROOT / report), rows=rows,
            typedSectionView=dict(bufferPointerOffset=0, pointerBytes=4, volatileIntOffset=4, intBytes=4),
            storageReconstructionCredit=0, nativeBehavioralReturns=0))
    print(dict(verifiedSourceObjects=len(rows), bufferOffset=0, volatileFlagOffset=4, sourceCredit=0))


if __name__ == '__main__':
    main()
