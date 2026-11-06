import copy
import random
import struct

from ov001_turn_order_itcm_cases_20261030 import contexts, vectors as order_vectors

TEAMS, RECORDS = (0x02236F6C, 0x022362AC), 0x02370000
INTENTS, CONTEXT, RNG = (0x02238D1C, 0x02238D2E), 0x022388EC, 0x020F6044


def copy_protocols():
    return [dict(address=0x02008E0C, arguments=[base + slot * 1088 + 0x22C,
                 base + slot * 1088 + 0x2A4, 120], returnWord=base + slot * 1088 + 0x2A4)
            for base in TEAMS for slot in range(3)]


def snapshot_vectors():
    output = []
    for index in range(64):
        seed = 1400000 + index
        rng = random.Random(seed)
        memory, patches = [], []
        for base in TEAMS:
            for slot in range(3):
                actor = bytearray(rng.randbytes(1088))
                if index < 4:
                    actor[0x22C:0x2A4] = bytes((0, 255, 85, 170)[index:index + 1]) * 120
                location = base + slot * 1088
                memory.append((location, bytes(actor)))
                patches += [(location + 0x2A4, bytes(actor[0x22C:0x2A4])), (location + 0x431, b'\x00')]
        output.append(dict(seed=seed, memory=memory, patches=patches, arguments=[], draws=[],
                           physicalR0=TEAMS[1] + 2 * 1088 + 0x2A4, protocols=copy_protocols()))
    return output


def turn_vectors(actions, overlay):
    output = []
    for context in contexts():
        for template in order_vectors(actions, overlay, context):
            if template['pattern'] not in ('ties', 'stages', 'sentinels'):
                continue
            for flag_pattern in (0, 1):
                vector = copy.deepcopy(template)
                vector['seed'] = 1410000 + len(output)
                randomizer = random.Random(vector['seed'])
                memory, patches, actors, originals = [], list(vector['patches']), {}, {}
                for location, payload in vector['memory']:
                    data = bytearray(payload)
                    for side, base in enumerate(TEAMS):
                        if base <= location < base + 3 * 1088 and (location - base) % 1088 == 0:
                            slot = (location - base) // 1088
                            data[0x31C], data[0x1FF], data[0x31E], data[0x31F] = 1, 0, side, slot
                            data[0x235], data[0x35D], data[0x431] = 1, 0xA1 | flag_pattern * 4, 255
                            actors[(side, slot)] = bytes(data)
                            patches += [(location + 0x2A4, bytes(data[0x22C:0x2A4])),
                                        (location + 0x431, b'\x00')]
                            if flag_pattern:
                                patches.append((location + 0x35D, b'\xA1'))
                    if location in INTENTS:
                        side = INTENTS.index(location)
                        for slot in range(3):
                            data[slot * 6 + 4] = 0 if (side * 3 + slot) % 2 == 0 else 128
                        originals[side] = bytes(data)
                    memory.append((location, bytes(data)))
                sequence = sorted(actors, key=lambda key: (-key[0] if context['opponentFirst'] else key[0], key[1]))
                protocols = []
                seed_context = vector['initialRng']
                old_state = seed_context ^ 0xA5A5A5A5 if context['rawScene'] == 2 else seed_context
                if context['rawScene'] == 2:
                    protocols += [dict(address=0x0204457C, returnWord=seed_context),
                                  dict(address=0x0203D2EC, arguments=[seed_context],
                                       returnWord=old_state, setRng=seed_context)]
                protocols += copy_protocols()
                final_intents = [bytearray(originals[side]) for side in (0, 1)]
                for side, slot in sequence:
                    if flag_pattern and originals[side][slot * 6 + 4] == 0:
                        struct.pack_into('<HBBB', final_intents[side], slot * 6, 6, side, 0, 0)
                        protocols.append(dict(address=0x021E8398, arguments=[side, slot], returnWord=0))
                patches = [(location, data) for location, data in patches if location != INTENTS[0]]
                patches.append((INTENTS[0], bytes(final_intents[0]) + bytes(final_intents[1])))
                before = bytearray(randomizer.randbytes(64))
                before[0x10] = 4 if vector['reverse'] else 0
                after = bytearray(before)
                after[0xE] = after[0x1E] = vector['own'] + vector['opposing']
                after[0x12] = after[0x1A] = after[0xB] = 0
                after[8] = 0x21
                memory += [(CONTEXT, bytes(before)), (0x020F69C4 + 12, struct.pack('<I', seed_context)),
                           (RNG, struct.pack('<I', old_state))]
                patches.append((CONTEXT, bytes(after)))
                for location in (0x0223896C, 0x02238950):
                    memory.append((location, randomizer.randbytes(28)))
                    patches.append((location, bytes(28)))
                    protocols.append(dict(address=0x02008D78, arguments=[location, 0, 28]))
                vector.update(memory=memory, patches=patches, protocols=protocols, arguments=[], physicalR0=1,
                              originalRng=old_state, seedContextWord=seed_context,
                              seedReplaced=context['rawScene'] == 2, flagPattern=flag_pattern,
                              conditionalReselectCalls=[row['arguments'] for row in protocols if row['address'] == 0x021E8398])
                output.append(vector)
    return output
