import hashlib
import random
from collections import Counter
from pathlib import Path
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
import arm7_channel_alloc_model_20261030_61 as independent
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS, SIZE, CODE = 0x037FF950, 460, 440
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
RANGES = {ADDRESS: CODE, 0x037FFD90: 36, 0x03800B38: 96}
ARITIES = {ADDRESS: 5, 0x037FFD90: 1, 0x03800B38: 3}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    base = dict(mask=65535, priority=127, flags=0, weak=0, strong=0, poolFlags=255,
        priorities=[100]*16, volumes=[127]*16, oldCallback='none', newCallback=0,
        callbackData=0xFFFFFFFF, invalidCallback=False, passes=1)
    result = []
    def add(**changes):
        result.append(dict(base, **changes))
    for channel in range(16):
        for priority in (0, 99, 100, 101, 255, 256, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF):
            add(mask=1 << channel, priority=priority)
    for mask in (0, 1, 65535, 65536, 0x80000000, 0xFFFFFFFF):
        for weak, strong in ((0, 0), (65535, 0), (0, 65535), (1, 16), (0xAAAAAAAA, 0x55555555)):
            for flags in (0, 1, 2, 256):
                add(mask=mask, weak=weak, strong=strong, flags=flags)
    for channel in range(16):
        for priority in (0, 1, 127, 128, 255):
            values = [255]*16
            values[channel] = priority
            add(priorities=values, priority=255)
    for shift in range(4):
        for first, second in ((0, 255), (255, 0), (0, 0), (127, 127), (128, 127), (127, 128)):
            volumes = [127]*16
            volumes[4], volumes[5] = (shift << 8) | first, (shift << 8) | second
            add(mask=(1 << 4) | (1 << 5), volumes=volumes)
    for flags in range(256):
        add(mask=16, poolFlags=flags)
    for callback in ('head', 'middle'):
        for channel in (0, 4, 15):
            add(mask=1 << channel, oldCallback=callback)
    add(mask=16, newCallback=0x03800B38, callbackData=memory.DATA+0x3000)
    for callback in ('none', 'head'):
        add(mask=16, oldCallback=callback, passes=3)
    return result


def setup(case, seed):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Original ARM7 module differs')
    rng = random.Random(20261030+seed)
    wram = bytearray(0x14000)
    wram[:len(raw)] = raw
    offset = independent.POOL-memory.BASE
    wram[offset:offset+84*16] = rng.randbytes(84*16)
    state = memory.Model(rng.randbytes(0x4000), wram)
    state.put(independent.MASKS, 4, case['weak'])
    state.put(independent.MASKS+4, 4, case['strong'])
    for channel in range(16):
        address = independent.POOL+channel*84
        track, previous = memory.DATA+0x400+channel*64, memory.DATA+0x1000+channel*0x60
        state.put(address, 1, channel)
        state.put(address+3, 1, case['poolFlags'])
        state.put(address+0x22, 1, case['priorities'][channel])
        state.put(address+0x24, 2, case['volumes'][channel])
        state.put(address+0x48, 4, 0 if case['oldCallback']=='none' else (0x03005000 if case['invalidCallback'] else 0x03800B38))
        state.put(address+0x4C, 4, track)
        state.put(address+0x50, 4, 0)
        state.put(track+0x3C, 4, previous if case['oldCallback']=='middle' else address)
        state.put(previous+0x50, 4, address)
    arguments = [case['mask'], case['priority'], case['flags'], case['newCallback'], case['callbackData']]
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
            raise ValueError('Channel allocator escaped qualified original helper code: ' + hex(pc))
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
                raise ValueError('Native root five-word calling convention differs')
            state = independent.Model(ram, wram)
            result = state.allocate(arguments)
            if observed[0] != result or writes[first_write:] != state.writes:
                raise ValueError('Independent channel-allocation return/store model differs: ' + repr((case, writes[first_write:], state.writes)))
            if bytes(machine.mem_read(memory.DATA, 0x4000)) != bytes(state.regions[memory.DATA]) or bytes(machine.mem_read(memory.BASE, 0x14000)) != bytes(state.regions[memory.BASE]):
                raise ValueError('Independent channel-allocation whole-memory model differs')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or frames != [(ADDRESS, memory.RETURN)]:
                raise ValueError('Channel-allocation saved-register/root/nested ABI differs')
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
            raise ValueError('Original/rebuilt channel-allocation native state differs: ' + repr(case))
        outer += len(expected['states'])*2
        visited.update(expected['visited'])
        for row in expected['states']:
            nested.update({key: value*2 for key, value in row['actualNestedReturns'].items()})
        records.append(dict(case=case, seed=seed, actualOriginalAndCompiledReturns=len(expected['states'])*2,
            results=[row['registers'][0] for row in expected['states']], stateSha256=digest(repr(expected).encode())))
    own = set(range(ADDRESS, ADDRESS+CODE, 4))
    if not own.issubset(visited):
        raise ValueError('Channel-allocation own instruction outcomes incomplete: '+repr(sorted(own-visited)))
    controls = []
    for name, case, limit in (('one-instruction-budget', cases()[0], 1),
            ('unmapped-old-callback', dict(cases()[2], oldCallback='head', invalidCallback=True), 100000)):
        expected, actual = execute(original, case, 0, limit), execute(rebuilt, case, 0, limit)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Unsupported channel-allocation path received return credit')
        controls.append(dict(name=name, returnCredit=0, state=expected))
    return dict(supported=True, verifiedReturn=True, vectors=len(records), actualOriginalAndCompiledReturns=outer,
        actualSeparatelyObservedNestedReturns=dict(nested), allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True, cpuModel='Unicorn TI925T ARMv4T surrogate', instructionLimit=100000,
        timeoutMicroseconds=100000, providerReplacements=[], independentTypedChannelSelectionAndSetupModel=True,
        records=records, unsupportedControls=controls, unsupportedReturnCredit=0, calleeSourceCredit=0,
        limitations=['Synthetic initialized sixteen-channel pool and unchanged original allocation/shift tables',
            'Packed volume high byte0..3 only; no claim for adjacent table reads or out-of-domain C shifts',
            'Original callback03800B38 removes a real synthetic list member with reason0; no ownership or physical audio claim',
            'Original LFO parameter initializer executes; callback and callee source credit remains zero'])
