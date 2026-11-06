import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD

MASK = 0xFFFFFFFF


def quotient(value, divisor):
    return abs(value) // divisor * (-1 if value < 0 else 1)


def recipes():
    rows = [dict(action=action, actorPointer=0, targetPointer=MASK) for action in
            (-2147483648, -1, 0, 42, 44, 150, 153, 247, 249, 0x10097, 2147483647)]
    rows += [dict(action=248, targetSecond=raw, actorPointer=0) for raw in (-32768, -2, -1, 0, 1, 32767)]
    rows += [dict(action=43, targetMaximum=raw, initialRng=seed, actorPointer=MASK)
             for raw, seed in product((-32768, -1, 0, 1, 900, 32767), (0, MASK))]
    rows += [dict(action=152, targetCurrent=current, flag=flag, targetSide=side, initialRng=seed, actorPointer=0)
             for current, flag, side, seed in product((-32768, -1, 0, 1, 1000, 32767), (0, 1, 255), (0, 1, 255), (0, MASK))]
    rows += [dict(action=151, actorCurrent=current, targetCurrent=target, kind=kind, flag=flag, targetSide=side, initialRng=seed)
             for current, target, kind, flag, side, seed in product((-32768, 0, 1000, 32767), (0, 1, 1000), (0, 1, 128), (0, 1), (0, 1), (0, MASK))]
    return rows


def vectors(blobs, main):
    flag_address = int.from_bytes(main[0x655E4:0x655E8], 'little') + 12
    output = []
    for index, row in enumerate(recipes()):
        action, flag, side = row['action'], row.get('flag', 0), row.get('targetSide', 0)
        actor_pointer, target_pointer = row.get('actorPointer', ATTACKER), row.get('targetPointer', TARGET)
        actor, target, record = bytearray(1088), bytearray(1088), bytearray(192)
        struct.pack_into('<I', actor, 0x1E8, ATTACKER_RECORD)
        struct.pack_into('<I', target, 0x1E8, TARGET_RECORD)
        struct.pack_into('<h', actor, 0x1F0, row.get('actorCurrent', 0))
        struct.pack_into('<h', target, 0x1F0, row.get('targetCurrent', 0))
        struct.pack_into('<h', target, 0x1F2, row.get('targetSecond', 0))
        struct.pack_into('<h', target, 0x21E, row.get('targetMaximum', 0))
        struct.pack_into('<h', record, 0x2A, row.get('kind', 0))
        target[0x31E] = side
        state, draws, protocols = row.get('initialRng', 0), [], []

        def random_value(limit):
            nonlocal state
            state = (state * 0x41C64E6D + 0x3039) & MASK
            value = (state >> 16) % limit if limit > 0 else 0
            draws.append((limit, value))
            return value

        expected = 0
        if action in (151, 152):
            protocols.append(dict(address=0x020655D8, returnWord=flag))
        if action == 248:
            raw = row['targetSecond']
            expected = quotient(raw + 2, 3) & MASK
            protocols.append(dict(address=0x021DBD30, arguments=[target_pointer], returnWord=raw & MASK))
        elif action == 43:
            maximum = min(row['targetMaximum'], 9999)
            expected = (quotient(maximum, 4) + random_value(6) + 5) & MASK
            protocols.append(dict(address=0x021DBCF0, arguments=[target_pointer], returnWord=maximum & MASK))
        elif action == 152 and not (flag and side == 1):
            current = row['targetCurrent']
            expected = (quotient(current * (random_value(31) + 30), 100) + 1) & MASK
            protocols.append(dict(address=0x021DBD24, arguments=[target_pointer], returnWord=current & MASK))
        elif action == 151 and not (flag and side == 1):
            current, kind = row['actorCurrent'], row['kind']
            bits = struct.unpack_from('<H', blobs['EnmyKindTbl.bin'], 8 + kind * 100 + 4)[0]
            denominator = (bits >> 8 & 15) // 3
            numerator = quotient(current, 30) + 25
            rate = quotient(numerator, denominator) if denominator else numerator
            success = int(random_value(100) < rate)
            protocols += [dict(address=0x021DBD24, arguments=[actor_pointer], returnWord=current & MASK),
                          dict(address=0x02044CDC, arguments=[kind], returnWord=denominator),
                          dict(address=0x02026144, arguments=[numerator & MASK, denominator], returnWord=rate & MASK),
                          dict(address=0x02210AD0, arguments=[actor_pointer, 100, rate & MASK], returnWord=success)]
            if success:
                expected = max(row['targetCurrent'] - 1, 1)
                protocols.append(dict(address=0x021DBD24, arguments=[target_pointer], returnWord=row['targetCurrent'] & MASK))
        output.append(dict(**row, physicalR0=expected, arguments=[actor_pointer, target_pointer, action], seed=1790000 + index,
                           draws=draws, protocols=protocols,
                           memory=[(ATTACKER, bytes(actor)), (TARGET, bytes(target)), (ATTACKER_RECORD, bytes(192)), (TARGET_RECORD, bytes(record)),
                                   (0x020DDD40, bytes(4)), (0x020F69E8, bytes(4)), (flag_address, bytes([flag])),
                                   (0x020F6044, struct.pack('<I', row.get('initialRng', 0)))],
                           patches=[(0x020F6044, struct.pack('<I', state))]))
    return output
