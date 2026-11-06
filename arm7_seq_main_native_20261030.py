import hashlib
import random
from pathlib import Path
from collections import Counter
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
import arm7_seq_public_native_20261030 as previous
import arm7_seq_main_model_20261030 as model
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS, CODE = 0x037FFF54, 344
RANGES = dict(previous.RANGES, **{})
RANGES.update({ADDRESS: CODE, 0x03800CF0: 2884})


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    base = {'step': 1, 'flags': 3, 'shared': True, 'player': 0, 'playerId': 0, 'players': 'one',
        'accumulator': 239, 'tempo': 120, 'ratio': 256, 'trackCase': 'waiting', 'pattern': 'one',
        'count': 0, 'kind': 0, 'active': 1, 'trackFlags': 1, 'wait': 0x100000, 'nodeLength': 0x100,
        'position': 0, 'positionLimit': 5, 'passes': 1}
    result = []
    def add(**changes):
        result.append(dict(base, **changes))
    for step in (0, 1, 2, 0x80000000, 0xFFFFFFFF):
        for flags in (0, 1, 2, 3, 4, 5, 6, 7, 128, 255):
            for shared in (False, True):
                add(step=step, flags=flags, shared=shared)
    for accumulator in (0, 1, 239, 240, 241, 480, 65535):
        for track_case in ('empty', 'null-current', 'waiting'):
            for pattern in ('empty', 'one', 'last', 'two', 'duplicate'):
                for count in (0, 3):
                    add(accumulator=accumulator, trackCase=track_case, pattern=pattern, count=count)
    for tempo, ratio, accumulator in ((0, 0, 0), (1, 256, 239), (65535, 65535, 65535), (32768, 32768, 1), (0, 65535, 65535)):
        for shared in (False, True):
            for player_id in (0, 15, 255):
                add(tempo=tempo, ratio=ratio, accumulator=accumulator, shared=shared, player=15, playerId=player_id, count=1)
    for length, position, limit in ((0, 0, 5), (1, 1, 5), (0x7FFFFFFF, 0x7FFFFFFF, 0x7FFFFFFF),
            (0x80000000, 0x80000000, 0), (0xFFFFFFFF, 0xFFFFFFFF, 0)):
        for count in (1, 3):
            for kind in (0, 3):
                for track_flags in (1, 17):
                    add(nodeLength=length, position=position, positionLimit=limit, count=count, kind=kind,
                        trackFlags=track_flags, accumulator=480)
    for players in ('one', 'last', 'three'):
        for track_case in ('empty', 'null-current', 'waiting'):
            add(players=players, trackCase=track_case, pattern='two', accumulator=480, count=3)
    for track_case in ('empty', 'null-current', 'waiting'):
        add(trackCase=track_case, accumulator=480, count=3, pattern='duplicate', passes=2)
    return result


def setup(case, seed):
    common = dict(previous.cases(0x03800340)[0], player=case['player'], flags=case['flags'], shared=False,
        pattern='empty' if case['trackCase'] == 'empty' else case['pattern'], count=case['count'], kind=case['kind'],
        active=case['active'], trackFlags=case['trackFlags'])
    common.update({key: case[key] for key in ('cycle', 'badNext') if key in case})
    ram, wram, unused = previous.setup({'address': '0x3800340'}, common, seed)
    state = model.Model(ram, wram)
    enabled = {'one': (case['player'],), 'last': (15,), 'three': (0, 7, 15)}[case['players']]
    for index in range(16):
        player = model.PLAYERS + index * 36
        state.put(player, 1, case['flags'] if index in enabled else 0)
        state.put(player + 1, 1, case['playerId'] if case['players'] == 'one' else index)
        for offset, value in ((0x18, case['tempo']), (0x1A, case['ratio']), (0x1C, case['accumulator'])):
            state.put(player + offset, 2, value)
    for index in range(4):
        track = memory.TRACKS + index * 64
        state.put(track + 0x28, 4, memory.DATA + 0x3000 if case['trackCase'] == 'waiting' else 0)
        state.put(track + 0x20, 4, case['wait'])
        node = state.get(track + 0x3C, 4)
        for position in range(case['count']):
            for offset, value in ((0x34, case['nodeLength']), (0x14, case['position']), (0x18, case['positionLimit'])):
                state.put(node + offset, 4, value)
            node = state.get(node + 0x50, 4)
    shared = memory.DATA + 0x400
    state.put(model.SHARED_POINTER, 4, shared if case['shared'] else 0)
    state.put(shared + 4, 4, 0xA5A5A5A5)
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE])


def execute(entry, body, case, seed, budget=2000000):
    ram, wram = setup(case, seed)
    mutable = bytearray(wram)
    mutable[ADDRESS - memory.BASE:ADDRESS - memory.BASE + len(body)] = body
    wram = bytes(mutable)
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base, size in ((memory.BASE, 0x14000), (memory.DATA, 0x4000), (memory.STACK, 0x4000), (memory.RETURN, 0x1000)):
        cpu.mem_map(base, size)
    cpu.mem_write(memory.BASE, wram)
    cpu.mem_write(memory.DATA, ram)
    cpu.mem_write(memory.STACK, random.Random(20261030 + seed).randbytes(0x4000))
    writes, visited, frames, completed, contracts = [], set(), [], Counter(), Counter()
    def code(machine, pc, size, unused):
        while frames and pc == frames[-1][1]:
            completed[frames.pop()[0]] += 1
        if not any(first <= pc < first + length for first, length in RANGES.items()):
            raise ValueError('Whole sequence caller escaped qualified original code')
        if pc == 0x03800DB4:
            raise model.UnsupportedScriptPath('Native sequence-byte boundary reached; no complete/error-result credit')
        if pc in RANGES:
            frames.append((pc, machine.reg_read(match_runtime.REGISTERS[-1])))
        if pc in (0x03800CF0, 0x03800A7C, 0x03800B00, 0x03800B98):
            first, second, third = [machine.reg_read(register) for register in match_runtime.REGISTERS[:3]]
            player = second if pc == 0x03800B98 else first
            if not model.PLAYERS <= player < model.PLAYERS + 16 * 36 or (player - model.PLAYERS) % 36:
                raise ValueError('Actual original caller dependency received an unqualified player pointer')
            if pc == 0x03800CF0 and second != 1 or pc == 0x03800A7C and not 0 <= second < 16:
                raise ValueError('Actual original step/getter argument contract differs')
            if pc == 0x03800B98 and (first not in [memory.TRACKS + index * 64 for index in range(4)] or third not in (0, 1)):
                raise ValueError('Actual original track-update pointer/release ABI differs')
            contracts[(pc, third if pc == 0x03800B98 else second if pc == 0x03800CF0 else 0)] += 1
        visited.add(pc)
    def write(machine, access, location, size, value, unused):
        if not memory.STACK <= location < memory.STACK + 0x4000:
            writes.append([location, size, value & ((1 << (size * 8)) - 1)])
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    states = []
    for phase in range(case['passes']):
        rng = random.Random(20261030 + seed + phase * 9000)
        registers = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
        registers[0], registers[-2:] = case['step'], [memory.STACK + 0x3F00, memory.RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            cpu.reg_write(register, value)
        first_write, old_completed, old_contracts = len(writes), Counter(completed), Counter(contracts)
        fault, boundary = None, None
        try:
            cpu.emu_start(ADDRESS, memory.RETURN, count=budget, timeout=2000000)
        except UcError as error:
            fault = error.errno
        except model.UnsupportedScriptPath as error:
            boundary = str(error)
        returned = cpu.reg_read(UC_ARM_REG_PC) == memory.RETURN
        observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if returned:
            predicted = model.Model(ram, wram)
            predicted.main(case['step'])
            if writes[first_write:] != predicted.writes or bytes(cpu.mem_read(memory.DATA, 0x4000)) != bytes(predicted.regions[memory.DATA]) or bytes(cpu.mem_read(memory.BASE, 0x14000)) != bytes(predicted.regions[memory.BASE]):
                raise ValueError('Independent complete caller/counter/tick/update/stop/global-state model differs')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or frames != [(ADDRESS, memory.RETURN)]:
                raise ValueError('Sequence caller full root/nested/saved-register ABI differs')
            ram, wram = bytes(predicted.regions[memory.DATA]), bytes(predicted.regions[memory.BASE])
            frames.clear()
        delta, argument_delta = completed - old_completed, contracts - old_contracts
        states.append({'actualReturn': returned, 'fault': fault, 'analysisBoundaryStop': boundary, 'pc': cpu.reg_read(UC_ARM_REG_PC),
            'registers': observed, 'cpsr': cpu.reg_read(UC_ARM_REG_CPSR), 'writes': writes[first_write:],
            'actualNestedReturns': {hex(key): value for key, value in sorted(delta.items())},
            'actualArgumentContracts': {hex(key[0]) + ':' + str(key[1]): value for key, value in sorted(argument_delta.items())},
            'remainingFrames': [list(row) for row in frames], 'ramSha256': digest(bytes(cpu.mem_read(memory.DATA, 0x4000))),
            'wramAndBssSha256': digest(bytes(cpu.mem_read(memory.BASE, 0x14000))), 'stackSha256': digest(bytes(cpu.mem_read(memory.STACK, 0x4000)))})
        if not returned:
            break
    return {'states': states, 'visited': sorted(visited)}


def oracle(entry, original, rebuilt):
    records, visited, returns, nested = [], set(), 0, Counter()
    for seed, case in enumerate(cases()):
        expected, actual = execute(entry, original, case, seed), execute(entry, rebuilt, case, seed)
        if expected != actual or any(not row['actualReturn'] or row['fault'] is not None or row['analysisBoundaryStop'] for row in expected['states']):
            raise ValueError('Sequence main native/rebuilt complete execution differs or failed actual return')
        returns += len(expected['states']) * 2
        visited.update(expected['visited'])
        for state in expected['states']:
            nested.update({key: count * 2 for key, count in state['actualNestedReturns'].items()})
        records.append({'case': case, 'seed': seed, 'actualOriginalAndCompiledReturns': len(expected['states']) * 2,
            'stateSha256': digest(repr(expected).encode()), 'argumentContracts': [row['actualArgumentContracts'] for row in expected['states']]})
    own = set(range(ADDRESS, ADDRESS + CODE, 4))
    if not own.issubset(visited):
        raise ValueError('Whole sequence caller own instruction coverage incomplete: ' + repr(sorted(own - visited)))
    controls = []
    active_case = dict(cases()[0], flags=3, step=1, shared=True, trackCase='waiting', pattern='one', players='one', player=0)
    for name, changes, count in (('single-instruction-budget', {}, 1), ('sequence-byte-boundary', {'wait': 1, 'accumulator': 240}, 2000000),
            ('cyclic-node-budget', {'cycle': True, 'count': 3, 'step': 0}, 2000), ('malformed-next', {'badNext': True, 'count': 3, 'step': 0}, 2000)):
        case = dict(active_case, **changes)
        expected, actual = execute(entry, original, case, 0, count), execute(entry, rebuilt, case, 0, count)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Unsupported whole sequence caller path received return credit')
        controls.append({'name': name, 'returnCredit': 0, 'supportedErrorResultCredit': 0, 'state': expected})
    return {'supported': True, 'verifiedReturn': True, 'vectors': len(records), 'actualOriginalAndCompiledReturns': returns,
        'actualSeparatelyObservedNestedReturns': dict(nested), 'freshMachinePerScenario': True,
        'instructionLimit': 2000000, 'timeoutMicroseconds': 2000000, 'cpuModel': 'Unicorn TI925T ARMv4T surrogate',
        'allOwnInstructionAddressesVisited': sorted(own), 'providerReplacements': [],
        'independentWholeCallerAndBoundedOriginalDependencyModel': True, 'records': records, 'unsupportedControls': controls,
        'unsupportedReturnCredit': 0, 'calleeSourceCredit': 0, 'returnContract': 'void; incidental R0 compared only as machine state',
        'limitations': ['Full caller returns only in synthetic empty/null-current/waiting-track contexts; qualified original callees remain zero-credit dependencies',
            'Sequence-byte interpretation at03800DB4 is an explicit unsupported analysis boundary, not a native error or return',
            'IDs255/shared-track aliases are raw adjacent/synthetic contexts, not ordinary-game validity/ownership evidence',
            'No physical audio, story, timing, area or renewal meaning is assigned; boundary migration remains a separate coordinator decision']}
