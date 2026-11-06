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

ADDRESS, SIZE = 0x027E54E8, 248
SOURCE = 'src/arm7/20261029mode34/native_arm7_main_027e54e8.c'
SOURCE_HASH = '43ebbca880b10b884f50f6f5ef874d959c40bfd745a30e4d606c43ac3fa786ab'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
WORK = ROOT / 'work/lowlevel-recovery/20261029-arm7-mode-proof'
ARENA, GLOBAL, STOP = 0x03002000, 0x027F8000, 0x0301E000
REQUEST, CONTEXT, RESPONSE, PAYLOAD, FIRST_MESSAGE, FINAL_MESSAGE = [ARENA + n for n in [0x100, 0x200, 0x600, 0x700, 0x900, 0xA00]]
NATIVE_HELPERS = [0x037FE070, 0x037FE12C]


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
                raise ValueError('Mode caller callee lacks qualified canonical ARM7 ARM entry')
            probe = directory / f'binding{index}.o'
            binding_object(name, 'arm', flags, probe)
            memory.append(f'BIND{index}: ORIGIN = {target:#x} > binding{index}.bin')
            sections.append(f'.binding{index}: {{ binding{index}.o(.text) }} > BIND{index}')
            objects.append(probe)
            binding.update(kind='function', module=specs[target]['module'], mode='arm', initializedCodeBytes=0, sourceCredit=0)
        else:
            if target != 0x027F8884:
                raise ValueError('Unexpected shared-context data relocation')
            assignments.append(f'{name} = {target:#x};')
            binding.update(kind='data', module='arm7-main', mode='data')
        bindings.append(binding)
    lcf = directory / 'unit.lcf'
    lcf.write_text('MEMORY {\n' + '\n'.join(memory) + '\n}\nSECTIONS {\n' + '\n'.join(sections + assignments) + '\n}\n')
    linked, raw = directory / 'linked.elf', directory / 'caller.bin'
    for output in [linked, raw]:
        output.unlink(missing_ok=True)
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm7tdmi', '-main', entry['name'], str(lcf), *map(str, objects), '-o', str(linked)]
    process = subprocess.run(command, cwd=directory, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    if process.returncode or raw.read_bytes() != native:
        raise ValueError('Real mode caller MW link differs: ' + process.stdout + process.stderr)
    with linked.open('rb') as stream:
        symbols = list(ELFFile(stream).get_section_by_name('.symtab').iter_symbols())
        symbol = next(symbol for symbol in symbols if symbol.name == entry['name'])
        if symbol['st_value'] != ADDRESS or symbol['st_size'] != SIZE:
            raise ValueError('Linked mode caller symbol boundary differs')
        for binding in bindings:
            if binding['kind'] == 'function':
                symbol = next(symbol for symbol in symbols if symbol.name == binding['name'])
                if symbol['st_value'] != int(binding['address'], 0) or symbol['st_size'] != 0:
                    raise ValueError('Mode binding acquired executable callee source credit')
    if any(path.stat().st_size for path in directory.glob('binding*.bin')):
        raise ValueError('Mode binding emitted initialized callee bytes')
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
    raw_mode, status, alignment, result, stack_response = vector
    rng = random.Random(0x202610293400 + seed)
    before, shared = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
    setting = rng.getrandbits(32)
    struct.pack_into('<I', shared, 0xDD4, CONTEXT)
    struct.pack_into('<III', before, REQUEST - ARENA + 4, raw_mode, PAYLOAD + alignment, setting)
    struct.pack_into('<H', before, RESPONSE - ARENA + 4, status)
    expected, caller_writes = bytearray(before), []
    def put(address, value, size):
        struct.pack_into('<I' if size == 4 else '<H', expected, address - ARENA, value)
        caller_writes.append([address, size, value])
    mode = raw_mode & 0xFFFF
    put(CONTEXT + 0x196, mode, 2)
    enabled = int(mode in [1, 2, 3])
    put(CONTEXT + 0x198, enabled, 4)
    expected[CONTEXT - ARENA + 0x19C:CONTEXT - ARENA + 0x1EC] = before[PAYLOAD - ARENA + alignment:PAYLOAD - ARENA + alignment + 80] if enabled else bytes(80)
    put(CONTEXT + 0xC4, setting & 0xFFFF, 2)
    if status:
        for offset, value in [(0, 0x14), (2, 1), (4, 0x207), (6, status)]:
            put(FIRST_MESSAGE + offset, value, 2)
    put(FINAL_MESSAGE, 0x27, 2)
    put(FINAL_MESSAGE + 2, 0, 2)
    calls = [[0x037FE12C, [PAYLOAD + alignment, CONTEXT + 0x19C, 80]]] if enabled else [[0x037FE070, [CONTEXT + 0x19C, 0, 80]]]
    calls.append([0x027E2458, ['scratch512', setting & 0xFFFF]])
    if status:
        calls += [[0x038073F0, []], [0x038073A4, [FIRST_MESSAGE]]]
    calls += [[0x038073F0, []], [0x038073A4, [FINAL_MESSAGE]]]
    return bytes(before), bytes(shared), bytes(expected), caller_writes, calls, status, result, stack_response


def execute(code, spec, specs, data, seed, thumb):
    before, shared, expected, expected_writes, expected_calls, status, result, stack_response = data
    rng = random.Random(0x202610293401 + seed)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for base, size in [(0x027E0000, 0x30000), (0x037F8000, 0x20000), (0x03000000, 0x20000)]:
        uc.mem_map(base, size)
    for target in NATIVE_HELPERS:
        callee = specs[target]
        binary = (ROOT / callee['binary']).read_bytes()
        uc.mem_write(target, binary[target - callee['base']:target - callee['base'] + callee['bytes']])
    uc.mem_write(ADDRESS, code)
    uc.mem_write(ARENA, before)
    uc.mem_write(GLOBAL, shared)
    uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    initial = [rng.getrandbits(32) for unused in matcher.common.REGISTERS]
    initial[0], initial[-2:] = REQUEST, [0x0301FF00, STOP | int(thumb)]
    for register, value in zip(matcher.common.REGISTERS, initial):
        uc.reg_write(register, value)
    all_writes, caller_writes, calls, visited = [], [], [], set()
    current_address, allocations = 0, 0
    def record(uc, access, address, size, value, user):
        all_writes.append([address, size, value])
        if ADDRESS <= current_address < ADDRESS + SIZE and ARENA <= address < ARENA + 4096:
            caller_writes.append([address, size, value])
    def observe(uc, address, size, user):
        nonlocal current_address, allocations
        current_address = address
        if ADDRESS <= address < ADDRESS + SIZE:
            visited.add(address)
            return
        for target in NATIVE_HELPERS:
            if target <= address < target + specs[target]['bytes']:
                if address == target:
                    calls.append([target, [uc.reg_read(register) for register in matcher.common.REGISTERS[:3]]])
                return
        if address not in [0x027E2458, 0x038073F0, 0x038073A4]:
            raise ValueError('Mode caller escaped its measured helpers/provider contracts')
        width = 2 if address == 0x027E2458 else 0 if address == 0x038073F0 else 1
        arguments = [uc.reg_read(register) for register in matcher.common.REGISTERS[:width]]
        response = None
        if address == 0x027E2458:
            pointer = arguments[0]
            if not 0x0301F000 <= pointer <= initial[-2] - 8 - 512:
                raise ValueError('Measured 512-byte provider scratch escaped its allocated frame')
            scratch = bytearray(rng.randbytes(512))
            struct.pack_into('<H', scratch, 4, status)
            uc.mem_write(pointer, bytes(scratch))
            arguments[0] = 'scratch512'
            response = pointer if stack_response else RESPONSE
        elif address == 0x038073F0:
            response = FIRST_MESSAGE if status and allocations == 0 else FINAL_MESSAGE
            allocations += 1
        else:
            response = result
        calls.append([address, arguments])
        returned = uc.reg_read(matcher.common.REGISTERS[-1])
        for register in [*matcher.common.REGISTERS[:4], matcher.common.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.common.REGISTERS[0], response)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | ((returned & 1) << 5))
        uc.reg_write(UC_ARM_REG_PC, returned & ~1)
    uc.hook_add(UC_HOOK_CODE, observe)
    uc.hook_add(UC_HOOK_MEM_WRITE, record)
    uc.emu_start(ADDRESS, STOP, count=6000)
    registers = [uc.reg_read(register) for register in matcher.common.REGISTERS]
    if uc.reg_read(UC_ARM_REG_PC) != STOP or registers[0] != result or registers[4:12] != initial[4:12] or registers[-2] != initial[-2]:
        raise ValueError('Mode caller failed actual return/result/preservation model')
    if uc.reg_read(UC_ARM_REG_CPSR) & 0x3F != 0x10 | (0x20 if thumb else 0):
        raise ValueError('Mode caller returned in a different CPU/instruction mode')
    if bytes(uc.mem_read(ARENA, 4096)) != expected or bytes(uc.mem_read(GLOBAL, 4096)) != shared or caller_writes != expected_writes or calls != expected_calls:
        raise ValueError('Independent complete-context/copy/clear/message/call model differs')
    return {'registers': registers, 'cpsr': uc.reg_read(UC_ARM_REG_CPSR), 'calls': calls, 'callerWrites': caller_writes, 'nativeAndStackWrites': all_writes, 'visited': sorted(visited), 'arenaSha256': digest(bytes(uc.mem_read(ARENA, 4096))), 'stackSha256': digest(bytes(uc.mem_read(0x0301F000, 4096)))}


def main():
    if sha256(ROOT / SOURCE) != SOURCE_HASH or sha256(COMPILER) != COMPILER_HASH or sha256(LINKER) != LINKER_HASH:
        raise ValueError('Frozen mode-caller source/compiler/linker differs')
    matcher.WORK = WORK / 'compile'
    specs = {spec['address']: spec for spec in matcher.candidates(10000)}
    spec = specs[ADDRESS]
    if spec['bytes'] != SIZE or spec['module'] != 'arm7-main':
        raise ValueError('Canonical mode-caller boundary differs')
    for output in (matcher.WORK / 'compile' / (ROOT / SOURCE).stem).glob('*.o'):
        output.unlink()
    entry, code = matcher.compare(ROOT / SOURCE, spec, COMPILER, COMPILER_HASH, 2, 'off')
    if code is None:
        raise ValueError('Complete ordinary C mode caller stopped matching')
    offset = ADDRESS - spec['base']
    native = (ROOT / spec['binary']).read_bytes()[offset:offset + SIZE]
    entry['isolatedRealMwCallerLink'] = real_link(entry, native, specs)
    vectors = itertools.product([0, 1, 2, 3, 4, 0x7FFF, 0xFFFF, 0x10001, 0xFFFF0003], [0, 1, 0x8000, 0xFFFF], [0, 1, 2, 3], [0, 1, 0xFFFFFFFF], [False, True])
    hashes, covered = [], set()
    for index, vector in enumerate(vectors):
        data = fixture(vector, index)
        for thumb in [False, True]:
            first = execute(native, spec, specs, data, index, thumb)
            second = execute(code, spec, specs, data, index, thumb)
            if first != second:
                raise ValueError('Fresh native/source mode-caller machines differ')
            hashes.append(digest(json.dumps(first, sort_keys=True).encode()))
            covered.update(first['visited'])
    if covered != {instruction.address for instruction in spec['instructions']}:
        raise ValueError('Mode fixtures did not cover every native caller instruction')
    entry['ordinaryCBytes'], entry['justifiedAssemblyBytes'] = SIZE, 0
    entry['oracle'] = {
        'cases': len(hashes), 'nativeAndRecompiledCalls': len(hashes) * 2, 'verifiedReturn': True,
        'returnModes': ['arm', 'thumb'], 'instructionLimit': 6000, 'stateSha256': hashes,
        'nativeInstructionCoverage': len(covered), 'nativeInstructions': len(spec['instructions']),
        'nativeCalleesExecuted': [hex(target) for target in NATIVE_HELPERS], 'nativeCalleeBodySourceCredit': 0,
        'independentModel': 'Truncated mode/setting fields, copy/zero80-byte payload, optional status message and final header, complete RAM/shared page, ordered caller stores/call words, 512-byte scratch bounds, R0/R4-R11/SP/modes',
        'limitations': ['Native copy/clear bodies execute as scaffolding with zero new source credit.', 'Command, allocation and send implementations use explicit return/ABI-clobber contracts; no hardware or transmission is executed.', 'Context, request, payload and message pointers are valid; arbitrary malformed pointers and provider side effects are unsupported.']
    }
    report = {
        'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
        'processor': 'arm7', 'runtimeMappingCanonical': True, 'matches': [entry],
        'nativeSymbols': {relocation['symbol']: relocation['target'] for relocation in entry['relocations']},
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False
    }
    write_json(ROOT / 'evidence/matches/arm7-20261029mode34.json', report)
    print({'functions': 1, 'bytes': SIZE, 'nativeAndRecompiledCalls': len(hashes) * 2})


if __name__ == '__main__':
    main()
