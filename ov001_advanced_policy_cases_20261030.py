import copy
import struct

from ov001_action_candidate_cases_20261030 import RNG, TEAMS, vectors as candidate_vectors

CONTROLLER = 0x022388EC


def predict(side, mode, phase, skills, state, turn):
    limits, draws, validations, events = [], [], [], []
    original_phase = phase

    def random(limit):
        nonlocal state
        state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
        value = (state >> 16) % limit
        limits.append(limit)
        draws.append(value)
        return value

    def valid(action):
        result = int(side != 0 or action != 1)
        validations.append({'action': action, 'result': result})
        return result

    for attempt in range(13):
        action = 0
        if mode == 4:
            action = skills[phase % 6]
        elif mode == 5:
            draw = random(2)
            action = skills[(phase % 3) * 2 + draw]
        elif mode == 6:
            index = random(5) + 1 if phase % 2 else 0
            action = skills[index]
            if not valid(action):
                if index == 0:
                    action = 0
                else:
                    seen = {index}
                    events.append(['firstWrite', index])
                    while len(seen) < 5:
                        index = random(5) + 1
                        events.append(['read', index, int(index in seen)])
                        if index not in seen:
                            action = skills[index]
                            if valid(action):
                                break
                            seen.add(index)
                            events.append(['write', index])
                        if len(limits) > 1000:
                            raise ValueError('Synthetic slot search exceeded bounded model')
                    if len(seen) == 5:
                        action = 0
        elif mode == 7:
            quarter = phase % 4
            action = skills[quarter + 2] if quarter >= 2 else skills[quarter * 2 + random(2)]
        if not (turn >= 1 and action == 1):
            break
        phase = (phase + 1) & 255
    else:
        action = 0
    return {'action': action, 'phase': phase, 'state': state, 'limits': limits,
            'draws': draws, 'validations': validations, 'visitedEvents': events,
            'attempts': attempt + 1, 'initialPhase': original_phase}


def vectors():
    candidates = candidate_vectors()
    templates = {side: next(row for row in candidates if row['branch'] == 'policy6'
                           and row['side'] == side and row['slot'] == 0 and row['phase'] == 0)
                 for side in (0, 1)}
    profiles = {'all-valid': [2] * 6, 'all-action1': [1] * 6,
                'alternating': [2, 1, 2, 1, 2, 1], 'last-valid': [1, 1, 1, 1, 1, 2]}
    result = []
    for side in (0, 1):
        for turn in (0, 1):
            for mode in (4, 5, 6, 7):
                for phase in (0, 1, 2, 3, 4, 5, 254, 255):
                    for label, skills in profiles.items():
                        seed = 1220000 + len(result)
                        base = copy.deepcopy(templates[side])
                        actor = base['arguments'][0]
                        memory = []
                        for address, payload in base['memory']:
                            data = bytearray(payload)
                            if address == actor:
                                data[0x35B] = phase
                            if len(data) == 528:
                                data[8:14] = bytes(skills)
                            memory.append((address, bytes(data)))
                        memory.append((CONTROLLER + 0x1A, bytes([turn])))
                        state = (base['initialRng'] + seed * 0x9E3779B9) & 0xFFFFFFFF
                        memory.append((RNG, struct.pack('<I', state)))
                        expected = predict(side, mode, phase, skills, state, turn)
                        result.append({'seed': seed, 'side': side, 'mode': mode, 'turn': turn,
                                       'profile': label, 'skills': skills, 'actor': actor,
                                       'initialState': state, 'memory': memory,
                                       'arguments': [actor, TEAMS[side], TEAMS[1 - side], mode],
                                       'patches': [(RNG, struct.pack('<I', expected['state'])),
                                                   (actor + 0x35B, bytes([expected['phase']]))],
                                       'expected': expected})
    return result
