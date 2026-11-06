import copy
import os
import re
import subprocess
import sys
import match_runtime
from elftools.elf.elffile import ELFFile
from elf_units import split_symbol
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, LINKER, LINKER_HASH
from main_case_compare_fixture_20261031 import execute, ENTRY, SIZE


NAME, ADDRESS = 'native_data_020d8d04', 0x020D8D04
SOURCE = 'src/runtime/20261031_ascii_lower_data/native_ascii_lower.c'
WORK = ROOT / 'work/main-ascii-lower-data-20261031'
FLAGS = ['-O3', '-opt', 'speed', '-proc', 'arm946e', '-sym', 'on', '-nolink']


def source_text(values):
    lines = [f'const unsigned char {NAME}[128] = {{']
    lines += ['    ' + ', '.join(str(value) for value in values[i:i + 8]) + (',' if i < 120 else '') for i in range(0, 128, 8)]
    return '\n'.join([*lines, '};', ''])


def build(source, directory):
    directory.mkdir(parents=True, exist_ok=True)
    assert sha256(match_runtime.COMPILER) == match_runtime.COMPILER_PINS[match_runtime.COMPILER.relative_to(ROOT).as_posix()]
    assert sha256(LINKER) == LINKER_HASH
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    obj = directory / 'data.o'
    command = [str(match_runtime.COMPILER), *FLAGS, '-c', str(source), '-o', str(obj)]
    subprocess.run(command, cwd=ROOT, env=env, check=True, capture_output=True, timeout=30)
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == NAME)
        section = elf.get_section(symbol['st_shndx'])
        assert symbol['st_info']['type'] == 'STT_OBJECT' and symbol['st_size'] == 128 and symbol['st_value'] == 0
        assert section['sh_type'] == 'SHT_PROGBITS' and not section['sh_flags'] & 4 and section['sh_size'] == 128
        assert not any(row['sh_type'] in ['SHT_REL', 'SHT_RELA'] and row['sh_info'] == symbol['st_shndx'] and row.num_relocations() for row in elf.iter_sections())
        payload = section.data()
        section_name, section_index = section.name, symbol['st_shndx']
        split = directory / 'data-split.o'
        split_symbol(elf, NAME, split, target_section='.rodata')
    lcf = directory / 'data.lcf'
    lcf.write_text('MEMORY {\nDATA: ORIGIN = 0x020d8d04 > data.bin\n}\nSECTIONS {\n.rodata: { data-split.o(.rodata) } > DATA\n}\n')
    linked = directory / 'data.elf'
    link_command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-main', NAME, str(lcf), str(split), '-o', str(linked)]
    subprocess.run(link_command, cwd=directory, env=env, check=True, capture_output=True, timeout=30)
    actual = (directory / 'data.bin').read_bytes()
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == NAME)
        assert symbol['st_info']['type'] == 'STT_OBJECT' and symbol['st_value'] == ADDRESS and symbol['st_size'] == 128
    assert actual == payload
    return payload, dict(name=NAME, symbol=NAME, nativeAlias='data_020d8d04', processor='arm9', module='main',
        mode='data', kind='data', sourceLanguage='C', address=hex(ADDRESS), bytes=128, size=128,
        initializedBytes=128, compiledBytes=128, sourceSymbolType='STT_OBJECT', section=section_name,
        targetSection='.rodata', sectionIndex=section_index, sectionOffset=0, sectionPaddingBytes=0,
        source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), object=obj.relative_to(ROOT).as_posix(),
        objectSha256=sha256(obj), compiler=match_runtime.COMPILER.relative_to(ROOT).as_posix(),
        compilerSha256=sha256(match_runtime.COMPILER), compilerFlags=FLAGS, compileCommand=command,
        splitObject=split.relative_to(ROOT).as_posix(), splitObjectSha256=sha256(split), relocations=[],
        linkedElf=linked.relative_to(ROOT).as_posix(), linkedElfSha256=sha256(linked),
        linkedDataBinary=(directory / 'data.bin').relative_to(ROOT).as_posix(), linkedDataBinarySha256=sha256(directory / 'data.bin'),
        lcf=lcf.relative_to(ROOT).as_posix(), lcfSha256=sha256(lcf), linkerSha256=LINKER_HASH, linkCommand=link_command)


def main():
    assert sys.version_info[:3] == (3, 13, 5)
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, original, symbols = measured_module('main')
    assert 'data_020d8d04 kind:data(any) addr:0x020d8d04' in symbols.splitlines()
    assert 'data_020d8d84 kind:data(any) addr:0x020d8d84' in symbols.splitlines()
    delinks = (ROOT / 'config/arm9/delinks.txt').read_text()
    assert any(int(a, 0) <= ADDRESS and ADDRESS + 128 <= int(b, 0) for a, b in re.findall(r'^\s*\.rodata\s+start:(0x[0-9a-f]+)\s+end:(0x[0-9a-f]+)', delinks, re.M))
    assert not any(int(a, 0) < ADDRESS + 128 and ADDRESS < int(a, 0) + int(n, 0) for n, a in re.findall(r'^\S+ kind:function\((?:arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$', symbols, re.M))
    values = [value + 32 if 65 <= value <= 90 else value for value in range(128)]
    source = ROOT / SOURCE
    assert source.read_text() == source_text(values)
    payload, row = build(source, WORK / 'positive')
    offset = ADDRESS - int(metadata['base'], 0)
    assert payload == bytes(values) == original[offset:offset + 128]
    row.update(targetSha256=sha256(WORK / 'positive/data.bin'), outputSha256=sha256(WORK / 'positive/data.bin'),
        inputModuleSha256=metadata['sha256'], exactBytes=True, exactAfterDeclaredRelocation=True,
        exactAfterRealMwLink=True, ordinaryFunctionCredit=0, executableByteCredit=0)
    code = original[ENTRY - 0x02000000:ENTRY - 0x02000000 + SIZE]
    replaced = bytearray(original)
    replaced[offset:offset + 128] = payload
    cases = []
    for index in range(1792):
        first, second = execute(original, code, index), execute(bytes(replaced), code, index)
        assert first == second and first['modelPassed']
        cases.append(dict(index=index, result=first, actualReturns=2))
    wrong_values = values[:]
    wrong_values[68] = 68
    negative = ROOT / 'nonmatching/main-runtime/20261031-ascii-lower-data-control/source.c'
    negative.parent.mkdir(parents=True, exist_ok=True)
    negative.write_text(source_text(wrong_values), encoding='utf-8')
    wrong, wrong_row = build(negative, WORK / 'negative')
    mutated = bytearray(original)
    mutated[offset:offset + 128] = wrong
    controls = []
    for index in [68, 324, 580, 0, 65, 97, 128, 255]:
        first, second = execute(original, code, index), execute(bytes(mutated), code, index)
        assert first['modelPassed']
        controls.append(dict(index=index, original=first, wrong=second, actualReturns=2))
    assert any(not item['wrong']['modelPassed'] for item in controls)
    assert any(item['wrong']['modelPassed'] for item in controls)
    write_json(ROOT / 'evidence/matches/main-ascii-lower-data-20261031.json', dict(
        romSha256=config['romSha256'], module='main', processor='arm9', dataMatches=[row],
        nativeSymbols={}, dataAliases={'data_020d8d04': hex(ADDRESS)}, initializedDataBytes=128,
        ordinaryFunctionCredit=0, executableByteCredit=0, generatedFromIndependentMathematics=True,
        cases=cases, negativeControls=controls, wrongData=wrong_row,
        limitations=['Only the128-byte bounded reader view; no enclosing original object-name/size claim',
            'Actual original comparator consumers,0providers; C consumer source is qualified separately',
            'No generalized encoding, locale or Unicode claim; following data remains separate']))
    print(dict(initializedDataBytes=128, ordinaryFunctionCredit=0, actualConsumerReturns=3584, negativeReturns=16))


if __name__ == '__main__':
    main()
