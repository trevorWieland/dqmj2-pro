import hashlib
import random
import struct

from match_ov001_current_stat_restore_20261030 import divide, short
from prove_reward_return_abi_20261029 import execute as machine_execute, OUTPUT

ADDRESS, RECORDS, ACTORS = 0x021DA268, 0x02330000, OUTPUT
DESCRIPTORS, ITEM, EQUIP = 0x02340000, 0x02350000, 0x02360000
POLICY, STRIDE = 0x02102E2C, 0xAC


def status_ids(asset):
    count = struct.unpack_from('<I', asset, 4)[0]
    if count < 60 or len(asset) < 8 + count * 14:
        raise ValueError('Measured battle status table lacks60 full native descriptors')
    return [struct.unpack_from('<h', asset, 8 + number * 14 + 4)[0] for number in range(60)]


def policy_inputs(ids, vector):
    unique = list(dict.fromkeys(ids))
    rng = random.Random(vector['seed'] ^ 0xAC)
    payload = bytearray(rng.randbytes(32 * STRIDE))
    rows = []
    for number in range(32):
        position = (number + vector['ordinal'] * 7) % max(1, len(unique))
        identity = unique[position] if number < len(unique) else -2147483648
        flags = rng.getrandbits(16) & ~1 | ((number + vector['ordinal']) % 2)
        if vector['ordinal'] % 7 == 0 and number == 1:
            identity = rows[0][0]
            flags = rows[0][1] ^ 1
        struct.pack_into('<i', payload, number * STRIDE + 4, identity)
        struct.pack_into('<H', payload, number * STRIDE + 0x78, flags)
        rows.append((identity, flags))
    preserved = []
    for identity in ids:
        flag = next((flags for entry, flags in rows if entry == identity), 0)
        preserved.append(bool(flag & 1))
    return bytes(payload), preserved, rows


def vectors():
    for index in range(128):
        yield {'ordinal': index, 'validMask': index % 8, 'restoreCurrent': [0, 1, 0xFFFFFFFF][index % 3],
               'seed': 202610300356 + index, 'policySource': 'synthetic32-slot runtime table, not observed scene state'}


def normalize(actor):
    result = bytearray(actor)
    hp_base, mp_base, hp, mp = struct.unpack_from('<4h', actor, 0x1EC)
    hp_delta, mp_delta = struct.unpack_from('<2h', actor, 0x21C)
    total_hp, total_mp = hp_base + hp_delta, mp_base + mp_delta
    hp = 0 if total_hp <= 0 else short(divide(hp * hp_base + total_hp - 1, total_hp))
    mp = 0 if total_mp <= 0 else short(divide(mp * mp_base + total_mp - 1, total_mp))
    if hp > 0:
        hp = min(hp, hp_base)
    mp = min(mp, mp_base)
    struct.pack_into('<2h', result, 0x1F0, hp, mp)
    return bytes(result)


def components(vector):
    rng = random.Random(vector['seed'])
    records, actors = [], []
    bases, modifiers, currents = [0, 1, 100, 9999], [-32768, -1, 0, 1, 100, 32767], [-32768, -1, 0, 1, 99, 9999, 32767]
    for slot in range(3):
        record, actor = bytearray(rng.randbytes(0x210)), bytearray(rng.randbytes(0x440))
        struct.pack_into('<h', record, 0x2E, [0, 1, 4][slot] if vector['validMask'] & (1 << slot) else -1)
        record[0x4A:0x8A] = bytes(64)
        record[0xB0] = int((vector['ordinal'] + slot) % 3 != 0)
        struct.pack_into('<I', actor, 0x1E8, RECORDS + slot * 0x210 + 4)
        actor[0x1EC:0x20C] = bytes(32)
        index = vector['ordinal'] + slot
        struct.pack_into('<4h', actor, 0x1EC, bases[index % 4], bases[index // 4 % 4], currents[index % 7], currents[index // 7 % 7])
        struct.pack_into('<2h', actor, 0x21C, modifiers[index % 6], modifiers[index // 6 % 6])
        actor[0x31C] = [0, 1, 255][index % 3]
        actor[0x1FF] = [0, 1, 255][index // 3 % 3]
        records.append(bytes(record))
        actors.append(bytes(actor))
    return records, actors


def model(records, actors, preserved, vector):
    result_records, result_actors, details = [], [], []
    processed = 0
    for slot, (record, actor) in enumerate(zip(records, actors)):
        output = bytearray(record)
        if struct.unpack_from('<h', record, 0x2E)[0] < 0:
            output[0x201] = 3
            result_records.append(bytes(output))
            result_actors.append(actor)
            details.append({'slot': slot, 'processed': False, 'stateByte201': 3})
            continue
        processed += 1
        updated_actor = normalize(actor) if vector['restoreCurrent'] else actor
        output[0x11C:0x13C] = updated_actor[0x1EC:0x20C]
        output[0x13C:0x1B4] = updated_actor[0x22C:0x2A4]
        output[0x203:0x20D] = updated_actor[0x432:0x43C]
        output[0x20D] = updated_actor[0x43C]
        for number in range(60):
            if not preserved[number]:
                output[0x1C4 + number] = updated_actor[0x39E + number]
        output[0x1B4:0x1C4] = updated_actor[0x21C:0x22C]
        output[0x202] = 1
        output[0x201] = 1 if updated_actor[0x31C] and updated_actor[0x1FF] else 2 if updated_actor[0x31C] and record[0xB0] else 0
        result_records.append(bytes(output))
        result_actors.append(updated_actor)
        details.append({'slot': slot, 'processed': True, 'stateByte201': output[0x201],
                        'sourceSpecies': struct.unpack_from('<h', record, 0x2E)[0],
                        'restoredCurrent': bool(vector['restoreCurrent']),
                        'preservedStatusBytes': sum(preserved), 'copiedStatusBytes': 60 - sum(preserved)})
    return result_records, result_actors, processed, details


def execute(main, overlay, code, blobs, vector):
    ids = status_ids(blobs['BtlStsTbl.bin'])
    policy, preserved, rows = policy_inputs(ids, vector)
    records, actors = components(vector)
    output_records, output_actors, count, details = model(records, actors, preserved, vector)
    memory = [(RECORDS, b''.join(records)), (ACTORS, b''.join(actors)),
              (DESCRIPTORS, blobs['BtlStsTbl.bin']), (0x02232B28, struct.pack('<I', DESCRIPTORS)),
              (POLICY, policy), (ITEM, blobs['ItemTbl.bin'][8:]), (0x021C2AB4, struct.pack('<I', ITEM)),
              (EQUIP, blobs['EquipTbl.bin'][8:]), (0x021C6BF4, struct.pack('<I', EQUIP)),
              (0x020F69E4, bytes(4))]
    patches = [(RECORDS, b''.join(output_records))]
    for slot, actor in enumerate(output_actors):
        patches.append((ACTORS + slot * 0x440 + 0x1F0, actor[0x1F0:0x1F4]))
    rebuilt_overlay = bytearray(overlay)
    rebuilt_overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + len(code)] = code
    result = machine_execute(main, bytes(rebuilt_overlay), blobs, ADDRESS,
                             [RECORDS, ACTORS, vector['restoreCurrent']], memory, patches, count, vector['seed'])
    result.update(vector=vector, slots=details, preservedPolicyByStatusIndex=preserved,
                  nativeStatusIds=ids, syntheticPolicySlots=rows,
                  syntheticPolicySha256=hashlib.sha256(policy).hexdigest(),
                  independentPreparedRecordAndActorEffects=True)
    return result
