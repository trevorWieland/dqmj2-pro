import ov003_panel652_machine_20261101 as M


def signed8(value):
    return ((value + 128) & 255) - 128


def profiles():
    result = []
    for pattern in ['empty', 'active15', 'sentinel127', 'unmapped', 'flags-off', 'mixed']:
        for mode in [0, 3, 128, 255]:
            for salt in range(3):
                slots = []
                for index in range(36):
                    tag = 15 if pattern == 'active15' else 127 if pattern == 'sentinel127' else 128 if pattern == 'unmapped' else [128, 255, 0, 1, 12, 13, 14, 15, 16, 17, 18, 127][(index + salt) % 12]
                    present = pattern != 'empty' and (pattern != 'mixed' or index % 4 != 0)
                    flags = 0xA5000000 | (0 if pattern == 'flags-off' or pattern == 'mixed' and index % 4 == 1 else 2)
                    slots.append(dict(present=present, flags=flags, tag=tag, coordinates=[[0, 127, 128, 255], [255, 128, 127, 0], [1, 254, 128, 129]][(index + salt) % 3]))
                first = [[0, 255], [128, 127], [254, 1]] if salt == 0 else [[128, 255], [1, 254], [127, 0]] if salt == 1 else [[127, 128], [255, 0], [128, 255]]
                result.append(dict(name='%s-mode%d-salt%d' % (pattern, mode, salt), pattern=pattern, mode=mode, slots=slots, firstCoordinates=first))
    return result


def model(result, mapping):
    p = result['profile']
    keys = [signed8(mapping[index]) for index in range(0, 63, 3)]
    expected, draws, map_calls = bytearray(result['before']), [], []
    def lookup(key):
        map_calls.append(key & 0xFFFFFFFF)
        return 127 if key == 127 else keys.index(key) if key in keys else 0
    initial = []
    if p['mode'] != 3:
        for index in range(2):
            initial.append([M.CONTEXT] + [signed8(values[index]) & 0xFFFFFFFF for values in p['firstCoordinates']] + [2])
    for index, slot in enumerate(p['slots']):
        if not slot['present'] or slot['flags'] & 2 != 2:
            continue
        tag = signed8(slot['tag'])
        mapped = lookup(tag)
        if mapped == 127:
            continue
        if tag == 127:
            raise ValueError('652 stable pure mapping cannot enter inner sentinel branch')
        if tag == 15:
            if 8 <= index <= 14:
                tag = 13
                expected[M.SLOTS - M.BASE + 12 * index + 5] = tag
            if 15 <= index <= 21:
                tag = lookup(14)
                expected[M.SLOTS - M.BASE + 12 * index + 5] = tag
            mapped = lookup(tag)
        draws.append([M.DESCRIPTORS + 12 * mapped] + [signed8(value) & 0xFFFFFFFF for value in slot['coordinates']])
    lo, hi = M.STACK - 65536 - M.BASE, M.STACK + 256 - M.BASE
    if bytes(expected[:lo]) != result['after'][:lo] or bytes(expected[hi:]) != result['after'][hi:]:
        raise ValueError(('652 independent complete nonstack RAM model differs', p['name']))
    expected_providers = ([(0x0206B324, [0])] if p['mode'] == 3 else [])
    expected_providers += [(0x0206006C, words) for words in draws]
    expected_providers += [(M.LOW, [mode, index]) for mode in [1, 2] for index in range(35)]
    if [(event['entry'], event['preparedWords']) for event in result['providedCalls']] != expected_providers:
        raise ValueError('652 prepared rendering/cleanup contracts or order differ')
    if [record['preparedWords'] for record in result['nativeReturns'] if record['entry'] == M.CONSTRUCTOR] != initial:
        raise ValueError('652 actual zero-count constructor five-word view differs')
    getter = [record for record in result['nativeReturns'] if record['entry'] == M.GETTER]
    if [(record['preparedWords'][0], record['returnedWords'][0]) for record in getter] != [(index, M.SLOTS + 12 * index) for index in range(36)]:
        raise ValueError('652 actual slot getter addresses/order differ')
    observed = [record for record in result['nativeReturns'] if record['entry'] == M.MAPPER]
    if [record['preparedWords'][0] for record in observed] != map_calls:
        raise ValueError('652 original native mapping input sequence differs')
    for record in observed:
        key = record['preparedWords'][0]
        key = key - 0x100000000 if key & 0x80000000 else key
        wanted = 127 if key == 127 else keys.index(key) if key in keys else 0
        if record['returnedWords'][0] != wanted:
            raise ValueError('652 original native first-match/sentinel mapping differs')
    if result['coreRegistersAndCpsr'][0] != 35:
        raise ValueError('652 physical final cleanup-loop return differs')
    return dict(draws=draws, firstFiveWordCalls=initial, mapInputWords=map_calls, updatedTagBytes=[expected[M.SLOTS - M.BASE + 12 * index + 5] for index in range(36)], finalPhysicalR0=35)
