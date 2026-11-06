import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_LR, UC_ARM_REG_SP

SPECS = {
    'save_main_pointer': (0x02063ab0, 12),
    'save_record_pointer': (0x02063abc, 20),
    'save_numeric_get': (0x02063b18, 16),
    'save_numeric_set': (0x02063b28, 24),
    'save_event_get': (0x02063b40, 32),
    'save_event_set': (0x02063b60, 92),
    'save_secondary_get': (0x02063bbc, 32),
    'save_secondary_history_get': (0x02063bdc, 36),
    'save_secondary_set': (0x02063c00, 148),
    'save_secondary_history_set': (0x02063c94, 96),
    'save_counter_first_get': (0x02063cf4, 16),
    'save_counter_first_increment': (0x02063d04, 44),
    'save_counter_second_get': (0x02063d30, 16),
    'save_counter_second_increment': (0x02063d40, 44),
    'save_counter_third_get': (0x02063d6c, 16),
    'save_counter_third_increment': (0x02063d7c, 44),
    'save_section2_pointer': (0x02063e8c, 12),
    'save_section3_pointer': (0x02063f48, 12),
    'save_section4_pointer': (0x02063f6c, 12),
    'save_minimum_set': (0x02063f24, 36),
    'save_gold_get': (0x02062b0c, 16),
    'save_gold_replace': (0x02062b1c, 24),
    'save_gold_adjust': (0x02062b34, 52),
    'save_gold_halve': (0x02062b68, 52),
    'save_inventory_get': (0x02063144, 24),
    'save_payload_valid': (0x0207dac8, 32),
    'save_payload_header28_valid': (0x0207dae8, 60),
    'save_deserialize': (0x0207e160, 132),
    'save_bank_validate': (0x0207e088, 216),
    'save_load_primary': (0x0207e1e4, 140),
    'save_load_async': (0x0207e270, 168),
    'save_load_primary_async': (0x0207e318, 20),
    'save_load_backup_async': (0x0207e32c, 20),
    'save_load_async_poll': (0x0207e340, 184),
}
GLOBALS = {
    'native_main': 0x021bd51c,
    'native_numeric': 0x021c0dc8,
    'native_event': 0x021c0e20,
    'native_secondary': 0x021c0ee0,
    'native_counters': 0x021bd61c,
    'native_section2': 0x021b9eb4,
    'native_section3': 0x021bb278,
    'native_section4': 0x021b9ee8,
    'native_record_array': 0x021c0c7c,
    'native_minimums': 0x021bd50c,
    'native_money': 0x021bd51c,
    'native_inventory': 0x021bd558,
    'save_payload_checksum': 0x0207da70,
    'native_copy': 0x02008e0c,
    'save_header_checksum': 0x0207daa0,
    'native_save_io': 0x021c6bfc,
    'native_allocate': 0x0202a37c,
    'native_save_read': 0x02027d8c,
    'native_free': 0x0202a498,
    'native_save_async_read': 0x02027e44,
    'native_save_poll': 0x02027ef4,
}
FLAGS = ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e', '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off', '-RTTI', 'off', '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink', '-msgstyle', 'gcc']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def compile_and_compare(arm, optimization, inline='off'):
    output = ROOT / f'work/save-worker/accessors-{optimization}-{inline}.o'
    output.parent.mkdir(parents=True, exist_ok=True)
    compiler = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    flags = [f'-O{optimization}', *FLAGS[1:]]
    flags[flags.index('-inline') + 1] = inline
    result = subprocess.run([str(compiler), *flags, '-c', str(ROOT / 'src/save_accessors.c'), '-o', str(output)], env=env, capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError(result.stdout.decode(errors='replace') + result.stderr.decode(errors='replace'))
    object_hash = sha(output.read_bytes())
    stable_output = ROOT / 'work/save-worker/objects' / (object_hash + '.o')
    stable_output.parent.mkdir(parents=True, exist_ok=True)
    if not stable_output.exists():
        stable_output.write_bytes(output.read_bytes())
    records = []
    compiled = {}
    with output.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = {s.name: s for s in elf.get_section_by_name('.symtab').iter_symbols()}
        for name, (address, size) in SPECS.items():
            symbol = symbols[name]
            raw = elf.get_section(symbol['st_shndx']).data()
            start = symbol['st_value']
            code = bytearray(raw[start:start + symbol['st_size']])
            relocations = []
            for section in elf.iter_sections():
                if section['sh_type'] not in ('SHT_REL', 'SHT_RELA') or section['sh_info'] != symbol['st_shndx']:
                    continue
                table = elf.get_section(section['sh_link'])
                for rel in section.iter_relocations():
                    if not start <= rel['r_offset'] < start + len(code):
                        continue
                    target_name = table.get_symbol(rel['r_info_sym']).name
                    target = GLOBALS.get(target_name, SPECS.get(target_name, (None,))[0])
                    if target is None:
                        raise ValueError(('unknown relocation', target_name))
                    at = rel['r_offset'] - start
                    value = struct.unpack_from('<I', code, at)[0]
                    kind = rel['r_info_type']
                    if kind == 2:
                        addend = rel['r_addend'] if section['sh_type'] == 'SHT_RELA' else value
                        struct.pack_into('<I', code, at, (target + addend) & 0xffffffff)
                    elif kind in (1, 28, 29):
                        if section['sh_type'] == 'SHT_RELA':
                            addend = rel['r_addend']
                        else:
                            addend = (value & 0xffffff) << 2
                            if addend & 0x2000000:
                                addend -= 0x4000000
                        displacement = target + addend - (address + at)
                        struct.pack_into('<I', code, at, (value & 0xff000000) | ((displacement >> 2) & 0xffffff))
                    else:
                        raise ValueError(('unsupported relocation', kind))
                    relocations.append({'offset': at, 'type': kind, 'symbol': target_name, 'target': hex(target), 'addend': addend})
            target = arm[address - 0x02000000:address - 0x02000000 + size]
            match = code == target
            records.append({'name': name, 'module': 'arm9', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'compiledBytes': len(code), 'matchingBytes': sum(a == b for a, b in zip(code, target)), 'exactAfterDeclaredRelocation': match, 'targetSha256': sha(target), 'outputSha256': sha(code), 'relocations': relocations, 'flags': flags, 'objectSha256': object_hash, 'object': str(stable_output.relative_to(ROOT)), 'sectionIndex': symbol['st_shndx'], 'sectionOffset': start, 'nativeAlias': f'func_{address:08x}'})
            if match:
                compiled[name] = bytes(code)
    return records, compiled

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', action='store_true')
    args = parser.parse_args()
    rom = (ROOT / 'inputs/game.nds').read_bytes()
    save = (ROOT / 'inputs/save.sav').read_bytes()
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    if sha(rom) != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
        raise ValueError('Wrong measured ROM')
    if sha(save) != '169d65a4c6ffcb0fe996d652f73a01f70d594a08ad2385098f628abbe1c4b8f0':
        raise ValueError('Wrong measured save')
    if sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise ValueError('Wrong extracted ARM9 module')
    compiler_bytes = (ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe').read_bytes()
    if sha(compiler_bytes) != '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880':
        raise ValueError('Wrong pinned compiler')
    all_records = []
    matches = {}
    configurations = [(2, 'off'), (2, 'noauto')]
    if args.search:
        configurations.extend((value, 'off') for value in (0, 1, 3, 4))
    for optimization, inline in configurations:
        records, compiled = compile_and_compare(arm, optimization, inline)
        all_records.extend(records)
        for name in compiled:
            if name not in matches:
                matches[name] = (next(r for r in records if r['name'] == name), compiled[name])
    report = {'schemaVersion': 1, 'romSha256': sha(rom), 'saveSha256': sha(save), 'arm9Sha256': sha(arm), 'source': 'src/save_accessors.c', 'sourceSha256': sha((ROOT / 'src/save_accessors.c').read_bytes()), 'compilerSha256': sha((ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe').read_bytes()), 'matches': [record for record, code in matches.values()], 'attempts': all_records, 'nativeSymbols': {**{name: hex(address) for name, address in GLOBALS.items()}, **{name: hex(spec[0]) for name, spec in SPECS.items()}}, 'wholeLinkedRebuild': False}
    sys.path.insert(0, str(ROOT / 'evidence/save'))
    from validate import validate
    report['oracle'] = validate(arm, save, matches, ROOT)
    for record in report['matches']:
        record.update({'source': report['source'], 'sourceSha256': report['sourceSha256'], 'compilerSha256': report['compilerSha256'], 'linked': False, 'state': 'function-matched'})
    for path_name, expected in [('game.nds', report['romSha256']), ('save.sav', report['saveSha256'])]:
        if sha((ROOT / 'inputs' / path_name).read_bytes()) != expected:
            raise ValueError('Input changed during validation')
    report['inputsUnchanged'] = True
    report['limitations'] = ['Each match includes the complete target span and literal pool after declared ELF relocations.', 'Module linking and whole-ROM reconstruction are validated separately.', 'The header word at offset0x28 is not assigned a gameplay or chronology meaning.', 'Rejected compiler configurations are retained in attempts.']
    path = ROOT / 'evidence/matches/save-accessors.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'matchedFunctions': len(matches), 'matchedBytes': sum(r['bytes'] for r, code in matches.values()), 'compilerAttempts': len(all_records), 'oracleCases': report['oracle']['cases'], 'oracleCalls': report['oracle']['nativeAndRecompiledCalls'], 'unmatched': [name for name in SPECS if name not in matches]}, indent=2))

if __name__ == '__main__':
    main()
