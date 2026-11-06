import random
import struct

BASES = (0x02238D1C, 0x02238D2E)


def vectors():
    result = []
    for side in (0, 1, 2, 3, 255, 0xFFFFFFFF, 0x80000000):
        for slot in range(3):
            for variant in range(4):
                seed = 1110000 + len(result)
                data = bytearray(random.Random(seed).randbytes(36))
                for index in range(6):
                    struct.pack_into('<H', data, index * 6, (0, 65535, 32768, 32767)[variant])
                    data[index * 6 + 2] = (0, 1, 128, 255)[variant]
                selected = BASES[0 if side == 0 else 1]
                address = selected + slot * 6
                result.append({'seed': seed, 'side': side, 'slot': slot, 'variant': variant,
                               'memory': [(BASES[0], bytes(data))],
                               'patches': [(address, b'\x06\x00'), (address + 3, b'\xff\x01')],
                               'physicalR0': selected + 4})
    return result
