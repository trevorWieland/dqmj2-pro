import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import match_runtime
from elftools.elf.elffile import ELFFile
from elf_units import split_symbol
from project import write_json
from derive_arm7_crc_table32_20261031 import derive, source_text, NAME
from arm7_crc_table32_scope_20261031 import classify, FIRST, LAST, MODULE_SHA

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030/lane-crc-table32-final'
SOURCE = 'src/utility/lane_20261031_crc_table32/native_crc_table32.c'
COMPILER = 'tools/mwccarm/mwccarm/1.2/sp2p3/mwccarm.exe'
COMPILER_SHA = 'a0db9f5dd49ceb619dbc64993660b39f96cca10821a698a9859824e2d4ae2a81'
LINKER = 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_SHA = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
FLAGS = ['-O2', '-opt', 'space', '-proc', 'arm7tdmi', '-lang', 'c99', '-sym', 'on', '-nolink']
REPORT = ROOT / 'evidence/data/arm7-child-crc-table32-20261031.json'
ROM_SHA = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
PIN_FILE = ROOT / 'nonmatching/arm7-bulk/20261031/lane-child-crc-table32-final/generator-pins.json'
PIN_SHA = 'ba09be4fe1675303833ccce331c56d41e552eec9327d1bbb51298bc4df0d0f76'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    if digest(PIN_FILE.read_bytes()) != PIN_SHA or digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM_SHA:
        raise ValueError('Pinned mathematical data input/runtime closure differs')
    pins = json.loads(PIN_FILE.read_text())['files']
    for row in pins:
        if digest((ROOT / row['path']).read_bytes()) != row['sha256']:
            raise ValueError('Mathematical data dependency changed: ' + row['path'])
    return pins


def build_data(source, directory):
    directory.mkdir(parents=True, exist_ok=True)
    if digest((ROOT / COMPILER).read_bytes()) != COMPILER_SHA or digest((ROOT / LINKER).read_bytes()) != LINKER_SHA:
        raise ValueError('Pinned data compiler/linker differs')
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    obj = directory / 'table.o'
    command = [str(ROOT / COMPILER), *FLAGS, '-c', str(source), '-o', str(obj)]
    call = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
    if call.returncode:
        raise ValueError({'command': command, 'exitCode': call.returncode, 'stdout': call.stdout, 'stderr': call.stderr})
    split = directory / 'table-split.o'
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == NAME)
        section = elf.get_section(symbol['st_shndx'])
        if symbol['st_info']['type'] != 'STT_OBJECT' or symbol['st_size'] != 32 or section['sh_type'] != 'SHT_PROGBITS' or section['sh_flags'] & 4:
            raise ValueError('Data must be a complete non-executable32-byte C object')
        if any(row['sh_type'] in ('SHT_RELA', 'SHT_REL') and row['sh_info'] == symbol['st_shndx'] and row.num_relocations() for row in elf.iter_sections()):
            raise ValueError('Mathematical table acquired relocations')
        compiled = section.data()[symbol['st_value']:symbol['st_value'] + 32]
        section_name, section_index, section_offset = section.name, symbol['st_shndx'], symbol['st_value']
        padding = section['sh_size'] - 32
        if padding or section_offset:
            raise ValueError('Complete source object acquired undeclared data/padding')
        split_symbol(elf, NAME, split, target_section='.data')
    lcf = directory / 'table.lcf'
    lcf.write_text('MEMORY {\nCRC_DATA: ORIGIN = 0x027f7f74 > table.bin\n}\nSECTIONS {\n.data: { table-split.o(.data) } > CRC_DATA\n}\n')
    linked = directory / 'table.elf'
    command_link = [str(ROOT / LINKER), '-nostdlib', '-nodeadstrip', '-main', NAME, str(lcf), str(split), '-o', str(linked)]
    call = subprocess.run(command_link, cwd=directory, env=env, capture_output=True, text=True, timeout=30)
    if call.returncode:
        raise ValueError({'command': command_link, 'exitCode': call.returncode, 'stdout': call.stdout, 'stderr': call.stderr})
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == NAME)
        if symbol['st_info']['type'] != 'STT_OBJECT' or symbol['st_value'] != FIRST or symbol['st_size'] != 32:
            raise ValueError('Genuine linked data symbol address/type/extent differs')
        regions = [row for row in elf.iter_sections() if row['sh_addr']]
        segments = [dict(row.header) for row in elf.iter_segments()]
        if len(regions) != 1 or regions[0].name != 'CRC_DATA' or regions[0]['sh_addr'] != FIRST or regions[0]['sh_size'] != 0 or regions[0]['sh_flags'] != 0x10000000:
            raise ValueError('Unexpected MWLD external-region ELF sidecar sections')
        if len(segments) != 1 or any(segments[0][key] != value for key, value in {'p_type': 'PT_LOAD', 'p_vaddr': FIRST, 'p_paddr': FIRST, 'p_filesz': 0, 'p_memsz': 32, 'p_flags': 0x80000000, 'p_align': 4}.items()):
            raise ValueError('Unexpected MWLD external raw-region/ELF allocation sidecar layout')
    payload_path = directory / 'table.bin'
    payload = payload_path.read_bytes()
    if len(payload) != 32 or payload != compiled:
        raise ValueError('Compiler/genuine-linker complete data payload differs')
    return payload, {'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': digest(source.read_bytes()),
        'object': obj.relative_to(ROOT).as_posix(), 'objectSha256': digest(obj.read_bytes()), 'compiler': COMPILER, 'compilerSha256': COMPILER_SHA,
        'compilerFlags': FLAGS, 'compileCommand': command, 'compileCwd': str(ROOT), 'section': section_name, 'targetSection': '.data',
        'sectionIndex': section_index, 'sectionOffset': section_offset, 'sectionPaddingBytes': padding, 'sourceSymbolType': 'STT_OBJECT',
        'splitObject': split.relative_to(ROOT).as_posix(), 'splitObjectSha256': digest(split.read_bytes()), 'linkedElf': linked.relative_to(ROOT).as_posix(),
        'linkedElfSha256': digest(linked.read_bytes()), 'linkedDataBinary': payload_path.relative_to(ROOT).as_posix(), 'linkedDataBinarySha256': digest(payload),
        'lcf': lcf.relative_to(ROOT).as_posix(), 'lcfSha256': digest(lcf.read_bytes()), 'linkerSha256': LINKER_SHA,
        'linkCommand': command_link, 'linkCwd': str(directory), 'relocations': [], 'originalDataCompilerInput': False, 'executableSourceCredit': 0,
        'mwldExternalRawRegionElfSidecar': {'programHeaders': segments, 'regionSection': 'CRC_DATA', 'sectionFlags': 0x10000000,
            'sectionPayloadBytes': 0, 'rawCompanionBytes': 32, 'runtimeExecutePermissionClaimed': False}}


def compile_data():
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned table generation/runtime differs')
    verify_inputs()
    scope = classify()
    values = derive()
    expected = b''.join(value.to_bytes(2, 'little') for value in values)
    source = ROOT / SOURCE
    if source.read_text() != source_text(values):
        raise ValueError('Source differs from independent polynomial generation')
    raw = (ROOT / scope['inputModule']).read_bytes()
    original = raw[FIRST - int(scope['moduleBase'], 0):LAST - int(scope['moduleBase'], 0)]
    if original != expected:
        raise ValueError('Polynomial generation differs from exact initialized native read span')
    consumer_source = ROOT / 'src/utility/lane_20261031_crc120/native_utility_child_arm7_main_027e93d4.c'
    if 'extern u16 ' + NAME + '[16];' not in consumer_source.read_text():
        raise ValueError('Consumer/table declaration closure is incompatible')
    payload, row = build_data(source, WORK)
    if payload != original:
        raise ValueError('Genuine compiled-source table bytes differ')
    return dict(row, name=NAME, symbol=NAME, nativeAlias=NAME, program=scope['program'], processor='arm7', module=scope['module'],
        kind='initialized-data', mode='data', address=hex(FIRST), size=32, bytes=32, initializedBytes=32, compiledBytes=32,
        targetSha256=digest(original), outputSha256=digest(payload), rawSha256=digest(payload), inputModuleSha256=MODULE_SHA,
        inputModule=scope['inputModule'], exactBytes=True, exactAfterDeclaredRelocation=True, exactAfterRealMwLink=True,
        ordinaryFunctionCredit=0, sourceLanguage='C', mathematicalDerivation={'polynomial': '0xa001', 'nibbleInputs': list(range(16)),
            'iterationsPerEntry': 4, 'values': values, 'originalDataBytesUsedToGenerateSource': 0}, classification=scope,
        compatibleConsumerDeclaration={'path': consumer_source.relative_to(ROOT).as_posix(), 'sha256': digest(consumer_source.read_bytes()),
            'type': 'extern u16 table[16]; mutable definition matches', 'originalTotalObjectExtentClaimed': False})


def main():
    pins = verify_inputs()
    row = compile_data()
    from arm7_crc_table32_native_20261031 import oracle
    payload = (ROOT / row['linkedDataBinary']).read_bytes()
    native = oracle(payload)
    names = sorted({Path(__file__).name, PIN_FILE.relative_to(ROOT).as_posix(), SOURCE} | {row['path'] for row in pins})
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'generatorSources': [{'path': name, 'sha256': digest((ROOT / name).read_bytes())} for name in names],
        'pinnedGeneratorAndRuntimeDependencies': pins,
        'romSha256': ROM_SHA, 'dataMatches': [row], 'dataAliases': {NAME: hex(FIRST)}, 'nativeSymbols': {}, 'initializedDataBytes': 32,
        'ordinaryCCodeBytes': 0, 'ordinaryFunctionCredit': 0, 'generatedFromIndependentMathematics': True,
        'sourceDataBytesFromNativeInput': 0, 'nativeOriginalConsumers': native, 'sourceCreditAcceptedByThisScript': 0,
        'wholeModuleLinked': False, 'configuredBoundariesOrSymbolsChanged': False,
        'limitations': ['Exact32-byte non-executable source-data view only; no full original object extent/name, consumer source or whole-game completion claim']}
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': digest(REPORT.read_bytes()), 'dataBytes': 32,
        'ordinaryFunctionCredit': 0, 'actualOriginalConsumerReturns': native['actualOriginalConsumerReturns']}), flush=True)


if __name__ == '__main__':
    main()
