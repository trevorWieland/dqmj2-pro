import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD

MASK = 0xFFFFFFFF


def signed(word):
    return word if word < 0x80000000 else word - 0x100000000


def quotient(value, divisor):
    return abs(value) // divisor * (-1 if value < 0 else 1)


def recipes():
    rows = []
    for native_id, divisor in ((0x2714, 4), (0x2715, 6), (0x271B, 2), (0x271D, 8), (0x271E, 16)):
        for raw, value, double, triple in product((-32768, -1, 0, 1, 99, 1000, 32767), (0, 0x7FFFFFFF), (0, 1), (0, 1)):
            rows.append(dict(kind='fraction', nativeId=native_id, divisor=divisor, targetRaw=raw, initial=value, double=double, triple=triple))
    for raw, maximum, control, double, triple in product((-32768, -1, 100, 32767), (-1, 500, 32767), (0, 1, 2, 3), (0, 1), (0, 1)):
        rows.append(dict(kind='difference', nativeId=0x2717, actorRaw=raw, maximumRaw=maximum, control=control, initial=0xFFFFFFFF, double=double, triple=triple))
    for extra, double, triple in product((0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF), (0, 1), (0, 1)):
        rows.append(dict(kind='extra', nativeId=0x2713, extra=extra, initial=123, double=double, triple=triple))
    for native_id, control, double, triple in product((0x2716, 0x2712, 0x2718), (0, 1, 2, 3), (0, 1), (0, 1)):
        rows.append(dict(kind='zero-or-default', nativeId=native_id, control=control, initial=123, double=double, triple=triple))
    for action, control, double, triple in product((43, 8, 78), (0, 1, 2, 3), (0, 1), (0, 1)):
        rows.append(dict(kind='original-special', originalAction=action, control=control, initial=123, double=double, triple=triple))
    for mode, value, double, triple in product((1, 0x705), (0, 0x7FFFFFFF, 0xFFFFFFFF), (0, 1), (0, 1)):
        rows.append(dict(kind='inactive', suppliedMode=mode, initial=value, double=double, triple=triple))
    return rows


def vectors(blob):
    output = []
    for index, recipe in enumerate(recipes()):
        action = recipe.get('originalAction', 253)
        side, seed = index % 2, (0, 0xFFFFFFFF, 0xA5821347)[index % 3]
        state, draws = seed, []

        def draw(limit, controlled=True):
            nonlocal state
            control = recipe.get('control', 1) if controlled else 0
            if control in (0, 3):
                state = (state * 0x41C64E6D + 0x3039) & MASK
                result = (state >> 16) % limit if limit > 0 else 0
                draws.append((limit, result))
                return result
            return limit - 1 if control == 2 else 0

        record = bytearray(blob[8 + action * 40:8 + (action + 1) * 40])
        native_id = recipe.get('nativeId', struct.unpack_from('<h', record, 0x10 + side * 4)[0])
        if 'originalAction' not in recipe:
            struct.pack_into('<h', record, 0x10, native_id)
            struct.pack_into('<h', record, 0x14, native_id)
        if native_id == 0x2718:
            struct.pack_into('<h', record, 0x12, native_id)
            struct.pack_into('<h', record, 0x16, native_id)
            record[0x18:0x1C] = bytes(4)
        if recipe['kind'] == 'inactive':
            struct.pack_into('<H', record, 8, recipe['suppliedMode'])
        actor, target = bytearray(1088), bytearray(1088)
        for data, pointer, team in ((actor, ATTACKER_RECORD, side), (target, TARGET_RECORD, 1 - side)):
            struct.pack_into('<I', data, 0x1E8, pointer)
            data[0x31C], data[0x31E] = 1, team
        struct.pack_into('<h', actor, 0x1F0, recipe.get('actorRaw', 0))
        struct.pack_into('<h', actor, 0x21C, recipe.get('maximumRaw', 500))
        struct.pack_into('<h', target, 0x1F0, recipe.get('targetRaw', 0))
        struct.pack_into('<h', target, 0x21E, 900)
        actor[0x1FC] = 7
        protocols = []
        value = recipe['initial']
        if recipe['kind'] != 'inactive':
            protocols.append(dict(address=0x021EEFF0, arguments=[side, action], returnWord=native_id))
            if recipe['kind'] == 'fraction':
                raw = recipe['targetRaw']
                protocols.append(dict(address=0x021DBD24, arguments=[TARGET], returnWord=raw & MASK))
                value = (value + quotient(raw, recipe['divisor'])) & MASK
            elif recipe['kind'] == 'difference':
                current, maximum = recipe['actorRaw'], min(recipe['maximumRaw'], 9999)
                protocols += [dict(address=0x021DBD24, arguments=[ATTACKER], returnWord=current & MASK),
                              dict(address=0x021DBCBC, arguments=[ATTACKER], returnWord=maximum & MASK)]
                random_word = draw(6)
                protocols.append(dict(address=0x0207B94C, arguments=[6, recipe['control']], returnWord=random_word))
                value = (value + maximum - current + quotient(signed(current * random_word & MASK), 100)) & MASK
            elif recipe['kind'] == 'extra':
                value = quotient(signed(recipe['extra'] * 3 & MASK), 2) & MASK
            elif recipe['kind'] == 'zero-or-default':
                if native_id in (0x2716, 0x2712):
                    address = 0x021EF224 if native_id == 0x2716 else 0x021EF0B0
                    protocols.append(dict(address=address, arguments=[ATTACKER, TARGET, action], returnWord=0))
                    value = value if native_id == 0x2716 else 0
                else:
                    protocols.append(dict(address=0x021DBE68, arguments=[ATTACKER], returnWord=1))
                    random_word = draw(1)
                    protocols += [dict(address=0x0207B974, arguments=[action, 1, side, 0], stackArguments=[recipe['control']], returnWord=native_id),
                                  dict(address=0x0207B94C, arguments=[1, recipe['control']], returnWord=random_word)]
                    value = native_id
            else:
                if action == 43:
                    value = (value + 900 // 4 + draw(6, False) + 5) & MASK
                    protocols += [dict(address=0x021EF224, arguments=[ATTACKER, TARGET, action], returnWord=(900 // 4 + draws[-1][1] + 5)),
                                  dict(address=0x021DBCF0, arguments=[TARGET], returnWord=900)]
                else:
                    value = 7 + draw(200) if action == 8 else 7 * 2 + draw(6) + 5
                    protocols.append(dict(address=0x021EF0B0, arguments=[ATTACKER, TARGET, action, recipe['control']], returnWord=value))
            if recipe['double']:
                value = value * 2 & MASK
            if recipe['triple']:
                value = quotient(signed(value * 3 & MASK), 2) & MASK
        output.append(dict(**recipe, action=action, side=side, nativeIdWord=native_id, initialRng=seed, physicalR0=value,
                           arguments=[recipe['initial'], action, ATTACKER, TARGET, recipe.get('extra', 0), recipe.get('control', 1), recipe['double'], recipe['triple']],
                           seed=1630000 + index, draws=draws, protocols=protocols,
                           memory=[(ATTACKER, bytes(actor)), (TARGET, bytes(target)), (ATTACKER_RECORD, bytes(192)), (TARGET_RECORD, bytes(192)),
                                   (0x020DDD40, bytes(4)), (0x020F69E8, bytes(4)), (0x020F6044, struct.pack('<I', seed)),
                                   (0x02320000 + action * 40, bytes(record))], patches=[(0x020F6044, struct.pack('<I', state))]))
    return output
