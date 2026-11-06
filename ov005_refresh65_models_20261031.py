import struct

CONTEXT, SELECTION, INPUT, RAW_BYTE = 0x021ED438, 0x021ED348, 0x020EDEB8, 0x021D423D


def recipes():
    return [dict(seed=0x165000 + index, counter=counter, flags=flags, raw=value, cached=value if variant == 0 else value ^ 255)
        for index, (counter, flags, value, variant) in enumerate((counter, flags, value, variant)
            for counter in (0, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF) for flags in (0, 2, 3, 0xFFFF)
            for value, variant in ((0, 0), (128, 1), (255, 1)))]


def model(recipe, initial):
    result, services = bytearray(initial), []
    struct.pack_into('<I', result, 0x20, (recipe['counter'] + 1) & 0xFFFFFFFF)

    def call(address, arguments=(), return_word=0xDEAD1234, writes=(), probes=()):
        services.append(dict(address=address, arguments=list(arguments), result=return_word, writes=list(writes), probes=list(probes)))

    writes = [(RAW_BYTE, bytes([recipe['raw']]))]
    call(0x021E6004, [0], writes=writes, probes=[(CONTEXT + 0x20, bytes(result[0x20:0x24]))])
    call(0x02049604, [SELECTION, 1])
    call(0x021E653C, writes=[(CONTEXT + 1, bytes([recipe['cached']]))])
    result[1] = recipe['cached']
    if result[1] != recipe['raw']:
        result[1] = recipe['raw']
        call(0x02048094, [recipe['raw'], 0], probes=[(CONTEXT + 1, bytes([recipe['raw']]))])
        call(0x021E0818)
        call(0x021E0730, [0x13, 2, 3])
    if recipe['flags'] & 2:
        call(0x021E0818)
        call(0x021E1144, [0])
        struct.pack_into('<H', result, 0xC, 0)
        struct.pack_into('<I', result, 0x34, 0)
        result[2] = 30
        call(0x021E1048, [0x53], probes=[(CONTEXT + 0xC, bytes(2)), (CONTEXT + 0x34, bytes(4)), (CONTEXT + 2, b'\x1e')])
        call(0x021E0730, [0x13, 2, 0x1F])
        call(0x021E085C, [1])
        call(0x021E155C, [0x16], return_word=0xF0000016)
        return_word = 0xF0000016
    else:
        return_word = recipe['flags']
    return result, services, return_word, writes
