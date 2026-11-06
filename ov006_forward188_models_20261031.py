import random

BUFFER, FONT = 0x0301FE6C, 0x021C9698


def recipes():
    rows = []
    for index in range(192):
        rng = random.Random(0x188000 + index)
        words = [rng.getrandbits(32) for unused in range(7)]
        words[4] = [0, 1, 127, 128, 255, 256, 0x800000FF, 0xFFFFFFFF][index % 8]
        words[5] = [0, 1, 0x80000000, 0xFFFFFFFF][index % 4]
        words[6] = [0xFFFFFFFF, 0x80000000, 1, 0][(index // 4) % 4]
        rows.append(dict(seed=0x188000 + index, arguments=words,
            result=[0, 1, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF, 0xFFFF0001][index % 6]))
    return rows


def construct(recipe):
    rng = random.Random(recipe['seed'] ^ 0x800000)
    buffer = rng.randbytes(128)
    words = recipe['arguments']
    return [dict(address=0x02046AF4, arguments=[FONT, words[1], words[4] & 255, 0, BUFFER, 255],
            result=rng.getrandbits(32), bufferBefore=b'\0' * 128, bufferAfter=buffer),
        dict(address=0x021E775C, arguments=[words[0], BUFFER, words[2], words[3], *words[4:7]],
            result=recipe['result'], bufferBefore=buffer, bufferAfter=buffer[:-4] + b'\xFF\0\x80\x7F')]
