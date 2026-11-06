import hashlib
import json
import random
import struct
import time
from pathlib import Path

from project import ROOT, configuration, native_dependencies, verify_inputs, write_json

CONFIG = configuration()
native_dependencies(CONFIG)
from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
import mechanics_save_record_update_oracle as record_model
import mechanics_save_features_oracle as feature_model
import mechanics_save_feature_bonus_oracle as bonus_model
import mechanics_save_skill_observe_oracle as skill_model

EKT = 0x02500000
SKILL = 0x02510000
FEAT = 0x02520000
ITEM = 0x02530000
INPUT = 0x02540080
RECORD = 0x021bd674
STOP = 0x027ff800
REPORTS = ('record-update', 'features', 'feature-bonus', 'skill-observe')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def compiled(arm):
    result = {}
    for module in (record_model, feature_model, bonus_model, skill_model):
        result.update(module.dependencies(ROOT, arm))
    for suffix in REPORTS:
        document = json.loads((ROOT / ('evidence/matches/mechanics-save-' + suffix + '.json')).read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Connected record ROM namespace differs')
        for row in document['matches']:
            if sha((ROOT / row['source']).read_bytes()) != row['sourceSha256'] or sha((ROOT / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Connected record source/object identity differs')
            with (ROOT / row['object']).open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
                code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
            address = int(row['address'], 16)
            for relocation in row.get('relocations', []):
                at = relocation['offset']
                target = int(relocation['target'], 16) + relocation['addend']
                previous = struct.unpack_from('<I', code, at)[0]
                value = target if relocation['type'] == 2 else (previous & 0xff000000) | (((target - address - at) >> 2) & 0xffffff)
                struct.pack_into('<I', code, at, value & 0xffffffff)
            if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError('Connected record source span differs')
            result[address] = (row, bytes(code))
    return result

def expected(memory, blobs, name, second, third, gate, success, present):
    ekt, skills, feat, items, levels = blobs
    species = struct.unpack('<h', read(memory, RECORD + 24, 2))[0]
    variant = read(memory, RECORD + 26, 1)[0]
    trace = []
    if name == 'saved_record_block20_initialize':
        features, count = feature_model.collect(ekt, skills if present else None, feat, species, variant, read(memory, RECORD + 122, 10), 256, 256)
        if second:
            write(memory, RECORD + 32, read(memory, second, 32))
        else:
            kind = ekt[species * 100:species * 100 + 100]
            write(memory, RECORD + 32, bytes(32))
            write(memory, RECORD + 32, kind[28:32])
            for family, at in ((24, 36), (26, 38)):
                base = struct.unpack('<h', read(memory, RECORD + (32 if family == 24 else 34), 2))[0]
                value = base + bonus_model.bonus(features, family)
                if read(memory, bonus_model.TOGGLE, 1)[0]:
                    value += items[8 + (33 if family == 24 else 34)]
                write(memory, RECORD + at, struct.pack('<H', min(value, 9999) & 65535))
            write(memory, RECORD + 40, kind[32:40])
            write(memory, RECORD + 48, b'\x01')
            value, trace = skill_model.expected(memory, ekt, skills, levels, 'saved_record_level_word', species, variant, 2, gate, success, present)
            put(memory, RECORD + 56, value)
        return 1, trace
    if name == 'saved_record_skill_initialize':
        at = RECORD + 122 + second * 2
        write(memory, at, read(memory, third, 2) if third else bytes([ekt[species * 100 + 95], 0]))
        identity, allocated = read(memory, at, 2)
        skill_model.expected(memory, ekt, skills, levels, 'saved_skill_observe', species, identity, allocated, gate, success, present)
        return 1, trace
    if name == 'saved_record_skill_allocated_add':
        at = RECORD + 123 + second * 2
        write(memory, at, bytes([(read(memory, at, 1)[0] + third) & 255]))
        return 1, trace
    if name == 'saved_record_skill_nonzero_count':
        return sum(read(memory, RECORD + 122 + index * 2, 1)[0] != 0 for index in range(5)), trace
    raise AssertionError('Unexpected connected operation')

def main():
    identities = verify_inputs(CONFIG)
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    save = (ROOT / 'inputs/save.sav').read_bytes()
    functions = compiled(arm)
    names = {row['name']: address for address, (row, code) in functions.items()}
    rom = NintendoDSRom((ROOT / 'inputs/game.nds').read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'SkillTbl.bin', 'FeatTbl.bin', 'ItemTbl.bin', 'LevelUpTbl.bin')}
    blobs = (assets['EnmyKindTbl.bin'][8:], assets['SkillTbl.bin'], assets['FeatTbl.bin'], assets['ItemTbl.bin'], assets['LevelUpTbl.bin'])
    context = {}
    hits = set()

    def source_entry(machine, address, size, user):
        hits.add(address)

    def resource(machine, address, size, user):
        first, destination, count, offset = [machine.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        if machine.mem_read(first, 15) != b'LevelUpTbl.bin\0' or destination != skill_model.OUTPUT_WORD or count != 4 or offset + count > len(blobs[4]):
            raise AssertionError('Connected resource contract differs')
        context['trace'].append(('LevelUpTbl.bin', destination, count, offset, context['success']))
        if context['success']:
            machine.mem_write(destination, blobs[4][offset:offset + 4])
        for register, value in [(UC_ARM_REG_R0, int(context['success'])), (UC_ARM_REG_R1, 0x11223344), (UC_ARM_REG_R2, 0x22334455), (UC_ARM_REG_R3, 0x33445566)]:
            machine.reg_write(register, value)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for address, (row, code) in functions.items():
                machine.mem_write(address, code)
                machine.hook_add(UC_HOOK_CODE, source_entry, begin=address, end=address)
        machine.hook_add(UC_HOOK_CODE, resource, begin=0x0202a818, end=0x0202a818)
        machines.append(machine)
    rng = random.Random(20261027)
    vectors = [(species, variant, species & 1, species & 2 != 0, True, True, None) for species in range(512) for variant in (0, 1, 2)]
    for bank in (0, 0x7100):
        for index in range(100):
            data = save[bank + 0x1e8 + index * 132:bank + 0x1e8 + (index + 1) * 132]
            species = struct.unpack_from('<h', data, 24)[0]
            if struct.unpack_from('<I', data, 20)[0] and 0 <= species < 512:
                vectors.append((species, data[26], True, True, True, True, data))
    vectors += [(species, 2, gate, toggle, success, present, None) for species in (0, 139, 353, 511) for gate in (False, True) for toggle in (0, 255) for success in (False, True) for present in (False, True)]
    cases = calls = operations = 0
    for species, variant, gate, toggle, success, present, captured in vectors:
        original = {0x020ddd00: bytearray(rng.randbytes(0x100)), 0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021b9000: bytearray(rng.randbytes(0x9000)), 0x021c2a00: bytearray(rng.randbytes(0x1000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), EKT: bytearray(blobs[0] + bytes(0x10000 - len(blobs[0]))), SKILL: bytearray(blobs[1] + bytes(0x4000 - len(blobs[1]))), FEAT: bytearray(blobs[2] + bytes(0x1000 - len(blobs[2]))), ITEM: bytearray(blobs[3][8:] + bytes(0x6000 - len(blobs[3][8:]))), 0x02540000: bytearray(rng.randbytes(0x1000))}
        write(original, 0x021bd51c, save[0x90:0x3a68])
        data = bytearray(captured or rng.randbytes(132))
        struct.pack_into('<IhB', data, 20, 0x12345678, species, variant)
        if captured is None:
            data[122:132] = bytes([1, 0, 2, 255, 128, 100, 255, 255, 0, 0])
        write(original, RECORD, bytes(data))
        put(original, 0x020f69f0, EKT)
        put(original, 0x021c673c, SKILL if present else 0)
        put(original, 0x021c6740, 256)
        put(original, 0x021c6750, FEAT)
        put(original, 0x021c6754, FEAT + 8)
        put(original, 0x021c2ab4, ITEM)
        write(original, bonus_model.TOGGLE, bytes([int(toggle)]))
        put(original, skill_model.EVENT, u32(original, skill_model.EVENT) | (1 << 16) if gate else u32(original, skill_model.EVENT) & ~(1 << 16))
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
        memory = {address: bytearray(data) for address, data in original.items()}
        sequence = [('saved_record_block20_initialize', 0, 0), ('saved_record_skill_initialize', 0, 0), ('saved_record_skill_initialize', 4, INPUT), ('saved_record_skill_allocated_add', 4, 257), ('saved_record_skill_nonzero_count', 0, 0), ('saved_record_block20_initialize', INPUT, 0), ('saved_record_block20_initialize', RECORD + 32, 0), ('saved_record_block20_initialize', 0, 0), ('saved_record_skill_initialize', 1, RECORD + 124)]
        for name, second, third in sequence:
            result, trace = expected(memory, blobs, name, second, third, gate, success, present)
            for machine in machines:
                context.update({'trace': [], 'success': success})
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), (0x12345678, second, third)):
                    machine.reg_write(register, value)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(names[name], STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Connected record execution bounds', species, name))
                if machine.reg_read(UC_ARM_REG_R0) != result or context['trace'] != trace:
                    raise AssertionError(('Connected record result/trace', species, variant, name, context['trace'], trace))
                for address, data in memory.items():
                    observed = bytes(machine.mem_read(address, len(data)))
                    if observed != data:
                        at = next(index for index, (left, right) in enumerate(zip(observed, data)) if left != right)
                        raise AssertionError(('Connected record expected RAM', species, variant, name, hex(address + at), observed[at], data[at]))
                calls += 1
            operations += 1
        cases += 1
    required = {0x0207b460, 0x0207c2b8, 0x0207c3d8, 0x020634cc, 0x0207aebc}
    if not required.issubset(hits):
        raise AssertionError('Former gameplay boundaries did not execute accepted source')
    report = {'schemaVersion': 1, 'romSha256': identities['rom']['sha256'], 'saveSha256': identities['save']['sha256'], 'source': 'verify_record_features.py', 'sourceSha256': sha(Path(__file__).read_bytes()), 'matches': [], 'nativeSymbols': {}, 'protocolOnly': True, 'oracle': {'cases': cases, 'operations': operations, 'nativeAndRecompiledCalls': calls, 'patchedSourceFunctions': len(functions), 'executedSourceFunctions': [functions[address][0]['name'] for address in sorted(hits)], 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimitPerCall': 2, 'returnPcVerified': True, 'independentExpectedRecordLibraryAndResourceTrace': True, 'platformStubs': {'0x0202a818': 'bounded read-only LevelUpTbl resource reader'}, 'retainedNativeDependencies': [{'module': 'main', 'mode': 'ARM', 'address': '0x02008d78', 'bytes': 148, 'sha256': sha(arm[0x8d78:0x8e0c]), 'role': 'SDK fill bytes; native code executes without substitution'}], 'assetSha256': {name: sha(blob) for name, blob in assets.items()}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in functions.values()]}, 'observations': ['Nine operations execute sequentially per fixture, preserving their record, library and LevelUp scratch effects between calls.', 'All512 native species and three variants, captured occupied records from both banks, category2 event gating, equipment-toggle modes, missing skill table, failed resource reads and input aliasing are included.', 'The five former isolated record-update gameplay providers now execute their native or declared-relocation-verified C bodies in the connected chain.'], 'limitations': ['The read-only resource service remains a controlled contract and the SDK fill148-byte body remains retained native ARM, not recovered C.', 'Table-derived raw field behavior does not establish complete stat, experience, feature or unlock semantics; malformed missing-ID faults remain covered by the separate record-update oracle.', 'This evidence promotes no save partition bytes and changes no original game/save.']}
    verify_inputs(CONFIG)
    write_json(ROOT / 'evidence/matches/mechanics-save-record-features.json', report)
    print(json.dumps({'cases': cases, 'operations': operations, 'nativeAndRecompiledCalls': calls, 'patchedSourceFunctions': len(functions), 'passed': True}, indent=2))

if __name__ == '__main__':
    main()
