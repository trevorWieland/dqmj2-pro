import hashlib
from pathlib import Path
import random
import match_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
BASE = 0x027E0000
MODULE = 'extract/utility/runtime/utility-child-arm7-main.bin'
MODULE_SHA = 'a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a'
VIRTUAL = 0x026A0000
STACK = 0x02300000
BUFFER = 0x02220000
PAYLOAD = BUFFER + 0x100
CONTROL = 0x040001C0
DATA = 0x040001C2
RETURN = 0x02500000
SPECS = {0x027F6428: {'bytes': 300, 'kind': 'emit', 'opcode': 2, 'dummy': False},
    0x027F6554: {'bytes': 300, 'kind': 'emit', 'opcode': 10, 'dummy': False},
    0x027F6680: {'bytes': 316, 'kind': 'capture', 'opcode': 11, 'dummy': True},
    0x027F67BC: {'bytes': 288, 'kind': 'capture', 'opcode': 3, 'dummy': False}}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address):
    rows = [{'address': value, 'count': count, 'busyReadsPerPoll': delay, 'stuck': False}
        for value in (0, 1, 0x7F, 0xF0, 0xFF, 0x100, 0x123456, 0x1234F0, 0x00FFFFFF, 0xFFFFFFFF)
        for count in (0, 1, 2, 17, 32) for delay in (0, 2)]
    if SPECS[address]['kind'] == 'emit':
        rows.extend({'address': 0xFFFFFFFF, 'count': count, 'busyReadsPerPoll': delay, 'stuck': False}
            for count in (0x80000001, 0xFFFFFFFF) for delay in (0, 2))
    return rows


def effective_count(spec, case):
    count, address = case['count'], case['address']
    if not count:
        return 0
    if spec['kind'] == 'emit':
        last = (address + count - 1) & 0xFFFFFFFF
        if last >> 8 > address >> 8:
            count = 256 - (address & 255)
        bound = (count - 1) & 0xFFFFFFFF
        if bound >= 0x80000000:
            return 1
    return count


def input_word(index, seed):
    return (0x9A00 ^ (index * 0x1357 + seed * 0x211)) & 0xFFFF


def model(spec, case, seed, initial_buffer):
    count = effective_count(spec, case)
    image, writes = bytearray(initial_buffer), []
    if not count:
        return {'r0': case['address'], 'count': 0, 'writes': [], 'controlReads': 0, 'dataReads': 0,
            'bufferReads': 0, 'buffer': bytes(image), 'ports': [0x1234, 0]}
    if count > 0x300:
        raise ValueError('Large transfer model is outside this bounded source fixture')
    writes.extend([[CONTROL, 2, 0x8900], [DATA, 2, spec['opcode']]])
    writes.extend([DATA, 2, case['address'] >> shift & 255] for shift in (16, 8, 0))
    if spec['dummy']:
        writes.append([DATA, 2, 0])
    for index in range(count):
        if index == count - 1:
            writes.append([CONTROL, 2, 0x8100])
        value = image[0x100 + index] if spec['kind'] == 'emit' else 0
        writes.append([DATA, 2, value])
        if spec['kind'] == 'capture':
            value = input_word(index, seed) & 255
            image[0x100 + index] = value
            writes.append([PAYLOAD + index, 1, value])
    groups = count + 5 + int(spec['dummy'])
    return {'r0': 0 if spec['kind'] == 'emit' else count - 1, 'count': count, 'writes': writes,
        'controlReads': groups * (case['busyReadsPerPoll'] + 1),
        'dataReads': count if spec['kind'] == 'capture' else 0, 'bufferReads': count if spec['kind'] == 'emit' else 0,
        'buffer': bytes(image), 'ports': [0x8100, image[0x100 + count - 1] if spec['kind'] == 'emit' else input_word(count - 1, seed)]}


def execute(address, body, case, seed, virtual=False, budget=50000):
    spec = SPECS[address]
    raw = (ROOT / MODULE).read_bytes()
    if digest(raw) != MODULE_SHA:
        raise ValueError('Measured child ARM7 image changed')
    start = VIRTUAL if virtual else address
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE, 0x20000)
    cpu.mem_write(BASE, raw)
    if virtual:
        cpu.mem_map(VIRTUAL, 0x2000)
    cpu.mem_write(start, body)
    cpu.mem_map(STACK, 0x4000)
    cpu.mem_map(BUFFER, 0x4000)
    cpu.mem_map(CONTROL & ~0xFFF, 0x1000)
    rng = random.Random(20261031 + seed)
    stack, buffer = rng.randbytes(0x4000), rng.randbytes(0x4000)
    cpu.mem_write(STACK, stack)
    cpu.mem_write(BUFFER, buffer)
    cpu.mem_write(CONTROL, (0x1234).to_bytes(2, 'little'))
    initial = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    initial[:3], initial[-2:] = [case['address'], case['count'], PAYLOAD], [STACK + 0x3E00, RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    writes, control_reads, data_reads, buffer_reads, visited = [], [], [], [], set()
    pending, control_word = case['busyReadsPerPoll'], 0x1234

    def code(machine, pc, size, unused):
        if not start <= pc < start + len(body) - 8:
            raise ValueError('Source execution delegated to original code or entered a pool/outside its full body')
        visited.add(pc - start)

    def read(machine, access, location, size, value, unused):
        nonlocal pending
        if location == CONTROL:
            if size != 2:
                raise ValueError('Native control read width changed')
            value = control_word & ~0x80 | (0x80 if pending or case['stuck'] else 0)
            if pending:
                pending -= 1
            machine.mem_write(CONTROL, value.to_bytes(2, 'little'))
            control_reads.append(value)
        elif location == DATA:
            if size != 2:
                raise ValueError('Native data read width changed')
            value = input_word(len(data_reads), seed)
            machine.mem_write(DATA, value.to_bytes(2, 'little'))
            data_reads.append(value)
        elif BUFFER <= location < BUFFER + 0x4000:
            if not PAYLOAD <= location < PAYLOAD + 0x300 or size != 1:
                raise ValueError('Unqualified input buffer read outside bounded byte storage')
            buffer_reads.append(location)

    def write(machine, access, location, size, value, unused):
        nonlocal pending, control_word
        value &= (1 << (size * 8)) - 1
        if STACK <= location < STACK + 0x4000:
            if not initial[-2] - 0x100 <= location < initial[-2]:
                raise ValueError('Source/native stack write escaped bounded temporary frame')
            return
        if location in (CONTROL, DATA):
            if size != 2:
                raise ValueError('Native control/data write width changed')
            if location == CONTROL:
                control_word = value
            else:
                pending = case['busyReadsPerPoll']
        elif not PAYLOAD <= location < PAYLOAD + 0x300 or size != 1:
            raise ValueError('Native/source wrote outside qualified port/destination/stack context')
        writes.append([location, size, value])

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_READ, read)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    fault = None
    try:
        cpu.emu_start(start, RETURN, count=budget, timeout=2000000)
    except UcError as error:
        fault = error.errno
    observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    pc, cpsr = cpu.reg_read(UC_ARM_REG_PC), cpu.reg_read(UC_ARM_REG_CPSR)
    returned = pc == RETURN
    image = bytes(cpu.mem_read(BUFFER, 0x4000))
    ports = [int.from_bytes(cpu.mem_read(location, 2), 'little') for location in (CONTROL, DATA)]
    if returned:
        predicted = model(spec, case, seed, buffer)
        if fault is not None or observed[0] != predicted['r0'] or image != predicted['buffer'] or writes != predicted['writes'] or ports != predicted['ports']:
            raise ValueError('Independent native raw argument/transfer/full-buffer/ordered-write model differs')
        if len(control_reads) != predicted['controlReads'] or len(data_reads) != predicted['dataReads'] or len(buffer_reads) != predicted['bufferReads']:
            raise ValueError('Native source/bus read-count and width model differs')
        if observed[4:12] != initial[4:12] or observed[-2:] != initial[-2:] or cpsr & 0xFF != 0xD3:
            raise ValueError('Native/source callee-saved/return/mode contract differs')
        current_stack = bytes(cpu.mem_read(STACK, 0x4000))
        if current_stack[:0x3D00] != stack[:0x3D00] or current_stack[0x3E00:] != stack[0x3E00:]:
            raise ValueError('Native/source stack guard changed')
    return {'actualReturn': returned, 'fault': fault, 'r0': observed[0], 'preservedRegisters': observed[4:12],
        'sp': observed[-2], 'lr': observed[-1], 'mode': cpsr & 0xFF, 'writes': writes,
        'controlReads': len(control_reads), 'dataReads': len(data_reads), 'bufferReads': len(buffer_reads),
        'controlReadSha256': digest(repr(control_reads).encode()), 'dataReadSha256': digest(repr(data_reads).encode()),
        'bufferReadSha256': digest(repr(buffer_reads).encode()), 'bufferSha256': digest(image), 'finalPortWords': ports,
        'internalUnmatchedMachineState': {'scratchRegisters': observed[1:4] + [observed[12]], 'apsr': cpsr & 0xF0000000,
            'pcOffsetOrReturn': 'returned' if returned else hex(pc - start), 'visitedOwnInstructionOffsets': sorted(visited),
            'temporaryStackSha256': digest(bytes(cpu.mem_read(STACK, 0x4000)))}}


def functional(state):
    return {key: value for key, value in state.items() if key != 'internalUnmatchedMachineState'}
