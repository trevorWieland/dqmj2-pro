import hashlib
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC

FRAME = 0x021bd000
LENGTH = 0x4000
MAIN = 0x021bd51c
RECORDS = 0x021bd674
PARTY = 0x021bd540
RESERVE = 0x021bd54c
STOP = 0x027ff800

def lookup(frame, identity):
    if not identity:
        return 0
    for index in range(100):
        if struct.unpack_from('<I', frame, RECORDS - FRAME + index * 0x84 + 0x14)[0] == identity:
            return RECORDS + index * 0x84
    return 0

def validate(arm, save, matches, root):
    machines = []
    calls = 0
    counts = {}
    touched = set()
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for record, code in matches.values():
                machine.mem_write(int(record['address'], 16), code)
        machines.append(machine)

    def check(name, frame, expected, first=0, second=0, result=None):
        nonlocal calls
        if name not in matches:
            return
        address = int(matches[name][0]['address'], 16)
        for machine in machines:
            machine.mem_write(FRAME, bytes(frame))
            machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
            machine.reg_write(UC_ARM_REG_R1, second & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(address, STOP, count=100000)
            if machine.reg_read(UC_ARM_REG_PC) != STOP or time.monotonic() - began > 1:
                raise AssertionError('Record accessor exceeded execution bounds')
            if bytes(machine.mem_read(FRAME, LENGTH)) != expected:
                raise AssertionError((name, first, second, 'RAM effects differ'))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result & 0xffffffff:
                raise AssertionError((name, first, second, 'Return differs', machine.reg_read(UC_ARM_REG_R0), result))
            calls += 1
        counts[name] = counts.get(name, 0) + 1
        touched.add(name)

    rng = random.Random(20261027)
    frames = [('zero', bytes(LENGTH)), ('ff', bytes([255]) * LENGTH)]
    for bank in range(2):
        frame = bytearray(rng.randbytes(LENGTH))
        frame[MAIN - FRAME:MAIN - FRAME + 0x39d8] = save[bank * 0x7100 + 0x90:bank * 0x7100 + 0x3a68]
        frames.append((f'real-bank-{bank}', bytes(frame)))
    for number in range(4):
        frame = bytearray(rng.randbytes(LENGTH))
        for index in range(100):
            identity = index + 1
            if number == 0:
                identity = 0
            elif number == 1:
                identity = 7 if index in (0, 50, 99) else 0
            elif number == 2:
                identity = index + 1 if index == 99 else 0
            struct.pack_into('<I', frame, RECORDS - FRAME + index * 0x84 + 0x14, identity)
        party = [0, 7, 0xffffffff] if number < 2 else [100, 100, 100]
        reserve = [7, 0, 7] if number < 2 else [1, 100, 101]
        struct.pack_into('<III', frame, PARTY - FRAME, *party)
        struct.pack_into('<III', frame, RESERVE - FRAME, *reserve)
        frames.append((f'synthetic-record-layout-{number}', bytes(frame)))
    for label, frame in frames:
        identities = sorted(set([0, 1, 7, 100, 101, 0x7fffffff, 0x80000000, 0xffffffff] + [struct.unpack_from('<I', frame, RECORDS - FRAME + index * 0x84 + 0x14)[0] for index in range(100)]))
        for identity in identities:
            pointer = lookup(frame, identity)
            check('save_record_by_id', frame, frame, identity, result=pointer)
            for value in [0, 1, 127, 128, 255, 256, 0xffffffff]:
                expected = bytearray(frame)
                if pointer:
                    expected[pointer - FRAME + 0x32] = value & 255
                check('save_record_byte32_set', frame, expected, identity, value)
        for prefix, base in [('party', PARTY), ('reserve', RESERVE)]:
            for slot in [-1, 0, 1, 2, 3, 4]:
                identity = struct.unpack_from('<I', frame, base - FRAME + slot * 4)[0]
                check(f'save_{prefix}_id', frame, frame, slot, result=identity)
                check(f'save_{prefix}_record', frame, frame, slot, result=lookup(frame, identity))
            expected_count = sum(bool(lookup(frame, struct.unpack_from('<I', frame, base - FRAME + slot * 4)[0])) for slot in range(3))
            check(f'save_{prefix}_count', frame, frame, result=expected_count)
        for name, pointer in [('save_records_pointer', RECORDS), ('save_summary_word_pointer', MAIN), ('save_summary_tail_pointer', 0x021b9eb4)]:
            check(name, frame, frame, result=pointer)
        for value in [0, 1, 3, 4, 9, 10, 0x7fffffff, 0x80000000, 0xffffffff]:
            expected = 50 if value < 4 else 75 if value < 10 else 100
            check('save_record_byte_query', frame, frame, value, result=expected)
    if touched != set(matches):
        raise AssertionError(('Untested source matches', set(matches) - touched))
    return {'engine': 'Unicorn', 'cases': sum(counts.values()), 'nativeAndRecompiledCalls': calls, 'counts': counts, 'testedFunctions': sorted(touched), 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 1, 'returnPcVerified': True, 'independentExpectedPointersAndRam': True, 'boundaryStubs': [], 'frames': [{'name': name, 'sha256': hashlib.sha256(data).hexdigest()} for name, data in frames], 'observations': ['Zero identity returns null even when zero-valued record IDs exist.', 'Nonzero identity lookup scans100 records of stride0x84, compares word0x14 and returns the first match.', 'Party/reserve slots resolve stored identities rather than treating position as identity; repeated references remain repeated slots.', 'The raw query returns50 below4,75 below10 and100 otherwise using unsigned comparison.'], 'limitations': ['Native record lookup behavior does not by itself establish current ownership, slot validity or gameplay identity semantics for every field.', 'Out-of-capacity slot probes observe bounded memory arithmetic only and do not establish legal runtime indices.', 'Field0x32 and threshold-query arguments remain technically named until independently associated with native callers and game semantics.']}
