import hashlib
import json
import struct
from pathlib import Path

from project import ROOT, configuration, native_dependencies, verify_inputs, write_json

CONFIG = configuration()
native_dependencies(CONFIG)
from elftools.elf.elffile import ELFFile
import mechanics_save_enemy_initialize_oracle as model

def sha(data):
    return hashlib.sha256(data).hexdigest()

def source_match(arm):
    report = json.loads((ROOT / 'evidence/matches/mechanics-save-enemy-initialize.json').read_text(encoding='utf-8'))
    row = report['matches'][0]
    if report['romSha256'] != CONFIG['romSha256'] or not row['exactAfterDeclaredRelocation']:
        raise AssertionError('Group proof caller namespace or match differs')
    if sha((ROOT / row['source']).read_bytes()) != row['sourceSha256'] or sha((ROOT / row['object']).read_bytes()) != row['objectSha256']:
        raise AssertionError('Group proof caller source/object differs')
    with (ROOT / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
        code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
    address = int(row['address'], 16)
    for relocation in row['relocations']:
        at = relocation['offset']
        target = int(relocation['target'], 16) + relocation['addend']
        previous = struct.unpack_from('<I', code, at)[0]
        value = target if relocation['type'] == 2 else (previous & 0xff000000) | (((target - address - at) >> 2) & 0xffffff)
        struct.pack_into('<I', code, at, value & 0xffffffff)
    if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
        raise AssertionError('Group proof caller native bytes differ')
    return {row['name']: (row, bytes(code))}

def main():
    identities = verify_inputs(CONFIG)
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    save = (ROOT / 'inputs/save.sav').read_bytes()
    matches = source_match(arm)
    original_write = model.write
    transformed = set()

    def distinct_group_write(memory, address, data):
        if len(data) == 132:
            for base in (model.SAVED_GROUPS, model.RUNTIME_GROUPS):
                relative = address - base - 48
                if 0 <= relative < 4 * 444 and relative % 444 in (0, 132, 264):
                    group = relative // 444
                    slot = relative % 444 // 132
                    identity = struct.unpack_from('<I', data, 20)[0]
                    if identity:
                        changed = bytearray(data)
                        species = (struct.unpack_from('<h', data, 24)[0] + group * 13) % 512
                        struct.pack_into('<IhB', changed, 20, ((group + 1) << 16) | (slot + 1), species, group % 3)
                        data = bytes(changed)
                        transformed.add((base, group, slot))
                    break
        original_write(memory, address, data)

    model.write = distinct_group_write
    try:
        oracle = model.validate(arm, save, matches, ROOT)
    finally:
        model.write = original_write
    if not all(any(base == expected and group == index for base, group, slot in transformed) for expected, count in ((model.SAVED_GROUPS, 4), (model.RUNTIME_GROUPS, 3)) for index in range(count)):
        raise AssertionError('Distinct saved/runtime group coverage absent')
    oracle['distinctGroupFixtureWrites'] = [{'ramBase': hex(base), 'selector': group, 'slot': slot} for base, group, slot in sorted(transformed)]
    oracle['distinctGroupRule'] = 'Nonzero records receive ID((group+1)<<16)|(slot+1), species(original+group*13)%512 and variantgroup%3; zero-ID captured records remain untouched.'
    report = {'schemaVersion': 1, 'romSha256': identities['rom']['sha256'], 'saveSha256': identities['save']['sha256'], 'source': 'verify_section3_groups.py', 'sourceSha256': sha(Path(__file__).read_bytes()), 'matches': [], 'nativeSymbols': {}, 'protocolOnly': True, 'oracle': oracle, 'supportingOracle': {'source': 'mechanics_save_enemy_initialize_oracle.py', 'sha256': sha((ROOT / 'mechanics_save_enemy_initialize_oracle.py').read_bytes())}, 'callerMatch': [{key: row[key] for key in ('name', 'module', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in matches.values()], 'limitations': ['This adds distinct source-group fixtures and no additional function credit.', 'The source match and retained-native/platform limits remain those of the initializer proof.', 'Selectors are controlled native-machine fixtures; four fitting saved groups do not establish a valid selector bound, group purpose or promoted save semantics.']}
    verify_inputs(CONFIG)
    write_json(ROOT / 'evidence/matches/mechanics-save-section3-groups.json', report)
    print(json.dumps({'cases': oracle['cases'], 'nativeAndRecompiledCalls': oracle['nativeAndRecompiledCalls'], 'distinctGroupSlots': len(transformed), 'passed': True}, indent=2))

if __name__ == '__main__':
    main()
