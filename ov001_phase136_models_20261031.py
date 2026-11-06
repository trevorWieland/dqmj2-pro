import itertools
import struct

CONTEXT, DESCRIPTOR = 0x0223989C, 0x02380000


def recipes():
    return [dict(seed=0x136000 + index, variant=index, phase=phase, counter=counter, nibble=nibble, out=out, ready=ready)
        for index, (phase, counter, nibble, out, ready) in enumerate(itertools.product(
            [0, 10, 100, 255], [0, 14, 15, 16, 254, 255], [0, 1, 15], [0, 1], [0, 0xFFFFFFFF]))]


def construct(recipe, raw_context):
    context = bytearray(raw_context)
    v = recipe['variant']
    initial50 = (v * 1709) & 65535
    struct.pack_into('<H', context, 0x50, initial50)
    initial = [(CONTEXT, bytes(context)), (DESCRIPTOR + 8, struct.pack('<H', (recipe['nibble'] << 12) | (v & 4095)))]
    calls = []

    def call(address, arguments, result=0, effects=(), stackOutput=None):
        calls.append(dict(address=address, arguments=arguments, result=result, effects=list(effects), stackOutput=stackOutput))
        for offset, content in effects:
            context[offset:offset + len(content)] = content

    latest50 = (initial50 ^ 0xFFFF) & 65535
    word80 = [0, 1, 0x80000000, 0xFFFFFFFF][v % 4]
    word84 = [0xFFFFFFFF, 0x80000000, 1, 0][v % 4]
    call(0x0207AFEC, [initial50], DESCRIPTOR, effects=[(0x20, bytes([recipe['phase']])), (0x1F, bytes([recipe['counter']])),
        (0x50, struct.pack('<H', latest50)), (0x80, struct.pack('<II', word80, word84))])
    if context[0x20] == 0:
        call(0x021F521C, [word84, word80 if recipe['nibble'] == 0 else 0, latest50, 0, 'sp+4'],
            0x80000000, [(0x84, struct.pack('<I', word84 ^ 0xFFFFFFFF)), (0x20, b'\xFF'), (0x1F, b'\xFF')], recipe['out'])
        if recipe['out']:
            call(0x021E215C, [word84 ^ 0xFFFFFFFF], 0xFFFFFFFF, [(0x20, b'\x80'), (0x1F, b'\xFD'), (0x1B, b'\x80')])
        context[0x1F], context[0x20] = 0, 10
    if context[0x20] == 10:
        context[0x1F] = (context[0x1F] + 1) & 255
        if context[0x1F] > 15:
            call(0x02212290, [], recipe['ready'], [(0x20, bytes([100 if recipe['out'] else 255]))])
            if recipe['ready'] == 0:
                context[0x20] = 100
    if context[0x20] == 100:
        context[0x20], context[0x1B] = 0, 27
    return initial, bytes(context), calls
