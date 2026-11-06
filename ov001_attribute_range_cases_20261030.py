import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD

MASK = 0xFFFFFFFF


def nibble_vectors(blob):
    rows = [(action, side, scene, TARGET) for action, side, scene in product(range(256), (0, 1, 255), (0, 7))]
    rows += [(action, 255, 7, pointer) for action, pointer in product((0, 8, 64, 128, 255), (0, MASK))]
    output = []
    for index, (action, side, scene, pointer) in enumerate(rows):
        actor = bytearray(1088)
        actor[0x31E] = side
        byte = blob[8 + action * 40 + 0x22]
        expected = (byte >> (0 if scene == 7 or side == 0 else 4)) & 15
        output.append(dict(action=action, side=side, suppliedScene=scene, actorPointer=pointer, metadataByte=byte,
                           arguments=[pointer, action], physicalR0=expected, seed=1670000 + index, draws=[], patches=[],
                           memory=[(TARGET, bytes(actor)), (0x020F69E8, struct.pack('<I', scene))],
                           protocols=[dict(address=0x020444A8, returnWord=int(scene == 7)),
                                      dict(address=0x0207AFEC, arguments=[action], returnWord=0x02320000 + action * 40)]))
    return output


def range_vectors(blob):
    recognized = (0x74, 0x75, 8, 0x90, 0x91, 0x92, 0x93, 0xFB, 0x4E, 0x9F, 0x9E)
    rows = list(product(recognized, (0, 1, 127, 255), (0, 1, 2, 3, MASK), (0, 0xFFFFFFFF, 0xA5821347)))
    rows += list(product((0, 6, 255), (0, 255), (0, MASK), (0,)))
    output = []
    for index, (action, counter, control, initial) in enumerate(rows):
        side, state, draws = index % 2, initial, []
        limits = {0x74: 41, 0x75: 41, 8: 200, 0x4E: 6, 0x9F: 6, 0x9E: 4}
        limit = limits.get(action, 21)
        if action in recognized:
            if control in (0, 3):
                state = (state * 0x41C64E6D + 0x3039) & MASK
                random_word = (state >> 16) % limit
                draws.append((limit, random_word))
            else:
                random_word = limit - 1 if control == 2 else 0
            if action in (0x74, 0x75):
                expected = counter + random_word + 160
            elif action == 8:
                expected = counter + random_word
            elif action == 0x4E:
                expected = random_word + 2 * counter + 5
            elif action == 0x9F:
                expected = counter + random_word + 5
            elif action == 0x9E:
                expected = counter + random_word
            else:
                expected = ((counter >> 1) + 120) * (random_word + 90) // 100
        else:
            random_word, expected = None, 0
        actor, target = bytearray(1088), bytearray(1088)
        for data, record, team in ((actor, ATTACKER_RECORD, side), (target, TARGET_RECORD, 1 - side)):
            struct.pack_into('<I', data, 0x1E8, record)
            data[0x31C], data[0x31E] = 1, team
        actor[0x1FC] = counter
        metadata = blob[8 + action * 40 + 0x22]
        attribute = metadata >> (0 if target[0x31E] == 0 else 4) & 15
        protocols = [dict(address=0x02209490, arguments=[TARGET + 0x22C]),
                     dict(address=0x021F08EC, arguments=[TARGET, action], returnWord=attribute)]
        if random_word is not None:
            protocols.append(dict(address=0x0207B94C, arguments=[limit, control], returnWord=random_word))
        output.append(dict(action=action, counter=counter, control=control, initialRng=initial, side=side, physicalR0=expected,
                           arguments=[ATTACKER, TARGET, action, control], seed=1710000 + index, draws=draws, protocols=protocols,
                           memory=[(ATTACKER, bytes(actor)), (TARGET, bytes(target)), (ATTACKER_RECORD, bytes(192)), (TARGET_RECORD, bytes(192)),
                                   (0x020F69E8, bytes(4)), (0x020DDD40, bytes(4)), (0x020F6044, struct.pack('<I', initial))],
                           patches=[(0x020F6044, struct.pack('<I', state))]))
    return output
