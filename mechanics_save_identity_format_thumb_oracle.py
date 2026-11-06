import hashlib
import json
import random
import re
import struct
import time

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

BASE = 0x02500000
INPUT = BASE + 0x40
OUTPUT = BASE + 0x400
STOP = 0x027ff800
ALPHABET = b'0123456789abcdefghijklmnopqrstuv'
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02096ca8}
    paths = ('evidence/matches/main-thumb-runtime02.json', 'evidence/matches/mechanics-save-identity-values-thumb.json')
    extra = {0x02096c90, 0x02096f50}
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


def base32(code, length):
    return bytes(ALPHABET[(code >> (5 * position)) & 31] for position in reversed(range(length)))

def validate(arm, save, matches, root):
    from match_mechanics_save_identity_format_thumb import SPECS
    if set(matches) != set(SPECS):
        raise AssertionError('Complete identity formatter source batch is required')
    reused = dependencies(root, arm)
    strings = []
    for address, data in ((0x020deaf0, b'%012llu\0'), (0x020deaf8, ALPHABET + b'\0'), (0x020deb1c, b'%s%c%c%c%c%s\0')):
        if arm[address - 0x02000000:address - 0x02000000 + len(data)] != data:
            raise AssertionError('Identity formatter native string namespace differs')
        strings.append({'address': hex(address), 'module': 'main', 'processor': 'arm9', 'kind': 'data', 'bytes': len(data), 'sha256': sha(data), 'sourceCredit': 0})
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused]:
                actual = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
                    raise AssertionError('Identity formatter actual MW caller snapshot differs')
                machine.mem_write(int(row['address'], 0), actual)
        machines.append(machine)
    rng = random.Random(2026102784)
    codes = (0, 1, 9, 10, 999999999999, 1000000000000, 0x7fffffffffffffff, 0x8000000000000000, 0xffffffffffffffff)
    vectors = []
    for code in (*codes, *(rng.getrandbits(64) for index in range(256))):
        vectors.append(('saved_identity_decimal_format', code, 0))
        for bits in (-100, -9, -5, -4, -3, -1, 0, 1, 4, 5, 31, 32, 43, 63, 64, 65, 320):
            vectors.append(('saved_identity_base32_format', code, bits))
    for first in (0, 1, 0x7ff, 0x800, 0x1000, 0x1800, 0x7fffffff, 0x80000000, 0xffffffff):
        for second in (0, 1, 0x7fffffff, 0x80000000, 0xffffffff):
            for third in (0, 1, 0xffffffff):
                for key in (0, 0x000100ff, 0x41424344, 0x80ff007f, 0xffffffff):
                    vectors.append(('saved_identity_combined_format', (first, second, third), key))
    for first in (0, 0x1800, 0xffffffff):
        for key in (0, 0x41424344, 0x80ff007f):
            for offset in (0x40, 0x44, 0x48, 0x50):
                vectors.append(('saved_identity_combined_format', (first, 0x12345678, 0xffffffff, BASE + offset), key))
    cases = calls = 0
    for name, value, option in vectors:
        initial = bytearray(rng.randbytes(0x1000))
        expected = bytearray(initial)
        if name == 'saved_identity_decimal_format':
            text = str(value).rjust(12, '0').encode()[:12] + b'\0'
            expected[0x400:0x400 + len(text)] = text
            inputs = (OUTPUT, value & 0xffffffff, value >> 32)
        elif name == 'saved_identity_base32_format':
            numerator = option + 4
            length = abs(numerator) // 5 * (-1 if numerator < 0 else 1)
            if length > 0:
                expected[0x400:0x400 + length] = base32(value, length)
            expected[0x400 + length] = 0
            inputs = (value & 0xffffffff, value >> 32, option & 0xffffffff, OUTPUT)
        else:
            first, second, third = value[:3]
            output = value[3] if len(value) == 4 else OUTPUT
            struct.pack_into('<III', initial, 0x40, first, second, third)
            expected[:] = initial
            text = base32(second | ((first & 0x7ff) << 32), 9) + option.to_bytes(4, 'big') + base32(third, 7) + b'\0'
            expected[output - BASE:output - BASE + len(text)] = text
            inputs = (INPUT, option, output)
        incoming = [rng.getrandbits(32) for register in SAVED]
        stack = rng.randbytes(0x10000)
        guard = rng.randbytes(0x1000)
        row, code = matches[name]
        for machine in machines:
            machine.mem_write(BASE, bytes(initial))
            machine.mem_write(0x021d0000, guard)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), inputs):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            began = time.monotonic()
            machine.emu_start(int(row['address'], 0) | 1, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                raise AssertionError(('Formatter bounded return/ABI', name, inputs))
            actual = bytes(machine.mem_read(BASE, 0x1000))
            if actual != expected or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                differing = [(index, left, right) for index, (left, right) in enumerate(zip(actual, expected)) if left != right][:8]
                raise AssertionError(('Formatter independent complete RAM/guard', name, inputs, differing))
            for string in strings:
                if sha(bytes(machine.mem_read(int(string['address'], 0), string['bytes']))) != string['sha256']:
                    raise AssertionError('Native formatter strings changed')
            calls += 1
        cases += 1
    protocols = 0
    parser = next((row, code) for row, code in reused if int(row['address'], 0) == 0x02096f50)
    for value in (*codes, *(rng.getrandbits(64) for index in range(64))):
        initial = bytearray(rng.randbytes(0x1000))
        expected = bytearray(initial)
        digits = str(value).rjust(12, '0').encode()[:12]
        expected[0x400:0x40d] = digits + b'\0'
        guard = rng.randbytes(0x1000)
        for machine in machines:
            machine.mem_write(BASE, bytes(initial))
            machine.mem_write(0x021d0000, guard)
        operations = ((matches['saved_identity_decimal_format'], (OUTPUT, value & 0xffffffff, value >> 32), None), (parser, (OUTPUT,), int(digits)))
        for (row, code), arguments, result in operations:
            incoming = [rng.getrandbits(32) for register in SAVED]
            for machine in machines:
                machine.mem_write(0x027f0000, rng.randbytes(0x10000))
                for register, word_value in zip(SAVED, incoming):
                    machine.reg_write(register, word_value)
                for register, word_value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                    machine.reg_write(register, word_value)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
                began = time.monotonic()
                machine.emu_start(int(row['address'], 0) | 1, STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                    raise AssertionError(('Formatter/parser protocol bound/ABI', value))
                actual = machine.reg_read(UC_ARM_REG_R0) | (machine.reg_read(UC_ARM_REG_R1) << 32)
                if result is not None and actual != result:
                    raise AssertionError(('Formatter/parser independent truncation', value, result, actual))
                if bytes(machine.mem_read(BASE, 0x1000)) != expected or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                    raise AssertionError(('Formatter/parser protocol RAM/guard', value))
                calls += 1
            cases += 1
        protocols += 1
    malformed = []
    for name, inputs in (('saved_identity_base32_format', (1, 0, 0, 0)), ('saved_identity_base32_format', (1, 0, 5, 0)), ('saved_identity_combined_format', (0, 0x41424344, OUTPUT))):
        initial = rng.randbytes(0x1000)
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        outcomes = []
        for machine in machines:
            machine.mem_write(BASE, initial)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), inputs):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | 1)
            began = time.monotonic()
            try:
                machine.emu_start(SPECS[name][0] | 1, STOP, count=1000000)
            except UcError as error:
                if time.monotonic() - began > 2:
                    raise AssertionError('Formatter malformed fault exceeded bound')
                outcomes.append((str(error), machine.reg_read(UC_ARM_REG_PC), machine.reg_read(UC_ARM_REG_SP), [machine.reg_read(register) for register in SAVED], bytes(machine.mem_read(BASE, 0x1000)), bytes(machine.mem_read(0x027f0000, 0x10000))))
            else:
                raise AssertionError('Formatter malformed pointer unexpectedly returned')
            calls += 1
        expected_pc = 0x02096c90 if name == 'saved_identity_combined_format' else 0x02096ff4 if inputs[2] == 0 else 0x02096fe2
        if outcomes[0] != outcomes[1] or outcomes[0][1] != expected_pc or outcomes[0][4] != initial:
            raise AssertionError(('Formatter malformed partial state/fault location differs', name))
        malformed.append({'name': name, 'arguments': list(inputs), 'fault': outcomes[0][0], 'pc': hex(outcomes[0][1]), 'completeArenaUnchanged': True, 'nativeAndRecompiledFaultStackAndSavedRegistersEqual': True})
        cases += 1
    retained = []
    config = (root / 'config/arm9/symbols.txt').read_text()
    for address in (0x020061ac, 0x02026144, 0x02026124):
        match = re.search(r'kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', config, re.M)
        if not match:
            raise AssertionError(('Formatter retained dependency missing', address))
        size = int(match[1], 0)
        retained.append({'address': hex(address), 'mode': 'arm', 'module': 'main', 'processor': 'arm9', 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])})
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedThumbBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'randomizedInitialStack': True, 'independentByteStringAndIntegerModels': True, 'connectedDecimalFormatParseProtocols': protocols, 'platformStubs': {}, 'reusedAcceptedSources': [row for row, code in reused], 'retainedNativeEntries': retained, 'nativeData': strings, 'malformedPointerCases': malformed, 'observations': ['Decimal formatting uses minimum width12 zero padding and a13-byte snprintf capacity; values exceeding12 decimal digits retain the first12 digits plus terminator.', 'Base32 uses alphabet0123456789abcdefghijklmnopqrstuv, writes ceil(bits/5) low-value digits for positive bits and terminates at the signed truncated division result(bits+4)/5.', 'Combined formatting writes nine login digits, four raw key bytes in big-endian order and seven word2 digits, then a terminator within21 bytes. Embedded zero key bytes do not prevent subsequent output writes.', 'Aliased combined output can overwrite identity storage because both raw fields are consumed into stack buffers before snprintf begins.', 'Decimal format/parse composition round-trips the12 retained digits, including decimal truncation for larger64-bit values.', 'Negative bit counts are bounded pointer-offset observations inside a mapped larger allocation, without asserting legal SDK inputs.'], 'limitations': ['The SDK snprintf and signed division implementations remain native; strings/alphabet are explicitly retained original data without source credit.', 'Synthetic identities and arbitrary formatting arguments do not establish valid profile IDs, user-visible text encoding or online behavior.', 'Signed addition overflow at bits aboveINT_MAX-4 is excluded from the portable-source test domain; no save partition meaning or original input changes.']}
