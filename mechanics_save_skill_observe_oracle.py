import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

EKT = 0x02500000
SKILL = 0x02510000
OBSERVED = 0x021c0ba4
LEVELS = 0x021c0bc4
FEATURES = 0x021c0b84
EVENT = 0x021c0e20
OUTPUT_WORD = 0x021b9e9c
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x020449d4, 0x02044cdc, 0x02044f9c, 0x0207aa98, 0x0207ad80, 0x0203d128, 0x0203d0cc, 0x02063b40, 0x020636e0, 0x02063704, 0x02063734, 0x02063758, 0x02063798, 0x020637bc}
    reports = [root / batch['report'] for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']]
    reports.append(root / 'evidence/matches/mechanics-save-library.json')
    result = {}
    for path in reports:
        document = json.loads(path.read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Skill dependency namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if address not in wanted or row.get('module') not in ('main', 'arm9'):
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Skill dependency identity differs')
            with (root / row['object']).open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
                code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
            for relocation in row.get('relocations', []):
                at = relocation['offset']
                target = int(relocation['target'], 16) + relocation['addend']
                previous = struct.unpack_from('<I', code, at)[0]
                value = target if relocation['type'] == 2 else (previous & 0xff000000) | (((target - address - at) >> 2) & 0xffffff)
                struct.pack_into('<I', code, at, value & 0xffffffff)
            if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError('Skill dependency native span differs')
            result[address] = (row, bytes(code))
    if not {0x020449d4, 0x02044cdc, 0x02044f9c, 0x0207aa98, 0x0207ad80, 0x0203d128}.issubset(result):
        raise AssertionError('Required skill dependency source absent')
    return result

def prefix_count(record, allocated):
    count = 0
    for index in range(10):
        if not (record[10 + index * 4] or record[50 + index]) or record[index] > allocated:
            break
        count += 1
    return count

def bit_set(memory, base, index):
    at = base + (index >> 5) * 4
    put(memory, at, u32(memory, at) | (1 << (index & 31)))

def level_get(memory, index):
    return (u32(memory, LEVELS + (index >> 3) * 4) >> ((index & 7) * 4)) & 15

def level_set(memory, index, value):
    at = LEVELS + (index >> 3) * 4
    shift = (index & 7) * 4
    put(memory, at, (u32(memory, at) & ~(15 << shift)) | ((value << shift) & 0xffffffff))

def expected(memory, ekt, skill, level_table, name, first, second, third, enabled, file_success, table_present):
    trace = []
    if name == 'saved_skill_threshold_prefix_count':
        return prefix_count(read(memory, first, 60), second), trace
    if name == 'saved_skill_entry_native_id':
        record = read(memory, first, 60)
        return record[10 + second * 4] or record[50 + second], trace
    if name == 'saved_record_level_word':
        if not 1 <= third <= 100:
            return 0, trace
        curve = ekt[first * 100 + 67]
        offset = curve * 400 + (third - 1) * 4
        trace.append(('LevelUpTbl.bin', OUTPUT_WORD, 4, offset, file_success))
        if file_success:
            value = struct.unpack_from('<I', level_table, offset)[0]
            put(memory, OUTPUT_WORD, value)
            return value, trace
        return 0, trace
    if name == 'saved_skill_observe':
        category = ((struct.unpack_from('<H', ekt, first * 100 + 4)[0] >> 8) & 15) // 3
        if category == 2 and not enabled:
            return None, trace
        bit_set(memory, OBSERVED, second)
        if not table_present or not 0 <= second < 256:
            return None, trace
        record = skill[8 + second * 60:8 + second * 60 + 60]
        count = prefix_count(record, third) & 255
        if level_get(memory, second) < count:
            level_set(memory, second, count)
        for index in range(count):
            if record[10 + index * 4] == 0:
                bit_set(memory, FEATURES, record[50 + index])
        return None, trace
    raise AssertionError(('Unknown skill observation function', name))

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    machines = []
    context = {}
    rom = NintendoDSRom((root / 'inputs/game.nds').read_bytes())
    blobs = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'SkillTbl.bin', 'LevelUpTbl.bin')}
    ekt = blobs['EnmyKindTbl.bin'][8:]
    skill = blobs['SkillTbl.bin']
    levels = blobs['LevelUpTbl.bin']
    if len(levels) != 7200:
        raise AssertionError('Measured LevelUp table length differs')

    def resource(machine, address, size, user):
        first, destination, count, offset = [machine.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        if machine.mem_read(first, 15) != b'LevelUpTbl.bin\0' or destination != OUTPUT_WORD or count != 4 or offset + count > len(levels):
            raise AssertionError('Native LevelUp resource-read contract differs')
        context['trace'].append(('LevelUpTbl.bin', destination, count, offset, context['success']))
        if context['success']:
            machine.mem_write(destination, levels[offset:offset + count])
        for register, value in [(UC_ARM_REG_R0, int(context['success'])), (UC_ARM_REG_R1, 0x11223344), (UC_ARM_REG_R2, 0x22334455), (UC_ARM_REG_R3, 0x33445566)]:
            machine.reg_write(register, value)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machine.hook_add(UC_HOOK_CODE, resource, begin=0x0202a818, end=0x0202a818)
        machines.append(machine)
    rng = random.Random(20261027)
    synthetic = bytearray(skill)
    record = bytearray(60)
    record[:10] = bytes([0, 200, 1, 3, 4, 5, 6, 7, 8, 9])
    record[10] = 7
    record[50] = 8
    record[51] = 9
    record[18] = 3
    synthetic[68:128] = record
    representatives = [next(index for index in range(512) if ((struct.unpack_from('<H', ekt, index * 100 + 4)[0] >> 8) & 15) // 3 == category) for category in range(3)]
    curve_species = {}
    for species in range(512):
        curve_species.setdefault(ekt[species * 100 + 67], species)
    cases = 0
    calls = 0
    for label, table, present in [('measured', skill, True), ('synthetic', bytes(synthetic), True), ('absent-table', skill, False)]:
        vectors = []
        if present:
            for identity in (range(256) if label == 'measured' else [1]):
                data = table[8 + identity * 60:8 + identity * 60 + 60]
                points = sorted({-1, 0, 255, 256, *[max(-1, value + delta) for value in data[:10] for delta in (-1, 0, 1)]})
                vectors += [('saved_skill_threshold_prefix_count', SKILL + 8 + identity * 60, allocated, 0, 0, True, 0) for allocated in points]
                vectors += [('saved_skill_entry_native_id', SKILL + 8 + identity * 60, index, 0, 0, True, 0) for index in range(10)]
        for species in representatives:
            for identity in (-1, 0, 1, 127, 255, 256):
                for allocated in (-1, 0, 1, 99, 255, 256):
                    for enabled in (False, True):
                        for old_level in (0, 1, 10, 15):
                            vectors.append(('saved_skill_observe', species, identity, allocated, enabled, True, old_level))
        if label == 'measured':
            vectors += [('saved_record_level_word', species, 0, level, 0, True, 0) for species in curve_species.values() for level in range(1, 101)]
            vectors += [('saved_record_level_word', species, variant, level, 0, success, 0) for species in range(512) for variant in (0, 2) for level, success in [(2, True), (100, True), (2, False)]]
            vectors += [('saved_record_level_word', species, 0, level, 0, True, 0) for species in representatives for level in (-1, 0, 101, 0x7fffffff)]
        for name, first, second, third, enabled, success, old_level in vectors:
            if name not in matches:
                continue
            original = {0x021b9000: bytearray(rng.randbytes(0x9000)), 0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), EKT: bytearray(ekt + bytes(0x10000 - len(ekt))), SKILL: bytearray(table + bytes(0x4000 - len(table)))}
            write(original, 0x021bd51c, save[0x90:0x3a68])
            put(original, 0x020f69f0, EKT)
            put(original, 0x021c673c, SKILL if present else 0)
            put(original, 0x021c6740, 256)
            if name == 'saved_skill_observe':
                at = EVENT
                put(original, at, u32(original, at) | (1 << 16) if enabled else u32(original, at) & ~(1 << 16))
                if 0 <= second < 256:
                    level_set(original, second, old_level)
            memory = {address: bytearray(data) for address, data in original.items()}
            result, trace = expected(memory, ekt, table, levels, name, first, second, third, enabled, success, present)
            row, code = matches[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                context.update({'trace': [], 'success': success})
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), (first, second, third)):
                    machine.reg_write(register, value & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Skill observation bounds', label, name, first, second, third))
                if (result is not None and machine.reg_read(UC_ARM_REG_R0) != result & 0xffffffff) or context['trace'] != trace:
                    raise AssertionError(('Skill/LevelUp result or resource trace differs', label, name, first, second, third, context['trace'], trace))
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        raise AssertionError(('Skill observation/library/event/LevelUp/input/guard RAM differs', label, name, first, second, third))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedSkillLibraryAndNativeLevelTable': True, 'platformStubs': {'0x0202a818': 'bounded read-only LevelUpTbl resource contract'}, 'assetSha256': {name: sha(blob) for name, blob in blobs.items()}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Threshold prefix count stops at the first empty action/feature stage or unmet allocated-point threshold, even when later stages would qualify.', 'Entry-ID getter prefers the action byte and falls back to the feature byte; observed feature flags are set only for feature-kind stages.', 'Category2 skill observation is gated by native event16; other categories bypass that gate.', 'Observation marks the raw skill bit even when no skill table row is available; existing nibble level only increases.', 'Level word reader accepts levels1..100, ignores the variant through the measured growth-type getter, and reads curve*400+(level-1)*4 from the7200-byte local LevelUpTbl.', 'Failed resource reads return0 and preserve the previous scratch word; invalid levels never invoke the resource service.'], 'limitations': ['The resource reader is a controlled memory contract; its file/cache/allocator implementation remains outside this batch.', 'Negative/out-of-table skill IDs are isolated raw bit-bank probes, not valid skill identity claims.', 'Raw library bits/nibbles, action/feature domains and event16 gate do not establish complete unlock or gameplay semantics.', 'The entry getter uses the signed-byte caller ABI observed in the native observer; tested entry indices are0..9.', 'No original table, game or save is mutated.']}
