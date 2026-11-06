import struct

CONTEXT, RAW_STATE = 0x02239A14, 0x020F6102


def recipes():
    rows = []
    for phase_b in (0, 10, 100, 7):
        for phase_9 in (0, 10, 100, 7):
            for phase_2 in (0, 10, 20, 100, 7):
                index = len(rows)
                rows.append(dict(seed=0x158000 + index, phase19=(0, 100)[index % 2], phaseB=phase_b, phase9=phase_9, phase2=phase_2,
                    counter13=(0, 23, 24, 25, 30, 31, 254, 255)[index % 8], counter8=(0, 29, 30, 31, 254, 255)[index % 6],
                    ready=(0, 1, 0xFFFFFFFF)[index % 3], rawState=(0, 1, 255)[index % 3]))
    for phase19 in (0, 100, 7):
        for counter in (24, 25, 30, 255):
            rows.append(dict(seed=0x158000 + len(rows), phase19=phase19, phaseB=100, phase9=10, phase2=10,
                counter13=counter, counter8=counter, ready=1, rawState=255))
    return rows


def model(recipe, initial):
    result, calls = bytearray(initial), []

    def call(address, arguments, return_word=0xDEAD1234, writes=None):
        calls.append(dict(address=address, arguments=arguments, result=return_word, writes=writes or []))

    if result[0x19] == 0:
        call(0x021F1354, [1, 2, 0, 1])
        call(0x021F989C, [])
        result[0x19] = 100
    if result[0xB] == 0:
        call(0x021E3564, [0x16, 1])
        call(0x021F949C, [0xE9, 1])
        result[0xB] = 10
    if result[0xB] == 10:
        call(0x021E3584, [], recipe['ready'])
        if recipe['ready']:
            call(0x021E3564, [0x17, 1])
            result[0xB] = 100
    if result[9] == 0:
        result[0x13], result[9] = 0, 10
    if result[9] == 10:
        word = (31 - result[0x13]) & 0xFFFFFFFF
        call(0x021D8CC8, [(word | word << 5 | word << 10) & 0xFFFF])
        result[0x13] = (result[0x13] + 1) & 255
        if result[0x13] > 24:
            result[9] = 100
    if result[2] == 0:
        result[8], result[2] = 0, 10
    writes = []
    if result[2] == 10:
        result[8] = (result[8] + 1) & 255
        if result[8] > 30:
            writes = [(RAW_STATE, bytes([recipe['rawState']]))]
            call(0x02041510, [1, 3, 15], writes=writes)
            result[2] = 20
    native = result[2] == 20
    if native and recipe['rawState'] != 1:
        result[2] = 100
    if all(result[offset] == 100 for offset in (0x19, 0xB, 9, 2)):
        for offset in (0x19, 0xB, 9, 2):
            result[offset] = 0
        result[10] = 3
    return result, calls, native, writes
