import random
import struct

from ov001_action_candidate_cases_20261030 import RNG

ACTORS, PREPARED, SAVED = 0x022362AC, 0x021C1544, 0x022355E8


def vectors():
    result = []
    for initialize in (0, 1, 0xFFFFFFFF):
        for gates in ([1, 1, 1], [0, 1, 2], [3, 1, 1], [0, 0, 0]):
            for presence in ([1, 1, 1], [0, -1, 1], [-32768, 0, 32767]):
                for policies in ([4, 7, 5], [7, 4, 6], [255, 0, 3]):
                    seed = 1250000 + len(result)
                    rng = random.Random(seed)
                    state = rng.getrandbits(32)
                    current = state
                    actors = bytearray(rng.randbytes(3 * 1088))
                    records = bytearray(rng.randbytes(3 * 528))
                    saved = bytes([0, 127, 255])
                    memory, patches, limits, draws, eligible = [], [], [], [], []
                    for slot in range(3):
                        base = slot * 1088
                        actors[base + 0x322] = gates[slot]
                        struct.pack_into('<I', actors, base + 0x1E8, PREPARED + slot * 528 + 4)
                        struct.pack_into('<h', records, slot * 528 + 0x2E, presence[slot])
                        records[slot * 528 + 0xAE] = policies[slot]
                        if presence[slot] >= 0 and gates[slot] == 1:
                            eligible.append(slot)
                            if initialize == 0:
                                phase = saved[slot]
                            elif policies[slot] in (4, 7):
                                limit = 6 if policies[slot] == 4 else 2
                                current = (current * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
                                phase = (current >> 16) % limit
                                limits.append(limit)
                                draws.append(phase)
                            else:
                                phase = 0
                            patches.append((ACTORS + base + 0x35B, bytes([phase])))
                    memory.extend([(ACTORS, bytes(actors)), (PREPARED, bytes(records)),
                                   (SAVED, saved), (RNG, struct.pack('<I', state))])
                    patches.append((RNG, struct.pack('<I', current)))
                    result.append({'seed': seed, 'initialize': initialize, 'gates': gates,
                                   'presence': presence, 'policies': policies, 'initialState': state,
                                   'memory': memory, 'patches': patches, 'eligibleSlots': eligible,
                                   'limits': limits, 'draws': draws, 'finalState': current})
    return result
