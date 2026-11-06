import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD

MASK = 0xFFFFFFFF
VALUES = (0, 1, 2, 5, 6, 7, 101, 9999, MASK, 0xFFFFFF9B, 0x80000000, 0x7FFFFFFF)
SPECIES_FLAGS = 0x02300004


def signed(value):
    return (value & MASK) - (0x100000000 if value & 0x80000000 else 0)


def divide(numerator, denominator):
    quotient = abs(numerator) // abs(denominator)
    return -quotient if (numerator < 0) != (denominator < 0) else quotient


def scale(value, multiplier, denominator):
    return divide(signed(value * multiplier), denominator) & MASK


def recipes(address):
    rows = [dict(action=action, intent_action=action, value=VALUES[action % 12], stage=action % 5, counter=action % 256,
                  raw_flag=action % 2, denominator=(0, 1, 2, 255)[action % 4], control=(0, 1, 2, 3, MASK)[action % 5],
                  side=action % 2, slot=action % 3, scene=(0, 7)[action % 2], original=True) for action in range(256)]
    if address == 0x021EF878:
        rows += [dict(value=value, flags=flags, raw_flag=flag, initial=initial) for value, flags, flag, initial
                 in product(VALUES, (0, 0x80), (0, 1, 128, 255), (0, MASK))]
    elif address == 0x021EFB14:
        rows += [dict(value=value, mode=mode, category=category) for value, mode, category in product(VALUES, (0, 1, 15), (0, 1, 2, 5))]
    elif address == 0x021EFB88:
        rows += [dict(value=value, mode=1, denominator=denominator, control=control, initial=initial)
                 for value, denominator, control, initial in product(VALUES, (0, 1, 2, 3, 255), (0, 1, 2, 3, MASK), (0, MASK))]
    elif address == 0x021EFBF4:
        rows += [dict(value=value, flags=0x20000000, stage=stage, side=side, scene=scene)
                 for value, stage, side, scene in product(VALUES, range(-4, 5), (0, 1), (0, 7))]
    elif address == 0x021EFC7C:
        rows += [dict(value=value, flags=0x20000000, stage=stage, counter=counter)
                 for value, stage, counter in product(VALUES, (-128, -1, 0, 1, 4, 127), (0, 1, 4, 5, 254, 255))]
    elif address == 0x021EFCF8:
        rows += [dict(value=value, mode=mode, category=category, flags=flags)
                 for value, mode, category, flags in product(VALUES, (0, 1, 4, 5, 6, 7, 15), (0, 1, 2, 3, 5), (0, 0x40000000))]
    elif address == 0x021F0254:
        rows += [dict(value=value, intent_mode=2, intent_count=count, flags=0x40, side=side, slot=slot)
                 for value, count, side, slot in product(VALUES, (-32768, -1, 0, 1, 2, 3, 32767), (0, 1), (0, 1, 2))]
        rows += [dict(value=value, intent_mode=mode, intent_count=count, flags=flags)
                 for value, count, (mode, flags) in product(VALUES, (-32768, 32767), ((0, 0), (0, 0x40), (1, 0), (1, 0x40), (15, 0), (15, 0x40), (2, 0)))]
    elif address == 0x021F040C:
        rows += [dict(value=value, flags=flags, stage=stage)
                 for value, flags, stage in product(VALUES, (0, 0x800000), (-128, -4, -1, 0, 1, 3, 4, 5, 127))]
    if address in (0x021EF878, 0x021EFBF4, 0x021EFC7C, 0x021F040C):
        rows += [dict(value=MASK, flags=0, opaque=pointer) for pointer in (0, MASK)]
    if address in (0x021EFB88, 0x021EFCF8):
        rows += [dict(value=MASK, mode=0, opaque=pointer) for pointer in (0, MASK)]
    return rows


def vectors(address, blobs, overlay):
    output = []
    intent_bases = struct.unpack_from('<II', overlay, 0x021E81E8 - 0x021D7240)
    table_a, table_b = struct.unpack_from('<II', overlay, 0x021EFC70 - 0x021D7240)
    if intent_bases != (0x02238D1C, 0x02238D2E) or (table_a, table_b) != (0x0222DF40, 0x0222DF4C):
        raise ValueError('Native data literal identities differ')
    for index, row in enumerate(recipes(address)):
        action = row.get('action', 254 if address == 0x021F0254 else 253)
        intent_action = row.get('intent_action', 253)
        metadata = bytearray(blobs['ActTbl.bin'][8 + action * 40:8 + (action + 1) * 40])
        selected = bytearray(blobs['ActTbl.bin'][8 + intent_action * 40:8 + (intent_action + 1) * 40])
        if 'flags' in row:
            struct.pack_into('<I', metadata, 0, row['flags'])
        if 'mode' in row:
            struct.pack_into('<H', metadata, 8, row['mode'])
        if 'intent_mode' in row:
            struct.pack_into('<H', selected, 8, row['intent_mode'])
            struct.pack_into('<h', selected, 0x10, row['intent_count'])
        flags, mode = struct.unpack_from('<I', metadata)[0], struct.unpack_from('<H', metadata, 8)[0] & 15
        actor, target = bytearray(1088), bytearray(1088)
        for data, saved in ((actor, ATTACKER_RECORD), (target, TARGET_RECORD)):
            struct.pack_into('<I', data, 0x1E8, saved)
        side, slot, scene = row.get('side', index % 2), row.get('slot', index % 3), row.get('scene', 0)
        stage, counter, raw_flag, denominator = row.get('stage', 0), row.get('counter', 0), row.get('raw_flag', 0), row.get('denominator', 0)
        actor[0x31E], actor[0x31F], actor[0x234], actor[0x1FC], actor[0x246], actor[0x356] = side, slot, stage & 255, counter, raw_flag, denominator
        memory = [(ATTACKER, bytes(actor)), (TARGET, bytes(target)), (ATTACKER_RECORD, bytes(192)), (TARGET_RECORD, bytes(192)),
                  (0x020F69E8, struct.pack('<I', scene)), (0x020DDD40, bytes(4))]
        if not row.get('original'):
            memory.append((0x02320000 + action * 40, bytes(metadata)))
        original_flags = struct.unpack_from('<H', blobs['EnmyKindTbl.bin'], 12)[0]
        category = (original_flags >> 8 & 15) // 3
        if 'category' in row:
            category = row['category']
            memory.append((SPECIES_FLAGS, struct.pack('<H', original_flags & 0xF0FF | category * 3 << 8)))
        value, control, initial = row.get('value', 101), row.get('control', 0), row.get('initial', (0, MASK, 0xA5821347)[index % 3])
        expected, state, draws, protocols = value, initial, [], []

        def random_word(limit):
            nonlocal state
            state = (state * 0x41C64E6D + 0x3039) & MASK
            result = (state >> 16) % limit
            draws.append((limit, result))
            return result

        if address == 0x021EF878:
            if flags & 0x80 and raw_flag:
                expected = scale(value, random_word(6) + 20, 10)
        elif address == 0x021EFB14:
            protocols = [dict(address=0x021DB9E0, arguments=[ATTACKER], returnWord=category)]
            if category == 1 and mode == 1:
                expected = scale(value, 15, 10)
        elif address == 0x021EFB88:
            if mode == 1 and denominator > 1:
                quotient = divide(signed(value), denominator)
                protocols.append(dict(address=0x02026144, arguments=[value, denominator], returnWord=quotient & MASK))
                if quotient > 2:
                    draw = random_word(4) if control in (0, 3) else 3 if control == 2 else 0
                    protocols.append(dict(address=0x0207B94C, arguments=[4, control], returnWord=draw))
                    quotient = max(quotient + draw - 1, 0)
                expected = quotient & MASK
        elif address == 0x021EFBF4:
            if flags & 0x20000000 and stage:
                if side:
                    protocols.append(dict(address=0x020444A8, returnWord=int(scene == 7)))
                table = table_a if side == 0 or scene == 7 else table_b
                factor = overlay[table - 0x021D7240 + stage + 4]
                expected = scale(value, factor, 10)
        elif address == 0x021EFC7C:
            if flags & 0x20000000:
                protocols.append(dict(address=0x02210BA8, arguments=[TARGET], returnWord=0))
                if stage > 0:
                    addend = stage * ((counter * 4096) // 5 + 4096) // 4096
                    expected = value + addend & MASK
        elif address == 0x021EFCF8:
            if mode in (5, 6) and not flags & 0x40000000:
                protocols.append(dict(address=0x021DB9E0, arguments=[ATTACKER], returnWord=category))
                if category == 1:
                    expected = scale(value, 5, 4)
                elif category == 2:
                    expected = scale(value, 15, 10)
        elif address == 0x021F0254:
            intent_address = intent_bases[int(side != 0)] + 6 * slot
            memory.append((intent_address, struct.pack('<HBBBB', intent_action, 0, 0, 0, 0)))
            if intent_action != action or 'intent_mode' in row:
                memory.append((0x02320000 + intent_action * 40, bytes(selected)))
            selected_mode = struct.unpack_from('<H', selected, 8)[0] & 15
            selected_count = struct.unpack_from('<h', selected, 0x10)[0]
            count = selected_count if selected_mode == 2 and flags & 0x40 else 0
            protocols = [dict(address=0x021EEF98, arguments=[ATTACKER, action], returnWord=count & MASK),
                         dict(address=0x021E81D0, arguments=[side, slot], returnWord=intent_address)]
            if count > 1:
                numerator = signed(value + count - 1)
                expected = divide(numerator, count) & MASK
                protocols.append(dict(address=0x02026144, arguments=[numerator & MASK, count], returnWord=expected))
        elif address == 0x021F040C:
            if flags & 0x800000 and stage == 4:
                expected = scale(value, 7, 10)
        else:
            raise ValueError('Unsupported stage identity')
        memory.append((0x020F6044, struct.pack('<I', initial)))
        actor_address = row.get('opaque', ATTACKER)
        arguments = [value, action, actor_address]
        if address == 0x021EFB88:
            arguments.append(control)
        if address == 0x021EFC7C:
            arguments.append(row.get('opaque', TARGET))
        output.append(dict(**row, effectiveAction=action, effectiveMode=mode, derivedCategory=category, physicalR0=expected,
            arguments=arguments, memory=memory, patches=[(0x020F6044, struct.pack('<I', state))], seed=1800000 + index,
            draws=draws, protocols=protocols))
    return output
