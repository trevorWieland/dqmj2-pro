import hashlib
import random
import match_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_CPU_ARM_946

STACK, RETURN, DATA, DATA_SIZE = 0x023E0000, 0x023FF000, 0x027FC000, 0x6000
PATTERNS = (0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x12345678)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def execute(entry, body, index, seed, flags, count=64):
    address = int(entry['address'], 0)
    target = ((index * 4 & 0xFFFFFFFF) + entry['dataBase'] + entry['dataWordIndex'] * 4) & 0xFFFFFFFF
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for first, size in ((address & ~0xFFF, 0x1000), (STACK, 0x1000), (RETURN, 0x1000), (DATA, DATA_SIZE)):
        machine.mem_map(first, size)
    rng = random.Random(20261030 + seed)
    machine.mem_write(address, body)
    stack, data = rng.randbytes(0x1000), bytearray(rng.randbytes(DATA_SIZE))
    value = PATTERNS[(index + seed) % len(PATTERNS)]
    if DATA <= target < DATA + DATA_SIZE:
        data[target - DATA:target - DATA + 4] = value.to_bytes(4, 'little')
    machine.mem_write(STACK, stack)
    machine.mem_write(DATA, bytes(data))
    registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    registers[0] = index
    registers[-2:] = [STACK + 0xFF0, RETURN]
    before = list(registers)
    initial_flags = flags << 28 | 0xD3
    machine.reg_write(UC_ARM_REG_CPSR, initial_flags)
    for register, word in zip(match_runtime.REGISTERS, registers):
        machine.reg_write(register, word)
    visited, reads = [], []
    def code(cpu, pc, size, unused):
        if not address <= pc < address + entry['bytes']:
            raise ValueError('Indexed-load execution left complete body')
        visited.append(pc)
    def read(cpu, access, location, size, word, unused):
        reads.append([location, size])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_READ, read)
    fault = None
    try:
        machine.emu_start(address, RETURN, count=count, timeout=100000)
    except UcError as error:
        fault = error.errno
    returned = machine.reg_read(UC_ARM_REG_PC) == RETURN
    registers = [machine.reg_read(register) for register in match_runtime.REGISTERS]
    if returned:
        before[0] = value
        if registers != before or reads != [[target, 4]] or machine.reg_read(UC_ARM_REG_CPSR) != initial_flags:
            raise ValueError('Independent wrapping address/full-word/read/register model differs')
        if bytes(machine.mem_read(STACK, 0x1000)) != stack or bytes(machine.mem_read(DATA, DATA_SIZE)) != bytes(data):
            raise ValueError('Indexed read modified synthetic mapped state')
    return {'actualReturn': returned, 'fault': fault, 'pc': machine.reg_read(UC_ARM_REG_PC), 'registers': registers,
        'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'reads': reads, 'visited': visited,
        'stackSha256': digest(bytes(machine.mem_read(STACK, 0x1000))), 'dataSha256': digest(bytes(machine.mem_read(DATA, DATA_SIZE))),
        'codeSha256': digest(bytes(machine.mem_read(address & ~0xFFF, 0x1000))), 'returnMapSha256': digest(bytes(machine.mem_read(RETURN, 0x1000)))}


def oracle(entry, original, rebuilt):
    vectors = [(index, index % 8, index % 16) for index in range(256)]
    edges = (0, 1, 0x100, 0x3FF, 0x400, 0xFFFFFC00, 0xFFFFFF00, 0xFFFFFFFE, 0xFFFFFFFF, 0x40000000, 0x80000000, 0xC0000000)
    vectors += [(index, flag % 8, flag) for index in edges for flag in range(16)]
    records, visited = [], set()
    for index, seed, flags in vectors:
        expected, actual = execute(entry, original, index, seed, flags), execute(entry, rebuilt, index, seed, flags)
        if expected != actual or not expected['actualReturn'] or expected['fault'] is not None:
            raise ValueError('Native/source indexed-load result or complete state differs')
        visited.update(expected['visited'])
        records.append({'index': index, 'seed': seed, 'flags': flags, 'actualOriginalAndCompiledReturns': 2,
            'readAddress': expected['reads'][0][0], 'resultWord': expected['registers'][0], 'stateSha256': digest(repr(expected).encode())})
    if visited != set(range(int(entry['address'], 0), int(entry['address'], 0) + entry['bytes'], 4)):
        raise ValueError('Some own indexed-load instruction was not executed')
    controls = []
    for name, index, count in (('instruction-budget', 0, 4), ('unmapped-read', 0x20000000, 64)):
        expected, actual = execute(entry, original, index, 0, 15, count), execute(entry, rebuilt, index, 0, 15, count)
        if expected != actual or expected['actualReturn'] or (name == 'unmapped-read' and expected['fault'] is None):
            raise ValueError('Unsupported indexed-load path received return credit')
        controls.append({'name': name, 'index': index, 'instructionLimit': count, 'returnCredit': 0, 'state': expected})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'freshMachinePerExecution': True, 'instructionLimit': 64, 'timeoutMicroseconds': 100000,
        'independentUnsignedAddressFullWordAndPreservedStateModel': True, 'allOwnInstructionAddressesVisited': sorted(visited),
        'records': records, 'unsupportedControls': controls, 'unsupportedReturnCredit': 0,
        'externalMemoryContract': {'base': DATA, 'size': DATA_SIZE, 'syntheticDisposableBytes': True, 'originalDataSourceCredit': 0,
            'limitations': ['Mapping is a bounded synthetic memory oracle, not proof of physical hardware aliases, original object extent or valid caller indices',
                'Only the tested mapped index domain returns; the full index domain can fault; fixed 32-bit address arithmetic needs an address abstraction for Android']}}
