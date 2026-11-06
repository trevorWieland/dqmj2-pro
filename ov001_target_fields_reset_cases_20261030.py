import random
import struct

TEAMS = (0x02236F6C, 0x022362AC, 0x022355EC, 0x02237C2C)
RECORDS, INPUT = 0x02370000, 0x02378000


def vectors():
    result = []
    for side in (0, 1, 2, 255):
        for mask in range(8):
            for invalid_kind in range(3):
                seed = 910000 + len(result)
                rng = random.Random(seed)
                memory, patches = [], []
                source = bytearray(rng.randbytes(1088))
                source[0x31E] = side
                memory.append((INPUT, bytes(source)))
                selected = 1 if side == 0 else 0
                for team, base in enumerate(TEAMS):
                    for index in range(3):
                        actor = bytearray(rng.randbytes(1088))
                        record = bytearray(rng.randbytes(528))
                        pointer = RECORDS + (team * 3 + index) * 528
                        valid = bool(mask >> index & 1)
                        actor[0x31C] = (1, 128, 255)[index]
                        actor[0x1FF] = 0
                        record[0xAC] = 0
                        if not valid:
                            if invalid_kind == 0:
                                actor[0x31C] = 0
                                pointer = 0
                            elif invalid_kind == 1:
                                actor[0x1FF] = (1, 128, 255)[index]
                                pointer = 0
                            else:
                                record[0xAC] = (1, 128, 255)[index]
                        struct.pack_into('<I', actor, 0x1E8, pointer)
                        struct.pack_into('<HH', actor, 0x340, (0, 0xFFFF, 0x8000)[index],
                                         (0x7FFF, 1, 0)[index])
                        memory.append((base + index * 1088, bytes(actor)))
                        if pointer:
                            memory.append((pointer, bytes(record)))
                        if team == selected and valid:
                            patches.append((base + index * 1088 + 0x340, b'\xff' * 4))
                physical_r0 = TEAMS[selected] + 2 * 1088 + 0x300 if mask & 4 else 0
                result.append({'seed': seed, 'side': side, 'validMask': mask,
                               'invalidKind': invalid_kind, 'memory': memory,
                               'patches': patches, 'physicalR0': physical_r0})
    return result
