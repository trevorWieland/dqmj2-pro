import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

ADDRESS = 0x02010C5C
COMMAND = 0x02010BA8
TRANSFER = 0x02010C08
BACKEND = 0x020E5500
PAGE = 0x020E5000
PARAMETERS = 0x020E5B40
DESCRIPTOR = 0x020E54A0
REPLACEMENT = 0x020E58F0
STACK = 0x02500000
STOP = 0x027FF800
IO = 0x04000000
STATUS = IO + 0x1A4
CALLBACK_ARM = 0x020F0100
CALLBACK_THUMB = 0x020F0201
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
PROVIDERS = {0x0200877C: 'dma-stop', 0x02005D50: 'irq-mask-disable', 0x02005D80: 'irq-request-reset', 0x02010FA8: 'qualified-read-id', 0x02011504: 'qualified-release', 0x02007FF4: 'irq-disable', 0x02008008: 'irq-restore', 0x02006924: 'queue-wake', 0x0200698C: 'thread-wake', 0x02009034: 'dma-prepare', CALLBACK_ARM: 'callback-arm', CALLBACK_THUMB & ~1: 'callback-thumb'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(data, address):
    return struct.unpack_from('<I', data, address - PAGE)[0]


def write(data, address, value):
    struct.pack_into('<I', data, address - PAGE, value & 0xFFFFFFFF)


def dependencies(root, arm):
    rows = []
    for family, address in [('command', COMMAND), ('transfer', TRANSFER)]:
        report = json.loads((root / f'evidence/matches/mechanics-save-20261029-card-{family}.json').read_text())
        entry = next(row for row in report['matches'] if int(row['address'], 0) == address)
        for field in ['source', 'object']:
            if sha((root / entry[field]).read_bytes()) != entry[field + 'Sha256']:
                raise AssertionError('Matching continuation source/object changed')
        proof = validate_link(entry, report['nativeSymbolEntries'], root / 'work/mechanics-save/20261029-card-dma-complete/dependencies' / entry['objectSha256'])
        row = entry | freeze_link(proof)
        code = (root / row['isolatedCallerBinary']).read_bytes()
        if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
            raise AssertionError('Continuation dependency differs after actual MW link')
        rows.append((row, code))
    return rows


def model(before, bus, fixture):
    arena, io = bytearray(before), bytearray(bus)
    remaining = (read(before, BACKEND + 0x24) - 512) & 0xFFFFFFFF
    for offset in [0x1C, 0x20]:
        write(arena, BACKEND + offset, read(before, BACKEND + offset) + 512)
    write(arena, BACKEND + 0x24, remaining)
    events = ['dma-stop']
    expected_io_writes = []
    if remaining:
        events += ['transfer', 'dma-prepare', 'command']
        struct.pack_into('<I', io, STATUS - IO, read(before, PARAMETERS + 4))
        io[0x1A1] = 0xC0
        command = bytes([0xB7]) + read(arena, BACKEND + 0x1C).to_bytes(4, 'big') + bytes(3)
        io[0x1A8:0x1B0] = command
        expected_io_writes = [[IO + 0x1A1, 1, 0xC0], *[[IO + 0x1A8 + index, 1, byte] for index, byte in enumerate(command)], [STATUS, 4, read(before, PARAMETERS + 4)]]
    else:
        events += ['irq-mask-disable', 'irq-request-reset', 'qualified-read-id', 'qualified-release', 'irq-disable', 'queue-wake']
        write(arena, BACKEND, REPLACEMENT)
        write(arena, REPLACEMENT, 0)
        write(arena, BACKEND + 0x38, 0)
        write(arena, BACKEND + 0x3C, fixture['argument'] ^ 0xFFFFFFFF)
        flags = (read(before, BACKEND + 0x114) & ~0x4C & ~0x10) | (0x10 if fixture['wake'] else 0)
        write(arena, BACKEND + 0x114, flags)
        if fixture['wake']:
            events.append('thread-wake')
            write(arena, BACKEND + 0xA8, 1)
        events.append('irq-restore')
        if fixture['callback']:
            events.append('callback-thumb' if fixture['callback'] & 1 else 'callback-arm')
            write(arena, BACKEND + 0x30, fixture['seed'] ^ 0xABCDEF00)
    return bytes(arena), bytes(io), events, expected_io_writes


def run(bodies, before, bus, stack, fixture, registers, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_map(IO, 4096)
    for address, body in bodies.items():
        machine.mem_write(address, body)
    for address, data in [(PAGE, before), (IO, bus), (STACK, stack)]:
        machine.mem_write(address, data)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(REGISTERS, registers):
        machine.reg_write(register, value)
    writes, io_writes, events, polls, visits = [], [], [], [], set()
    saved_irq = flags & 0x80
    expected_arena, expected_bus, plan, expected_io_writes = model(before, bus, fixture)

    def memword(address):
        return struct.unpack('<I', bytes(machine.mem_read(address, 4)))[0]

    def memwrite(address, value):
        value &= 0xFFFFFFFF
        machine.mem_write(address, struct.pack('<I', value))
        writes.append([address, 4, value])

    def observe(uc, pc, size, data):
        if pc not in PROVIDERS:
            length = {ADDRESS: 204, COMMAND: 88, TRANSFER: 68}
            if not any(start <= pc < start + length[start] for start in bodies):
                raise AssertionError(('DMA-completion caller escaped reconstructed bodies', hex(pc)))
            visits.add(pc)
            if pc in [TRANSFER, COMMAND]:
                events.append('transfer' if pc == TRANSFER else 'command')
            return
        name = PROVIDERS[pc]
        events.append(name)
        argument = uc.reg_read(UC_ARM_REG_R0)
        irq = uc.reg_read(UC_ARM_REG_CPSR) & 0x80
        result = (fixture['seed'] ^ pc ^ len(events)) & 0xFFFFFFFF
        if name == 'dma-stop' and argument != read(before, BACKEND + 0x28):
            raise AssertionError('DMA-stop channel differs')
        if name in ['irq-mask-disable', 'irq-request-reset'] and argument != 0x80000:
            raise AssertionError('Card IRQ mask argument differs')
        if name == 'qualified-release':
            for address, value in [(BACKEND, REPLACEMENT), (BACKEND + 0x38, fixture['callback']), (BACKEND + 0x3C, fixture['argument'])]:
                memwrite(address, value)
        elif name == 'irq-disable':
            if memword(REPLACEMENT) != 0:
                raise AssertionError('Result word not cleared before callback capture/IRQ disable')
            memwrite(BACKEND + 0x38, 0)
            memwrite(BACKEND + 0x3C, fixture['argument'] ^ 0xFFFFFFFF)
            result, irq = saved_irq, 0x80
        elif name == 'queue-wake':
            if argument != BACKEND + 0x10C or memword(BACKEND + 0x114) != read(before, BACKEND + 0x114) & ~0x4C:
                raise AssertionError('Busy flags/queue before wake differ')
            memwrite(BACKEND + 0x114, (memword(BACKEND + 0x114) & ~0x10) | (0x10 if fixture['wake'] else 0))
        elif name == 'thread-wake':
            if argument != BACKEND + 0x44:
                raise AssertionError('Worker wake argument differs')
            memwrite(BACKEND + 0xA8, 1)
        elif name == 'irq-restore':
            if argument != saved_irq:
                raise AssertionError('Completion lost its saved IRQ state')
            irq = saved_irq
        elif name == 'dma-prepare':
            expected = [read(before, BACKEND + 0x28), 0x04100010, read(expected_arena, BACKEND + 0x20), 512]
            if [uc.reg_read(register) for register in REGISTERS[:4]] != expected:
                raise AssertionError('Continuation did not use advanced destination/DMA arguments')
        elif name.startswith('callback-'):
            if pc != fixture['callback'] & ~1 or bool(uc.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(fixture['callback'] & 1) or argument != fixture['argument'] or irq != saved_irq:
                raise AssertionError('Captured callback/argument/IRQ/interworking differs')
            memwrite(BACKEND + 0x30, fixture['seed'] ^ 0xABCDEF00)
        for number, register in enumerate([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(register, (fixture['seed'] ^ pc ^ (number * 0x1234567)) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_CPSR, ((fixture['seed'] + len(events)) & 15) << 28 | irq | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR) & ~1)

    def observe_read(uc, access, address, size, value, data):
        if IO <= address < IO + 4096:
            if address != STATUS or size != 4 or len(polls) > fixture['busy']:
                raise AssertionError('Unexpected continuation mapped-status read')
            status = struct.unpack_from('<I', bus, STATUS - IO)[0] & 0x7FFFFFFF
            if len(polls) < fixture['busy']:
                status |= 0x80000000
            uc.mem_write(STATUS, struct.pack('<I', status))
            polls.append(status)

    def observe_write(uc, access, address, size, value, data):
        if not any(start <= address and address + size <= start + length for start, length in [(PAGE, len(before)), (IO, len(bus)), (STACK, len(stack))]):
            raise AssertionError('DMA-completion caller wrote outside explicit state windows')
        writes.append([address, size, value])
        if IO <= address < IO + 4096:
            io_writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_READ, observe_read)
    machine.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    machine.emu_start(ADDRESS, STOP, count=4000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise AssertionError('DMA-completion caller did not actually return within its bound')
    actual = [machine.reg_read(register) for register in REGISTERS]
    arena, io = bytes(machine.mem_read(PAGE, len(before))), bytes(machine.mem_read(IO, len(bus)))
    continuing = read(expected_arena, BACKEND + 0x24) != 0
    if arena != expected_arena or io != expected_bus or events != plan or io_writes != expected_io_writes or len(polls) != (fixture['busy'] + 1 if continuing else 0):
        raise AssertionError(('Independent DMA-completion state/call model differs', events, plan))
    if actual[4:12] != registers[4:12] or actual[-2] != registers[-2] or machine.reg_read(UC_ARM_REG_CPSR) & 0x80 != saved_irq:
        raise AssertionError('DMA-completion preserved registers/SP/qualified IRQ state differ')
    return {'registers': actual, 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'arena': arena, 'io': io, 'stack': bytes(machine.mem_read(STACK, len(stack))), 'events': events, 'writes': writes, 'polls': polls, 'visited': sorted(visits)}


def validate(arm, save, matches, root):
    if set(matches) != {'saved_20261029_card_dma_complete'}:
        raise AssertionError('Exact208-byte DMA-completion source is required')
    reused = dependencies(root, arm)
    rows = [*matches.values(), *reused]
    rebuilt = {int(row['address'], 0): body for row, body in rows}
    native = {address: arm[address - 0x02000000:address - 0x02000000 + len(body)] for address, body in rebuilt.items()}
    rng = random.Random(20261029010512)
    vectors = [(512, flag, callback, wake, 0, seed) for seed, flag in enumerate([0, 4, 8, 0x10, 0x20, 0x40, 0x4C, 0x5C, 0x7FFFFFFF, 0xFFFFFFFF]) for callback in [0, CALLBACK_ARM, CALLBACK_THUMB] for wake in [False, True]]
    vectors += [(512, rng.getrandbits(32), [0, CALLBACK_ARM, CALLBACK_THUMB][seed % 3], bool(seed & 1), 0, seed + 1000) for seed in range(256)]
    vectors += [(length, rng.getrandbits(32), 0, False, busy, seed + 2000) for seed, length in enumerate([0, 1, 511, 513, 1024, 1536, 0xFFFFFFFF]) for busy in [0, 2] for unused in range(16)]
    hashes, coverage = [], set()
    finishing, continuing = 0, 0
    for length, flag, callback, wake, busy, seed in vectors:
        arena, bus, stack = bytearray(rng.randbytes(4096)), rng.randbytes(4096), rng.randbytes(0x8000)
        fixture = {'callback': callback, 'wake': wake, 'argument': rng.getrandbits(32), 'busy': busy, 'seed': seed}
        for address, value in [(BACKEND, DESCRIPTOR), (BACKEND + 0x1C, rng.getrandbits(32)), (BACKEND + 0x20, 0x02410100), (BACKEND + 0x24, length), (BACKEND + 0x28, seed % 4), (BACKEND + 0x114, flag)]:
            write(arena, address, value)
        registers = [rng.getrandbits(32) for unused in REGISTERS]
        registers[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | ((seed & 1) << 7) | 0x10
        original = run(native, bytes(arena), bus, stack, fixture, registers, flags)
        compiled = run(rebuilt, bytes(arena), bus, stack, fixture, registers, flags)
        if original != compiled:
            raise AssertionError('Native/source connected DMA-completion effects differ')
        coverage.update(original['visited'])
        finishing += length == 512
        continuing += length != 512
        encoded = {**original, **{name: sha(original[name]) for name in ['arena', 'io', 'stack']}}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
    pcs = sorted(pc for pc in coverage if ADDRESS <= pc < ADDRESS + 204)
    if pcs != list(range(ADDRESS, ADDRESS + 204, 4)):
        raise AssertionError('DMA-completion instruction coverage is incomplete')
    return {'cases': len(vectors), 'nativeAndRecompiledCalls': len(vectors) * 2, 'completionCases': finishing, 'continuationCases': continuing, 'verifiedReturn': True, 'instructionLimit': 4000, 'independentMachineStatePerExecution': True, 'stateSha256': hashes, 'nativeInstructionAddressesVisited': pcs, 'reusedMatchedSources': [row for row, body in reused], 'sourceBodiesExecuted': len(rows), 'retainedNativeCalleeCodeBytes': 0, 'platformProviders': {hex(address): name for address, name in PROVIDERS.items()}, 'physicalDeviceExecuted': False, 'observations': ['Source/destination advance by512 and remaining count decrements by512 with measured unsigned32-bit arithmetic after DMA-stop.', 'A nonzero remaining count executes the actual matched84-byte continuation and96-byte mapped command bodies.', 'Completion clears the descriptor selected by the qualified release provider before IRQ-disable and captures callback/argument before that provider changes their stored words.', 'Queue wake observes flags cleared with4C; a controlled change of bit10 then determines actual worker wake.', 'Captured callbacks execute through controlled ARM/Thumb providers with their captured argument after restoration of the saved qualified IRQ state.', 'All normal fixtures actually return and match full arena/register page/stack/register/write effects against native execution and an independent state/call model.'], 'limitations': ['Physical DMA, ROM-ID acquisition, completion timing, queue scheduling, IRQ safety and removal handling remain unexecuted qualified platform contracts.', 'Numerical underflow inputs exercise measured unsigned behavior only and do not establish valid physical transfer requests.', 'Mapped readiness and callback effects are synthetic; command traffic is not game-save record serialization.', 'Previously matching84/96-byte source bodies earn no duplicate recovered-source credit.']}
