import hashlib
import json
import random
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link

ADDRESS = 0x020100E4
BACKEND = 0x020E5500
DESCRIPTOR = 0x020E54A0
ENABLED = 0x020E5480
THREAD = BACKEND + 0x44
THREAD_STATE = THREAD + 0x64
TASK = 0x02011244
CALLBACK = 0x02011210
RUNTIME = 0x020E5B20
PAGE = 0x020E5000
HEADER = 0x027FF000
MODE = 0x027FFC40
SOURCE_HEADER = 0x027FFE00
DESTINATION_HEADER = 0x027FFA80
STACK = 0x02500000
STOP = 0x027FF800
ENABLE = 0x0201021C
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]
PROVIDERS = {0x02008C58: 'clear-fast', 0x02007308: 'cache-flush', 0x02008E0C: 'copy-header', 0x020065F0: 'thread-create', 0x0200698C: 'thread-wake', 0x0200A3D0: 'fifo-register'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def word(data, offset, value):
    struct.pack_into('<I', data, offset, value & 0xFFFFFFFF)


def dependencies(root, arm):
    report = json.loads((root / 'evidence/matches/save-write-configuration.json').read_text())
    entry = next(row for row in report['matches'] if int(row['address'], 0) == ENABLE)
    row = {**report, **entry}
    for field in ['source', 'object']:
        if sha((root / row[field]).read_bytes()) != row[field + 'Sha256']:
            raise AssertionError('Accepted enable setter identity changed')
    bindings = {relocation['symbol']: {'address': relocation['target'], 'mode': 'data', 'module': 'main', 'processor': 'arm9', 'kind': 'data'} for relocation in row['relocations']}
    folder = root / 'work/mechanics-save/20261029-common/dependencies' / row['objectSha256']
    proof = validate_link(row, bindings, folder)
    row.update(freeze_link(proof))
    code = (root / row['isolatedCallerBinary']).read_bytes()
    if code != arm[ENABLE - 0x02000000:ENABLE - 0x02000000 + 16]:
        raise AssertionError('Reused enable setter differs after real MW link')
    evidence_fields = ['isolatedCallerBinary', 'isolatedCallerBinarySha256', 'isolatedCallerLinkSnapshotManifest', 'isolatedCallerLinkSnapshotManifestSha256']
    return entry | {field: row[field] for field in evidence_fields}, code


def model(arena, header, second_mode):
    expected, shared = bytearray(arena), bytearray(header)
    first_mode = struct.unpack_from('<H', header, MODE - HEADER)[0]
    for offset, value in [(0, DESCRIPTOR), (8, 0xFFFFFFFD), (12, 0), (24, 0), (0x118, 0xFFFFFFFF), (0x11C, 0xFFFFFFFF), (0x14, 0), (0x10, 0), (0x110, 0), (0x10C, 0), (0x108, 4)]:
        word(expected, BACKEND - PAGE + offset, value)
    expected[DESCRIPTOR - PAGE:DESCRIPTOR - PAGE + 96] = bytes(96)
    events = ['clear-fast', 'cache-flush']
    if first_mode != 2:
        shared[DESTINATION_HEADER - HEADER:DESTINATION_HEADER - HEADER + 352] = header[SOURCE_HEADER - HEADER:SOURCE_HEADER - HEADER + 352]
        events.append('copy-header')
    word(expected, THREAD_STATE - PAGE, 1)
    struct.pack_into('<H', shared, MODE - HEADER, second_mode)
    events += ['thread-create', 'thread-wake', 'fifo-register']
    if second_mode != 2:
        word(expected, ENABLED - PAGE, 1)
        events.append('enable')
    return bytes(expected), bytes(shared), events


def run(bodies, arena, header, stack, seed, second_mode, registers, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    for address, body in bodies.items():
        machine.mem_write(address, body)
    for address, data in [(PAGE, arena), (HEADER, header), (STACK, stack)]:
        machine.mem_write(address, data)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(REGISTERS, registers):
        machine.reg_write(register, value)
    events, writes, visited = [], [], set()

    def read(address):
        return struct.unpack('<I', bytes(machine.mem_read(address, 4)))[0]

    def write(address, payload):
        machine.mem_write(address, payload)
        writes.append([address, len(payload), sha(payload)])

    def observe(uc, pc, size, data):
        if pc not in PROVIDERS:
            if not any(address <= pc < address + (244 if address == ADDRESS else 12) for address in bodies):
                raise AssertionError(('Common initializer escaped source bodies', hex(pc)))
            visited.add(pc)
            if pc == ENABLE:
                events.append('enable')
                if uc.reg_read(UC_ARM_REG_R0) != 1:
                    raise AssertionError('Enable setter argument differs')
            return
        name = PROVIDERS[pc]
        events.append(name)
        arguments = [uc.reg_read(register) for register in REGISTERS[:4]]
        if name == 'clear-fast':
            if arguments[:3] != [0, DESCRIPTOR, 96] or [read(BACKEND + offset) for offset in [0, 8, 12, 24]] != [DESCRIPTOR, 0xFFFFFFFD, 0, 0]:
                raise AssertionError('Common initialization prefix/clear arguments differ')
            write(DESCRIPTOR, bytes(96))
        elif name == 'cache-flush':
            if arguments[:2] != [DESCRIPTOR, 96] or bytes(uc.mem_read(DESCRIPTOR, 96)) != bytes(96):
                raise AssertionError('Cache provider called before descriptor clear')
        elif name == 'copy-header':
            if arguments[:3] != [SOURCE_HEADER, DESTINATION_HEADER, 352]:
                raise AssertionError('Header copy arguments differ')
            write(DESTINATION_HEADER, bytes(uc.mem_read(SOURCE_HEADER, 352)))
        elif name == 'thread-create':
            stack_pointer = uc.reg_read(UC_ARM_REG_SP)
            if arguments != [THREAD, TASK, 0, RUNTIME] or [read(stack_pointer), read(stack_pointer + 4)] != [1024, 4]:
                raise AssertionError('Thread creation six-argument contract differs')
            if [read(BACKEND + offset) for offset in [0x14, 0x10, 0x110, 0x10C, 0x108, 0x118, 0x11C]] != [0, 0, 0, 0, 4, 0xFFFFFFFF, 0xFFFFFFFF]:
                raise AssertionError('Queue/priority/threshold initialization order differs')
            write(THREAD_STATE, struct.pack('<I', 2))
        elif name == 'thread-wake':
            if arguments[0] != THREAD or read(THREAD_STATE) != 2:
                raise AssertionError('Thread wake was not after its creation')
            write(THREAD_STATE, struct.pack('<I', 1))
        elif name == 'fifo-register':
            if arguments[:2] != [11, CALLBACK] or read(THREAD_STATE) != 1:
                raise AssertionError('FS FIFO callback registration differs')
            write(MODE, struct.pack('<H', second_mode))
        result = (seed ^ pc ^ (len(events) * 0x13579B)) & 0xFFFFFFFF
        for number, register in enumerate([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]):
            uc.reg_write(register, (result ^ (number * 0x1234567)) & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_CPSR, (seed & 15) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def observe_write(uc, access, address, size, value, data):
        if not any(start <= address and address + size <= start + length for start, length in [(PAGE, len(arena)), (HEADER, len(header)), (STACK, len(stack))]):
            raise AssertionError(('Common initializer wrote outside its explicit state windows', hex(address), size))
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    machine.emu_start(ADDRESS, STOP, count=2000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise AssertionError('Common initializer did not actually return within its bound')
    actual_registers = [machine.reg_read(register) for register in REGISTERS]
    if actual_registers[4:12] != registers[4:12] or actual_registers[-2] != registers[-2]:
        raise AssertionError('Common initializer did not restore preserved registers/SP')
    actual_arena = bytes(machine.mem_read(PAGE, len(arena)))
    actual_header = bytes(machine.mem_read(HEADER, len(header)))
    expected_arena, expected_header, plan = model(arena, header, second_mode)
    if actual_arena != expected_arena or actual_header != expected_header or events != plan:
        raise AssertionError(('Independent common initializer RAM/call model differs', events, plan))
    return {'registers': actual_registers, 'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'arena': actual_arena, 'header': actual_header, 'stack': bytes(machine.mem_read(STACK, len(stack))), 'events': events, 'writes': writes, 'visited': sorted(visited)}


def validate(arm, save, matches, root):
    if set(matches) != {'saved_20261029_card_common_initialize'}:
        raise AssertionError('The exact common initializer source is required')
    dependency = dependencies(root, arm)
    rows = [*matches.values(), dependency]
    rebuilt = {int(row['address'], 0): code for row, code in rows}
    native = {address: arm[address - 0x02000000:address - 0x02000000 + len(code)] for address, code in rebuilt.items()}
    rng = random.Random(20261029010004)
    cases, coverage, hashes = 0, set(), []
    mode_values = [*range(256), 0x100, 0x102, 0x7FFF, 0x8000, 0xFF02, 0xFFFE, 0xFFFF]

    def compare(arena, header, stack, seed, second_mode):
        registers = [rng.getrandbits(32) for unused in REGISTERS]
        registers[-2:] = [STACK + len(stack) - 16, STOP]
        flags = rng.getrandbits(4) << 28 | 0x10
        original = run(native, arena, header, stack, seed, second_mode, registers, flags)
        compiled = run(rebuilt, arena, header, stack, seed, second_mode, registers, flags)
        if original != compiled:
            raise AssertionError('Native/source common initializer effects differ')
        coverage.update(original['visited'])
        encoded = {**original, **{name: sha(original[name]) for name in ['arena', 'header', 'stack']}}
        hashes.append(sha(json.dumps(encoded, sort_keys=True).encode()))
        return original

    for first_mode in mode_values:
        for second_mode in [0, 2, 0xFFFF]:
            arena, header, stack = rng.randbytes(4096), bytearray(rng.randbytes(4096)), rng.randbytes(0x8000)
            struct.pack_into('<H', header, MODE - HEADER, first_mode)
            compare(arena, bytes(header), stack, cases, second_mode)
            cases += 1
    for seed in range(32):
        arena, header, stack = rng.randbytes(4096), bytearray(rng.randbytes(4096)), rng.randbytes(0x8000)
        struct.pack_into('<H', header, MODE - HEADER, 2 if seed & 1 else 0)
        for second_mode in [2, 0, 0xFFFF, 2]:
            result = compare(arena, bytes(header), stack, seed + 1000, second_mode)
            arena, header, stack = result['arena'], bytearray(result['header']), result['stack']
            cases += 1
    pcs = sorted(pc for pc in coverage if ADDRESS <= pc < ADDRESS + 244)
    if len(pcs) != 61:
        raise AssertionError('Common initializer native instruction coverage is incomplete')
    return {'cases': cases, 'nativeAndRecompiledCalls': cases * 2, 'verifiedReturn': True, 'instructionLimit': 2000, 'independentMachineStatePerExecution': True, 'stateSha256': hashes, 'nativeInstructionAddressesVisited': pcs, 'reusedAcceptedSources': [dependency[0]], 'sourceBodiesExecuted': len(rows), 'retainedNativeCalleeCodeBytes': 0, 'platformProviders': {hex(address): name for address, name in PROVIDERS.items()}, 'observations': ['The complete272-byte common initializer and previously accepted16-byte enable setter execute as separately linked recovered bodies.', 'Descriptor clearing, lock ownership/refcount, both queues, four-byte priority and both flush thresholds precede the measured dependent calls.', 'The initial full16-bit boot mode controls the352-byte header copy; the independently changed later mode controls enabling.', 'Thread creation receives the measured six arguments including task pointer,1024-byte stack size and priority4; registration uses channel11 and callback02011210.', 'Repeated initialization, full arena/header/stack effects, ordered writes, all architectural registers and actual return are compared.'], 'limitations': ['Clear/copy/cache, thread creation/wake and FIFO registration are explicit synthetic platform boundaries; their physical/hardware semantics are not claimed.', 'No task-thread body, callback body, timing, IRQ scheduling, backup-device protocol or concurrent initializer safety is established.', 'Existing16-byte enable setter earns no additional recovered-source credit.']}
