import struct
from itertools import product

from ov001_damage_pipeline_cases_20261030 import ATTACKER, TARGET, ATTACKER_RECORD, TARGET_RECORD, STAGES


def vectors(blob):
    mode = struct.unpack_from('<H', blob, 16)[0]
    if mode & 15 != 1 or (mode >> 8) & 15 == 7:
        raise ValueError('Original action0 is no longer the measured ordinary attack mode')
    output = []
    for side, control, critical, final_flag, seed in product((0, 1), (0, 1, 2, 3), (0, 1), (0, 1), (0, 1, 0xFFFFFFFF, 0xA5821347)):
        state, draws = seed, []

        def random_value(limit):
            nonlocal state
            state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            result = (state >> 16) % limit if limit > 0 else 0
            draws.append((limit, result))
            return result

        def controlled(limit):
            return random_value(limit) if control in (0, 3) else limit - 1 if control == 2 else 0

        base = 45 + controlled(5) - 2 + controlled(3) - 2
        critical_value = max(95 + random_value(10), base * 12 // 10) if critical else base
        final = critical_value * (2 if final_flag else 1)
        actor, target = bytearray(1088), bytearray(1088)
        for data, record, team in ((actor, ATTACKER_RECORD, side), (target, TARGET_RECORD, 1 - side)):
            struct.pack_into('<I', data, 0x1E8, record)
            struct.pack_into('<h', data, 0x1F8, 1000)
            struct.pack_into('<h', data, 0x220, 100)
            struct.pack_into('<h', data, 0x222, 20)
            data[0x31C], data[0x31E] = 1, team
        protocols = []
        value = base
        for address in STAGES:
            incoming = 0 if address == STAGES[0] else value
            if address == 0x021F00C4:
                value = critical_value
            if address == 0x021F045C:
                value = final
            protocols.append(dict(address=address, arguments=[incoming], returnWord=value))
        protocols[-3]['arguments'] = [critical_value, 0, TARGET, final_flag]
        output.append(dict(side=side, control=control, critical=critical, finalFlag=final_flag, initialRng=seed,
                           baseValue=base, criticalValue=critical_value, physicalR0=final,
                           arguments=[ATTACKER, TARGET, 0, critical, 0, 0, control, 0, 0, 0, final_flag],
                           seed=1530000 + len(output), draws=draws, protocols=protocols,
                           memory=[(ATTACKER, bytes(actor)), (TARGET, bytes(target)),
                                   (ATTACKER_RECORD, bytes(192)), (TARGET_RECORD, bytes(192)),
                                   (0x020DDD40, bytes(4)), (0x020F6044, struct.pack('<I', seed))],
                           patches=[(0x020F6044, struct.pack('<I', state))]))
    return output
