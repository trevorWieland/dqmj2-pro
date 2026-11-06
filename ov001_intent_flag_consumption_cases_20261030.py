import random
import struct

from ov001_turn_order_itcm_cases_20261030 import contexts

ADDRESS, TEAMS = 0x021DCBE4, (0x02236F6C, 0x022362AC)
INTENTS, RECORDS = (0x02238D1C, 0x02238D2E), 0x02370000


def vectors():
    output = []
    for context in contexts():
        for pattern in range(8):
            for presence in range(5):
                for marker_pattern in range(4):
                    seed = 1390000 + len(output)
                    rng = random.Random(seed)
                    memory, patches, actors, rows = [], [], {}, []
                    for side, base in enumerate(TEAMS):
                        intents = bytearray(rng.randbytes(18))
                        final = bytearray(intents)
                        for slot in range(3):
                            ordinal = side * 3 + slot
                            actor = bytearray(rng.randbytes(1088))
                            record = bytearray(rng.randbytes(528))
                            record_pointer = RECORDS + ordinal * 528
                            struct.pack_into('<I', actor, 0x1E8, record_pointer)
                            actor[0x31C], actor[0x1FF], record[0xAC] = 1, 0, 0
                            actor[0x31E], actor[0x31F], actor[0x235] = side, slot, 1
                            unavailable = bool(presence == 4 or presence and ordinal % 2)
                            if unavailable:
                                if presence in (1, 4):
                                    actor[0x31C] = 0
                                elif presence == 2:
                                    actor[0x1FF] = 1
                                else:
                                    record[0xAC] = 1
                            flag = (0, 4, 251, 255, 85, 170, 1, 128)[(pattern + ordinal) % 8]
                            actor[0x35D] = flag
                            marker = (0, 1, 255, (0, 1, 128)[ordinal % 3])[marker_pattern]
                            intents[slot * 6 + 4] = marker
                            final[slot * 6 + 4] = marker
                            consume = not unavailable and bool(flag & 4)
                            after = flag & ~4 if consume else flag
                            reselect = consume and marker == 0
                            if reselect:
                                struct.pack_into('<HBBB', final, slot * 6, 6, side, 0, 0)
                            memory += [(base + slot * 1088, bytes(actor)), (record_pointer, bytes(record))]
                            if consume:
                                patches.append((base + slot * 1088 + 0x35D, bytes([after])))
                            actors[(side, slot)] = dict(side=side, slot=slot, usable=not unavailable,
                                                       flag=flag, after=after, marker=marker, reselect=reselect)
                        memory.append((INTENTS[side], bytes(intents)))
                        patches.append((INTENTS[side], bytes(final)))
                    memory += context['memory']
                    last = actors[(0 if context['opponentFirst'] else 1, 2)]
                    physical_r0 = last['after'] if last['usable'] and last['flag'] & 4 else 0
                    sequence = sorted(actors, key=lambda item: (-item[0] if context['opponentFirst'] else item[0], item[1]))
                    output.append(dict(seed=seed, context=context, pattern=pattern, presence=presence,
                                       markerPattern=marker_pattern, memory=memory, patches=patches,
                                       arguments=[], draws=[], physicalR0=physical_r0,
                                       actorEffects=[actors[key] for key in sequence],
                                       reselectCalls=[list(key) for key in sequence if actors[key]['reselect']]))
    return output
