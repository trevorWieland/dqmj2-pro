import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

SOURCE = 'nonmatching/save-core/20261029-preparation/allocation_commit.c'
COMPILER = 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
SPECS = {'preparation_commit': (0x02076D70,124)}
GLOBALS = {'preparation_state': (0x021C6234,'data'), 'preparation_delta': (0x021C6434,'data'), 'preparation_selected_slot': (0x021C6330,'data'), 'native_allocated_add': (0x02062F3C,'arm'), 'native_rebuild': (0x02078978,'arm'), 'native_skill_observe': (0x0207AEBC,'arm')}
FLAGS = ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e', '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off', '-RTTI', 'off', '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink', '-msgstyle', 'gcc']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def bindings():
    values = {**GLOBALS, **{name: (address, 'arm') for name, (address, size) in SPECS.items()}}
    return {name: {'address': hex(address), 'mode': mode, 'module': 'main', 'processor': 'arm9', 'kind': 'data' if mode == 'data' else 'function'} for name, (address, mode) in values.items()}

def compile_and_link(arm, optimization, goal):
    flags = [f'-O{optimization}', *FLAGS[1:]] + (['-opt', 'speed'] if goal == 'speed' else [])
    directory = ROOT / 'work/mechanics-save/20261029-preparation'
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / f'preparation-{optimization}-{goal}.o'
    process = subprocess.run([str(ROOT / COMPILER), *flags, '-c', str(ROOT / SOURCE), '-o', str(output)], env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, timeout=60)
    if process.returncode:
        raise ValueError(process.stdout.decode(errors='replace') + process.stderr.decode(errors='replace'))
    object_hash = sha(output.read_bytes())
    stable = directory / 'objects' / (object_hash + '.o')
    stable.parent.mkdir(parents=True, exist_ok=True)
    if not stable.exists():
        stable.write_bytes(output.read_bytes())
    attempts = []
    matched = {}
    with stable.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = {symbol.name: symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols()}
        for name, (address, size) in SPECS.items():
            symbol = symbols[name]
            start = symbol['st_value'] & ~1
            row = {'name': name, 'module': 'main', 'processor': 'arm9', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'compiledBytes': symbol['st_size'], 'targetSha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'source': SOURCE, 'sourceSha256': sha((ROOT / SOURCE).read_bytes()), 'object': str(stable.relative_to(ROOT)), 'objectSha256': object_hash, 'compilerSha256': COMPILER_HASH, 'flags': flags, 'nativeAlias': f'func_{address:08x}', 'sectionIndex': symbol['st_shndx'], 'sectionOffset': start, 'exactAfterDeclaredRelocation': False, 'linked': False, 'sourceLanguage': 'C', 'ordinaryCBytes': size}
            relocations = []
            for section in elf.iter_sections():
                if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != symbol['st_shndx']:
                    continue
                table = elf.get_section(section['sh_link'])
                for relocation in section.iter_relocations():
                    offset = relocation['r_offset'] - start
                    if not 0 <= offset < symbol['st_size']:
                        continue
                    target_name = table.get_symbol(relocation['r_info_sym']).name
                    if section['sh_type'] != 'SHT_RELA' or target_name not in bindings():
                        raise ValueError('Unexpected recent-item lookup relocation format/target')
                    target = bindings()[target_name]
                    relocations.append({'offset': offset, 'type': relocation['r_info_type'], 'symbol': target_name, 'target': target['address'], 'addend': relocation['r_addend'], 'format': section['sh_type'], 'targetModule': 'main', 'targetMode': target['mode'], 'processor': 'arm9'})
            row['relocations'] = relocations
            if symbol['st_size'] != size:
                row['failure'] = 'Complete source symbol size differs from configured native span'
            else:
                try:
                    proof = validate_link(row, bindings())
                except ValueError as error:
                    row['failure'] = str(error)
                else:
                    folder = (ROOT / proof['linkedElf']).parent
                    binary = folder / 'caller.bin'
                    validation = folder / 'validation.json'
                    code = binary.read_bytes()
                    row.update({'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True, 'matchingBytes': size, 'outputSha256': sha(code), 'state': 'function-matched'})
                    row.update(freeze_link(proof))
                    matched[name] = (row, code, proof)
            attempts.append(row)
    return attempts, matched
