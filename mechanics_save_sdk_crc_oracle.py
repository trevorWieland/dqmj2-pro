import hashlib
import json
import random
import re
import struct
import time
import zlib

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link
from mechanics_save_identity_core_thumb_oracle import expected_code

BASE = 0x02500000
TABLE = BASE + 0x100
STATE = BASE + 0x800
DATA = BASE + 0x1000
PROFILE = BASE + 0x2800
IDENTITY = BASE + 0x2900
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
WIDTHS = {8: (1, 0x07, 0x02019b58), 16: (2, 0xa001, 0x02019b80), 32: (4, 0xedb88320, 0x02019ba8)}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02019b58, 0x02019b80, 0x02019ba8}
    paths = ('evidence/matches/main-runtime08.json', 'evidence/matches/mechanics-save-identity-core-thumb.json', 'evidence/matches/mechanics-save-identity-validator-thumb.json', 'evidence/matches/mechanics-save-identity-profile-storage-thumb.json')
    extra = {0x02096e74, 0x02096ee4, 0x020971bc, 0x0209725c, 0x020972c0}
    result = []
    config = (root / 'config/arm9/symbols.txt').read_text()
    for path in paths:
        report = json.loads((root / path).read_text(encoding='utf-8'))
        for entry in report['matches']:
            address = int(entry['address'], 0)
            if address not in wanted | extra:
                continue
            for field in ('source', 'object'):
                if sha((root / entry[field]).read_bytes()) != entry[field + 'Sha256']:
                    raise AssertionError(('Profile dependency source/object differs', entry['name']))
            row = dict(entry)
            if 'isolatedCallerBinary' not in row:
                bindings = {}
                for relocation in row['relocations']:
                    target = int(relocation['target'], 0) & ~1
                    match = re.search(r'kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:0x' + f'{target:08x}' + r'$', config, re.M)
                    if not match:
                        raise AssertionError(('Profile dependency target missing', target))
                    bindings[relocation['symbol']] = {'address': hex(target), 'mode': match[1], 'module': 'main', 'processor': 'arm9', 'kind': 'function'}
                row.update(freeze_link(validate_link(row, bindings)))
            binary = (root / row['isolatedCallerBinary']).read_bytes()
            if sha(binary) != row['isolatedCallerBinarySha256'] or binary != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError(('Profile dependency actual linked bytes differ', row['name']))
            result.append((row, binary))
    if {int(row['address'], 0) for row, code in result} != wanted | extra:
        raise AssertionError('Profile dependency batch incomplete')
    return result


def table_bytes(bits, polynomial):
    values = []
    for index in range(256):
        value = index
        for bit in range(8):
            if bits == 8:
                value = ((value << 1) ^ (polynomial if value & 128 else 0)) & 0xffffffff
            else:
                value = (value >> 1) ^ (polynomial if value & 1 else 0)
        values.append((value & ((1 << bits) - 1)).to_bytes(bits // 8, 'little'))
    return b''.join(values)

def table_update(bits, table, value, data):
    width = bits // 8
    for byte in data:
        index = (value ^ byte) & 255
        lookup = int.from_bytes(table[index * width:(index + 1) * width], 'little')
        value = lookup if bits == 8 else lookup ^ (value >> 8)
    return value

def bit_update(bits, polynomial, value, data):
    mask = (1 << bits) - 1
    for byte in data:
        value ^= byte
        for bit in range(8):
            if bits == 8:
                value = ((value << 1) ^ (polynomial if value & 128 else 0)) & mask
            else:
                value = ((value >> 1) ^ (polynomial if value & 1 else 0)) & mask
    return value

def validate(arm, save, matches, root):
    required = {f'saved_crc{bits}_{kind}' for bits in WIDTHS for kind in ('table', 'update')}
    if set(matches) != required:
        raise AssertionError('Complete CRC table/update source batch is required')
    reused = dependencies(root, arm)
    entries = {int(row['address'], 0): (row, code) for row, code in [*matches.values(), *reused]}
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in entries.values():
                actual = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
                    raise AssertionError('CRC actual MW caller snapshot differs')
                machine.mem_write(int(row['address'], 0), actual)
        machines.append(machine)
    rng = random.Random(2026102789)
    cases = calls = 0
    def invoke(row, arguments, initial, expected, result=None, wide=False):
        nonlocal cases, calls
        stack = rng.randbytes(0x10000)
        guard = rng.randbytes(0x1000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        for machine in machines:
            if initial is not None:
                machine.mem_write(BASE, bytes(initial))
            machine.mem_write(0x021d0000, guard)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), arguments):
                machine.reg_write(register, value & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            began = time.monotonic()
            machine.emu_start(int(row['address'], 0) | int(row['mode'].lower() == 'thumb'), STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                raise AssertionError(('CRC bounded return/ABI', row['name'], arguments))
            actual = machine.reg_read(UC_ARM_REG_R0) | (machine.reg_read(UC_ARM_REG_R1) << 32 if wide else 0)
            if result is not None and actual != result:
                raise AssertionError(('CRC independent result', row['name'], arguments, result, actual))
            if bytes(machine.mem_read(BASE, 0x4000)) != expected or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                raise AssertionError(('CRC complete arena/global guards', row['name'], arguments))
            calls += 1
        cases += 1
    observed_input_values = set()
    polynomials = (0, 1, 7, 0x80, 0xff, 0x1021, 0x8005, 0xa001, 0xffff, 0x80000000, 0xedb88320, 0xffffffff)
    for bits, (width, polynomial, wrapper) in WIDTHS.items():
        for poly in (*polynomials, *(range(256) if bits == 8 else (rng.getrandbits(32) for index in range(64)))):
            initial = bytearray(rng.randbytes(0x4000))
            expected = bytearray(initial)
            expected[0x100:0x100 + 256 * width] = table_bytes(bits, poly)
            invoke(matches[f'saved_crc{bits}_table'][0], (TABLE, poly), initial, expected)
        valid_table = table_bytes(bits, polynomial)
        for random_table in (False, True):
            table = rng.randbytes(256 * width) if random_table else valid_table
            for length in (0, 1, 2, 3, 7, 8, 9, 31, 32, 63, 64, 65, 255, 256, 1024, 4096):
                for state in (0, 1, 127, 255, 0x7fffffff, 0x80000000, 0xffffffff):
                    value = state & ((1 << bits) - 1)
                    initial = bytearray(rng.randbytes(0x4000))
                    initial[0x100:0x100 + len(table)] = table
                    initial[0x800:0x800 + width] = value.to_bytes(width, 'little')
                    expected = bytearray(initial)
                    data = bytes(initial[0x1000:0x1000 + length])
                    observed_input_values.update(data)
                    updated = table_update(bits, table, value, data)
                    expected[0x800:0x800 + width] = updated.to_bytes(width, 'little')
                    invoke(matches[f'saved_crc{bits}_update'][0], (TABLE, STATE, DATA, length), initial, expected)
                    initial_state = 0xffffffff if bits == 32 else 0
                    result = table_update(bits, table, initial_state, data) ^ (0xffffffff if bits == 32 else 0)
                    invoke(entries[wrapper][0], (TABLE, DATA, length), initial, initial, result)
                    if not random_table and updated != bit_update(bits, polynomial, value, data):
                        raise AssertionError('Independent bitwise/table CRC models disagree')
                    if bits == 32 and not random_table and result != zlib.crc32(data):
                        raise AssertionError('Independent zlib CRC32 differs')
        for table_pointer, state_pointer, data_pointer, length in ((0, STATE, 0, 0), (TABLE, TABLE, DATA, 64), (TABLE, DATA, DATA, 64), (TABLE, STATE, TABLE, 64), (TABLE, STATE, DATA + 1, 63)):
            initial = bytearray(rng.randbytes(0x4000))
            initial[0x100:0x100 + len(valid_table)] = valid_table
            expected = bytearray(initial)
            offset = state_pointer - BASE
            value = int.from_bytes(initial[offset:offset + width], 'little')
            table = bytes(initial[0x100:0x100 + len(valid_table)])
            data = bytes(initial[data_pointer - BASE:data_pointer - BASE + length]) if length else b''
            result = table_update(bits, table, value, data)
            expected[offset:offset + width] = result.to_bytes(width, 'little')
            invoke(matches[f'saved_crc{bits}_update'][0], (table_pointer, state_pointer, data_pointer, length), initial, expected)
    protocols = 0
    for bits, (width, polynomial, wrapper) in WIDTHS.items():
        for length in (0, 1, 7, 8, 9, 63, 64, 65, 255, 1024):
            current = bytearray(rng.randbytes(0x4000))
            current[0x800:0x800 + width] = (0xffffffff if bits == 32 else 0).to_bytes(width, 'little')
            for machine in machines:
                machine.mem_write(BASE, bytes(current))
            current[0x100:0x100 + 256 * width] = table_bytes(bits, polynomial)
            invoke(matches[f'saved_crc{bits}_table'][0], (TABLE, polynomial), None, current)
            table = bytes(current[0x100:0x100 + 256 * width])
            consumed = 0
            while consumed < length:
                chunk = min((consumed % 17) + 1, length - consumed)
                value = int.from_bytes(current[0x800:0x800 + width], 'little')
                changed = table_update(bits, table, value, current[0x1000 + consumed:0x1000 + consumed + chunk])
                current[0x800:0x800 + width] = changed.to_bytes(width, 'little')
                invoke(matches[f'saved_crc{bits}_update'][0], (TABLE, STATE, DATA + consumed, chunk), None, current)
                consumed += chunk
            initial_state = 0xffffffff if bits == 32 else 0
            result = bit_update(bits, polynomial, initial_state, current[0x1000:0x1000 + length]) ^ (0xffffffff if bits == 32 else 0)
            invoke(entries[wrapper][0], (TABLE, DATA, length), None, current, result)
            protocols += 1
    for identity in (0, 1, 127, 255, 65535, 0x7fffffff, 0x80000000, 0xffffffff):
        for key in (0, 1, 0xffffffff, 0x4a324a42):
            initial = rng.randbytes(0x4000)
            code = expected_code(identity, key, 0)
            invoke(entries[0x02096e74][0], (identity, key, 0), initial, initial, code, True)
            for corrupt in (0, 1, 1 << 32, 1 << 63):
                value = code ^ corrupt
                low = value & 0xffffffff
                result = int(0 < low < 0x80000000 and value == expected_code(low, key, 0))
                invoke(entries[0x02096ee4][0], (low, value >> 32, key, 0), initial, initial, result)
    for dirty in (0, 1, 0xffffffff):
        for value in (0, 1, 0x7fffffff, 0x80000000, 0xffffffff):
            current = bytearray(rng.randbytes(0x4000))
            struct.pack_into('<I', current, 0x2820, dirty)
            for machine in machines:
                machine.mem_write(BASE, bytes(current))
            current[0x2810:0x281c] = current[0x2900:0x290c]
            struct.pack_into('<I', current, 0x281c, value)
            struct.pack_into('<I', current, 0x283c, zlib.crc32(current[0x2800:0x283c]))
            struct.pack_into('<I', current, 0x2820, dirty | 1)
            invoke(entries[0x0209725c][0], (PROFILE, IDENTITY, value), None, current)
            result = int(zlib.crc32(current[0x2800:0x283c]) == struct.unpack_from('<I', current, 0x283c)[0])
            invoke(entries[0x020971bc][0], (PROFILE,), None, current, result)
            struct.pack_into('<I', current, 0x2820, (dirty | 1) & ~1)
            struct.pack_into('<I', current, 0x283c, zlib.crc32(current[0x2800:0x283c]))
            invoke(entries[0x020972c0][0], (PROFILE,), None, current)
            invoke(entries[0x020971bc][0], (PROFILE,), None, current, 1)
            protocols += 1
    malformed = []
    for bits, (width, polynomial, wrapper) in WIDTHS.items():
        for arguments, expected_pc in (((TABLE, 0, DATA, 0), {8: 0x02019a28, 16: 0x02019aa4, 32: 0x02019b24}[bits]), ((TABLE, STATE, 0, 1), {8: 0x02019a34, 16: 0x02019ab0, 32: 0x02019b30}[bits]), ((0, STATE, DATA, 1), {8: 0x02019a48, 16: 0x02019ac8, 32: 0x02019b44}[bits])):
            initial = rng.randbytes(0x4000)
            stack = rng.randbytes(0x10000)
            incoming = [rng.getrandbits(32) for register in SAVED]
            outcomes = []
            row = matches[f'saved_crc{bits}_update'][0]
            for machine in machines:
                machine.mem_write(BASE, initial)
                machine.mem_write(0x027f0000, stack)
                for register, value in zip(SAVED, incoming):
                    machine.reg_write(register, value)
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), arguments):
                    machine.reg_write(register, value)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                try:
                    machine.emu_start(int(row['address'], 0), STOP, count=1000000)
                except UcError as error:
                    if time.monotonic() - began > 2:
                        raise AssertionError('CRC malformed fault exceeded bound')
                    outcomes.append((str(error), machine.reg_read(UC_ARM_REG_PC), machine.reg_read(UC_ARM_REG_SP), [machine.reg_read(register) for register in SAVED], bytes(machine.mem_read(BASE, 0x4000)), bytes(machine.mem_read(0x027f0000, 0x10000))))
                else:
                    raise AssertionError('CRC malformed pointer unexpectedly returned')
                calls += 1
            if outcomes[0] != outcomes[1] or outcomes[0][1] != expected_pc or outcomes[0][4] != initial:
                raise AssertionError(('CRC malformed partial state/fault location', bits, arguments, outcomes[0][:3]))
            malformed.append({'bits': bits, 'arguments': list(arguments), 'fault': outcomes[0][0], 'pc': hex(outcomes[0][1]), 'completeArenaUnchanged': True, 'nativeAndRecompiledFaultStackAndSavedRegistersEqual': True})
            cases += 1
    if observed_input_values != set(range(256)):
        raise AssertionError('CRC byte-input coverage differs')
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'connectedStreamingAndProfileProtocols': protocols, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedSourceBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'independentBitwiseTableAndZlibModels': True, 'inputByteValuesCovered': len(observed_input_values), 'codeCallerFixturesUseCrcMode0Only': True, 'platformStubs': {}, 'reusedAcceptedSources': [row for row, code in reused], 'retainedNativeEntries': [], 'malformedPointerCases': malformed, 'observations': ['The eight-bit table advances toward the most-significant byte bit;16/32-bit tables shift right and XOR their supplied polynomial on low-bit1.', 'Update functions read the initial state even for zero length, read no input/table for zero length, and store state only after the entire buffer.', 'State/data/table aliases preserve original table/data until the final state write; all byte inputs and unaligned byte input pointers are permitted by these bounded fixtures.', 'Accepted CRC wrapper callers initialize8/16-bit state0 and32-bit stateFFFFFFFF, with the32-bit wrapper applying final inversion.', 'Streaming chunk updates agree with independent bitwise CRC and Python zlib; code constructor/validator and profile write/check/refresh execute these source CRC primitives through real accepted callers.'], 'limitations': ['Arbitrary polynomial/high-bit inputs characterize target instruction behavior without asserting official SDK argument legality.', 'This14-body C closure covers the tested CRC/code/profile paths without native callees, but does not establish physical save timing, bank chronology or authentication.', 'No semantic save partition meaning or original input changes are made.']}
