import hashlib
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
from mechanics_save_record_update_oracle import dependencies, lookup

RECORDS = 0x021bd674
INPUT = 0x02500080
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def expected(memory, name, identity, value):
    record = lookup(memory, identity)
    if name == 'saved_record_has_skill':
        return int(bool(record) and any(read(memory, record + 122 + index * 2, 1)[0] == value for index in range(5)))
    if not record:
        return None
    if name == 'saved_record_raw58_replace':
        if value:
            for offset in range(0, 56, 4):
                data = read(memory, value + offset, 4)
                write(memory, record + 64 + offset, data)
            write(memory, record + 120, read(memory, value + 56, 2))
        else:
            write(memory, record + 64, bytes(58))
    else:
        offset = {'saved_record_byte1b_set': 27, 'saved_record_byte1e_set': 30, 'saved_record_byte1c_set': 28, 'saved_record_byte1d_set': 29, 'saved_record_variant_set': 26}[name]
        write(memory, record + offset, bytes([value & 255]))
    return None

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*reused.values(), *matches.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rng = random.Random(20261027)
    cases = calls = 0
    for label in ('captured-primary', 'captured-backup', 'synthetic', 'duplicate'):
        original = {0x021bd000: bytearray(rng.randbytes(0x5000)), 0x02500000: bytearray(rng.randbytes(0x1000))}
        bank = 0x7100 if label == 'captured-backup' else 0
        write(original, 0x021bd51c, save[bank + 0x90:bank + 0x3a68])
        if label in ('synthetic', 'duplicate'):
            write(original, RECORDS, bytes(13200))
            data = bytearray(rng.randbytes(132))
            struct.pack_into('<I', data, 20, 1)
            data[122:132] = bytes([0, 0, 1, 255, 128, 100, 255, 0, 1, 1])
            write(original, RECORDS, bytes(data))
            if label == 'duplicate':
                other = bytearray(data)
                other[122:132] = b'\x07' * 10
                write(original, RECORDS + 132, bytes(other))
        identities = {u32(original, RECORDS + index * 132 + 20) for index in range(100)}
        present = next(identity for identity in identities if identity)
        missing = 0xffffffff
        while missing in identities:
            missing -= 1
        target = lookup(original, present)
        for name, (row, code) in matches.items():
            for identity in (present, 0, missing):
                values = list(range(-1, 257)) if name == 'saved_record_has_skill' else [0, INPUT, INPUT + 2, target + 64, target + 62, target + 66, target + 68, target + 32] if name == 'saved_record_raw58_replace' else [-0x80000000, -257, -256, -1, 0, 1, 127, 128, 255, 256, 257, 0x7fffffff]
                for value in values:
                    memory = {address: bytearray(data) for address, data in original.items()}
                    result = expected(memory, name, identity, value)
                    for machine in machines:
                        for address, data in original.items():
                            machine.mem_write(address, bytes(data))
                        machine.reg_write(UC_ARM_REG_R0, identity)
                        machine.reg_write(UC_ARM_REG_R1, value & 0xffffffff)
                        machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                        machine.reg_write(UC_ARM_REG_LR, STOP)
                        began = time.monotonic()
                        machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                        if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                            raise AssertionError(('Record fields execution bounds', label, name, identity, value))
                        if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                            raise AssertionError(('Record skill membership return', label, identity, value))
                        for address, data in memory.items():
                            if bytes(machine.mem_read(address, len(data))) != data:
                                raise AssertionError(('Record fields write/copy/lookup/guard RAM', label, name, identity, value))
                        calls += 1
                    cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRecordFieldAndSequentialCopyRam': True, 'platformStubs': {}, 'retainedNativeDependency': {'module': 'main', 'mode': 'ARM', 'address': '0x02008d78', 'bytes': 148, 'sha256': sha(arm[0x8d78:0x8e0c]), 'role': 'SDK fill'}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Skill membership scans all five native slots and compares the untruncated signed argument against the slot ID byte; zero matches an empty slot.', 'The58-byte writer copies fourteen pairs of halfwords then a final halfword, or clears all58 bytes when input is null.', 'Direct setters truncate values to bytes at record offsets1A,1B,1C,1D,1E; missing identities perform no write.', 'Captured banks, duplicate identities, absent IDs, halfword-aligned input and directional overlap cases are checked against sequential native load/store expectations.'], 'limitations': ['Overlapping struct assignment cases are isolated native/recompiled ARM probes; the C expression is not a portable overlap-copy contract.', 'Raw58-byte region and byte-field roles remain unnamed apart from the existing native variant byte; no new save semantics are promoted.', 'The SDK fill executes retained native bytes and is not credited as recovered C.', 'Void setter return registers are not semantic outputs.']}
