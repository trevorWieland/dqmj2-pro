import hashlib
import random
import struct
import time

from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put
from verify_record_features import compiled

EKT = 0x02500000
OUTPUT = 0x02530080
FEATURES = 0x02530200
TABLE = 0x020db1fc
STOP = 0x027ff800
NATIVE_FEATURES = list(range(201, 207)) + list(range(211, 228)) + [208, 228, 207, 209, 210]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def projected(memory, arm, species, variant, raw):
    if raw < 8:
        return raw & 255
    group = struct.unpack('<H', read(memory, EKT + species * 100 + 4, 2))[0] & 15
    offset = (group - 1) // 3 if group else 0
    at = TABLE + (raw - 8) * 3 + variant * (2 if offset == 1 else 1)
    return arm[at - 0x02000000]

def ekt_project(memory, arm, species, variant, output):
    for index in range(28):
        value = read(memory, EKT + species * 100 + 48 + index // 2, 1)[0]
        raw = (value >> (4 if index & 1 else 0)) & 15
        write(memory, output + index + 1, bytes([projected(memory, arm, species, variant, raw)]))

def add_feature(memory, feature, output):
    if feature not in NATIVE_FEATURES:
        return
    at = output + NATIVE_FEATURES.index(feature) + 1
    value = read(memory, at, 1)[0]
    if value < 5:
        write(memory, at, bytes([min(value + 2, 5)]))

def expected(memory, arm, name, first, second, third, fourth):
    if name == 'saved_projection_value':
        return projected(memory, arm, first, second, third)
    if name == 'saved_projection_feature_add':
        add_feature(memory, first, second)
        return None
    if name == 'saved_projection_ekt':
        ekt_project(memory, arm, first, second, third)
        return None
    if name == 'saved_projection_with_features':
        write(memory, fourth, bytes(32))
        ekt_project(memory, arm, first, second, fourth)
        for index in range(64):
            feature = read(memory, third + index, 1)[0]
            if not feature:
                break
            add_feature(memory, feature, fourth)
        return None
    raise AssertionError('Unexpected projection function')

def validate(arm, save, matches, root):
    wanted = {0x020449d4, 0x02044d84}
    reused = {address: item for address, item in compiled(arm).items() if address in wanted}
    if set(reused) != wanted:
        raise AssertionError('Projection dependency source absent')
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*reused.values(), *matches.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    asset = bytes(NintendoDSRom((root / 'inputs/game.nds').read_bytes()).getFileByName('EnmyKindTbl.bin'))
    ekt = asset[8:]
    rng = random.Random(20261027)
    lists = [bytes(64), bytes(NATIVE_FEATURES) + bytes(36), bytes([201]) * 64, bytes([228, 0, 201]) + bytes(61), bytes([200, 229, 255]) + bytes(61), bytes([identity for identity in reversed(NATIVE_FEATURES)]) * 2 + bytes(8)]
    vectors = []
    for name in matches:
        if name == 'saved_projection_value':
            vectors.extend((name, species, variant, raw, 0, None) for species in range(512) for variant in (0, 1, 2) for raw in range(16))
            vectors.extend((name, 0, 0, raw, 0, None) for raw in (-0x80000000, -257, -256, -1, 0, 7))
        elif name == 'saved_projection_feature_add':
            vectors.extend((name, feature, OUTPUT, 0, 0, value) for feature in (-0x80000000, -1, 0, 200, *range(201, 229), 229, 255, 0x7fffffff) for value in (0, 1, 2, 3, 4, 5, 6, 127, 255))
        elif name == 'saved_projection_ekt':
            vectors.extend((name, species, variant, OUTPUT, 0, None) for species in range(512) for variant in (0, 1, 2))
            vectors.extend((name, species, variant, EKT + species * 100 + 44, 0, None) for species in (0, 139, 353, 500, 511) for variant in (0, 1, 2))
        else:
            vectors.extend((name, species, species % 3, FEATURES, OUTPUT, index) for species in range(512) for index in range(len(lists)))
            vectors.extend((name, species, variant, pointer, OUTPUT, 1) for species in (0, 139, 353, 500, 511) for variant in (0, 1, 2) for pointer in (OUTPUT, OUTPUT + 1))
    cases = calls = 0
    for name, first, second, third, fourth, pattern in vectors:
        original = {0x020f6900: bytearray(rng.randbytes(0x1000)), EKT: bytearray(ekt + bytes(0x10000 - len(ekt))), 0x02530000: bytearray(rng.randbytes(0x1000))}
        put(original, 0x020f69f0, EKT)
        if name == 'saved_projection_feature_add':
            write(original, OUTPUT, bytes([pattern]) * 32)
        elif name == 'saved_projection_with_features':
            write(original, FEATURES, lists[pattern])
        memory = {address: bytearray(data) for address, data in original.items()}
        result = expected(memory, arm, name, first, second, third, fourth)
        row, code = matches[name]
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (first, second, third, fourth)):
                machine.reg_write(register, value & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError(('Projection bounds', name, first, second, third, pattern))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('Projection scalar return', first, second, third))
            for address, data in memory.items():
                if bytes(machine.mem_read(address, len(data))) != data:
                    raise AssertionError(('Projection/EKT/list/guard RAM', name, first, second, third, pattern))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedPackedEktProjectionAndCappedFeatures': True, 'platformStubs': {}, 'retainedNativeDependency': {'module': 'main', 'mode': 'ARM', 'address': '0x02008d78', 'bytes': 148, 'sha256': sha(arm[0x8d78:0x8e0c]), 'role': 'SDK fill'}, 'ektAssetSha256': sha(asset), 'nativeProjectionData': {'address': hex(TABLE), 'comparedWindowBytes': 32, 'sha256': sha(arm[TABLE - 0x02000000:TABLE - 0x02000000 + 32]), 'arrayExtentKnown': False}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Fourteen EKT bytes0x30..0x3D become28 low/high nibble projections at output bytes1..28; the bare projector preserves bytes0/29/30/31.', 'Raw values below8 return their byte truncation; larger values index native ROM data with stride3 and a variant multiplier2 only when the native variant offset equals1.', 'Feature IDs201..228 select28 fixed output bytes in native switch order; values below5 gain2 capped at5, while values5..255 remain unchanged.', 'The wrapper clears all32 bytes, projects the EKT fields, then applies up to64 nonzero feature IDs and stops at the first zero.', 'All512 species, variants0..2, raw nibbles0..15, byte-cap boundaries, repeated/terminated feature lists and output/EKT or output/list alias probes are included.'], 'limitations': ['Projection byte purposes, feature labels and the complete native ROM lookup-array extent remain unknown.', 'Native index arithmetic is established for bounded addresses only; row-crossing variants and alias probes are ARM observations rather than legal table-edit or portable array-bounds claims.', 'The SDK fill executes retained native code and receives no source credit; no platform provider is substituted.', 'No new save semantic bytes or original tables are modified.']}
