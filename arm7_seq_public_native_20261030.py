import hashlib
import random
from pathlib import Path
from collections import Counter
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
import arm7_seq_neighbor_native_20261030 as lower
import arm7_seq_access_native_20261030 as access
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
PLAYERS, SHARED = 0x03808420, 0x03807EDC
SIZES = {0x038002F0: 28, 0x03800340: 84, 0x0380039C: 116, 0x038004E0: 104,
    0x0380054C: 108, 0x038005BC: 136, 0x038006A4: 64, 0x038006E8: 152}
RANGES = dict(access.RANGES, **{})
RANGES.update(SIZES)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases(address):
    base = {'player': 0, 'flags': 0xA5, 'pattern': 'two', 'count': 1, 'kind': 0, 'active': 1,
        'mask': 0x8001, 'mode': 0, 'flag': 0, 'shared': True, 'channels': 0xABCD1234,
        'offset': 4, 'data': 0x87654321, 'size': 4, 'bounds': [0x023C0300, 0x023C0300],
        'playerPattern': 'one', 'passes': 1}
    result = []
    def add(**changes):
        result.append(dict(base, trackFlags=(0, 1, 128, 255)[len(result) % 4], **changes))
    patterns, masks = ('empty', 'one', 'last', 'two', 'duplicate'), (0, 1, 2, 0x8000, 0x8001, 0xFFFF, 0x10000, 0xFFFFFFFF)
    if address == 0x038002F0:
        for player in (0, 15):
            for flags in range(256):
                add(player=player, flags=flags)
    elif address == 0x03800340:
        for flags in (0, 1, 128, 255):
            for shared in (False, True):
                for pattern in patterns:
                    for count in (0, 3):
                        add(flags=flags, shared=shared, pattern=pattern, count=count)
    elif address == 0x0380039C:
        for flag in (0, 1, 2, 255, 256, 257, 0x80000000, 0xFFFFFFFF):
            for flags in (0, 1, 128, 255):
                for pattern in patterns:
                    for count in (0, 3):
                        add(flag=flag, flags=flags, pattern=pattern, count=count)
    elif address == 0x038004E0:
        for mode in (0, 1, 2, 3, 4, 0x80000000, 0xFFFFFFFF):
            for mask in masks:
                for pattern in patterns:
                    add(mode=mode, mask=mask, pattern=pattern)
    elif address == 0x0380054C:
        for channels in (0, 1, 0xFFFF, 0x10000, 0x80000000, 0xFFFFFFFF):
            for mask in masks:
                for pattern in patterns:
                    add(channels=channels, mask=mask, pattern=pattern)
    elif address == 0x038005BC:
        for bounds in ((0, 0), (0, 0xFFFFFFFF), (0x023C02FF, 0x023C02FF), (0x023C0300, 0x023C0300),
                (0x023C0300, 0x023C0301), (0x023C0301, 0x023C0301), (0xFFFFFFFF, 0xFFFFFFFF), (0x023C0301, 0x023C0300)):
            for player_pattern in ('none', 'one', 'last', 'three'):
                for pattern in patterns:
                    add(bounds=list(bounds), playerPattern=player_pattern, pattern=pattern)
    elif address in (0x038006A4, 0x038006E8):
        for size in (0, 1, 2, 3, 4, 0x80000000, 0xFFFFFFFF):
            for data in (0, 255, 256, 0x80000000, 0xFFFFFFFF):
                for offset in (0, 4, 32):
                    serial = len(result)
                    add(size=size, data=data, offset=offset, player=15 if serial % 2 else 0,
                        mask=masks[serial % len(masks)], pattern=patterns[serial % len(patterns)])
        if address == 0x038006E8:
            for mask in masks:
                for pattern in patterns:
                    for size in (1, 2, 4):
                        add(mask=mask, pattern=pattern, size=size, offset=28)
    else:
        raise ValueError('Unknown SDK public API')
    add(player=15, mode=3, flag=256, count=3, passes=2)
    return result


def setup(entry, case, seed):
    common = dict(lower.cases(0x03800B00)[0], count=case['count'], kind=case['kind'], active=case['active'], pattern=case['pattern'])
    common.update({key: case[key] for key in ('cycle', 'badNext') if key in case})
    ram, wram, unused = lower.setup({'address': '0x3800b00'}, common, seed)
    state = memory.Model(ram, wram)
    address = int(entry['address'], 0)
    template = bytes(state.regions[memory.DATA][memory.PLAYER - memory.DATA:memory.PLAYER - memory.DATA + 36])
    for index in range(16):
        for offset, value in enumerate(template):
            state.put(PLAYERS + index * 36 + offset, 1, value)
        state.put(PLAYERS + index * 36, 1, 0)
        state.put(PLAYERS + index * 36 + 1, 1, index)
    selected = PLAYERS + (case['player'] if 0 <= case['player'] < 16 else 0) * 36
    state.put(selected, 1, case['flags'])
    if address == 0x038005BC:
        for index in range(16):
            enabled = index in {'none': (), 'one': (0,), 'last': (15,), 'three': (0, 7, 15)}[case['playerPattern']]
            state.put(PLAYERS + index * 36, 1, case['flags'] if enabled else 0)
    for index in range(4):
        state.put(memory.TRACKS + index * 64, 1, case['trackFlags'])
        state.put(memory.TRACKS + index * 64 + 0x28, 4, 0x023C0300 if index == 0 else 0x023C0301)
    state.put(SHARED, 4, memory.DATA + 0x3000 if case['shared'] else 0)
    state.put(memory.DATA + 0x3004, 4, 0xA5A5A5A5)
    if address == 0x038002F0:
        arguments = [case['player']]
    elif address == 0x03800340:
        arguments = [case['player']]
    elif address == 0x0380039C:
        arguments = [case['player'], case['flag']]
    elif address == 0x038004E0:
        arguments = [case['player'], case['mask'], case['mode']]
    elif address == 0x0380054C:
        arguments = [case['player'], case['mask'], case['channels']]
    elif address == 0x038005BC:
        arguments = list(case['bounds'])
    elif address == 0x038006A4:
        arguments = [case['player'], case['offset'], case['data'], case['size']]
    else:
        arguments = [case['player'], case['mask'], case['offset'], case['data'], case['size']]
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE]), arguments


def modeled(address, ram, wram, arguments):
    state = memory.Model(ram, wram)
    current = PLAYERS + arguments[0] * 36
    if address == 0x038002F0:
        state.put(current, 1, state.get(current, 1) | 2)
    elif address == 0x03800340:
        if state.get(current, 1) & 1:
            state.invoke(0x03800B00, [current, 0, 0])
            shared = state.get(SHARED, 4)
            if shared:
                state.put(shared + 4, 4, state.get(shared + 4, 4) & ~(1 << arguments[0]))
    elif address == 0x0380039C:
        flag = arguments[1]
        state.put(current, 1, state.get(current, 1) & ~4 | (flag & 1) << 2)
        if flag:
            for index in range(16):
                track = state.getter(current, index)
                if track:
                    state.release(track, current, 127)
                    state.free_chain(track)
    elif address in (0x038004E0, 0x0380054C, 0x038006E8):
        mask = arguments[1]
        for index in range(16):
            if mask & 1:
                track = state.getter(current, index)
                if track:
                    if address == 0x038004E0:
                        mode = arguments[2]
                        if mode == 0:
                            state.put(track, 1, state.get(track, 1) & ~4)
                        elif mode in (1, 2, 3):
                            state.put(track, 1, state.get(track, 1) | 4)
                            if mode in (2, 3):
                                state.release(track, current, 0xFFFFFFFF if mode == 2 else 127)
                            if mode == 3:
                                state.free_chain(track)
                    elif address == 0x0380054C:
                        state.put(track + 0x1E, 2, arguments[2])
                        state.put(track, 1, state.get(track, 1) | 128)
                    elif arguments[4] in (1, 2, 4):
                        state.put(track + arguments[2], arguments[4], arguments[3])
            mask >>= 1
            if not mask:
                break
    elif address == 0x038005BC:
        start, end = arguments
        for index in range(16):
            player = PLAYERS + index * 36
            if not state.get(player, 1) & 1:
                continue
            for slot in range(16):
                track = state.getter(player, slot)
                if track and start <= state.get(track + 0x28, 4) <= end:
                    state.invoke(0x03800B00, [player, 0, 0])
                    break
    elif address == 0x038006A4 and arguments[3] in (1, 2, 4):
        state.put(current + arguments[1], arguments[3], arguments[2])
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE]), state.writes


def execute(entry, body, case, seed, budget=100000):
    address = int(entry['address'], 0)
    ram, wram, arguments = setup(entry, case, seed)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first, size in ((memory.BASE, 0x14000), (memory.DATA, 0x4000), (memory.STACK, 0x4000), (memory.RETURN, 0x1000)):
        machine.mem_map(first, size)
    machine.mem_write(memory.BASE, wram)
    machine.mem_write(memory.DATA, ram)
    machine.mem_write(address, body)
    machine.mem_write(memory.STACK, random.Random(20261030 + seed).randbytes(0x4000))
    writes, visited, frames, returned_callees = [], set(), [], Counter()
    def code(cpu, pc, size, unused):
        while frames and pc == frames[-1][1]:
            returned_callees[frames.pop()[0]] += 1
        if not any(first <= pc < first + length for first, length in RANGES.items()):
            raise ValueError('SDK public API escaped qualified original code')
        if pc in RANGES:
            frames.append((pc, cpu.reg_read(match_runtime.REGISTERS[-1])))
        visited.add(pc)
    def write(cpu, access_type, location, size, value, unused):
        if not memory.STACK <= location < memory.STACK + 0x4000:
            writes.append([location, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    states = []
    for phase in range(case['passes']):
        rng = random.Random(20261030 + seed + phase * 9000)
        registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
        registers[:min(4, len(arguments))] = arguments[:4]
        registers[-2:] = [memory.STACK + 0x3F00, memory.RETURN]
        if len(arguments) == 5:
            machine.mem_write(registers[-2], arguments[4].to_bytes(4, 'little'))
        machine.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            machine.reg_write(register, value)
        first_write, old_callees = len(writes), Counter(returned_callees)
        fault = None
        try:
            machine.emu_start(address, memory.RETURN, count=budget, timeout=200000)
        except UcError as error:
            fault = error.errno
        returned = machine.reg_read(UC_ARM_REG_PC) == memory.RETURN
        observed = [machine.reg_read(register) for register in match_runtime.REGISTERS]
        if returned:
            expected_ram, expected_wram, expected_writes = modeled(address, ram, wram, arguments)
            if writes[first_write:] != expected_writes or bytes(machine.mem_read(memory.DATA, 0x4000)) != expected_ram or bytes(machine.mem_read(memory.BASE, 0x14000)) != expected_wram:
                raise ValueError('Independent global-player/mask/store/list/whole-memory model differs')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or frames != [(address, memory.RETURN)]:
                raise ValueError('SDK public API root/nested return or saved-register ABI differs')
            ram, wram = expected_ram, expected_wram
            frames.clear()
        delta = returned_callees - old_callees
        states.append({'actualReturn': returned, 'fault': fault, 'pc': machine.reg_read(UC_ARM_REG_PC), 'registers': observed,
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'writes': writes[first_write:],
            'actualNestedReturns': {hex(key): value for key, value in sorted(delta.items())}, 'remainingFrames': [list(row) for row in frames],
            'ramSha256': digest(bytes(machine.mem_read(memory.DATA, 0x4000))), 'wramAndBssSha256': digest(bytes(machine.mem_read(memory.BASE, 0x14000))),
            'stackSha256': digest(bytes(machine.mem_read(memory.STACK, 0x4000)))})
        if not returned:
            break
    return {'states': states, 'visited': sorted(visited)}


def oracle(entry, original, rebuilt):
    address = int(entry['address'], 0)
    records, visited, outer, nested = [], set(), 0, Counter()
    for seed, case in enumerate(cases(address)):
        expected, actual = execute(entry, original, case, seed), execute(entry, rebuilt, case, seed)
        if expected != actual or any(not row['actualReturn'] or row['fault'] is not None for row in expected['states']):
            raise ValueError('SDK public original/source complete return/state differs')
        outer += len(expected['states']) * 2
        visited.update(expected['visited'])
        for state in expected['states']:
            nested.update({key: value * 2 for key, value in state['actualNestedReturns'].items()})
        records.append({'case': case, 'seed': seed, 'actualOriginalAndCompiledReturns': len(expected['states']) * 2,
            'stateSha256': digest(repr(expected).encode())})
    own = set(range(address, address + entry['codeBytes'], 4))
    if not own.issubset(visited):
        raise ValueError('SDK public own instruction coverage incomplete: ' + repr(sorted(own - visited)))
    controls = []
    unsupported = [('single-instruction-budget', {}, 1)]
    if address in (0x03800340, 0x0380039C, 0x038004E0, 0x038005BC):
        common = {'player': 0, 'flags': 1, 'pattern': 'one', 'mask': 1, 'mode': 2, 'flag': 1,
            'count': 3, 'bounds': [0, 0xFFFFFFFF], 'playerPattern': 'one'}
        unsupported.extend((('cyclic-list-budget', dict(common, cycle=True), 2000),
            ('malformed-next', dict(common, badNext=True), 2000)))
    elif address in (0x038006A4, 0x038006E8):
        unsupported.append(('unmapped-parameter-target', {'offset': 0x80000000, 'mask': 1, 'pattern': 'one', 'size': 4}, 2000))
    elif address == 0x038002F0:
        unsupported.append(('unmapped-player-target', {'player': 0x10000000}, 2000))
    for name, changed, limit in unsupported:
        case = dict(cases(address)[0], **changed)
        expected, actual = execute(entry, original, case, 0, limit), execute(entry, rebuilt, case, 0, limit)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Unsupported SDK public path received return credit')
        controls.append({'name': name, 'returnCredit': 0, 'state': expected})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': outer,
        'actualSeparatelyObservedNestedReturns': dict(nested), 'freshMachinePerScenario': True, 'instructionLimit': 100000,
        'timeoutMicroseconds': 200000, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate', 'allOwnInstructionAddressesVisited': sorted(own),
        'independentGlobalPlayerMasksWidthsAndListEffectsModel': True, 'providerReplacements': [],
        'records': records, 'unsupportedControls': controls, 'unsupportedReturnCredit': 0, 'calleeSourceCredit': 0,
        'returnContract': 'void; incidental R0 compared only as machine state',
        'limitations': ['Synthetic player indices0..15 and bounded mapped aligned parameter offsets only; no caller validity or extent claim',
            'No physical audio, scene reachability, synchronization or gameplay meanings are inferred',
            'Original lower callees/BSS/data receive zero reconstructed-source credit from these callers']}
