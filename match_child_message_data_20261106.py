import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from child_message_data_codec_20261106 import c_source


LAYOUT = 'src/utility/parallel_wave20261105/child-message-data/layout.json'
WORK = ROOT / 'work/child-message-data-native'
REPORT = ROOT / 'evidence/data/child-message-semantic-20261106.json'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
FLAGS = ['-O2', '-proc', 'arm946e', '-sym', 'on', '-nolink', '-lang', 'c99']


def generate(layout, bmg):
    assert (layout['program'], layout['processor'], layout['module'], layout['base']) == (
        'dwc/utility.bin/move/child.srl', 'arm9', 'utility-child-arm9-main', '0x2000000')
    values = []
    for asset in layout['assets']:
        pin = ROOT / asset['semanticSource']
        assert sha256(pin) == asset['semanticSourceSha256']
        address = int(asset['address'], 0)
        symbol = f'native_child_message_data_{address:08x}'
        text, payload, encoded, alignment = c_source(read_json(pin), symbol, bmg)
        assert len(payload) == asset['bytes'] and encoded == asset['encodedAssetBytes']
        assert alignment == asset['measuredZeroAlignmentBytes']
        assert hashlib.sha256(payload).hexdigest() == asset['targetSha256']
        values.append((asset, symbol, text, payload))
    assert len(values) == 8 and sum(len(row[3]) for row in values) == 3808
    return values


def compile_unit(source, directory, compiler, flags, env):
    directory.mkdir(parents=True, exist_ok=True)
    obj = directory / 'compiled.o'
    command = [str(compiler), *flags, '-c', str(source), '-o', str(obj)]
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    stable = WORK / 'objects' / (sha256(obj) + '.o')
    stable.parent.mkdir(parents=True, exist_ok=True)
    if not stable.exists():
        shutil.copyfile(obj, stable)
    assert sha256(stable) == sha256(obj)
    return stable, command


def inspect_object(obj, symbol, expected):
    from elftools.elf.elffile import ELFFile
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        entry = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == symbol)
        section = elf.get_section(entry['st_shndx'])
        assert entry['st_info']['type'] == 'STT_OBJECT' and entry['st_size'] == len(expected)
        assert section['sh_type'] == 'SHT_PROGBITS' and section['sh_flags'] == 2
        assert section.data()[entry['st_value']:entry['st_value'] + len(expected)] == expected
        assert not any(s['sh_flags'] & 4 and s['sh_size'] for s in elf.iter_sections())
        debug_relocations = 0
        for reloc in elf.iter_sections():
            if reloc['sh_type'] not in ('SHT_REL', 'SHT_RELA'):
                continue
            target = elf.get_section(reloc['sh_info'])
            if target['sh_flags'] & 2:
                assert reloc.num_relocations() == 0
            else:
                assert target.name.startswith('.debug')
                debug_relocations += reloc.num_relocations()
        return section.name, entry['st_shndx'], entry['st_value'], debug_relocations


def link_unit(obj, symbol, section, address, expected, directory, linker, env):
    from elftools.elf.elffile import ELFFile
    lcf = directory / 'data.lcf'
    lcf.write_text('MEMORY { DATA: ORIGIN = ' + hex(address) + ' > data.bin }\nSECTIONS {\n' +
        section + ': { ' + obj.name + '(' + section + ') } > DATA\n}\n', encoding='utf-8')
    local = directory / obj.name
    shutil.copyfile(obj, local)
    before = sha256(obj)
    linked = directory / 'linked.elf'
    command = [str(linker), '-nostdlib', '-nodeadstrip', '-proc', 'arm946e', '-main', symbol,
               str(lcf), str(local), '-o', str(linked)]
    result = subprocess.run(command, cwd=directory, env=env, capture_output=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert sha256(obj) == before and sha256(local) == before
    output = directory / 'data.bin'
    assert output.read_bytes() == expected
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        entry = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == symbol)
        assert entry['st_info']['type'] == 'STT_OBJECT'
        assert entry['st_value'] == address and entry['st_size'] == len(expected)
    return dict(exactDataBytes=True, objectUnmodified=True, linkedElf=linked.relative_to(ROOT).as_posix(),
                linkedElfSha256=sha256(linked), linkedDataSha256=sha256(output), command=command)


def main():
    config = configuration()
    native_dependencies(config)
    import ndspy.bmg as bmg
    import utility_runtime
    layout = read_json(ROOT / LAYOUT)
    flags = FLAGS
    assert sha256(COMPILER) == COMPILER_HASH
    assert sha256(LINKER) == LINKER_HASH
    original_open = Path.open
    def source_only_open(path, *args, **kwargs):
        resolved = path.resolve()
        assert not any(resolved.is_relative_to(ROOT / name) for name in ['inputs', 'extract'])
        return original_open(path, *args, **kwargs)
    with patch.object(Path, 'open', source_only_open):
        values = generate(layout, bmg)
        for denied in [config['rom'], ROOT / layout['binary']]:
            try:
                denied.read_bytes()
            except AssertionError:
                pass
            else:
                raise AssertionError('Original comparison input was readable during source generation')
    runtime, unused = utility_runtime.derive()
    module = next(row for row in runtime['modules'] if row['id'] == layout['module'])
    assert module['sha256'] == layout['inputModuleSha256'] and module['binary'] == layout['binary']
    native_path = ROOT / layout['binary']
    assert sha256(native_path) == layout['inputModuleSha256']
    native = native_path.read_bytes()
    env = dict(os.environ, LM_LICENSE_FILE=str(config['license']))
    matches, controls = [], []
    for asset, symbol, text, expected in values:
        address = int(asset['address'], 0)
        assert native[address - 0x02000000:address - 0x02000000 + len(expected)] == expected
        directory = WORK / f'{address:08x}'
        directory.mkdir(parents=True, exist_ok=True)
        source = ROOT / f'generated/child-message-data/{address:08x}.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            assert source.read_text() == text
        else:
            source.write_text(text, encoding='utf-8')
        obj, command = compile_unit(source, directory, COMPILER, flags, env)
        section, section_index, section_offset, debug = inspect_object(obj, symbol, expected)
        real_link = link_unit(obj, symbol, section, address, expected, directory, LINKER, env)
        bad_source = directory / 'wrong-data.c'
        value = expected[0] ^ 1
        bad_source.write_text(text.replace('0x10', f'0x{value:02x}', 1), encoding='utf-8')
        bad_obj, unused_command = compile_unit(bad_source, directory / 'wrong', COMPILER, flags, env)
        try:
            inspect_object(bad_obj, symbol, expected)
        except AssertionError:
            rejected = True
        else:
            rejected = False
        assert rejected
        controls.append(dict(address=hex(address), sameSizeWrongDataObjectRejected=True, wrongObjectSha256=sha256(bad_obj)))
        matches.append(dict(program=layout['program'], processor='arm9', module=layout['module'], mode='data',
            name=symbol, symbol=symbol, kind='data', address=hex(address), bytes=len(expected), size=len(expected),
            compiledBytes=len(expected), initializedBytes=len(expected), allocatedZeroFillBytes=0,
            encodedAssetBytes=asset['encodedAssetBytes'], measuredZeroAlignmentBytes=asset['measuredZeroAlignmentBytes'],
            source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            sourceDependencies=[dict(path=name, sha256=sha256(ROOT / name)) for name in [LAYOUT, asset['semanticSource']]],
            object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj),
            compiler=COMPILER.relative_to(ROOT).as_posix(), compilerSha256=sha256(COMPILER),
            compilerFlags=flags, sourceLanguage='C', section=section, sectionType='SHT_PROGBITS', sectionFlags=2,
            sectionIndex=section_index, sectionOffset=section_offset, relocations=[], nonAllocatedDebugRelocations=debug,
            targetSha256=hashlib.sha256(expected).hexdigest(), outputSha256=hashlib.sha256(expected).hexdigest(),
            inputModuleSha256=layout['inputModuleSha256'], exactAfterDeclaredRelocation=True, realLink=real_link,
            executableSectionBytes=0, ordinaryFunctionCredit=0, sourceOnlyGeneration=True, command=command))
    report = dict(schemaVersion=1, romSha256=config['romSha256'], program=layout['program'], processor='arm9',
        module=layout['module'], runtimeMappingCanonical=True, dataMatches=matches, nativeSymbols={},
        dataMatchedBytes=3808, encodedAssetBytes=3799, measuredZeroAlignmentBytes=9, functionMatched=0,
        functionMatches=[], sourceCreditPendingSharedAcceptance=True, dataSourceCohortAdmissionImplemented=False,
        generationOriginalInputsBlocked=True, originalReadRejectionControls=2, originalRomUsedOnlyForComparison=True, controls=controls,
        generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in
                          ['match_child_message_data_20261106.py', 'child_message_data_codec_20261106.py']],
        wholeModuleLinked=False, sourceReconstructionComplete=False, sourceOnlyRomProven=False)
    write_json(REPORT, report)
    print(dict(dataObjects=8, initializedDataBytes=3808, encodedAssetBytes=3799, alignmentBytes=9,
               sourceCredit=0, wrongDataObjectsRejected=len(controls), originalInputsBlockedDuringGeneration=True))


if __name__ == '__main__':
    main()
