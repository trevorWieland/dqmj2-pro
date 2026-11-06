import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32

ROOTS = 0x020da084
POINTERS = 0x02500000
BASE = 0x02520000
SUFFIX = 0x02530000
OUTPUT = 0x02540080
INPUT = 0x02541080
EKT = 0x02550000
STOP = 0x027ff800
BUILDER = 0x02044ff4

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x0205dcbc, 0x0205dcfc, 0x02044d84, 0x020449d4}
    result = {}
    paths = [root / batch['report'] for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']]
    paths.append(root / 'evidence/matches/mechanics-save-features.json')
    for path in paths:
        document = json.loads(path.read_text(encoding='utf-8'))
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if row.get('module') not in ('main', 'arm9') or address not in wanted:
                continue
            if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6' or sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Text dependency identity differs')
            with (root / row['object']).open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
                code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
            for relocation in row.get('relocations', []):
                at = relocation['offset']
                target = int(relocation['target'], 16) + relocation['addend']
                previous = struct.unpack_from('<I', code, at)[0]
                value = target if relocation['type'] == 2 else (previous & 0xff000000) | (((target - address - at) >> 2) & 0xffffff)
                struct.pack_into('<I', code, at, value & 0xffffffff)
            if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError('Text dependency native bytes differ')
            result[address] = (row, bytes(code))
    if set(result) != wanted:
        raise AssertionError('Text source dependency absent')
    return result

def continues(memory, pointer):
    return int(bool(pointer) and read(memory, pointer, 1) != b'\0' and read(memory, pointer, 2) != b'\xe3\x1b')

def copy(memory, destination, source):
    original = destination
    for count in range(128):
        value = read(memory, source, 1)
        write(memory, destination, value)
        source += 1
        destination += 1
        if not continues(memory, source):
            write(memory, destination, b'\xe3\x1b')
            return original
    raise AssertionError('Text copy fixture exceeded bound')

def append(memory, destination, source):
    original = destination
    for count in range(128):
        if not continues(memory, destination):
            copy(memory, destination, source)
            return original
        destination += 1
    raise AssertionError('Text append fixture exceeded bound')

def pointer(memory, group, table, index):
    return u32(memory, u32(memory, u32(memory, ROOTS + group * 4) + table * 4) + index * 4)

def expected(memory, name, first, second, third):
    if name == 'saved_native_text_pointer':
        return pointer(memory, first, second, third)
    if name == 'saved_native_text_continues':
        return continues(memory, first)
    if name == 'copy':
        return copy(memory, first, second)
    if name == 'append':
        return append(memory, first, second)
    if name == 'native-builder':
        if not third:
            write(memory, first, b'\xe3\x1b\xe3\x1b')
        copy(memory, first, pointer(memory, 2, 0, second))
        if third:
            group = struct.unpack('<H', read(memory, EKT + second * 100 + 4, 2))[0] & 15
            offset = (group - 1) // 3 if group else 0
            append(memory, first, pointer(memory, 2, 1, third + offset))
        return first
    raise AssertionError('Unexpected text operation')

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*reused.values(), *matches.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    ekt = bytes(NintendoDSRom((root / 'inputs/game.nds').read_bytes()).getFileByName('EnmyKindTbl.bin'))[8:]
    rng = random.Random(20261027)
    base = {0x020da000: bytearray(arm[0xda000:0xdb000]), 0x020f6900: bytearray(rng.randbytes(0x1000)), POINTERS: bytearray(rng.randbytes(0x6000)), BASE: bytearray(0x4000), SUFFIX: bytearray(0x2000), 0x02540000: bytearray(rng.randbytes(0x2000)), EKT: bytearray(ekt + bytes(0x10000 - len(ekt)))}
    put(base, 0x020f69f0, EKT)
    for group in range(4):
        put(base, ROOTS + group * 4, POINTERS + group * 8)
        for table in range(2):
            vector = POINTERS + 0x1000 + (group * 2 + table) * 0x800
            put(base, POINTERS + group * 8 + table * 4, vector)
            for index in range(512):
                put(base, vector + index * 4, BASE + index * 32 if table == 0 else SUFFIX + index * 16)
    for index in range(512):
        write(base, BASE + index * 32, bytes([0x80 + index % 64, 0x40 + index // 64, 0x60 + index % 16, 0xe3, 0x1b]))
        write(base, SUFFIX + index * 16, bytes([0x50 + index % 16, 0x70 + index // 64, 0xe3, 0x1b]))
    tests = {name: (int(row['address'], 16), name) for name, (row, code) in matches.items()}
    tests.update({'copy': (0x0205dcbc, 'copy'), 'append': (0x0205dcfc, 'append'), 'native-builder': (BUILDER, 'native-builder')})
    strings = [b'\0', b'\xe3\x1b\0', b'A\0', b'A\xe3\x1b\0', b'\xe3\x1c\0', b'AB\xe3\x1bC\0', bytes(range(1, 64)) + b'\0']
    vectors = []
    for name in tests:
        if name == 'saved_native_text_pointer':
            vectors.extend((name, group, table, index, None) for group in range(4) for table in range(2) for index in range(512))
        elif name == 'saved_native_text_continues':
            vectors.extend((name, INPUT, 0, 0, bytes([first, second, 0])) for first in range(256) for second in (0, 1, 27, 255))
            vectors.extend((name, INPUT, 0, 0, bytes([227, second, 0])) for second in range(256))
            vectors.append((name, 0, 0, 0, None))
        elif name == 'native-builder':
            vectors.extend((name, OUTPUT, species, variant, None) for species in range(512) for variant in (0, 1, 2))
            vectors.extend((name, OUTPUT, 0, variant, value) for value in strings for variant in (0, 1, 2))
        else:
            vectors.extend((name, OUTPUT, INPUT, 0, (source, destination)) for source in strings for destination in strings)
    cases = calls = 0
    for name, first, second, third, pattern in vectors:
        original = {address: bytearray(data) for address, data in base.items()}
        if name in ('copy', 'append'):
            source, destination = pattern
            write(original, INPUT, source + bytes(16))
            write(original, OUTPUT, destination + bytes(16))
        elif name == 'saved_native_text_continues':
            if pattern is not None:
                write(original, INPUT, pattern)
        elif name == 'native-builder' and pattern is not None:
            write(original, INPUT, pattern + bytes(16))
            put(original, POINTERS + 0x1000 + 4 * 0x800, INPUT)
        memory = {address: bytearray(data) for address, data in original.items()}
        result = expected(memory, name, first, second, third)
        address, operation = tests[name]
        for machine in machines:
            for at, data in original.items():
                machine.mem_write(at, bytes(data))
            machine.mem_write(0x027fefea, b'\0\0')
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), (first, second, third)):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(address, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError(('Native text bounds', name, first, second, third))
            if machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('Native text pointer/stop/copy/name return', name, first, second, third))
            for at, data in memory.items():
                if bytes(machine.mem_read(at, len(data))) != data:
                    raise AssertionError(('Native text buffers/pointers/EKT/guard RAM', name, first, second, third))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'reusedEntryPointsTested': ['0x0205dcbc', '0x0205dcfc'], 'retainedEntryPointTested': hex(BUILDER), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRawTextAndSyntheticPointerTables': True, 'platformStubs': {}, 'retainedNativeDependency': {'module': 'main', 'mode': 'ARM', 'address': hex(BUILDER), 'bytes': 148, 'sha256': sha(arm[0x44ff4:0x45088]), 'role': 'native name builder; draft has unresolved scheduling/allocations'}, 'nativeNameSeed': {'address': '0x020d92fc', 'bytes': 2, 'hex': arm[0xd92fc:0xd92fe].hex()}, 'seededBuilderStackPadding': {'address': '0x027fefea', 'bytes': 2, 'valueHex': '0000', 'reason': 'Native two-byte seed copy can read beyond its initialized local before the later base copy; bound the inherited stack bytes explicitly.'}, 'ektPayloadSha256': sha(ekt), 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Text lookup performs three pointer loads using group/table/index without a native bounds guard.', 'Continuation is false at null,00 or E31B; all other first-byte values and every E3 second-byte case are tested.', 'The existing copy always copies its first byte before testing the following source position, then writes E31B; append scans to the first stop position and invokes that copy.', 'The retained builder copies group2/table0/species and appends group2/table1/(variant+native offset) when variant is nonzero.', 'All512 species and three variants run against synthetic bounded pointer tables/raw strings; controls and short/empty forms have independent byte expectations.'], 'limitations': ['The148-byte name builder remains native ARM and is not accepted as recovered C; only its lookup and stop helpers receive new source credit.', 'Two stack padding bytes are explicitly zeroed in the retained builder fixtures; no guarantee about arbitrary preexisting stack contents is inferred.', 'Synthetic pointer tables and raw strings establish mechanics rather than actual decoded names, encoding, Unicode mappings or legal table bounds.', 'Unterminated, dangling and overlapping strings are outside this bounded proof; no new save meanings are promoted.']}
