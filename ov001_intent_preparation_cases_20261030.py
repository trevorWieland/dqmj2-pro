import copy
import struct

from ov001_action_candidate_cases_20261030 import MODE, RNG, TEAMS, advance, vectors as candidates
from ov001_action_retry_cases_20261030 import vectors as retries

ADDRESS, INTENTS = 0x021E7538, (0x02238D1C, 0x02238D2E)


def change_actor(vector, gate):
    address = TEAMS[vector['side']] + vector['slot'] * 1088
    vector['memory'] = [(start, payload[:0x322] + bytes([gate]) + payload[0x323:]
                         if start == address else payload) for start, payload in vector['memory']]
    vector['arguments'] = [vector['slot'], TEAMS[vector['side']], TEAMS[1 - vector['side']], 0]
    vector['gate'] = gate
    return address


def vectors():
    result = []
    for original in retries():
        if original['gate'] != 1:
            continue
        vector = copy.deepcopy(original)
        change_actor(vector, 1)
        output = next(payload for address, payload in vector['patches'] if address == vector['intent'])
        vector['physicalR0'] = struct.unpack('b', output[3:4])[0] & 0xFFFFFFFF
        vector['recipeClass'] = 'candidate-and-native-validation'
        result.append(vector)
    for original in candidates():
        if original['branch'] not in ('absent', 'policy0', 'policy6') or original['phase'] not in (0, 255):
            continue
        for gate in ((0, 3, 128, 255) if original['branch'] == 'absent' else (2,)):
            vector = copy.deepcopy(original)
            actor = change_actor(vector, gate)
            side, slot = vector['side'], vector['slot']
            intent = INTENTS[side] + slot * 6
            vector['memory'].append((INTENTS[0], bytes([0xA5]) * 36))
            if gate == 0:
                action, target_side, target_slot, limits = 6, side, 0, []
            elif gate == 2:
                action, target_side, target_slot, limits = (2 if original['branch'] == 'policy6' else 1), 1 - side, 0, []
                vector['memory'].append((0x020F69C4 + 0x1C, bytes(4)))
            else:
                action, target_side, limits = 0, 1 - side, [3]
                target_slot = advance(vector['initialRng'], limits)[1][0]
            state, draws = advance(vector['initialRng'], limits)
            vector.update(limits=limits, draws=draws, finalRng=state, physicalR0=target_slot,
                          intent=intent, actor=actor, recipeClass='bounded-gate-and-fallback',
                          expectedAction=action, expectedTargetSide=target_side, expectedTargetSlot=target_slot)
            vector['patches'] = [(MODE, vector['memory'][0][1]), (RNG, struct.pack('<I', state)),
                                 (intent, struct.pack('<HBB', action, target_side, target_slot)),
                                 (actor + 0x35B, bytes([vector['phase']]))]
            result.append(vector)
    return result
