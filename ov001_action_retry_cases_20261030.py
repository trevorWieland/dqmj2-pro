import copy
import random
import struct

from ov001_action_candidate_cases_20261030 import MODE, RNG, TEAMS, vectors as candidate_vectors, advance

INTENTS = (0x02238D1C, 0x02238D2E)


def make_vector(candidate, gate):
    vector = copy.deepcopy(candidate)
    actor = vector['arguments'][0]
    side, slot, phase = vector['side'], vector['slot'], vector['phase']
    vector['gate'] = gate
    vector['memory'] = [(address, payload[:0x322] + bytes([gate]) + payload[0x323:]
                         if address == actor else payload) for address, payload in vector['memory']]
    intent_data = bytearray(random.Random(vector['seed'] ^ 0x8540).randbytes(36))
    for index in range(6):
        struct.pack_into('<H', intent_data, index * 6, 0)
        intent_data[index * 6 + 4] = 0
    vector['memory'].append((INTENTS[0], bytes(intent_data)))
    intent = INTENTS[side] + slot * 6
    vector['intent'] = intent
    vector['actor'] = actor
    vector['arguments'] = [side, slot]
    attempts = 0 if gate != 1 else 33 if side == 0 and vector['branch'] in ('policy0', 'policy1', 'policy2', 'policy3', 'policy4', 'policy5') else 1
    failures = attempts if attempts == 33 else 0
    vector['attempts'], vector['failures'] = attempts, failures
    limits = candidate['limits'] * attempts + ([3] if failures else [])
    final_rng, draws = advance(vector['initialRng'], limits)
    vector['limits'], vector['draws'], vector['finalRng'] = limits, draws, final_rng
    vector['patches'] = [(MODE, vector['memory'][0][1]), (RNG, struct.pack('<I', final_rng))]
    if attempts:
        if failures:
            output = struct.pack('<HBB', 0, 1 - side, draws[-1])
            vector['physicalR0'] = draws[-1]
        else:
            output = candidate['patches'][2][1]
            vector['physicalR0'] = 1
        vector['patches'].append((intent, output))
    else:
        vector['physicalR0'] = gate
    vector['patches'].append((actor + 0x35B, bytes([(phase + failures) & 255])))
    vector['expectedValidators'] = [1, 1] if attempts and vector['branch'] == 'policy6' else [0] * 33 if failures else [1] if attempts else []
    return vector


def vectors():
    candidates = candidate_vectors()
    result = [make_vector(row, 1) for row in candidates if row['branch'] != 'special' or row['side'] == 1]
    for gate in (0, 2, 255):
        for row in candidates:
            if row['branch'] == 'policy0' and row['phase'] == 255:
                result.append(make_vector(row, gate))
    return result
