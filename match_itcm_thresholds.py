import json
import os
import re
import subprocess
from pathlib import Path
import match_lowlevel as matcher
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control50/thresholds.c'
OUTPUT = ROOT / 'evidence/data/itcm-thresholds.json'
ADDRESS = 0x01FFBB04
SIZE = 48
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Threshold data compiler pin changed')
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    if matcher.sha(binary) != '69b4ab1dc8c4f9c05388bbcc456ba6037fd8f09ab774d65a3eb8adc130e1c1fb':
        raise ValueError('Threshold table input module changed')
    delinks = ROOT / 'config/arm9/itcm/delinks.txt'
    extent = re.search(r'^\s*\.text\s+start:(0x[0-9a-f]+) end:(0x[0-9a-f]+) kind:code', delinks.read_text(), re.M)
    if extent is None:
        raise ValueError('Measured ITCM text extent is missing')
    first, last = map(lambda value: int(value, 0), extent.groups())
    if (first, last) != (0x01FF8000, 0x01FFF894) or not first <= ADDRESS < ADDRESS + SIZE <= last:
        raise ValueError('Threshold table does not lie inside the measured native ITCM text extent')
    for mode, size, address in re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', (ROOT / 'config/arm9/itcm/symbols.txt').read_text()):
        first, count = int(address, 0), int(size, 0)
        if first < ADDRESS + SIZE and ADDRESS < first + count:
            raise ValueError('Threshold data overlaps a configured function')
    work = ROOT / 'work/lowlevel-recovery/itcm-thresholds'
    work.mkdir(parents=True, exist_ok=True)
    output = work / 'thresholds.o'
    flags = ['-O2', '-proc', 'arm946e', '-sym', 'on', '-nolink', '-c']
    command = [str(matcher.COMPILER), *flags, str(SOURCE), '-o', str(output)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30,
                            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:
        raise ValueError('Threshold table compilation failed: ' + result.stdout + result.stderr)
    object_hash = matcher.sha(output.read_bytes())
    stable = work / (object_hash + '.o')
    if not stable.exists():
        stable.write_bytes(output.read_bytes())
    with output.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(item for item in elf.get_section_by_name('.symtab').iter_symbols() if item.name == 'native_data_01ffbb04')
        section = elf.get_section(symbol['st_shndx'])
        if section['sh_type'] != 'SHT_PROGBITS' or section['sh_flags'] & 4 or symbol['st_size'] != SIZE or symbol['st_info']['type'] != 'STT_OBJECT':
            raise ValueError('Threshold source did not emit the expected non-executable typed data extent')
        start = symbol['st_value']
        payload = section.data()[start:start + SIZE]
        if any(item['sh_type'] in ('SHT_REL', 'SHT_RELA') and item['sh_info'] == symbol['st_shndx'] and item.num_relocations() for item in elf.iter_sections()):
            raise ValueError('Numeric threshold table unexpectedly contains relocations')
        native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + SIZE]
        if payload != native:
            raise ValueError('Compiled s32 threshold table differs from native initialized data')
        entry = {'name': symbol.name, 'symbol': symbol.name, 'module': 'itcm', 'processor': 'arm9', 'kind': 'data',
                 'address': hex(ADDRESS), 'bytes': SIZE, 'size': SIZE, 'initializedBytes': SIZE, 'compiledBytes': SIZE,
                 'allocatedZeroFillBytes': 0, 'nativeAlias': 'data_01ffbb04', 'section': section.name,
                 'targetSection': '.text', 'sourceSymbolType': symbol['st_info']['type'],
                 'nativeDataDeclaration': {'name': 'data_01ffbb04', 'kind': 'data(word)', 'address': '0x01ffbb04'},
                 'targetSectionEvidence': {'path': delinks.relative_to(ROOT).as_posix(), 'sha256': matcher.sha(delinks.read_bytes()),
                                           'section': '.text', 'start': hex(first), 'end': hex(last),
                                           'rangeStart': hex(ADDRESS), 'rangeEnd': hex(ADDRESS + SIZE)},
                 'sectionType': section['sh_type'], 'sectionFlags': section['sh_flags'], 'sectionIndex': symbol['st_shndx'],
                 'sectionOffset': start, 'source': SOURCE.relative_to(ROOT).as_posix(), 'sourceSha256': matcher.sha(SOURCE.read_bytes()),
                 'object': stable.relative_to(ROOT).as_posix(), 'objectSha256': object_hash,
                 'compiler': matcher.COMPILER.relative_to(ROOT).as_posix(), 'compilerSha256': PIN, 'compilerFlags': flags,
                 'inputModuleSha256': matcher.sha(binary), 'targetSha256': matcher.sha(native), 'outputSha256': matcher.sha(payload),
                 'relocations': [], 'exactAfterDeclaredRelocation': True, 'linked': False,
                 'dataProof': {'consumer': 'itcm:arm9:0x01ffbffc', 'entryWidth': 4, 'entryKind': 'signed-numeric-threshold',
                               'indexMinimum': 0, 'indexMaximum': 11, 'countedFlags': 10,
                               'nativeIndexedLoadAddresses': ['0x01ffc11c', '0x01ffc124'],
                               'followingWordAt01ffbb34Classified': False}}
    report = {'schemaVersion': 1, 'romSha256': matcher.sha((ROOT / 'inputs/game.nds').read_bytes()),
              'module': 'itcm', 'dataMatches': [entry], 'nativeSymbols': {}, 'functionMatched': 0, 'dataMatchedBytes': SIZE,
              'bssMatchedBytes': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'limitations': ['Twelve indexed numeric words are reconstructed as typed data, with zero function credit',
                              'The following native word is outside the demonstrated index range and remains unclassified',
                              'The typed table describes measured arithmetic use; historical identifier and application meaning remain unknown']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print({'dataMatchedBytes': SIZE, 'functions': 0, 'followingWordClassified': False})


if __name__ == '__main__':
    main()
