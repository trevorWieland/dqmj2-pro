import copy
import random
import struct

from ov001_action_candidate_cases_20261030 import TEAMS, vectors as candidate_vectors

FLAGS, CLASSIFIERS, CONTROLLER = 0x022430C8, 0x02243DC8, 0x022388EC
INTENTS = (0x02238D1C, 0x02238D2E)


def history_vectors():
    result = []
    for side in (0, 1):
        for slot in range(3):
            for flag in (0, 0x20, 0xFF, 0xDF):
                for turn in (0, 1, 255):
                    for profile in ('none', 'self-only', 'other'):
                        for own_match in (False, True):
                            seed = 1230000 + len(result)
                            rng = random.Random(seed)
                            action = (0, 1, 40, 255)[len(result) % 4]
                            actor = TEAMS[side] + slot * 1088
                            body = bytearray(rng.randbytes(1088))
                            own_history = action if own_match else action ^ 0xFFFF
                            struct.pack_into('<H', body, 0x344, own_history)
                            intent_data = bytearray(rng.randbytes(36))
                            intents = [action ^ 0xFFFF] * 3
                            if profile != 'none':
                                intents[slot if profile == 'self-only' else (slot + 1) % 3] = action
                            for member, value in enumerate(intents):
                                struct.pack_into('<H', intent_data, side * 18 + member * 6, value)
                            flags = bytearray(256 * 5)
                            flags[action * 5 + 4] = flag
                            signed_turn = turn if turn < 128 else turn - 256
                            expected = int(bool(flag & 0x20) and
                                           ((signed_turn + 1 >= 2 and own_history == action) or
                                            any(value == action for member, value in enumerate(intents) if member != slot)))
                            memory = [(actor, bytes(body)), (INTENTS[0], bytes(intent_data)),
                                      (FLAGS, bytes(flags)), (CONTROLLER + 0x1A, bytes([turn]))]
                            result.append({'kind': 'history', 'seed': seed, 'arguments': [side, action, slot],
                                           'memory': memory, 'patches': [], 'returnWord': expected,
                                           'side': side, 'slot': slot, 'action': action, 'flag': flag,
                                           'turnByte': turn, 'ownHistory': own_history, 'intents': intents,
                                           'profile': profile})
    return result


def target_vectors():
    templates = candidate_vectors()
    result = []
    for side in (0, 1):
        for slot in range(3):
            template = next(row for row in templates if row['branch'] == 'policy6' and
                            row['side'] == side and row['slot'] == slot and row['phase'] == 0)
            for tier in range(5):
                for action in (0, 2, 205):
                    for selector in (0, 1, 8, 9):
                        actor = template['arguments'][0]
                        memory = []
                        for address, payload in copy.deepcopy(template['memory']):
                            data = bytearray(payload)
                            if address == actor:
                                data[0x322] = 1
                            if len(data) == 528:
                                data[0xA9] = tier
                            memory.append((address, bytes(data)))
                        memory.append((CLASSIFIERS, bytes([selector]) * (256 * 8 + 16)))
                        result.append({'kind': 'target', 'seed': 1240000 + len(result),
                                       'arguments': [actor, TEAMS[1 - side], action], 'memory': memory,
                                       'patches': [], 'returnWord': slot if selector == 9 else 0,
                                       'side': side, 'slot': slot, 'tier': tier, 'action': action,
                                       'selector': selector, 'callback': 0x02226CD8 + selector * 8})
    return result
