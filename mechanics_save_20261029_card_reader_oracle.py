import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

ADDRESS = 0x02010EB8
COMMAND = 0x02010BA8
CACHE_COPY = 0x02010B1C
COPY = 0x02008E0C
BACKEND = 0x020E5500
PAGE = 0x020E5000
CACHE_PAGE = 0x02400000
CACHE = CACHE_PAGE + 0x100
DESTINATION = 0x02410000
STACK = 0x02500000
STOP = 0x027FF800
IO = 0x04000000
STATUS = IO + 0x1A4
FIFO_PAGE = 0x04100000
FIFO = FIFO_PAGE + 0x10
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


def write(data, offset, value):
    struct.pack_into('<I', data, offset, value & 0xFFFFFFFF)


def stream_word(base, index, seed):
    return ((base >> 2) ^ index ^ seed ^ 0x91A2B3C4) & 0xFFFFFFFF


def dependencies(root, arm):
    rows = []
    for relative, address in [('evidence/matches/mechanics-save-20261029-card-command.json', COMMAND), ('evidence/matches/mechanics-save-20261029-card-cache.json', CACHE_COPY), ('evidence/matches/mechanics-save-sdk-memory-original-asm.json', COPY)]:
        report = json.loads((root / relative).read_text())
        entry = next(row for row in report['matches'] if int(row['address'], 0) == address)
        for field in ['source', 'object']:
            if sha((root / entry[field]).read_bytes()) != entry[field + 'Sha256']:
                raise AssertionError('Polling dependency source/object identity changed')
        proof = validate_link(entry, report.get('nativeSymbolEntries', {}), root / 'work/mechanics-save/20261029-card-reader/dependencies' / entry['objectSha256'])
        row = entry | freeze_link(proof)
        code = (root / row['isolatedCallerBinary']).read_bytes()
        if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
            raise AssertionError('Polling dependency differs after actual MW link')
        rows.append((row, code))
    return rows


def model(arena, cache, destination, bus, fixture):
    expected, buffer, output, io = bytearray(arena), bytearray(cache), bytearray(destination), bytearray(bus)
    blocks = []
    while True:
        source, pointer, length = [read(expected, BACKEND - PAGE + offset) for offset in [0x1C, 0x20, 0x24]]
        base = source & 0xFFFFFE00
        direct = source == base and pointer % 4 == 0 and length >= 512
        target = pointer if direct else CACHE + 32
        if not direct:
            write(buffer, CACHE - CACHE_PAGE + 8, base)
        for index in range(min(128, fixture['words'])):
            payload = struct.pack('<I', stream_word(base, index, fixture['seed']))
            if direct:
                offset = target - DESTINATION + 4 * index
                output[offset:offset + 4] = payload
            else:
                offset = CACHE - CACHE_PAGE + 32 + 4 * index
                buffer[offset:offset + 4] = payload
        count = 512 if direct else min(512 - (source - base), length)
        if not direct:
            source_offset = CACHE - CACHE_PAGE + 32 + source - base
            output[pointer - DESTINATION:pointer - DESTINATION + count] = buffer[source_offset:source_offset + count]
        for field, value in [(0x1C, source + count), (0x20, pointer + count), (0x24, length - count)]:
            write(expected, BACKEND - PAGE + field, value)
        blocks.append({'source': source, 'destination': pointer, 'length': length, 'base': base, 'direct': direct, 'target': target, 'count': count})
        if length == count:
            break
        if len(blocks) > 8:
            raise AssertionError('Fixture model exceeds supported bounded block count')
    control = read(cache, CACHE - CACHE_PAGE + 4) & ~0x80800000
    write(io, STATUS - IO, control | (0x800000 if fixture['words'] else 0))
    io[0x1A1] = 0xC0
    io[0x1A8:0x1B0] = bytes([0xB7]) + blocks[-1]['base'].to_bytes(4, 'big') + bytes(3)
    return bytes(expected), bytes(buffer), bytes(output), bytes(io), blocks


def run(bodies, arena, cache, destination, bus, stack, fixture, registers, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_map(IO, 4096)
    machine.mem_map(FIFO_PAGE, 4096)
    for address, body in bodies.items():
        machine.mem_write(address, body)
    for address, data in [(PAGE, arena), (CACHE_PAGE, cache), (DESTINATION, destination), (IO, bus), (STACK, stack)]:
        machine.mem_write(address, data)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(REGISTERS, registers):
        machine.reg_write(register, value)
    expected_arena, expected_cache, expected_destination, expected_bus, blocks = model(arena, cache, destination, bus, fixture)
    visits, writes, io_writes, events, fifo_reads = set(), [], [], [], []
    state = {'phase': None, 'nextBlock': 0, 'active': None, 'commandPolls': 0, 'samples': [], 'sample': 0, 'fifo': 0}

    def memword(address):
        return struct.unpack('<I', bytes(machine.mem_read(address, 4)))[0]

    def observe(uc, pc, size, data):
        lengths = {ADDRESS: 228, COMMAND: 88, CACHE_COPY: 136, COPY: 304}
        if not any(start <= pc < start + lengths[start] for start in bodies):
            raise AssertionError(('Polling reader escaped recovered source bodies', hex(pc)))
        visits.add(pc)
        if pc == COMMAND:
            if state['nextBlock'] >= len(blocks) or state['phase'] == 'data' and (state['sample'] != len(state['samples']) or state['fifo'] != fixture['words']):
                raise AssertionError('Polling reader started an unexpected/incomplete next page')
            block = blocks[state['nextBlock']]
            if [uc.reg_read(register) for register in REGISTERS[:2]] != [0xB7000000 | block['base'] >> 8, block['base'] << 24 & 0xFFFFFFFF]:
                raise AssertionError('Polling page command words differ')
            state.update({'phase': 'command', 'active': state['nextBlock'], 'commandPolls': 0})
            state['nextBlock'] += 1
            events.append(['command', block['base']])
        elif pc == CACHE_COPY:
            block = blocks[state['active']]
            if block['direct'] or uc.reg_read(UC_ARM_REG_R0) != CACHE:
                raise AssertionError('Polling cached-copy route differs')
            events.append(['cache-copy', block['count']])
        elif pc == COPY:
            block = blocks[state['active']]
            expected = [CACHE + 32 + block['source'] - block['base'], block['destination'], block['count']]
            if [uc.reg_read(register) for register in REGISTERS[:3]] != expected:
                raise AssertionError('Actual recovered SDK copy arguments differ')
            events.append(['sdk-copy', block['count']])

    def observe_read(uc, access, address, size, value, data):
        if address == STATUS and size == 4:
            if state['phase'] == 'command':
                if state['commandPolls'] > fixture['busy']:
                    raise AssertionError('Polling page command exceeded its readiness script')
                status = memword(STATUS) & 0x7FFFFFFF
                if state['commandPolls'] < fixture['busy']:
                    status |= 0x80000000
                state['commandPolls'] += 1
            elif state['phase'] == 'data':
                if state['sample'] >= len(state['samples']):
                    raise AssertionError('Polling reader exhausted its finite data-status script')
                status = state['samples'][state['sample']]
                state['sample'] += 1
            else:
                raise AssertionError('Unexpected mapped card status read')
            uc.mem_write(STATUS, struct.pack('<I', status))
        elif address == FIFO and size == 4:
            if state['phase'] != 'data' or not memword(STATUS) & 0x800000 or state['fifo'] >= fixture['words']:
                raise AssertionError('Unexpected or surplus-exhausted FIFO read')
            base = blocks[state['active']]['base']
            payload = stream_word(base, state['fifo'], fixture['seed'])
            uc.mem_write(FIFO, struct.pack('<I', payload))
            fifo_reads.append([base, state['fifo'], payload])
            state['fifo'] += 1
        elif IO <= address < IO + 4096 or FIFO_PAGE <= address < FIFO_PAGE + 4096:
            raise AssertionError('Undeclared mapped register read')

    def observe_write(uc, access, address, size, value, data):
        if not any(start <= address and address + size <= start + length for start, length in [(PAGE, len(arena)), (CACHE_PAGE, len(cache)), (DESTINATION, len(destination)), (IO, len(bus)), (STACK, len(stack))]):
            raise AssertionError('Polling reader wrote outside explicit state windows')
        writes.append([address, size, value])
        if IO <= address < IO + 4096:
            io_writes.append([address, size, value])
        if address == STATUS:
            if size != 4 or state['phase'] != 'command' or state['commandPolls'] != fixture['busy'] + 1 or value != read(cache, CACHE - CACHE_PAGE + 4):
                raise AssertionError('Polling data-phase control write/order differs')
            control = value & ~0x80800000
            samples = []
            for index in range(fixture['words']):
                if index % 16 == 0:
                    samples += [control | 0x80000000] * fixture['gaps']
                samples.append(control | 0x80800000)
            if samples:
                samples[-1] &= ~0x80000000
            else:
                samples = [control]
            state.update({'phase': 'data', 'samples': samples, 'sample': 0, 'fifo': 0})

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_READ, observe_read)
    machine.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    machine.emu_start(ADDRESS, STOP, count=20000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or state['nextBlock'] != len(blocks) or state['sample'] != len(state['samples']) or state['fifo'] != fixture['words']:
        raise AssertionError('Polling reader did not actually return after complete finite device scripts')
    actual = [machine.reg_read(register) for register in REGISTERS]
    output = {name: bytes(machine.mem_read(address, length)) for name, address, length in [('arena', PAGE, len(arena)), ('cache', CACHE_PAGE, len(cache)), ('destination', DESTINATION, len(destination)), ('io', IO, len(bus)), ('stack', STACK, len(stack))]}
    if [output[name] for name in ['arena', 'cache', 'destination', 'io']] != [expected_arena, expected_cache, expected_destination, expected_bus]:
        raise AssertionError('Independent polling reader complete-state model differs')
    expected_io_writes, expected_events = [], []
    for block in blocks:
        command = bytes([0xB7]) + block['base'].to_bytes(4, 'big') + bytes(3)
        expected_io_writes += [[IO + 0x1A1, 1, 0xC0], *[[IO + 0x1A8 + index, 1, byte] for index, byte in enumerate(command)], [STATUS, 4, read(cache, CACHE - CACHE_PAGE + 4)]]
        expected_events.append(['command', block['base']])
        if not block['direct']:
            expected_events += [['cache-copy', block['count']], ['sdk-copy', block['count']]]
    if io_writes != expected_io_writes or events != expected_events or len(fifo_reads) != len(blocks) * fixture['words']:
        raise AssertionError('Independent polling reader call/write/FIFO model differs')
    if actual[4:12] != registers[4:12] or actual[-2] != registers[-2]:
        raise AssertionError('Polling reader did not restore preserved registers/SP')
    return {**output, 'registers': actual, 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'writes': writes, 'events': events, 'fifoReads': fifo_reads, 'visited': sorted(visits), 'blocks': len(blocks)}


def validate(arm, save, matches, root):
    if set(matches) != {'saved_20261029_card_read_polling'}:
        raise AssertionError('Exact240-byte polling reader source is required')
    reused = dependencies(root, arm)
    rows = [*matches.values(), *reused]
    rebuilt = {int(row['address'], 0): body for row, body in rows}
    native = {address: arm[address - 0x02000000:address - 0x02000000 + len(body)] for address, body in rebuilt.items()}
    rng = random.Random(20261029010524)
    vectors = [(offset, length, alignment, 128 + (offset + length + alignment) % 4) for offset in [0, 1, 2, 3, 4, 7, 15, 16, 31, 32, 255, 256, 508, 509, 510, 511] for length in [0, 1, 2, 3, 4, 31, 32, 511, 512, 513, 1024, 1541] for alignment in range(4)]
    vectors += [(offset, [0, 1, 511, 512][offset % 4], offset % 4, 128 + offset % 3) for offset in range(512)]
    vectors += [(offset, length, alignment, words) for offset in [0, 1] for length in [0, 1, 512, 513] for alignment in [0, 1] for words in [0, 1, 127]]
    hashes, coverage = [], set()
    total_blocks, total_fifo, short_cases = 0, 0, 0
    for seed, (offset, length, alignment, words) in enumerate(vectors):
        arena, cache = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
        for field, value in [(0x1C, [0, 0x02000000, 0x7FFFFE00, 0xFFFFFE00][seed % 4] + offset), (0x20, DESTINATION + 0x100 + alignment), (0x24, length)]:
            write(arena, BACKEND - PAGE + field, value)
        fixture = {'seed': seed, 'busy': seed % 4, 'gaps': seed % 3, 'words': words}
        bus, stack, destination = rng.randbytes(4096), rng.randbytes(0x8000), rng.randbytes(4096)
        registers = [rng.getrandbits(32) for unused in REGISTERS]
        registers[0] = CACHE
        registers[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | 0x10
        original = run(native, bytes(arena), bytes(cache), destination, bus, stack, fixture, registers, flags)
        compiled = run(rebuilt, bytes(arena), bytes(cache), destination, bus, stack, fixture, registers, flags)
        if original != compiled:
            raise AssertionError('Native/source connected polling-reader effects differ')
        coverage.update(original['visited'])
        total_blocks += original['blocks']
        total_fifo += len(original['fifoReads'])
        short_cases += words < 128
        encoded = {**original, **{name: sha(original[name]) for name in ['arena', 'cache', 'destination', 'io', 'stack']}}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
    pcs = sorted(pc for pc in coverage if ADDRESS <= pc < ADDRESS + 228)
    if pcs != list(range(ADDRESS, ADDRESS + 228, 4)):
        raise AssertionError('Polling reader instruction coverage is incomplete')
    return {'cases': len(vectors), 'nativeAndRecompiledCalls': len(vectors) * 2, 'verifiedReturn': True, 'instructionLimit': 20000, 'independentMachineStatePerExecution': True, 'stateSha256': hashes, 'nativeInstructionAddressesVisited': pcs, 'scriptedBlocksPerEngine': total_blocks, 'scriptedFifoReadsPerEngine': total_fifo, 'shortFiniteScriptCases': short_cases, 'reusedMatchedSources': [row for row, body in reused], 'sourceBodiesExecuted': len(rows), 'retainedNativeCalleeCodeBytes': 0, 'platformProviders': {}, 'physicalDeviceExecuted': False, 'observations': ['All512 logical source offsets and aligned/unaligned destination routes execute with zero, partial, full and multiple-page requests.', 'The actual matched command/cache-copy bodies and accepted original SDK copy source execute, without synthetic function providers.', 'Readiness gaps and surplus-ready words preserve every native FIFO read while destination writes are capped at512 bytes per page.', 'Direct pages advance by512; cached pages copy the required suffix/prefix and update the current source/destination/remaining words.', 'Short finite data scripts expose measured unchecked completion behavior under emulated input; no physical error-handling claim is made.', 'All successful fixtures actually return after complete finite scripts; entire common/cache/destination/register pages, stack and architectural effects are compared.'], 'limitations': ['FIFO values, ready/busy transitions and short scripts are explicit emulated device inputs, not physical card or DMA execution.', 'Timing, real cartridge data, removal handling, IRQ safety, fairness and concurrency are not established.', 'Requests beyond the bounded disposable destination/window sizes are unsupported by this oracle.', 'Existing96/140/304-byte sources earn no duplicate recovery credit; card command traffic is not save-record serialization.']}
