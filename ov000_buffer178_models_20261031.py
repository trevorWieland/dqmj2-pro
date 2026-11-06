import itertools
import struct

CONTEXT, POINTERS, TEXT, FONT = 0x02238520, 0x02238514, 0x0223852B, 0x021C9698
OBJECTS = (0x023A0000, 0x023A1000)
BUFFER = 0x0301FE70


def signed16(value):
    return ((value & 65535) ^ 32768) - 32768


def signed32(value):
    return (value ^ 0x80000000) - 0x80000000


def recipes():
    return [dict(seed=0x178000 + index, variant=index, selector=selector, valid=valid, alignment=alignment, width=width,
        length=[0, 1, 7, 63][index % 4], x=[-32768, -1, 0, 32767][(index // 4) % 4],
        y=[32767, 0, -1, -32768][index % 4], flags=[0, 1, 128, 255][(index // 3) % 4])
        for index, (selector, valid, alignment, width) in enumerate(itertools.product(
            [0, 1, 128, 255], [False, True], [0, 1, 2, 3, 255], [0, 1, 2, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF]))]


def construct(recipe, rng):
    context = bytearray(rng.randbytes(11))
    context[8], context[9], context[10] = recipe['selector'], 99, 77
    selected = 1 if recipe['selector'] == 0 else 0
    pointers = list(OBJECTS)
    if not recipe['valid']:
        pointers[selected] = 0
    objects = {a: bytearray(rng.randbytes(128)) for a in OBJECTS}
    initial = [(CONTEXT, bytes(context)), (POINTERS, struct.pack('<II', *pointers))] + [(a, bytes(b)) for a, b in objects.items()]
    if not recipe['valid']:
        return initial, [], [], [], 0
    address = OBJECTS[selected]
    late_word, late_byte = (recipe['variant'] * 0x10204081) & 0xFFFFFFFF, [0, 1, 255][recipe['variant'] % 3]
    services = []
    final = {CONTEXT: context, **objects}

    def effect(address, content):
        for base, data in final.items():
            if base <= address < base + len(data):
                data[address - base:address - base + len(content)] = content
                break

    def call(pc, arguments, result=0, effects=(), buffer_before=None):
        services.append(dict(address=pc, arguments=arguments, result=result, effects=list(effects), bufferBefore=buffer_before))
        for a, data in effects:
            effect(a, data)

    call(0x020852B0, [address + 0x3C, TEXT], 0xFFFFFFFF,
        [(address + 0x68, struct.pack('<I', late_word)), (address + 0x5E, bytes([late_byte])),
            (CONTEXT, struct.pack('<hh', 0x3333, 0x4444)), (CONTEXT + 8, bytes([recipe['selector'] ^ 255]))], b'\0' * 128)
    text = b''.join(struct.pack('<H', 1 + ((recipe['variant'] * 173 + i * 257) % 65535)) for i in range(recipe['length']))
    buffer = text + b'\0' * (128 - len(text))
    call(0x02046AF4, [FONT, late_word, late_byte, 0, BUFFER, 255], 0x80000000,
        [(BUFFER, buffer), (CONTEXT, struct.pack('<hh', recipe['x'], recipe['y']))], b'\0' * 128)
    final[address][0x6C:0x6E] = struct.pack('<H', recipe['length'])
    call(0x02087674, [FONT, address + 0x3C, BUFFER], recipe['width'],
        [(CONTEXT, struct.pack('<hh', signed16(recipe['x'] ^ 65535), signed16(recipe['y'] ^ 65535))),
            (CONTEXT + 9, bytes([recipe['alignment'], recipe['flags']])), (BUFFER, b'\xFF\xFF')], buffer)
    changed_buffer = b'\xFF\xFF' + buffer[2:]
    x = recipe['x']
    if recipe['alignment'] == 1:
        x = signed16(x - (signed32(recipe['width']) >> 1))
    elif recipe['alignment'] == 2:
        x = signed16(x - recipe['width'])
    call(0x02087A48, [address, 0, x & 0xFFFFFFFF, recipe['y'] & 0xFFFFFFFF, recipe['flags'], BUFFER],
        [0, 0x80000000, 0xFFFFFFFF][recipe['variant'] % 3], [(address + 0x6C, b'\xEF\xBE')], changed_buffer)
    native = [dict(address='0x2008be0', arguments=[0, BUFFER, 128], result=0),
        dict(address='0x20470fc', arguments=[BUFFER], result=recipe['length'])]
    return initial, [(a, bytes(b)) for a, b in final.items()], services, native, 1
