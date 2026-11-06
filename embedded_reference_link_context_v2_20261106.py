import contextlib
import copy
import hashlib
import re
from functools import lru_cache
from pathlib import Path
from unittest.mock import patch
from project import ROOT, sha256
import qualify_arm9_thumb_reference_inputs_20261105 as original

@lru_cache(maxsize=1)
def native_context():
    image = original.derive()
    symbols = {}
    for line in (ROOT / 'config/arm9/symbols.txt').read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'func_([0-9a-fA-F]{8}) kind:function\((arm|thumb),size=(0x[0-9a-fA-F]+)\) addr:(0x[0-9a-fA-F]+)', line)
        if match:
            address = int(match[4], 0)
            assert int(match[1], 16) == address and address not in symbols
            symbols[address] = (int(match[3], 0), match[2])
    assert symbols
    return image, symbols


def inspect(row, native):
    from elftools.elf.elffile import ELFFile
    address = int(row['address'], 0)
    image, symbols = native_context()
    assert address in symbols
    size, mode = symbols[address]
    assert (row.get('program') or '', row['processor'], row['module'], row['mode']) == ('', 'arm9', 'main', mode)
    assert row['bytes'] == size and size > 0
    assert not any(address < other < address + size for other in symbols)
    source = (ROOT / row['source']).resolve()
    assert source.is_relative_to(ROOT / 'src') and source.suffix == '.c' and source.is_file()
    assert native == image[address - 0x02000000:address - 0x02000000 + size]
    assert sha256(ROOT / row['source']) == row['sourceSha256']
    assert len(native) == size and hashlib.sha256(native).hexdigest() == row['targetSha256']
    link = row['realLink']; flat = link['legacyExternalOutputLink']
    assert link['normalEmbeddedLinkMatchesIndependentFlatOutput'] is True
    assert link['callerBinExtractedFromActualEmbeddedSection'] is True
    for key in ['name', 'module', 'processor', 'address', 'bytes', 'sourceSha256', 'sourceObjectSha256',
            'splitObjectSha256', 'linkedCallerSha256', 'nativeSpanSha256', 'linkerSha256',
            'bindingOnlyProbes', 'originalRelocations']:
        assert link[key] == flat[key], ('Embedded/flat contract differs', key)
    assert link['sourceObjectSha256'] == row['objectSha256']
    assert link['linkedCallerSha256'] == link['nativeSpanSha256'] == row['targetSha256']
    assert link['exactCallerBytes'] is flat['exactCallerBytes'] is True
    def objects(proof):
        paths = [Path(value) for value in proof['linkerAttempt']['command'] if str(value).endswith('.o')]
        assert paths and all(p.resolve().is_relative_to(ROOT / 'work') for p in paths)
        return [(p.name, sha256(p)) for p in paths]
    assert objects(link) == objects(flat)
    assert objects(link)[0][1] == link['splitObjectSha256']
    path = (ROOT / link['linkedElf']).resolve()
    assert path.is_relative_to(ROOT / 'work') and sha256(path) == link['linkedElfSha256']
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        assert elf.elfclass == 32 and elf.little_endian and elf['e_machine'] == 'EM_ARM'
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        entries = [s for s in symbols if s.name == row['name']]
        assert len(entries) == 1
        entry = entries[0]
        assert entry['st_info']['type'] == 'STT_FUNC' and entry['st_value'] & ~1 == address and entry['st_size'] == size
        section = elf.get_section(entry['st_shndx'])
        assert section['sh_type'] == 'SHT_PROGBITS' and section['sh_addr'] == address and section['sh_size'] == size
        assert section.data() == native
        assert any(s.name == ('$t' if mode == 'thumb' else '$a') and s['st_value'] & ~1 == address for s in symbols)
        segments = [s for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD' and s['p_filesz']
            and s['p_vaddr'] <= address and address + size <= s['p_vaddr'] + s['p_filesz']]
        assert len(segments) == 1
        segment = segments[0]
        offset = address - segment['p_vaddr']
        assert segment.data()[offset:offset + size] == native
        assert segment['p_offset'] + offset == section['sh_offset']
    return dict(passed=True, sourceCredit=0, actualFileBackedSectionAndLoadBytesEqual=True,
        originalCompilerModeRequiredSeparately=True, originalFlatRecipePreserved=True,
        copiedObjectHashesIdentical=True, embeddedElfSha256=sha256(path), vendorExecutableFlagsNotReinterpreted=True)


@contextlib.contextmanager
def validation_route():
    previous = original.linked_output
    def linked_output(row, directory, native):
        if 'legacyExternalOutputLink' not in row['realLink']:
            return previous(row, directory, native)
        proof = inspect(row, native)
        adapted = copy.deepcopy(row)
        adapted['realLink'] = copy.deepcopy(row['realLink']['legacyExternalOutputLink'])
        result = previous(adapted, directory, native)
        result['independentEmbeddedStorageQualification'] = proof
        return result
    with patch.object(original, 'linked_output', linked_output):
        yield
