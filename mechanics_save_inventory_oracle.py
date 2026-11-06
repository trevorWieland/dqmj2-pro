import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

MAIN = 0x021bd51c
COUNTS = 0x021bd558
SLOTS = 0x021bd658
OPTIONS = 0x021bd664
MARKER = 0x021bd66e
TABLE_STATE = 0x021c2ab4
TABLE = 0x02500000
SECONDARY = 0x021c0ee0
EVENT = 0x021c0e20
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02063144, 0x02063280, 0x020632e0, 0x02063348, 0x02063294, 0x02063b40, 0x02063b60, 0x02063bbc, 0x02063bdc, 0x02063c00, 0x02063c94}
    result = {}
    for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']:
        document = json.loads((root / batch['report']).read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Inventory dependency namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if address not in wanted or row.get('module') not in ('main', 'arm9'):
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Accepted inventory dependency hash differs')
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
                raise AssertionError('Accepted inventory dependency bytes differ')
            result[address] = (row, bytes(code))
    if not {0x02063144, 0x02063294, 0x02063c00}.issubset(result):
        raise AssertionError('Required inventory/source membership dependencies absent')
    return result

def bit(memory, base, index):
    return (u32(memory, base + (index >> 5) * 4) >> (index & 31)) & 1

def set_bit(memory, base, index):
    at = base + (index >> 5) * 4
    put(memory, at, u32(memory, at) | (1 << (index & 31)))

def expected(memory, table, defaults, name, first):
    if name == 'saved_native_item_record':
        return (TABLE + first * 88) & 0xffffffff
    if name == 'saved_inventory_nonzero_type_count':
        counts = read(memory, COUNTS, 255)
        return sum(value != 0 and (first not in (0, 1) or bool(table[index * 88 + 46] & (1 << first))) for index, value in enumerate(counts))
    if name == 'saved_raw_slots_initialize':
        write(memory, SLOTS, defaults)
        write(memory, OPTIONS, bytes([127]) * 4)
        write(memory, MARKER, b'\x7f')
        previous = bit(memory, SECONDARY, 0)
        set_bit(memory, SECONDARY, 0)
        if not previous:
            set_bit(memory, SECONDARY, 64)
            set_bit(memory, EVENT, 76)
        return None
    slots = read(memory, SLOTS, 12)
    if name == 'saved_raw_slot_insert':
        if 127 not in slots:
            return 0
        write(memory, SLOTS + slots.index(127), bytes([first & 255]))
        return 1
    if name == 'native_main_02063294':
        return int(first in list(slots))
    raise AssertionError(('Unknown inventory function', name))

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    tests = dict(matches)
    row, code = reused[0x02063294]
    tests[row['name']] = (row, code)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    blob = NintendoDSRom((root / 'inputs/game.nds').read_bytes()).getFileByName('ItemTbl.bin')
    if len(blob) != 22536 or blob[:8] != b'ITEM\0\x01\0\0':
        raise AssertionError('Measured ItemTbl layout differs')
    actual_table = blob[8:]
    synthetic_table = bytearray(actual_table)
    for index in range(256):
        synthetic_table[index * 88 + 46] = index & 3
    defaults = arm[0xdae7c:0xdae88]
    rng = random.Random(20261027)
    cases = 0
    calls = 0
    for fixture, table in [('measured', actual_table), ('synthetic-flags', bytes(synthetic_table))]:
        for bank in (0, 0x7100):
            vectors = []
            for name in tests:
                if name == 'saved_native_item_record':
                    vectors += [(name, index, None) for index in [-1, *range(257)]]
                elif name == 'saved_inventory_nonzero_type_count':
                    vectors += [(name, category, counts) for category in (-1, 0, 1, 2, 255) for counts in [None, bytes(255), bytes([1]) * 255, bytes([255]) * 255, bytes([0, 127, 128]) * 85, *[rng.randbytes(255) for _ in range(32)]]]
                elif name == 'saved_raw_slots_initialize':
                    vectors += [(name, index, None) for index in range(8)]
                elif name == 'saved_raw_slot_insert':
                    vectors += [(name, value, position) for value in (-1, 0, 127, 128, 255, 256, 0xffffffff) for position in range(-1, 14)]
                else:
                    vectors += [(name, value, None) for value in [-1, *range(257)]]
            for name, first, detail in vectors:
                original = {0x021bd000: bytearray(rng.randbytes(0x5000)), 0x021c2a00: bytearray(rng.randbytes(0x1000)), TABLE: bytearray(table + bytes(0x6000 - len(table)))}
                write(original, MAIN, save[bank + 0x90:bank + 0x3a68])
                put(original, TABLE_STATE, TABLE)
                if name == 'saved_inventory_nonzero_type_count' and detail is not None:
                    write(original, COUNTS, detail)
                elif name == 'saved_raw_slots_initialize':
                    for base, index, enabled in [(SECONDARY, 0, first & 1), (SECONDARY, 64, first & 2), (EVENT, 76, first & 4)]:
                        at = base + (index >> 5) * 4
                        mask = 1 << (index & 31)
                        put(original, at, u32(original, at) | mask if enabled else u32(original, at) & ~mask)
                elif name == 'saved_raw_slot_insert':
                    slots = bytearray([12 + index for index in range(12)])
                    if detail == 12:
                        slots[:] = bytes([127]) * 12
                    elif detail == 13:
                        slots[2] = slots[9] = 127
                    elif detail >= 0:
                        slots[detail] = 127
                    write(original, SLOTS, bytes(slots))
                memory = {address: bytearray(data) for address, data in original.items()}
                result = expected(memory, table, defaults, name, first)
                row, code = tests[name]
                for machine in machines:
                    for address, data in original.items():
                        machine.mem_write(address, bytes(data))
                    machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
                    machine.reg_write(UC_ARM_REG_R1, 0)
                    machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                    machine.reg_write(UC_ARM_REG_LR, STOP)
                    began = time.monotonic()
                    machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                    if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                        raise AssertionError(('Inventory bounds', fixture, name, bank, first))
                    if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                        raise AssertionError(('Inventory result differs', fixture, name, first, machine.reg_read(UC_ARM_REG_R0), result))
                    for address, data in memory.items():
                        if bytes(machine.mem_read(address, len(data))) != data:
                            raise AssertionError(('Inventory/selector/secondary/itemtable/guard RAM differs', fixture, name, first, detail))
                    calls += 1
                cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(tests), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRamAndReturn': True, 'platformStubs': {}, 'itemAssetSha256': sha(blob), 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['The count loops through255 slots and counts every nonzero signed inventory byte, including negative values; this is not a count of available resources.', 'Category0/1 filter ItemTbl byte0x2E bit0/bit1 respectively; all other category arguments skip those filters.', 'Raw selector initialization copies12 measured default bytes, writes127 to four option bytes and one marker, then invokes recovered secondary bit0 update.', 'A newly set secondary bit0 also sets history bit64 and event bit76; existing bit0 skips those additional effects.', 'Insertion writes the first127 sentinel slot, truncates the value to8 bits and returns1 even if127 is written back; a full array returns0.'], 'limitations': ['No platform or gameplay function is substituted; existing inventory/selector/secondary sources execute.', 'Raw selector/option/marker purpose and ItemTbl flag labels remain unnamed.', 'The ItemTbl contains256 records but the nonzero-count loop excludes index255.', 'Out-of-table pointer results are arithmetic probes without dereference or legal-index claims.', 'No new semantic partition promotion or inventory-consumption claim is made.']}
