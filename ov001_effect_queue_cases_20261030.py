import random
import struct

QUEUE, POOL, STRIDE = 0x02238DEC, 0x021043AC, 0x11C
KINDS = (0xFFFFFFFF, 0xFFFFFFFE, 0x80000000, 0, 1, 2, 0x7FFFFFFF)


def full_pool(seed, pattern):
    rng = random.Random(seed)
    data = bytearray(rng.randbytes(STRIDE * 32))
    for index in range(32):
        data[index * STRIDE] = (1, 255, 1 + index % 254)[pattern]
    return bytes(data)


def dependency_protocols(identifier, actor, kind, include_constructor):
    calls = []
    if include_constructor:
        calls.append(dict(address=0x021EEC7C, arguments=[identifier, actor, kind], returnWord=0xFFFFFFFF))
    if kind < 0x80000000:
        calls += [dict(address=0x0205CBA4, arguments=[identifier, actor, kind], returnWord=0xFFFFFFFF),
                  dict(address=0x0205C9D8, returnWord=0xFFFFFFFF)]
    return calls


def queue_vectors():
    output = []
    for first in range(-1, 10):
        for identifier in (0, 65535, 0xFFFFFFFF):
            for actor in (0, 0x02370000, 0xFFFFFFFF):
                for kind in KINDS:
                    seed = 1430000 + len(output)
                    occupied = (0, 1, 0xFFFFFFFE, 0x80000000, 0x7FFFFFFF, 0x80000001)
                    queue = [occupied[(seed + index) % len(occupied)] for index in range(10)]
                    if first >= 0:
                        queue[first] = 0xFFFFFFFF
                        for index in range(first + 1, 10):
                            if (index + seed) % 2:
                                queue[index] = 0xFFFFFFFF
                    memory = [(QUEUE, struct.pack('<10I', *queue))]
                    protocols, patches = [], []
                    if first >= 0:
                        protocols = dependency_protocols(identifier, actor, kind, True)
                        patches.append((QUEUE + first * 4, bytes.fromhex('ffffffff')))
                        if kind < 0x80000000:
                            memory.append((POOL, full_pool(seed, first % 3)))
                    output.append(dict(seed=seed, firstFree=first, queueWords=[hex(word) for word in queue],
                                       identifierWord=hex(identifier), actorWord=hex(actor), kindWord=hex(kind),
                                       arguments=[identifier, actor, kind], memory=memory, patches=patches,
                                       protocols=protocols, draws=[], physicalR0=int(first >= 0)))
    return output


def constructor_vectors():
    output = []
    for identifier in (0, 65535, 0xFFFFFFFF):
        for actor in (0, 0x02370000, 0xFFFFFFFF):
            for kind in KINDS:
                for pattern in ((0,) if kind >= 0x80000000 else (0, 1, 2)):
                    seed = 1440000 + len(output)
                    memory = [] if kind >= 0x80000000 else [(POOL, full_pool(seed, pattern))]
                    output.append(dict(seed=seed, identifierWord=hex(identifier), actorWord=hex(actor),
                                       kindWord=hex(kind), poolPattern=pattern, arguments=[identifier, actor, kind],
                                       memory=memory, patches=[], draws=[], physicalR0=0xFFFFFFFF,
                                       protocols=dependency_protocols(identifier, actor, kind, False)))
    return output
