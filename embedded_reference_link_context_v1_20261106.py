import contextlib
import copy
import hashlib
from pathlib import Path
from unittest.mock import patch
from project import ROOT, sha256
import qualify_arm9_thumb_reference_inputs_20261105 as original

SCOPES = {
    0x020abf18: (204, 'thumb', 'gpi-buddy-resume-next/first/'),
    0x020abfe4: (242, 'thumb', 'gpi-buddy-resume-next/first/'),
    0x020ac0d8: (88, 'thumb', 'gpi-buddy-resume-next/first/'),
    0x020ac130: (724, 'thumb', 'gpi-buddy-resume-next/second/'),
    0x020d0ad8: (292, 'arm', 'main-grid-resume-next/first/'),
    0x020d0bfc: (124, 'arm', 'main-grid-controls-next/first/'),
    0x020d0844: (360, 'arm', 'main-grid-controls-next/first/')}


def inspect(row, native):
    from elftools.elf.elffile import ELFFile
    address = int(row['address'], 0)
    assert address in SCOPES
    size, mode, suffix = SCOPES[address]
    assert (row.get('program') or '', row['processor'], row['module'], row['mode']) == ('', 'arm9', 'main', mode)
    assert row['bytes'] == size and row['source'].startswith('src/runtime/parallel_wave20261106/' + suffix)
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
