import itertools
import struct

CONTEXT, MODE_BYTE, MODE_WORD, OFF_BYTE = 0x0223989C, 0x020F69E8, 0x020DD9BC, 0x021C0F00
POOLS = (0x02236F6C, 0x022362AC, 0x022355EC, 0x02237C2C)
INFO = 0x02370000


def recipes():
    rows = [dict(argument=argument, mode=mode, word=word, off=off, profile=index % 10)
        for index, (argument, mode, word, off) in enumerate(itertools.product(
            [0, 1, 0xFFFFFFFF, 0x80000000], [0, 1, 2, 4, 5, 7, 9, 255], [0, 9, 0xFFFFFFFF], [0, 1, 255]))]
    rows += [dict(argument=argument, mode=0, word=0, off=0, profile=profile)
        for argument, profile in itertools.product([0, 1, 0xFFFFFFFF, 0x80000000], range(10))]
    return [dict(row, seed=0x160000 + index, flag18=[0, 1, 2, 128, 255][index % 5],
        flag19=[255, 0, 128, 2, 1][(index // 5) % 5]) for index, row in enumerate(rows)]


def construct(recipe, rng):
    context = bytearray(rng.randbytes(0x30))
    context[0x18], context[0x19] = recipe['flag18'], recipe['flag19']
    initial = [(CONTEXT, bytes(context)), (MODE_BYTE, bytes([recipe['mode']])),
        (MODE_WORD, struct.pack('<I', recipe['word'])), (OFF_BYTE, bytes([recipe['off']]))]
    actors = {}
    for side in range(2):
        pool = bytearray(rng.randbytes(3 * 1088))
        for slot in range(3):
            address, info = POOLS[side] + slot * 1088, INFO + side * 0x1000 + slot * 0x100
            ready, excluded, detail, action = 1, 0, 0, [0, 1, 255][slot]
            profile = recipe['profile']
            if profile in [1, 2, 3] and slot == profile - 1:
                action = 2
            elif profile == 4:
                ready, action = 0, 2
            elif profile == 5:
                excluded, action = 255, 2
            elif profile == 6:
                detail, action = 128, 2
            elif profile == 7:
                ready, excluded, detail, action = [0, 255, 128][slot], [0, 1, 0][slot], [0, 0, 255][slot], 2
            elif profile == 8:
                ready, action = 255, 255
            elif profile == 9:
                action = 2
            offset = slot * 1088
            pool[offset + 0x31C], pool[offset + 0x1FF], pool[offset + 0x322] = ready, excluded, action
            struct.pack_into('<I', pool, offset + 0x1E8, info)
            initial.append((info, rng.randbytes(0xAC) + bytes([detail])))
            actors[address] = dict(eligible=int(ready != 0 and excluded == 0 and detail == 0), action=action)
        initial.append((POOLS[side], bytes(pool)))
    entries, returns = [], []

    def enter(address, arguments=()):
        entries.append(dict(address=hex(address), arguments=list(arguments)))

    def leave(address, result):
        returns.append(dict(address=hex(address), result=result))
        return result

    def scalar(address, result, arguments=()):
        enter(address, arguments)
        return leave(address, result)

    enter(0x020444A8)
    enter(0x020444EC)
    scalar(0x020443EC, recipe['mode'])
    blocked = leave(0x020444EC, int(recipe['mode'] in [2, 4]))
    if not blocked:
        enter(0x0204453C)
        scalar(0x020443EC, recipe['mode'])
        blocked = leave(0x0204453C, int(recipe['mode'] == 5))
    if not blocked:
        blocked = scalar(0x02044520, int(recipe['word'] == 9))
    if not blocked:
        blocked = int(scalar(0x020443EC, recipe['mode']) == 7)
    leave(0x020444A8, blocked)
    result = int(context[0x18 if recipe['argument'] == 0 else 0x19] == 0)
    if not blocked:
        if scalar(0x020655D8, recipe['off']):
            result = 0
        else:
            side = 1 if recipe['argument'] == 0 else 0
            for slot in range(3):
                address = POOLS[side] + slot * 1088
                scalar(0x021DB438, address, [side, slot])
                eligible = scalar(0x021DB8D0, actors[address]['eligible'], [address])
                if eligible and actors[address]['action'] == 2:
                    result = 0
                    break
    return initial, result, entries, returns
