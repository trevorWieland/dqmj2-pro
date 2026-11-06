import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD

MASK = 0xFFFFFFFF
OUTPUT = 0x02350600
VALUES = (0, 1, 101, 9999, MASK, 0xFFFFFF9B, 0x80000000, 0x7FFFFFFF)


def percent(value, factor):
    word = value * factor & MASK
    signed = word - (0x100000000 if word & 0x80000000 else 0)
    return (-((-signed) // 100) if signed < 0 else signed // 100) & MASK


def recipes():
    rows = [dict(value=value, tier=tier, coefficient=coefficient, output_kind=output, classification=0)
            for value, tier, coefficient, output in product(VALUES, (0, 1, 4, 5, 7, 255), (0, 1, 25, 100, 255), ('word', 'null'))]
    for index, (classification, tier, coefficient, control, mode) in enumerate(product((1, 2, 255), (0, 4, 5, 7, 255),
                                                                                   (0, 1, 50, 100, 255), (0, MASK), (0, 1))):
        features = ((0, 0), (1, 0), (0, MASK))[index % 3]
        rows.append(dict(value=VALUES[index % 8], tier=tier, coefficient=coefficient, classification=classification,
                         control=control, mode=mode, features=features, output_kind='word'))
    for index, (tier, features, mode, control, output) in enumerate(product((0, 1, 4, 5, 7), ((0, 0), (1, 0), (0, MASK), (0x80000000, 1)),
                                                                         (0, 1), (0, MASK), ('word', 'null', 'alias'))):
        rows.append(dict(value=VALUES[index % 8], tier=tier, coefficient=100, classification=1, features=features,
                         mode=mode, control=control, output_kind=output))
    rows += [dict(value=value, tier=first, second_tier=second, primary=1, secondary=2, coefficient=25,
                  classification=0, output_kind='word') for (first, second), value in product(((0, 7), (7, 0), (4, 5), (5, 4), (255, 7)), VALUES[:4])]
    rows += [dict(value=value, tier=7, coefficient=255, classification=1, primary=0, modifier=modifier,
                  output_kind=output, opaque=opaque) for value, modifier, output, opaque in product(VALUES, (0, 1, MASK),
                                                                                              ('word', 'null', 'alias'), (None, 0, MASK))]
    rows += [dict(value=MASK, tier=7, coefficient=coefficient, classification=classification, mode=15, output_kind='word')
             for classification, coefficient in product((0, 1, 255), (0, 100, 255))]
    return rows


def vectors(blobs, wrapper=False):
    output = []
    for index, row in enumerate(recipes()):
        primary, secondary = row.get('primary', 1), row.get('secondary', 0)
        if row['output_kind'] == 'alias' and primary:
            primary, secondary = 2, 3
        action, attribute, mode = 253, index % 16, row.get('mode', 0)
        metadata = bytearray(blobs['ActTbl.bin'][8 + action * 40:8 + (action + 1) * 40])
        struct.pack_into('<H', metadata, 8, mode)
        metadata[0x1F], metadata[0x20], metadata[0x22] = primary, secondary, attribute * 17
        actor, target, saved = bytearray(1088), bytearray(1088), bytearray(192)
        struct.pack_into('<I', actor, 0x1E8, ATTACKER_RECORD)
        struct.pack_into('<I', target, 0x1E8, TARGET_RECORD)
        target[0x31E] = index % 4
        saved[0x86 + primary] = row['tier']
        if secondary:
            saved[0x86 + secondary] = row.get('second_tier', 4)
        address = 0 if row['output_kind'] == 'null' else TARGET_RECORD + 0x88 if row['output_kind'] == 'alias' else OUTPUT
        initial_saved = bytes(saved)
        if row['output_kind'] == 'alias':
            saved[0x88:0x8C] = bytes(4)
        raw_tier = saved[0x86 + primary]
        if secondary:
            raw_tier = min(raw_tier, saved[0x86 + secondary])
        feature_a, feature_b = row.get('features', (0, 0))
        tier, classification, coefficient = raw_tier, row['classification'], row['coefficient']
        if classification == 1 and (feature_a or feature_b) and tier <= 4:
            tier = 0
        control, initial, draws = row.get('control', 0), (0, MASK, 0xA5821347)[index % 3], []
        rng, value = initial, row['value']
        protocols = []
        if primary:
            protocols = [dict(address=0x021F08EC, arguments=[TARGET, action], returnWord=attribute),
                         dict(address=0x02209490, arguments=[TARGET + 0x22C], returnWord=0),
                         dict(address=0x021F0D10, arguments=[ATTACKER, TARGET, action, 0], returnWord=raw_tier),
                         dict(address=0x021D90C4, arguments=[attribute, 0], returnWord=classification),
                         dict(address=0x021D908C, arguments=[attribute, tier, 0], returnWord=coefficient)]
            if classification == 0:
                value = percent(value, coefficient)
            elif mode & 15 != 1:
                rng = (rng * 0x41C64E6D + 0x3039) & MASK
                draw = rng >> 16
                draw %= 100
                draws = [(100, draw)]
                chance = int(draw < coefficient)
                protocols.append(dict(address=0x02210AD0, arguments=[ATTACKER, 100, coefficient], returnWord=chance))
                if not chance and control == 0:
                    value = 0
            if tier == 7 and not (classification != 0 and mode & 15 == 1):
                value = -value & MASK
            result_status = tier
        else:
            result_status = 0
        opaque = row.get('opaque')
        actor_address, target_address = (ATTACKER, TARGET) if opaque is None else (opaque, opaque)
        modifier = row.get('modifier', 0)
        if wrapper:
            public_modifier = modifier if not primary else (1, MASK, 0x80000000)[index % 3]
            modifier = int(public_modifier == 0)
            arguments = [row['value'], action, actor_address, target_address, control, address, public_modifier, feature_a, feature_b]
            protocols.insert(0, dict(address=0x021F0D5C, arguments=[row['value'], actor_address, target_address, action],
                                     stackArguments=[control, address, modifier, feature_a, feature_b], returnWord=value))
        else:
            arguments = [row['value'], actor_address, target_address, action, control, address, modifier, feature_a, feature_b]
        memory = [(ATTACKER, bytes(actor)), (TARGET, bytes(target)), (ATTACKER_RECORD, bytes(192)), (TARGET_RECORD, initial_saved),
                  (OUTPUT, struct.pack('<I', 0xDEADBEEF)), (0x02320000 + action * 40, bytes(metadata)),
                  (0x02232B90 + attribute * 9, bytes([classification])), (0x02232B91 + attribute * 9 + tier, bytes([coefficient])),
                  (0x020F69E8, bytes(4)), (0x020DDD40, bytes(4)), (0x020F6044, struct.pack('<I', initial))]
        patches = [(0x020F6044, struct.pack('<I', rng))]
        if address:
            patches.append((address, struct.pack('<I', result_status)))
        output.append(dict(**row, action=action, attribute=attribute, primaryMode=primary, secondaryMode=secondary, suppliedRawTier=raw_tier,
            finalTier=result_status, initialRng=initial, physicalR0=value, arguments=arguments, memory=memory, patches=patches,
            seed=1780000 + index, draws=draws, protocols=protocols))
    return output
