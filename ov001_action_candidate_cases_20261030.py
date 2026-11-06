import random
import struct

TEAMS = (0x02236F6C, 0x022362AC, 0x022355EC, 0x02237C2C)
RECORDS, OUTPUT, MODE, RNG = 0x02370000, 0x02379000, 0x0222F160, 0x020F6044


def advance(seed, limits):
    state, draws = seed, []
    for limit in limits:
        state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
        draws.append((state >> 16) % limit if limit > 0 else 0)
    return state, draws


def vectors():
    result = []
    for branch in ('absent', 'blocked', 'special', 'policy0', 'policy1', 'policy2', 'policy3', 'policy4', 'policy5', 'policy6'):
        for side in (0, 1):
            for slot in range(3):
                for phase in (0, 1, 254, 255):
                    seed = 1010000 + len(result)
                    rng = random.Random(seed)
                    initial_rng = rng.getrandbits(32)
                    if branch == 'special':
                        while advance(initial_rng, [8])[1][0] != 7:
                            initial_rng = (initial_rng + 1) & 0xFFFFFFFF
                        limits, action = [8], 205
                    elif branch.startswith('policy'):
                        policy = int(branch[6:])
                        limits = [256] if policy < 4 else [2] if policy == 5 else [5] if policy == 6 and phase & 1 else []
                        action = 2 if policy == 6 else 1
                    else:
                        limits, action = [], 6
                    memory = [(MODE, bytes([(0, 1, 128, 255)[phase % 4]])),
                              (RNG, struct.pack('<I', initial_rng)), (OUTPUT, b'\x00\x80\xff\x80'),
                              (0x020F69E8, b'\x00')]
                    for team, base in enumerate(TEAMS):
                        for member in range(3):
                            pointer = RECORDS + (team * 3 + member) * 528
                            record = bytearray(528)
                            record[8:14] = bytes([2 if branch == 'policy6' else 1] * 6)
                            struct.pack_into('<h', record, 0x2E, 1)
                            for field in range(7):
                                struct.pack_into('<h', record, 0x120 + 2 * field, 300)
                            actor = bytearray(1088)
                            actor[0x31C], actor[0x31E], actor[0x31F] = 1, team, member
                            struct.pack_into('<I', actor, 0x1E8, pointer)
                            struct.pack_into('<hh', actor, 0x1F0, 300, 300)
                            if team == side and member == slot:
                                actor[0x35B] = phase
                                if branch == 'absent':
                                    actor[0x31C] = 0
                                elif branch == 'blocked':
                                    actor[0x235] = 1
                                elif branch == 'special':
                                    actor[0x237] = 1
                                else:
                                    record[0xAA] = int(branch[6:])
                            memory.extend([(base + member * 1088, bytes(actor)), (pointer, bytes(record))])
                    final_rng, draws = advance(initial_rng, limits)
                    selected_side = side if action != 6 else 0
                    selected_slot = slot if action != 6 else 0
                    patches = [(MODE, memory[0][1]), (RNG, struct.pack('<I', final_rng)),
                               (OUTPUT, struct.pack('<HBB', action, selected_side, selected_slot))]
                    result.append({'seed': seed, 'branch': branch, 'side': side, 'slot': slot,
                                   'phase': phase, 'memory': memory, 'patches': patches,
                                   'initialRng': initial_rng, 'finalRng': final_rng,
                                   'limits': limits, 'draws': draws,
                                   'arguments': [TEAMS[side] + slot * 1088, TEAMS[side], TEAMS[1 - side],
                                                 OUTPUT, OUTPUT + 2, OUTPUT + 3]})
    return result
