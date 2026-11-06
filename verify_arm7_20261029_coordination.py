import hashlib
import itertools
import json
import os
import random
import struct
import subprocess
import sys
from project import ROOT, configuration, now, sha256, write_json

sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC
import match_arm7 as matcher
from elf_units import split_symbol
from link_runtime_unit import binding_object

PINS = {
    0x037FBA94: (116, '095d1bb64765715286c7a2e6254d3d8a788657db5bdb0ade6b655186b123297a'),
    0x037FC888: (132, 'f454cdfff017f9a041158a03055b15b9f6065fcc3ed444bddeca0ca6f155d7b4'),
    0x037FD5C0: (136, '7f428fcba5e4467b8ae5bf8c7e56612678614bc7311d8803f6905b53b6e91d59')
}
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
WORK = ROOT / 'work/lowlevel-recovery/20261029-arm7-coordination-proof'
ARENA, GLOBAL, STOP, CALLBACK = 0x03002000, 0x03807000, 0x0301E000, 0x0301A000
OBJECT, THREAD, OTHER, FOLLOWING, PREVIOUS = [ARENA + n for n in [0x100, 0x400, 0x700, 0xA00, 0xD00]]
IRQ = {0x037FDD00: 0x80, 0x037FDD14: 0x80, 0x037FDD2C: 0xC0, 0x037FDD40: 0xC0}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def location(address):
    return (0, address - ARENA) if ARENA <= address < ARENA + 4096 else (1, address - GLOBAL)


def word(buffers, address):
    page, offset = location(address)
    return struct.unpack_from('<I', buffers[page], offset)[0]


def put(buffers, address, value, writes=None, size=4):
    page, offset = location(address)
    struct.pack_into('<I' if size == 4 else '<H', buffers[page], offset, value)
    if writes is not None:
        writes.append([address, size, value])


def geometries(address):
    if address == 0x037FBA94:
        return list(itertools.product([0, 1, 0xFFFFFFFF], [0, 1, 0x80000000], [0, CALLBACK, CALLBACK | 1]))
    if address == 0x037FC888:
        return list(itertools.product(['free', 'recursive', 'wait-free', 'wait-recursive', 'wait-twice'], [0, 0xFFFFFFFF], [0, PREVIOUS]))
    return list(itertools.product([0, 1, 0xFFFFFFFF], [0, FOLLOWING], [0, PREVIOUS]))


def prepare(address, geometry, seed, initial_irq):
    rng = random.Random(0x202610290039 + seed)
    buffers = [bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))]
    arguments = [rng.getrandbits(32), OBJECT, 0, 0]
    calls, writes, wait_plan = [], [], []
    if address == 0x037FBA94:
        mode, result, callback = geometry
        arguments[2:4] = [callback, mode]
        mask = 0xC0 if mode else 0x80
        calls = [[0x037FDD2C if mode else 0x037FDD00, []], [0x037FE2AC, arguments[:2]]]
        expected = [bytearray(page) for page in buffers]
        if result == 0:
            if callback:
                calls.append([callback & ~1, []])
            put(expected, OBJECT + 4, arguments[0] & 0xFFFF, writes, 2)
        calls.append([0x037FDD40 if mode else 0x037FDD14, [initial_irq & mask]])
    elif address == 0x037FC888:
        kind, count, tail = geometry
        arguments[0] = OBJECT
        owner = 0 if kind == 'free' else THREAD if kind == 'recursive' else OTHER
        put(buffers, 0x03807718, THREAD)
        put(buffers, OBJECT + 8, owner)
        put(buffers, OBJECT + 0xC, count)
        put(buffers, THREAD + 0x70, tail)
        wait_plan = [OTHER, 0] if kind == 'wait-twice' else [0] if kind == 'wait-free' else [THREAD] if kind == 'wait-recursive' else []
        expected = [bytearray(page) for page in buffers]
        calls = [[0x037FDD00, []]]
        for new_owner in wait_plan:
            put(expected, THREAD + 0x68, OBJECT, writes)
            calls.append([0x037FC290, [OBJECT]])
            put(expected, OBJECT + 8, new_owner, writes)
            put(expected, THREAD + 0x68, 0, writes)
        owner = word(expected, OBJECT + 8)
        if owner == 0:
            put(expected, OBJECT + 8, THREAD, writes)
            put(expected, OBJECT + 0xC, (count + 1) & 0xFFFFFFFF, writes)
            calls.append([0x037FC9A4, [THREAD, OBJECT]])
            put(expected, THREAD + 0x6C if tail == 0 else tail + 0x10, OBJECT, writes)
            put(expected, OBJECT + 0x14, tail, writes)
            put(expected, OBJECT + 0x10, 0, writes)
            put(expected, THREAD + 0x70, OBJECT, writes)
        else:
            put(expected, OBJECT + 0xC, (count + 1) & 0xFFFFFFFF, writes)
        calls.append([0x037FDD14, [initial_irq & 0x80]])
        result = 0x80
    else:
        active, following, previous = geometry
        arguments[0] = OBJECT
        put(buffers, OBJECT, active)
        put(buffers, OBJECT + 0x18, following)
        put(buffers, OBJECT + 0x14, previous)
        expected = [bytearray(page) for page in buffers]
        calls = [[0x037FDD00, []]]
        if active:
            put(expected, 0x038078B0 if following == 0 else following + 0x14, previous, writes)
            if previous:
                put(expected, previous + 0x18, following, writes)
            else:
                put(expected, 0x038078AC, following, writes)
                if following:
                    calls.append([0x037FD2C0, [following]])
            for offset in [0, 0x1C, 0x20]:
                put(expected, OBJECT + offset, 0, writes)
        calls.append([0x037FDD14, [initial_irq & 0x80]])
        result = 0x80
    return buffers, expected, arguments, calls, writes, result, wait_plan


def real_link(entry, native, specs):
    directory = WORK / 'linked' / entry['name']
    directory.mkdir(parents=True, exist_ok=True)
    caller = directory / 'caller.o'
    with (ROOT / entry['object']).open('rb') as stream:
        elf = ELFFile(stream)
        flags = elf['e_flags']
        split_symbol(elf, entry['name'], caller)
    memory = [f"CALL: ORIGIN = {entry['address']} > caller.bin"]
    sections, assignments, objects, bindings = ['.caller: { caller.o(.text) } > CALL'], [], [caller], []
    for index, relocation in enumerate(entry['relocations']):
        name, target = relocation['symbol'], int(relocation['target'], 0)
        if any(binding['name'] == name for binding in bindings):
            continue
        binding = {'name': name, 'address': hex(target), 'processor': 'arm7', 'module': 'arm7-wram'}
        if name.startswith('native_arm7_fn_'):
            if target not in specs or specs[target]['module'] != 'arm7-wram':
                raise ValueError('ARM7 callee lacks a canonical qualified ARM function entry')
            probe = directory / f'binding{index}.o'
            binding_object(name, 'arm', flags, probe)
            objects.append(probe)
            memory.append(f'BIND{index}: ORIGIN = {target:#x} > binding{index}.bin')
            sections.append(f'.binding{index}: {{ binding{index}.o(.text) }} > BIND{index}')
            binding.update(kind='function', mode='arm', initializedCodeBytes=0, sourceCredit=0)
        else:
            if target not in (0x03807714, 0x038078A8):
                raise ValueError('Unexpected unqualified global data address')
            assignments.append(f'{name} = {target:#x};')
            binding.update(kind='data')
        bindings.append(binding)
    lcf = directory / 'unit.lcf'
    lcf.write_text('MEMORY {\n' + '\n'.join(memory) + '\n}\nSECTIONS {\n' + '\n'.join(sections + assignments) + '\n}\n')
    linked, raw = directory / 'linked.elf', directory / 'caller.bin'
    for output in [linked, raw]:
        output.unlink(missing_ok=True)
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm7tdmi', '-main', entry['name'], str(lcf), *map(str, objects), '-o', str(linked)]
    process = subprocess.run(command, cwd=directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    if process.returncode or raw.read_bytes() != native:
        raise ValueError('Qualified ARM7 caller link differs: ' + process.stdout + process.stderr)
    with linked.open('rb') as stream:
        symbols = list(ELFFile(stream).get_section_by_name('.symtab').iter_symbols())
        symbol = next(symbol for symbol in symbols if symbol.name == entry['name'])
        if symbol['st_value'] != int(entry['address'], 0) or symbol['st_size'] != entry['bytes']:
            raise ValueError('Linked caller symbol boundary differs')
        for binding in bindings:
            if binding['kind'] == 'function':
                symbol = next(symbol for symbol in symbols if symbol.name == binding['name'])
                if symbol['st_value'] != int(binding['address'], 0) or symbol['st_size'] != 0:
                    raise ValueError('Binding-only anchor acquired executable source credit')
    for path in directory.glob('binding*.bin'):
        if path.stat().st_size:
            raise ValueError('Mode anchor emitted initialized executable bytes')
    return {
        'exactCallerBytes': True, 'sourceObjectSha256': entry['objectSha256'],
        'splitObjectSha256': sha256(caller), 'linkedCallerSha256': sha256(raw),
        'linkedElf': linked.relative_to(ROOT).as_posix(), 'linkedElfSha256': sha256(linked),
        'lcf': lcf.relative_to(ROOT).as_posix(), 'lcfSha256': sha256(lcf),
        'linkerSha256': LINKER_HASH, 'command': command, 'exitCode': process.returncode,
        'stdout': process.stdout, 'stderr': process.stderr, 'qualifiedBindings': bindings,
        'calleeCodeOrSourceCredit': 0, 'wholeModuleLinked': False
    }


def execute(code, spec, specs, fixture, seed, thumb, initial_irq):
    before, expected, arguments, expected_calls, expected_writes, result, wait_plan = fixture
    rng = random.Random(0x202610290139 + seed)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(0x037F8000, 0x20000)
    uc.mem_map(0x03000000, 0x20000)
    for target in [*IRQ, 0x037FC9A4]:
        callee = specs[target]
        binary = (ROOT / callee['binary']).read_bytes()
        uc.mem_write(target, binary[target - callee['base']:target - callee['base'] + callee['bytes']])
    uc.mem_write(spec['address'], code)
    for address, page in zip([ARENA, GLOBAL], before):
        uc.mem_write(address, bytes(page))
    uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x1F | initial_irq)
    registers = [rng.getrandbits(32) for unused in matcher.common.REGISTERS]
    registers[:4] = arguments
    registers[-2:] = [0x0301FF00, STOP | int(thumb)]
    for register, value in zip(matcher.common.REGISTERS, registers):
        uc.reg_write(register, value)
    writes, calls, visited, all_writes = [], [], set(), []
    wait_index = 0
    def record(uc, access, address, size, value, user):
        all_writes.append([address, size, value])
        if ARENA <= address < ARENA + 4096 or GLOBAL <= address < GLOBAL + 4096:
            writes.append([address, size, value])
    def observe(uc, address, size, user):
        nonlocal wait_index
        if spec['address'] <= address < spec['address'] + len(code):
            visited.add(address)
            return
        for target in [*IRQ, 0x037FC9A4]:
            if target <= address < target + specs[target]['bytes']:
                if address == target:
                    width = 0 if target in (0x037FDD00, 0x037FDD2C) else 2 if target == 0x037FC9A4 else 1
                    calls.append([target, [uc.reg_read(register) for register in matcher.common.REGISTERS[:width]]])
                return
        if address not in [0x037FE2AC, 0x037FC290, 0x037FD2C0, CALLBACK]:
            raise ValueError('Caller escaped its explicit bounded native/callee contracts')
        if address == CALLBACK and bool(uc.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(arguments[2] & 1):
            raise ValueError('Callback did not enter its declared ARM/Thumb mode')
        width = 2 if address == 0x037FE2AC else 0 if address == CALLBACK else 1
        calls.append([address, [uc.reg_read(register) for register in matcher.common.REGISTERS[:width]]])
        if address == 0x037FC290:
            if wait_index >= len(wait_plan):
                raise ValueError('Scheduler contract exceeded its finite wake plan')
            value = wait_plan[wait_index]
            wait_index += 1
            uc.mem_write(OBJECT + 8, struct.pack('<I', value))
            writes.append([OBJECT + 8, 4, value])
        returned = uc.reg_read(matcher.common.REGISTERS[-1])
        for register in [*matcher.common.REGISTERS[:4], matcher.common.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        if address == 0x037FE2AC:
            uc.reg_write(matcher.common.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | (uc.reg_read(UC_ARM_REG_CPSR) & 0xDF) | ((returned & 1) << 5))
        uc.reg_write(UC_ARM_REG_PC, returned & ~1)
    uc.hook_add(UC_HOOK_MEM_WRITE, record)
    uc.hook_add(UC_HOOK_CODE, observe)
    uc.emu_start(spec['address'], STOP, count=2000)
    after = [uc.reg_read(register) for register in matcher.common.REGISTERS]
    cpsr = uc.reg_read(UC_ARM_REG_CPSR)
    if uc.reg_read(UC_ARM_REG_PC) != STOP or after[0] != result or after[4:12] != registers[4:12] or after[-2:] != registers[-2:]:
        raise ValueError('Native/source caller failed actual return or independent result/preservation model')
    if cpsr & 0xFF != 0x1F | initial_irq | (0x20 if thumb else 0):
        raise ValueError('Native IRQ primitives did not restore original control state')
    pages = [bytes(uc.mem_read(address, 4096)) for address in [ARENA, GLOBAL]]
    if pages != [bytes(page) for page in expected] or calls != expected_calls or writes != expected_writes:
        raise ValueError('Independent sequential RAM/global/call contract differs')
    return {'registers': after, 'cpsr': cpsr, 'writes': writes, 'stackAndNativeWrites': all_writes, 'calls': calls, 'visited': sorted(visited), 'memorySha256': [digest(page) for page in pages]}


def main():
    if sha256(COMPILER) != COMPILER_HASH or sha256(LINKER) != LINKER_HASH:
        raise ValueError('Pinned compiler/linker differs')
    matcher.WORK = WORK / 'compile'
    specs = {spec['address']: spec for spec in matcher.candidates(10000)}
    matches = []
    for address, (size, source_hash) in PINS.items():
        spec = specs[address]
        source = ROOT / f'src/arm7/20261029rotated29/native_arm7_wram_{address:08x}.c'
        if spec['bytes'] != size or spec['module'] != 'arm7-wram' or sha256(source) != source_hash:
            raise ValueError('Frozen ordinary C source or native boundary differs')
        for output in (matcher.WORK / 'compile' / source.stem).glob('*.o'):
            output.unlink()
        entry, code = matcher.compare(source, spec, COMPILER, COMPILER_HASH, 2, 'off')
        if code is None:
            raise ValueError('Complete ordinary C body no longer matches')
        offset = address - spec['base']
        native = (ROOT / spec['binary']).read_bytes()[offset:offset + size]
        entry['isolatedRealMwCallerLink'] = real_link(entry, native, specs)
        hashes, covered, native_callees = [], set(), set()
        for index, geometry in enumerate(geometries(address)):
            for initial_irq in [0, 0x40, 0x80, 0xC0]:
                fixture = prepare(address, geometry, index, initial_irq)
                for thumb in [False, True]:
                    first = execute(native, spec, specs, fixture, index, thumb, initial_irq)
                    second = execute(code, spec, specs, fixture, index, thumb, initial_irq)
                    if first != second:
                        raise ValueError('Fresh native/source coordination machines differ')
                    covered.update(first['visited'])
                    native_callees.update(target for target, unused in first['calls'] if target in IRQ or target == 0x037FC9A4)
                    hashes.append(digest(json.dumps(first, sort_keys=True).encode()))
        instruction_addresses = {instruction.address for instruction in spec['instructions']}
        if covered != instruction_addresses:
            raise ValueError('Bounded fixtures did not cover every caller instruction')
        entry['oracle'] = {
            'cases': len(hashes), 'nativeAndRecompiledCalls': len(hashes) * 2,
            'verifiedReturn': True, 'returnModes': ['arm', 'thumb'], 'instructionLimit': 2000,
            'nativeInstructionCoverage': len(covered), 'nativeInstructions': len(instruction_addresses),
            'independentModel': 'Sequential RAM/global stores and native call arguments, finite wake plans, return R0, preserved R4-R11/SP/LR, original IRQ/FIQ mask restoration',
            'stateSha256': hashes, 'nativeCalleeBodySourceCredit': 0,
            'nativeCalleesExecuted': [hex(target) for target in sorted(native_callees)],
            'syntheticCalleeContracts': ['037FE2AC deterministic result', 'callback ARM/Thumb ABI clobbers', '037FC290 finite mutex-owner wake plan', '037FD2C0 recorded timer-target call'],
            'limitations': ['Native IRQ and append helpers execute measured native bytes as scaffolding with zero new source credit.', 'Scheduler, timer, lock-test and callback implementations remain explicit bounded contracts rather than physical native execution.', 'Privileged isolated CPSR/RAM execution does not establish hardware interrupt delivery, thread switching, timer timing, or arbitrary malformed pointers.']
        }
        entry['ordinaryCBytes'], entry['justifiedAssemblyBytes'] = size, 0
        matches.append(entry)
    report = {
        'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
        'processor': 'arm7', 'runtimeMappingCanonical': True, 'matches': matches,
        'nativeSymbols': {relocation['symbol']: relocation['target'] for entry in matches for relocation in entry['relocations']},
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False
    }
    write_json(ROOT / 'evidence/matches/arm7-20261029rotated29.json', report)
    print({'functions': len(matches), 'bytes': sum(entry['bytes'] for entry in matches), 'nativeAndRecompiledCalls': sum(entry['oracle']['nativeAndRecompiledCalls'] for entry in matches)})


if __name__ == '__main__':
    main()
