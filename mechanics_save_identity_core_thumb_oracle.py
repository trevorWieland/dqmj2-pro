import hashlib
import random
import re
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

INPUT = 0x02500040
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def crc8(data):
    value = 0
    for byte in data:
        value ^= byte
        for bit in range(8):
            value = ((value << 1) ^ (7 if value & 128 else 0)) & 255
    return value

def expected_code(identity, key, mode):
    data = struct.pack('<II', identity, key)
    tag = crc8(data) & 127 if mode == 0 else (hashlib.md5(data).digest()[0] >> 1) & 127
    return identity | (tag << 32)

def validate(arm, save, matches, root):
    required = {'saved_identity_code', 'saved_sdk_identity_kind_set', 'saved_sdk_profile_code', 'saved_sdk_identity_create'}
    if set(matches) != required:
        raise AssertionError('Complete identity Thumb source batch is required')
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in matches.values():
                linked = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(linked) != row['isolatedCallerBinarySha256'] or linked != code:
                    raise AssertionError('Identity Thumb actual MW caller binary differs')
                machine.mem_write(int(row['address'], 16), linked)
        machines.append(machine)
    rng = random.Random(2026102780)
    identities = (0, 1, 2, 127, 255, 65535, 0x7fffffff, 0x80000000, 0xffffffff)
    keys = (0, 1, 0xffffffff, struct.unpack_from('<I', (root / 'inputs/game.nds').read_bytes(), 12)[0])
    modes = (0, 1, 2, -1, -2147483648, 2147483647)
    vectors = [('saved_identity_code', (identity, key, mode), 0) for identity in identities for key in keys for mode in modes]
    vectors += [('saved_identity_code', (rng.getrandbits(32), rng.getrandbits(32), mode), 0) for index in range(128) for mode in (0, 1)]
    vectors += [('saved_sdk_profile_code', (identity, key), 0) for identity in identities for key in keys]
    vectors += [('saved_sdk_profile_code', (rng.getrandbits(32), rng.getrandbits(32)), 0) for index in range(32)]
    vectors += [('saved_sdk_identity_kind_set', (kind,), flags) for flags in (0, 1, 0x7ff, 0x800, 0x1000, 0x1800, 0x80000000, 0xffffffff) for kind in (0, 1, 2, 3, 4, 7, 0x1fffff, 0x200000, 0x80000000, 0xffffffff)]
    vectors += [('saved_sdk_identity_kind_set', (rng.getrandbits(32),), rng.getrandbits(32)) for index in range(128)]
    vectors += [('saved_sdk_identity_create', (identity, key), 0) for identity in identities for key in keys]
    vectors += [('saved_sdk_identity_create', (rng.getrandbits(32), rng.getrandbits(32)), 0) for index in range(32)]
    cases = calls = 0
    for name, arguments, flags in vectors:
        memory = bytearray(rng.randbytes(0x1000))
        guard = rng.randbytes(0x1000)
        result = None
        if name == 'saved_identity_code':
            inputs = arguments
            result = expected_code(*arguments)
        elif name == 'saved_sdk_profile_code':
            struct.pack_into('<I', memory, 0x40 + 28, arguments[0])
            struct.pack_into('<I', memory, 0x40 + 36, arguments[1])
            inputs = (INPUT,)
            result = expected_code(*arguments, 1) if arguments[0] else 0
        elif name == 'saved_sdk_identity_kind_set':
            struct.pack_into('<I', memory, 0x40, flags)
            inputs = (INPUT, arguments[0])
            value = (((flags >> 11) & 0x1fffff) & ~3) | arguments[0]
            success = not value & ~0x1fffff
            result = int(success)
        else:
            inputs = (INPUT, *arguments)
        expected = bytearray(memory)
        if name == 'saved_sdk_identity_kind_set' and success:
            struct.pack_into('<I', expected, 0x40, (flags & 0x7ff) | (value << 11))
        elif name == 'saved_sdk_identity_create':
            struct.pack_into('<III', expected, 0x40, 0x1000, *arguments)
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        return_thumb = cases & 1
        row, code = matches[name]
        for machine in machines:
            machine.mem_write(0x02500000, bytes(memory))
            machine.mem_write(0x021d0000, guard)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), inputs):
                machine.reg_write(register, value & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | return_thumb)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16) | 1, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(return_thumb):
                raise AssertionError(('Identity Thumb bounded return/ABI/state', name, arguments))
            actual = machine.reg_read(UC_ARM_REG_R0)
            if name in ('saved_identity_code', 'saved_sdk_profile_code'):
                actual |= machine.reg_read(UC_ARM_REG_R1) << 32
            if result is not None and actual != result:
                raise AssertionError(('Independent identity CRC/MD5/flags result', name, arguments, hex(result), hex(actual)))
            if bytes(machine.mem_read(0x02500000, 0x1000)) != expected or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                raise AssertionError(('Identity Thumb complete data/guard differs', name, arguments))
            calls += 1
        cases += 1
    config = (root / 'config/arm9/symbols.txt').read_text()
    from match_mechanics_save_identity_core_thumb import GLOBALS
    retained = []
    for name, (address, mode) in GLOBALS.items():
        boundary = re.search(r'kind:function\(' + mode + r',size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', config, re.M)
        if not boundary:
            raise AssertionError(('Identity Thumb dependency mode/range missing', name))
        size = int(boundary[1], 0)
        retained.append({'name': name, 'module': 'main', 'processor': 'arm9', 'mode': mode, 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])})
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedThumbBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'randomizedInitialStack': True, 'independentCrc8Polynomial7AndHashlibMd5ExpectedValues': True, 'platformStubs': {}, 'retainedNativeEntries': retained, 'reusedAcceptedSources': [], 'observations': ['The64-bit code retains the first input word in its low32 bits and a7-bit tag in its high word.', 'Mode0 uses CRC-8 polynomial7 over the eight little-endian input bytes, masks the result to7 bits; all other tested signed modes use the first MD5 digest byte shifted right1 and masked to7 bits.', 'Profile code returns0 for a zero word at+0x1C, otherwise hashes that word with+0x24 in mode1.', 'Type update changes the low two flags within a21-bit field at word0 bits11..31, preserving lower11 bits; arguments setting bits above the21-bit field are rejected unchanged by the retained checked writer.', 'Creation clears12 bytes, stores low/high words at+4/+8 and sets raw type2, yielding first word0x1000.', 'The C bodies return correctly to either ARM or Thumb callers under randomized stack and preserved-register state.'], 'limitations': ['CRC/MD5 and selected SDK field/memory primitives remain native dependencies; this report recovers the four Thumb callers, not those callee implementations.', 'Observed arbitrary mode/kind inputs are bounded native probes and do not certify valid profile IDs, SDK kinds or online legality.', 'Hash inputs establish raw word use without semantic-partition promotion or original profile changes.']}
