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

ADDRESS, SIZE = 0x027F1584, 252
SOURCE = 'src/arm7/20261029packet32/native_arm7_main_027f1584.c'
SOURCE_HASH = 'dc65ee77cc4f583dd1ad0b3dcd4bc1addee7fea4a5ee7f73bac50c0aaaee6167'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
WORK = ROOT / 'work/lowlevel-recovery/20261029-arm7-packet-proof'
ARENA, GLOBAL, STOP = 0x03002000, 0x0380F000, 0x0301E000
BUFFER, PAYLOAD, RECORD = ARENA + 0x900, ARENA + 0xD00, ARENA + 0x344
CALLEES = [0x027EAC88, 0x027EAD30, 0x037FDF9C]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def real_link(entry, native, specs):
    directory = WORK / 'linked'
    directory.mkdir(parents=True, exist_ok=True)
    caller = directory / 'caller.o'
    with (ROOT / entry['object']).open('rb') as stream:
        elf = ELFFile(stream)
        flags = elf['e_flags']
        split_symbol(elf, entry['name'], caller)
    memory = [f'CALL: ORIGIN = {ADDRESS:#x} > caller.bin']
    sections, assignments, objects, bindings = ['.caller: { caller.o(.text) } > CALL'], [], [caller], []
    for index, relocation in enumerate(entry['relocations']):
        name, target = relocation['symbol'], int(relocation['target'], 0)
        if any(binding['name'] == name for binding in bindings):
            continue
        binding = {'name': name, 'address': hex(target), 'processor': 'arm7'}
        if name.startswith('native_arm7_fn_'):
            if target not in specs:
                raise ValueError('ARM7 callee lacks a canonical ARM function boundary')
            probe = directory / f'binding{index}.o'
            binding_object(name, 'arm', flags, probe)
            memory.append(f'BIND{index}: ORIGIN = {target:#x} > binding{index}.bin')
            sections.append(f'.binding{index}: {{ binding{index}.o(.text) }} > BIND{index}')
            objects.append(probe)
            binding.update(kind='function', module=specs[target]['module'], mode='arm', initializedCodeBytes=0, sourceCredit=0)
        else:
            if target not in [0x0380FFF0, 0x0380FFF4]:
                raise ValueError('Unexpected fixed shared-RAM data binding')
            assignments.append(f'{name} = {target:#x};')
            binding.update(kind='fixed-shared-ram-data', mode='data')
        bindings.append(binding)
    lcf = directory / 'unit.lcf'
    lcf.write_text('MEMORY {\n' + '\n'.join(memory) + '\n}\nSECTIONS {\n' + '\n'.join(sections + assignments) + '\n}\n')
    linked, raw = directory / 'linked.elf', directory / 'caller.bin'
    for output in [linked, raw]:
        output.unlink(missing_ok=True)
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm7tdmi', '-main', entry['name'], str(lcf), *map(str, objects), '-o', str(linked)]
    process = subprocess.run(command, cwd=directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    if process.returncode or raw.read_bytes() != native:
        raise ValueError('Real ARM7 packet caller link differs: ' + process.stdout + process.stderr)
    with linked.open('rb') as stream:
        symbols = list(ELFFile(stream).get_section_by_name('.symtab').iter_symbols())
        symbol = next(symbol for symbol in symbols if symbol.name == entry['name'])
        if symbol['st_value'] != ADDRESS or symbol['st_size'] != SIZE:
            raise ValueError('Linked packet caller symbol boundary differs')
        for binding in bindings:
            if binding['kind'] == 'function':
                symbol = next(symbol for symbol in symbols if symbol.name == binding['name'])
                if symbol['st_value'] != int(binding['address'], 0) or symbol['st_size'] != 0:
                    raise ValueError('Mode anchor acquired executable callee credit')
    if any(path.stat().st_size for path in directory.glob('binding*.bin')):
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


def fixture(vector, seed):
    length, prefix, marker, shared_word = vector
    rng = random.Random(0x202610293200 + seed)
    before, shared = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
    struct.pack_into('<I', shared, 0xFF4, ARENA)
    struct.pack_into('<H', shared, 0xFF0, shared_word)
    struct.pack_into('<H', before, RECORD - ARENA + 0xA0, length)
    struct.pack_into('<H', before, RECORD - ARENA + 0x96, prefix)
    struct.pack_into('<H', before, RECORD - ARENA + 0xA2, (rng.getrandbits(16) & ~1) | (prefix & 1))
    struct.pack_into('<I', before, RECORD - ARENA + 0x9C, PAYLOAD)
    struct.pack_into('<I', before, 0x4AC, BUFFER)
    struct.pack_into('<H', before, 0x690, (rng.getrandbits(16) & ~4) | marker)
    expected, writes, calls = bytearray(before), [], []
    cursor = BUFFER + 0x24 + prefix
    def half(address, value):
        struct.pack_into('<H', expected, address - ARENA, value)
        writes.append([address, 2, value])
    def byte(address, value):
        calls.append([0x027EAD30, [address, value]])
        aligned = address & ~1
        old = struct.unpack_from('<H', expected, aligned - ARENA)[0]
        half(aligned, (old & 0xFF) | (value << 8) if address & 1 else (old & 0xFF00) | value)
    if length:
        count = length + (2 if prefix & 1 else 1)
        target = cursor + (9 if prefix & 1 else 10)
        rounded = (count + 1) & ~1
        calls += [[0x027EAC88, [target, PAYLOAD, count]], [0x037FDF9C, [PAYLOAD, target, rounded]]]
        for offset in range(0, rounded, 2):
            half(target + offset, struct.unpack_from('<H', expected, PAYLOAD - ARENA + offset)[0])
        if prefix & 1:
            byte(cursor + 9, shared_word >> 8)
    half(BUFFER + 0xA, prefix + 0x26 + length)
    byte(cursor + 1, (length + 8) & 0xFF)
    if marker:
        target = (cursor + 0xD + length) & ~3
        half(target, 0xB6B8)
        half(target + 2, 0x1D46)
    half(RECORD + 0xA4, 0)
    return bytes(before), bytes(shared), bytes(expected), writes, calls


def execute(code, spec, specs, data, seed, thumb):
    before, shared, expected, expected_writes, expected_calls = data
    rng = random.Random(0x202610293201 + seed)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for base, size in [(0x027E0000, 0x20000), (0x037F8000, 0x20000), (0x03000000, 0x20000)]:
        uc.mem_map(base, size)
    for target in CALLEES:
        callee = specs[target]
        binary = (ROOT / callee['binary']).read_bytes()
        uc.mem_write(target, binary[target - callee['base']:target - callee['base'] + callee['bytes']])
    uc.mem_write(ADDRESS, code)
    uc.mem_write(ARENA, before)
    uc.mem_write(GLOBAL, shared)
    uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    initial = [rng.getrandbits(32) for unused in matcher.common.REGISTERS]
    initial[-2:] = [0x0301FF00, STOP | int(thumb)]
    for register, value in zip(matcher.common.REGISTERS, initial):
        uc.reg_write(register, value)
    writes, all_writes, calls, visited = [], [], [], set()
    def record(uc, access, address, size, value, user):
        all_writes.append([address, size, value])
        if ARENA <= address < ARENA + 4096 or GLOBAL <= address < GLOBAL + 4096:
            writes.append([address, size, value])
    def observe(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + SIZE:
            visited.add(address)
            return
        for target in CALLEES:
            if target <= address < target + specs[target]['bytes']:
                if address == target:
                    count = 2 if target == 0x027EAD30 else 3
                    calls.append([target, [uc.reg_read(register) for register in matcher.common.REGISTERS[:count]]])
                return
        raise ValueError('Packet caller escaped its measured caller/helper bodies')
    uc.hook_add(UC_HOOK_MEM_WRITE, record)
    uc.hook_add(UC_HOOK_CODE, observe)
    uc.emu_start(ADDRESS, STOP, count=10000)
    registers = [uc.reg_read(register) for register in matcher.common.REGISTERS]
    if uc.reg_read(UC_ARM_REG_PC) != STOP or registers[0] != 0 or registers[4:12] != initial[4:12] or registers[-2] != initial[-2]:
        raise ValueError('Packet caller failed actual return/result/preservation model')
    if uc.reg_read(UC_ARM_REG_CPSR) & 0x3F != 0x10 | (0x20 if thumb else 0):
        raise ValueError('Packet caller returned in a different instruction/CPU mode')
    if bytes(uc.mem_read(ARENA, 4096)) != expected or bytes(uc.mem_read(GLOBAL, 4096)) != shared or writes != expected_writes or calls != expected_calls:
        raise ValueError('Independent complete-buffer/shared-word/copy/ordered-store/call model differs')
    return {'registers': registers, 'cpsr': uc.reg_read(UC_ARM_REG_CPSR), 'writes': writes, 'stackAndNativeWrites': all_writes, 'calls': calls, 'visited': sorted(visited), 'memorySha256': digest(bytes(uc.mem_read(ARENA, 4096)))}


def main():
    if sha256(ROOT / SOURCE) != SOURCE_HASH or sha256(COMPILER) != COMPILER_HASH or sha256(LINKER) != LINKER_HASH:
        raise ValueError('Frozen packet source/compiler/linker differs')
    matcher.WORK = WORK / 'compile'
    specs = {spec['address']: spec for spec in matcher.candidates(10000)}
    spec = specs[ADDRESS]
    if spec['bytes'] != SIZE or spec['module'] != 'arm7-main':
        raise ValueError('Canonical ARM7 main function boundary differs')
    source = ROOT / SOURCE
    for output in (matcher.WORK / 'compile' / source.stem).glob('*.o'):
        output.unlink()
    entry, code = matcher.compare(source, spec, COMPILER, COMPILER_HASH, 2, 'off')
    if code is None:
        raise ValueError('Complete packet C body no longer matches')
    offset = ADDRESS - spec['base']
    native = (ROOT / spec['binary']).read_bytes()[offset:offset + SIZE]
    entry['isolatedRealMwCallerLink'] = real_link(entry, native, specs)
    hashes, covered = [], set()
    vectors = list(itertools.product([0, 1, 2, 3, 4, 7, 8, 255], [0, 1, 4, 5, 14, 15], [0, 4], [0, 0x1234, 0xFFFF]))
    for index, vector in enumerate(vectors):
        data = fixture(vector, index)
        for thumb in [False, True]:
            first = execute(native, spec, specs, data, index, thumb)
            second = execute(code, spec, specs, data, index, thumb)
            if first != second:
                raise ValueError('Fresh native/source packet machines differ')
            covered.update(first['visited'])
            hashes.append(digest(json.dumps(first, sort_keys=True).encode()))
    if covered != {instruction.address for instruction in spec['instructions']}:
        raise ValueError('Packet fixtures did not cover every native caller instruction')
    entry['ordinaryCBytes'], entry['justifiedAssemblyBytes'] = SIZE, 0
    entry['reconstructionChoices'] = ['Unsigned16-bit marker store retains the measured zero-extended literal; signed16-bit storage produced a different literal pool despite identical low halfword stores.']
    entry['oracle'] = {
        'cases': len(hashes), 'nativeAndRecompiledCalls': len(hashes) * 2, 'verifiedReturn': True,
        'returnModes': ['arm', 'thumb'], 'instructionLimit': 10000, 'stateSha256': hashes,
        'nativeInstructionCoverage': len(covered), 'nativeInstructions': len(spec['instructions']),
        'nativeCalleesExecuted': [hex(target) for target in CALLEES], 'nativeCalleeBodySourceCredit': 0,
        'syntheticCalleeContracts': [],
        'independentModel': 'Rounded-even payload copy, halfword-preserving byte writes, length/header/marker fields and all ordered stores/call arguments, complete RAM/shared page, R0/R4-R11/SP and return modes',
        'limitations': ['Measured native copy/write helpers execute as scaffolding with zero new source credit.', 'Fixture lengths keep aligned payload copies and all fields within a bounded valid RAM arena; arbitrary overlapping/unmapped pointers are unsupported.', 'Packet and marker meanings are structural inferences; physical wireless memory behavior and external transmission are unverified.']
    }
    report = {
        'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
        'processor': 'arm7', 'runtimeMappingCanonical': True, 'matches': [entry],
        'nativeSymbols': {relocation['symbol']: relocation['target'] for relocation in entry['relocations']},
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False
    }
    write_json(ROOT / 'evidence/matches/arm7-20261029packet32.json', report)
    print({'functions': 1, 'bytes': SIZE, 'nativeAndRecompiledCalls': len(hashes) * 2})


if __name__ == '__main__':
    main()
