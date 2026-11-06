import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

COMMAND = 0x02010BA8
TRANSFER = 0x02010C08
DMA = 0x02009034
BACKEND = 0x020E5500
PARAMETERS = 0x020E5B40
PAGE = 0x020E5000
IO = 0x04000000
STATUS = IO + 0x1A4
CONTROL = IO + 0x1A1
COMMAND_BYTES = IO + 0x1A8
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
    report = json.loads((root / 'evidence/matches/mechanics-save-20261029-card-command.json').read_text())
    entry = next(row for row in report['matches'] if int(row['address'], 0) == COMMAND)
    for field in ['source', 'object']:
        if sha((root / entry[field]).read_bytes()) != entry[field + 'Sha256']:
            raise AssertionError('Matching command serializer source/object identity changed')
    proof = validate_link(entry, {}, root / 'work/mechanics-save/20261029-card-transfer/dependencies' / entry['objectSha256'])
    row = entry | freeze_link(proof)
    code = (root / row['isolatedCallerBinary']).read_bytes()
    if code != arm[COMMAND - 0x02000000:COMMAND - 0x02000000 + 96]:
        raise AssertionError('Command serializer dependency differs after actual MW link')
    return row, code


def model(before, bus, fixture, transfer):
    arena, io = bytearray(before), bytearray(bus)
    ready = read(bus, STATUS - IO) & 0x7FFFFFFF
    write(io, STATUS - IO, ready)
    if transfer:
        write(arena, BACKEND - PAGE + 0x1C, fixture['afterSource'])
        write(arena, PARAMETERS - PAGE + 4, fixture['afterControl'])
        command = bytes([0xB7]) + fixture['afterSource'].to_bytes(4, 'big') + bytes(3)
    else:
        command = fixture['first'].to_bytes(4, 'big') + fixture['second'].to_bytes(4, 'big')
    io[CONTROL - IO] = 0xC0
    io[COMMAND_BYTES - IO:COMMAND_BYTES - IO + 8] = command
    expected_writes = [[CONTROL, 1, 0xC0], *[[COMMAND_BYTES + index, 1, byte] for index, byte in enumerate(command)]]
    if transfer:
        write(io, STATUS - IO, fixture['afterControl'])
        expected_writes.append([STATUS, 4, fixture['afterControl']])
    return bytes(arena), bytes(io), expected_writes


def run(bodies, before, bus, stack, fixture, transfer, registers, flags):
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
    writes, io_writes, visits, events, provider_writes, reads = [], [], set(), [], [], []
    expected_arena, expected_io, expected_writes = model(before, bus, fixture, transfer)

    def observe(uc, pc, size, data):
        if pc == DMA and transfer:
            events.append('qualified-dma')
            arguments = [uc.reg_read(register) for register in REGISTERS[:4]]
            if arguments != [read(before, BACKEND - PAGE + 0x28), 0x04100010, read(before, BACKEND - PAGE + 0x20), 512]:
                raise AssertionError('Transfer preparation DMA arguments differ')
            for address, value in [(BACKEND + 0x1C, fixture['afterSource']), (PARAMETERS + 4, fixture['afterControl'])]:
                uc.mem_write(address, struct.pack('<I', value))
                provider_writes.append([address, 4, value])
            for number, register in enumerate([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
                uc.reg_write(register, (fixture['afterSource'] ^ pc ^ (number * 0x1234567)) & 0xFFFFFFFF)
            uc.reg_write(UC_ARM_REG_CPSR, (fixture['afterControl'] & 15) << 28 | 0x10)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if not any(start <= pc < start + (88 if start == COMMAND else 68) for start in bodies):
            raise AssertionError(('Card command/transfer escaped declared source bodies', hex(pc)))
        visits.add(pc)
        if pc == COMMAND:
            events.append('command')
            expected = [0xB7000000 | fixture['afterSource'] >> 8, (fixture['afterSource'] << 24) & 0xFFFFFFFF] if transfer else [fixture['first'], fixture['second']]
            if [uc.reg_read(register) for register in REGISTERS[:2]] != expected:
                raise AssertionError('Command-word construction differs')

    def observe_read(uc, access, address, size, value, data):
        if IO <= address < IO + 4096:
            if address != STATUS or size != 4 or len(reads) > fixture['busyReads']:
                raise AssertionError('Unexpected or excess emulated status poll')
            status = read(bus, STATUS - IO) & 0x7FFFFFFF
            if len(reads) < fixture['busyReads']:
                status |= 0x80000000
            uc.mem_write(STATUS, struct.pack('<I', status))
            reads.append(status)

    def observe_write(uc, access, address, size, value, data):
        if not any(start <= address and address + size <= start + length for start, length in [(IO, 4096), (STACK, len(stack))]):
            raise AssertionError(('Card routine wrote outside explicit mapped IO/stack', hex(address), size))
        writes.append([address, size, value])
        if IO <= address < IO + 4096:
            io_writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_READ, observe_read)
    machine.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    entry = TRANSFER if transfer else COMMAND
    machine.emu_start(entry, STOP, count=2000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise AssertionError('Card command/transfer did not actually return within its bound')
    actual_registers = [machine.reg_read(register) for register in REGISTERS]
    arena, io = bytes(machine.mem_read(PAGE, len(before))), bytes(machine.mem_read(IO, len(bus)))
    if arena != expected_arena or io != expected_io or io_writes != expected_writes or len(reads) != fixture['busyReads'] + 1 or events != (['qualified-dma', 'command'] if transfer else ['command']):
        raise AssertionError('Independent card command mapped-register/call model differs')
    if actual_registers[4:12] != registers[4:12] or actual_registers[-2] != registers[-2]:
        raise AssertionError('Card routine preserved registers/SP differ')
    actual_stack = bytes(machine.mem_read(STACK, len(stack)))
    if not transfer and actual_stack != stack:
        raise AssertionError('Leaf command serializer unexpectedly changed stack contents')
    return {'registers': actual_registers, 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'arena': arena, 'io': io, 'stack': actual_stack, 'writes': writes, 'providerWrites': provider_writes, 'statusPolls': reads, 'events': events, 'visited': sorted(visits)}


def validate(arm, save, matches, root):
    names = set(matches)
    transfer = names == {'saved_20261029_card_transfer_prepare'}
    if not transfer and names != {'saved_20261029_card_command'}:
        raise AssertionError('The complete command or transfer source is required')
    reused = [dependencies(root, arm)] if transfer else []
    rows = [*matches.values(), *reused]
    rebuilt = {int(row['address'], 0): body for row, body in rows}
    native = {address: arm[address - 0x02000000:address - 0x02000000 + len(body)] for address, body in rebuilt.items()}
    rng = random.Random(20261029010 + int(transfer))
    vectors = []
    if transfer:
        for source in [0, 1, 255, 256, 511, 512, 0x12345678, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF]:
            for channel in range(4):
                for control in [0, 0x80000000, 0xFFFFFFFF, 0xA5A55A5A]:
                    for busy in [0, 1, 3]:
                        vectors.append({'afterSource': source, 'afterControl': control, 'channel': channel, 'busyReads': busy})
        vectors += [{'afterSource': rng.getrandbits(32), 'afterControl': rng.getrandbits(32), 'channel': seed % 4, 'busyReads': seed % 9} for seed in range(128)]
    else:
        for first in [0, 1, 0x80, 0xFF, 0x100, 0x8000, 0x10000, 0x80000000, 0xFFFFFFFF, 0x12345678]:
            for second in [0, 1, 0x80, 0xFF, 0x100, 0x8000, 0x10000, 0x80000000, 0xFFFFFFFF, 0x12345678]:
                for busy in [0, 1, 2, 7]:
                    vectors.append({'first': first, 'second': second, 'busyReads': busy})
        vectors += [{'first': rng.getrandbits(32), 'second': rng.getrandbits(32), 'busyReads': seed % 9} for seed in range(128)]
    hashes, coverage = [], set()
    for fixture in vectors:
        arena, bus, stack = bytearray(rng.randbytes(4096)), rng.randbytes(4096), rng.randbytes(0x8000)
        if transfer:
            write(arena, BACKEND - PAGE + 0x28, fixture['channel'])
            write(arena, BACKEND - PAGE + 0x20, 0x02410100)
        registers = [rng.getrandbits(32) for unused in REGISTERS]
        if not transfer:
            registers[:2] = [fixture['first'], fixture['second']]
        registers[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | 0x10
        original = run(native, bytes(arena), bus, stack, fixture, transfer, registers, flags)
        compiled = run(rebuilt, bytes(arena), bus, stack, fixture, transfer, registers, flags)
        if original != compiled:
            raise AssertionError('Native/source mapped card command/transfer effects differ')
        coverage.update(original['visited'])
        encoded = {**original, **{name: sha(original[name]) for name in ['arena', 'io', 'stack']}}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
    expected_pcs = set(range(COMMAND, COMMAND + 88, 4))
    if transfer:
        expected_pcs |= set(range(TRANSFER, TRANSFER + 68, 4))
    if coverage != expected_pcs:
        raise AssertionError('Mapped card command/transfer instruction coverage is incomplete')
    observations = ['The mapped status bit is polled until the explicit readiness script clears bit31; every successful fixture actually returns.', 'The command routine writes control byteC0 followed by two words as eight big-endian command bytes in exact measured order.', 'Full mapped register page, common arena, stack, registers/CPSR, polls and ordered writes are compared.']
    if transfer:
        observations.extend(['The transfer caller passes channel/FIFO source/destination/512 to the qualified DMA provider, then constructsB7 plus the updated32-bit source offset and three zero command bytes.', 'The final transfer control word is read after the provider and command call and written to the mapped status/control address.'])
    return {'cases': len(vectors), 'nativeAndRecompiledCalls': len(vectors) * 2, 'verifiedReturn': True, 'instructionLimit': 2000, 'independentMachineStatePerExecution': True, 'stateSha256': hashes, 'nativeInstructionAddressesVisited': sorted(coverage), 'reusedMatchedSources': [row for row, body in reused], 'sourceBodiesExecuted': len(rows), 'retainedNativeCalleeCodeBytes': 0, 'emulatedMappedMmio': True, 'physicalDeviceExecuted': False, 'platformProviders': {hex(DMA): 'qualified-dma-preparation'} if transfer else {}, 'observations': observations, 'limitations': ['Mapped MMIO and scripted readiness are emulated observations; no physical card device, DMA, cache coherence, IRQ timing or concurrent transfer is established.', 'Command register serialization is distinct from game-save record serialization.', 'The transfer-only DMA provider explicitly changes source/control words to test post-call observations; its implementation is not executed.', 'Both routines have void interfaces; architectural results are compared without a semantic return-value claim.']}
