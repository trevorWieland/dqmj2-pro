import hashlib
import random
from collections import Counter
from pathlib import Path
import match_runtime
import arm7_seq_prepare_native_20261030_62 as producer
import arm7_value_parse_native_20261030_63 as parser
import arm7_seq_neighbor_model_20261030 as memory
import arm7_player_step_model_20261030_64_v5 as independent
import arm7_note_on_native_20261030_60 as note_native
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS, SIZE, CODE = 0x03800CF0, 2896, 2884
RANGES = dict(producer.RANGES, **{})
RANGES.update(parser.RANGES)
RANGES.update(note_native.RANGES)
RANGES.update({0x037FF950: 440, 0x03801948: 384, 0x037FFB1C: 20, 0x037FF934: 12, 0x037FF940: 16})
RANGES[0x038009D0] = 16
RANGES[0x038007C0] = 48
RANGES[0x038018C8] = 128
RANGES[ADDRESS] = CODE
ARITIES = dict(producer.ARITIES, **{})
ARITIES.update(parser.ARITIES)
ARITIES.update(note_native.ARITIES)
ARITIES.update({0x037FF950: 5, 0x03801948: 4, 0x037FFB1C: 1, 0x037FF934: 1, 0x037FF940: 1})
ARITIES[0x038009D0] = 3
ARITIES[0x038007C0] = 1
ARITIES[0x038018C8] = 3
ARITIES[ADDRESS] = 2
PLAYER = 0x03808420
TRACK = 0x03808660


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    base = dict(stream=[255], notes=0, setFlags=0, clearFlags=0, wait=0, transpose=0, passes=1)
    result = []
    def add(**changes):
        result.append(dict(base, **changes))
    add()
    for wait in (1, 2, 127, 0x7FFFFFFF):
        add(wait=wait, passes=2)
    for note in (0, 60, 127):
        for length in (0, 1, 127):
            for transpose in (0, 127, 128, 255):
                add(stream=[note, 127, length, 255], transpose=transpose, passes=2)
    for notes in (0, 1, 2, 0xFFFFFFFF):
        add(stream=[60, 100, 1, 255], notes=notes, setFlags=4, passes=2)
    for opcode in (192, 193, 194, 195, 196, 197, 198, 199, 202, 203, 204, 205,
            206, 207, 208, 209, 210, 211, 213):
        for parameter in (0, 1, 127, 128, 255):
            add(stream=[opcode, parameter, 128, 1, 255])
    for opcode in (224, 225, 227):
        for parameter in (0, 1, 32767, 32768, 65535):
            add(stream=[opcode, parameter & 255, parameter >> 8, 128, 1, 255])
    for enabled in (True, False):
        for opcode, parameter in ((193, 0), (194, 255), (128, 1)):
            add(stream=[162, opcode, parameter, 255], clearFlags=0 if enabled else 64)
    for header in ([160, 128, 1, 0, 1, 0, 255], [161, 128, 0, 255]):
        add(stream=header)
    for kind in (1, 2, 3, 4):
        for note in (0, 60, 127):
            for length in (0, 1, 127):
                add(stream=[note, 100, length, 255], notes=1, positive=True, instrumentType=kind, passes=2)
    for opcode in (200, 201, 214, 215):
        for parameter in (0, 1, 2, 3, 127, 255):
            add(stream=[opcode, parameter, 128, 1, 255], passes=2)
    for count in (1, 2, 3):
        add(stream=[212, count, 193, 55, 252, 128, 1, 255], passes=2)
    add(stream=[148, 6, 0, 0, 193, 42, 128, 1, 255], passes=2)
    add(stream=[149, 8, 0, 0, 128, 1, 255, 255, 193, 42, 253], passes=2)
    add(stream=[253, 128, 1, 255], passes=2)
    add(stream=[252, 128, 1, 255], passes=2)
    for opcode in (149, 212):
        add(stream=[149, 8, 0, 0, 128, 1, 255, 255, 193, 42, 253] if opcode == 149 else [212, 3, 128, 1, 255], patches=[[TRACK+0x3B, 1, 3]], passes=2)
    for opcode in range(176, 190):
        for parameter in ((0, 1, 2, 15, 65535, 65521) if opcode == 181 else (0, 1, 32767, 32768, 65535)):
            prefix = [176, 0, 5, 0]
            add(stream=prefix+[opcode, 0, parameter & 255, parameter >> 8, 128, 1, 255], passes=2)
    for index in (0, 15, 16, 31, 255):
        add(stream=[176, index, 0x34, 0x12, 128, 1, 255], passes=2)
        add(stream=[176, index, 0x34, 0x12, 128, 1, 255], shared=False, passes=2)
    for patches in ([[TRACK+0x1E, 2, 0]], [[0x03807EB8, 4, 65535]], [[0x03807EBC, 4, 65535]], [[memory.DATA+0x1000+0x38, 4, 0]], [[memory.DATA+0x1000+0x18, 4, 0]], [[memory.DATA+0x1400+0x38, 4, 0]]):
        add(stream=[60, 100, 1, 255], notes=1, patches=patches, passes=2)
    for kind in (0, 5, 6, 15, 18, 255):
        add(stream=[60, 100, 1, 255], notes=1, instrumentType=kind, passes=2)
    for kind in (1, 2, 3, 4):
        for tie in (0, 1):
            add(stream=[200, tie, 60, 100, 1, 62, 90, 1, 128, 1, 255], notes=1, clearFlags=2, instrumentType=kind, passes=2)
        for envelope in (0, 50, 126, 127):
            add(stream=[208, envelope, 209, envelope, 210, envelope, 211, envelope, 60, 100, 1, 255], notes=1, instrumentType=kind, passes=2)
    for slot in (0, 1, 15, 16, 255):
        add(stream=[254, 3, 0, 147, slot, 12, 0, 0, 128, 1, 255, 255, 193, 77, 128, 1, 255], passes=2)
        add(stream=[254, 3, 0, 162, 147, slot, 13, 0, 0, 128, 1, 255, 255, 193, 77, 128, 1, 255], clearFlags=64, passes=2)
    for program in ([129, 0, 128, 1, 255], [129, 255, 255, 3, 128, 1, 255], [129, 128, 128, 4, 128, 1, 255], [161, 129, 0, 128, 1, 255]):
        add(stream=program, passes=2)
    for time in (1, 5, 255):
        for sweep in (0, 32767, 32768):
            add(stream=[201, 127, 207, time, 227, sweep & 255, sweep >> 8, 60, 100, 1, 255], notes=1, passes=2)
    for kind in (16, 17):
        for note in (0, 59, 60, 61, 62, 63, 127):
            for inner in (0, 1, 2, 3, 4):
                add(stream=[note, 100, 1, 255], notes=1, instrumentType=kind, innerType=inner, passes=2)
    add(stream=[214, 0, 128, 1, 255], patches=[[0x03807EC0, 4, 1]], passes=2)
    add(stream=[214, 255, 128, 1, 255], patches=[[0x03807EC0, 4, 1]], passes=2)
    for command in (130, 143, 144, 146, 150, 163, 175, 190, 191, 216, 223, 226, 239, 240, 251):
        category = command & 240
        operands = [0] if category in (128, 192, 208) else [0, 0] if category == 224 else [0, 0, 0] if category == 176 else []
        add(stream=[command]+operands+[128, 1, 255], passes=2)
    for stream in ([162, 129, 0, 128, 1, 255], [162, 148, 0, 0, 0, 128, 1, 255], [162, 149, 0, 0, 0, 128, 1, 255], [162, 255, 128, 1, 255], [162, 254, 128, 1, 255]):
        add(stream=stream, clearFlags=64, passes=2)
    for velocity in range(256):
        add(stream=[60, velocity, 1, 255], notes=1, passes=2)
    add(stream=[128, 1, 254, 128, 1, 255], passes=3)
    return result


def setup(case, seed):
    base = dict(producer.cases()[0], command=case['stream'][0], mask=0, shared=case.get('shared', True), bank=memory.DATA+0x1000)
    ram, wram, arguments = producer.setup(base, seed)
    state = independent.Model(ram, wram)
    for offset, value in enumerate(case['stream']):
        state.put(producer.STREAM+offset, 1, value)
    bank, archive, wave = [memory.DATA+offset for offset in (0x1000, 0x1400, 0x1800)]
    for index in range(16):
        channel = 0x03807EE0+index*84
        for offset, size, value in ((0, 1, index), (3, 1, 0), (0x22, 1, 0), (0x24, 2, 0), (0x48, 4, 0), (0x4C, 4, 0), (0x50, 4, 0)):
            state.put(channel+offset, size, value)
    kind = case.get('instrumentType', 1)
    state.put(bank+0x18, 4, archive)
    state.put(bank+0x38, 4, 1)
    state.put(bank+0x3C, 4, (0x200 << 8) | kind)
    low, high = (wave & 65535, wave >> 16) if kind == 4 else (0, 0)
    parameters = [low & 255, low >> 8, high & 255, high >> 8, 60, 127, 50, 127, 127, 64]
    for offset, value in enumerate(parameters):
        state.put(bank+0x200+offset, 1, value)
    if kind in (16, 17):
        inner = case.get('innerType', 1)
        params = list(parameters)
        if inner == 4:
            params[:4] = [wave & 255, wave >> 8 & 255, wave >> 16 & 255, wave >> 24]
        header = [60, 62] if kind == 16 else [0, 31, 63, 95, 127, 255, 255, 255]
        for offset, value in enumerate(header):
            state.put(bank+0x200+offset, 1, value)
        for index in range(3 if kind == 16 else 8):
            for offset, value in enumerate([inner, 0]+params):
                state.put(bank+0x200+len(header)+index*12+offset, 1, value)
    state.put(archive+0x38, 4, 1)
    state.put(archive+0x3C, 4, wave)
    for offset, value in enumerate(bytes.fromhex('78563412efcdab8901234567')):
        state.put(wave+offset, 1, value)
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE]), arguments


def execute(body, case, seed, budget=100000):
    ram, wram, prepare_arguments = setup(case, seed)
    modified = bytearray(wram)
    modified[ADDRESS-memory.BASE:ADDRESS-memory.BASE+len(body)] = body
    wram = bytes(modified)
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base, size in ((memory.BASE, 0x14000), (memory.DATA, 0x4000), (memory.STACK, 0x4000), (memory.RETURN, 0x1000)):
        cpu.mem_map(base, size)
    cpu.mem_write(memory.BASE, wram)
    cpu.mem_write(memory.DATA, ram)
    cpu.mem_write(memory.STACK, random.Random(20261031+seed).randbytes(0x4000))
    writes, visited, frames, nested, contracts = [], set(), [], Counter(), []
    def code(machine, pc, size, unused):
        while frames and pc == frames[-1][1]:
            nested[frames.pop()[0]] += 1
        if not any(first <= pc < first+length for first, length in RANGES.items()):
            raise ValueError('Player step escaped qualified original code: '+hex(pc))
        if pc in RANGES:
            frames.append((pc, machine.reg_read(match_runtime.REGISTERS[-1])))
            words = [machine.reg_read(register) for register in match_runtime.REGISTERS[:min(ARITIES[pc], 4)]]
            if ARITIES[pc] > 4:
                stack = machine.reg_read(match_runtime.REGISTERS[-2])
                words += [int.from_bytes(machine.mem_read(stack+index*4, 4), 'little') for index in range(ARITIES[pc]-4)]
            if pc == 0x03801948:
                if not memory.STACK <= words[3] <= memory.STACK+0x4000-12:
                    raise ValueError('Actual bank output is outside bounded stack instrument object')
                words[3] = {'stackInstrumentOutputBytes': 12}
            elif pc == 0x03801B08:
                pointer = words[5]
                if not memory.STACK <= pointer <= memory.STACK+0x4000-12:
                    raise ValueError('Actual note input is outside bounded stack instrument object')
                data = bytes(machine.mem_read(pointer, 12))
                words[5] = {'instrumentBytesIgnoringUnusedPadding1': (data[:1]+data[2:]).hex()}
            contracts.append([pc, words])
        visited.add(pc)
    def write(machine, access, location, size, value, unused):
        if not memory.STACK <= location < memory.STACK+0x4000:
            writes.append([location, size, value & ((1 << (size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    def invoke(address, arguments, phase):
        registers = [random.Random(20261030+seed+phase*9000+index).getrandbits(32) for index in range(15)]
        registers[:len(arguments)] = arguments
        registers[-2:] = [memory.STACK+0x3F00, memory.RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            cpu.reg_write(register, value)
        fault = None
        try:
            cpu.emu_start(address, memory.RETURN, count=budget, timeout=100000)
        except UcError as error:
            fault = error.errno
        returned = cpu.reg_read(UC_ARM_REG_PC) == memory.RETURN
        observed = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if returned and (observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or frames != [(address, memory.RETURN)]):
            raise ValueError('Actual root/nested/saved-register ABI differs')
        return returned, fault, observed
    prepared, prepare_fault, prepare_registers = invoke(producer.ADDRESS, prepare_arguments, 0)
    if not prepared or prepare_fault is not None:
        raise ValueError('Actual original preparer did not return')
    state = independent.Model(ram, wram)
    state.prepare(prepare_arguments)
    if writes != state.writes or bytes(cpu.mem_read(memory.DATA, 0x4000)) != bytes(state.regions[memory.DATA]) or bytes(cpu.mem_read(memory.BASE, 0x14000)) != bytes(state.regions[memory.BASE]):
        raise ValueError('Actual preparer state differs from independent model')
    prepare_evidence = dict(actualReturn=True, registers=prepare_registers, writes=writes[:],
        nestedReturns={hex(key): count for key,count in sorted(nested.items())}, arguments=contracts[:])
    flags = (state.get(TRACK, 1) | case['setFlags']) & ~case['clearFlags']
    for offset, size, value in ((0, 1, flags), (0x20, 4, case['wait']), (0x13, 1, case['transpose'])):
        state.put(TRACK+offset, size, value)
        cpu.mem_write(TRACK+offset, int(value).to_bytes(size, 'little'))
    for address, size, value in case.get('patches', []):
        state.put(address, size, value)
        cpu.mem_write(address, int(value).to_bytes(size, 'little'))
    ram, wram = bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE])
    states = []
    frames.clear()
    for phase in range(case['passes']):
        first_write, first_contract, previous_nested = len(writes), len(contracts), Counter(nested)
        returned, fault, observed = invoke(ADDRESS, [PLAYER, case['notes']], phase+1)
        if returned:
            expected = independent.Model(ram, wram)
            result = expected.player_step(PLAYER, case['notes'])
            if observed[0] != result or writes[first_write:] != expected.writes:
                raise ValueError('Independent player-step return/ordered-store model differs: '+repr((case, writes[first_write:], expected.writes)))
            if bytes(cpu.mem_read(memory.DATA, 0x4000)) != bytes(expected.regions[memory.DATA]) or bytes(cpu.mem_read(memory.BASE, 0x14000)) != bytes(expected.regions[memory.BASE]):
                raise ValueError('Independent player-step complete memory/code preservation differs')
            ram, wram = bytes(expected.regions[memory.DATA]), bytes(expected.regions[memory.BASE])
            frames.clear()
        delta = nested-previous_nested
        states.append(dict(actualReturn=returned, fault=fault, pc=cpu.reg_read(UC_ARM_REG_PC), registers=observed,
            cpsr=cpu.reg_read(UC_ARM_REG_CPSR), writes=writes[first_write:],
            actualArgumentWords=contracts[first_contract:], actualNestedReturns={hex(key):count for key,count in sorted(delta.items())},
            remainingFrames=[list(row) for row in frames], ramSha256=digest(bytes(cpu.mem_read(memory.DATA, 0x4000))),
            wramAndBssSha256=digest(bytes(cpu.mem_read(memory.BASE, 0x14000))), stackSha256=digest(bytes(cpu.mem_read(memory.STACK, 0x4000)))))
        if not returned:
            break
    return dict(actualOriginalPrepareReturn=prepare_evidence, states=states, visited=sorted(visited))
