import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD

MASK = 0xFFFFFFFF
MODE_SKILLS = tuple((90 + index, 1 + index) for index in range(6)) + tuple((98 + index, 7 + index) for index in range(17)) + ((116, 24), (117, 28), (115, 25), (97, 27), (96, 26))
QUERY_IDS = (118,) + tuple(skill for skill, mode in MODE_SKILLS)
RANK_PAIRS = ((0, 7), (4, 5), (5, 4), (7, 255), (255, 7), (255, 255))
EXTREME_PAIRS = RANK_PAIRS + ((-1, 5), (5, -1), (-2147483648, 2147483647), (2147483647, -2147483648))


def prefix(skills):
    skills = tuple(skills[:64])
    return skills[:skills.index(0)] if 0 in skills else skills


def rank_model(primary_mode, secondary_mode, first, second, bypass, skills):
    if secondary_mode == 0:
        second = 8
    if bypass:
        return min(first, second) & MASK, []
    learned = prefix(skills)
    primary_modifier = secondary_modifier = 118 in learned
    for skill, mode in MODE_SKILLS:
        if skill in learned:
            if primary_mode == mode:
                primary_modifier = True
            elif secondary_mode == mode:
                secondary_modifier = True
    if primary_modifier:
        first = 0 if first <= 4 else 5
    if secondary_modifier:
        second = 0 if second <= 4 else 5
    protocols = [dict(address=0x0207B674, arguments=[skill, ATTACKER_RECORD + 0x46], returnWord=learned.count(skill)) for skill in QUERY_IDS]
    return min(first, second) & MASK, protocols


def direct_recipes():
    rows = []
    for (skill, mode), secondary, ranks in product(((118, 1),) + MODE_SKILLS, (0, 1, 2), RANK_PAIRS):
        second_mode = 0 if secondary == 0 else mode if secondary == 1 else mode % 28 + 1
        rows.append(dict(primary=mode, secondary=second_mode, first=ranks[0], second=ranks[1], skills=(skill,), bypass=0))
    rows += [dict(primary=mode % 28 + 1, secondary=mode, first=first, second=second, skills=(skill,), bypass=0)
             for (skill, mode), (first, second) in product(MODE_SKILLS, RANK_PAIRS)]
    rows += [dict(primary=primary, secondary=secondary, first=first, second=second, skills=(), bypass=0)
             for primary, secondary, (first, second) in product((0, 1, 28, 29, -1, -2147483648), (0, 1, 28, 29, -1), EXTREME_PAIRS)]
    mixes = ((90, 90, 118), (90, 0, 118), QUERY_IDS, (118,) * 64,
             tuple(MODE_SKILLS[index % 28][0] for index in range(64)), (1, 2, 3, 255), (90, 91), (117, 97, 96))
    rows += [dict(primary=primary, secondary=secondary, first=first, second=second, skills=skills, bypass=0)
             for skills, (primary, secondary), (first, second) in product(mixes, ((1, 1), (1, 2), (24, 28), (26, 27), (28, 0), (-1, 29)), RANK_PAIRS)]
    rows += [dict(primary=29, secondary=secondary, first=first, second=second, skills=(), bypass=bypass, record_pointer=pointer)
             for bypass, pointer, secondary, (first, second) in product((1, 128, 255), (ATTACKER_RECORD, 0, MASK), (0, 1), EXTREME_PAIRS)]
    return rows


def common_memory(row, target_record=None):
    actor, target, saved = bytearray(1088), bytearray(1088), bytearray(192)
    actor[0x261] = row.get('bypass', 0)
    struct.pack_into('<I', actor, 0x1E8, row.get('record_pointer', ATTACKER_RECORD))
    struct.pack_into('<I', target, 0x1E8, TARGET_RECORD)
    skills = tuple(row.get('skills', ()))
    if len(skills) > 64:
        raise ValueError('Native skill list exceeds its observed bound')
    saved[0x46:0x46 + len(skills)] = bytes(skills)
    saved[0x86] = 118
    return [(ATTACKER, bytes(actor)), (TARGET, bytes(target)), (ATTACKER_RECORD, bytes(saved)),
            (TARGET_RECORD, target_record or bytes(192)), (0x020F6044, struct.pack('<I', 0xA5821347))]


def direct_vectors():
    output = []
    for index, row in enumerate(direct_recipes()):
        expected, protocols = rank_model(row['primary'], row['secondary'], row['first'], row['second'], row['bypass'], row['skills'])
        output.append(dict(**row, physicalR0=expected, arguments=[ATTACKER, row['primary'], row['secondary'], row['first'], row['second']],
                           memory=common_memory(row), patches=[], seed=1840000 + index, draws=[], protocols=protocols))
    return output


def wrapper_recipes():
    rows = []
    for (skill, mode), secondary, (first, second), modifier in product(((118, 1),) + MODE_SKILLS, (0, 1, 2), RANK_PAIRS, (0, 1, MASK)):
        second_mode = 0 if secondary == 0 else mode if secondary == 1 else mode % 28 + 1
        rows.append(dict(primary=mode, secondary=second_mode, first=first, second=second, modifier=modifier, skills=(skill,), bypass=0))
    rows += [dict(primary=mode % 28 + 1, secondary=mode, first=first, second=second, modifier=modifier, skills=(skill,), bypass=0)
             for (skill, mode), (first, second), modifier in product(MODE_SKILLS, RANK_PAIRS, (1, MASK))]
    for primary, modifier, pointer in product((0, -1, -2147483648), (0, 1, MASK), (0, MASK)):
        rows.append(dict(primary=primary, secondary=1, first=255, second=7, modifier=modifier, skills=(), bypass=0, opaque=pointer))
    rows += [dict(primary=1, secondary=2, first=first, second=second, modifier=modifier, skills=skills, bypass=bypass)
             for skills, bypass, modifier, (first, second) in product(((118,) * 64, (90, 0, 118), (90, 91), ()), (0, 1, 255), (0, 1, MASK), RANK_PAIRS)]
    return rows


def wrapper_vectors(blobs, action_wrapper=False):
    output = []
    for index, row in enumerate(wrapper_recipes()):
        primary, secondary = row['primary'], row['secondary']
        if action_wrapper and primary < 0:
            continue
        record = bytearray(192)
        if primary > 0:
            record[0x86 + primary] = row['first']
            if secondary:
                record[0x86 + secondary] = row['second']
            first, second = record[0x86 + primary], record[0x86 + secondary] if secondary else 0
        else:
            first, second = row['first'], row['second']
        if primary <= 0:
            expected, protocols = 1, []
        elif row['modifier']:
            expected, queries = rank_model(primary, secondary, first, second, row['bypass'], row['skills'])
            protocols = [dict(address=0x0220E3A8, arguments=[ATTACKER, primary, secondary, first], stackArguments=[second], returnWord=expected)] + queries
        else:
            expected, protocols = min(first, second) if secondary else first, []
        actor_address = row.get('opaque', ATTACKER)
        target_address = row.get('opaque', TARGET)
        memory = common_memory(row, bytes(record))
        if action_wrapper:
            action = 253
            metadata = bytearray(blobs['ActTbl.bin'][8 + 40 * action:8 + 40 * (action + 1)])
            metadata[0x1F], metadata[0x20] = primary, secondary
            memory.append((0x02320000 + 40 * action, bytes(metadata)))
            arguments = [actor_address, target_address, action, row['modifier']]
            protocols.insert(0, dict(address=0x021F0CA0, arguments=[actor_address, target_address, primary, secondary],
                                     stackArguments=[row['modifier']], returnWord=expected))
        else:
            arguments = [actor_address, target_address, primary, secondary, row['modifier']]
        output.append(dict(**row, storedPrimary=first, storedSecondary=second, physicalR0=expected, arguments=arguments,
                           memory=memory, patches=[], seed=1850000 + index, draws=[], protocols=protocols))
    return output
