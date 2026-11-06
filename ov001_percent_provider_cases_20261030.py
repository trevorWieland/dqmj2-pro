import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD

MASK = 0xFFFFFFFF
TEAMS = (0x02236F6C, 0x022362AC, 0x022355EC, 0x02237C2C)
VALUES = (0, 1, 101, 9999, 0xFFFFFFFF, 0xFFFFFF9B, 0x80000000, 0x7FFFFFFF)


def signed(word):
    return (word & MASK) - (0x100000000 if word & 0x80000000 else 0)


def scaled(value, multiplier, divisor):
    product_word = signed((value * multiplier) & MASK)
    quotient = -((-product_word) // divisor) if product_word < 0 else product_word // divisor
    return quotient & MASK


def kinds(blob):
    output = {}
    for index in range((len(blob) - 8) // 100):
        group = struct.unpack_from('<H', blob, 8 + index * 100 + 4)[0] >> 4 & 15
        output.setdefault(group, index)
    if not all(group in output for group in range(9)):
        raise ValueError('Measured species groups changed')
    return output


def category_match(blob, kind, secondary):
    group = struct.unpack_from('<H', blob, 8 + kind * 100 + 4)[0] >> 4 & 15
    bit = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128}.get(group, 0)
    return int(bool(secondary & bit))


def state(side, kind, actor_flag=0, item=0, slot=0, eligibility=None):
    actor, target, record = bytearray(1088), bytearray(1088), bytearray(192)
    struct.pack_into('<I', actor, 0x1E8, ATTACKER_RECORD)
    struct.pack_into('<I', target, 0x1E8, TARGET_RECORD)
    struct.pack_into('<h', record, 0x2A, kind)
    actor[0x31E], target[0x31E], target[0x31F] = 1 - side % 2, side, slot
    actor[0x236], actor[0x1FD] = actor_flag, item
    memory = [(ATTACKER, bytes(actor)), (TARGET, bytes(target)), (ATTACKER_RECORD, bytes(192)), (TARGET_RECORD, bytes(record))]
    rows = eligibility or ((1, 0, 0),) * 3
    preceding = 0
    for index, (enabled, marker, record_flag) in enumerate(rows):
        row, saved = bytearray(1088), bytearray(192)
        pointer = 0x02350200 + 0x100 * index
        row[0x31C], row[0x31F], row[0x1FF], saved[0xAC] = enabled, index, marker, record_flag
        struct.pack_into('<I', row, 0x1E8, pointer)
        memory += [(TEAMS[side] + 1088 * index, bytes(row)), (pointer, bytes(saved))]
    for index, (enabled, marker, record_flag) in enumerate(rows):
        if enabled and not marker and not record_flag:
            if index == slot:
                break
            preceding += 1
    return memory, preceding


def action_record(blob, action, override):
    record = bytearray(blob[8 + action * 40:8 + (action + 1) * 40])
    if override is not None:
        flags, secondary, mode, scalar = override
        struct.pack_into('<I', record, 0, flags)
        struct.pack_into('<H', record, 4, secondary)
        struct.pack_into('<H', record, 8, mode)
        struct.pack_into('<h', record, 0x12, scalar)
    return record


def eligible_vectors(blobs):
    groups, output = kinds(blobs['EnmyKindTbl.bin']), []
    rows = [dict(action=action, slot=slot, value=VALUES[(action + slot) % len(VALUES)], kind=groups[action % 9], actor_flag=1)
            for action, slot in product(range(256), (0, 1, 2, 255))]
    scenarios = [(253, 0, 0, 0, 1, 0, None, 0, groups[0]),
                 (253, 0x08000000, 1, 0, 128, 0, None, 0, groups[1]),
                 (253, 0x08000000, 0, 0, 255, 0, None, 0, groups[1]),
                 (253, 0, 0, 0x1001, 0, 0, None, 0, groups[0]),
                 (253, 0, 0, 1, 0, 0, None, 0, groups[0]),
                 (253, 0, 0x100, 0x1001, 1, 0, None, 0, groups[0])]
    scenarios += [(action, 0, 0, 0, 0, 255, 4, control, groups[0])
                  for action, control in product((0, 203, 204), (0, 1, MASK))]
    for scenario, slot, value in product(scenarios, (0, 1, 2, 255), VALUES):
        action, flags, secondary, mode, actor_flag, item, item_type, control, kind = scenario
        rows.append(dict(action=action, slot=slot, value=value, kind=kind, actor_flag=actor_flag, item=item,
                         item_type=item_type, control=control, override=(flags, secondary, mode, 0)))
    for rowspec, slot in product((((0, 0, 0), (1, 0, 0), (1, 0, 0)),
                                  ((1, 255, 0), (255, 0, 0), (1, 0, 0)),
                                  ((1, 0, 255), (1, 0, 0), (1, 0, 0)),
                                  ((0, 0, 0),) * 3), (0, 1, 2, 255)):
        rows.append(dict(action=253, slot=slot, value=901, kind=groups[0], actor_flag=1,
                         eligibility=rowspec, override=(0, 0, 0, 0)))
    rows += [dict(action=253, slot=0, value=MASK, kind=groups[0], actor_flag=0, opaque=pointer,
                  override=(0, 0x100, 0, 0)) for pointer in (0, MASK)]
    for index, row in enumerate(rows):
        action, side, kind = row['action'], index % 4, row['kind']
        override, item = row.get('override'), row.get('item', 0)
        metadata = action_record(blobs['ActTbl.bin'], action, override)
        flags, secondary, mode = struct.unpack_from('<I', metadata)[0], struct.unpack_from('<H', metadata, 4)[0], struct.unpack_from('<H', metadata, 8)[0]
        item_type = row.get('item_type')
        if item_type is None:
            item_type = blobs['ItemTbl.bin'][8 + 88 * item + 0x2D]
        memory, preceding = state(side, kind, row['actor_flag'], item, row['slot'], row.get('eligibility'))
        control, value = row.get('control', 0), row['value']
        active = not secondary & 0x100 and ((item_type == 4 and action in (0, 203, 204) and control == 0) or
                                          (mode & 15 == 1 and mode >> 12 == 1) or row['actor_flag'] != 0)
        match, factor, protocols = category_match(blobs['EnmyKindTbl.bin'], kind, secondary), None, []
        if active:
            protocols.append(dict(address=0x021DCA60, arguments=[TARGET], returnWord=preceding))
            if flags & 0x08000000:
                protocols.append(dict(address=0x021EF398, arguments=[action, TARGET], returnWord=match))
            factors = (120, 70, 35) if flags & 0x08000000 and match else (70, 35, 15) if flags & 0x08000000 else (90, 50, 25)
            factor = factors[preceding] if preceding < 3 else None
        expected = scaled(value, factor, 100) if factor is not None else value
        if override is not None:
            memory.append((0x02320000 + action * 40, bytes(metadata)))
        if row.get('item_type') is not None:
            memory.append((0x02330000 + 88 * item + 0x2D, bytes([item_type])))
        initial = (0xA5821347 + index) & MASK
        memory.append((0x020F6044, struct.pack('<I', initial)))
        output.append(dict(**row, suppliedSide=side, precedingEligible=preceding, metadataShaSource='original' if override is None else 'runtime-copy',
            physicalR0=expected, arguments=[value, action, row.get('opaque', ATTACKER), row.get('opaque', TARGET), control],
            memory=memory, patches=[], seed=1750000 + index, draws=[], protocols=protocols))
    return output


def metadata_vectors(blobs):
    groups, output = kinds(blobs['EnmyKindTbl.bin']), []
    rows = [dict(action=action, value=value, kind=groups[action % 9]) for action, value in product(range(256), VALUES)]
    scenarios = [(0x08000000, secondary, mode, 0) for secondary, mode in product((0, 1), (0, 1, 2, 0x1001))]
    scenarios += [(flags, 0, mode, scalar) for flags, mode, scalar in product((0, 1), (0, 1), (-32768, -1, 0, 1, 0x271C, 32767))]
    for override, value, initial in product(scenarios, VALUES, (0, MASK)):
        rows.append(dict(action=253, value=value, kind=groups[1], override=override, initial=initial))
    for index, row in enumerate(rows):
        action, value, kind, override = row['action'], row['value'], row['kind'], row.get('override')
        record = action_record(blobs['ActTbl.bin'], action, override)
        flags, secondary, mode = struct.unpack_from('<I', record)[0], struct.unpack_from('<H', record, 4)[0], struct.unpack_from('<H', record, 8)[0]
        scalar = struct.unpack_from('<h', record, 0x12)[0]
        memory, unused = state(index % 4, kind)
        initial, draws, protocols, expected = row.get('initial', 0xA5821347), [], [], value
        rng = initial
        if flags & 0x08000000:
            match = category_match(blobs['EnmyKindTbl.bin'], kind, secondary)
            protocols = [dict(address=0x02210BA8, arguments=[TARGET], returnWord=0),
                         dict(address=0x021EF398, arguments=[action, TARGET], returnWord=match)]
            if match:
                if mode & 15 != 1:
                    expected = scaled(value, 13, 10)
                elif mode >> 12 == 0:
                    expected = scaled(value, 27, 20)
        elif flags & 1 and mode & 15 == 1:
            if scalar == 0x271C:
                rng = (rng * 0x41C64E6D + 0x3039) & MASK
                draw = (rng >> 16) % 21
                draws = [(21, draw)]
                expected = scaled(value, draw + 20, 100)
            else:
                expected = scaled(value, scalar, 10)
        if override is not None:
            memory.append((0x02320000 + action * 40, bytes(record)))
        memory.append((0x020F6044, struct.pack('<I', initial)))
        output.append(dict(**row, metadataShaSource='original' if override is None else 'runtime-copy', physicalR0=expected,
            arguments=[value, action, (0, MASK, ATTACKER)[index % 3], TARGET], memory=memory,
            patches=[(0x020F6044, struct.pack('<I', rng))], seed=1760000 + index, draws=draws, protocols=protocols))
    return output
