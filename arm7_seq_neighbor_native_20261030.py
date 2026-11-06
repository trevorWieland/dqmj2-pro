import hashlib
import random
from pathlib import Path
from collections import Counter
import match_runtime
import arm7_seq_neighbor_model_20261030 as model
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
RANGES = {0x038009E0: 104, 0x03800A48: 52, 0x03800A7C: 40, 0x03800AA8: 84, 0x03800B00: 56,
    0x03800B38: 96, 0x03800B98: 340, 0x037FF934: 12, 0x037FF940: 16, 0x037FF918: 28,
    0x037FFE64: 80, 0x037FFB1C: 20, 0x03806C38: 0x20C}
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address):
    base = {'count': 1, 'kind': 0, 'active': 1, 'release': 0xFFFFFFFF, 'index': 0, 'slot': 0,
        'selected': 0, 'status': 0, 'pattern': 'one', 'contextClass': 'bounded-synthetic; no enclosing caller-validity claim'}
    result = []
    def add(**changes):
        result.append(dict(base, **changes))
    if address == 0x038009E0:
        for count in (0, 1, 3):
            for kind in (0, 3):
                for active in (0, 1, 128, 255):
                    for release in (0xFFFFFFFF, 0, 1, 49, 50, 125, 126, 127, 128, 255, 0x80000000):
                        add(count=count, kind=kind, active=active, release=release,
                            contextClass='rate128-or255-bounded-malformed-context' if release in (128, 255) else base['contextClass'])
    elif address == 0x03800A48:
        for count in range(9):
            for active in (0, 1, 128, 255):
                add(count=count, active=active)
    elif address == 0x03800AA8:
        for index in range(16):
            for slot in (0, 3):
                for count in (0, 1, 3):
                    for active in (0, 1):
                        add(index=index, slot=slot, count=count, active=active)
            add(index=index, pattern='empty')
        for index in (16, 0x7FFFFFFF, 0xFFFFFFFF):
            add(index=index, contextClass='synthetic-index-bound-or-before-array-context')
    elif address == 0x03800B00:
        for pattern in ('empty', 'one', 'last', 'two', 'duplicate'):
            for count in (0, 1, 3):
                for active in (0, 1):
                    for kind in (0, 3):
                        add(pattern=pattern, count=count, active=active, kind=kind)
    elif address == 0x03800B38:
        for count in range(1, 6):
            for selected in (-1, 0, count // 2, count - 1):
                for status in (0, 1, 2, 0x101, 0x80000000, 0xFFFFFFFF):
                    add(count=count, selected=selected, status=status)
    else:
        raise ValueError('Unknown SDK neighbor native corpus')
    add(count=3, active=1, release=50, selected=1, status=1, contextReentry=True)
    return result


def setup(entry, case, seed):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Measured ARM7 WRAM input changed')
    wram = bytearray(0x14000)
    wram[:len(raw)] = raw
    ram = bytearray(random.Random(20261030 + seed).randbytes(0x4000))
    initial = model.Model(ram, wram)
    def put(address, size, value):
        initial.put(address, size, value)
    put(model.PLAYER, 1, 0xA5)
    put(model.PLAYER + 5, 1, 127)
    put(model.PLAYER + 6, 2, 0)
    for index in range(16):
        put(model.PLAYER + 8 + index, 1, 255)
    def track(address, number):
        for offset, value in ((0, 0xA5), (1, 255 if seed % 7 == 0 else 127), (4, 0 if seed % 11 == 0 else 127),
                (5, 0 if seed % 11 == 0 else 127), (6, 128 if seed % 3 == 0 else 127), (7, 255), (8, 128), (9, 127)):
            put(address + offset, 1, value)
        put(address + 10, 2, -32768 if seed % 2 else 32767)
        put(address + 12, 2, 32767)
        put(address + 0x3C, 4, model.NODES + number * 0x400 if case['count'] else 0)
        for index in range(case['count']):
            node = model.NODES + number * 0x400 + index * 0x80
            put(node + 2, 1, case['kind'] if index == 0 else (3 if index == 1 else 255))
            put(node + 3, 1, case['active'])
            put(node + 0x34, 4, 0x100)
            put(node + 0x48, 4, 0x12345678)
            put(node + 0x4C, 4, 0x80000000)
            put(node + 0x50, 4, node + 0x80 if index + 1 < case['count'] else 0)
        if case.get('cycle'):
            put(model.NODES + number * 0x400 + (case['count'] - 1) * 0x80 + 0x50, 4, model.NODES + number * 0x400)
        if case.get('badNext'):
            put(model.NODES + number * 0x400 + (case['count'] - 1) * 0x80 + 0x50, 4, 0x03000000)
    track(model.TRACK, 0)
    for number in range(4):
        track(model.TRACKS + number * 64, number)
    address = int(entry['address'], 0)
    if address in (0x03800AA8, 0x03800B00):
        if case['pattern'] == 'one' and case['index'] < 16:
            put(model.PLAYER + 8 + case['index'], 1, case['slot'])
        elif case['pattern'] == 'last':
            put(model.PLAYER + 23, 1, 0)
        elif case['pattern'] in ('two', 'duplicate'):
            put(model.PLAYER + 8, 1, 0)
            put(model.PLAYER + 23, 1, 0 if case['pattern'] == 'duplicate' else 3)
        if case['index'] == 0xFFFFFFFF:
            put(model.PLAYER + 7, 1, 255)
    if address == 0x038009E0:
        arguments = [model.TRACK, model.PLAYER, case['release']]
    elif address == 0x03800A48:
        arguments = [model.TRACK, 0, 0]
    elif address in (0x03800AA8, 0x03800B00):
        arguments = [model.PLAYER, case['index'], 0]
    else:
        selected = model.NODES + case['selected'] * 0x80 if case['selected'] >= 0 else model.DATA + 0x3800
        put(selected + 0x50, 4, 0)
        if 0 <= case['selected'] < case['count'] - 1:
            put(selected + 0x50, 4, selected + 0x80)
        arguments = [selected, case['status'], model.TRACK]
    return bytes(initial.regions[model.DATA]), bytes(initial.regions[model.BASE]), arguments


def execute(entry, body, case, seed, budget=30000, previous=None, capture=None):
    address = int(entry['address'], 0)
    ram, wram, arguments = setup(entry, case, seed)
    if previous is not None:
        ram, wram = previous['ram'], previous['wram']
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first, size in ((model.BASE, 0x14000), (model.DATA, 0x4000), (model.STACK, 0x4000), (model.RETURN, 0x1000)):
        machine.mem_map(first, size)
    machine.mem_write(model.BASE, wram)
    machine.mem_write(model.DATA, ram)
    machine.mem_write(address, body)
    stack = random.Random(20261031 + seed).randbytes(0x4000)
    machine.mem_write(model.STACK, stack)
    rng = random.Random(seed + 20261030)
    registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    registers[:3], registers[-2:] = arguments, [model.STACK + 0x3F00, model.RETURN]
    machine.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
    for register, value in zip(match_runtime.REGISTERS, registers):
        machine.reg_write(register, value)
    writes, visited, frames, completed = [], set(), [], Counter()
    def code(cpu, pc, size, unused):
        while frames and pc == frames[-1][1]:
            completed[frames.pop()[0]] += 1
        if not any(first <= pc < first + length for first, length in RANGES.items()):
            raise ValueError('SDK neighbor left qualified original code dependency ranges')
        if pc in RANGES:
            frames.append((pc, cpu.reg_read(match_runtime.REGISTERS[-1])))
        visited.add(pc)
    def write(cpu, access, location, size, value, unused):
        if not model.STACK <= location < model.STACK + 0x4000:
            writes.append([location, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    fault = None
    try:
        machine.emu_start(address, model.RETURN, count=budget, timeout=100000)
    except UcError as error:
        fault = error.errno
    returned = machine.reg_read(UC_ARM_REG_PC) == model.RETURN
    observed = [machine.reg_read(register) for register in match_runtime.REGISTERS]
    if returned:
        if frames != [(address, model.RETURN)] or observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:]:
            raise ValueError('SDK neighbor actual root/nested return or callee-saved ABI differs')
        expected = model.Model(ram, wram)
        expected.invoke(address, arguments)
        if writes != expected.writes or bytes(machine.mem_read(model.DATA, 0x4000)) != bytes(expected.regions[model.DATA]):
            raise ValueError('Independent SDK neighbor whole RAM/ordered effects model differs')
        if bytes(machine.mem_read(model.BASE, 0x14000)) != bytes(expected.regions[model.BASE]):
            raise ValueError('Independent SDK neighbor initialized/BSS state model differs')
    if capture is not None:
        capture.update(ram=bytes(machine.mem_read(model.DATA, 0x4000)), wram=bytes(machine.mem_read(model.BASE, 0x14000)))
    return {'actualReturn': returned, 'fault': fault, 'pc': machine.reg_read(UC_ARM_REG_PC), 'registers': observed,
        'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'writes': writes, 'visited': sorted(visited),
        'actualNestedReturns': {hex(key): value for key, value in sorted(completed.items())}, 'remainingFrames': frames,
        'ramSha256': digest(bytes(machine.mem_read(model.DATA, 0x4000))), 'wramAndBssSha256': digest(bytes(machine.mem_read(model.BASE, 0x14000))),
        'stackSha256': digest(bytes(machine.mem_read(model.STACK, 0x4000))), 'returnMapSha256': digest(bytes(machine.mem_read(model.RETURN, 0x1000)))}


def oracle(entry, original, rebuilt):
    address = int(entry['address'], 0)
    records, covered, nested = [], set(), Counter()
    for index, case in enumerate(cases(address)):
        previous_native, previous_source = None, None
        for phase in range(2 if case.get('contextReentry') else 1):
            captured_native, captured_source = {}, {}
            expected = execute(entry, original, case, index, previous=previous_native, capture=captured_native)
            actual = execute(entry, rebuilt, case, index, previous=previous_source, capture=captured_source)
            if expected != actual or not expected['actualReturn'] or expected['fault'] is not None:
                raise ValueError('SDK neighbor original/source full return/state differs')
            covered.update(expected['visited'])
            nested.update({key: value * 2 for key, value in expected['actualNestedReturns'].items()})
            records.append({'case': case, 'seed': index, 'persistentContextPhase': phase, 'actualOriginalAndCompiledReturns': 2,
                'actualNestedReturns': expected['actualNestedReturns'], 'stateSha256': digest(repr(expected).encode())})
            previous_native, previous_source = captured_native, captured_source
    own = set(range(address, address + entry['codeBytes'], 4))
    if not own.issubset(covered):
        raise ValueError('SDK neighbor own instruction coverage incomplete')
    controls = []
    for label, change in (('cyclic-list', {'cycle': True}), ('malformed-next', {'badNext': True})):
        case = dict(cases(address)[0], count=3, selected=-1, pattern='one', **change)
        expected, actual = execute(entry, original, case, 0, 2000), execute(entry, rebuilt, case, 0, 2000)
        if expected != actual or expected['actualReturn']:
            raise ValueError('SDK neighbor unsupported list path received return credit')
        controls.append({'name': label, 'returnCredit': 0, 'state': expected})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'actualSeparatelyObservedNestedReturns': dict(nested), 'freshMachinePerExecution': True,
        'instructionLimit': 30000, 'timeoutMicroseconds': 100000, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate',
        'allOwnInstructionAddressesVisited': sorted(own), 'independentWholeRamBssOrderedStoreModel': True,
        'originalCalleesExecuted': True, 'providerReplacements': [], 'calleeSourceCredit': 0,
        'contextReentry': 'One two-call persistent RAM/BSS scenario per unit, with an explicitly fresh caller CPU/stack state for each invocation',
        'records': records, 'unsupportedControls': controls, 'unsupportedReturnCredit': 0,
        'limitations': ['Synthetic mapped player/track/list contexts, no enclosing scene/physical sound/ownership claim',
            'Negative indices and release128/255 are bounded malformed-context probes, not valid ordinary inputs',
            'Original initialized lookup/global BSS state and qualified software-division block are zero-credit native dependencies',
            'Cycle/fault paths have no return/error-result credit; source API is void, incidental R0 is compared only as machine state']}
