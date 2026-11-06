import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

SECTION = 0x021bb278
FLAGS = 0x021bd504
RECORD76 = 0x021bb5b8
RECORD12 = 0x021bc8b8
INPUT = 0x02500100
SECOND = 0x02501000
STOP = 0x027ff800
DATE = bytes(range(0x20, 0x30))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02063ed4, 0x02063eb0, 0x02063ebc, 0x02063eec, 0x02068594, 0x02068520, 0x02067748, 0x02067a40, 0x02008e0c, 0x02008ca4, 0x02008d78, 0x020685c8, 0x020685f0, 0x0206877c}
    result = {}
    for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']:
        document = json.loads((root / batch['report']).read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Accepted section3 dependency namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if address not in wanted or row.get('module') not in ('main', 'arm9'):
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Accepted section3 dependency hash differs')
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
                raise AssertionError('Accepted section3 dependency native span differs')
            result[address] = (row, bytes(code))
    if not {0x02068594, 0x02068520, 0x020685c8, 0x020685f0, 0x0206877c}.issubset(result):
        raise AssertionError('Required accepted section3 callees absent')
    return result

def expected(memory, name, first, second):
    if name in ('saved_section3_flag_write', 'saved_section3_flag_get'):
        shift = first & 255
        mask = 1 << shift if shift < 32 else 0
        flags = u32(memory, FLAGS)
        if name.endswith('_get'):
            return int(bool(flags & mask))
        put(memory, FLAGS, flags | mask if second == 1 else flags & ~mask)
    elif name == 'saved_section3_first20_differ':
        return int(read(memory, first, 20) != read(memory, second, 20))
    elif name == 'saved_section3_record76_merge':
        if not 0 <= first < 64:
            return 0
        destination = RECORD76 + first * 76
        previous = read(memory, destination, 20)
        if read(memory, second, 1)[0]:
            write(memory, destination, bytes(20))
            write(memory, destination, read(memory, second, 20))
        if read(memory, second + 20, 1)[0]:
            write(memory, destination + 20, bytes(24))
            write(memory, destination + 20, read(memory, second + 20, 20))
        value = read(memory, second + 44, 2)
        if value != bytes(2):
            write(memory, destination + 44, value)
        for offset in (48, 52, 56):
            value = read(memory, second + offset, 4)
            if value != bytes(4):
                write(memory, destination + offset, value)
        write(memory, destination + 60, DATE)
        return int(previous != read(memory, second, 20))
    elif name == 'saved_section3_record12_write':
        if not 0 <= first < 64:
            return 0
        write(memory, RECORD12 + first * 12, read(memory, second, 12))
        return 1
    elif name == 'native_main_02068520':
        old = u32(memory, FLAGS)
        write(memory, 0x021bcc0c, bytes(256))
        write(memory, 0x021c373c, bytes(12))
        write(memory, 0x021c37b8, bytes(56))
        put(memory, FLAGS, 8 if old else 0)
    elif name == 'native_main_02068594':
        return int(0 <= first < 64)
    elif name in ('native_main_020685c8', 'native_main_020685f0', 'native_main_0206877c'):
        if not 0 <= first < 64:
            return 0
        base, stride = {'native_main_020685c8': (0x021bb2b8, 12), 'native_main_020685f0': (RECORD76, 76), 'native_main_0206877c': (RECORD12, 12)}[name]
        return base + first * stride
    else:
        raise AssertionError(('Unmodeled section3 function', name))
    return None

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    tests = dict(matches)
    for address in (0x02068520, 0x02068594, 0x020685c8, 0x020685f0, 0x0206877c):
        row, code = reused[address]
        tests[row['name']] = (row, code)
    context = {}
    machines = []

    def date(machine, address, size, user):
        context['dates'].append(machine.reg_read(UC_ARM_REG_R0))
        machine.mem_write(machine.reg_read(UC_ARM_REG_R0), DATE)
        for register, value in [(UC_ARM_REG_R0, 0), (UC_ARM_REG_R1, 0x12345678), (UC_ARM_REG_R2, 0x23456789), (UC_ARM_REG_R3, 0x3456789a)]:
            machine.reg_write(register, value)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machine.hook_add(UC_HOOK_CODE, date, begin=0x0200f3e0, end=0x0200f3e0)
        machines.append(machine)
    rng = random.Random(20261027)
    vectors = []
    indices = [-0x80000000, -1, 0, 1, 31, 32, 63, 64, 255, 256, 0x7fffffff]
    for name in tests:
        if name.startswith('saved_section3_flag_'):
            vectors.extend((name, index, value, 0) for index in [-1, *range(33), 63, 255, 256] for value in (0, 1, 2, -1, 0x7fffffff))
        elif name == 'saved_section3_first20_differ':
            vectors.extend((name, INPUT, SECOND, difference) for difference in range(7))
        elif name in ('saved_section3_record76_merge', 'saved_section3_record12_write'):
            vectors.extend((name, index, alias, mask) for index in indices for alias in (INPUT, 0) for mask in range(64))
        else:
            vectors.extend((name, index, 0, mask) for index in indices for mask in (0, 1, 0x80000000, 0xffffffff))
    calls = 0
    cases = 0
    for bank in (0, 0x7100):
        for name, first, second, mask in vectors:
            original = {0x021b9000: bytearray(rng.randbytes(0xb000)), 0x02500000: bytearray(rng.randbytes(0x3000))}
            write(original, SECTION, save[bank + 0x3a9c:bank + 0x5d40])
            put(original, FLAGS, mask if name == 'native_main_02068520' else rng.getrandbits(32))
            if name == 'saved_section3_first20_differ':
                data = rng.randbytes(20)
                write(original, first, data)
                write(original, second, data)
                if mask < 5:
                    put(original, second + mask * 4, u32(original, second + mask * 4) ^ 1)
            elif name in ('saved_section3_record76_merge', 'saved_section3_record12_write'):
                data = bytearray(rng.randbytes(76))
                data[0] = 1 if mask & 1 else 0
                data[20] = 1 if mask & 2 else 0
                struct.pack_into('<H', data, 44, 0xabcd if mask & 4 else 0)
                for bit_index, offset in enumerate((48, 52, 56), 3):
                    struct.pack_into('<I', data, offset, rng.getrandbits(32) or 1 if mask & (1 << bit_index) else 0)
                if second == 0 and 0 <= first < 64:
                    second = (RECORD76 + first * 76) if name == 'saved_section3_record76_merge' else RECORD12 + first * 12
                if second:
                    write(original, second, bytes(data))
            memory = {address: bytearray(data) for address, data in original.items()}
            result = expected(memory, name, first, second)
            expected_dates = [RECORD76 + first * 76 + 60] if name == 'saved_section3_record76_merge' and 0 <= first < 64 else []
            row, code = tests[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                context['dates'] = []
                machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
                machine.reg_write(UC_ARM_REG_R1, second & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Section3 bounds', name, bank, first, second, mask))
                if (result is not None and machine.reg_read(UC_ARM_REG_R0) != result) or context['dates'] != expected_dates:
                    raise AssertionError(('Section3 result/date differs', name, bank, first, second, mask))
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        actual = machine.mem_read(address, len(data))
                        differences = [(hex(address + index), actual[index], value) for index, value in enumerate(data) if actual[index] != value]
                        raise AssertionError(('Section3/neighbor/cache/input/guard RAM differs', name, bank, first, second, mask, differences[:8]))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(tests), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedWholeSectionAndGuardRam': True, 'platformStubs': {'0x0200f3e0': 'date16 controlled provider'}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Native indexed subarrays accept signed indices0..63:12-byte entries at section+0x40,76-byte entries at+0x340 and12-byte entries at+0x1640.', 'The76-byte merge conditionally replaces first20/second20 bytes, clears24 bytes for the latter, preserves zero-valued halfword/word inputs, and writes a16-byte date.', 'Merge return compares previous first20 bytes against current input bytes, even when the first input byte prevented replacement; it is not a general changed-state predicate.', 'Aliased input/destination tests preserve sequential native clear/copy effects, including input bytes changed by the operation.', 'Flag write sets a bit only for value exactly1; all other values clear it.', 'Existing recovered reset clears a256-byte saved region and two runtime caches, normalizing any nonzero prior flag word to bit3.'], 'limitations': ['Only date acquisition is substituted; native memory copies, index predicates and pointer callers execute.', 'All array fields, flags, runtime caches and record gameplay purposes remain technically named; no semantic partition promotion occurs.', 'Out-of-range flag shifts are isolated ARM probes; the C shift is not portable outside0..31.', 'Invalid record indices return before accessing even null input, as bounded native machine behavior.']}
