import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD

MASK = 0xFFFFFFFF
VALUES = (0, 1, 5, 101, 9999, MASK, 0x80000000, 0x7FFFFFFF)
MODES = {17: 1, 18: 2, 19: 3, 20: 4, 21: 5, 22: 6, 70: 24, 250: 28}
ORDER = [43, 87, 88, 57, 243, 244, 245, 195, 191, 246, 194, 247, 248, 249, 193, 196, 192, 73, 38, 71, 50]
LIMITS = {skill: (10, 1) for skill in (57, 243, 244, 245, 191, 246)}
LIMITS.update({skill: (100, 5) for skill in (195, 194, 247, 248, 249, 193, 196)})
FLAG, OUTPUT, LIST, STATUS_VIEW = 0x02356000, 0x02356100, 0x02358000, 0x0237A000
ROSTERS = (0x02236F6C, 0x022362AC)


def signed(value):
    word = value & MASK
    return word - 0x100000000 if word & 0x80000000 else word


def divide(value, divisor):
    return abs(value) // divisor * (-1 if value < 0 else 1)


def scale(value, factor, divisor):
    return divide(signed(value * factor), divisor) & MASK


def terminated(values):
    output = []
    for value in values[:64]:
        if value == 0:
            break
        output.append(value)
    return output


def scalar_vectors(address, blobs):
    lists = [[], [0, 31, 17], [31], [32], [31, 32], [32, 31], [31, 0, 32], [99],
             [31] * 64, [32] * 64, [31, 32] * 32, list(MODES), [17] * 64]
    lists += [[skill] for skill in MODES]
    combinations = product(lists, VALUES, range(6)) if address == 0x02210888 else product(lists, VALUES, (0, 1, 6, 24, 28))
    output = []
    for index, (skills, value, control) in enumerate(combinations):
        action, primary, secondary = 253, control, (0, 1, 28)[index % 3]
        actor, target, saved = bytearray(1088), bytearray(1088), bytearray(192)
        struct.pack_into('<I', actor, 0x1E8, ATTACKER_RECORD)
        struct.pack_into('<I', target, 0x1E8, TARGET_RECORD)
        payload = bytes((skills + [0] * 64)[:64])
        saved[0x46:0x86], saved[0x86] = payload, 31
        kind = bytearray(blobs['EnmyKindTbl.bin'][8:108])
        struct.pack_into('<H', kind, 4, (control * 3 << 8) if address == 0x02210888 else 0)
        metadata = bytearray(blobs['ActTbl.bin'][8 + action * 40:8 + (action + 1) * 40])
        metadata[0x1F], metadata[0x20] = primary, secondary
        result, protocols = value, []
        for skill in terminated(skills):
            if address == 0x02210748 and skill in MODES:
                mode = MODES[skill]
                updated = scale(result, 5, 4) if mode in (primary, secondary) else result
                protocols.append(dict(address=0x0220EE3C, arguments=[action, result, mode], returnWord=updated))
                result = updated
            elif address == 0x02210888 and skill in (31, 32):
                protocols.append(dict(address=0x02044CDC, arguments=[0], returnWord=control))
                if skill == 31 and control == 1:
                    result = scale(result, 5, 4)
                elif skill == 31 and control == 2:
                    result = scale(result, 3, 2)
                elif skill == 32 and control == 0:
                    result = scale(result, 12, 10)
        output.append(dict(skills=skills, initialValue=hex(value), classificationOrPrimary=control, secondary=secondary,
            physicalR0=result, seed=2010000 + index, draws=[], protocols=protocols,
            arguments=[LIST, action, value] if address == 0x02210748 else [ATTACKER, TARGET, value],
            memory=[(ATTACKER, bytes(actor)), (TARGET, bytes(target)), (ATTACKER_RECORD, bytes(saved)), (TARGET_RECORD, bytes(192)),
                    (LIST, payload + bytes([17])), (0x02300000, bytes(kind)), (0x02320000 + action * 40, bytes(metadata))], patches=[]))
    return output


def collector_recipes():
    rows = [dict(skills=skills, capacity=capacity, initial=initial, side=side, ready=True, counter=counter, flag=0,
                 opposing_stage=1, own_stage=1) for skills, capacity, initial, side, counter
            in product([[skill] for skill in ORDER] + [ORDER, ORDER[::-1], [], [57] * 64, [57, 0, 196]],
                       (0, 1, 3, MASK), (0, MASK), (0, 1), (0, 1))]
    rows += [dict(skills=ORDER, capacity=3, initial=initial, side=side, ready=ready, counter=counter,
                  flag=flag, opposing_stage=opposing, own_stage=own)
             for initial, side, ready, counter, flag, opposing, own
             in product((0, MASK), (0, 1, 255), (False, True), (-2, -1, 0, 1, 0x7FFFFFFF, 0x80000000),
                        (0, MASK), (0, 1), (0, 1))]
    return rows


def collector_vectors(blobs, main, overlay):
    counter_base = struct.unpack_from('<I', main, 0x02044420 - 0x02000000)[0]
    descriptor = struct.unpack_from('<I', overlay, 0x021D8E1C - 0x021D7240)[0]
    if counter_base != 0x020F69C4 or descriptor != 0x02232B20:
        raise ValueError('Native counter/status-view literals differ')
    output = []
    for index, recipe in enumerate(collector_recipes()):
        skills, initial = terminated(recipe['skills']), recipe['initial']
        state, draws, protocols, emitted = initial, [], [], []
        ready, flag, capacity = recipe['ready'], recipe['flag'], recipe['capacity']

        def query(skill):
            count = skills.count(skill)
            protocols.append(dict(address=0x0207B674, arguments=[skill, ATTACKER_RECORD + 0x46], returnWord=count))
            return count > 0

        def eligible():
            protocols.append(dict(address=0x021DC108, arguments=[ATTACKER], returnWord=int(ready)))
            return ready

        def draw(limit):
            nonlocal state
            state = (state * 0x41C64E6D + 0x3039) & MASK
            value = (state >> 16) % limit
            draws.append((limit, value))
            return value

        def chance(limit, threshold):
            start = len(protocols)
            success = draw(limit) < threshold
            query(41 if success else 40)
            protocols.insert(start, dict(address=0x02210AD0, arguments=[ATTACKER, limit, threshold], returnWord=int(success)))
            return success

        own = int(recipe['side'] != 0)
        if query(43) and eligible() and flag == 0 and recipe['opposing_stage'] > 0 and capacity > 0:
            flag = 1
            emitted.append(43)
        if query(87) and eligible():
            result = int(recipe['opposing_stage'] > 0)
            protocols.append(dict(address=0x0220FF30, arguments=[1 - own, 4], returnWord=result))
            if result and draw(10) < 2 and len(emitted) < capacity:
                emitted.append(87)
        if query(88) and eligible():
            result = int(recipe['own_stage'] != 0)
            protocols.append(dict(address=0x0220FF30, arguments=[own, 1], returnWord=result))
            if result and draw(10) < 2 and len(emitted) < capacity:
                emitted.append(88)
        for skill in ORDER[3:]:
            if not query(skill) or not eligible():
                continue
            if skill in LIMITS:
                limit, threshold = LIMITS[skill]
                success = draw(limit) < threshold
            else:
                if skill in (38, 71):
                    protocols.append(dict(address=0x02044414, arguments=[], returnWord=recipe['counter'] & MASK))
                    number = signed(recipe['counter'])
                    if number - divide(number, 2) * 2 != int(skill == 71):
                        continue
                success = chance(100 if skill == 192 else 10, 10 if skill == 192 else 1 if skill == 73 else 2)
            if success and len(emitted) < capacity:
                emitted.append(skill)
        actor, saved = bytearray(1088), bytearray(192)
        struct.pack_into('<I', actor, 0x1E8, ATTACKER_RECORD)
        actor[0x31C], actor[0x31E], actor[0x236] = 1, recipe['side'], 0 if ready else 1
        saved[0x46:0x86], saved[0x86] = bytes((recipe['skills'] + [0] * 64)[:64]), 196
        memory = [(ATTACKER, bytes(actor)), (ATTACKER_RECORD, bytes(saved)),
                  (FLAG, struct.pack('<I', recipe['flag'])), (OUTPUT, bytes([0xA5]) * 32),
                  (0x020F6044, struct.pack('<I', initial)), (counter_base + 0x1C, struct.pack('<I', recipe['counter'] & MASK))]
        for side in (0, 1):
            roster = bytearray(3 * 1088)
            for slot in range(3):
                record = 0x02352000 + side * 0x400 + slot * 0x100
                struct.pack_into('<I', roster, slot * 1088 + 0x1E8, record)
                roster[slot * 1088 + 0x31C] = 1
                stage = recipe['own_stage'] if side == own else recipe['opposing_stage']
                struct.pack_into('<b', roster, slot * 1088 + 0x234, stage)
                memory.append((record, bytes(192)))
            memory.append((ROSTERS[side], bytes(roster)))
        view = bytearray(8 + 60 * 14)
        struct.pack_into('<I', view, 4, 60)
        view[8 + 8 * 14], view[8 + 8 * 14 + 3], view[8 + 8 * 14 + 8] = 1, 5, 2
        memory += [(STATUS_VIEW, bytes(view)), (descriptor + 8, struct.pack('<I', STATUS_VIEW))]
        final_list = bytes(emitted) + bytes([0xA5]) * (32 - len(emitted))
        output.append(dict(**recipe, emitted=emitted, physicalR0=len(emitted), seed=2040000 + index, protocols=protocols, draws=draws,
            arguments=[ATTACKER, FLAG, OUTPUT, capacity], memory=memory,
            patches=[(FLAG, struct.pack('<I', flag)), (OUTPUT, final_list), (0x020F6044, struct.pack('<I', state))]))
    return output
