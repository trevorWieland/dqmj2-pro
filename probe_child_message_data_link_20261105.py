import os
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from inspect_child_message_assets_20261105 import from_source, encode_with_recipe


def main():
    native_dependencies(configuration())
    import ndspy.bmg as bmg
    from elftools.elf.elffile import ELFFile
    import match_runtime as compiler
    from link_runtime_unit import LINKER, LINKER_HASH
    proof_name = 'evidence/lanes/parallel-wave20261105/source95-data-inspection/semantic-roundtrip.json'
    protection_name = 'evidence/lanes/parallel-wave20261105/source95-data-inspection/range-protection-audit.json'
    semantic = read_json(ROOT / proof_name)
    protection = read_json(ROOT / protection_name)
    assert semantic['passed'] and protection['passed'] and not protection['overlaps']
    assert sha256(compiler.COMPILER) == compiler.COMPILER_PINS[compiler.COMPILER.relative_to(ROOT).as_posix()]
    assert sha256(LINKER) == LINKER_HASH
    protected = ['recovery.json', 'source-preferences.json', proof_name, protection_name]
    before = {name: sha256(ROOT / name) for name in protected}
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    flags = list(compiler.FLAGS)
    rows = []
    for asset in semantic['assets']:
        pin = ROOT / asset['sourcePath']
        assert sha256(pin) == asset['sourceSha256']
        source = read_json(pin)
        encoded = encode_with_recipe(from_source(source['source'], bmg), source['compressionRecipe'])
        import hashlib
        assert hashlib.sha256(encoded).hexdigest() == asset['originalEncodedSha256']
        address = int(asset['address'], 0)
        name = f'native_child_message_{address:08x}'
        directory = ROOT / 'work/source95-child-message-data' / f'{address:08x}'
        directory.mkdir(exist_ok=True, parents=True)
        unit = directory / 'message.c'
        lines = ['const unsigned char ' + name + '[] = {']
        for offset in range(0, len(encoded), 16):
            lines.append('    ' + ', '.join(f'0x{value:02x}' for value in encoded[offset:offset + 16]) + ',')
        lines.append('};')
        unit.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        obj = directory / 'message.o'
        command = [str(compiler.COMPILER), *flags, '-c', str(unit), '-o', str(obj)]
        run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=60)
        assert run.returncode == 0, run.stdout + run.stderr
        with obj.open('rb') as stream:
            elf = ELFFile(stream)
            symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == name)
            assert symbol['st_info']['type'] == 'STT_OBJECT' and symbol['st_size'] == len(encoded)
            section = elf.get_section(symbol['st_shndx'])
            assert section['sh_type'] == 'SHT_PROGBITS' and not section['sh_flags'] & 4
            offset = symbol['st_value']
            assert section.data()[offset:offset + len(encoded)] == encoded
            assert not any(s['sh_flags'] & 4 and s['sh_size'] for s in elf.iter_sections())
            debug_relocations = 0
            for relocation in elf.iter_sections():
                if relocation['sh_type'] not in ('SHT_REL', 'SHT_RELA'):
                    continue
                target = elf.get_section(relocation['sh_info'])
                if target['sh_flags'] & 2:
                    assert relocation.num_relocations() == 0
                else:
                    assert target.name.startswith('.debug')
                    debug_relocations += relocation.num_relocations()
            section_name = section.name
        object_hash = sha256(obj)
        lcf = directory / 'message.lcf'
        lcf.write_text('MEMORY {\nDATA: ORIGIN = ' + hex(address) + ' > message.bin\n}\nSECTIONS {\n'
            + section_name + ': { message.o(' + section_name + ') } > DATA\n}\n', encoding='utf-8')
        linked = directory / 'message.elf'
        link = [str(LINKER), '-nostdlib', '-nodeadstrip', '-main', name, str(lcf), str(obj), '-o', str(linked)]
        run = subprocess.run(link, cwd=directory, env=env, capture_output=True, timeout=60)
        assert run.returncode == 0, run.stdout + run.stderr
        assert sha256(obj) == object_hash
        with linked.open('rb') as stream:
            elf = ELFFile(stream)
            symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == name)
            assert symbol['st_info']['type'] == 'STT_OBJECT'
            assert symbol['st_value'] == address and symbol['st_size'] == len(encoded)
        payload = (directory / 'message.bin').read_bytes()
        assert payload[:len(encoded)] == encoded
        padding = payload[len(encoded):]
        assert len(padding) < 4 and not any(padding)
        rows.append(dict(address=hex(address), bytes=len(encoded), dataSymbol=name,
            semanticSource=asset['sourcePath'], semanticSourceSha256=sha256(pin),
            generatedC=unit.relative_to(ROOT).as_posix(), generatedCSha256=sha256(unit),
            object=obj.relative_to(ROOT).as_posix(), objectSha256=object_hash,
            linkedElf=linked.relative_to(ROOT).as_posix(), linkedElfSha256=sha256(linked),
            lcf=lcf.relative_to(ROOT).as_posix(), lcfSha256=sha256(lcf), compilerFlags=flags,
            actualObjectType='STT_OBJECT', initializedDataExact=True, completeNativeAddressAndSizeExact=True,
            executableSectionBytes=0, initializedDataRelocations=0, nonAllocatedDebugRelocations=debug_relocations,
            objectOrInstructionPatches=0,
            unclaimedOutputAlignmentBytes=len(padding), ordinaryFunctionCredit=0))
    assert before == {name: sha256(ROOT / name) for name in before}
    write_json(ROOT / 'evidence/lanes/parallel-wave20261105/source95-data-inspection/compiled-data-probe.json',
        dict(passed=True, sourceCredit=0, dataSourceCredit=0, inspectionOnly=True,
            initializedAssetBytes=sum(row['bytes'] for row in rows), assets=rows,
            compilerSha256=sha256(compiler.COMPILER), linkerSha256=sha256(LINKER),
            generatorSha256=sha256(__file__), unchangedProductionInputs=before,
            generationConsumesOriginalRomOrExtractedBytes=False,
            limitations=['Unaccepted private data-source probe; no registry, module composition or source coverage changed.',
                'Source metadata supplies semantic BMG messages and original data compression choices, without original compressed literals.',
                'Whole unmodified C objects pass the real pinned compiler and linker; object/executable patching is absent.',
                'Alignment bytes outside each measured encoded asset are unclaimed.',
                'An admitted data packet, source-data cohort accounting, fresh copied-root replay and all original gates remain required.']))
    print(dict(passed=True, assets=len(rows), initializedDataBytes=sum(row['bytes'] for row in rows), sourceCredit=0))


if __name__ == '__main__':
    main()
