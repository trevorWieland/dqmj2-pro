import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

EKT = 0x02500000
EKT_STATE = 0x020f69ec
OBTAINED = 0x021c0a04
SEEN = 0x021c0ac4
SECONDARY = 0x021c0ee0
EVENT = 0x021c0e20
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    specifications = [('main-runtime08.json', {0x020449d4, 0x02045088}), ('save-accessors.json', {0x02063b40, 0x02063b60, 0x02063bbc, 0x02063bdc, 0x02063c00, 0x02063c94})]
    result = {}
    for report, addresses in specifications:
        document = json.loads((root / 'evidence/matches' / report).read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Dependency ROM namespace differs')
        for row in document['matches']:
            address = int(row['address'], 16)
            if address not in addresses:
                continue
            source, obj = root / row['source'], root / row['object']
            if sha(source.read_bytes()) != row['sourceSha256'] or sha(obj.read_bytes()) != row['objectSha256']:
                raise AssertionError('Frozen dependency identity differs')
            with obj.open('rb') as stream:
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
                raise AssertionError('Frozen dependency bytes differ')
            result[address] = (row, bytes(code))
    if len(result) != 8:
        raise AssertionError('Required accepted dependencies missing')
    return result

def canonical(table, identity, variant):
    alias = struct.unpack_from('<H', table, identity * 100 + 8)[0]
    return (alias, variant & 0xffff) if alias else (identity, variant)

def bit(memory, base, identity):
    return (u32(memory, base + (identity >> 5) * 4) >> (identity & 31)) & 1

def set_bit(memory, base, identity):
    at = base + (identity >> 5) * 4
    put(memory, at, u32(memory, at) | (1 << (identity & 31)))

def library_get(memory, table, base, identity, variant):
    identity, variant = canonical(table, identity, variant)
    return bit(memory, base + variant * 64, identity)

def expected(memory, table, name, identity, value, third):
    if name == 'saved_native_id_alias':
        alias = struct.unpack_from('<H', table, identity * 100 + 8)[0]
        return alias | ((value & 0xffff) << 16) if alias else 0
    if name == 'saved_native_id_predicate':
        return int(identity == 353 or identity in (139, 176, 188, 350) and third != 0)
    if name == 'saved_native_category':
        return ((struct.unpack_from('<H', table, identity * 100 + 4)[0] >> 8) & 15) // 3
    if name == 'native_main_020449d4':
        return EKT + identity * 100
    if name == 'native_main_02045088':
        flags = struct.unpack_from('<H', table, identity * 100 + 6)[0] >> 13
        shift = value & 255
        return (flags >> shift) & 1 if shift < 32 else 0
    if name.startswith('saved_library_'):
        base = OBTAINED if 'obtained' in name else SEEN
        if name.endswith('_get'):
            return library_get(memory, table, base, identity, value)
        if base == SEEN and identity in (353, 452, 455):
            return 0
        if base == SEEN and identity == 500:
            identity, value = 431, 2
        else:
            identity, value = canonical(table, identity, value)
        previous = library_get(memory, table, base, identity, value)
        set_bit(memory, base + value * 64, identity)
        category = ((struct.unpack_from('<H', table, identity * 100 + 4)[0] >> 8) & 15) // 3
        if base == SEEN and category == 1:
            was_set = bit(memory, SECONDARY, 17)
            set_bit(memory, SECONDARY, 17)
            if not was_set:
                set_bit(memory, SECONDARY, 81)
                set_bit(memory, EVENT, 76)
        return previous
    if 'nibbles' in name:
        at = 0x021c0bc4 + (identity >> 3) * 4
        shift = (identity & 7) * 4
        previous = (u32(memory, at) >> shift) & 15
        if name.endswith('_set'):
            put(memory, at, (u32(memory, at) & ~(15 << shift)) | ((value << shift) & 0xffffffff))
        return previous
    if 'raw_bits' in name:
        base = 0x021c0ba4 if '0ba4' in name else 0x021c0b84
        previous = bit(memory, base, identity)
        if name.endswith('_set'):
            set_bit(memory, base, identity)
        return previous
    raise AssertionError(('Unmodeled library function', name))

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    tests = dict(matches)
    for address in (0x020449d4, 0x02045088):
        row, code = reused[address]
        tests[row['name']] = (row, code)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for record, code in [*matches.values(), *reused.values()]:
                machine.mem_write(int(record['address'], 16), code)
        machines.append(machine)
    blob = NintendoDSRom((root / 'inputs/game.nds').read_bytes()).getFileByName('EnmyKindTbl.bin')
    if blob[:8] != b'EKT\0\0\x02\0\0' or len(blob) != 51208:
        raise AssertionError('Measured EKT table identity differs')
    actual_table = blob[8:]
    synthetic = bytearray(actual_table)
    rng = random.Random(20261027)
    for identity in range(512):
        struct.pack_into('<HHH', synthetic, identity * 100 + 4, rng.getrandbits(16), rng.getrandbits(16), 0)
    for source, target in [(16, 17), (17, 18), (25, 25), (30, 31), (31, 30), (431, 432)]:
        struct.pack_into('<H', synthetic, source * 100 + 8, target)
    struct.pack_into('<H', synthetic, 431 * 100 + 4, 0x300)
    cases = 0
    calls = 0
    for fixture, table in [('measured', actual_table), ('synthetic-aliases', bytes(synthetic))]:
        original = {0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021c0800: bytearray(rng.randbytes(0x1000)), EKT: bytearray(table + bytes(0x10000 - len(table)))}
        put(original, EKT_STATE + 4, EKT)
        begin = 0x021c0800 - 0x021bd51c + 0x90
        write(original, 0x021c0800, save[begin:0x3a68])
        if fixture != 'measured':
            write(original, 0x021c0800, rng.randbytes(0x1000))
        vectors = []
        identities = range(512) if fixture == 'measured' else [0, 16, 17, 18, 25, 30, 31, 139, 176, 188, 350, 353, 431, 452, 455, 500, 511]
        for name in tests:
            if name == 'saved_native_id_predicate':
                vectors.extend((name, identity, 0x12345678, enabled) for identity in [*range(-1, 513), -0x80000000, 0x7fffffff] for enabled in (0, 1, -1))
            elif 'raw_' in name:
                vectors.extend((name, identity, value, 0) for identity in (-33, -32, -8, -1, 0, 7, 8, 31, 32, 63, 127, 255, 511) for value in (0, 1, 15, 16, 255, 0xffffffff))
            elif name == 'native_main_02045088':
                vectors.extend((name, identity, bit_index, 0) for identity in identities for bit_index in (0, 1, 2, 3, 31, 32, 255, 256))
            else:
                variants = (0, 1, 2, 0x10001, -1) if name == 'saved_native_id_alias' else (0, 1, 2) if name.startswith('saved_library_') else (0,)
                vectors.extend((name, identity, value, 0) for identity in identities for value in variants)
        for name, identity, value, third in vectors:
            memory = {address: bytearray(data) for address, data in original.items()}
            result = expected(memory, table, name, identity, value, third)
            record, code = tests[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                for register, argument in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), (identity, value, third)):
                    machine.reg_write(register, argument & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(record['address'], 16), STOP, count=100000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Library execution bounds', fixture, name, identity, value))
                if machine.reg_read(UC_ARM_REG_R0) != (result & 0xffffffff):
                    raise AssertionError(('Library return differs', fixture, name, identity, value, machine.reg_read(UC_ARM_REG_R0), result))
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        differences = [(hex(address + index), actual, wanted) for index, (actual, wanted) in enumerate(zip(machine.mem_read(address, len(data)), data)) if actual != wanted]
                        raise AssertionError(('Library/table/secondary/guard RAM differs', fixture, name, identity, value, differences[:8]))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(tests), 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRamAndReturn': True, 'platformStubs': {}, 'ektAssetSha256': sha(blob), 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Obtained/seen getters canonicalize once; setters canonicalize their write identity and then invoke a getter that canonicalizes again.', 'Synthetic alias chains and cycles verify the distinction between returned old flag and written flag without claiming such chains occur in the measured EKT.', 'Seen setter excludes IDs353,452,455, remaps500 to431 variant2, and conditionally updates secondary bit17, history bit81 and event bit76 through existing recovered code.', 'The native ID predicate accepts353 unconditionally and139/176/188/350 only when its third argument is nonzero.', 'Raw nibble setter does not mask its input value before shifting, so high bits can affect adjacent nibbles; raw banks retain address-based names.'], 'limitations': ['All EKT/library/secondary callees execute; no gameplay routine or platform provider is substituted.', 'Stored library flags do not establish individual ownership, valid completion denominators or live availability.', 'Bounds of raw bit/nibble indices remain unknown; negative/boundary indices are isolated ARM behavior probes.', 'Native category/variant fields remain technical projections, without community names or new dated-partition semantics.']}
