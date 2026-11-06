import copy
import hashlib
import struct
import uuid
from project import ROOT, read_json, write_json, sha256
import embedded_reference_link_context_v2_20261106 as context
from qualify_arm9_thumb_reference_inputs_20261105 import derive
import qualify_arm9_thumb_reference_inputs_20261105 as original


def main():
    manifest_name = 'evidence/verification/embedded-reference-link-context-v2-control-inputs-20261106.json'
    manifest = read_json(ROOT / manifest_name)
    rows = []
    for pin in manifest['reports']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
        selected = [r for r in read_json(ROOT / pin['path'])['matches'] if r['address'] in pin['addresses']]
        assert {r['address'] for r in selected} == set(pin['addresses'])
        assert all('legacyExternalOutputLink' in r['realLink'] for r in selected)
        rows.extend(selected)
    assert len(rows) == manifest['expectedFunctions'] == 10
    assert len({r['address'] for r in rows}) == 10 and sum(r['bytes'] for r in rows) == manifest['expectedBytes'] == 3102
    data = derive()
    work = ROOT / 'work/integration/cohort172-embedded-reference-generic-controls' / uuid.uuid4().hex[:12]
    work.mkdir(parents=True)
    positives, rejected = [], []
    for row in rows:
        address = int(row['address'], 0)
        native = data[address - 0x02000000:address - 0x02000000 + row['bytes']]
        with context.validation_route():
            proof = original.linked_output(row, work / row['address'] / 'positive-flat-relink', native)
        positives.append(dict(address=row['address'], bytes=row['bytes'], proof=proof))
        cases = []
        for label, key, value in [('wrong-program', 'program', 'child.srl'), ('wrong-cpu', 'processor', 'arm7'),
                ('wrong-module', 'module', 'ov006'), ('wrong-mode', 'mode', 'arm' if row['mode'] == 'thumb' else 'thumb'),
                ('wrong-size', 'bytes', row['bytes'] + 4), ('wrong-source', 'source', 'src/unqualified.c'),
                ('wrong-source-hash', 'sourceSha256', '0' * 64), ('wrong-native-hash', 'targetSha256', '0' * 64)]:
            changed = copy.deepcopy(row); changed[key] = value
            cases.append((label, changed, native))
        for key in ['sourceObjectSha256', 'splitObjectSha256', 'linkedCallerSha256', 'nativeSpanSha256', 'linkerSha256']:
            changed = copy.deepcopy(row)
            changed['realLink']['legacyExternalOutputLink'][key] = '0' * 64
            cases.append(('mismatched-flat-' + key, changed, native))
        cases.append(('wrong-native-payload', copy.deepcopy(row), bytes([native[0] ^ 1]) + native[1:]))
        source = ROOT / row['realLink']['linkedElf']
        from elftools.elf.elffile import ELFFile
        with source.open('rb') as stream:
            elf = ELFFile(stream)
            entry = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == row['name'])
            section = elf.get_section(entry['st_shndx'])
            section_header = elf['e_shoff'] + entry['st_shndx'] * elf['e_shentsize']
            segment_index = next(i for i, s in enumerate(elf.iter_segments()) if s['p_type'] == 'PT_LOAD' and s['p_filesz']
                and s['p_vaddr'] <= address and address + row['bytes'] <= s['p_vaddr'] + s['p_filesz'])
            segment_header = elf['e_phoff'] + segment_index * elf['e_phentsize']
            positions = [('actual-stored-code-change', section['sh_offset'], None),
                ('source-section-not-file-backed', section_header + 4, 8),
                ('load-segment-no-file-payload', segment_header + 16, 0)]
        for label, at, value in positions:
            payload = bytearray(source.read_bytes())
            if value is None:
                payload[at] ^= 1
            else:
                struct.pack_into('<I', payload, at, value)
            target = work / row['address'] / (label + '.elf')
            target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(payload)
            changed = copy.deepcopy(row)
            changed['realLink'].update(linkedElf=target.relative_to(ROOT).as_posix(), linkedElfSha256=sha256(target))
            cases.append((label, changed, native))
        for label, changed, body in cases:
            try:
                context.inspect(changed, body)
            except (AssertionError, ValueError, KeyError, OSError) as error:
                rejected.append(dict(address=row['address'], case=label, rejected=True, reason=type(error).__name__))
            else:
                raise ValueError('Bad embedded storage/reference contract admitted: ' + label)
    assert len(rejected) == 170
    output = ROOT / 'evidence/verification/cohort172-embedded-reference-link-route-v2-20261106.json'
    write_json(output, dict(passed=True, sourceCredit=0, originalQualifierAndFlatGenuineRelinkerUnchanged=True,
        supportedFunctions=len(rows), supportedBytes=sum(r['bytes'] for r in rows), positives=positives,
        negativeControls=rejected, missingOutputNeverFilledFromNativeOrOriginalScaffolding=True,
        onlyActualSourceGeneratedEmbeddedSectionsRead=True,
        helper=dict(path='embedded_reference_link_context_v2_20261106.py', sha256=sha256(ROOT / 'embedded_reference_link_context_v2_20261106.py')),
        generatorSha256=sha256(__file__), controlManifest=dict(path=manifest_name, sha256=sha256(ROOT / manifest_name)),
        productionSourcesObjectsFlagsAndReadyPacketsChanged=False))
    print(dict(passed=True, functions=len(rows), bytes=sum(r['bytes'] for r in rows), negativeControls=len(rejected)))


if __name__ == '__main__':
    main()
