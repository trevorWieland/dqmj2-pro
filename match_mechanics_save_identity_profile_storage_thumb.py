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

SOURCE = 'src/mechanics_save/identity_profile_storage_thumb.c'
COMPILER = 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
SPECS = {'saved_profile_checksum_valid':(0x20971bc,60),'saved_profile_identity_write':(0x209725c,68),'saved_profile_dirty':(0x20972a8,14),'saved_profile_checksum_refresh':(0x20972c0,52),'saved_profile_identity_read':(0x2097370,56),'saved_identity_word_create':(0x20973a8,32),'saved_profile_identity_value':(0x20972f4,58)}
GLOBALS = {'native_crc32_init':(0x2019adc,'arm'),'native_crc32_update':(0x2019ba8,'arm'),'native_fill':(0x2008d78,'arm'),'native_profile_has_value':(0x209718c,'thumb'),'native_identity_word1_set':(0x2096ce4,'thumb'),'native_identity_kind_set':(0x2096db4,'thumb'),'native_identity_kind':(0x2096cf8,'thumb'),'native_identity_word1':(0x2096cbc,'thumb'),'native_identity_pair':(0x2096cac,'thumb'),'native_identity_code_extract':(0x2096f10,'thumb')}
FLAGS = ['-O2', '-thumb', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e', '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off', '-RTTI', 'off', '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink', '-msgstyle', 'gcc']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def bindings():
    values = {**GLOBALS, **{name: (address, 'thumb') for name, (address, size) in SPECS.items()}}
    return {name: {'address': hex(address), 'mode': mode, 'module': 'main', 'processor': 'arm9', 'kind': 'function'} for name, (address, mode) in values.items()}

def compile_and_link(arm, optimization, goal):
    flags = [f'-O{optimization}', *FLAGS[1:]] + (['-opt', 'speed'] if goal == 'speed' else [])
    directory = ROOT / 'work/mechanics-save'
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / f'identity-profile-storage-thumb-{optimization}-{goal}.o'
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
            row = {'name': name, 'module': 'main', 'processor': 'arm9', 'mode': 'Thumb', 'address': hex(address), 'bytes': size, 'compiledBytes': symbol['st_size'], 'targetSha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'source': SOURCE, 'sourceSha256': sha((ROOT / SOURCE).read_bytes()), 'object': str(stable.relative_to(ROOT)), 'objectSha256': object_hash, 'compilerSha256': COMPILER_HASH, 'flags': flags, 'nativeAlias': f'func_{address:08x}', 'sectionIndex': symbol['st_shndx'], 'sectionOffset': start, 'exactAfterDeclaredRelocation': False, 'linked': False}
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
                        raise ValueError('Unexpected Thumb caller relocation format/target')
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', action='store_true')
    args = parser.parse_args()
    rom = (ROOT / 'inputs/game.nds').read_bytes()
    save = (ROOT / 'inputs/save.sav').read_bytes()
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    if sha(rom) != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6' or sha(save) != '169d65a4c6ffcb0fe996d652f73a01f70d594a08ad2385098f628abbe1c4b8f0' or sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise ValueError('Identity Thumb input namespace differs')
    if sha((ROOT / COMPILER).read_bytes()) != COMPILER_HASH:
        raise ValueError('Identity Thumb compiler pin differs')
    attempts = []
    matches = {}
    for optimization, goal in [(2, 'space'), *((2, 'speed'), (3, 'space'), (3, 'speed'))] if args.search else [(2, 'space'), (2, 'speed')]:
        rows, selected = compile_and_link(arm, optimization, goal)
        attempts.extend(rows)
        for name, value in selected.items():
            matches.setdefault(name, value)
    report = {'schemaVersion': 1, 'romSha256': sha(rom), 'saveSha256': sha(save), 'arm9Sha256': sha(arm), 'source': SOURCE, 'sourceSha256': sha((ROOT / SOURCE).read_bytes()), 'compilerSha256': COMPILER_HASH, 'nativeSymbolEntries': bindings(), 'nativeSymbols': {name: row['address'] for name, row in bindings().items()}, 'nativeSymbolModules': {name: 'main' for name in bindings()}, 'matches': [row for row, code, proof in matches.values()], 'attempts': attempts, 'isolatedRealMwCallerLinks': [proof for row, code, proof in matches.values()], 'nativeCalleeCodeOrSourceCredit': 0, 'wholeLinkedRebuild': False}
    from mechanics_save_identity_profile_storage_thumb_oracle import validate
    report['oracle'] = validate(arm, save, {name: (row, code) for name, (row, code, proof) in matches.items()}, ROOT)
    report['oracleSource'] = 'mechanics_save_identity_profile_storage_thumb_oracle.py'
    report['oracleSourceSha256'] = sha((ROOT / report['oracleSource']).read_bytes())
    report['inputsUnchanged'] = sha((ROOT / 'inputs/game.nds').read_bytes()) == report['romSha256'] and sha((ROOT / 'inputs/save.sav').read_bytes()) == report['saveSha256']
    report['limitations'] = ['Seven complete Thumb profile storage bodies are ordinary C verified by the pinned real MW linker with unchanged source RELA calls and zero-code mode bindings.', 'The oracle composes twelve previously accepted C bodies and independently checks raw profile state using Python zlib and hashlib; CRC32, memory fill and the44-byte identity validator remain native boundaries.', 'Malformed and overlapping-pointer probes compare bounded native/compiled behavior, without certifying portable overlap semantics or complete profile legality.', 'No full profile initialization, online behavior, semantic save partition promotion or original input modification is claimed.']
    (ROOT / 'evidence/matches/mechanics-save-identity-profile-storage-thumb.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'matchedFunctions': len(matches), 'matchedBytes': sum(row['bytes'] for row, code, proof in matches.values()), 'oracleCases': report['oracle']['cases'], 'oracleCalls': report['oracle']['nativeAndRecompiledCalls'], 'unmatched': sorted(set(SPECS) - set(matches))}, indent=2))
    if set(matches) != set(SPECS):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
