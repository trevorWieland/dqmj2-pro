import random
import struct

ADDRESS, ORDER, RNG, ACT = 0x021E7740, 0x02238D40, 0x020F6044, 0x02320000
TEAMS, RECORD = (0x02236F6C, 0x022362AC), 0x02370000
INTENTS = (0x02238D1C, 0x02238D2E)


def advance(state, limit):
    state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    return state, (state >> 16) % limit if limit > 0 else 0


def vectors(actions, overlay, context):
    class_actions = {kind: next(index for index in range(len(actions) // 40)
                               if struct.unpack_from('b', actions, index * 40 + 38)[0] == kind)
                     for kind in range(-3, 4)}
    output = []
    for own in range(4):
        for opposing in range(4):
            for reverse in (False, True):
                for pattern in ('mixed', 'ties', 'negative', 'sentinels', 'stages', 'grouping', 'positive-fallback', 'mixed-flags'):
                    seed = 1310000 + context['index'] * 2000 + len(output)
                    randomizer = random.Random(seed)
                    state = initial_state = randomizer.getrandbits(32)
                    memory = [(ACT, actions), (0x021C6748, struct.pack('<I', ACT)),
                              (0x020DDD40, bytes(1)), (0x020F69E8, bytes(1)),
                              (0x022355E4, bytes([0xA5, 0x5A, opposing, own])),
                              (0x022388EC + 0x10, bytes([4 if reverse else 0]))]
                    positions, actors, keys, classes, draws = [], {}, {}, {}, []
                    expected_intents = {}
                    for side, count in enumerate((own, opposing)):
                        intents = bytearray(randomizer.randbytes(18))
                        for slot in range(3):
                            ordinal = side * 3 + slot
                            kind = (ordinal + seed) % 7 - 3 if pattern in ('mixed', 'mixed-flags') else 0 if pattern in ('ties', 'stages', 'grouping') else (-1, -2, -3)[ordinal % 3]
                            if pattern == 'positive-fallback':
                                kind = (1, 0, 2)[ordinal % 3]
                            if pattern == 'sentinels':
                                kind = 0
                            action = class_actions[kind]
                            struct.pack_into('<H', intents, slot * 6, action)
                            actor = bytearray(1088)
                            record = bytearray(528)
                            record_address = RECORD + ordinal * 528
                            struct.pack_into('<I', actor, 0x1E8, record_address)
                            raw = 1 if pattern == 'ties' else 50 + ordinal * 43
                            stage = (-2, -1, 0, 1, 2, 0)[ordinal] if pattern == 'stages' else 0
                            trait = (8, 9, 0)[ordinal % 3] if pattern == 'sentinels' else 0
                            struct.pack_into('<h', actor, 0x1F8, raw)
                            actor[0x22F], record[0x46] = stage & 255, trait
                            actor[0x265] = int(pattern in ('grouping', 'positive-fallback') or pattern == 'mixed-flags' and ordinal % 2)
                            memory += [(TEAMS[side] + slot * 1088, bytes(actor)), (record_address, bytes(record))]
                            actors[(side, slot)] = dict(raw=raw, stage=stage, trait=trait, flagged=actor[0x265])
                            classes[(side, slot)] = kind
                            if slot < count:
                                positions.append((side, slot))
                        memory.append((INTENTS[side], bytes(intents)))
                        expected_intents[side] = bytearray(intents)
                    if context['opponentFirst']:
                        positions.sort(key=lambda value: value[0], reverse=True)
                    memory += context['memory']
                    for position in positions:
                        actor = actors[position]
                        state, draw = advance(state, 51)
                        draws.append((51, draw))
                        base, stage = min(actor['raw'], 9999), actor['stage']
                        stat = base * 2 if stage >= 2 else base * 3 >> 1 if stage == 1 else base >> 1 if stage == -1 else base >> 2 if stage <= -2 else base
                        stat = max(1, min(stat, 9999))
                        key = stat * (draw + 50) // 100
                        keys[position] = -1 if actor['trait'] == 8 else 9999 if actor['trait'] == 9 else key
                    table = 0x0222DF13 if reverse else 0x0222DF0C
                    priorities = struct.unpack('7b', overlay[table - 0x021D7240:table - 0x021D7240 + 7])
                    boundary = 0
                    for priority in priorities[:6]:
                        for left in range(boundary, len(positions)):
                            for right in range(left, len(positions)):
                                a, b = positions[left], positions[right]
                                swap = classes[a] != priority and classes[b] == priority
                                if classes[a] == priority and classes[b] == priority:
                                    swap = keys[a] > keys[b] if reverse else keys[a] < keys[b]
                                if swap:
                                    positions[left], positions[right] = b, a
                        boundary += sum(classes[position] == priority for position in positions[boundary:])
                    tie = []
                    for unused in positions:
                        state, draw = advance(state, 256)
                        draws.append((256, draw))
                        tie.append(draw)
                    for unused in range(6):
                        for left in range(len(positions)):
                            for right in range(left, len(positions)):
                                a, b = positions[left], positions[right]
                                if keys[a] == keys[b] and classes[a] == classes[b] and tie[left] < tie[right]:
                                    tie[left], tie[right] = tie[right], tie[left]
                                    positions[left], positions[right] = b, a
                    grouped, positive, fallbacks, copies = [0, 0], [0, 0], [], 0
                    for index in range(len(positions)):
                        item = positions[index]
                        side, slot = item
                        if not actors[item]['flagged']:
                            continue
                        if positive[side]:
                            struct.pack_into('<H', expected_intents[side], slot * 6, 6)
                            expected_intents[side][slot * 6 + 3:slot * 6 + 5] = b'\xff\x01'
                            fallbacks.append(dict(side=side, slot=slot))
                        elif classes[item] == 0:
                            if grouped[side]:
                                previous = index - 1
                                copies += 2
                                while positions[previous][0] != side:
                                    positions[previous + 1] = positions[previous]
                                    previous -= 1
                                    copies += 1
                                positions[previous + 1] = item
                            grouped[side] += 1
                        elif classes[item] > 0:
                            positive[side] += 1
                    before = randomizer.randbytes(24)
                    expected = bytearray(before)
                    for index, (side, slot) in enumerate(positions):
                        struct.pack_into('<bbh', expected, index * 4, side, slot, keys[(side, slot)])
                    memory += [(ORDER, before), (RNG, struct.pack('<I', initial_state))]
                    output.append(dict(seed=seed, own=own, opposing=opposing, reverse=reverse, pattern=pattern,
                                       memory=memory, patches=[(ORDER, bytes(expected)), (RNG, struct.pack('<I', state)),
                                                               (INTENTS[0], bytes(expected_intents[0]) + bytes(expected_intents[1]))],
                                       expectedOrder=[dict(side=side, slot=slot, key=keys[(side, slot)],
                                                           priority=classes[(side, slot)]) for side, slot in positions],
                                       initialRng=initial_state, nextRng=state, draws=draws, context=context,
                                       expectedFallbacks=fallbacks, expectedCopyCalls=copies,
                                       arguments=[randomizer.getrandbits(32), own, randomizer.getrandbits(32), opposing]))
    return output


def contexts():
    recipes = [(0, 0, 0, 0, 0, False), (2, 0, 0, 1, 0, False),
               (2, 0, 257, 1, 0, True), (4, 1, 0, 0, 0, False),
               (4, 1, 0, 0, 1, True)]
    output = []
    for index, (scene, mode, sdk, counter, session, opponent_first) in enumerate(recipes):
        memory = [(0x020F69E8, bytes([scene])), (0x021CEBE0 + 0x30, struct.pack('<I', mode)),
                  (0x021CEBE0 + 6, bytes([counter])), (0x021C72A0 + 12, struct.pack('<H', sdk)),
                  (0x021D19E0, struct.pack('<I', 0x02380000)), (0x02380000 + 0x2C, bytes([session]))]
        output.append(dict(index=index, rawScene=scene, rawModeWord=mode, rawSdkWord=sdk,
                           rawCounterByte=counter, rawSessionByte=session,
                           opponentFirst=opponent_first, memory=memory))
    return output
