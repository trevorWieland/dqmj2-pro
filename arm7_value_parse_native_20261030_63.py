import hashlib
import random
from collections import Counter
from pathlib import Path
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
import arm7_value_parse_model_20261030_63 as independent
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS, SIZE, CODE = 0x038007F0, 256, 256
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
RANGES = {ADDRESS: CODE, 0x03801840: 64, 0x03800784: 56, 0x03800290: 88, 0x037FEEC4: 40}
ARITIES = {ADDRESS: 3, 0x03801840: 2, 0x03800784: 1, 0x03800290: 1, 0x037FEEC4: 0}
TRACK, PLAYER, STREAM, SHARED_BACKING = [memory.DATA+offset for offset in (0x100, 0x200, 0x1000, 0x2000)]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    base = dict(type=0, bytes=[0], offset=0, playerId=0, random=0x12345678,
        shared=True, invalidStream=False, passes=1, definedContract=True)
    result = []
    def add(**changes):
        result.append(dict(base, **changes))
    for byte in range(256):
        add(bytes=[byte])
    for word in (0, 1, 127, 128, 255, 256, 32767, 32768, 65535):
        for offset in (0, 3, 13, 15):
            add(type=1, bytes=[word & 255, word >> 8], offset=offset)
    for prefix in (0x80, 0x81, 0xFF):
        for length in range(1, 9):
            for final in (0, 1, 127):
                add(type=2, bytes=[prefix]*(length-1)+[final], offset=15)
    inverse = pow(1664525, -1, 1 << 32)
    seeds = [0, 1, 0x12345678, 0xFFFFFFFF]
    seeds += [((word << 16)-1013904223)*inverse & 0xFFFFFFFF for word in (0, 1, 32767, 32768, 65535)]
    for lower, upper in ((0, 0), (0, 1), (-1, 1), (-32768, 32767), (32767, -32768), (-1, -32768), (32767, 32767)):
        data = [lower & 255, lower >> 8 & 255, upper & 255, upper >> 8 & 255]
        for seed in seeds:
            add(type=3, bytes=data, random=seed)
    for index in range(256):
        for player in (0, 15):
            add(type=4, bytes=[index], playerId=player, offset=index % 16)
    for kind, data in ((0, [1, 2, 3]), (1, [1, 2, 3, 4, 5, 6]), (2, [0x81, 1, 0, 2]), (3, [0, 0, 1, 0]*3), (4, [0, 15, 31])):
        add(type=kind, bytes=data, passes=3)
    return result


def setup(case, seed):
    raw = (ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Original ARM7 module differs')
    rng = random.Random(20261030+seed)
    wram = bytearray(0x14000)
    wram[:len(raw)] = raw
    state = memory.Model(rng.randbytes(0x4000), wram)
    current = STREAM+case['offset']
    for offset, value in enumerate(case['bytes']):
        state.put(current+offset, 1, value)
    state.put(TRACK+0x28, 4, 0x03000000 if case['invalidStream'] else current)
    state.put(PLAYER+1, 1, case['playerId'])
    state.put(0x03807EDC, 4, SHARED_BACKING if case['shared'] else 0)
    state.put(0x03807EC4, 4, 0)
    state.put(0x03807EC8, 4, 0)
    state.put(independent.RANDOM_STATE, 4, case['random'])
    arguments = [TRACK, PLAYER, case['type']]
    return bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE]), arguments


def execute(body, case, seed, budget=100000):
    ram, wram, arguments = setup(case, seed)
    mutable = bytearray(wram)
    mutable[ADDRESS-memory.BASE:ADDRESS-memory.BASE+len(body)] = body
    wram = bytes(mutable)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base, size in ((memory.BASE, 0x14000), (memory.DATA, 0x4000), (memory.STACK, 0x4000), (memory.RETURN, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(memory.BASE, wram)
    machine.mem_write(memory.DATA, ram)
    machine.mem_write(memory.STACK, random.Random(20261031 + seed).randbytes(0x4000))
    writes, visited, frames, nested, contracts = [], set(), [], Counter(), []
    def code(cpu, pc, size, unused):
        while frames and pc == frames[-1][1]:
            nested[frames.pop()[0]] += 1
        if not any(first <= pc < first + length for first, length in RANGES.items()):
            raise ValueError('Value parser escaped qualified original helper code: ' + hex(pc))
        if pc in RANGES:
            frames.append((pc, cpu.reg_read(match_runtime.REGISTERS[-1])))
            words = [cpu.reg_read(register) for register in match_runtime.REGISTERS[:min(ARITIES[pc], 4)]]
            if ARITIES[pc] > 4:
                stack = cpu.reg_read(match_runtime.REGISTERS[-2])
                words += [int.from_bytes(cpu.mem_read(stack + 4*index, 4), 'little') for index in range(ARITIES[pc]-4)]
            contracts.append([pc, words])
        visited.add(pc)
    def write(cpu, access, location, size, value, unused):
        if not memory.STACK <= location < memory.STACK + 0x4000:
            writes.append([location, size, value & ((1 << (size*8))-1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    states = []
    for phase in range(case['passes']):
        rng = random.Random(20261030 + seed + phase*9000)
        registers = [rng.getrandbits(32) for unused in match_runtime.REGISTERS]
        registers[:3], registers[-2:] = arguments[:3], [memory.STACK+0x3F00, memory.RETURN]
        machine.mem_write(registers[-2], b''.join(word.to_bytes(4, 'little') for word in arguments[4:]))
        machine.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
        for register, value in zip(match_runtime.REGISTERS, registers):
            machine.reg_write(register, value)
        first_write, before_nested, first_contract = len(writes), Counter(nested), len(contracts)
        fault = None
        try:
            machine.emu_start(ADDRESS, memory.RETURN, count=budget, timeout=100000)
        except UcError as error:
            fault = error.errno
        returned = machine.reg_read(UC_ARM_REG_PC) == memory.RETURN
        observed = [machine.reg_read(register) for register in match_runtime.REGISTERS]
        if returned:
            if contracts[first_contract] != [ADDRESS, arguments]:
                raise ValueError('Native root three-word calling convention differs')
            state = independent.Model(ram, wram)
            result = state.parse(arguments)
            if observed[0] != result or writes[first_write:] != state.writes:
                raise ValueError('Independent value-parser return/store model differs: ' + repr((case, writes[first_write:], state.writes)))
            if bytes(machine.mem_read(memory.DATA, 0x4000)) != bytes(state.regions[memory.DATA]) or bytes(machine.mem_read(memory.BASE, 0x14000)) != bytes(state.regions[memory.BASE]):
                raise ValueError('Independent value-parser whole-memory model differs')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or frames != [(ADDRESS, memory.RETURN)]:
                raise ValueError('Value-parser saved-register/root/nested ABI differs')
            ram, wram = bytes(state.regions[memory.DATA]), bytes(state.regions[memory.BASE])
            frames.clear()
        delta = nested-before_nested
        states.append(dict(actualReturn=returned, fault=fault, pc=machine.reg_read(UC_ARM_REG_PC), registers=observed,
            cpsr=machine.reg_read(UC_ARM_REG_CPSR), writes=writes[first_write:],
            actualArgumentWords=contracts[first_contract:],
            actualNestedReturns={hex(key): count for key, count in sorted(delta.items())}, remainingFrames=[list(row) for row in frames],
            ramSha256=digest(bytes(machine.mem_read(memory.DATA, 0x4000))),
            wramAndBssSha256=digest(bytes(machine.mem_read(memory.BASE, 0x14000))),
            stackSha256=digest(bytes(machine.mem_read(memory.STACK, 0x4000)))))
        if not returned:
            break
    return dict(states=states, visited=sorted(visited))


def oracle(original, rebuilt):
    records, visited, outer, nested = [], set(), 0, Counter()
    for seed, case in enumerate(cases()):
        expected, actual = execute(original, case, seed), execute(rebuilt, case, seed)
        if expected != actual or any(not row['actualReturn'] or row['fault'] is not None for row in expected['states']):
            raise ValueError('Original/rebuilt value-parser native state differs: ' + repr(case))
        outer += len(expected['states'])*2
        visited.update(expected['visited'])
        for row in expected['states']:
            nested.update({key: value*2 for key, value in row['actualNestedReturns'].items()})
        records.append(dict(case=case, seed=seed, actualOriginalAndCompiledReturns=len(expected['states'])*2,
            results=[row['registers'][0] for row in expected['states']], stateSha256=digest(repr(expected).encode())))
    own = set(range(ADDRESS, ADDRESS+CODE, 4))
    if not own.issubset(visited):
        raise ValueError('Value-parser own instruction outcomes incomplete: '+repr(sorted(own-visited)))
    controls = []
    for name, case, limit in (('one-instruction-budget', cases()[0], 1),
            ('unmapped-stream', dict(cases()[2], invalidStream=True), 100000)):
        expected, actual = execute(original, case, 0, limit), execute(rebuilt, case, 0, limit)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Unsupported value-parser path received return credit')
        controls.append(dict(name=name, returnCredit=0, state=expected))
    return dict(supported=True, verifiedReturn=True, vectors=len(records), actualOriginalAndCompiledReturns=outer,
        actualSeparatelyObservedNestedReturns=dict(nested), allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True, cpuModel='Unicorn TI925T ARMv4T surrogate', instructionLimit=100000,
        timeoutMicroseconds=100000, providerReplacements=[], independentValueWidthVlvVariableAndWrappedRandomModel=True,
        records=records, unsupportedControls=controls, unsupportedReturnCredit=0, calleeSourceCredit=0,
        limitations=['Synthetic typed selectors0..4 and nonnull variable backing only',
            'Variable indexes32..255 measure adjacent synthetic shared bytes without assigning global-variable meaning',
            'VLV arithmetic wraps32 bits; random range multiplication wraps32 bits before signed arithmetic shift',
            'Invalid selectors and null variable pointers leave a native saved register uninitialized and have no defined C semantic credit'])
