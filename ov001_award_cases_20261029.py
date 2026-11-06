import hashlib
import struct

from ndspy.rom import NintendoDSRom
from project import ROOT, configuration, sha256

CONTEXT, ROSTER, FORMATION = 0x02238CD4, 0x021BD674, 0x021BD540
ACTIVE, RESERVE, MONSTER = 0x02236F6C, 0x022355EC, 0x02300000
TABLE, LEVELS, ABILITY, BATTLE = 0x02500000, 0x02400000, 0x02410000, 0x02420000
ASSETS = ('EnmyKindTbl.bin', 'LevelUpTbl.bin', 'SkillPointTbl.bin', 'AbilityTbl.bin', 'BtlStsTbl.bin')


def read32(data, offset=0):
    return struct.unpack_from('<I', data, offset)[0]


def assets():
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM identity differs')
    rom = NintendoDSRom(config['rom'].read_bytes())
    result = {name: bytes(rom.getFileByName(name)) for name in ASSETS}
    if len(result['LevelUpTbl.bin']) != 7200 or len(result['SkillPointTbl.bin']) < 100:
        raise ValueError('Measured experience/skill table bounds differ')
    return result


def curve(blobs, species):
    identifier = blobs['EnmyKindTbl.bin'][8 + species * 100 + 0x43]
    return identifier, struct.unpack_from('<100i', blobs['LevelUpTbl.bin'], identifier * 400)


def level_cap(plus):
    return 50 if plus < 4 else 75 if plus < 10 else 100


def vectors(address):
    pools = [0, 1, 11, 12, 13, 23, 24, 25, 100, 1000, 10000, 999999]
    for index in range(48):
        yield {'seed': 202610300000 + address + index, 'ordinal': index,
               'pool': pools[index % len(pools)], 'species': [1, 4, 20, 33][(index + index // 12) % 4],
               'level': [1, 9, 10, 39, 40, 49, 50, 74, 75, 99, 100, 1][(index + index // 6) % 12],
               'plus': [0, 3, 4, 9, 10, 255][(index + index // 8) % 6], 'variant': (index + index // 12) % 3,
               'skills': (index + index // 12) % 6, 'skillPoints': [0, 1, 990, 999][index % 4],
               'invalid': index % 8, 'ioSuccess': (index + index // 12) % 4 != 3,
               'priorProgress': (index + index // 12) % 2, 'domain': 'nonnegative-bounded-pool'}
    for index, pool in enumerate([-1, -11, -12, -13, -23, -24, -25, -35, -47, -48]):
        yield {'seed': 202610300000 + address + 100 + index, 'ordinal': 48 + index,
               'pool': pool, 'species': 1, 'level': 1, 'plus': 0, 'variant': 0,
               'skills': 1, 'skillPoints': 0, 'invalid': 0, 'ioSuccess': True,
               'priorProgress': 0, 'domain': 'synthetic-negative-pool-no-signed-overflow'}


def setup(machine, blobs, vector):
    def put(address, data):
        machine.mem_write(address, bytes(data))

    def word(address, value):
        put(address, struct.pack('<I', value & 0xFFFFFFFF))

    put(TABLE, blobs['EnmyKindTbl.bin'][8:])
    put(LEVELS, blobs['LevelUpTbl.bin'])
    put(ABILITY, blobs['AbilityTbl.bin'])
    put(BATTLE, blobs['BtlStsTbl.bin'])
    put(0x02232B2C, blobs['SkillPointTbl.bin'])
    word(0x020F69F0, TABLE)
    word(0x02238D58, ABILITY)
    word(0x02232B28, BATTLE)
    word(0x020F69E4, 0)
    for index in range(18):
        word(0x021C6758 + index * 4, LEVELS + index * 400)
    put(CONTEXT, bytes(0x3C))
    word(CONTEXT + 0x30, vector['pool'])
    word(CONTEXT + 0x38, vector['pool'])
    put(ROSTER, bytes(100 * 0x84))
    put(FORMATION, struct.pack('<6I', 1001, 1002, 1003, 1004, 1005, 1006))
    put(0x021C0E20, bytes(0xE0))
    if vector['priorProgress']:
        word(0x021C0EE0, 1 << 19)
    rows = []
    for index in range(8):
        species = vector['species']
        identifier, thresholds = curve(blobs, species)
        plus = vector['plus']
        old_level = min(vector['level'], level_cap(plus))
        record = bytearray(0x84)
        struct.pack_into('<IhBB', record, 0x14, 1001 + index, species, vector['variant'], 0)
        record[0x1C] = plus
        record[0x30] = old_level
        record[0x33] = int(index == 7 and vector['invalid'] == 2)
        struct.pack_into('<IIh', record, 0x34, thresholds[old_level - 1],
                         thresholds[old_level] if old_level < 100 else 0, vector['skillPoints'])
        for slot in range(vector['skills']):
            record[0x7A + slot * 2] = slot + 1
        if index == 7 and vector['invalid'] == 3:
            struct.pack_into('<I', record, 0x14, 0)
        put(ROSTER + index * 0x84, record)
        actor_address = (ACTIVE if index < 3 else RESERVE) + index % 3 * 0x440 if index < 6 else None
        actor = None
        if actor_address is not None:
            actor = bytearray(0x440)
            monster = bytearray(0xB0)
            struct.pack_into('<I', monster, 0, 1001 + index)
            struct.pack_into('<hB', monster, 0x2A, species, vector['variant'])
            monster[0xA8], monster[0xAB] = vector['skills'], plus
            monster[0xAC] = int(index % 3 == 2 and vector['invalid'] == 1)
            monster_address = MONSTER + index * 0x100
            put(monster_address, monster)
            struct.pack_into('<I', actor, 0x1E8, monster_address)
            actor[0x1FC] = old_level
            actor[0x1FF] = int(index % 3 == 1 and vector['invalid'] == 2)
            struct.pack_into('<IIh', actor, 0x200, thresholds[old_level - 1],
                             thresholds[old_level] if old_level < 100 else 0, vector['skillPoints'])
            actor[0x31C] = int(not (index % 3 == 0 and vector['invalid'] == 3))
            actor[0x31F] = index % 3
            put(actor_address, actor)
        rows.append({'index': index, 'species': species, 'plus': plus, 'level': old_level,
                     'curve': identifier, 'thresholds': thresholds, 'record': bytes(record),
                     'actor': bytes(actor) if actor is not None else None, 'actorAddress': actor_address})
    return rows


def expected(address, rows, blobs, vector):
    outcomes, result = [], 0
    selected = rows[:3] if address == 0x021E49D0 else rows[3:6] if address == 0x021E4B34 else rows[6:]
    for row in selected:
        storage = address == 0x021E4C34
        old = row['record'] if storage else row['actor']
        eligible = bool(read32(old, 0x14)) and old[0x33] == 0 if storage else bool(old[0x31C]) and not old[0x1FF]
        if not storage and row['index'] % 3 == 2 and vector['invalid'] == 1:
            eligible = False
        if not eligible:
            outcomes.append({'row': row['index'], 'eligible': False})
            continue
        numerator = vector['pool'] + (23 if storage else 11)
        share = (abs(numerator) // (24 if storage else 12)) * (-1 if numerator < 0 else 1)
        gain = vector['pool'] if address == 0x021E49D0 else share
        experience = min(read32(old, 0x34 if storage else 0x200) + gain,
                         row['thresholds'][level_cap(row['plus']) - 1])
        level = min(level_cap(row['plus']), next((i for i, threshold in enumerate(row['thresholds']) if experience < threshold), 100))
        skill_gain = sum((vector['skills'] * blobs['SkillPointTbl.bin'][i - 1] + 4) // 5 for i in range(row['level'] + 1, level + 1))
        next_experience = row['thresholds'][level] if level < 100 else 0
        if storage and level <= row['level']:
            next_experience = read32(old, 0x38)
        elif storage and not vector['ioSuccess']:
            next_experience = 0
        outcomes.append({'row': row['index'], 'eligible': True, 'experience': experience,
                         'level': max(level, row['level']), 'nextExperience': next_experience,
                         'skillPoints': min(999, vector['skillPoints'] + skill_gain), 'rawSkillGain': skill_gain})
        if storage:
            result += 1
        elif level > row['level']:
            result = 1 if address == 0x021E49D0 else result + 1
    return result, outcomes
