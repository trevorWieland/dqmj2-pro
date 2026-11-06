import hashlib
import random
import struct
from pathlib import Path
import match_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
BASE, DATA, STACK, RETURN = 0x037F8000, 0x023C0000, 0x023E0000, 0x023FF000
TRACK, PLAYER, NODES, TABLE, CALLEE = DATA + 0x100, DATA + 0x200, DATA + 0x1000, 0x0380704C, 0x037FF934
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def signed(value, bits):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> (bits - 1) else value


def cases():
    base = {'volume': 127, 'expression': 127, 'playerVolume': 127, 'panRange': 127, 'pan': 0, 'extPan': 0,
        'pitchBend': 0, 'bendRange': 0, 'extPitch': 0, 'extFader': 0, 'playerFader': 0, 'release': 0,
        'nodeCount': 1, 'kind': 0, 'length': 1, 'passes': 1, 'contextClass': 'bounded-synthetic-no-caller-validity-claim'}
    result = []
    def add(**changes):
        result.append(dict(base, **changes))
    for key in ('volume', 'expression', 'playerVolume'):
        for index in range(128):
            add(**{key: index})
        for index in (128, 129, 192, 255):
            add(**{key: index, 'contextClass': 'adjacent-initialized-memory-not-verified-table-or-caller-input'})
    for volume, expression, player in ((0, 0, 0), (0, 0, 127), (1, 1, 1), (127, 127, 127), (128, 128, 128), (255, 255, 255)):
        add(volume=volume, expression=expression, playerVolume=player,
            contextClass='adjacent-initialized-memory-not-verified-table-or-caller-input' if max(volume, expression, player) >= 128 else base['contextClass'])
    for scale in (0, 1, 126, 127, 128, 255):
        for pan in (-128, -1, 0, 1, 127):
            for extra in (-128, -1, 0, 1, 127):
                add(panRange=scale, pan=pan, extPan=extra)
    for bend in (-128, -1, 0, 1, 127):
        for scale in (0, 1, 127, 128, 255):
            for extra in (-32768, -1, 0, 32767):
                add(pitchBend=bend, bendRange=scale, extPitch=extra)
    for left in (-32768, -1, 0, 1, 32767):
        for right in (-32768, -1, 0, 1, 32767):
            add(extFader=left, playerFader=right)
    for count in (0, 1, 3):
        for kind in (0, 3, 255):
            for length in (0, 1, 0x100, 0xFFFFFFFF):
                for release in (0, 1, 0x80000000, 0xFFFFFFFF):
                    add(nodeCount=count, kind=kind, length=length, release=release)
    for flags in range(16):
        add(nodeCount=3, kind=0, length=0, release=1, passes=2, flags=flags)
    return result


def initial_data(case, seed):
    data = bytearray(random.Random(20261030 + seed).randbytes(0x4000))
    def put(address, size, value):
        offset = address - DATA
        data[offset:offset + size] = (value & ((1 << (size * 8)) - 1)).to_bytes(size, 'little')
    for offset, key in ((1, 'panRange'), (4, 'volume'), (5, 'expression'), (6, 'pitchBend'), (7, 'bendRange'), (8, 'pan'), (9, 'extPan')):
        put(TRACK + offset, 1, case[key])
    for offset, key in ((10, 'extFader'), (12, 'extPitch')):
        put(TRACK + offset, 2, case[key])
    put(PLAYER + 5, 1, case['playerVolume'])
    put(PLAYER + 6, 2, case['playerFader'])
    put(TRACK + 0x3C, 4, NODES if case['nodeCount'] else 0)
    for index in range(case['nodeCount']):
        node = NODES + index * 0x100
        put(node + 2, 1, case['kind'] if index == 0 else (3 if index == 1 else 255))
        put(node + 0x34, 4, case['length'] if index == 0 else (0 if index == 1 else 0x100))
        put(node + 0x50, 4, node + 0x100 if index + 1 < case['nodeCount'] else 0)
    if case.get('cycle'):
        put(NODES + 0x50, 4, NODES)
    if case.get('badNext'):
        put(NODES + 0x50, 4, 0x03000000)
    return bytes(data)


def modeled_pass(current, raw, release):
    data, writes, table_reads = bytearray(current), [], []
    def get(address, size, is_signed=False):
        return int.from_bytes(data[address - DATA:address - DATA + size], 'little', signed=is_signed)
    def put(address, size, value):
        value &= (1 << (size * 8)) - 1
        data[address - DATA:address - DATA + size] = value.to_bytes(size, 'little')
        writes.append([address, size, value])
    indices = [get(TRACK + 4, 1), get(TRACK + 5, 1), get(PLAYER + 5, 1)]
    values = []
    for index in indices:
        target = TABLE + index * 2
        values.append(int.from_bytes(raw[target - BASE:target - BASE + 2], 'little', signed=True))
        table_reads.append([target, 2])
    volume_sum = sum(values)
    fader_sum = get(TRACK + 10, 2, True) + get(PLAYER + 6, 2, True)
    volume, fader = max(-32768, volume_sum), max(-32768, fader_sum)
    pitch = get(TRACK + 12, 2, True) + ((get(TRACK + 6, 1, True) * (get(TRACK + 7, 1) << 6)) >> 7)
    pan, scale = get(TRACK + 8, 1, True), get(TRACK + 1, 1)
    if scale != 127:
        pan = (pan * scale + 64) >> 7
    pan += get(TRACK + 9, 1, True)
    unclamped_pan = pan
    pan = max(-128, min(127, pan))
    node, released, skipped = get(TRACK + 0x3C, 4), 0, 0
    while node:
        put(node + 6, 2, fader)
        if get(node + 2, 1) != 3:
            put(node + 12, 2, volume)
            put(node + 14, 2, pitch)
            put(node + 11, 1, pan)
            put(node + 4, 1, scale)
            for offset in (0, 2, 4):
                put(node + 0x28 + offset, 2, get(TRACK + 0x18 + offset, 2))
            if get(node + 0x34, 4) == 0 and release != 0:
                put(node + 0x22, 1, 1)
                put(node + 2, 1, 3)
                released += 1
        else:
            skipped += 1
        node = get(node + 0x50, 4)
    return bytes(data), writes, table_reads, {'volumeLowClamp': volume_sum < -32768, 'faderLowClamp': fader_sum < -32768,
        'panLowClamp': unclamped_pan < -128, 'panHighClamp': unclamped_pan > 127, 'scaleBypass': scale == 127,
        'released': released, 'skippedType3': skipped}


def execute(entry, body, case, seed, budget=10000):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Measured ARM7 WRAM input differs')
    address = int(entry['address'], 0)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first, length in ((BASE, 0x10000), (DATA, 0x4000), (STACK, 0x4000), (RETURN, 0x1000)):
        machine.mem_map(first, length)
    machine.mem_write(BASE, raw)
    machine.mem_write(address, body)
    current = initial_data(case, seed)
    machine.mem_write(DATA, current)
    stack = bytearray(random.Random(20261031 + seed).randbytes(0x4000))
    machine.mem_write(STACK, bytes(stack))
    writes, table_reads, visited, nested, pending = [], [], set(), [0], [False]
    def code(cpu, pc, length, unused):
        if not (address <= pc < address + entry['bytes'] - 4 or CALLEE <= pc < CALLEE + 12):
            raise ValueError('Track update left complete body/qualified real 12-byte setter')
        if pc == CALLEE:
            if pending[0] or cpu.reg_read(match_runtime.REGISTERS[0]) < NODES:
                raise ValueError('Unexpected nested native setter ABI')
            pending[0] = True
        if pc == 0x03800CD8 and pending[0]:
            pending[0] = False
            nested[0] += 1
        visited.add(pc)
    def write(cpu, access, location, size, value, unused):
        writes.append([location, size, value & ((1 << (size * 8)) - 1)])
    def read(cpu, access, location, size, value, unused):
        if TABLE <= location < TABLE + 512:
            table_reads.append([location, size])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.hook_add(UC_HOOK_MEM_READ, read)
    states = []
    for iteration in range(case['passes']):
        rng = random.Random(20261030 + seed + iteration * 9000)
        registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
        registers[:3] = [TRACK, PLAYER, case['release']]
        registers[-2:] = [STACK + 0x3F00, RETURN]
        before = list(registers)
        machine.reg_write(UC_ARM_REG_CPSR, case.get('flags', seed % 16) << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            machine.reg_write(register, value)
        first_write, first_read, first_nested = len(writes), len(table_reads), nested[0]
        fault = None
        try:
            machine.emu_start(address, RETURN, count=budget, timeout=100000)
        except UcError as error:
            fault = error.errno
        returned = machine.reg_read(UC_ARM_REG_PC) == RETURN
        observed = [machine.reg_read(register) for register in match_runtime.REGISTERS]
        expected_tags = None
        if returned:
            expected, expected_writes, expected_reads, expected_tags = modeled_pass(current, raw, case['release'])
            frame = [[before[-2] - 40 + index * 4, 4, value] for index, value in enumerate(before[3:12] + [before[-1]])]
            stack[0x3F00 - 40:0x3F00] = struct.pack('<10I', *(before[3:12] + [before[-1]]))
            if writes[first_write:] != frame + expected_writes or table_reads[first_read:] != expected_reads:
                raise ValueError('Independent track signed-halfword/ordered store/table-read model differs')
            if bytes(machine.mem_read(DATA, 0x4000)) != expected or bytes(machine.mem_read(STACK, 0x4000)) != bytes(stack):
                raise ValueError('Independent track complete RAM/stack model differs')
            if observed[3:12] != before[3:12] or observed[-2:] != before[-2:] or machine.reg_read(UC_ARM_REG_CPSR) != 0x600000D3:
                raise ValueError('Actual track return/saved-register/final-flags ABI differs')
            if pending[0] or nested[0] - first_nested != expected_tags['released']:
                raise ValueError('Nested real native setter did not actually return')
            current = expected
        states.append({'actualReturn': returned, 'fault': fault, 'pc': machine.reg_read(UC_ARM_REG_PC), 'registers': observed,
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'writes': writes[first_write:], 'tableReads': table_reads[first_read:],
            'actualNestedSetterReturns': nested[0] - first_nested, 'modelTags': expected_tags,
            'ramSha256': digest(bytes(machine.mem_read(DATA, 0x4000))), 'stackSha256': digest(bytes(machine.mem_read(STACK, 0x4000))),
            'wramSha256': digest(bytes(machine.mem_read(BASE, 0x10000))), 'returnMapSha256': digest(bytes(machine.mem_read(RETURN, 0x1000)))})
        if not returned:
            break
    return {'states': states, 'visited': sorted(visited)}


def oracle(entry, original, rebuilt):
    records, visited, returns, nested = [], set(), 0, 0
    for index, case in enumerate(cases()):
        expected, actual = execute(entry, original, case, index), execute(entry, rebuilt, case, index)
        if expected != actual or not all(row['actualReturn'] and row['fault'] is None for row in expected['states']):
            raise ValueError('Actual original/source track return/state differs')
        visited.update(expected['visited'])
        own_count = len(expected['states']) * 2
        callee_count = sum(row['actualNestedSetterReturns'] for row in expected['states']) * 2
        returns += own_count
        nested += callee_count
        records.append({'case': case, 'seed': index, 'actualOriginalAndCompiledReturns': own_count, 'actualNestedSetterReturns': callee_count,
            'modelTags': [row['modelTags'] for row in expected['states']], 'stateSha256': digest(repr(expected).encode())})
    own = set(range(int(entry['address'], 0), int(entry['address'], 0) + entry['bytes'] - 4, 4))
    if not own.issubset(visited) or not set(range(CALLEE, CALLEE + 12, 4)).issubset(visited):
        raise ValueError('Track own/callee instruction coverage incomplete')
    controls = []
    for name, changes in (('cycle-instruction-budget', {'cycle': True}), ('malformed-next-pointer', {'badNext': True})):
        case = dict(cases()[0], **changes)
        expected, actual = execute(entry, original, case, 0, 256), execute(entry, rebuilt, case, 0, 256)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Unsupported linked-list path received return credit')
        controls.append({'name': name, 'returnCredit': 0, 'state': expected})
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': returns,
        'actualSeparatelyObservedNestedSetterReturns': nested, 'freshMachinePerScenario': True,
        'instructionLimit': 10000, 'timeoutMicroseconds': 100000, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate; not physical ARM7 timing/peripherals',
        'independentSignedArithmeticWholeRamStackOrderedStoreModel': True,
        'records': records, 'allOwnInstructionAddressesVisited': sorted(own), 'unsupportedControls': controls, 'unsupportedReturnCredit': 0,
        'qualifiedNativeCallee': {'processor': 'arm7', 'program': '', 'module': 'arm7-wram', 'address': hex(CALLEE), 'mode': 'arm',
            'bytes': 12, 'sha256': digest(raw[CALLEE - BASE:CALLEE - BASE + 12]), 'providerReplacement': False, 'sourceCredit': 0},
        'inputTable': {'address': hex(TABLE), 'referenceClaimedEntries': 128, 'entryBytes': 2, 'signed': True,
            'native128EntrySha256': digest(raw[TABLE - BASE:TABLE - BASE + 256]), 'adjacent128WordSha256': digest(raw[TABLE - BASE + 256:TABLE - BASE + 512]),
            'originalDataSourceCredit': 0, 'above127CallerValidity': 'unproved-adjacent-initialized-memory-probes-only'},
        'returnContract': 'void; raw R0 is compared as machine state but receives no semantic result meaning',
        'limitations': ['Disposable synthetic track/player/channel state, no physical sound or enclosing scene',
            'Reference names/layout are hypotheses independently checked against the target; same SDK version is not presumed',
            'Aliased track/player/channel objects and arbitrary invalid list contexts are not established valid caller inputs']}
