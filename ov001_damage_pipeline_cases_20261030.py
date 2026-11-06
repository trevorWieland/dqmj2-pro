import struct
from itertools import product

ATTACKER, TARGET = 0x02360000, 0x02370000
ATTACKER_RECORD, TARGET_RECORD = 0x02350000, 0x02350100
STAGES = (0x021EF4CC, 0x021EF638, 0x021EF878, 0x021EF8D0, 0x021EFAF4, 0x021EFB14,
          0x021EFCF8, 0x021EFB6C, 0x021EFBF4, 0x021EFC7C, 0x021EFD88, 0x021EFDE0,
          0x021EFE44, 0x021EFEDC, 0x021F0030, 0x021F0084, 0x021F01BC, 0x021F00C4,
          0x021EFB88, 0x021F01D4, 0x021F021C, 0x021F0288, 0x021F02A0, 0x021F0254,
          0x021F02E8, 0x021F0354, 0x021F0380, 0x021F03C8, 0x021F040C, 0x021F045C,
          0x021F049C, 0x021F056C)


def vectors(blob):
    output = []
    for action in (6, 7):
        if struct.unpack_from('<H', blob, 8 + action * 40 + 8)[0] != 0 or blob[8 + action * 40 + 0x1F] != 0:
            raise ValueError('Original zero-mode action fixture changed')
        for side in (0, 1):
            for option6, option9, flag in product((1, 0x80000000, 0xFFFFFFFF), (0, 1), (0, 1, 0x80000000, 0xFFFFFFFF)):
                actor = bytearray(1088)
                target = bytearray(1088)
                struct.pack_into('<I', actor, 0x1E8, ATTACKER_RECORD)
                struct.pack_into('<I', target, 0x1E8, TARGET_RECORD)
                actor[0x31E], target[0x31E] = side, 1 - side
                protocols = [dict(address=address, arguments=[0], returnWord=0) for address in STAGES]
                protocols[-3]['arguments'] = [0, action, TARGET, flag]
                output.append(dict(action=action, side=side, option6=option6, option9=option9, finalFlag=flag, physicalR0=0,
                                   arguments=[ATTACKER, TARGET, action, 0, 0, 0, option6, 0, 0, option9, flag],
                                   seed=1510000 + len(output), draws=[], protocols=protocols, patches=[],
                                   memory=[(ATTACKER, bytes(actor)), (TARGET, bytes(target)),
                                           (ATTACKER_RECORD, bytes(192)), (TARGET_RECORD, bytes(192)),
                                           (0x020F6044, struct.pack('<I', 0xA5820000 + len(output)))]))
    return output
