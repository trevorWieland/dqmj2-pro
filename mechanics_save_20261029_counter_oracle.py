import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

PAGE = 0x021BD000
STATE = 0x021BD61C
STACK = 0x02500000
STOP = 0x027FF800
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
FUNCTIONS = {0x02063CF4: (0x4C, False), 0x02063D04: (0x4C, True), 0x02063D30: (0x4E, False), 0x02063D40: (0x4E, True), 0x02063D6C: (0x50, False), 0x02063D7C: (0x50, True)}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def value(data, field):
    return struct.unpack_from('<H', data, STATE - PAGE + field)[0]


def model(before, field, increment):
    expected = bytearray(before)
    previous = value(before, field)
    writes = []
    if increment:
        updated = (previous + 1) % 65536
        writes.append([STATE + field, 2, updated])
        if updated > 9999:
            updated = 9999
            writes.append([STATE + field, 2, updated])
        struct.pack_into('<H', expected, STATE - PAGE + field, updated)
    return bytes(expected), previous, writes


def run(bodies, before, stack, entry, registers, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    for address, body in bodies.items():
        machine.mem_write(address, body)
    machine.mem_write(PAGE, before)
    machine.mem_write(STACK, stack)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, content in zip(REGISTERS, registers):
        machine.reg_write(register, content)
    writes, visited = [], set()

    def observe(uc, pc, size, data):
        if not any(address <= pc < address + (36 if FUNCTIONS[address][1] else 12) for address in bodies):
            raise AssertionError(('Counter execution escaped reconstructed bodies', hex(pc)))
        visited.add(pc)

    def observe_write(uc, access, address, size, content, data):
        if not PAGE <= address or address + size > PAGE + len(before):
            raise AssertionError('Counter leaf wrote outside the explicit state page')
        writes.append([address, size, content])

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    machine.emu_start(entry, STOP, count=200)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise AssertionError('Counter leaf did not actually return within its bound')
    field, increment = FUNCTIONS[entry]
    expected, previous, expected_writes = model(before, field, increment)
    arena = bytes(machine.mem_read(PAGE, len(before)))
    actual = [machine.reg_read(register) for register in REGISTERS]
    if arena != expected or writes != expected_writes or not increment and actual[0] != previous:
        raise AssertionError('Independent counter halfword/ordered-write/result model differs')
    actual_stack = bytes(machine.mem_read(STACK, len(stack)))
    if actual_stack != stack or actual[4:12] != registers[4:12] or actual[-2] != registers[-2] or machine.reg_read(UC_ARM_REG_CPSR) & 0xFF != flags & 0xFF:
        raise AssertionError('Counter leaf altered stack/preserved registers/CPU mode')
    return {'registers': actual, 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'arena': arena, 'stack': actual_stack, 'writes': writes, 'visited': sorted(visited)}


def validate(arm, save, matches, root):
    if {int(row['address'], 0) for row, code in matches.values()} != set(FUNCTIONS):
        raise AssertionError('All six exact counter functions are required')
    rebuilt = {int(row['address'], 0): code for row, code in matches.values()}
    native = {address: arm[address - 0x02000000:address - 0x02000000 + len(code)] for address, code in rebuilt.items()}
    rng = random.Random(20261029063180)
    hashes, coverage = [], set()
    counts = {hex(entry): 0 for entry in FUNCTIONS}

    def compare(before, stack, entry):
        registers = [rng.getrandbits(32) for unused in REGISTERS]
        registers[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | (rng.randrange(4) << 6) | 0x10
        original = run(native, before, stack, entry, registers, flags)
        compiled = run(rebuilt, before, stack, entry, registers, flags)
        if original != compiled:
            raise AssertionError('Native/source counter leaf effects differ')
        coverage.update(original['visited'])
        counts[hex(entry)] += 1
        encoded = {**original, 'arena': sha(original['arena']), 'stack': sha(original['stack'])}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
        return original

    boundaries = [0, 1, 2, 9997, 9998, 9999, 10000, 32767, 32768, 65533, 65534, 65535]
    for entry, (field, increment) in FUNCTIONS.items():
        for initial in boundaries + [rng.randrange(65536) for unused in range(128)]:
            before = bytearray(rng.randbytes(4096))
            struct.pack_into('<H', before, STATE - PAGE + field, initial)
            compare(bytes(before), rng.randbytes(0x8000), entry)
    for entry, (field, increment) in FUNCTIONS.items():
        if not increment:
            continue
        for seed in range(16):
            before, stack = bytearray(rng.randbytes(4096)), rng.randbytes(0x8000)
            struct.pack_into('<H', before, STATE - PAGE + field, [0, 9998, 9999, 65534, 65535][seed % 5])
            for unused in range(8):
                result = compare(bytes(before), stack, entry)
                before, stack = bytearray(result['arena']), result['stack']
    expected_pcs = {pc for entry, (field, increment) in FUNCTIONS.items() for pc in range(entry, entry + (36 if increment else 12), 4)}
    if coverage != expected_pcs:
        raise AssertionError('Counter native instruction coverage is incomplete')
    cases = sum(counts.values())
    return {'cases': cases, 'nativeAndRecompiledCalls': cases * 2, 'verifiedReturn': True, 'instructionLimit': 200, 'independentMachineStatePerExecution': True, 'stateSha256': hashes, 'casesByEntry': counts, 'nativeInstructionAddressesVisited': sorted(coverage), 'sourceBodiesExecuted': len(FUNCTIONS), 'retainedNativeCalleeCodeBytes': 0, 'platformProviders': {}, 'observations': ['Getters return the unsigned16-bit words at context offsets4C/4E/50.', 'Increment first stores the16-bit wrapped value, reloads it, and conditionally stores9999 when that reloaded value is larger.', '9998 increments to9999;9999 and10000 finish at9999;FFFF wraps to0000 before clipping and therefore finishes at zero.', 'Exact one-or-two halfword-write chronology, unchanged neighboring bytes, complete state/stack pages and architectural effects satisfy independent/native models.', 'Repeated increments cover ordinary growth, stable clipping and growth after theFFFF-to-zero wrap; every execution actually returns.'], 'limitations': ['Game-facing counter labels, valid gameplay ranges and serialized-save offsets are not established by these RAM fields alone.', 'The isolated proof establishes no persistence timing, atomicity, concurrent-writer behavior, checksum effect or save-bank chronology.', 'Increment has a void interface; architectural register results are compared without assigning a semantic return value.']}
