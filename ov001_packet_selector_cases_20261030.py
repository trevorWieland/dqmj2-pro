import random
import struct

ADDRESS, STATE, PEERS = 0x022030B8, 0x02239D04, 0x02380000
ACTORS, INTENTS, COUNTS = 0x022362AC, 0x02238D2E, 0x022355E4


def vectors():
    output = []
    for count in range(4):
        for raw in (0, 1, 4, 5, 127, 255):
            for marker in (0, 1, 128, 255):
                for other in (0, 1):
                    seed = 1330000 + len(output)
                    rng = random.Random(seed)
                    state = bytearray(rng.randbytes(0x80))
                    peers = bytearray(rng.randbytes(0x100))
                    payloads = []
                    for peer in range(2):
                        struct.pack_into('<HH', peers, peer * 128, 0x1234, 0x8000)
                        payload = bytearray(rng.randbytes(0x7C))
                        payload[0] = (count + raw) % 2
                        payload[1:4] = bytes([raw, (raw + 1) & 255, raw])
                        for slot in range(3):
                            struct.pack_into('<HBBBx', payload, 4 + slot * 6,
                                             (0, 65535, 32767)[slot], (0, 1, 255)[slot],
                                             (4, 128, 255)[slot], marker)
                        peers[peer * 128 + 4:(peer + 1) * 128] = payload
                        payloads.append(payload)
                    packet = payloads[other]
                    memory = [(STATE, bytes(state)), (PEERS, bytes(peers)),
                              (COUNTS, bytes([0xA5, 0x5A, count, 0])),
                              (INTENTS, rng.randbytes(18)),
                              (0x020F69C4 + 0x1C, bytes(4)),
                              (0x020F69C4 + 0x0C, struct.pack('<I', rng.getrandbits(32))),
                              (0x021CEBE0, bytes(0x34)), (0x021CEBE0 + 6, bytes([other])),
                              (0x021C72A0, bytes(0x20)), (0x021C72A0 + 3, b'\x01'),
                              (0x021C72A0 + 0x18, b'\x03\x00'),
                              (0x021C9600, bytes(0x20)), (0x021C9600 + 8, b'\x80\x00'),
                              (0x021C9600 + 12, struct.pack('<I', PEERS)),
                              (0x021CEC60, b'\x34\x12')]
                    patches = [(STATE + 0x34, bytes([packet[0]])),
                               (STATE + 0x50, bytes(packet[0x1C:0x28])),
                               (STATE + 0x5C, bytes(packet[0x28:0x34])),
                               (0x020F69C4 + 0x0C, bytes(payloads[0][0x18:0x1C]))]
                    expected_actor_bytes = []
                    for slot in range(3):
                        actor = bytearray(rng.randbytes(1088))
                        actor[0x1FE] = packet[slot + 1] if slot == 1 else raw ^ 255
                        before_type, before_flags = actor[0x1FE], actor[0x35D]
                        memory.append((ACTORS + slot * 1088, bytes(actor)))
                        if packet[0] != 1 and slot < count:
                            value = packet[slot + 1]
                            flags = before_flags | 4 if before_type != value else before_flags
                            patches += [(ACTORS + slot * 1088 + 0x1FE, bytes([value])),
                                        (ACTORS + slot * 1088 + 0x35D, bytes([flags]))]
                            row = packet[4 + slot * 6:10 + slot * 6]
                            target_side, target_slot = int(row[2] != 1), 0 if row[3] == 4 else row[3]
                            patches += [(INTENTS + slot * 6, bytes(row[:2]) + bytes([target_side, target_slot, row[4]]))]
                            expected_actor_bytes.append(dict(slot=slot, before=before_type, after=value,
                                                             beforeFlags=before_flags, afterFlags=flags))
                    output.append(dict(seed=seed, count=count, raw=raw, marker=marker, other=other,
                                       memory=memory, patches=patches, expectedReturn=1,
                                       actorWrites=expected_actor_bytes, branch='received'))
    for failure in ('no-first-packet', 'no-second-packet', 'wrong-kind', 'wrong-header'):
        vector = dict(output[0])
        vector.update(seed=1340000 + len(output), branch=failure, expectedReturn=0, patches=[], actorWrites=[])
        vector['memory'] = list(vector['memory'])
        if failure == 'no-first-packet':
            vector['memory'].append((0x021C72A0 + 0x18, bytes(2)))
        elif failure == 'no-second-packet':
            vector['memory'] += [(0x021CEBE0 + 6, b'\x01'), (0x021C72A0 + 0x18, b'\x01\x00')]
        elif failure == 'wrong-kind':
            vector['memory'].append((PEERS + 2, bytes(2)))
        else:
            vector['memory'].append((PEERS, bytes(2)))
        output.append(vector)
    return output
