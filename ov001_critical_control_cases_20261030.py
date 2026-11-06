import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD


def recipes():
    values = (-2147483648, -1000, -1, 0, 50, 1000, 178956970, 178956971, 1073741824, 2147483647)
    output = [(attack, value, control, mode, 0, 0, seed, index & 1)
              for index, (attack, value, control, mode, seed) in enumerate(product((0, 9, 10, 100, 32767), values,
                                                                                 (1, 0xFFFFFFFF), (0, 7), (0, 0xFFFFFFFF)))]
    output += [(0, value, 0, mode, 0, 0, 0xA5821347, index & 1)
               for index, (value, mode) in enumerate(product(values, (0, 5, 7)))]
    output += [(attack, value, 1, 5, classification, action, seed, side)
               for attack, value, classification, action, seed, side in product((9, 100), (-1, 1000), (0, 1, 255),
                                                                               (0, 6), (0, 0xFFFFFFFF), (0, 1))]
    return output


def vectors(blob):
    if any(blob[8 + action * 40 + 0x22] != 0 for action in (0, 6)):
        raise ValueError('Original supported target attributes differ')
    if struct.unpack_from('<H', blob, 16)[0] & 15 != 1 or struct.unpack_from('<H', blob, 16 + 6 * 40)[0] & 15 != 0:
        raise ValueError('Original supported action modes differ')
    output = []
    for raw_attack, value, control, mode, classification, action, seed, side in recipes():
        state, draws = seed, []
        attack = min(max(raw_attack, 1), 9999)
        active = control != 0 and (mode != 5 or classification == 1 and action == 0)
        if active:
            limit = attack // 10
            state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            draw = (state >> 16) % limit if limit > 0 else 0
            draws.append((limit, draw))
            candidate = attack + draw - attack // 20
            if mode == 7:
                candidate = -candidate
            product_word = (value * 12) & 0xFFFFFFFF
            signed_product = product_word if product_word < 0x80000000 else product_word - 0x100000000
            scaled = abs(signed_product) // 10 * (-1 if signed_product < 0 else 1)
            expected = (min(candidate, scaled) if mode == 7 else max(candidate, scaled)) & 0xFFFFFFFF
        else:
            expected = value & 0xFFFFFFFF
        actor, target = bytearray(1088), bytearray(1088)
        for data, record, team in ((actor, ATTACKER_RECORD, side), (target, TARGET_RECORD, 1 - side)):
            struct.pack_into('<I', data, 0x1E8, record)
            struct.pack_into('<h', data, 0x1F8, 1000)
            struct.pack_into('<h', data, 0x220, raw_attack)
            data[0x31C], data[0x31E] = 1, team
        protocols = [dict(address=0x021F08EC, arguments=[TARGET, action], returnWord=0),
                     dict(address=0x0207AFEC, arguments=[action], returnWord=0x02320000 + action * 40)]
        if control != 0 and mode == 5:
            protocols.append(dict(address=0x021D90C4, arguments=[0, 0], returnWord=classification))
            if classification == 1:
                protocols.append(dict(address=0x0207AFEC, arguments=[action], returnWord=0x02320000 + action * 40))
        if active:
            protocols.append(dict(address=0x021DBD3C, arguments=[ATTACKER], returnWord=attack))
        output.append(dict(rawAttack=raw_attack, value=value, control=control, mode=mode, syntheticClassification=classification,
                           action=action, side=side, initialRng=seed, active=active, physicalR0=expected,
                           arguments=[value, ATTACKER, TARGET, action, control, mode], seed=1590000 + len(output),
                           draws=draws, protocols=protocols,
                           memory=[(ATTACKER, bytes(actor)), (TARGET, bytes(target)),
                                   (ATTACKER_RECORD, bytes(192)), (TARGET_RECORD, bytes(192)),
                                   (0x020DDD40, bytes(4)), (0x020F69E8, bytes(4)),
                                   (0x02232B90, bytes([classification]) + bytes(143)), (0x020F6044, struct.pack('<I', seed))],
                           patches=[(0x020F6044, struct.pack('<I', state))]))
    return output
