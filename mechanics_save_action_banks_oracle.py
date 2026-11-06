import hashlib
import random
import struct
import time

from ndspy.rom import NintendoDSRom
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_INVALID
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put
from verify_record_features import compiled

SKILL = 0x02510000
PRIMARY = 0x02530080
SECONDARY = 0x02530100
SKILLS = 0x02530200
FEATURES = 0x02530300
TEMP = 0x027fff00
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def set_bit(memory, pointer, identity):
    at = pointer + (identity // 32) * 4
    put(memory, at, u32(memory, at) | (1 << (identity % 32)))

def feature3(memory, pointer):
    if not pointer:
        return False
    values = read(memory, pointer, 64)
    return 3 in values[:values.index(0) if 0 in values else 64]

def banks(memory, table, skill_pointer, feature_pointer, primary, secondary, present):
    if primary:
        write(memory, primary, bytes(32))
    if secondary:
        write(memory, secondary, bytes(32))
    if primary:
        put(memory, primary, 3)
    if skill_pointer:
        for slot in range(5):
            identity, allocated = read(memory, skill_pointer + slot * 2, 2)
            if not identity or not present:
                continue
            row = table[8 + identity * 60:8 + (identity + 1) * 60]
            for stage in range(10):
                if allocated < row[stage]:
                    break
                action = row[10 + stage * 4]
                if not action:
                    continue
                if primary:
                    set_bit(memory, primary, action)
                for other in row[11 + stage * 4:14 + stage * 4]:
                    if not other:
                        break
                    if secondary:
                        set_bit(memory, secondary, other)
    if feature3(memory, feature_pointer):
        if not primary:
            return 0x0207b1b0
        put(memory, primary, u32(memory, primary) | 4)
    return None

def expected(memory, table, name, first, second, third, fourth, present):
    if name == 'saved_skill_action_banks':
        return banks(memory, table, first, second, third, fourth, present)
    memory[TEMP] = bytearray(32)
    fault = banks(memory, table, first, second, third, TEMP, present)
    if fault is None:
        if not third:
            fault = 0x0207b1e4
        else:
            for index in range(8):
                put(memory, third + index * 4, u32(memory, third + index * 4) & ~u32(memory, TEMP + index * 4))
    del memory[TEMP]
    return fault

def validate(arm, save, matches, root):
    wanted = {0x0207aa98, 0x0207b674}
    reused = {address: item for address, item in compiled(arm).items() if address in wanted}
    if set(reused) != wanted:
        raise AssertionError('Action-bank dependencies missing')
    context = {}

    def invalid(machine, access, address, size, value, user):
        context['fault'] = machine.reg_read(UC_ARM_REG_PC)
        return False

    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*reused.values(), *matches.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machine.hook_add(UC_HOOK_MEM_INVALID, invalid)
        machines.append(machine)
    actual = bytes(NintendoDSRom((root / 'inputs/game.nds').read_bytes()).getFileByName('SkillTbl.bin'))
    synthetic = bytearray(actual)
    row = bytearray(60)
    row[:10] = bytes([0, 200, 1, 3, 4, 5, 6, 7, 8, 9])
    row[10:50] = bytes([7, 8, 9, 0, 255, 1, 2, 0, 31, 32, 0, 255, 0, 100, 101, 102, 128, 255, 254, 253, 255, 0, 1, 2, 1, 2, 3, 4, 2, 1, 0, 3, 0, 99, 99, 99, 0, 0, 0, 0])
    synthetic[68:128] = row
    rng = random.Random(20261027)
    cases = calls = faults = 0
    for label, table, present in [('measured', actual, True), ('synthetic', bytes(synthetic), True), ('absent-table', actual, False)]:
        vectors = []
        for name in matches:
            for identity in (range(256) if label == 'measured' else [0, 1, 255]):
                row = table[8 + identity * 60:8 + (identity + 1) * 60]
                points = sorted({0, 1, 255, *[max(0, min(255, point + delta)) for point in row[:10] for delta in (-1, 0, 1)]})
                vectors.extend((name, bytes([identity, allocated]) * 5, None, PRIMARY, SECONDARY) for allocated in points)
            vectors.extend((name, save[0x1e8 + index * 132 + 122:0x1e8 + index * 132 + 132], bytes([3, 0]) + bytes(62), PRIMARY, SECONDARY) for index in range(100))
            vectors.extend((name, skills, feature_list, primary, secondary) for skills in (None, bytes([1, 255]) * 5) for feature_list in (None, bytes(64), bytes([3]) * 64, bytes([1, 0, 3]) + bytes(61)) for primary in (0, PRIMARY) for secondary in (0, SECONDARY, PRIMARY))
        for name, skills, features, primary, secondary in vectors:
            original = {0x021c6700: bytearray(rng.randbytes(0x1000)), SKILL: bytearray(table + bytes(0x4000 - len(table))), 0x02530000: bytearray(rng.randbytes(0x1000))}
            put(original, 0x021c673c, SKILL if present else 0)
            put(original, 0x021c6740, 256)
            if skills is not None:
                write(original, SKILLS, skills)
            if features is not None:
                write(original, FEATURES, features)
            first = SKILLS if skills is not None else 0
            second = FEATURES if features is not None else 0
            memory = {address: bytearray(data) for address, data in original.items()}
            fault = expected(memory, table, name, first, second, primary, secondary, present)
            row, code = matches[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                context['fault'] = None
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (first, second, primary, secondary)):
                    machine.reg_write(register, value)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                try:
                    machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                except UcError:
                    if fault is None:
                        raise
                if time.monotonic() - began > 2 or context['fault'] != fault or (fault is None and machine.reg_read(UC_ARM_REG_PC) != STOP):
                    raise AssertionError(('Action bank execution/fault bounds', label, name, primary, secondary, fault, context['fault']))
                if fault is None and machine.reg_read(UC_ARM_REG_R0) != 1:
                    raise AssertionError('Action bank return differs')
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        raise AssertionError(('Action bank/table/input/feature/guard RAM', label, name, primary, secondary))
                calls += 1
            faults += int(fault is not None)
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'expectedMalformedFaultCases': faults, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcOrExpectedFaultVerified': True, 'independentExpectedTwoBanksAndFilter': True, 'platformStubs': {}, 'retainedNativeDependency': {'module': 'main', 'mode': 'ARM', 'address': '0x02008c14', 'bytes': 20, 'sha256': sha(arm[0x8c14:0x8c28]), 'role': 'SDK word fill; value/destination/size ABI'}, 'skillAssetSha256': sha(actual), 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['The primary256-bit bank begins with IDs0/1, gains threshold-qualified stage action IDs and gains ID2 when feature ID3 occurs before the feature-list terminator.', 'A stage action byte of0 skips all three linked bytes; linked processing stops at its first zero, while the stage loop stops at its first unmet threshold.', 'The secondary bank contains linked action IDs; the wrapper removes every secondary-bank bit from the primary bank.', 'Five captured skill pairs, all256 table rows at threshold boundaries, duplicate stages, linked zeros, absent tables, null bank pointers and aliased output banks are exercised.'], 'limitations': ['SDK word fill20 bytes executes retained native ARM and receives no C source credit.', 'A null primary pointer can fault at0x0207B1B0 when feature3 is present; the filter additionally faults at0x0207B1E4 for a null primary. Expected native PCs and partial effects are checked as malformed machine probes.', 'The native action/feature IDs and linked relations remain technical domains; full action legality or gameplay effects are not inferred.', 'No save-byte meanings or original inputs are changed.']}
