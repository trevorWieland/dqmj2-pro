import copy

from ov001_policy_helper_cases_20261030 import target_vectors


def vectors():
    result = []
    for template in target_vectors():
        for raw_slot in ((0, 1, 2, 4, 127, 128, 255) if template['selector'] == 9 else (template['slot'],)):
            vector = copy.deepcopy(template)
            vector['seed'] = 1380000 + len(result)
            if vector['selector'] == 9:
                memory = []
                for location, payload in vector['memory']:
                    body = bytearray(payload)
                    if location == vector['arguments'][0]:
                        body[0x31F] = raw_slot
                    memory.append((location, bytes(body)))
                vector.update(memory=memory, returnWord=raw_slot)
            vector['rawActorSlot'] = raw_slot
            result.append(vector)
    return result
