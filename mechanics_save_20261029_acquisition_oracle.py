import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

PAGE = 0x021C0000
PRIMARY = 0x021C0E20
LIBRARY = 0x021C0EE0
STACK = 0x02500000
STOP = 0x027FF800
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
FUNCTIONS = {'primary-get': (0x02063B40, 32), 'primary-set': (0x02063B60, 92), 'library-get': (0x02063BBC, 32), 'aux-get': (0x02063BDC, 36), 'library-set': (0x02063C00, 148), 'aux-set': (0x02063C94, 96)}
NAMES = {address: name for name, (address, size) in FUNCTIONS.items()}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bit(data, base, index):
    word = struct.unpack_from('<I', data, base - PAGE + (index // 32) * 4)[0]
    return (word >> (index % 32)) & 1


def change(data, base, index, value, writes):
    address = base + (index // 32) * 4
    current = struct.unpack_from('<I', data, address - PAGE)[0]
    mask = 1 << (index % 32)
    updated = current | mask if value else current & ~mask
    struct.pack_into('<I', data, address - PAGE, updated)
    writes.append([address, 4, updated])


def model(before, entry, index, value):
    expected = bytearray(before)
    events, writes = [entry], []
    if entry in ['primary-get', 'primary-set']:
        previous = bit(expected, PRIMARY, index)
        if entry == 'primary-set':
            events.append('primary-get')
            change(expected, PRIMARY, index, value, writes)
    elif entry in ['library-get', 'library-set']:
        previous = bit(expected, LIBRARY, index)
        if entry == 'library-set':
            events.append('library-get')
            change(expected, LIBRARY, index, value, writes)
            if value and not previous:
                events += ['aux-set', 'aux-get', 'primary-set', 'primary-get']
                change(expected, LIBRARY, index + 64, value, writes)
                change(expected, PRIMARY, 76, 1, writes)
    else:
        previous = bit(expected, LIBRARY, index + 64)
        if entry == 'aux-set':
            events.append('aux-get')
            change(expected, LIBRARY, index + 64, value, writes)
    return bytes(expected), previous, events, writes


def run(bodies, before, stack, entry, index, value, registers, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    for address, body in bodies.items():
        machine.mem_write(address, body)
    machine.mem_write(PAGE, before)
    machine.mem_write(STACK, stack)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, content in zip(REGISTERS, registers):
        machine.reg_write(register, content)
    events, writes, state_writes, visited = [], [], [], set()

    def observe(uc, pc, size, data):
        if not any(address <= pc < address + len(body) - 4 for address, body in bodies.items()):
            raise AssertionError(('Flag transition escaped recovered source bodies', hex(pc)))
        visited.add(pc)
        if pc in NAMES:
            events.append(NAMES[pc])

    def observe_write(uc, access, address, size, content, data):
        if not any(start <= address and address + size <= start + length for start, length in [(PAGE, len(before)), (STACK, len(stack))]):
            raise AssertionError(('Flag transition wrote outside explicit state windows', hex(address), size))
        writes.append([address, size, content])
        if PAGE <= address < PAGE + len(before):
            state_writes.append([address, size, content])

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    machine.emu_start(FUNCTIONS[entry][0], STOP, count=2000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise AssertionError('Flag transition did not actually return within its bound')
    actual = [machine.reg_read(register) for register in REGISTERS]
    arena = bytes(machine.mem_read(PAGE, len(before)))
    expected, previous, plan, expected_writes = model(before, entry, index, value)
    if arena != expected or actual[0] != previous or events != plan or state_writes != expected_writes:
        raise AssertionError(('Independent flag bit/result/call/write model differs', entry, index, value, events, plan))
    if actual[4:12] != registers[4:12] or actual[-2] != registers[-2] or machine.reg_read(UC_ARM_REG_CPSR) & 0xFF != flags & 0xFF:
        raise AssertionError('Flag transition preserved registers/SP/CPU mode differ')
    return {'registers': actual, 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'arena': arena, 'stack': bytes(machine.mem_read(STACK, len(stack))), 'events': events, 'writes': writes, 'visited': sorted(visited)}


def validate(arm, save, matches, root):
    rows = [row for row, code in matches.values()]
    if {int(row['address'], 0) for row in rows} != set(NAMES):
        raise AssertionError('All six exact flag-transition sources are required')
    rebuilt = {int(row['address'], 0): code for row, code in matches.values()}
    native = {address: arm[address - 0x02000000:address - 0x02000000 + len(body)] for address, body in rebuilt.items()}
    rng = random.Random(20261029063436)
    hashes, coverage, counts = [], set(), {name: 0 for name in FUNCTIONS}

    def compare(before, stack, entry, index, value):
        registers = [rng.getrandbits(32) for unused in REGISTERS]
        registers[:2] = [index, value]
        registers[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | (rng.randrange(4) << 6) | 0x10
        original = run(native, before, stack, entry, index, value, registers, flags)
        compiled = run(rebuilt, before, stack, entry, index, value, registers, flags)
        if original != compiled:
            raise AssertionError('Native/source flag transition architectural effects differ')
        coverage.update(original['visited'])
        counts[entry] += 1
        encoded = {**original, 'arena': sha(original['arena']), 'stack': sha(original['stack'])}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
        return original

    indices = [*range(64), 64, 65, 95, 96, 127, 128, 255]
    for entry in FUNCTIONS:
        values = [0, 1, 2, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF] if entry.endswith('-set') else [0]
        base = PRIMARY if entry.startswith('primary') else LIBRARY
        for index in indices:
            physical_index = index + 64 if entry.startswith('aux') else index
            for value in values:
                for previous in [0, 1]:
                    before = bytearray(rng.randbytes(4096))
                    change(before, base, physical_index, previous, [])
                    compare(bytes(before), rng.randbytes(0x8000), entry, index, value)
    for index in range(64):
        before = bytearray(rng.randbytes(4096))
        for base, physical_index in [(LIBRARY, index), (LIBRARY, index + 64), (PRIMARY, 76)]:
            change(before, base, physical_index, 0, [])
        arena, stack = bytes(before), rng.randbytes(0x8000)
        for value in [1, 1, 0, 0, 2, 0xFFFFFFFF]:
            result = compare(arena, stack, 'library-set', index, value)
            arena, stack = result['arena'], result['stack']
    for index in range(64):
        before, stack = rng.randbytes(4096), rng.randbytes(0x8000)
        first = compare(before, stack, 'aux-get', index, 0)
        second = compare(before, stack, 'library-get', index + 64, 0)
        if first['registers'][0] != second['registers'][0]:
            raise AssertionError('Auxiliary/base offset64 alias observation differs')
    expected_pcs = {address for start, size in FUNCTIONS.values() for address in range(start, start + size - 4, 4)}
    if coverage != expected_pcs:
        raise AssertionError('Flag transition instruction coverage is incomplete')
    cases = sum(counts.values())
    return {'cases': cases, 'nativeAndRecompiledCalls': cases * 2, 'verifiedReturn': True, 'instructionLimit': 2000, 'independentMachineStatePerExecution': True, 'casesByEntry': counts, 'stateSha256': hashes, 'nativeInstructionAddressesVisited': sorted(coverage), 'sourceBodiesExecuted': len(rows), 'retainedNativeCalleeCodeBytes': 0, 'platformProviders': {}, 'observations': ['Every getter returns the measured selected bit; every setter returns its prior bit even for noncanonical nonzero32-bit input values.', 'Setting a previously clear library bit also sets its offset64 auxiliary bit and primary bit76, through the actual reconstructed callees.', 'Clearing the current library bit leaves its auxiliary bit and primary bit76 unchanged.', 'Repeated0-to-nonzero transitions invoke the coupled callees again even if the auxiliary bit was already set; this is not proof of a once-ever event.', 'Auxiliary getter indexi aliases the base getter at indexi+64 for the tested nonnegative index range.', 'All six functions, nested call order, exact state-word write order, prior-bit result, full arena, stack and architectural effects are checked.'], 'limitations': ['Primary/library/auxiliary are address-based labels; game-facing meaning and valid native ID limits are not established by these isolated bit effects.', 'Negative indices, signed index overflow and backing-object bounds beyond the disposable tested region are unsupported.', 'No save-bank checksum, serialization ordering, persistence timing or concurrent writer behavior is established.', 'The observed offset64 relation is not an inferred physical save-bank selector.']}
