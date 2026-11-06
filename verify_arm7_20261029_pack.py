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

ADDRESS, SIZE, HELPER, ARGUMENT_ADDRESS = 0x03802A0C, 160, 0x03802860, 0x03802924
SOURCE = 'src/arm7/20261029pack33/native_arm7_wram_03802a0c.c'
SOURCE_HASH = 'e051dde42ef9066c332ef4cfe12dfd187448fcf27ea23e441919504cebe6020f'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
WORK = ROOT / 'work/lowlevel-recovery/20261029-arm7-pack-proof'
ARENA, CONTEXT, GLOBAL, STOP = 0x03002000, 0x03002100, 0x03809000, 0x0301E000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def real_link(entry, native, specs):
    if HELPER not in specs or specs[HELPER]['module'] != 'arm7-wram':
        raise ValueError('Formatter helper lacks canonical ARM7 ARM boundary')
    directory = WORK / 'linked'
    directory.mkdir(parents=True, exist_ok=True)
    caller, probe = directory / 'caller.o', directory / 'binding.o'
    with (ROOT / entry['object']).open('rb') as stream:
        elf = ELFFile(stream)
        flags = elf['e_flags']
        split_symbol(elf, entry['name'], caller)
    binding_object('native_arm7_fn_03802860', 'arm', flags, probe)
    lcf = directory / 'unit.lcf'
    lcf.write_text(
        f'MEMORY {{\nCALL: ORIGIN = {ADDRESS:#x} > caller.bin\n'
        f'BIND: ORIGIN = {HELPER:#x} > binding.bin\n}}\nSECTIONS {{\n'
        '.caller: { caller.o(.text) } > CALL\n.binding: { binding.o(.text) } > BIND\n'
        'native_arm7_data_038090c0 = 0x038090c0;\n'
        'native_arm7_data_03802924 = 0x03802924;\n}\n'
    )
    linked, raw = directory / 'linked.elf', directory / 'caller.bin'
    for output in [linked, raw]:
        output.unlink(missing_ok=True)
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm7tdmi', '-main', entry['name'], str(lcf), str(caller), str(probe), '-o', str(linked)]
    process = subprocess.run(command, cwd=directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    anchor_output = directory / 'binding.bin'
    if process.returncode or raw.read_bytes() != native or (anchor_output.exists() and anchor_output.stat().st_size):
        raise ValueError('Real ARM7 formatter caller link differs: ' + process.stdout + process.stderr)
    with linked.open('rb') as stream:
        symbols = list(ELFFile(stream).get_section_by_name('.symtab').iter_symbols())
        symbol = next(symbol for symbol in symbols if symbol.name == entry['name'])
        anchor = next(symbol for symbol in symbols if symbol.name == 'native_arm7_fn_03802860')
        if symbol['st_value'] != ADDRESS or symbol['st_size'] != SIZE or anchor['st_value'] != HELPER or anchor['st_size'] != 0:
            raise ValueError('Linked caller or uninitialized function anchor boundary differs')
    return {
        'exactCallerBytes': True, 'sourceObjectSha256': entry['objectSha256'],
        'splitObjectSha256': sha256(caller), 'linkedCallerSha256': sha256(raw),
        'linkedElf': linked.relative_to(ROOT).as_posix(), 'linkedElfSha256': sha256(linked),
        'lcf': lcf.relative_to(ROOT).as_posix(), 'lcfSha256': sha256(lcf),
        'linkerSha256': LINKER_HASH, 'command': command, 'exitCode': process.returncode,
        'stdout': process.stdout, 'stderr': process.stderr,
        'calleeBinding': {'processor': 'arm7', 'module': 'arm7-wram', 'address': hex(HELPER), 'mode': 'arm', 'initializedCodeBytes': 0},
        'fixedDataAddresses': ['0x038090c0', '0x03802924'],
        'calleeCodeOrSourceCredit': 0, 'wholeModuleLinked': False
    }


def packed(mode, first, second):
    if mode == 1:
        return (second | ((first >> 5) & 8) | ((first & 0xFF) << 8)) & 0xFFFFFFFF
    if mode == 2:
        return (second | (first & 0xFF00) | ((first & 0xFF) << 16)) & 0xFFFFFFFF
    return (second | ((first >> 8) & 0xFF00) | ((first & 0xFF00) << 8) | ((first & 0xFF) << 24)) & 0xFFFFFFFF


def execute(code, mode, first, second, result, seed, thumb, boundary=False):
    rng = random.Random(0x202610293300 + seed)
    arena, shared = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
    struct.pack_into('<I', arena, CONTEXT - ARENA + 0x28, mode & 0xFFFFFFFF)
    struct.pack_into('<I', shared, 0xC0, CONTEXT)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(0x037F8000, 0x20000)
    uc.mem_map(0x03000000, 0x20000)
    uc.mem_write(ADDRESS, code)
    uc.mem_write(ARENA, bytes(arena))
    uc.mem_write(GLOBAL, bytes(shared))
    uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    initial = [rng.getrandbits(32) for unused in matcher.common.REGISTERS]
    initial[:2], initial[-2:] = [first, second], [0x0301FF00, STOP | int(thumb)]
    for register, value in zip(matcher.common.REGISTERS, initial):
        uc.reg_write(register, value)
    calls, writes, visited = [], [], set()
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value]))
    def observe(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + SIZE:
            visited.add(address)
            return
        if address != HELPER or calls:
            raise ValueError('Formatter escaped its one explicit helper contract')
        arguments = [uc.reg_read(register) for register in matcher.common.REGISTERS[:4]]
        if arguments[1:] != [0, (mode + 1) & 0xFFFFFFFF, ARGUMENT_ADDRESS]:
            raise ValueError('Formatter helper register words differ')
        if not 0x0301F000 <= arguments[0] <= 0x0301FF00:
            raise ValueError('Formatted word pointer escaped the valid stack frame')
        if boundary:
            calls.append({'arguments': arguments, 'bufferInterpreted': False})
            uc.emu_stop()
            return
        actual_word = struct.unpack('<I', bytes(uc.mem_read(arguments[0], 4)))[0]
        if actual_word != packed(mode, first, second):
            raise ValueError('Independent unsigned byte/flag packing model differs')
        calls.append({'arguments': arguments, 'bufferWord': actual_word, 'bufferInterpreted': True})
        returned = uc.reg_read(matcher.common.REGISTERS[-1])
        for register in [*matcher.common.REGISTERS[:4], matcher.common.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.common.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | ((returned & 1) << 5))
        uc.reg_write(UC_ARM_REG_PC, returned & ~1)
    uc.hook_add(UC_HOOK_CODE, observe)
    uc.emu_start(ADDRESS, STOP, count=500)
    registers = [uc.reg_read(register) for register in matcher.common.REGISTERS]
    pc, cpsr = uc.reg_read(UC_ARM_REG_PC), uc.reg_read(UC_ARM_REG_CPSR)
    if not calls or bytes(uc.mem_read(ARENA, 4096)) != arena or bytes(uc.mem_read(GLOBAL, 4096)) != shared:
        raise ValueError('Formatter changed context/global RAM or missed its helper')
    if boundary:
        if pc != HELPER:
            raise ValueError('Unsupported mode did not stop before helper interpretation')
    elif pc != STOP or registers[0] != result or registers[4:12] != initial[4:12] or registers[-2] != initial[-2] or cpsr & 0x3F != 0x10 | (0x20 if thumb else 0):
        raise ValueError('Formatter failed actual return/result/preservation/mode model')
    return {'registers': registers, 'pc': pc, 'cpsr': cpsr, 'calls': calls, 'writes': writes, 'visited': sorted(visited), 'stackSha256': digest(bytes(uc.mem_read(0x0301F000, 4096)))}


def main():
    if sha256(ROOT / SOURCE) != SOURCE_HASH or sha256(COMPILER) != COMPILER_HASH or sha256(LINKER) != LINKER_HASH:
        raise ValueError('Frozen formatter source/compiler/linker differs')
    matcher.WORK = WORK / 'compile'
    specs = {spec['address']: spec for spec in matcher.candidates(10000)}
    spec = specs[ADDRESS]
    if spec['bytes'] != SIZE or spec['module'] != 'arm7-wram':
        raise ValueError('Canonical formatter function boundary differs')
    for output in (matcher.WORK / 'compile' / (ROOT / SOURCE).stem).glob('*.o'):
        output.unlink()
    entry, code = matcher.compare(ROOT / SOURCE, spec, COMPILER, COMPILER_HASH, 2, 'off')
    if code is None:
        raise ValueError('Complete ordinary C formatter body stopped matching')
    offset = ADDRESS - spec['base']
    native = (ROOT / spec['binary']).read_bytes()[offset:offset + SIZE]
    entry['isolatedRealMwCallerLink'] = real_link(entry, native, specs)
    first_values = [0, 1, 0xFF, 0x100, 0x101, 0xFFFF, 0x10000, 0x80000000, 0xFFFFFFFF, 0x11223344]
    vectors = itertools.product([1, 2, 3], first_values, [0, 1, 0x80, 0xA5, 0xFFFFFFFF], [0, 1, 0x80000000, 0xFFFFFFFF])
    hashes, covered = [], set()
    for index, (mode, first, second, result) in enumerate(vectors):
        for thumb in [False, True]:
            original = execute(native, mode, first, second, result, index, thumb)
            rebuilt = execute(code, mode, first, second, result, index, thumb)
            if original != rebuilt:
                raise ValueError('Fresh native/source formatter machines differ')
            hashes.append(digest(json.dumps(original, sort_keys=True).encode()))
            covered.update(original['visited'])
    boundary_hashes = []
    for mode in [-1, 0, 4]:
        original = execute(native, mode, 0x11223344, 0xA5, 0, 0, False, True)
        rebuilt = execute(code, mode, 0x11223344, 0xA5, 0, 0, False, True)
        if original != rebuilt:
            raise ValueError('Native/source unsupported-mode boundary states differ')
        boundary_hashes.append(digest(json.dumps(original, sort_keys=True).encode()))
        covered.update(original['visited'])
    if covered != {instruction.address for instruction in spec['instructions']}:
        raise ValueError('Returning and boundary fixtures did not cover every caller instruction')
    entry['ordinaryCBytes'], entry['justifiedAssemblyBytes'] = SIZE, 0
    entry['oracle'] = {
        'cases': len(hashes), 'nativeAndRecompiledCalls': len(hashes) * 2, 'verifiedReturn': True,
        'supportedModes': [1, 2, 3], 'returnModes': ['arm', 'thumb'], 'instructionLimit': 500,
        'stateSha256': hashes, 'nativeInstructions': len(spec['instructions']),
        'nativeInstructionCoverageIncludingSeparateBoundaryProbes': len(covered), 'externalCalleesExecuted': 0,
        'independentModel': 'Unsigned byte/flag packing, complete four-byte stack value, all helper argument words, unchanged RAM/global pages, result R0, R4-R11/SP and return modes',
        'limitations': ['The external helper uses an explicit deterministic return/ABI-clobber contract; no physical device or callback behavior is executed.', 'Modes outside1/2/3 leave the native stack word uninitialized and remain unsupported; separate probes stop before its interpretation.', 'Original API names and peripheral meanings remain inferred.']
    }
    entry['unsupportedModeBoundaryProbes'] = {
        'modes': [-1, 0, 4], 'cases': len(boundary_hashes), 'nativeAndRecompiledExecutions': len(boundary_hashes) * 2,
        'stateSha256': boundary_hashes, 'stoppedAtAddress': hex(HELPER),
        'bufferInterpreted': False, 'actualReturnClaimed': False
    }
    report = {
        'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
        'processor': 'arm7', 'runtimeMappingCanonical': True, 'matches': [entry],
        'nativeSymbols': {relocation['symbol']: relocation['target'] for relocation in entry['relocations']},
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False
    }
    write_json(ROOT / 'evidence/matches/arm7-20261029pack33.json', report)
    print({'functions': 1, 'bytes': SIZE, 'returningExecutions': len(hashes) * 2, 'boundaryExecutions': len(boundary_hashes) * 2})


if __name__ == '__main__':
    main()
