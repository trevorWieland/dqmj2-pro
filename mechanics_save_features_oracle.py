import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put

EKT = 0x02500000
SKILL = 0x02510000
FEAT = 0x02520000
SKILLS = 0x02530040
LIST = 0x02530100
OUTPUT = 0x02540080
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x020449d4, 0x02044cdc, 0x0207aa98, 0x02008d78}
    registry = json.loads((root / 'recovery.json').read_text(encoding='utf-8'))
    reports = [root / batch['report'] for batch in registry['batches']]
    reports.append(root / 'evidence/matches/mechanics-save-library.json')
    result = {}
    for path in reports:
        document = json.loads(path.read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Feature dependency namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if address not in wanted or row.get('module') not in ('main', 'arm9'):
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Feature dependency identity differs')
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
                raise AssertionError('Feature dependency native span differs')
            result[address] = (row, bytes(code))
    if not {0x020449d4, 0x02044cdc, 0x0207aa98}.issubset(result):
        raise AssertionError('Required feature dependencies absent')
    return result

def variant_offset(ekt, species):
    group = struct.unpack_from('<H', ekt, species * 100 + 4)[0] & 15
    return (group - 1) // 3 if group else 0

def append_allowed(feat, feature, values, count):
    at = 8 + feature * 8
    return int(bool(feat[at] & 4) or all(value not in (feature, feat[at + 1]) for value in values[:max(count, 0)]))

def parent_find(feat, feature, feature_count):
    return next((index for index in range(max(feature_count, 0)) if feat[8 + index * 8 + 1] == feature), 0)

def collect(ekt, skills_table, feat, species, variant, skills, skill_count, feature_count):
    category = ((struct.unpack_from('<H', ekt, species * 100 + 4)[0] >> 8) & 15) // 3
    offset = variant_offset(ekt, species)
    maximum = min(variant + offset + 2, 4) if category == 0 else min(int((variant + offset) / 2) + 3, 4) if category == 1 else 4
    if category not in (0, 1, 2):
        raise AssertionError('Uninitialized native maximum outside tested categories')
    values = [value for value in ekt[species * 100 + 63:species * 100 + 63 + max(maximum, 0)] if value]
    if skills is not None and skills_table is not None:
        for slot in range(5):
            identity, allocated = skills[slot * 2:slot * 2 + 2]
            if not identity or identity >= skill_count:
                continue
            record = skills_table[8 + identity * 60:8 + identity * 60 + 60]
            for index in range(10):
                feature = record[50 + index]
                if feature and allocated >= record[index] and append_allowed(feat, feature, values, len(values)):
                    parent = parent_find(feat, feature, feature_count)
                    if parent > 0 and parent in values:
                        values.remove(parent)
                    values.append(feature)
    if len(values) > 64:
        raise AssertionError('Test fixture exceeded native output capacity')
    return bytes(values) + bytes(64 - len(values)), len(values)

def expected(memory, ekt, skill_table, feat, name, first, second, third, fourth, skill_count, feature_count):
    if name == 'saved_native_variant_offset':
        return variant_offset(ekt, first)
    if name == 'saved_feature_parent_find':
        return parent_find(feat, first, feature_count)
    values = bytearray(read(memory, LIST, 64))
    if name == 'saved_feature_append_allowed':
        return append_allowed(feat, first, values, third)
    if name == 'saved_feature_remove_first':
        if third > 0 and first in list(values[:third]):
            at = values[:third].index(first)
            values[at:third - 1] = values[at + 1:third]
            third -= 1
            values[third] = 0
            write(memory, LIST, bytes(values))
        return third
    if name == 'saved_feature_occurrences':
        if not second:
            return 0
        stop = values.index(0) if 0 in values else 64
        return sum(value == first for value in values[:stop])
    if name == 'saved_feature_collect':
        skills = read(memory, third, 10) if third else None
        output, count = collect(ekt, skill_table, feat, first, second, skills, skill_count, feature_count)
        write(memory, fourth, output)
        return count
    raise AssertionError(('Unknown feature function', name))

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rom = NintendoDSRom((root / 'inputs/game.nds').read_bytes())
    blobs = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'SkillTbl.bin', 'FeatTbl.bin')}
    ekt = blobs['EnmyKindTbl.bin'][8:]
    skill_table = blobs['SkillTbl.bin']
    feat = blobs['FeatTbl.bin']
    if len(ekt) != 51200 or len(skill_table) != 15368 or len(feat) != 2056:
        raise AssertionError('Measured native feature table lengths differ')
    rng = random.Random(20261027)
    fixtures = [(ekt, skill_table, feat, 256, 256, 'measured')]
    synthetic_ekt = bytearray(ekt)
    struct.pack_into('<H', synthetic_ekt, 4, 1)
    synthetic_ekt[63:67] = bytes([10, 20, 0, 0])
    synthetic_feat = bytearray(feat)
    for index in range(256):
        synthetic_feat[8 + index * 8:10 + index * 8] = b'\0\0'
    for parent, child in [(10, 11), (20, 21), (11, 12)]:
        synthetic_feat[8 + parent * 8 + 1] = child
    synthetic_feat[8 + 99 * 8] = 4
    synthetic_skill = bytearray(skill_table)
    synthetic_skill[8 + 60:8 + 70] = bytes(range(10))
    synthetic_skill[8 + 60 + 50:8 + 120] = bytes([11, 21, 11, 12, 99, 99, 10, 20, 0, 11])
    for feature_count in (-1, 0, 1, 256):
        for skill_count in (0, 256):
            fixtures.append((bytes(synthetic_ekt), bytes(synthetic_skill), bytes(synthetic_feat), skill_count, feature_count, 'synthetic-groups'))
    maximal_ekt = bytearray(synthetic_ekt)
    struct.pack_into('<H', maximal_ekt, 4, 0x601)
    maximal_ekt[63:67] = bytes([99]) * 4
    maximal_skill = bytearray(synthetic_skill)
    maximal_skill[68:78] = bytes(10)
    maximal_skill[118:128] = bytes([99]) * 10
    fixtures.append((bytes(maximal_ekt), bytes(maximal_skill), bytes(synthetic_feat), 256, 256, 'synthetic-maximal'))
    fixtures.append((ekt, None, feat, 256, 256, 'absent-skill-table'))
    cases = 0
    calls = 0
    maximum_output = 0
    for ekt_data, skill_data, feat_data, skill_count, feature_count, label in fixtures:
        base = {0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), EKT: bytearray(ekt_data + bytes(0x10000 - len(ekt_data))), SKILL: bytearray((skill_data or bytes(len(skill_table))) + bytes(0x4000 - len(skill_table))), FEAT: bytearray(feat_data + bytes(0x1000 - len(feat_data))), 0x02530000: bytearray(rng.randbytes(0x1000)), 0x02540000: bytearray(rng.randbytes(0x1000))}
        put(base, 0x020f69f0, EKT)
        put(base, 0x021c673c, SKILL if skill_data is not None else 0)
        put(base, 0x021c6740, skill_count)
        put(base, 0x021c6750, FEAT)
        put(base, 0x021c6754, FEAT + 8)
        put(base, FEAT + 4, feature_count)
        vectors = []
        ids = range(256) if label == 'measured' else [0, 10, 11, 12, 20, 21, 99, 255]
        for feature in ids:
            vectors.append(('saved_feature_parent_find', feature, 0, 0, OUTPUT, 0))
            for count in (-1, 0, 1, 8, 64):
                for pattern in range(3):
                    vectors.append(('saved_feature_append_allowed', feature, LIST, count, OUTPUT, pattern))
                    vectors.append(('saved_feature_remove_first', feature, LIST, count, OUTPUT, pattern))
            for pattern in range(4):
                vectors.append(('saved_feature_occurrences', feature, LIST if pattern != 3 else 0, 0, OUTPUT, pattern))
        if label == 'measured':
            vectors += [('saved_native_variant_offset', species, 0, 0, OUTPUT, 0) for species in range(512)]
            vectors += [('saved_feature_collect', species, variant, 0, OUTPUT, 0) for species in range(512) for variant in (0, 1, 2)]
            vectors += [('saved_feature_collect', species, species % 3, SKILLS, OUTPUT, species % 100) for species in range(512)]
        else:
            vectors += [('saved_feature_collect', 0, variant, SKILLS, OUTPUT, allocated) for variant in (-7, -1, 0, 1, 2) for allocated in (0, 1, 2, 3, 4, 5, 9, 255)]
        for name, first, second, third, fourth, pattern in vectors:
            if name not in matches:
                continue
            original = {address: bytearray(data) for address, data in base.items()}
            if name == 'saved_feature_collect' and third:
                skills = save[0x1e8 + (pattern % 100) * 132 + 122:0x1e8 + (pattern % 100) * 132 + 132] if label == 'measured' else bytes([1, pattern & 255]) * 5
                write(original, SKILLS, skills)
            values = bytes(64) if pattern == 0 else bytes([first & 255]) * 64 if pattern == 1 else bytes((index * 7 + first) & 255 for index in range(64))
            write(original, LIST, values)
            memory = {address: bytearray(data) for address, data in original.items()}
            result = expected(memory, ekt_data, skill_data, feat_data, name, first, second, third, fourth, skill_count, feature_count)
            if name == 'saved_feature_collect':
                maximum_output = max(maximum_output, result)
            row, code = matches[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (first, second, third, fourth)):
                    machine.reg_write(register, value & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Feature bounds', label, name, first, second, third, pattern))
                if machine.reg_read(UC_ARM_REG_R0) != result & 0xffffffff:
                    raise AssertionError(('Feature return differs', label, name, first, second, third, pattern, machine.reg_read(UC_ARM_REG_R0), result))
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        raise AssertionError(('Feature output/list/table/input/guard RAM differs', label, name, first, second, third, pattern))
                calls += 1
            cases += 1
    if maximum_output != 54:
        raise AssertionError('Maximal bounded feature fixture did not reach54 entries')
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedNativeTableFeatureLists': True, 'platformStubs': {}, 'assetSha256': {name: sha(blob) for name, blob in blobs.items()}, 'maximumObservedOutputCount': maximum_output, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Collector clears64 output bytes and appends nonzero innate feature IDs according to native category/variant-offset limits.', 'Five saved skill slots contribute up to ten features each when allocated points meet each native threshold.', 'Feature flag4 bypasses duplicate/parent exclusion; other features are rejected when themselves or their declared parent byte already occur.', 'A reverse parent lookup returning an index above0 removes the first matching predecessor before appending the new feature.', 'Innate duplicates are preserved, feature occurrences stop at zero or64 bytes, and skill table absence is handled by the native getter.', 'A maximal synthetic valid-category fixture reaches54 entries:four innate plus50 skill features, leaving ten cleared output bytes.'], 'limitations': ['Only native EKT categories0/1/2 are exercised; the original collector has no defined maximum assignment for other categories.', 'No feature names or complete gameplay effects are inferred from raw native feature IDs.', 'Current output capacity is64; exhaustive legal allocation bounds and all possible future table edits remain outside this proof.', 'All callees execute without platform/gameplay substitution; no original asset or save is changed.']}
