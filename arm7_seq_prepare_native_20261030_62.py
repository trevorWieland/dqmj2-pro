import hashlib
import random
from collections import Counter
from pathlib import Path
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
import arm7_seq_prepare_model_20261030_62 as independent
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS, SIZE, CODE = 0x038000B4, 476, 464
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
RANGES = {ADDRESS: CODE, 0x03800B00: 56, 0x03800AA8: 84, 0x03800A7C: 40,
    0x038009E0: 104, 0x03800A48: 52, 0x03800B98: 340,
    0x03801884: 64, 0x038008F0: 224, 0x037FFD90: 36,
    0x03800784: 56, 0x03800290: 88}
ARITIES = {ADDRESS: 4, 0x03800B00: 1, 0x03800AA8: 2, 0x03800A7C: 2,
    0x038009E0: 3, 0x03800A48: 1, 0x03800B98: 3,
    0x03801884: 0, 0x038008F0: 1, 0x037FFD90: 1,
    0x03800784: 1, 0x03800290: 1}
STREAM, SHARED_BACKING = memory.DATA+0x2000, memory.DATA+0x800


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    base = dict(player=0, flags=0, shared=True, freeMask=0xFFFFFFFF, command=254, mask=0,
        offset=0, bank=0x12345678, invalidSequence=False, passes=1)
    result = []
    def add(**changes):
        result.append(dict(base, **changes))
    for flags in range(256):
        add(player=flags % 16, flags=flags, shared=bool(flags & 1), command=flags)
    for free in (0, 1, 0x80000000, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555):
        for mask in (0, 1, 2, 3, 0x8000, 65535, 0x5555, 0xAAAA):
            for offset in (0, 3, 13, 15):
                add(freeMask=free, mask=mask, offset=offset)
    for player in range(16):
        for count in (1, 2, 16, 32):
            add(player=player, mask=65535, freeMask=(1 << count)-1)
    for bank in (0, 0x80000000, 0xFFFFFFFF):
        add(bank=bank, shared=False)
    for command, mask in ((0, 0), (254, 65535)):
        add(command=command, mask=mask, passes=3)
    return result


def setup(case, seed):
    raw = (ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Original ARM7 module differs')
    rng = random.Random(20261030+seed)
    wram = bytearray(0x14000)
    wram[:len(raw)] = raw
    for base, size in ((independent.PLAYERS, 16*36), (independent.TRACKS, 32*64)):
        wram[base-memory.BASE:base-memory.BASE+size] = rng.randbytes(size)
    state = memory.Model(rng.randbytes(0x4000), wram)
    for player in range(16):
        address = independent.PLAYERS+player*36
        state.put(address+1, 1, player)
        for slot in range(16):
            state.put(address+8+slot, 1, 255)
    state.put(independent.PLAYERS+case['player']*36, 1, case['flags'])
    for track in range(32):
        address = independent.TRACKS+track*64
        state.put(address, 1, (state.get(address, 1) & ~1) | int(not bool(case['freeMask'] & (1 << track))))
        state.put(address+0x3C, 4, 0)
    state.put(independent.SHARED, 4, SHARED_BACKING if case['shared'] else 0)
    current = STREAM+case['offset']
    for index, value in enumerate((case['command'], case['mask'] & 255, case['mask'] >> 8)):
        state.put(current+index, 1, value)
    sequence = 0x03000000 if case['invalidSequence'] else STREAM
    arguments = [case['player'], sequence, case['offset'], case['bank']]
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
            raise ValueError('Sequence preparation escaped qualified original helper code: ' + hex(pc))
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
        registers[:4], registers[-2:] = arguments[:4], [memory.STACK+0x3F00, memory.RETURN]
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
                raise ValueError('Native root four-word calling convention differs')
            state = independent.Model(ram, wram)
            result = state.prepare(arguments)
            if writes[first_write:] != state.writes:
                raise ValueError('Independent sequence-preparation return/store model differs: ' + repr((case, writes[first_write:], state.writes)))
            if bytes(machine.mem_read(memory.DATA, 0x4000)) != bytes(state.regions[memory.DATA]) or bytes(machine.mem_read(memory.BASE, 0x14000)) != bytes(state.regions[memory.BASE]):
                raise ValueError('Independent sequence-preparation whole-memory model differs')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or frames != [(ADDRESS, memory.RETURN)]:
                raise ValueError('Sequence-preparation saved-register/root/nested ABI differs')
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
            raise ValueError('Original/rebuilt sequence-preparation native state differs: ' + repr(case))
        outer += len(expected['states'])*2
        visited.update(expected['visited'])
        for row in expected['states']:
            nested.update({key: value*2 for key, value in row['actualNestedReturns'].items()})
        records.append(dict(case=case, seed=seed, actualOriginalAndCompiledReturns=len(expected['states'])*2,
            results=[row['registers'][0] for row in expected['states']], stateSha256=digest(repr(expected).encode())))
    own = set(range(ADDRESS, ADDRESS+CODE, 4))
    if not own.issubset(visited):
        raise ValueError('Sequence-preparation own instruction outcomes incomplete: '+repr(sorted(own-visited)))
    controls = []
    for name, case, limit in (('one-instruction-budget', cases()[0], 1),
            ('unmapped-sequence', dict(cases()[2], invalidSequence=True, freeMask=0xFFFFFFFF), 100000)):
        expected, actual = execute(original, case, 0, limit), execute(rebuilt, case, 0, limit)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Unsupported sequence-preparation path received return credit')
        controls.append(dict(name=name, returnCredit=0, state=expected))
    return dict(supported=True, verifiedReturn=True, vectors=len(records), actualOriginalAndCompiledReturns=outer,
        actualSeparatelyObservedNestedReturns=dict(nested), allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True, cpuModel='Unicorn TI925T ARMv4T surrogate', instructionLimit=100000,
        timeoutMicroseconds=100000, providerReplacements=[], independentPlayerTrackAllocationCacheAndSharedModel=True,
        records=records, unsupportedControls=controls, unsupportedReturnCredit=0, calleeSourceCredit=0,
        limitations=['Synthetic valid player indexes/IDs0..15 and zero-head active/inactive tracks',
            'Only initial allocation header parsing executes; no full sequence interpretation, ownership or physical audio claim',
            'Cached reader03800290 takes a Track pointer and advances current itself, unlike the separate-byte-reader SDK reference',
            'Original lower helpers execute without replacements and receive no new source credit'])
