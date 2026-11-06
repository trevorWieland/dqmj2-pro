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
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC
import match_arm7 as matcher
from elf_units import split_symbol
from link_runtime_unit import binding_object

PINS = {
    0x037FD898: '06bd323ec383b8951fe194c2f505296892928cbd5bf237a7bac1774dd2f89824',
    0x037FD928: '377000681c55119980b6a61c195616cd9d9063968cdaf71f1b7731caddb5d261'
}
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
WORK = ROOT / 'work/lowlevel-recovery/20261029-arm7-scanline-proof'
ARENA, OBJECT, MMIO, STOP = 0x03002000, 0x03002100, 0x04000000, 0x0301E000
IRQ = [0x037FDD00, 0x037FDD14]


def digest(data):
    return hashlib.sha256(data).hexdigest()


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
        binding = {'name': name, 'address': hex(target), 'processor': 'arm7'}
        if name.startswith('native_arm7_fn_'):
            if target not in specs or specs[target]['module'] != 'arm7-wram':
                raise ValueError('Callee lacks qualified canonical ARM7 ARM boundary')
            probe = directory / f'binding{index}.o'
            binding_object(name, 'arm', flags, probe)
            memory.append(f'BIND{index}: ORIGIN = {target:#x} > binding{index}.bin')
            sections.append(f'.binding{index}: {{ binding{index}.o(.text) }} > BIND{index}')
            objects.append(probe)
            binding.update(kind='function', module='arm7-wram', mode='arm', initializedCodeBytes=0, sourceCredit=0)
        else:
            if name != 'native_arm7_data_04000006' or target != MMIO + 6:
                raise ValueError('Unexpected fixed hardware data binding')
            assignments.append(f'{name} = {target:#x};')
            binding.update(kind='hardware-data', mode='data', accessWidthBytes=2)
        bindings.append(binding)
    lcf = directory / 'unit.lcf'
    lcf.write_text('MEMORY {\n' + '\n'.join(memory) + '\n}\nSECTIONS {\n' + '\n'.join(sections + assignments) + '\n}\n')
    linked, raw = directory / 'linked.elf', directory / 'caller.bin'
    for output in [linked, raw]:
        output.unlink(missing_ok=True)
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm7tdmi', '-main', entry['name'], str(lcf), *map(str, objects), '-o', str(linked)]
    process = subprocess.run(command, cwd=directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    if process.returncode or raw.read_bytes() != native:
        raise ValueError('Real ARM7 scanline caller link differs: ' + process.stdout + process.stderr)
    with linked.open('rb') as stream:
        symbols = list(ELFFile(stream).get_section_by_name('.symtab').iter_symbols())
        symbol = next(symbol for symbol in symbols if symbol.name == entry['name'])
        if symbol['st_value'] != int(entry['address'], 0) or symbol['st_size'] != entry['bytes']:
            raise ValueError('Linked source caller boundary differs')
        for binding in bindings:
            if binding['kind'] == 'function':
                symbol = next(symbol for symbol in symbols if symbol.name == binding['name'])
                if symbol['st_value'] != int(binding['address'], 0) or symbol['st_size'] != 0:
                    raise ValueError('Uninitialized function anchor acquired executable bytes')
    if any(path.stat().st_size for path in directory.glob('binding*.bin')):
        raise ValueError('Mode anchor emitted initialized callee bytes')
    return {
        'exactCallerBytes': True, 'sourceObjectSha256': entry['objectSha256'],
        'splitObjectSha256': sha256(caller), 'linkedCallerSha256': sha256(raw),
        'linkedElf': linked.relative_to(ROOT).as_posix(), 'linkedElfSha256': sha256(linked),
        'lcf': lcf.relative_to(ROOT).as_posix(), 'lcfSha256': sha256(lcf),
        'linkerSha256': LINKER_HASH, 'command': command, 'exitCode': process.returncode,
        'stdout': process.stdout, 'stderr': process.stderr, 'qualifiedBindings': bindings,
        'calleeCodeOrSourceCredit': 0, 'wholeModuleLinked': False
    }


def execute(code, spec, specs, vector, seed, thumb, initial_irq, invalid=None):
    line, threshold, frame = vector
    rng = random.Random(0x202610293000 + seed)
    before, hardware = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
    struct.pack_into('<H', hardware, 6, line)
    struct.pack_into('<I', before, OBJECT - ARENA, 0 if invalid != 'active' else 1)
    second = [-32768, -1, 0, 32767][seed % 4]
    handler = 0 if seed % 5 == 0 else rng.getrandbits(32)
    userdata = [0, 0xFFFFFFFF, rng.getrandbits(32)][seed % 3]
    arguments = [0 if invalid == 'null' else OBJECT, threshold & 0xFFFFFFFF, second & 0xFFFFFFFF, handler]
    expected, expected_writes = bytearray(before), []
    if invalid is None:
        output = (frame + int(threshold <= line)) & 0xFFFFFFFF
        fields = [(0x1C, int(spec['address'] == 0x037FD928), 4), (0x10, threshold & 0xFFFF, 2), (0xC, output, 4), (0x12, second & 0xFFFF, 2), (0, handler, 4), (4, userdata, 4), (0x24, 0, 4)]
        for offset, value, size in fields:
            struct.pack_into('<I' if size == 4 else '<H', expected, OBJECT - ARENA + offset, value)
            expected_writes.append([OBJECT + offset, size, value])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for base, size in [(0x037F8000, 0x20000), (0x03000000, 0x20000), (MMIO, 0x1000)]:
        uc.mem_map(base, size)
    for target in IRQ:
        callee = specs[target]
        binary = (ROOT / callee['binary']).read_bytes()
        uc.mem_write(target, binary[target - callee['base']:target - callee['base'] + callee['bytes']])
    uc.mem_write(spec['address'], code)
    uc.mem_write(ARENA, bytes(before))
    uc.mem_write(MMIO, bytes(hardware))
    uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x1F | initial_irq)
    initial = [rng.getrandbits(32) for unused in matcher.common.REGISTERS]
    initial[:4], initial[-2:] = arguments, [0x0301FF00, STOP | int(thumb)]
    for register, value in zip(matcher.common.REGISTERS, initial):
        uc.reg_write(register, value)
    uc.mem_write(initial[-2], struct.pack('<I', userdata))
    writes, all_writes, calls, reads, visited = [], [], [], [], set()
    def record(uc, access, address, size, value, user):
        all_writes.append([address, size, value])
        if ARENA <= address < ARENA + 4096:
            writes.append([address, size, value])
    def read(uc, access, address, size, value, user):
        if MMIO <= address < MMIO + 4096:
            reads.append([address, size])
    def observe(uc, address, size, user):
        if spec['address'] <= address < spec['address'] + len(code):
            visited.add(address)
            return
        for target in IRQ:
            if target <= address < target + specs[target]['bytes']:
                if target == address:
                    calls.append([target, [] if target == IRQ[0] else [uc.reg_read(matcher.common.REGISTERS[0])]])
                return
        if address == 0x037FDE70:
            if invalid is None:
                raise ValueError('Valid scanline record unexpectedly reached panic boundary')
            calls.append([address, []])
            uc.emu_stop()
            return
        if address not in [0x037FDCA8, 0x037FD7A8] or invalid is not None:
            raise ValueError('Scanline caller escaped its bounded contracts')
        calls.append([address, [uc.reg_read(matcher.common.REGISTERS[0])]])
        returned = uc.reg_read(matcher.common.REGISTERS[-1])
        for register in [*matcher.common.REGISTERS[:4], matcher.common.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        if address == 0x037FDCA8:
            uc.reg_write(matcher.common.REGISTERS[0], frame)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | (uc.reg_read(UC_ARM_REG_CPSR) & 0xDF) | ((returned & 1) << 5))
        uc.reg_write(UC_ARM_REG_PC, returned & ~1)
    uc.hook_add(UC_HOOK_CODE, observe)
    uc.hook_add(UC_HOOK_MEM_WRITE, record)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.emu_start(spec['address'], STOP, count=2000)
    registers = [uc.reg_read(register) for register in matcher.common.REGISTERS]
    pc, cpsr = uc.reg_read(UC_ARM_REG_PC), uc.reg_read(UC_ARM_REG_CPSR)
    expected_calls = [[IRQ[0], []], [0x037FDE70, []]] if invalid else [[IRQ[0], []], [0x037FDCA8, [line]], [0x037FD7A8, [OBJECT]], [IRQ[1], [initial_irq & 0x80]]]
    if calls != expected_calls or writes != expected_writes or bytes(uc.mem_read(ARENA, 4096)) != expected:
        raise ValueError('Independent complete-record/ordered-store/call model differs')
    if bytes(uc.mem_read(MMIO, 4096)) != hardware or reads != ([] if invalid else [[MMIO + 6, 2]]):
        raise ValueError('Sampled hardware halfword was changed or read incorrectly')
    if invalid:
        if pc != 0x037FDE70 or cpsr & 0xFF != 0x1F | initial_irq | 0x80:
            raise ValueError('Invalid record did not stop at the expected guarded panic entry')
    else:
        if pc != STOP or registers[0] != 0x80 or registers[4:12] != initial[4:12] or registers[-2] != initial[-2]:
            raise ValueError('Valid record failed actual return/result/preservation model')
        if cpsr & 0xFF != 0x1F | initial_irq | (0x20 if thumb else 0):
            raise ValueError('Native IRQ helpers did not restore initial control/return state')
    return {'registers': registers, 'pc': pc, 'cpsr': cpsr, 'calls': calls, 'writes': writes, 'stackAndCallerWrites': all_writes, 'hardwareReads': reads, 'visited': sorted(visited), 'memorySha256': digest(bytes(uc.mem_read(ARENA, 4096)))}


def main():
    if sha256(COMPILER) != COMPILER_HASH or sha256(LINKER) != LINKER_HASH:
        raise ValueError('Pinned compiler/linker differs')
    matcher.WORK = WORK / 'compile'
    specs = {spec['address']: spec for spec in matcher.candidates(10000)}
    vectors = list(itertools.product([0, 1, 191, 262, 263, 65535], [-32768, -1, 0, 1, 191, 263, 32767], [0, 0xFFFFFFFF]))
    matches = []
    for address, source_hash in PINS.items():
        spec = specs[address]
        source = ROOT / f'src/arm7/20261029rotated30/native_arm7_wram_{address:08x}.c'
        if spec['bytes'] != 144 or spec['module'] != 'arm7-wram' or sha256(source) != source_hash:
            raise ValueError('Frozen scanline-record source/native boundary differs')
        for output in (matcher.WORK / 'compile' / source.stem).glob('*.o'):
            output.unlink()
        entry, code = matcher.compare(source, spec, COMPILER, COMPILER_HASH, 2, 'off')
        if code is None:
            raise ValueError('Complete scanline-record C body no longer matches')
        offset = address - spec['base']
        native = (ROOT / spec['binary']).read_bytes()[offset:offset + spec['bytes']]
        entry['isolatedRealMwCallerLink'] = real_link(entry, native, specs)
        hashes, covered = [], set()
        for index, vector in enumerate(vectors):
            for initial_irq in [0, 0x40, 0x80, 0xC0]:
                for thumb in [False, True]:
                    first = execute(native, spec, specs, vector, index, thumb, initial_irq)
                    second = execute(code, spec, specs, vector, index, thumb, initial_irq)
                    if first != second:
                        raise ValueError('Fresh native/source scanline-record machines differ')
                    hashes.append(digest(json.dumps(first, sort_keys=True).encode()))
                    covered.update(first['visited'])
        guards = []
        for invalid in ['null', 'active']:
            for initial_irq in [0, 0x40, 0x80, 0xC0]:
                first = execute(native, spec, specs, vectors[0], 0, False, initial_irq, invalid)
                second = execute(code, spec, specs, vectors[0], 0, False, initial_irq, invalid)
                if first != second:
                    raise ValueError('Native/source guarded panic-entry states differ')
                guards.append(digest(json.dumps(first, sort_keys=True).encode()))
                covered.update(first['visited'])
        if covered != {instruction.address for instruction in spec['instructions']}:
            raise ValueError('Returning and guard fixtures did not cover every native caller instruction')
        entry['ordinaryCBytes'], entry['justifiedAssemblyBytes'] = spec['bytes'], 0
        entry['oracle'] = {
            'cases': len(hashes), 'nativeAndRecompiledCalls': len(hashes) * 2, 'verifiedReturn': True,
            'returnModes': ['arm', 'thumb'], 'instructionLimit': 2000, 'stateSha256': hashes,
            'nativeInstructionCoverageIncludingSeparateGuardChecks': len(covered), 'nativeInstructions': len(spec['instructions']),
            'independentModel': 'One sampled hardware halfword, signed threshold and unsigned frame wrap, all record writes/calls, fifth stack argument, R0/R4-R11/SP, IRQ/FIQ restoration',
            'nativeCalleesExecuted': [hex(target) for target in IRQ], 'nativeCalleeBodySourceCredit': 0,
            'limitations': ['Native IRQ helper bytes execute only as scaffolding with zero new source credit.', 'Counter and queue implementations are explicit return/ABI-clobber contracts; the MMIO page is a synthetic bounded register model.', 'Physical scanline timing, queue side effects and panic implementation behavior remain unverified.']
        }
        entry['guardEntryChecks'] = {
            'cases': len(guards), 'nativeAndRecompiledExecutions': len(guards) * 2, 'stateSha256': guards,
            'stoppedAtAddress': '0x037fde70', 'actualReturnClaimed': False,
            'scope': 'Null/in-use input guards reach the canonical panic entry before object/MMIO writes; deliberate stop does not characterize the panic body.'
        }
        matches.append(entry)
    report = {
        'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
        'processor': 'arm7', 'runtimeMappingCanonical': True, 'matches': matches,
        'nativeSymbols': {relocation['symbol']: relocation['target'] for entry in matches for relocation in entry['relocations']},
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False
    }
    write_json(ROOT / 'evidence/matches/arm7-20261029rotated30.json', report)
    print({'functions': len(matches), 'bytes': 288, 'returningExecutions': sum(entry['oracle']['nativeAndRecompiledCalls'] for entry in matches), 'guardEntryExecutions': sum(entry['guardEntryChecks']['nativeAndRecompiledExecutions'] for entry in matches)})


if __name__ == '__main__':
    main()
