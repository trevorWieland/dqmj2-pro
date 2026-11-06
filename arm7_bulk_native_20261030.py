import hashlib
import itertools
import random
import struct
import match_lowlevel
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

RAM, SIZE, STACK, RETURN = 0x02200000, 0x10000, 0x023E0000, 0x023FF000
HEADER, A, B, C = RAM + 0x1000, RAM + 0x2000, RAM + 0x2100, RAM + 0x2200


def digest(data):
    return hashlib.sha256(data).hexdigest()


def profiles(address):
    if address in (0x037FC994, 0x037FCA24):
        values = [{'head': head, 'next': following, 'tail': tail} for head, following, tail in itertools.product((0, A, HEADER), (0, B, A), (0, C))]
    elif address == 0x037FD6C4:
        values = [{'node': A, 'next': following, 'previousSlot': previous} for following, previous in itertools.product((0, B, A), (0, C, A))]
    elif address == 0x037FCD90:
        values = [{'node': A, 'next': following, 'previous': previous} for following, previous in itertools.product((0, B, A), (0, C, A))]
    elif address == 0x037FCDB4:
        values = [{'node': node, 'tail': tail} for node, tail in itertools.product((A, HEADER), (0, B, A))]
    elif address == 0x037FD6EC:
        values = [{'node': node, 'previousSlot': previous} for node, previous in itertools.product((A, HEADER), (0, C, A))]
    elif address == 0x037FF988:
        values = [{'pointer': pointer} for pointer in (0, HEADER, A, RAM + SIZE - 0x50)]
    else:
        raise ValueError('Unknown independently modelled ARM7 C family')
    return [dict(value, seed=seed) for value in values for seed in range(8)]


def initial(address, profile):
    rng = random.Random(20261030 + profile['seed'])
    data = bytearray(rng.randbytes(SIZE))
    def write(location, value):
        struct.pack_into('<I', data, location - RAM, value)
    if address in (0x037FC994, 0x037FCA24):
        write(HEADER, profile['head'])
        write(HEADER + 4, profile['tail'])
        if profile['head']:
            write(profile['head'] + (0x10 if address == 0x037FC994 else 0x64), profile['next'])
        args = [HEADER, rng.getrandbits(32)]
    elif address == 0x037FD6C4:
        write(A, profile['next'])
        write(A + 4, profile['previousSlot'])
        args = [rng.getrandbits(32), A]
    elif address == 0x037FCD90:
        write(A + 0x10, profile['next'])
        write(A + 0x14, profile['previous'])
        args = [HEADER, A]
    elif address == 0x037FCDB4:
        write(HEADER + 0x70, profile['tail'])
        args = [HEADER, profile['node']]
    elif address == 0x037FD6EC:
        args = [profile['previousSlot'], profile['node']]
    else:
        args = [profile['pointer'], rng.getrandbits(32)]
    return bytes(data), args


def expected(address, before, args):
    data, writes = bytearray(before), []
    def read(location):
        return struct.unpack_from('<I', data, location - RAM)[0]
    def write(location, value):
        struct.pack_into('<I', data, location - RAM, value)
        writes.append([location, 4, value])
    header, node = args
    if address in (0x037FC994, 0x037FCA24):
        result = read(header)
        if result:
            following = read(result + (0x10 if address == 0x037FC994 else 0x64))
            write(header, following)
            write(following + (0x14 if address == 0x037FC994 else 0x60) if following else header + 4, 0)
            if address == 0x037FCA24 and not following:
                write(result + 0x5C, 0)
    elif address == 0x037FD6C4:
        previous = read(node + 4)
        if previous:
            write(previous, read(node))
        following = read(node)
        if following:
            write(following + 4, read(node + 4))
            result = header
        else:
            result = read(node + 4)
    elif address == 0x037FCD90:
        following, previous = read(node + 0x10), read(node + 0x14)
        write(following + 0x14 if following else header + 0x70, previous)
        write(previous + 0x10 if previous else header + 0x6C, following)
        result = header
    elif address == 0x037FCDB4:
        tail = read(header + 0x70)
        write(tail + 0x10 if tail else header + 0x6C, node)
        write(node + 0x14, tail)
        write(node + 0x10, 0)
        write(header + 0x70, node)
        result = header
    elif address == 0x037FD6EC:
        write(node + 4, header)
        write(node, 0)
        if header:
            write(header, node)
        result = node
    else:
        if header:
            write(header + 0x48, 0)
            write(header + 0x4C, 0)
        result = header
    return bytes(data), writes, result


def execute(address, body, profile, instruction_limit=256, malformed=False, mode='arm'):
    before, args = initial(address, profile)
    u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    base, end = address & ~0xFFF, (address + len(body) + 0xFFF) & ~0xFFF
    for location, length in ((base, end - base), (RAM, SIZE), (STACK, 0x10000), (RETURN, 0x1000)):
        u.mem_map(location, length)
    u.mem_write(address, body)
    u.mem_write(RAM, before)
    rng = random.Random(20261030 + profile['seed'])
    u.mem_write(STACK, rng.randbytes(0x10000))
    stack_before = bytes(u.mem_read(STACK, 0x10000))
    initial_registers = [rng.getrandbits(32) for register in match_lowlevel.REGISTERS]
    initial_registers[:2] = args
    if malformed:
        initial_registers[0 if address in (0x037FC994, 0x037FCA24, 0x037FF988) else 1] = 0x01000000
    initial_registers[-2:] = [STACK + 0xFFF0, RETURN]
    u.reg_write(UC_ARM_REG_CPSR, ((profile['seed'] & 15) << 28) | 0xD3 | (0x20 if mode == 'thumb' else 0))
    for register, value in zip(match_lowlevel.REGISTERS, initial_registers):
        u.reg_write(register, value)
    visited, stores = [], []
    def code(machine, pc, size, unused):
        if pc == RETURN:
            return
        if not address <= pc < address + len(body):
            raise ValueError('Execution escaped the source-defined ARM7 body')
        visited.append(pc)
    u.hook_add(UC_HOOK_CODE, code)
    u.hook_add(UC_HOOK_MEM_WRITE, lambda machine, access, location, size, value, unused: stores.append([location, size, value]))
    fault = None
    try:
        u.emu_start(address | int(mode == 'thumb'), RETURN, count=instruction_limit, timeout=100000)
    except UcError as error:
        fault = error.errno
    pc = u.reg_read(UC_ARM_REG_PC)
    after = bytes(u.mem_read(RAM, SIZE))
    registers = [u.reg_read(register) for register in match_lowlevel.REGISTERS]
    returned = fault is None and pc == RETURN
    if returned and not malformed:
        expected_ram, expected_writes, expected_return = expected(address, before, args)
        if after != expected_ram or stores != expected_writes or registers[0] != expected_return:
            raise ValueError('Original independent ARM7 field/return/write-order model differs')
        if any(registers[index] != initial_registers[index] for index in range(4, 14)):
            raise ValueError('ARM7 call corrupted a callee-saved register or SP')
        if bytes(u.mem_read(STACK, 0x10000)) != stack_before:
            raise ValueError('Leaf ARM7 routine changed its guarded stack')
    return {'actualReturn': returned, 'fault': fault, 'pc': pc, 'registers': registers, 'cpsr': u.reg_read(UC_ARM_REG_CPSR),
        'ramSha256': digest(after), 'stackSha256': digest(bytes(u.mem_read(STACK, 0x10000))), 'codeMapSha256': digest(bytes(u.mem_read(base, end - base))),
        'returnMapSha256': digest(bytes(u.mem_read(RETURN, 0x1000))), 'orderedWrites': stores, 'visited': visited,
        'independentFieldModelPassed': returned and not malformed, 'providerCalls': 0, 'instructionLimit': instruction_limit}


def verify(address, native, rebuilt, mode='arm'):
    records, visited = [], set()
    for profile in profiles(address):
        original, source = execute(address, native, profile, mode=mode), execute(address, rebuilt, profile, mode=mode)
        if original != source or not original['actualReturn']:
            raise ValueError('Fresh isolated original and source-built ARM7 states/returns differ')
        visited.update(original['visited'])
        records.append({'profile': profile, 'actualOriginalAndRecompiledReturns': 2, 'stateSha256': digest(repr(original).encode()),
            'returnWord': original['registers'][0], 'orderedWrites': original['orderedWrites'], 'modelPassed': True})
    sample = profiles(address)[0]
    exhausted = execute(address, native, sample, instruction_limit=1, mode=mode)
    invalid_native, invalid_source = execute(address, native, sample, malformed=True, mode=mode), execute(address, rebuilt, sample, malformed=True, mode=mode)
    if exhausted['actualReturn'] or invalid_native['actualReturn'] or invalid_source['actualReturn'] or invalid_native != invalid_source:
        raise ValueError('ARM7 count-exhaustion or invalid-pointer negative control falsely returned')
    return {'vectors': len(records), 'actualOriginalAndRecompiledReturns': 2 * len(records), 'allFullStateAndOrderedWritesEqual': True,
        'independentFieldModelPassed': True, 'freshMachinePerExecution': True, 'boundedLeafNoProviders': True, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate, not hardware',
        'instructionLimit': 256, 'timeoutMicroseconds': 100000, 'malformedAndExhaustedReturnCredit': 0,
        'negativeControls': {'countExhausted': exhausted, 'invalidPointer': invalid_native}, 'records': records,
        'visitedAddresses': sorted(visited), 'unvisitedInstructionAddresses': [pc for pc in range(address, address + len(native), 2 if mode == 'thumb' else 4) if pc not in visited],
        'limitations': ['Synthetic mapped pointer graphs, including selected aliases; not all possible alias graphs or invalid pointers',
            'No scene, ownership, scheduler-concurrency or hardware reachability assertion']}
