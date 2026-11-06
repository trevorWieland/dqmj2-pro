import hashlib
import json
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from mechanics_save_sdk_md5_complete_oracle import dependencies
from mechanics_save_sdk_md5_oracle import INITIAL, CONSTANTS, ROTATIONS, compress, update, finish

BASE = 0x02500000
CONTEXT = BASE + 0x100
DATA = BASE + 0x1000
OUTPUT = BASE + 0x400
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_code(root, arm):
    result = dependencies(root, arm)
    document = json.loads((root / 'evidence/matches/mechanics-save-sdk-memory-original-asm.json').read_text(encoding='utf-8'))
    wanted = {0x02008d78, 0x02008e0c}
    for row in document['matches']:
        if int(row['address'], 0) not in wanted or row['sourceLanguage'] != 'assembly' or row['ordinaryCBytes']:
            raise AssertionError('MD5 data consumer helper classification differs')
        for field in ('source', 'object'):
            if sha((root / row[field]).read_bytes()) != row[field + 'Sha256']:
                raise AssertionError('MD5 data consumer helper source/object differs')
        code = (root / row['isolatedCallerBinary']).read_bytes()
        if sha(code) != row['isolatedCallerBinarySha256'] or code != arm[int(row['address'], 0) - 0x02000000:int(row['address'], 0) - 0x02000000 + row['bytes']]:
            raise AssertionError('MD5 data consumer actual MW binary differs')
        result.append((row, code))
    if len(result) != 6:
        raise AssertionError('MD5 typed data requires six complete recovered code bodies')
    return result


def compress_variant(context, constants, indices):
    initial = struct.unpack_from('<4I', context)
    words = struct.unpack_from('<16I', context, 24)
    a, b, c, d = initial
    for step in range(64):
        if step < 16:
            value, word = (b & c) | (~b & d), step
        elif step < 32:
            value, word = (b & d) | (c & ~d), indices[step - 16]
        elif step < 48:
            value, word = b ^ c ^ d, indices[step - 16]
        else:
            value, word = c ^ (b | ~d), indices[step - 16]
        value = (a + value + words[word] + constants[step]) & 0xffffffff
        shift = ROTATIONS[step // 16][step & 3]
        rotated = ((value << shift) | (value >> (32 - shift))) & 0xffffffff
        a, d, c, b = d, c, b, (b + rotated) & 0xffffffff
    struct.pack_into('<4I', context, 0, *((left + right) & 0xffffffff for left, right in zip(initial, (a, b, c, d))))


def finish_with_padding(context, padding):
    count = struct.unpack_from('<Q', context, 16)[0]
    update(context, bytes([padding]))
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
    if set(matches) != {'saved_md5_padding', 'saved_md5_indices', 'saved_md5_constants'}:
        raise AssertionError('MD5 typed data requires all three derived objects')
    code_rows = source_code(root, arm)
    known_bytes = set()
    for row, payload in matches.values():
        address = int(row['address'], 0)
        known_bytes.update(range(address, address + row['bytes']))
        for field in ('source', 'object'):
            if sha((root / row[field]).read_bytes()) != row[field + 'Sha256']:
                raise AssertionError('MD5 typed data source/object identity differs')
        actual = (root / row['linkedDataBinary']).read_bytes()
        if actual != payload or sha(actual) != row['linkedDataBinarySha256']:
            raise AssertionError('MD5 actual MW linked typed data differs')
    machines = []
    data_reads = [set(), set()]
    gap_reads = [set(), set()]
    entries = [{int(row['address'], 0): 0 for row, code in code_rows} for engine in range(2)]
    ranges = [(int(row['address'], 0), int(row['address'], 0) + row['bytes']) for row, code in code_rows]
    for engine in range(2):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        for address, size in ((0x02008000, 0x1000), (0x0200c000, 0x2000), (0x020dc000, 0x1000), (BASE, 0x8000), (0x027f0000, 0x10000)):
            machine.mem_map(address, size)
        for row, code in code_rows:
            address = int(row['address'], 0)
            machine.mem_write(address, code if engine else arm[address - 0x02000000:address - 0x02000000 + row['bytes']])
        def observed(uc, pc, size, user, engine=engine):
            if not any(start <= pc < end for start, end in ranges):
                raise AssertionError(('MD5 data execution escaped recovered source code', hex(pc)))
            if pc in entries[engine]:
                entries[engine][pc] += 1
        def read(uc, access, address, size, value, user, engine=engine):
            for offset in range(size):
                position = address + offset
                if position in known_bytes:
                    data_reads[engine].add(position)
                else:
                    gap_reads[engine].add(position)
        machine.hook_add(UC_HOOK_CODE, observed)
        machine.hook_add(UC_HOOK_MEM_READ, read, begin=0x020dcb6c, end=0x020dcd2f)
        machines.append(machine)
    rng = random.Random(2026102795)
    cases = calls = protocols = 0
    preset = {name: payload for name, (row, payload) in matches.items()}
    def install(values=None, varied_gap=False):
        nonlocal preset
        preset = dict(values or {name: payload for name, (row, payload) in matches.items()})
        gap = rng.randbytes(3) if varied_gap else arm[0xdcb6d:0xdcb70]
        for engine, machine in enumerate(machines):
            for name, payload in preset.items():
                machine.mem_write(int(matches[name][0]['address'], 0), payload)
            machine.mem_write(0x020dcb6d, gap)
    def seed(current):
        for machine in machines:
            machine.mem_write(BASE, bytes(current))
    def invoke(address, args, expected):
        nonlocal cases, calls
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        states = []
        incoming_flags = (rng.getrandbits(4) << 28) | 0x1f
        caller_values = [rng.getrandbits(32) for register in range(5)]
        for engine, machine in enumerate(machines):
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12), caller_values):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), args):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_CPSR, incoming_flags)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            began = time.monotonic()
            machine.emu_start(address, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 32) != bool(cases & 1):
                raise AssertionError('MD5 typed data bounded return/ABI differs')
            if bytes(machine.mem_read(BASE, 0x8000)) != bytes(expected):
                raise AssertionError(('MD5 typed data independent entire arena differs', hex(address)))
            for name, payload in preset.items():
                if bytes(machine.mem_read(int(matches[name][0]['address'], 0), len(payload))) != payload:
                    raise AssertionError('MD5 consumers wrote the typed algorithm constants/indices/padding')
            states.append(bytes(machine.mem_read(0x027f0000, 0x10000)))
            calls += 1
        if states[0] != states[1]:
            raise AssertionError('MD5 typed data source/native complete stack effects differ')
        cases += 1
    vectors = [(b'', 'd41d8cd98f00b204e9800998ecf8427e'), (b'a', '0cc175b9c0f1b6a831c399e269772661'), (b'abc', '900150983cd24fb0d6963f7d28e17f72'), (b'message digest', 'f96b697d7cb7938d525a2f31aaf161d0'), (b'abcdefghijklmnopqrstuvwxyz', 'c3fcd3d76192e4007dfb496cca67e13b'), (b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', 'd174ab98d277d9f5a5611c2c9f419d9f'), (b'1234567890' * 8, '57edf4a22be3c955ac49da2e2107b67a')]
    vectors.extend((rng.randbytes(length), None) for length in (0, 1, 7, 8, 15, 16, 31, 32, 55, 56, 57, 63, 64, 65, 119, 120, 127, 128, 129, 255, 256, 257, 1024, 4096) for strategy in range(2))
    for number, (data, literal) in enumerate(vectors):
        install(varied_gap=True)
        current = bytearray(rng.randbytes(0x8000))
        current[0x1000:0x1000 + len(data)] = data
        seed(current)
        context = bytearray(current[0x100:0x158])
        struct.pack_into('<4IQ', context, 0, *INITIAL, 0)
        current[0x100:0x158] = context
        invoke(0x0200cad0, (CONTEXT,), current)
        consumed = 0
        while consumed < len(data):
            chunk = min(len(data) - consumed, (1, 7, 63, 64, 65, 129)[(consumed + number) % 6]) if number & 1 else len(data)
            update(context, data[consumed:consumed + chunk])
            current[0x100:0x158] = context
            invoke(0x0200cb10, (CONTEXT, DATA + consumed, chunk), current)
            consumed += chunk
        digest = finish(context)
        if digest != hashlib.md5(data).digest() or literal and digest.hex() != literal:
            raise AssertionError('MD5 typed data independent literal/hashlib result differs')
        current[0x400:0x410] = digest
        current[0x100:0x158] = bytes(88)
        invoke(0x0200cbd8, (OUTPUT, CONTEXT), current)
        protocols += 1
    indices = list(struct.unpack('<48I', matches['saved_md5_indices'][1]))
    constants = list(CONSTANTS)
    mutant_cases = []
    original_context = bytearray(rng.randbytes(88))
    baseline = bytearray(original_context)
    compress_variant(baseline, constants, indices)
    for kind, values in (('constants', constants), ('indices', indices)):
        for index in range(len(values)):
            changed = values.copy()
            changed[index] = changed[index] ^ 1 if kind == 'constants' else (changed[index] + 1) & 15
            variant_constants = changed if kind == 'constants' else constants
            variant_indices = changed if kind == 'indices' else indices
            context = bytearray(original_context)
            compress_variant(context, variant_constants, variant_indices)
            if context == baseline:
                raise AssertionError('MD5 derived data negative control did not change expected state')
            payloads = {name: payload for name, (row, payload) in matches.items()}
            payloads['saved_md5_' + kind] = struct.pack('<' + str(len(changed)) + 'I', *changed)
            install(payloads)
            current = bytearray(rng.randbytes(0x8000))
            current[0x100:0x158] = original_context
            seed(current)
            current[0x100:0x158] = context
            invoke(0x0200cc90, (CONTEXT,), current)
            mutant_cases.append({'object': kind, 'wordIndex': index, 'original': values[index], 'mutated': changed[index], 'independentlyExpectedStateDiffers': True})
    payloads = {name: payload for name, (row, payload) in matches.items()}
    payloads['saved_md5_padding'] = b'\x81'
    install(payloads, True)
    current = bytearray(rng.randbytes(0x8000))
    seed(current)
    context = bytearray(current[0x100:0x158])
    struct.pack_into('<4IQ', context, 0, *INITIAL, 0)
    current[0x100:0x158] = context
    invoke(0x0200cad0, (CONTEXT,), current)
    changed_digest = finish_with_padding(context, 129)
    if changed_digest == hashlib.md5(b'').digest():
        raise AssertionError('MD5 padding negative control was not detected')
    current[0x400:0x410] = changed_digest
    current[0x100:0x158] = bytes(88)
    invoke(0x0200cbd8, (OUTPUT, CONTEXT), current)
    mutant_cases.append({'object': 'padding', 'original': 128, 'mutated': 129, 'independentlyExpectedEmptyMessageDigestDiffers': True})
    if any(values != known_bytes for values in data_reads) or any(not all(values.values()) for values in entries):
        raise AssertionError('MD5 full typed data byte/source entry coverage incomplete')
    return {'cases': cases, 'nativeAndSourceCalls': calls, 'validHashlibAndLiteralProtocols': protocols, 'mutationControls': mutant_cases, 'everySineConstantAndIndexWordMutantDetected': True, 'all449TypedDataBytesReadInBothEngines': True, 'uncreditedNeighborBytesRead': [[hex(position) for position in sorted(values)] for values in gap_reads], 'threeUncreditedAlignmentBytesVariedAcrossProtocolFixtures': protocols, 'instructionLimitPerCall': 1000000, 'secondsLimitPerCall': 2, 'executionOutsideSixRecoveredBodies': 0, 'completeArenaStackReturnsAndCalleeSavedRegistersCompared': True, 'retainedNativeCodeBodies': [], 'retainedNativeAlgorithmDataBytes': 0, 'platformStubs': {}, 'reusedAcceptedSources': [row for row, code in code_rows], 'entryCountsPerEngine': [{hex(address): count for address, count in values.items()} for values in entries], 'limitations': ['Four ordinary C MD5 bodies plus two explicitly verified original SDK assembly helpers execute the compiled typed C data; no other original code or algorithm data is loaded in the source engine.', 'Three alignment bytes remain uncredited and vary across fixtures identically in both engines, allowing complete stack-effect comparison; known hashlib digests do not change. Only the first neighbor byte is read through the target halfword helper and masked away.', 'Mutation controls alter emulator RAM values to demonstrate consumer dependence on all112 words and the padding byte; they do not mutate source objects, ROM/save inputs or claim portable writes to const C objects.', 'This proves deterministic MD5 algorithm data and native placement/use, without cryptographic security, original variable-name/type authenticity or semantic save-byte claims.']}
