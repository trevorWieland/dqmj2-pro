import hashlib
import random
from pathlib import Path
from collections import Counter
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
import arm7_seq_neighbor_native_20261030 as previous_native
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SHARED = 0x03807EDC
RANGES = dict(previous_native.RANGES, **{})
RANGES.update({0x03801840: 64, 0x03801884: 64, 0x038018C8: 128})


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address):
    result = []
    if address == 0x03801840:
        for pointer in (0, memory.DATA + 0x3000, 1, 0xFFFFFF00):
            for index in (0, 1, 15, 16, 17, 31, 32, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF):
                for player_id in (0, 1, 15, 127, 255):
                    result.append({'pointer': pointer, 'index': index, 'playerId': player_id,
                        'invalidPlayer': pointer == 0 or memory.signed(index) >= 16, 'passes': 1})
    elif address == 0x03801884:
        for first in range(33):
            for inactive in (0, 2, 128, 254):
                for active in (1, 3, 129, 255):
                    result.append({'firstFree': first, 'inactive': inactive, 'active': active, 'passes': 1})
        result.append({'firstFree': 0, 'inactive': 128, 'active': 255, 'secondFree': 31, 'passes': 3})
    elif address == 0x038018C8:
        for mode in (0, 1, 2, 3, 4, 0x101, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF):
            for count in (0, 1, 3):
                for kind in (0, 3):
                    for active in (0, 1, 128, 255):
                        result.append({'mode': mode, 'count': count, 'kind': kind, 'active': active, 'passes': 1})
        for mode in range(4):
            result.append({'mode': mode, 'count': 3, 'kind': 0, 'active': 1, 'passes': 2})
    else:
        raise ValueError('Unknown ordinary SDK state-access unit')
    return result


def setup(entry, case, seed):
    common = dict(previous_native.cases(0x038009E0)[0], count=case.get('count', 0), kind=case.get('kind', 0), active=case.get('active', 0))
    common.update({key: case[key] for key in ('cycle', 'badNext') if key in case})
    ram, wram, unused = previous_native.setup({'address': '0x38009e0'}, common, seed)
    initial = memory.Model(ram, wram)
    address = int(entry['address'], 0)
    if address == 0x03801840:
        initial.put(SHARED, 4, case['pointer'])
        initial.put(memory.PLAYER + 1, 1, case['playerId'])
        arguments = [0x03000000 if case['invalidPlayer'] else memory.PLAYER, case['index'], 0]
    elif address == 0x03801884:
        for index in range(32):
            initial.put(memory.TRACKS + index * 64, 1, case['active'])
        for index in (case['firstFree'], case.get('secondFree', 32)):
            if index < 32:
                initial.put(memory.TRACKS + index * 64, 1, case['inactive'])
        arguments = [0x12345678, 0x80000000, 0xFFFFFFFF]
    else:
        arguments = [memory.TRACK, memory.PLAYER, case['mode']]
    return bytes(initial.regions[memory.DATA]), bytes(initial.regions[memory.BASE]), arguments


def modeled(address, ram, wram, arguments):
    state = memory.Model(ram, wram)
    result = None
    if address == 0x03801840:
        player, index, unused = arguments
        pointer = state.get(SHARED, 4)
        if pointer == 0:
            result = 0
        elif memory.signed(index) < 16:
            result = (pointer + 0x20 + state.get(player + 1, 1) * 36 + index * 2) & 0xFFFFFFFF
        else:
            result = (pointer + 0x260 + (index - 16) * 2) & 0xFFFFFFFF
    elif address == 0x03801884:
        result = 0xFFFFFFFF
        for index in range(32):
            flags = state.get(memory.TRACKS + index * 64, 1)
            if not flags & 1:
                state.put(memory.TRACKS + index * 64, 1, flags & ~1 | 1)
                result = index
                break
    else:
        track, player, mode = arguments
        if mode == 0:
            state.put(track, 1, state.get(track, 1) & ~4)
        elif mode in (1, 2, 3):
            state.put(track, 1, state.get(track, 1) | 4)
            if mode in (2, 3):
                state.release(track, player, 0xFFFFFFFF if mode == 2 else 127)
            if mode == 3:
                state.free_chain(track)
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE]), state.writes, result


def execute(entry, body, case, seed, budget=30000):
    address = int(entry['address'], 0)
    ram, wram, arguments = setup(entry, case, seed)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first, size in ((memory.BASE, 0x14000), (memory.DATA, 0x4000), (memory.STACK, 0x4000), (memory.RETURN, 0x1000)):
        machine.mem_map(first, size)
    machine.mem_write(memory.BASE, wram)
    machine.mem_write(memory.DATA, ram)
    machine.mem_write(address, body)
    stack = random.Random(20261030 + seed).randbytes(0x4000)
    machine.mem_write(memory.STACK, stack)
    writes, visited, frames, returned_callees = [], set(), [], Counter()
    def code(cpu, pc, size, unused):
        while frames and pc == frames[-1][1]:
            returned_callees[frames.pop()[0]] += 1
        if not any(first <= pc < first + length for first, length in RANGES.items()):
            raise ValueError('SDK state accessor escaped own/qualified original ranges')
        if pc in RANGES:
            frames.append((pc, cpu.reg_read(match_runtime.REGISTERS[-1])))
        visited.add(pc)
    def write(cpu, access, location, size, value, unused):
        if not memory.STACK <= location < memory.STACK + 0x4000:
            writes.append([location, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    states = []
    for phase in range(case['passes']):
        rng = random.Random(20261030 + seed + phase * 9000)
        registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
        registers[:3], registers[-2:] = arguments, [memory.STACK + 0x3F00, memory.RETURN]
        machine.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            machine.reg_write(register, value)
        first_write, old_callees = len(writes), Counter(returned_callees)
        fault = None
        try:
            machine.emu_start(address, memory.RETURN, count=budget, timeout=100000)
        except UcError as error:
            fault = error.errno
        returned = machine.reg_read(UC_ARM_REG_PC) == memory.RETURN
        observed = [machine.reg_read(register) for register in match_runtime.REGISTERS]
        if returned:
            expected_ram, expected_wram, expected_writes, expected_result = modeled(address, ram, wram, arguments)
            if writes[first_write:] != expected_writes or bytes(machine.mem_read(memory.DATA, 0x4000)) != expected_ram or bytes(machine.mem_read(memory.BASE, 0x14000)) != expected_wram:
                raise ValueError('Independent state pointer/bit-plane/list/whole RAM/BSS/ordered-store model differs')
            if expected_result is not None and observed[0] != expected_result:
                raise ValueError('Independent full-word pointer or signed first-free sentinel model differs')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or frames != [(address, memory.RETURN)]:
                raise ValueError('SDK state accessor root/nested return or saved-register ABI differs')
            ram, wram = expected_ram, expected_wram
            frames.clear()
        delta = returned_callees - old_callees
        states.append({'actualReturn': returned, 'fault': fault, 'pc': machine.reg_read(UC_ARM_REG_PC), 'registers': observed,
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'writes': writes[first_write:], 'actualNestedReturns': {hex(key): value for key, value in sorted(delta.items())},
            'remainingFrames': [list(row) for row in frames], 'ramSha256': digest(bytes(machine.mem_read(memory.DATA, 0x4000))),
            'wramAndBssSha256': digest(bytes(machine.mem_read(memory.BASE, 0x14000))), 'stackSha256': digest(bytes(machine.mem_read(memory.STACK, 0x4000)))})
        if not returned:
            break
    return {'states': states, 'visited': sorted(visited)}


def oracle(entry, original, rebuilt):
    address = int(entry['address'], 0)
    records, visited, outer, nested = [], set(), 0, Counter()
    for seed, case in enumerate(cases(address)):
        expected, actual = execute(entry, original, case, seed), execute(entry, rebuilt, case, seed)
        if expected != actual or any(not row['actualReturn'] or row['fault'] is not None for row in expected['states']):
            raise ValueError('State accessor original/source complete return/register/flags/memory effects differ')
        outer += len(expected['states']) * 2
        visited.update(expected['visited'])
        for state in expected['states']:
            nested.update({key: value * 2 for key, value in state['actualNestedReturns'].items()})
        records.append({'case': case, 'seed': seed, 'actualOriginalAndCompiledReturns': len(expected['states']) * 2,
            'results': [row['registers'][0] for row in expected['states']], 'stateSha256': digest(repr(expected).encode())})
    own = set(range(address, address + entry['codeBytes'], 4))
    if not own.issubset(visited):
        raise ValueError('SDK state accessor own instruction coverage incomplete')
    controls = []
    if address == 0x038018C8:
        for name, changed in (('cycle-budget', {'cycle': True}), ('malformed-next', {'badNext': True})):
            case = dict(cases(address)[0], count=3, mode=2, **changed)
            expected, actual = execute(entry, original, case, 0, 2000), execute(entry, rebuilt, case, 0, 2000)
            if expected != actual or any(row['actualReturn'] for row in expected['states']):
                raise ValueError('Unsupported state-mode path received return credit')
            controls.append({'name': name, 'returnCredit': 0, 'state': expected})
    expected, actual = execute(entry, original, cases(address)[0], 0, 1), execute(entry, rebuilt, cases(address)[0], 0, 1)
    if expected != actual or any(row['actualReturn'] for row in expected['states']):
        raise ValueError('Exhausted SDK state accessor received return credit')
    controls.append({'name': 'single-instruction-budget', 'returnCredit': 0, 'state': expected})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': outer,
        'actualSeparatelyObservedNestedReturns': dict(nested), 'freshMachinePerScenario': True, 'instructionLimit': 30000,
        'timeoutMicroseconds': 100000, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate', 'allOwnInstructionAddressesVisited': sorted(own),
        'independentPointerIndexFirstFreeAndModeEffectsModel': True, 'originalCalleesExecuted': True, 'providerReplacements': [],
        'records': records, 'unsupportedControls': controls, 'unsupportedReturnCredit': 0, 'calleeSourceCredit': 0,
        'returnContract': ('s16* raw address; returned storage validity and dereference are not claimed' if address == 0x03801840 else
            'int first free index0..31 or full-word signed -1' if address == 0x03801884 else 'void; incidental R0 compared only as machine state'),
        'limitations': ['Bounded synthetic SDK contexts; no caller validity/ownership/physical audio or gameplay meaning inferred',
            'Returned out-of-range pointers are compared as raw addresses only, not dereferenced or declared valid storage',
            'Negative modes/defaults and full signed indices are measured; cycle/fault/budget paths have zero return/error-result credit']}
