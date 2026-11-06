import hashlib
import json
import random
import re
import struct
import time

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from mechanics_save_identity_core_thumb_oracle import expected_code
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

BASE = 0x02500000
INPUT = BASE + 0x40
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02096ed0}
    paths = ('evidence/matches/main-thumb-runtime02.json', 'evidence/matches/mechanics-save-identity-core-thumb.json', 'evidence/matches/mechanics-save-identity-values-thumb.json')
    extra = {0x02096e74, 0x02096f10}
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


def valid(code, key, mode):
    low = code & 0xffffffff
    return int(0 < low < 0x80000000 and code == expected_code(low, key, mode))

def validate(arm, save, matches, root):
    if set(matches) != {'saved_identity_code_valid'}:
        raise AssertionError('Complete identity validator source batch is required')
    reused = dependencies(root, arm)
    by_address = {int(row['address'], 0): (row, code) for row, code in reused}
    seen = {0x02096ee4: 0, 0x02096e74: 0}
    def entry(machine, address, size, user):
        seen[address] += 1
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused]:
                actual = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
                    raise AssertionError('Validator actual MW caller snapshot differs')
                machine.mem_write(int(row['address'], 0), actual)
        for address in seen:
            machine.hook_add(UC_HOOK_CODE, entry, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(2026102786)
    identities = (0, 1, 2, 127, 255, 65535, 0x7fffffff, 0x80000000, 0xffffffff)
    keys = (0, 1, 0xffffffff, 0x4a324a42)
    modes = (0, 1, 2, 0xffffffff, 0x80000000, 0x7fffffff)
    vectors = []
    for identity in identities:
        for key in keys:
            for mode in modes:
                code = expected_code(identity, key, mode)
                vectors.extend((code ^ corrupt, key, mode) for corrupt in (0, 1, 1 << 31, 1 << 32, 1 << 40, 1 << 63))
    for index in range(128):
        code, key = rng.getrandbits(64), rng.getrandbits(32)
        vectors.extend((code, key, mode) for mode in (0, 1))
    for mode in (0, 1):
        code = expected_code(1, 0, mode)
        vectors.extend((code ^ (1 << bit), 0, mode) for bit in range(64))
    calls = cases = 0
    direct = matches['saved_identity_code_valid']
    constructor_calls = validator_calls = 0
    for code, key, mode in vectors:
        low, high = code & 0xffffffff, code >> 32
        positive = 0 < low < 0x80000000
        crc_valid = bool(valid(code, key, 0))
        extraction = low if crc_valid or valid(code, key, 1) else 0
        operations = (
            (direct, (low, high, key, mode), valid(code, key, mode), 1, int(positive)),
            (by_address[0x02096ed0], (INPUT, low, high), valid(code, key, 1), 1, int(positive)),
            (by_address[0x02096f10], (low, high, key), extraction, 1 if crc_valid else 2, (1 if crc_valid else 2) if positive else 0))
        for (row, binary), arguments, expected, expected_validator, expected_constructor in operations:
            initial = bytearray(rng.randbytes(0x1000))
            struct.pack_into('<I', initial, 0x64, key)
            guard = rng.randbytes(0x1000)
            stack = rng.randbytes(0x10000)
            incoming = [rng.getrandbits(32) for register in SAVED]
            for machine in machines:
                for address in seen:
                    seen[address] = 0
                machine.mem_write(BASE, bytes(initial))
                machine.mem_write(0x021d0000, guard)
                machine.mem_write(0x027f0000, stack)
                for register, value in zip(SAVED, incoming):
                    machine.reg_write(register, value)
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), arguments):
                    machine.reg_write(register, value)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
                began = time.monotonic()
                machine.emu_start(int(row['address'], 0) | 1, STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                    raise AssertionError(('Validator bounded return/ABI', row['name'], code, key, mode))
                if machine.reg_read(UC_ARM_REG_R0) != expected:
                    raise AssertionError(('Validator independent CRC/MD5/signed-word result', row['name'], hex(code), key, mode, expected))
                if bytes(machine.mem_read(BASE, 0x1000)) != initial or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                    raise AssertionError(('Validator complete input/global guards', row['name']))
                if seen != {0x02096ee4: expected_validator, 0x02096e74: expected_constructor}:
                    raise AssertionError(('Validator/constructor call short-circuit differs', row['name'], seen, expected_validator, expected_constructor))
                calls += 1
                constructor_calls += expected_constructor
                validator_calls += expected_validator
            cases += 1
    initial = rng.randbytes(0x1000)
    stack = rng.randbytes(0x10000)
    incoming = [rng.getrandbits(32) for register in SAVED]
    outcomes = []
    for machine in machines:
        machine.mem_write(BASE, initial)
        machine.mem_write(0x027f0000, stack)
        for register, value in zip(SAVED, incoming):
            machine.reg_write(register, value)
        for register, value in ((UC_ARM_REG_R0, 0), (UC_ARM_REG_R1, 1), (UC_ARM_REG_R2, 0), (UC_ARM_REG_SP, 0x027ff000), (UC_ARM_REG_LR, STOP | 1)):
            machine.reg_write(register, value)
        began = time.monotonic()
        try:
            machine.emu_start(0x02096ed1, STOP, count=1000000)
        except UcError as error:
            if time.monotonic() - began > 2:
                raise AssertionError('Validator wrapper malformed fault exceeded bound')
            outcomes.append((str(error), machine.reg_read(UC_ARM_REG_PC), machine.reg_read(UC_ARM_REG_SP), [machine.reg_read(register) for register in SAVED], bytes(machine.mem_read(BASE, 0x1000)), bytes(machine.mem_read(0x027f0000, 0x10000))))
        else:
            raise AssertionError('Validator null profile wrapper unexpectedly returned')
        calls += 1
    if outcomes[0] != outcomes[1] or outcomes[0][1] != 0x02096ed8 or outcomes[0][4] != initial:
        raise AssertionError('Validator wrapper malformed partial state/fault location differs')
    cases += 1
    malformed = [{'address': '0x02096ed0', 'argument': 0, 'fault': outcomes[0][0], 'pc': hex(outcomes[0][1]), 'completeArenaUnchanged': True, 'nativeAndRecompiledFaultStackAndSavedRegistersEqual': True}]
    core = json.loads((root / 'evidence/matches/mechanics-save-identity-core-thumb.json').read_text(encoding='utf-8'))
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedThumbBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'randomizedInitialStack': True, 'independentCrc8AndHashlibMd5ExpectedValues': True, 'verifiedValidatorEntriesAcrossNativeAndRecompiled': validator_calls, 'verifiedConstructorEntriesAcrossNativeAndRecompiled': constructor_calls, 'malformedPointerCases': malformed, 'platformStubs': {}, 'reusedAcceptedSources': [row for row, binary in reused], 'retainedNativeEntries': [row for row in core['oracle']['retainedNativeEntries'] if int(row['address'], 0) in (0x020199e0, 0x02019b58, 0x0200cad0, 0x0200cb10, 0x0200cbd8)], 'observations': ['Validation rejects low words whose signed32 value is nonpositive before entering the constructor; every positive low word invokes the selected CRC8/MD5 constructor and compares all64 bits.', 'Mode0 selects CRC8; every other tested signed32 mode selects MD5 through the accepted constructor default branch.', 'The18-byte profile wrapper forces MD5 mode1 and reads key at profile+36.', 'The44-byte extraction caller tries CRC mode0 before MD5 mode1, stops on first match and returns the positive low word; invalid/signed-nonpositive codes return0.', 'All64 one-bit mutations of CRC and MD5 codes, high tag corruption, arbitrary64-bit values and signed low-word boundaries are independently modeled.'], 'limitations': ['CRC/MD5 primitives remain retained native dependencies with independent Python expected values; full profile/code legality or collision resistance is not claimed.', 'This is caller/constructor/validator composition, not complete identity equality, parsing or online service reconstruction.', 'No original input or semantic save partition changes are made.']}
