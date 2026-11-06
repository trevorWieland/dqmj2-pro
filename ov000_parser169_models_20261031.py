import itertools
import struct

POOL, INPUT, FLOAT_CONTEXT = 0x02234388, 0x02390000, 0x02391000
PREFIXES = (b'hasigo_', b'mapfix_', b'unknown')


def word(value):
    return value & 0xFFFFFFFF


def signed(value):
    return (value ^ 0x80000000) - 0x80000000


def bits(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def floating(value):
    return struct.unpack('<f', struct.pack('<I', value))[0]


def recipes():
    values = [0, 1, 17, 255, 256, -1, -17, -129, 524287, 524288, -524288, -524289, 0x7FFFFFFF, -0x80000000]
    return [dict(seed=0x169000 + index, slot=slot, branch=branch, first=word(value),
        second=word(-value if index % 2 else value), variant=index)
        for index, (slot, branch, value) in enumerate(itertools.product([-1, 0, 1, 31, 63], range(3), values))]


def construct(recipe, rng, setter_global):
    pool = bytearray(rng.randbytes(64 * 52))
    source = bytearray(rng.randbytes(64))
    source[:20] = b'##' + PREFIXES[recipe['branch']] + b'native\0xxxx'
    for slot in range(64):
        pool[slot * 52 + 0x1C] = 255
    if recipe['slot'] >= 0:
        pool[recipe['slot'] * 52 + 0x1C] = 0
    initial = [(POOL, bytes(pool)), (INPUT, bytes(source)), (setter_global + 4, rng.randbytes(4))]
    entries, returned, providers = [], [], []

    def native(address, arguments, result):
        entries.append(dict(address=hex(address), arguments=arguments))
        returned.append(dict(address=hex(address), result=word(result)))

    def provide(address, arguments, result, effects=()):
        providers.append(dict(address=address, arguments=arguments, result=word(result), effects=list(effects)))
        for address, data in effects:
            if POOL <= address < POOL + len(pool):
                pool[address - POOL:address - POOL + len(data)] = data

    native(0x021E3444, [], recipe['slot'])
    expected_extra = []
    if recipe['slot'] < 0:
        return initial, bytes(pool), expected_extra, entries, returned, providers, 0
    offset, address = recipe['slot'] * 52, POOL + recipe['slot'] * 52
    for destination, origin in [(0x18, 0x38), (0x0C, 0x2C), (0x10, 0x30), (0x14, 0x34), (0, 0x20), (4, 0x24), (8, 0x28)]:
        pool[offset + destination:offset + destination + 4] = source[origin:origin + 4]
    pool[offset + 0x1D] = 3
    native(0x021E3478, [address, INPUT, 3], address)
    difference = PREFIXES[recipe['branch']][0] - PREFIXES[0][0]
    native(0x0201D914, [INPUT + 2, 0x0222EC40, 7], difference)
    if recipe['branch'] == 0:
        provide(0x0201F274, [INPUT + 9], recipe['first'])
        pool[offset + 0x1E], pool[offset + 0x20] = recipe['first'] & 255, 2
    else:
        difference = PREFIXES[recipe['branch']][0] - PREFIXES[1][0]
        native(0x0201D914, [INPUT + 2, 0x0222EC48, 7], difference)
        if recipe['branch'] == 1:
            provide(0x0201F274, [INPUT + 9], recipe['first'])
            provide(0x0201F274, [INPUT + 9], recipe['second'])
            scaled = word(recipe['second'] << 12)
            converted = bits(signed(scaled))
            native(0x02025A28, [scaled], converted)
            if signed(recipe['first']) > 0:
                rounded = bits(0.5 + floating(converted))
                native(0x02024E0C, [bits(0.5), converted], rounded)
            else:
                rounded = bits(floating(converted) - 0.5)
                native(0x02025CA4, [converted, bits(0.5)], rounded)
            integral = max(-0x80000000, min(0x7FFFFFFF, int(floating(rounded))))
            native(0x020259B4, [rounded], integral)
            provide(0x020282A8, [0, word(integral)], recipe['variant'] ^ 0xAA55,
                [(address + 0x1E, b'\xEE'), (address + 0x20, b'\xEE')])
            pool[offset + 0x1E], pool[offset + 0x20] = 0, 1
            provide(0x021D8B24, [address, address + 0x0C], 0x80000000,
                [(address + 0x1C, b'\xEE'), (address + 0x20, b'\x80'), (address + 0x2C, struct.pack('<I', recipe['variant'] ^ 0x55AA))])
            native(0x021D8A08, [1], 1)
            expected_extra.append((setter_global + 4, struct.pack('<I', 1)))
    pool[offset + 0x1C] = 1
    return initial, bytes(pool), expected_extra, entries, returned, providers, 1
