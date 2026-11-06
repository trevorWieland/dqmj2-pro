import hashlib
import random
import match_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_CPU_ARM_946

STACK, RETURN, DATA, SIZE = 0x023E0000, 0x023FF000, 0x02400000, 0x3000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def execute(entry, body, destination, source, count, seed, flags, budget=4096):
    address = int(entry['address'], 0)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for first, length in ((address & ~0xFFF, 0x1000), (STACK, 0x1000), (RETURN, 0x1000), (DATA, SIZE)):
        machine.mem_map(first, length)
    rng = random.Random(20261030 + seed)
    data, stack = rng.randbytes(SIZE), rng.randbytes(0x1000)
    machine.mem_write(address, body)
    machine.mem_write(DATA, data)
    machine.mem_write(STACK, stack)
    registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    registers[:3] = [destination, source, count]
    registers[-2:] = [STACK + 0xFF0, RETURN]
    before = list(registers)
    initial_flags = flags << 28 | 0xD3
    machine.reg_write(UC_ARM_REG_CPSR, initial_flags)
    for register, value in zip(match_runtime.REGISTERS, registers):
        machine.reg_write(register, value)
    reads, writes, visited = [], [], []
    def code(cpu, pc, length, unused):
        if not address <= pc < address + entry['bytes']:
            raise ValueError('Overlap copy escaped complete own source body')
        visited.append(pc)
    def read(cpu, access, location, length, value, unused):
        reads.append([location, length])
    def write(cpu, access, location, length, value, unused):
        writes.append([location, length, value & ((1 << (length * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_READ, read)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    fault = None
    try:
        machine.emu_start(address, RETURN, count=budget, timeout=100000)
    except UcError as error:
        fault = error.errno
    returned = machine.reg_read(UC_ARM_REG_PC) == RETURN
    registers = [machine.reg_read(register) for register in match_runtime.REGISTERS]
    current_data = bytes(machine.mem_read(DATA, SIZE))
    if returned:
        order = range(count) if source >= destination else range(count - 1, -1, -1)
        expected_reads = [[source + index, 1] for index in order]
        expected_writes = [[destination + index, 1, data[source - DATA + index]] for index in order]
        expected_data = bytearray(data)
        expected_data[destination - DATA:destination - DATA + count] = data[source - DATA:source - DATA + count]
        if reads != expected_reads or writes != expected_writes or current_data != bytes(expected_data):
            raise ValueError('Independent overlap-safe snapshot/ordered-byte-effects model differs')
        if registers[0] != destination or registers[4:12] != before[4:12] or registers[-2:] != before[-2:]:
            raise ValueError('Copy pointer return or callee-saved ABI differs')
        if bytes(machine.mem_read(STACK, 0x1000)) != stack:
            raise ValueError('Copy unexpectedly modified caller stack')
    return {'actualReturn': returned, 'fault': fault, 'pc': machine.reg_read(UC_ARM_REG_PC), 'registers': registers,
        'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'reads': reads, 'writes': writes, 'visited': visited,
        'dataSha256': digest(current_data), 'stackSha256': digest(bytes(machine.mem_read(STACK, 0x1000))),
        'codeSha256': digest(bytes(machine.mem_read(address & ~0xFFF, 0x1000))), 'returnMapSha256': digest(bytes(machine.mem_read(RETURN, 0x1000)))}


def cases():
    result = []
    for count in range(129):
        for displacement in (-33, -1, 0, 1, 33):
            source = DATA + 0x800 + count % 4
            result.append((source + displacement, source, count, count % 8, (count + displacement) % 16))
    for count in (1, 3, 7, 15, 63, 127, 128, 255):
        for flags in range(16):
            result.append((DATA + SIZE - count, DATA, count, flags % 8, flags))
            result.append((DATA, DATA + SIZE - count, count, flags % 8, flags))
    return result


def oracle(entry, original, rebuilt):
    records, visited, covered_values = [], set(), set()
    for destination, source, count, seed, flags in cases():
        expected = execute(entry, original, destination, source, count, seed, flags)
        actual = execute(entry, rebuilt, destination, source, count, seed, flags)
        if expected != actual or not expected['actualReturn'] or expected['fault'] is not None:
            raise ValueError('Native/source full copy ABI/state/return differs')
        visited.update(expected['visited'])
        covered_values.update(write[2] for write in expected['writes'])
        records.append({'destination': destination, 'source': source, 'count': count, 'seed': seed, 'flags': flags,
            'direction': 'forward' if source >= destination else 'backward', 'actualOriginalAndCompiledReturns': 2,
            'writes': len(expected['writes']), 'stateSha256': digest(repr(expected).encode())})
    if visited != set(range(int(entry['address'], 0), int(entry['address'], 0) + entry['bytes'], 4)) or len(covered_values) != 256:
        raise ValueError('Copy own instruction or byte-value coverage incomplete')
    controls = []
    for name, destination, source, count, budget in (
            ('instruction-budget', DATA + 0x800, DATA + 0x100, 256, 128),
            ('unmapped-source', DATA + 0x100, 0x03000000, 1, 4096),
            ('unmapped-destination', 0x03000000, DATA + 0x100, 1, 4096)):
        expected = execute(entry, original, destination, source, count, 0, 15, budget)
        actual = execute(entry, rebuilt, destination, source, count, 0, 15, budget)
        if expected != actual or expected['actualReturn'] or ('unmapped' in name and expected['fault'] is None):
            raise ValueError('Unsupported copy path received return credit')
        controls.append({'name': name, 'returnCredit': 0, 'state': expected})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'freshMachinePerExecution': True, 'instructionLimit': 4096, 'timeoutMicroseconds': 100000,
        'independentSnapshotOrderedReadWriteAndPointerReturnModel': True, 'allOwnInstructionAddressesVisited': sorted(visited),
        'copiedByteValueCoverage': sorted(covered_values), 'records': records, 'unsupportedControls': controls, 'unsupportedReturnCredit': 0,
        'limitations': ['Synthetic mapped byte spans/counts0..128 and selected255-byte endpoints; no physical ownership/caller-validity guarantee',
            'Invalid pointers fault and budget exhaustion does not return an error result',
            'The source compares 32-bit target pointer values; an Android port must use its platform pointer/address model']}
