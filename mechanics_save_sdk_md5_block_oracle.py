import hashlib
import json
import math
import random
import re
import struct
import time

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

BASE = 0x02500000
CONTEXT = BASE + 0x100
OUTPUT = BASE + 0x400
DATA = BASE + 0x1000
STOP = 0x027ff800
INITIAL = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476)
CONSTANTS = tuple(int(abs(math.sin(index + 1)) * (1 << 32)) for index in range(64))
ROTATIONS = ((7, 12, 17, 22), (5, 9, 14, 20), (4, 11, 16, 23), (6, 10, 15, 21))
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x0200cad0, 0x0200cb10, 0x0200cbd8}
    paths = ('evidence/matches/main-runtime04.json', 'evidence/matches/mechanics-save-sdk-md5.json')
    extra = set()
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


def compress(context):
    initial = struct.unpack_from('<IIII', context)
    words = struct.unpack_from('<16I', context, 24)
    a, b, c, d = initial
    for index in range(64):
        if index < 16:
            value, word = (b & c) | (~b & d), index
        elif index < 32:
            value, word = (d & b) | (~d & c), (5 * index + 1) & 15
        elif index < 48:
            value, word = b ^ c ^ d, (3 * index + 5) & 15
        else:
            value, word = c ^ (b | ~d), (7 * index) & 15
        value = (value + a + CONSTANTS[index] + words[word]) & 0xffffffff
        shift = ROTATIONS[index // 16][index & 3]
        rotated = ((value << shift) | (value >> (32 - shift))) & 0xffffffff
        a, d, c, b = d, c, b, (b + rotated) & 0xffffffff
    struct.pack_into('<IIII', context, 0, *((left + right) & 0xffffffff for left, right in zip(initial, (a, b, c, d))))

def update(context, data):
    count = struct.unpack_from('<Q', context, 16)[0]
    used = count & 63
    space = 64 - used
    struct.pack_into('<Q', context, 16, (count + len(data)) & 0xffffffffffffffff)
    if space > len(data):
        context[24 + used:24 + used + len(data)] = data
        return
    context[24 + used:88] = data[:space]
    compress(context)
    consumed = space
    while len(data) - consumed >= 64:
        context[24:88] = data[consumed:consumed + 64]
        compress(context)
        consumed += 64
    if consumed < len(data):
        context[24:24 + len(data) - consumed] = data[consumed:]

def finish(context):
    count = struct.unpack_from('<Q', context, 16)[0]
    update(context, b'\x80')
    used = struct.unpack_from('<Q', context, 16)[0] & 63
    space = 64 - used
    if space < 8:
        context[24 + used:88] = bytes(space)
        compress(context)
        used, space = 0, 64
    if space > 8:
        context[24 + used:80] = bytes(space - 8)
    struct.pack_into('<Q', context, 80, (count << 3) & 0xffffffffffffffff)
    compress(context)
    return bytes(context[:16])

def validate(arm, save, matches, root):
    if set(matches) != {'saved_md5_compress'}:
        raise AssertionError('Complete MD5 compression source batch is required')
    reused = dependencies(root, arm)
    entries = {int(row['address'], 0): row for row, code in [*matches.values(), *reused]}
    if arm[0xdcb6c] != 128:
        raise AssertionError('Native MD5 padding byte differs')
    indices = tuple(((5 * i + 1) & 15) for i in range(16, 32)) + tuple(((3 * i + 5) & 15) for i in range(32, 48)) + tuple(((7 * i) & 15) for i in range(48, 64))
    if struct.unpack_from('<64I', arm, 0xdcc30) != CONSTANTS or struct.unpack_from('<48I', arm, 0xdcb70) != indices:
        raise AssertionError('MD5 retained constants/indices differ from independent calculations')
    retained_data = [{'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'module': 'main', 'processor': 'arm9', 'sourceCredit': 0} for address, size in ((0x020dcc30, 256), (0x020dcb70, 192))]
    machines = []
    entry_counts = [{address: 0 for address in (0x0200cad0, 0x0200cb10, 0x0200cbd8, 0x0200cc90, 0x02008e0c, 0x02008d78)} for engine in range(2)]
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused]:
                actual = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
                    raise AssertionError('MD5 actual MW caller snapshot differs')
                machine.mem_write(int(row['address'], 0), actual)
        engine = int(rebuilt)
        for address in entry_counts[engine]:
            def observe(uc, pc, size, user, engine=engine):
                entry_counts[engine][pc] += 1
            machine.hook_add(UC_HOOK_CODE, observe, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(2026102790)
    cases = calls = 0
    def invoke(address, arguments, expected):
        nonlocal cases, calls
        stack = rng.randbytes(0x10000)
        guard = rng.randbytes(0x1000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        for machine in machines:
            machine.mem_write(0x021d0000, guard)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            began = time.monotonic()
            try:
                machine.emu_start(address, STOP, count=1000000)
            except UcError as error:
                raise AssertionError(('MD5 unexpected valid-call fault', cases, hex(address), hex(machine.reg_read(UC_ARM_REG_PC)), hex(machine.reg_read(UC_ARM_REG_CPSR)), str(error))) from error
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(cases & 1):
                raise AssertionError(('MD5 bounded return/ABI', hex(address), arguments))
            if bytes(machine.mem_read(BASE, 0x4000)) != expected or bytes(machine.mem_read(0x021d0000, 0x1000)) != guard:
                actual = bytes(machine.mem_read(BASE, 0x4000))
                differing = [(index, left, right) for index, (left, right) in enumerate(zip(actual, expected)) if left != right][:8]
                raise AssertionError(('MD5 independent complete arena/guards', hex(address), arguments, differing))
            for data in retained_data:
                data_address = int(data['address'], 0)
                if sha(bytes(machine.mem_read(data_address, data['bytes']))) != data['sha256']:
                    raise AssertionError('MD5 compression changed retained read-only data')
            calls += 1
        cases += 1
    def seed(memory):
        for machine in machines:
            machine.mem_write(BASE, bytes(memory))
    compression_cases = 0
    fixtures = [bytes(88), bytes([255]) * 88, bytes(range(88))]
    for bit in range(128):
        context = bytearray(88)
        context[bit // 8] = 1 << (bit & 7)
        fixtures.append(bytes(context))
    for bit in range(512):
        context = bytearray(88)
        struct.pack_into('<IIII', context, 0, *INITIAL)
        context[24 + bit // 8] = 1 << (bit & 7)
        fixtures.append(bytes(context))
    for byte in range(256):
        context = bytearray(rng.randbytes(88))
        context[24:88] = bytes([byte]) * 64
        fixtures.append(bytes(context))
    fixtures.extend(rng.randbytes(88) for index in range(2048))
    for context in fixtures:
        current = bytearray(rng.randbytes(0x4000))
        current[0x100:0x158] = context
        seed(current)
        expected = bytearray(context)
        compress(expected)
        current[0x100:0x158] = expected
        invoke(0x0200cc90, (CONTEXT,), current)
        compression_cases += 1
    protocols = 0
    for length in (0, 1, 7, 8, 15, 16, 31, 32, 55, 56, 57, 63, 64, 65, 119, 120, 127, 128, 129, 255, 256, 257, 1024, 4096):
        for strategy in range(3):
            current = bytearray(rng.randbytes(0x4000))
            data = bytes(current[0x1000:0x1000 + length])
            seed(current)
            context = bytearray(current[0x100:0x158])
            struct.pack_into('<IIIIQ', context, 0, *INITIAL, 0)
            current[0x100:0x158] = context
            invoke(0x0200cad0, (CONTEXT,), current)
            consumed = 0
            while consumed < length:
                chunk = length - consumed if strategy == 0 else min((1, 7, 63, 64, 65, 129)[(consumed + strategy) % 6], length - consumed)
                update(context, data[consumed:consumed + chunk])
                current[0x100:0x158] = context
                invoke(0x0200cb10, (CONTEXT, DATA + consumed, chunk), current)
                consumed += chunk
            digest = finish(context)
            if digest != hashlib.md5(data).digest():
                raise AssertionError('Independent MD5 compression model disagrees with hashlib')
            current[0x400:0x410] = digest
            current[0x100:0x158] = bytes(88)
            invoke(0x0200cbd8, (OUTPUT, CONTEXT), current)
            protocols += 1
    standard_vectors = ((b'', 'd41d8cd98f00b204e9800998ecf8427e'), (b'a', '0cc175b9c0f1b6a831c399e269772661'), (b'abc', '900150983cd24fb0d6963f7d28e17f72'), (b'message digest', 'f96b697d7cb7938d525a2f31aaf161d0'), (b'abcdefghijklmnopqrstuvwxyz', 'c3fcd3d76192e4007dfb496cca67e13b'), (b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', 'd174ab98d277d9f5a5611c2c9f419d9f'), (b'1234567890' * 8, '57edf4a22be3c955ac49da2e2107b67a'))
    for data, digest_hex in standard_vectors:
        current = bytearray(rng.randbytes(0x4000))
        current[0x1000:0x1000 + len(data)] = data
        seed(current)
        context = bytearray(current[0x100:0x158])
        struct.pack_into('<IIIIQ', context, 0, *INITIAL, 0)
        current[0x100:0x158] = context
        invoke(0x0200cad0, (CONTEXT,), current)
        if data:
            update(context, data)
            current[0x100:0x158] = context
            invoke(0x0200cb10, (CONTEXT, DATA, len(data)), current)
        digest = finish(context)
        if digest.hex() != digest_hex or hashlib.md5(data).hexdigest() != digest_hex:
            raise AssertionError('MD5 standard literal/model/hashlib vector differs')
        current[0x400:0x410] = digest
        current[0x100:0x158] = bytes(88)
        invoke(0x0200cbd8, (OUTPUT, CONTEXT), current)
        protocols += 1
    counts = (0, 1, 55, 56, 63, 64, 65, 0x7fffffff, 0xfffffffe, 0xffffffff, 0x100000000, 0xfffffffffffffffe, 0xffffffffffffffff)
    synthetic = 0
    for count in counts:
        for length in (0, 1, 2, 7, 8, 63, 64, 65, 127, 128, 255):
            current = bytearray(rng.randbytes(0x4000))
            struct.pack_into('<Q', current, 0x110, count)
            seed(current)
            context = bytearray(current[0x100:0x158])
            update(context, current[0x1000:0x1000 + length])
            current[0x100:0x158] = context
            invoke(0x0200cb10, (CONTEXT, DATA if length else 0, length), current)
            synthetic += 1
        for output_offset in (0x100, 0x104, 0x110, 0x14c, 0x150, 0x158, 0x15c, 0x400):
            current = bytearray(rng.randbytes(0x4000))
            struct.pack_into('<Q', current, 0x110, count)
            seed(current)
            context = bytearray(current[0x100:0x158])
            digest = finish(context)
            current[0x100:0x158] = context
            current[output_offset:output_offset + 16] = digest
            current[0x100:0x158] = bytes(88)
            invoke(0x0200cbd8, (BASE + output_offset, CONTEXT), current)
            synthetic += 1
    malformed = []
    for address, arguments, expected_pc in ((0x0200cc90, (0,), 0x0200cc94), (0x0200cc90, (0x027ffff0,), 0x0200ccb8), (0x0200cb10, (0, DATA, 1), 0x0200cb18), (0x0200cbd8, (OUTPUT, 0), 0x0200cbe0), (0x0200cb10, (CONTEXT, 0, 1), 0x02008f24)):
        initial = bytearray(rng.randbytes(0x4000))
        if arguments[0] == CONTEXT:
            struct.pack_into('<Q', initial, 0x110, 0)
        expected_arena = bytearray(initial)
        if arguments[0] == CONTEXT:
            struct.pack_into('<Q', expected_arena, 0x110, 1)
        seed(initial)
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        outcomes = []
        for machine in machines:
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            try:
                machine.emu_start(address, STOP, count=1000000)
            except UcError as error:
                if time.monotonic() - began > 2:
                    raise AssertionError('MD5 malformed fault exceeded bound')
                outcomes.append((str(error), machine.reg_read(UC_ARM_REG_PC), machine.reg_read(UC_ARM_REG_SP), [machine.reg_read(register) for register in SAVED], bytes(machine.mem_read(BASE, 0x4000)), bytes(machine.mem_read(0x027f0000, 0x10000))))
            else:
                raise AssertionError('MD5 malformed pointer unexpectedly returned')
            calls += 1
        if outcomes[0] != outcomes[1] or outcomes[0][1] != expected_pc or outcomes[0][4] != expected_arena:
            raise AssertionError('MD5 malformed partial state/fault location differs')
        malformed.append({'address': hex(address), 'arguments': list(arguments), 'fault': outcomes[0][0], 'pc': hex(outcomes[0][1]), 'completeArenaUnchanged': initial == expected_arena, 'partialByteCountIncrementedBeforeInputFault': arguments[0] == CONTEXT, 'nativeAndRecompiledFaultStackAndSavedRegistersEqual': True})
        cases += 1
    config = (root / 'config/arm9/symbols.txt').read_text()
    retained = []
    for address in (0x02008e0c, 0x02008d78):
        match = re.search(r'kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', config, re.M)
        if not match:
            raise AssertionError(('MD5 native dependency span missing', address))
        size = int(match[1], 0)
        retained.append({'address': hex(address), 'module': 'main', 'processor': 'arm9', 'mode': 'arm', 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])})
    if entry_counts[0] != entry_counts[1] or not all(entry_counts[0].values()):
        raise AssertionError('MD5 connected source/native boundary entry coverage differs')
    return {'compressionStateCases': compression_cases, 'allStateAndBlockBitsCovered': True, 'allUniformInputByteValuesCovered': 256, 'entryCountsPerEngine': [{hex(address): count for address, count in values.items()} for values in entry_counts], 'retainedConstantsAndIndices': retained_data, 'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'validHashlibStreamingProtocols': protocols, 'standardLiteralDigestVectors': [{'messageHex': data.hex(), 'digestHex': digest} for data, digest in standard_vectors], 'syntheticCounterStateAndAliasCases': synthetic, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedSourceBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'independentCompressionStateAndHashlibModels': True, 'platformStubs': {}, 'reusedAcceptedSources': [row for row, code in reused], 'retainedNativeEntries': retained, 'nativePaddingData': {'address': '0x020dcb6c', 'module': 'main', 'processor': 'arm9', 'bytes': 1, 'sha256': sha(arm[0xdcb6c:0xdcb6d]), 'sourceCredit': 0}, 'malformedPointerCases': malformed, 'observations': ['The88-byte context contains four state words, a64-bit little-endian byte count at+16 and a64-byte buffer at+24.', 'Update increments the64-bit count modulo2^64 before copying/compressing, processes all full64-byte blocks and preserves the unused tail of its last buffer.', 'Finalization appends byte0x80, zero padding and the original byte count times8 modulo2^64 in little endian; it emits16 state bytes then clears the entire88-byte context.', 'Hashlib agrees with independent intermediate compression states for72 random valid message/chunk protocols through4096 bytes and seven standard literal digest vectors.', 'Synthetic counters crossing32/64-bit wrap and arbitrary states are modeled separately; output aliasing inside the context is cleared by final context zeroing.'], 'limitations': ['All four MD5 bodies execute matched C; the304-byte copy and148-byte fill remain native implementations with qualified source/hash boundaries.', 'Synthetic arbitrary states/counters characterize target mechanics and are not valid-message digest claims.', 'No authentication, collision resistance, physical save timing, bank chronology or semantic partition promotion is claimed; original inputs remain unchanged.']}
