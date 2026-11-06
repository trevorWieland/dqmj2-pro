import copy
import random
import struct

from ov001_turn_order_itcm_cases_20261030 import vectors as order_vectors, contexts, advance

ADDRESS, ORDER, RNG = 0x021E7FA8, 0x02238D40, 0x020F6044
TEAMS, INTENTS = (0x02236F6C, 0x022362AC), (0x02238D1C, 0x02238D2E)


def vectors(actions, overlay):
    output = []
    for context in contexts():
        for template in order_vectors(actions, overlay, context):
            if template['pattern'] not in ('ties', 'stages', 'sentinels'):
                continue
            for variant, presence in enumerate(('all', 'blocked-middle', 'no-opponent-usable')):
                vector = copy.deepcopy(template)
                vector['seed'] += variant * 300000
                rng = random.Random(vector['seed'] ^ 0x7FA8)
                memory, patches, usable = [], [], {}
                actor_fields = {}
                for side, base in enumerate(TEAMS):
                    for slot in range(3):
                        address = base + slot * 1088
                        actor = bytearray(next(data for start, data in vector['memory'] if start == address))
                        actor[0x31C], actor[0x31E], actor[0x31F] = 1, side, slot
                        actor[0x322] = 3 if side == 1 else 0
                        actor[0x1FF] = int(presence == 'blocked-middle' and side == 1 and slot == 1)
                        before = rng.getrandbits(8)
                        actor[0x35D] = before
                        actor_fields[address] = bytes(actor)
                        patches.append((address + 0x35D, bytes([before & ~4])))
                        pointer = struct.unpack_from('<I', actor, 0x1E8)[0]
                        record = bytearray(next(data for start, data in vector['memory'] if start == pointer))
                        record[0xAC] = int(presence == 'no-opponent-usable' and side == 1)
                        actor_fields[pointer] = bytes(record)
                        usable[(side, slot)] = actor[0x31C] != 0 and actor[0x1FF] == 0 and record[0xAC] == 0
                for start, payload in vector['memory']:
                    memory.append((start, actor_fields.get(start, payload)))
                intents = []
                for side in range(2):
                    raw = bytearray(next(data for start, data in memory if start == INTENTS[side]))
                    for slot in range(3):
                        struct.pack_into('<H', raw, slot * 6, 6)
                        raw[slot * 6 + 3:slot * 6 + 5] = b'\xff\x00'
                    intents.append(raw)
                order = bytearray(next(payload for start, payload in template['patches'] if start == ORDER))
                count = vector['own'] + vector['opposing']
                for index in range(count, 6):
                    order[index * 4 + 1] = 255
                state, draws, selected, stop = vector['nextRng'], list(vector['draws']), [], None
                for index, position in enumerate(vector['expectedOrder']):
                    side, slot = position['side'], position['slot']
                    if side != 1 or not usable[(side, slot)]:
                        continue
                    if selected:
                        state, draw = advance(state, 3)
                        draws.append((3, draw))
                        if draw == 0:
                            stop = dict(orderIndex=index, side=side, slot=slot)
                            break
                    state, draw = advance(state, 3)
                    draws.append((3, draw))
                    struct.pack_into('<HBB', intents[1], slot * 6, 0, 0, draw)
                    selected.append(slot)
                patches += [(ORDER, bytes(order)), (RNG, struct.pack('<I', state)),
                            (INTENTS[0], bytes(intents[0]) + bytes(intents[1]))]
                vector.update(memory=memory, patches=patches, draws=draws, nextRng=state,
                              arguments=[], presence=presence, selectedSlots=selected, stoppedBefore=stop)
                output.append(vector)
    return output
