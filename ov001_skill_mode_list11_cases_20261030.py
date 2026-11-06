import struct
from itertools import product

MASK = 0xFFFFFFFF
SKILLS = 0x02358000
MODES = {17: 1, 18: 2, 19: 3, 20: 4, 21: 5, 22: 6, 70: 24, 250: 28}


def signed(word):
    return word - 0x100000000 if word & 0x80000000 else word


def boost(word):
    value = signed(word * 5 & MASK)
    return (abs(value) // 4 * (-1 if value < 0 else 1)) & MASK


def vectors(blobs):
    lists = [[], [0, 17], [17, 0, 18], [99], list(MODES), list(MODES)[::-1], [17, 17], [250, 17, 250]]
    lists += [[skill] for skill in MODES]
    lists += [[skill] * 64 for skill in MODES]
    rows = []
    for index, (skills, value, primary) in enumerate(product(lists, (0, 1, 5, 101, 9999, MASK, 0x80000000, 0x7FFFFFFF), (0, 1, 2, 3, 4, 5, 6, 24, 28))):
        action, secondary = 253, (0, 1, 28)[index % 3]
        metadata = bytearray(blobs['ActTbl.bin'][8 + action * 40:8 + (action + 1) * 40])
        metadata[0x1F], metadata[0x20] = primary, secondary
        result, protocols = value, []
        for skill in skills[:64]:
            if skill == 0:
                break
            if skill not in MODES:
                continue
            mode = MODES[skill]
            updated = boost(result) if mode in (primary, secondary) else result
            protocols.append(dict(address=0x0220EE3C, arguments=[action, result, mode], returnWord=updated))
            result = updated
        payload = bytes((skills + [0] * 64)[:64]) + bytes([17])
        rows.append(dict(skills=skills, initialValue=hex(value), primary=primary, secondary=secondary,
            physicalR0=result, seed=2080000 + index, draws=[], protocols=protocols,
            arguments=[SKILLS, action, value], memory=[(SKILLS, payload), (0x02320000 + action * 40, bytes(metadata))], patches=[]))
    return rows
