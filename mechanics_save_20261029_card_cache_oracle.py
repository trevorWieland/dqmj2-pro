import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

ADDRESS = 0x02010B1C
COPY = 0x02008E0C
BACKEND = 0x020E5500
PAGE = 0x020E5000
CACHE_PAGE = 0x02400000
CACHE = CACHE_PAGE + 0x100
DESTINATION = 0x02410000
STACK = 0x02500000
STOP = 0x027FF800
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


def write(data, offset, value):
    struct.pack_into('<I', data, offset, value & 0xFFFFFFFF)


def dependencies(root, arm):
    report = json.loads((root / 'evidence/matches/mechanics-save-sdk-memory-original-asm.json').read_text())
    row = next(row for row in report['matches'] if int(row['address'], 0) == COPY)
    for field in ['source', 'object']:
        if sha((root / row[field]).read_bytes()) != row[field + 'Sha256']:
            raise AssertionError('Accepted original SDK copy source/object identity changed')
    proof = validate_link(row, {}, root / 'work/mechanics-save/20261029-cache-copy/dependencies' / row['objectSha256'])
    linked = row | freeze_link(proof)
    code = (root / linked['isolatedCallerBinary']).read_bytes()
    if code != arm[COPY - 0x02000000:COPY - 0x02000000 + 304]:
        raise AssertionError('Existing copy differs after actual MW relink')
    return linked, code


def model(arena, cache, destination):
    expected, output = bytearray(arena), bytearray(destination)
    source = read(arena, BACKEND - PAGE + 0x1C)
    pointer = read(arena, BACKEND - PAGE + 0x20)
    length = read(arena, BACKEND - PAGE + 0x24)
    base = source & 0xFFFFFE00
    arguments = []
    if base == read(cache, CACHE - CACHE_PAGE + 8):
        offset = source - base
        count = min(512 - offset, length)
        arguments = [CACHE + 32 + offset, pointer, count]
        output[pointer - DESTINATION:pointer - DESTINATION + count] = cache[CACHE - CACHE_PAGE + 32 + offset:CACHE - CACHE_PAGE + 32 + offset + count]
        for field, value in [(0x1C, source + count), (0x20, pointer + count), (0x24, length - count)]:
            write(expected, BACKEND - PAGE + field, value)
        length -= count
    return bytes(expected), bytes(output), int(length != 0), arguments


def run(bodies, arena, cache, destination, stack, registers, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    for address, code in bodies.items():
        machine.mem_write(address, code)
    for address, data in [(PAGE, arena), (CACHE_PAGE, cache), (DESTINATION, destination), (STACK, stack)]:
        machine.mem_write(address, data)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(REGISTERS, registers):
        machine.reg_write(register, value)
    expected_arena, expected_destination, result, arguments = model(arena, cache, destination)
    visits, writes, calls = set(), [], []

    def observe(uc, pc, size, data):
        if not any(start <= pc < start + length for start, length in [(ADDRESS, 136), (COPY, 304)]):
            raise AssertionError(('Cache-copy execution escaped declared recovered bodies', hex(pc)))
        visits.add(pc)
        if pc == COPY:
            actual = [uc.reg_read(register) for register in REGISTERS[:3]]
            if not arguments or actual != arguments or calls:
                raise AssertionError('Actual accepted copy invocation arguments/count differ')
            calls.append(actual)

    def observe_write(uc, access, address, size, value, data):
        if not any(start <= address and address + size <= start + length for start, length in [(PAGE, len(arena)), (DESTINATION, len(destination)), (STACK, len(stack))]):
            raise AssertionError(('Cache-copy wrote outside explicit writable windows', hex(address), size))
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    machine.emu_start(ADDRESS, STOP, count=4000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise AssertionError('Cache-copy did not actually return within its instruction bound')
    actual_registers = [machine.reg_read(register) for register in REGISTERS]
    actual_arena = bytes(machine.mem_read(PAGE, len(arena)))
    actual_destination = bytes(machine.mem_read(DESTINATION, len(destination)))
    if actual_arena != expected_arena or actual_destination != expected_destination or bytes(machine.mem_read(CACHE_PAGE, len(cache))) != cache or len(calls) != bool(arguments):
        raise AssertionError('Independent cache-copy memory/call model differs')
    if actual_registers[0] != result or actual_registers[4:12] != registers[4:12] or actual_registers[-2] != registers[-2]:
        raise AssertionError('Cache-copy boolean/preserved registers/SP differ')
    return {'registers': actual_registers, 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'arena': actual_arena, 'destination': actual_destination, 'stack': bytes(machine.mem_read(STACK, len(stack))), 'writes': writes, 'calls': calls, 'visited': sorted(visits)}


def validate(arm, save, matches, root):
    if set(matches) != {'saved_20261029_card_cache_copy'}:
        raise AssertionError('Complete cache-copy source is required')
    dependency = dependencies(root, arm)
    rows = [*matches.values(), dependency]
    rebuilt = {int(row['address'], 0): code for row, code in rows}
    native = {address: arm[address - 0x02000000:address - 0x02000000 + len(code)] for address, code in rebuilt.items()}
    rng = random.Random(20261029011028)
    hashes, coverage = [], set()
    cases, copy_calls = 0, 0

    def compare(arena, cache, destination, stack):
        nonlocal cases, copy_calls
        registers = [rng.getrandbits(32) for unused in REGISTERS]
        registers[0] = CACHE
        registers[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | 0x10
        original = run(native, arena, cache, destination, stack, registers, flags)
        compiled = run(rebuilt, arena, cache, destination, stack, registers, flags)
        if original != compiled:
            raise AssertionError('Native/source cache-copy machine effects differ')
        cases += 1
        copy_calls += len(original['calls'])
        coverage.update(original['visited'])
        encoded = {**original, **{name: sha(original[name]) for name in ['arena', 'destination', 'stack']}}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
        return original

    def fixture(offset, length, alignment, base, hit=True):
        arena, cache = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
        for field, value in [(0x1C, base + offset), (0x20, DESTINATION + 0x100 + alignment), (0x24, length)]:
            write(arena, BACKEND - PAGE + field, value)
        write(cache, CACHE - CACHE_PAGE + 8, base if hit else base ^ 512)
        return bytes(arena), bytes(cache), rng.randbytes(4096), rng.randbytes(0x8000)

    for offset in range(512):
        for index, length in enumerate([0, 1, 512 - offset, 513 - offset]):
            compare(*fixture(offset, length, (offset + index) % 4, [0, 0x02000000, 0x7FFFFE00, 0xFFFFFE00][offset % 4]))
    for offset in [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 255, 256, 508, 509, 510, 511]:
        for length in [0, 1, 2, 3, 7, 16, 31, 32, 255, 512, 513, 0xFFFFFFFF]:
            for alignment in range(4):
                compare(*fixture(offset, length, alignment, 0x10000000))
    for index in range(128):
        compare(*fixture(rng.randrange(512), [0, 32, 0xFFFFFFFF][index % 3], index % 4, 0xFFFFFE00, False))
    for seed in range(32):
        arena, cache, destination, stack = fixture(seed * 17 % 512, 1541, seed % 4, 0x02000000)
        for unused in range(5):
            next_cache = bytearray(cache)
            write(next_cache, CACHE - CACHE_PAGE + 8, read(arena, BACKEND - PAGE + 0x1C) & 0xFFFFFE00)
            cache = bytes(next_cache)
            result = compare(arena, cache, destination, stack)
            arena, destination, stack = result['arena'], result['destination'], result['stack']
        if read(arena, BACKEND - PAGE + 0x24):
            raise AssertionError('Repeated cache-copy sequence did not consume its complete supported request')
    pcs = sorted(pc for pc in coverage if ADDRESS <= pc < ADDRESS + 136)
    if pcs != list(range(ADDRESS, ADDRESS + 136, 4)):
        raise AssertionError('Cache-copy caller instruction coverage is incomplete')
    return {'cases': cases, 'nativeAndRecompiledCalls': cases * 2, 'verifiedReturn': True, 'instructionLimit': 4000, 'independentMachineStatePerExecution': True, 'stateSha256': hashes, 'nativeInstructionAddressesVisited': pcs, 'actualAcceptedCopyInvocations': copy_calls, 'reusedAcceptedSources': [dependency[0]], 'sourceBodiesExecuted': 2, 'retainedNativeCalleeCodeBytes': 0, 'platformProviders': {}, 'observations': ['All512 source offsets within a cache block, destination alignment residues, zero/partial/full/remainder counts and mismatched tags are exercised.', 'Matching tags copy the smaller of bytes left in the512-byte block and requested count, then update the measured three words and return whether data remains.', 'The separately relinked accepted304-byte SDK copy body actually executes; no synthetic copy/hardware provider is involved.', 'Full32-bit logical-offset/remaining-count boundaries include wrap to zero; memory destinations remain within disposable mapped RAM.', 'Repeated calls over successive declared cache tags consume a1541-byte request and preserve earlier copied data.'], 'limitations': ['This isolated RAM proof does not establish card transfer, cache population, cache coherence, interrupt behavior or concurrent source-offset mutation.', 'The reused verified-original SDK assembly is existing accepted source with zero additional recovered-source credit.']}
