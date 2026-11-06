import hashlib
import json
import random
import re
import struct
import sys
from project import ROOT, configuration, now, sha256, write_json

sys.path.insert(0, str(ROOT / 'deps/native'))
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC
import match_lowlevel as matcher
from link_runtime_unit import measured_module, validate

SOURCE = 'src/itcm/20261029_initialization/native_itcm_01ffa988.c'
HEADER = 'src/itcm/20261029_initialization/native_itcm_01ffa988.h'
SOURCE_HASH = '9b459ad3621c97c37fd692c33870ea7a2693360fccff93fd025da36813f5abb5'
HEADER_HASH = 'c6d5d794fabaed00dbe173733291f407df1bc1c4b5a97ed8aabface5869208d0'
COMPILER_HASH = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
ADDRESS, SIZE, STOP = 0x01FFA988, 520, 0x0301E000
PAGES = [0x01FFF000, 0x020DC000, 0x021CE000, 0x03002000]
STATE, POINT_SOURCE, TAIL, ACTOR, CONTEXT = 0x01FFF9A8, 0x020DC3B0, 0x021CEBE0, 0x03002200, 0x03002500
WORK = ROOT / 'work/lowlevel-recovery/20261029-itcm/initialization-proof'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def put(pages, address, value, size, writes=None):
    base = address & ~0xFFF
    struct.pack_into({1: '<B', 2: '<H', 4: '<I'}[size], pages[PAGES.index(base)], address - base, value)
    if writes is not None:
        writes.append([address, size, value])


def signed_byte(value):
    value &= 0xFF
    return value - 256 if value & 0x80 else value


def expected_fixture(seed, active):
    rng = random.Random(0x2026102900988 + seed)
    before = [bytearray(rng.randbytes(4096)) for unused in PAGES]
    x, y = [(0, 0), (0xFFFF, 0xFFFF), (0, 0xFFFF), (0x8000, 0x7FFF)][seed % 4]
    if seed >= 4:
        x, y = rng.getrandbits(16), rng.getrandbits(16)
    state_byte = [0, 1, 0x7F, 0x80, 0xFE, 0xFF][seed % 6]
    first, second = [(0, 1), (0x7F, 0x80), (0xFF, 0x100), (0x80000080, 0xFFFFFF7F), (0x12345600, 0x123456FF), (0xFFFFFFFF, 0)][seed % 6]
    handle, actor_value, mapping_result = rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32)
    put(before, POINT_SOURCE + 8, x, 2)
    put(before, POINT_SOURCE + 0xA, y, 2)
    put(before, STATE + 0x1C, state_byte, 1)
    put(before, ACTOR, active, 4)
    put(before, ACTOR + 4, actor_value, 4)
    expected, writes = [bytearray(page) for page in before], []
    for offset, value, size in [(2, 1, 2), (0, 0, 1), (6, 0, 2), (4, 0xFFFF, 2), (8, 0, 1)]:
        put(expected, STATE + offset, value, size, writes)
    for address, value, size in [(0x01FFF934, 0, 1), (0x01FFF950, 0, 4), (TAIL + 4, 0, 1), (TAIL + 0x44, 0, 4), (TAIL + 0x20, 0, 4)]:
        put(expected, address, value, size, writes)
    point = struct.pack('<HH', x, y)
    calls = [
        [0x01FFA968, [0x10]],
        [0x02048FCC, [0x01FFF9B4]],
        [0x01FFB340, []],
        [0x02048FCC, [CONTEXT]],
        *[[0x02223C04, [index, 0x20]] for index in range(4)],
        [0x02223C04, [1, 0x20]],
        [0x02048F1C, [3, 1]],
        [0x02048F2C, [2, 1]],
        [0x02048F3C, [0, 1]],
        [0x01FFB398, []],
        [0x01FFB34C, []],
        [0x0204B4F4, [handle, 'point', 0xE0, 2, 2, 0x24]],
        [0x020897EC, [0]],
        [0x02049AE4, []]
    ]
    if active:
        calls.append([0x020853C8, [actor_value]])
    calls.extend([
        [0x02216260, [0x1F, signed_byte(state_byte), 3, 0x16, 1, 0xA, 2, 1, 1]],
        [0x02216260, [0, signed_byte(state_byte), 0x7F, 1, 1, 0x18, 2, 1, 1]],
        [0x02048F6C, [1]], [0x02048F6C, [1]],
        [0x02223C14, [signed_byte(second)]],
        [0x02223C04, [signed_byte(first), mapping_result]],
        [0x0204B85C, [0x01FFF960, 'point', 8, 1, 0, 0x33, 0]],
        [0x0205FA4C, [0x01FFF960, 0]]
    ])
    calls = [[target, [value & 0xFFFFFFFF if isinstance(value, int) else value for value in arguments]] for target, arguments in calls]
    returns = {0x01FFB340: [CONTEXT], 0x01FFB34C: [handle], 0x02049AE4: [ACTOR], 0x02048F6C: [first, second], 0x02223C14: [mapping_result]}
    return before, expected, writes, calls, returns, point


def bindings_for(entry):
    bindings = {}
    for relocation in entry['relocations']:
        name, target = relocation['symbol'], int(relocation['target'], 0)
        module_name = 'ov000' if '_ov000_' in name else 'itcm' if target < 0x02000000 else 'main'
        module, binary, symbols = measured_module(module_name)
        kind = 'function' if name.startswith('native_fn_') else 'data'
        if kind == 'function':
            match = re.search(r'^\S+ kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:0x' + f'{target:08x}' + r'$', symbols, re.M)
            if match is None:
                raise ValueError('Callee lacks qualified module/address/mode boundary: ' + name)
            mode = match[1]
        else:
            mode = 'data'
            if not re.search(r'^\S+ kind:(?:data\([^\n]*\)|bss) addr:0x' + f'{target:08x}' + r'$', symbols, re.M):
                raise ValueError('Global lacks a configured data/BSS symbol: ' + name)
        bindings[name] = {
            'processor': 'arm9', 'module': module_name, 'kind': kind,
            'mode': mode, 'address': hex(target), 'inputModuleSha256': module['sha256']
        }
    return bindings


def execute(code, fixture, seed, thumb, bindings):
    before, expected, expected_writes, expected_calls, returns, point = fixture
    rng = random.Random(0x2026102901988 + seed)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for base, size in [(0x01FF8000, 0x8000), (0x02000000, 0x400000), (0x03000000, 0x20000)]:
        uc.mem_map(base, size)
    uc.mem_write(ADDRESS, code)
    for address, page in zip(PAGES, before):
        uc.mem_write(address, bytes(page))
    uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    initial = [rng.getrandbits(32) for unused in matcher.REGISTERS]
    initial[-2:] = [0x0301FF00, STOP | int(thumb)]
    for register, value in zip(matcher.REGISTERS, initial):
        uc.reg_write(register, value)
    function_modes = {int(binding['address'], 0): binding['mode'] for binding in bindings.values() if binding['kind'] == 'function'}
    observed_calls, writes, all_writes, reads, visited, occurrences = [], [], [], [], set(), {}
    def record(uc, access, address, size, value, user):
        all_writes.append([address, size, value])
        if address & ~0xFFF in PAGES:
            writes.append([address, size, value])
    def read(uc, access, address, size, value, user):
        if address in [POINT_SOURCE + 8, POINT_SOURCE + 0xA]:
            reads.append([address, size])
    def observe(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + SIZE:
            visited.add(address)
            return
        if address not in function_modes or len(observed_calls) >= len(expected_calls):
            raise ValueError('Initializer escaped its complete caller/callee contract')
        if bool(uc.reg_read(UC_ARM_REG_CPSR) & 0x20) != (function_modes[address] == 'thumb'):
            raise ValueError('Callee entered a different configured instruction mode')
        target, arguments = expected_calls[len(observed_calls)]
        if address != target:
            raise ValueError('Initializer called a different native module/address')
        values = [uc.reg_read(register) for register in matcher.REGISTERS[:min(4, len(arguments))]]
        stack = uc.reg_read(matcher.REGISTERS[-2])
        for offset in range(max(0, len(arguments) - 4)):
            values.append(struct.unpack('<I', bytes(uc.mem_read(stack + offset * 4, 4)))[0])
        for index, wanted in enumerate(arguments):
            if wanted == 'point':
                if bytes(uc.mem_read(values[index], 4)) != point:
                    raise ValueError('Four-byte point argument differs from original two coordinates')
                values[index] = 'point'
        if values != arguments:
            raise ValueError('Measured register/stack call words differ: ' + hex(address))
        observed_calls.append([address, values])
        index = occurrences.get(address, 0)
        occurrences[address] = index + 1
        result = returns[address][index] if address in returns else rng.getrandbits(32)
        returned = uc.reg_read(matcher.REGISTERS[-1])
        for register in [*matcher.REGISTERS[:4], matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | ((returned & 1) << 5))
        uc.reg_write(UC_ARM_REG_PC, returned & ~1)
    uc.hook_add(UC_HOOK_MEM_WRITE, record)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_CODE, observe)
    uc.emu_start(ADDRESS, STOP, count=10000)
    actual = [uc.reg_read(register) for register in matcher.REGISTERS]
    if uc.reg_read(UC_ARM_REG_PC) != STOP or actual[4:12] != initial[4:12] or actual[-2] != initial[-2]:
        raise ValueError('Initializer failed actual return or preserved-register model')
    if uc.reg_read(UC_ARM_REG_CPSR) & 0x3F != 0x10 | (0x20 if thumb else 0):
        raise ValueError('Initializer returned in a different CPU/instruction mode')
    pages = [bytes(uc.mem_read(address, 4096)) for address in PAGES]
    if pages != [bytes(page) for page in expected] or writes != expected_writes or observed_calls != expected_calls:
        raise ValueError('Independent complete global/object/ordered-call model differs')
    if reads != [[POINT_SOURCE + 0xA, 2], [POINT_SOURCE + 8, 2]]:
        raise ValueError('Measured coordinate halfword-read order differs')
    return {
        'registers': actual, 'cpsr': uc.reg_read(UC_ARM_REG_CPSR), 'calls': observed_calls,
        'writes': writes, 'stackAndCallerWrites': all_writes, 'pointReads': reads,
        'memorySha256': [digest(page) for page in pages], 'visited': sorted(visited)
    }


def main():
    if sha256(ROOT / SOURCE) != SOURCE_HASH or sha256(ROOT / HEADER) != HEADER_HASH or sha256(matcher.COMPILER) != COMPILER_HASH:
        raise ValueError('Frozen initializer source/header/compiler differs')
    matcher.WORK = WORK / 'compile'
    for output in (matcher.WORK / 'native_itcm_01ffa988').glob('*.o'):
        output.unlink()
    rows, found = matcher.compare(ROOT / SOURCE, 'itcm', 2, 'off', False)
    if len(found) != 1:
        raise ValueError('Complete initializer C body stopped matching')
    entry, code = next(iter(found.values()))
    bindings = bindings_for(entry)
    linked = validate(entry, bindings, WORK / 'real-link')
    native = (ROOT / 'extract/arm9/itcm.bin').read_bytes()[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + SIZE]
    hashes, covered = [], set()
    for seed in range(12):
        for active in [0, 1, 0x80000000]:
            fixture = expected_fixture(seed, active)
            for thumb in [False, True]:
                first = execute(native, fixture, seed, thumb, bindings)
                second = execute(code, fixture, seed, thumb, bindings)
                if first != second:
                    raise ValueError('Fresh native/source initializer machines differ')
                covered.update(first['visited'])
                hashes.append(digest(json.dumps(first, sort_keys=True).encode()))
    instruction_end = ADDRESS + min(relocation['offset'] for relocation in entry['relocations'] if relocation['type'] == 2)
    if covered != set(range(ADDRESS, instruction_end, 4)):
        raise ValueError('Initializer fixtures did not cover every native instruction')
    entry.update(ordinaryCBytes=SIZE, justifiedAssemblyBytes=0)
    entry['sourceInputs'] = {SOURCE: SOURCE_HASH, HEADER: HEADER_HASH}
    entry['sourceDependencies'] = [{'path': HEADER, 'sha256': HEADER_HASH}]
    entry['reconstructionChoices'] = ['Volatile source-record and local-point qualifiers express the measured two-load/two-store ordering; original declaration qualifiers are unproven.', 'External prototypes remain provisional; measured six-, nine- and seven-word call interfaces are independently checked.']
    entry['isolatedRealMwCallerLink'] = linked
    entry['oracle'] = {
        'cases': len(hashes), 'nativeAndRecompiledCalls': len(hashes) * 2, 'verifiedReturn': True,
        'returnModes': ['arm', 'thumb'], 'instructionLimit': 10000,
        'nativeInstructionCoverage': len(covered), 'nativeInstructions': (instruction_end - ADDRESS) // 4,
        'stateSha256': hashes, 'externalCalleesExecuted': 0,
        'independentModel': 'Complete ITCM/global/object pages, ordered typed stores and coordinate reads, every register/stack call word, four-byte point, preserved R4-R11/SP and return modes',
        'limitations': ['All external implementations use explicit deterministic return/ABI-clobber contracts; no game/hardware behavior is claimed for their bodies.', 'Volatile qualifiers and provisional C interfaces are reconstruction choices rather than recovered original declarations.', 'Actor memory is valid and aligned; arbitrary unmapped pointers and global changes from asynchronous hardware are unsupported.']
    }
    report = {
        'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
        'module': 'itcm', 'matches': [entry], 'nativeSymbols': {relocation['symbol']: relocation['target'] for relocation in entry['relocations']},
        'sourceDependencies': [{'path': HEADER, 'sha256': HEADER_HASH}],
        'qualifiedBindings': bindings, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False
    }
    write_json(ROOT / 'evidence/matches/itcm-20261029-initialization.json', report)
    print({'functions': 1, 'bytes': SIZE, 'oracleCases': len(hashes), 'nativeAndRecompiledCalls': len(hashes) * 2})


if __name__ == '__main__':
    main()
