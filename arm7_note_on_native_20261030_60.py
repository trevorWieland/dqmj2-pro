import hashlib
import random
from collections import Counter
from pathlib import Path
import match_runtime
import arm7_seq_neighbor_model_20261030 as memory
import arm7_note_on_model_20261030_60 as independent
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS, SIZE = 0x03801B08, 328
CHANNEL, BANK, ARCHIVE, WAVE, INSTRUMENT = [memory.DATA + value for value in (0x100, 0x400, 0x1000, 0x2000, 0x3000)]
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
RANGES = {ADDRESS: SIZE, 0x037FF760: 60, 0x037FF79C: 72, 0x037FF7E8: 64,
    0x037FF8D4: 28, 0x037FF8F4: 28, 0x037FF910: 8, 0x037FF918: 28,
    0x037FFE64: 80, 0x037FFEB8: 52, 0x03801AC8: 64,
    0x037FEFE4: 4, 0x037FEFE8: 4, 0x03806C38: 0x20C}
ARITIES = {ADDRESS: 6, 0x037FF760: 4, 0x037FF79C: 3, 0x037FF7E8: 2,
    0x037FF8D4: 2, 0x037FF8F4: 2, 0x037FF910: 2, 0x037FF918: 2,
    0x037FFE64: 1, 0x037FFEB8: 2, 0x03801AC8: 2,
    0x037FEFE4: 0, 0x037FEFE8: 0, 0x03806C38: 2}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    base = dict(type=1, channel=8, midi=64, velocity=127, length=120, archive=0, wave=0,
        count=1, pointer='relative', root=60, attack=127, decay=50, sustain=127, release=127,
        pan=64, nullArchive=False, invalidBank=False, invalidInstrument=False, passes=1)
    result = []
    def add(**changes):
        result.append(dict(base, **changes))
    for kind in range(256):
        add(type=kind)
    for kind in (2, 3):
        for channel in (0, 7, 8, 13, 14, 15, 16, 255):
            for release in (0, 127, 255):
                add(type=kind, channel=channel, release=release, wave=65535, invalidBank=True)
    for attack in (0, 108, 109, 126, 127, 128, 255):
        for decay in (0, 49, 50, 125, 126, 127, 128, 255):
            add(type=2, attack=attack, decay=decay, sustain=(attack + decay) & 255,
                release=decay, pan=(attack * 17 + decay) & 255)
    words = (0, 1, 255, 256, 0x80000000, 0xFFFFFFFF)
    for pan in range(256):
        add(type=3, channel=14, pan=pan, root=255-pan, midi=words[pan % 6],
            velocity=words[5-pan % 6], length=words[(pan + 3) % 6], release=(0, 127, 255)[pan % 3])
    for archive in (0, 1, 3):
        for wave in (0, 1, 3):
            for count in (0, 1, 3):
                for pointer in ('zero', 'relative', 'absolute'):
                    add(archive=archive, wave=wave, count=count, pointer=pointer)
    for wave in (0, 65535):
        add(wave=wave, nullArchive=True)
    for pointer in ('zero', 'absolute'):
        for length in words:
            add(type=4, pointer=pointer, length=length, invalidBank=True)
    for kind in (1, 2, 3, 4):
        add(type=kind, channel=14 if kind == 3 else 8, pointer='absolute', passes=3)
    return result


def setup(case, seed):
    raw = (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Original ARM7 module differs')
    wram = bytearray(0x14000)
    wram[:len(raw)] = raw
    state = memory.Model(random.Random(20261030 + seed).randbytes(0x4000), wram)
    state.put(CHANNEL, 1, case['channel'])
    for slot in range(4):
        state.put(BANK + 0x18 + slot * 8, 4, 0 if case['nullArchive'] else ARCHIVE)
    state.put(ARCHIVE + 0x38, 4, case['count'])
    stored = {'zero': 0, 'relative': 0x200, 'absolute': WAVE}[case['pointer']]
    for index in range(4):
        state.put(ARCHIVE + 0x3C + index * 4, 4, stored)
    header = bytes.fromhex('78563412efcdab8901234567')
    for wave in (ARCHIVE + 0x200, WAVE):
        for offset, byte in enumerate(header):
            state.put(wave + offset, 1, byte)
    state.put(INSTRUMENT, 1, case['type'])
    if case['type'] == 4:
        direct = WAVE if case['pointer'] != 'zero' else 0
        state.put(INSTRUMENT + 2, 2, direct)
        state.put(INSTRUMENT + 4, 2, direct >> 16)
    else:
        state.put(INSTRUMENT + 2, 2, case['wave'])
        state.put(INSTRUMENT + 4, 2, case['archive'])
    for offset, key in enumerate(('root', 'attack', 'decay', 'sustain', 'release', 'pan'), 6):
        state.put(INSTRUMENT + offset, 1, case[key])
    arguments = [CHANNEL, case['midi'], case['velocity'], case['length'],
        0x03000000 if case['invalidBank'] else BANK,
        0x03001000 if case['invalidInstrument'] else INSTRUMENT]
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
            raise ValueError('Note initializer escaped qualified original helper code: ' + hex(pc))
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
                raise ValueError('Native root six-word calling convention differs')
            state = independent.Model(ram, wram)
            result = state.note(arguments)
            if observed[0] != result or writes[first_write:] != state.writes:
                raise ValueError('Independent note-init return/store model differs: ' + repr((case, writes[first_write:], state.writes)))
            if bytes(machine.mem_read(memory.DATA, 0x4000)) != bytes(state.regions[memory.DATA]) or bytes(machine.mem_read(memory.BASE, 0x14000)) != bytes(state.regions[memory.BASE]):
                raise ValueError('Independent note-init whole-memory model differs')
            if observed[4:12] != registers[4:12] or observed[-2:] != registers[-2:] or frames != [(ADDRESS, memory.RETURN)]:
                raise ValueError('Note-init saved-register/root/nested ABI differs')
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
            raise ValueError('Original/rebuilt note-init native state differs: ' + repr(case))
        outer += len(expected['states'])*2
        visited.update(expected['visited'])
        for row in expected['states']:
            nested.update({key: value*2 for key, value in row['actualNestedReturns'].items()})
        records.append(dict(case=case, seed=seed, actualOriginalAndCompiledReturns=len(expected['states'])*2,
            results=[row['registers'][0] for row in expected['states']], stateSha256=digest(repr(expected).encode())))
    own = set(range(ADDRESS, ADDRESS+SIZE, 4))
    if not own.issubset(visited):
        raise ValueError('Note-init own instruction outcomes incomplete: '+repr(sorted(own-visited)))
    controls = []
    for name, case, limit in (('one-instruction-budget', cases()[0], 1),
            ('unmapped-bank', dict(cases()[1], invalidBank=True), 100000),
            ('unmapped-instrument', dict(cases()[1], invalidInstrument=True), 100000)):
        expected, actual = execute(original, case, 0, limit), execute(rebuilt, case, 0, limit)
        if expected != actual or any(row['actualReturn'] for row in expected['states']):
            raise ValueError('Unsupported note-init path received return credit')
        controls.append(dict(name=name, returnCredit=0, state=expected))
    return dict(supported=True, verifiedReturn=True, vectors=len(records), actualOriginalAndCompiledReturns=outer,
        actualSeparatelyObservedNestedReturns=dict(nested), allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True, cpuModel='Unicorn TI925T ARMv4T surrogate', instructionLimit=100000,
        timeoutMicroseconds=100000, providerReplacements=[], independentTypedNoteAndChannelModel=True,
        records=records, unsupportedControls=controls, unsupportedReturnCredit=0, calleeSourceCredit=0,
        limitations=['Synthetic aligned channel, four archive slots and wave indexes/counts0..3',
            'Raw envelope bytes128..255 include adjacent original-table reads; no instrument-validity claim',
            'Wave-header words and data pointers are measured raw values; no sample playback, physical audio or resource ownership',
            'Only bounded original helper bodies execute; no enclosing sequence/caller reachability claim'])
