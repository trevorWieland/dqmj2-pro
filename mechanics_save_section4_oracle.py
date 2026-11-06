import hashlib
import itertools
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

SECTION = 0x021b9ee8
CURRENT = 0x021d424c
SELECTION = 0x021d423c
HALFWORDS = 0x021d4328
MODE = 0x021c0efe
INPUT = 0x02500100
OUTPUT = 0x02501000
STRIDE = 0x268
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02063f6c, 0x020653d0, 0x02008e0c, 0x02008d78}
    result = {}
    registry = json.loads((root / 'recovery.json').read_text(encoding='utf-8'))
    for batch in registry['batches']:
        document = json.loads((root / batch['report']).read_text(encoding='utf-8'))
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if address not in wanted or row.get('module') not in ('main', 'arm9'):
                continue
            if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
                raise AssertionError('Dependency namespace differs')
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Accepted dependency identity differs')
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
                raise AssertionError('Accepted dependency native span differs')
            result[address] = (row, bytes(code))
    if 0x02063f6c not in result:
        raise AssertionError('Accepted section4 pointer source is required')
    return result

def record(index):
    return SECTION + 0x50 + index * STRIDE

def flag(memory, address, mask):
    write(memory, address, bytes([read(memory, address, 1)[0] | mask]))

def expected(memory, name, first, second):
    if name == 'saved_section4_current_set':
        write(memory, CURRENT, read(memory, first, STRIDE))
        write(memory, CURRENT + 0xaf, bytes([second & 255]))
    elif name == 'saved_section4_current_halfword_set':
        write(memory, HALFWORDS + first * 0x84, struct.pack('<H', second & 65535))
    elif name == 'saved_section4_append':
        count = read(memory, SECTION, 1)[0]
        if read(memory, CURRENT + 0xaf, 1)[0] >= 7 or count == 8:
            return 0
        write(memory, record(count), read(memory, CURRENT, STRIDE))
        mode = read(memory, MODE, 1)[0]
        if mode == 3:
            flag(memory, record(count) + 0x25b, 3)
        elif mode == 0:
            flag(memory, record(count) + 0x25b, 2)
        write(memory, SECTION, bytes([(count + 1) & 255]))
        return 1
    elif name == 'saved_section4_read':
        write(memory, second, read(memory, record(first), STRIDE))
        write(memory, SELECTION + 4, bytes([first & 255]))
    elif name == 'saved_section4_remove':
        write(memory, record(first), bytes(STRIDE))
        output = 0
        count = read(memory, SECTION, 1)[0]
        for index in range(count):
            if read(memory, record(index) + 0xaf, 1)[0]:
                write(memory, record(output), read(memory, record(index), STRIDE))
                output = (output + 1) & 255
        write(memory, SECTION, bytes([output]))
        for index in range(output, 8):
            write(memory, record(index), bytes(STRIDE))
    elif name == 'saved_section4_selected_flags_update':
        selected = read(memory, SELECTION + 4, 1)[0]
        mode = read(memory, MODE, 1)[0]
        if mode in (0, 3):
            flag(memory, record(selected) + 0x25b, 3 if mode == 3 else 2)
    else:
        raise AssertionError(('Unknown section4 function', name))
    return None

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rng = random.Random(20261027)
    vectors = []
    for mode, source in itertools.product([0, 1, 6, 7, 255, 256, 0xffffffff], [INPUT, CURRENT]):
        vectors.append(('saved_section4_current_set', source, mode, 0, 0, 0))
    for index, value in itertools.product([-1, 0, 1, 2, 3, 4, 5], [0, 65535, 65536, 0xffffffff]):
        vectors.append(('saved_section4_current_halfword_set', index, value, 0, 0, 0))
    for count, mode, current_mode, flags in itertools.product([0, 1, 7, 8, 9, 10], [0, 1, 2, 3, 255], [0, 1, 6, 7, 255], [0, 0x7f, 0x80, 0xff]):
        vectors.append(('saved_section4_append', 0, 0, count, mode, (current_mode, flags)))
    for index, destination in itertools.product([-1, 0, 1, 7, 8, 9, 10], [OUTPUT, CURRENT]):
        vectors.append(('saved_section4_read', index, destination, 0, 0, 0))
    for count, index, pattern in itertools.product([0, 1, 7, 8, 9, 10], [-1, 0, 1, 7, 8, 9], [0, 1, 2, 3]):
        vectors.append(('saved_section4_remove', index, 0, count, 0, pattern))
    for selected, mode, flags in itertools.product([0, 1, 7, 8, 9], [0, 1, 2, 3, 255], [0, 0x7f, 0x80, 0xff]):
        vectors.append(('saved_section4_selected_flags_update', 0, 0, selected, mode, flags))
    cases = 0
    calls = 0
    for bank in (0, 0x7100):
        for name, first, second, count, mode, detail in vectors:
            if name not in matches:
                continue
            memory = {0x021b9000: bytearray(rng.randbytes(0x9000)), 0x021d4000: bytearray(rng.randbytes(0x2000)), 0x02500000: bytearray(rng.randbytes(0x3000))}
            write(memory, SECTION, save[bank + 0x5d40:bank + 0x70d0])
            write(memory, MODE, bytes([mode]))
            if name in ('saved_section4_append', 'saved_section4_remove'):
                write(memory, SECTION, bytes([count]))
            if name == 'saved_section4_append':
                write(memory, CURRENT + 0xaf, bytes([detail[0]]))
                write(memory, CURRENT + 0x25b, bytes([detail[1]]))
            elif name == 'saved_section4_remove':
                for index in range(10):
                    value = 0 if detail == 0 else 1 if detail == 1 else index & 1 if detail == 2 else (index + count) & 7
                    write(memory, record(index) + 0xaf, bytes([value]))
            elif name == 'saved_section4_selected_flags_update':
                write(memory, SELECTION + 4, bytes([count]))
                write(memory, record(count) + 0x25b, bytes([detail]))
            original = {address: bytearray(data) for address, data in memory.items()}
            result = expected(memory, name, first, second)
            row, code = matches[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
                machine.reg_write(UC_ARM_REG_R1, second & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Section4 bounds', name, bank, first, count, mode, detail))
                if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                    raise AssertionError(('Section4 return differs', name, count, mode, detail))
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        actual = machine.mem_read(address, len(data))
                        differences = [(hex(address + index), actual[index], value) for index, value in enumerate(data) if actual[index] != value]
                        raise AssertionError(('Section4/current/selection/other-section guards differ', name, bank, first, count, mode, detail, differences[:8]))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedWholeSectionAndGuardRam': True, 'platformStubs': {}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['The5008-byte serialized section is80 prefix bytes plus8 records of616 bytes; this is structure-only evidence.', 'Append rejects current byte0xAF>=7 or count exactly8, copies616 bytes, applies mode-dependent flags and increments count.', 'Count values above8 bypass the equality guard and can write into neighboring mapped state; those are isolated malformed-state observations.', 'Removal zeroes the selected record, compacts records whose byte0xAF is nonzero, then clears unused records up to8.', 'Read copies a complete record and stores the low-byte selected index; selected flag update uses that raw index without a count check.', 'Current halfword setter uses stride0x84 and truncates to16 bits without an observed bound check.'], 'limitations': ['Record gameplay purpose, prefix fields, byte0xAF meaning and mode labels remain unnamed.', 'No field-meaning bytes are added to the saved semantic partition; section4 remains opaque except for measured byte structure.', 'Negative/out-of-capacity indices and counts9/10 are bounded ARM-state probes, not valid operation contracts.', 'Native copy/fill and mode/pointer callees execute; accepted sources are reused where already registered.', 'No device, UI, network or full-emulator operation is executed.']}
