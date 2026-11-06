import hashlib
import io
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from elf_units import split_symbol
from evidence.save.derive_md5_tables import tables, source_text
from match_mechanics_save_sdk_md5_block import FLAGS, COMPILER, COMPILER_HASH
from link_runtime_unit import LINKER, LINKER_HASH

SOURCE = 'src/mechanics_save/sdk_md5_tables.c'
SPECS = {'saved_md5_padding': (0x020dcb6c, 1, 'SAVED_MD5_PADDING', 'padding'), 'saved_md5_indices': (0x020dcb70, 192, 'SAVED_MD5_INDICES', 'indices'), 'saved_md5_constants': (0x020dcc30, 256, 'SAVED_MD5_CONSTANTS', 'constants')}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compile_data(arm):
    derived = tables()
    source = ROOT / SOURCE
    if source.read_text() != source_text(derived):
        raise AssertionError('MD5 typed C data does not equal independent mathematical rendering')
    if sha((ROOT / COMPILER).read_bytes()) != COMPILER_HASH or sha(LINKER.read_bytes()) != LINKER_HASH:
        raise AssertionError('MD5 typed data compiler/linker pin differs')
    config = (ROOT / 'config/arm9/symbols.txt').read_text()
    delinks = (ROOT / 'config/arm9/delinks.txt').read_text()
    objects = []
    matches = {}
    directory = ROOT / 'work/mechanics-save/md5-data'
    directory.mkdir(parents=True, exist_ok=True)
    for name, (address, size, selector, meaning) in SPECS.items():
        alias = f'data_{address:08x}'
        if not re.search(r'^' + alias + r' kind:data\(any\) addr:0x' + f'{address:08x}' + '$', config, re.M):
            raise AssertionError('MD5 canonical native data alias differs')
        ranges = [(int(start, 0), int(end, 0)) for start, end in re.findall(r'^\s*\.data\s+start:(0x[0-9a-f]+)\s+end:(0x[0-9a-f]+)', delinks, re.M)]
        if not any(start <= address and address + size <= end for start, end in ranges):
            raise AssertionError('MD5 native data lies outside measured writable data placement')
        flags = [*FLAGS, '-D' + selector]
        output = directory / (name + '.o')
        process = subprocess.run([str(ROOT / COMPILER), *flags, '-c', str(source), '-o', str(output)], capture_output=True, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), timeout=30)
        if process.returncode:
            raise AssertionError(('MD5 typed data compile failed', process.stdout, process.stderr))
        object_data = output.read_bytes()
        stable = directory / (sha(object_data) + '.o')
        stable.write_bytes(object_data)
        with io.BytesIO(object_data) as stream:
            elf = ELFFile(stream)
            symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == name)
            section = elf.get_section(symbol['st_shndx'])
            if symbol['st_info']['type'] != 'STT_OBJECT' or symbol['st_value'] != 0 or symbol['st_size'] != size or section['sh_type'] != 'SHT_PROGBITS' or section['sh_flags'] & 4:
                raise AssertionError('MD5 typed data ELF object type/extent/storage differs')
            payload = section.data()[:size]
            independent = bytes(derived[meaning]) if meaning == 'padding' else struct.pack('<' + str(size // 4) + 'I', *derived[meaning])
            target = arm[address - 0x02000000:address - 0x02000000 + size]
            if payload != independent or payload != target:
                raise AssertionError('MD5 compiled/independently derived/native data differ')
            if any(item['sh_type'] in ('SHT_REL', 'SHT_RELA') and item['sh_info'] == symbol['st_shndx'] and item.num_relocations() for item in elf.iter_sections()):
                raise AssertionError('MD5 mathematical data unexpectedly has relocations')
            padding = section['sh_size'] - size
            split = directory / (name + '-split.o')
            split_symbol(elf, name, split, section_padding=padding, target_section='.data')
            row = {'name': name, 'symbol': name, 'module': 'main', 'processor': 'arm9', 'kind': 'initialized-data', 'sourceLanguage': 'C', 'address': hex(address), 'size': size, 'bytes': size, 'initializedBytes': size, 'compiledBytes': size, 'sourceSymbolType': 'STT_OBJECT', 'section': '.rodata', 'targetSection': '.data', 'sectionIndex': symbol['st_shndx'], 'sectionOffset': 0, 'sectionPaddingBytes': padding, 'source': SOURCE, 'sourceSha256': sha(source.read_bytes()), 'object': stable.relative_to(ROOT).as_posix(), 'objectSha256': sha(object_data), 'compiler': COMPILER, 'compilerSha256': COMPILER_HASH, 'flags': flags, 'compilerFlags': flags, 'nativeAlias': alias, 'relocations': [], 'exactAfterDeclaredRelocation': True, 'rawSha256': sha(payload), 'outputSha256': sha(payload), 'targetSha256': sha(target), 'meaning': meaning, 'derivation': derived['derivation'][meaning], 'targetSectionEvidence': {'path': 'config/arm9/delinks.txt', 'sha256': sha((ROOT / 'config/arm9/delinks.txt').read_bytes()), 'section': '.data'}, 'splitObject': split.relative_to(ROOT).as_posix(), 'splitObjectSha256': sha(split.read_bytes())}
        objects.append(split)
        matches[name] = row, payload
    identity = sha(json.dumps([row['objectSha256'] for row, payload in matches.values()]).encode())
    linked_directory = directory / identity
    linked_directory.mkdir(parents=True, exist_ok=True)
    from shutil import copyfile
    memories = []
    sections = []
    for index, (name, (row, payload)) in enumerate(matches.items()):
        local = linked_directory / (name + '.o')
        copyfile(ROOT / row['splitObject'], local)
        memories.append(f'DATA{index}: ORIGIN = {row["address"]} > {name}.bin')
        sections.append(f'.data{index}: {{ {name}.o(.data) }} > DATA{index}')
    lcf = linked_directory / 'data.lcf'
    lcf.write_text('MEMORY {\n' + '\n'.join(memories) + '\n}\nSECTIONS {\n' + '\n'.join(sections) + '\n}\n')
    linked = linked_directory / 'data.elf'
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-main', 'saved_md5_padding', str(lcf), *(str(linked_directory / (name + '.o')) for name in matches), '-o', str(linked)]
    process = subprocess.run(command, cwd=linked_directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    if process.returncode:
        raise AssertionError(('MD5 typed data real link failed', process.stdout, process.stderr))
    with linked.open('rb') as stream:
        symbols = {symbol.name: symbol for symbol in ELFFile(stream).get_section_by_name('.symtab').iter_symbols()}
        for name, (row, payload) in matches.items():
            binary = linked_directory / (name + '.bin')
            actual = binary.read_bytes()
            symbol = symbols[name]
            if actual != payload or symbol['st_value'] != int(row['address'], 0) or symbol['st_size'] != row['bytes'] or symbol['st_info']['type'] != 'STT_OBJECT':
                raise AssertionError('MD5 actual linked data extent/bytes/type differs')
            row.update({'exactAfterRealMwLink': True, 'linkedDataBinary': binary.relative_to(ROOT).as_posix(), 'linkedDataBinarySha256': sha(actual), 'linkedElf': linked.relative_to(ROOT).as_posix(), 'linkedElfSha256': sha(linked.read_bytes()), 'lcf': lcf.relative_to(ROOT).as_posix(), 'lcfSha256': sha(lcf.read_bytes()), 'linkerSha256': LINKER_HASH})
    return matches, derived


def main():
    rom_sha = sha((ROOT / 'inputs/game.nds').read_bytes())
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    save = (ROOT / 'inputs/save.sav').read_bytes()
    if rom_sha != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6' or sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f' or sha(save) != '169d65a4c6ffcb0fe996d652f73a01f70d594a08ad2385098f628abbe1c4b8f0':
        raise AssertionError('MD5 typed data host input namespace differs')
    matches, derived = compile_data(arm)
    from mechanics_save_sdk_md5_data_oracle import validate
    oracle = validate(arm, save, matches, ROOT)
    report = {'schemaVersion': 1, 'date': '2026-10-27', 'romSha256': rom_sha, 'saveSha256': sha(save), 'arm9Sha256': sha(arm), 'module': 'main', 'processor': 'arm9', 'source': SOURCE, 'sourceSha256': sha((ROOT / SOURCE).read_bytes()), 'sourceLanguage': 'C', 'compilerSha256': COMPILER_HASH, 'dataMatches': [row for row, payload in matches.values()], 'dataAliases': {row['nativeAlias']: row['address'] for row, payload in matches.values()}, 'nativeSymbols': {}, 'initializedDataBytes': 449, 'ordinaryCCodeBytes': 0, 'alignmentPadding': {'address': '0x020dcb6d', 'bytes': 3, 'sourceCredit': 0}, 'mathematicalDerivation': derived, 'derivationSource': 'evidence/save/derive_md5_tables.py', 'derivationSourceSha256': sha((ROOT / 'evidence/save/derive_md5_tables.py').read_bytes()), 'oracle': oracle, 'oracleSource': 'mechanics_save_sdk_md5_data_oracle.py', 'oracleSourceSha256': sha((ROOT / 'mechanics_save_sdk_md5_data_oracle.py').read_bytes()), 'wholeModuleLinked': False, 'limitations': ['Only the padding byte,48 typed message-index words and64 typed sine-constant words are recovered as independently derived C data; no raw asset, code blob or semantic save-byte classification is included.', 'The three alignment bytes after the padding object remain separate/uncredited, even though the target memory helper may read an adjacent byte and mask it away.', 'No cryptographic security property or authenticated original source variable names are inferred from deterministic MD5 values and native use/layout.']}
    report['inputsUnchanged'] = sha((ROOT / 'inputs/game.nds').read_bytes()) == rom_sha and sha((ROOT / 'inputs/save.sav').read_bytes()) == sha(save)
    if not report['inputsUnchanged']:
        raise AssertionError('MD5 data original inputs changed')
    (ROOT / 'evidence/data/sdk-md5-tables.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'dataObjects': len(matches), 'typedInitializedBytes': 449, 'uncreditedAlignmentBytes': 3, 'oracleCases': oracle['cases'], 'oracleCalls': oracle['nativeAndSourceCalls']}, indent=2))


if __name__ == '__main__':
    main()
