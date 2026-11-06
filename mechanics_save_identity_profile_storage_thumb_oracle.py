import hashlib
import json
import random
import re
import struct
import time
import zlib

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from mechanics_save_identity_core_thumb_oracle import expected_code
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

BASE = 0x02500000
PROFILE = BASE + 0x40
IDENTITY = BASE + 0x100
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02096ce4, 0x02096cf8, 0x02096ce8, 0x02096da4, 0x0209718c, 0x02097178, 0x02096cbc}
    paths = ('evidence/matches/main-thumb-runtime02.json', 'evidence/matches/mechanics-save-identity-core-thumb.json', 'evidence/matches/mechanics-save-identity-values-thumb.json')
    extra = {0x02096db4, 0x02096cac, 0x02096c6c, 0x02096f10, 0x02096e74}
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

def word(data, offset):
    return struct.unpack_from('<I', data, offset)[0]

def put(data, offset, value):
    struct.pack_into('<I', data, offset, value & 0xffffffff)

def model(name, data, arguments):
    profile = arguments[0] - BASE
    result = None
    if name == 'saved_profile_checksum_valid':
        result = int(zlib.crc32(data[profile:profile + 60]) == word(data, profile + 60))
    elif name == 'saved_profile_dirty':
        result = word(data, profile + 32) & 1
    elif name == 'saved_profile_checksum_refresh':
        put(data, profile + 32, word(data, profile + 32) & ~1)
        put(data, profile + 60, zlib.crc32(data[profile:profile + 60]))
    elif name == 'saved_profile_identity_write':
        source = arguments[1] - BASE
        data[profile + 16:profile + 28] = data[source:source + 12]
        put(data, profile + 28, arguments[2])
        put(data, profile + 60, zlib.crc32(data[profile:profile + 60]))
        put(data, profile + 32, word(data, profile + 32) | 1)
    elif name == 'saved_profile_identity_read':
        target = arguments[1] - BASE
        data[target:target + 12] = bytes(12)
        if (word(data, profile + 16) >> 11) & 3 == 1:
            put(data, target + 4, word(data, profile + 28))
            put(data, target, 0x1800)
        else:
            data[target:target + 12] = data[profile + 4:profile + 16]
    elif name == 'saved_identity_word_create':
        data[profile:profile + 12] = struct.pack('<III', 0x1800, arguments[1], 0)
    elif name == 'saved_profile_identity_value':
        identity = arguments[1] - BASE
        flags, low, high = struct.unpack_from('<III', data, identity)
        kind = (flags >> 11) & 3
        result = 0
        if kind == 1:
            result = 0xffffffff
        elif kind == 3:
            result = low
        elif kind == 2 and 0 < low < 0x80000000:
            key = word(data, profile + 36)
            code = low | (high << 32)
            if any(expected_code(low, key, mode) == code for mode in (0, 1)):
                result = low
    else:
        raise AssertionError(name)
    return result

def validate(arm, save, matches, root):
    from match_mechanics_save_identity_profile_storage_thumb import SPECS, GLOBALS
    if set(matches) != set(SPECS):
        raise AssertionError('Complete profile storage source batch is required')
    reused = dependencies(root, arm)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused]:
                actual = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
                    raise AssertionError('Profile actual MW caller snapshot differs')
                machine.mem_write(int(row['address'], 0), actual)
        machines.append(machine)
    rng = random.Random(2026102782)
    vectors = []
    for index in range(256):
        data = bytearray(rng.randbytes(0x1000))
        put(data, 0x40 + 32, index)
        put(data, 0x40 + 16, (word(data, 0x50) & ~0x1800) | ((index & 3) << 11))
        if index & 1:
            put(data, 0x40 + 60, zlib.crc32(data[0x40:0x7c]))
        vectors.extend((name, bytes(data), arguments) for name, arguments in (
            ('saved_profile_checksum_valid', (PROFILE,)), ('saved_profile_dirty', (PROFILE,)),
            ('saved_profile_checksum_refresh', (PROFILE,)), ('saved_profile_identity_write', (PROFILE, IDENTITY, rng.getrandbits(32))),
            ('saved_profile_identity_read', (PROFILE, IDENTITY)), ('saved_identity_word_create', (IDENTITY, rng.getrandbits(32)))))
    for identity in (0, 1, 2, 0x7fffffff, 0x80000000, 0xffffffff):
        for key in (0, 1, 0xffffffff, 0x4a324a42):
            for kind in range(4):
                for mode in (0, 1):
                    for corrupt in (0, 1, 1 << 32, 1 << 63):
                        data = bytearray(rng.randbytes(0x1000))
                        code = expected_code(identity, key, mode) ^ corrupt
                        struct.pack_into('<III', data, 0x100, (rng.getrandbits(32) & ~0x1800) | (kind << 11), code & 0xffffffff, code >> 32)
                        put(data, 0x40 + 36, key)
                        vectors.append(('saved_profile_identity_value', bytes(data), (PROFILE, IDENTITY)))
    for offset in (0x40, 0x44, 0x50, 0x5c, 0x60, 0x7c):
        for kind in range(4):
            data = bytearray(rng.randbytes(0x1000))
            put(data, 0x50, (word(data, 0x50) & ~0x1800) | (kind << 11))
            vectors.append(('saved_profile_identity_read', bytes(data), (PROFILE, BASE + offset)))
            vectors.append(('saved_profile_identity_write', bytes(data), (PROFILE, BASE + offset, 0x80000001)))
    cases = calls = 0
    for name, initial, arguments in vectors:
        expected = bytearray(initial)
        result = model(name, expected, arguments)
        incoming = [rng.getrandbits(32) for register in SAVED]
        stack = rng.randbytes(0x10000)
        guard = rng.randbytes(0x1000)
        row, code = matches[name]
        for machine in machines:
            machine.mem_write(BASE, initial)
            machine.mem_write(0x021d0000, guard)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            began = time.monotonic()
            machine.emu_start(int(row['address'], 0) | 1, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                raise AssertionError(('Profile bounded return/ABI/state', name, arguments))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('Profile independent result', name, result, machine.reg_read(UC_ARM_REG_R0)))
            if bytes(machine.mem_read(BASE, 0x1000)) != expected or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                raise AssertionError(('Profile independent complete RAM/guard', name, arguments))
            calls += 1
        cases += 1
    protocols = 0
    for flags in range(64):
        current = bytearray(rng.randbytes(0x1000))
        put(current, 0x60, flags)
        guard = rng.randbytes(0x1000)
        for machine in machines:
            machine.mem_write(BASE, bytes(current))
            machine.mem_write(0x021d0000, guard)
        operations = (
            ('saved_profile_identity_write', (PROFILE, IDENTITY, rng.getrandbits(32))),
            ('saved_profile_dirty', (PROFILE,)), ('saved_profile_checksum_valid', (PROFILE,)),
            ('saved_profile_checksum_refresh', (PROFILE,)), ('saved_profile_dirty', (PROFILE,)),
            ('saved_profile_checksum_valid', (PROFILE,)))
        for name, arguments in operations:
            result = model(name, current, arguments)
            incoming = [rng.getrandbits(32) for register in SAVED]
            for machine in machines:
                machine.mem_write(0x027f0000, rng.randbytes(0x10000))
                for register, value in zip(SAVED, incoming):
                    machine.reg_write(register, value)
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                    machine.reg_write(register, value)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
                began = time.monotonic()
                machine.emu_start(SPECS[name][0] | 1, STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                    raise AssertionError(('Profile protocol bound/ABI', name, flags))
                if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                    raise AssertionError(('Profile protocol result', name, flags))
                if bytes(machine.mem_read(BASE, 0x1000)) != current or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                    raise AssertionError(('Profile protocol RAM/guard', name, flags))
                calls += 1
            cases += 1
        protocols += 1
    malformed = []
    for name, arguments in (('saved_profile_dirty', (0,)), ('saved_profile_checksum_valid', (0,)), ('saved_profile_identity_write', (0, IDENTITY, 7)), ('saved_profile_identity_write', (PROFILE, 0, 7))):
        initial = rng.randbytes(0x1000)
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        outcomes = []
        for machine in machines:
            machine.mem_write(BASE, initial)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | 1)
            began = time.monotonic()
            try:
                machine.emu_start(SPECS[name][0] | 1, STOP, count=1000000)
            except UcError as error:
                if time.monotonic() - began > 2:
                    raise AssertionError('Profile malformed fault exceeded time bound')
                outcomes.append((str(error), machine.reg_read(UC_ARM_REG_PC), machine.reg_read(UC_ARM_REG_SP), [machine.reg_read(register) for register in SAVED], bytes(machine.mem_read(BASE, 0x1000)), bytes(machine.mem_read(0x027f0000, 0x10000))))
            else:
                raise AssertionError('Profile malformed pointer unexpectedly returned')
            calls += 1
        expected_pc = {'saved_profile_dirty': 0x020972a8, 'saved_profile_checksum_valid': 0x02019b30}.get(name, 0x0209726e if arguments[0] == 0 else 0x0209726a)
        if outcomes[0][1] != expected_pc:
            raise AssertionError(('Profile malformed fault location differs', name))
        if outcomes[0] != outcomes[1] or outcomes[0][4] != initial:
            raise AssertionError(('Profile malformed partial state differs', name))
        malformed.append({'name': name, 'arguments': [hex(value) for value in arguments], 'fault': outcomes[0][0], 'pc': hex(outcomes[0][1]), 'completeArenaUnchanged': True, 'nativeAndRecompiledFaultStackAndSavedRegistersEqual': True})
        cases += 1
    config = (root / 'config/arm9/symbols.txt').read_text()
    retained = []
    patched = {int(row['address'], 0) for row, code in reused}
    for name, (address, mode) in {**GLOBALS, 'native_code_validator': (0x02096ee4, 'thumb')}.items():
        if address in patched:
            continue
        match = re.search(r'kind:function\(' + mode + r',size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', config, re.M)
        if not match:
            raise AssertionError(('Profile native dependency missing', name))
        size = int(match[1], 0)
        retained.append({'name': name, 'address': hex(address), 'bytes': size, 'mode': mode, 'module': 'main', 'processor': 'arm9', 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])})
    core = json.loads((root / 'evidence/matches/mechanics-save-identity-core-thumb.json').read_text(encoding='utf-8'))
    for entry in core['oracle']['retainedNativeEntries']:
        if int(entry['address'], 0) not in patched and not any(row['address'] == entry['address'] for row in retained):
            retained.append(entry)
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'connectedWriteDirtyChecksumRefreshProtocols': protocols, 'malformedPointerCases': malformed, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedThumbBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'randomizedInitialStack': True, 'independentPythonZlibCrc32AndHashlibModels': True, 'platformStubs': {}, 'reusedAcceptedSources': [row for row, code in reused], 'retainedNativeEntries': retained, 'observations': ['Profile64-byte checksum covers bytes0..59 using standard reflected CRC32 polynomialEDB88320 with all-one initialization and final inversion.', 'Identity write copies12 bytes into+16, writes raw value+28, computes checksum, then sets flags+32 bit0; a previously clear dirty bit therefore invalidates the just-written checksum.', 'Checksum refresh clears flags+32 bit0 before computing/storing checksum+60.', 'Profile identity read clears its12-byte output before testing type1 at profile+16; type1 creates raw type3 from profile+28, otherwise it copies profile+4.', 'Raw type1 value dispatch returnsFFFFFFFF; type2 validates both CRC and MD5 code modes using profile key+36; type3 returns word1; type0 returns0.', 'Aliased output/input cases retain native clear/copy ordering and are independently modeled.'], 'limitations': ['CRC32 table/update and memory fill remain native dependencies; the44-byte identity validator is unaccepted native code.', 'Partially overlapping struct-copy probes compare native and compiled binary behavior, without asserting portable defined C semantics for such overlap.', 'These routines establish raw profile storage behavior, not profile authenticity, online behavior or complete save legality.', 'No semantic save partition or original input is changed.']}
