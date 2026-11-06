import itertools
import struct

CONTEXT, GLOBAL = 0x0221C06C, 0x020DEB2C
CALLBACKS = [(0x021F5870, 'thumb'), (0x02500100, 'thumb'), (0x02500200, 'arm')]


def recipes():
    return [dict(seed=0x212000 + index, variant=index, first=(index * 0xF1234567) & 0xFFFFFFFF,
        mode=mode, flags=flags, iterations=iterations, initDone=index % 5 == 0)
        for index, (mode, flags, iterations) in enumerate(itertools.product(
            [0, 1, 2, 6, 7, 0xFFFFFFFF, 0x80000000], [0, 1, 2, 16, 17, 32, 48, 0x80000010, 0x80000000], [1, 3]))]


def construct(recipe, rng):
    context = bytearray(rng.randbytes(32))
    original = bytes(context)
    old = rng.getrandbits(32)
    global_word = old
    events, services = [], []

    def write(address, content):
        nonlocal global_word
        if address == GLOBAL:
            global_word = struct.unpack('<I', content)[0]
        elif CONTEXT <= address < CONTEXT + 32:
            context[address - CONTEXT:address - CONTEXT + len(content)] = content
        else:
            raise ValueError('Loop212 independent effect address differs')

    def native(address, arguments, result, effects):
        events.append(dict(address=address, arguments=arguments, result=result, contextBefore=bytes(context), globalBefore=global_word))
        for a, content in effects:
            write(a, content)

    def provider(address, arguments=(), effects=(), mode='thumb'):
        services.append(dict(address=address, arguments=list(arguments), result=rng.getrandbits(32), effects=list(effects),
            contextBefore=bytes(context), globalBefore=global_word, mode=mode))
        for a, content in effects:
            write(a, content)

    write(CONTEXT + 4, struct.pack('<I', recipe['first']))
    mode, flags = recipe['mode'], recipe['flags']
    valid = mode <= 6 and (flags & 15) <= 1 and not flags & 32 and (bool(flags & 16) if mode == 0 else not flags & 16)
    native(0x021F4FC0, [mode, flags], int(valid), [(CONTEXT, bytes([mode & 255])), (CONTEXT + 8, struct.pack('<I', flags))])
    if valid:
        native(0x0209747C, [], old, [])
        native(0x02097470, [0x0220D974], 0x0220D974, [(GLOBAL, struct.pack('<I', 0x0220D974))])
        write(CONTEXT + 1, b'\0')
        provider(0x021F5010, effects=[(CONTEXT + 16, rng.randbytes(4)), (CONTEXT + 1, b'\x80')])
        provider(0x021F50B0, effects=[(CONTEXT + 1, b'\0')])
        provider(0x021FF628, effects=[(CONTEXT + 1, b'\xFF' if recipe['initDone'] else b'\0')])
        native(0x021F52CC, [0x021F5871], 0x021F5871, [(CONTEXT + 12, struct.pack('<I', 0x021F5871))])
        iterations = 1 if recipe['initDone'] else recipe['iterations']
        for iteration in range(iterations):
            callback, callback_mode = CALLBACKS[(recipe['variant'] + iteration) % len(CALLBACKS)]
            pointer = callback | int(callback_mode == 'thumb')
            stop_index = recipe['variant'] % 6
            target = [0x02203CF0, callback, 0x022048A8, 0x02204150, 0x022047AC, 0x02008070]
            for ordinal, address in enumerate(target):
                effects = [(CONTEXT + 16, rng.randbytes(4))]
                if ordinal == 0:
                    effects.append((CONTEXT + 12, struct.pack('<I', pointer)))
                if ordinal == 1:
                    effects.append((GLOBAL, rng.randbytes(4)))
                if iteration == iterations - 1 and ordinal == stop_index:
                    effects.append((CONTEXT + 1, bytes([[1, 128, 255][recipe['variant'] % 3]])))
                provider(address, [0] if ordinal == 2 else [], effects,
                    callback_mode if ordinal == 1 else ('arm' if ordinal == 5 else 'thumb'))
        provider(0x021F527C, effects=[(GLOBAL, rng.randbytes(4)), (CONTEXT + 20, rng.randbytes(4))])
        native(0x02097470, [old], old, [(GLOBAL, struct.pack('<I', old))])
    return original, old, bytes(context), global_word, events, services, 0 if valid else 0xFFFFFFFF
