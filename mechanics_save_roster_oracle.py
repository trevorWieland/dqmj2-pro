import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

MAIN = 0x021bd51c
RECORDS = 0x021bd674
PARTY = 0x021bd540
RESERVE = 0x021bd54c
COUNTS = 0x021bd558
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02062a10, 0x02062a50, 0x02062a68, 0x02062a78, 0x02062a88, 0x02063144, 0x02062bf0}
    result = {}
    for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']:
        document = json.loads((root / batch['report']).read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Roster dependency namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if address not in wanted or row.get('module') not in ('main', 'arm9'):
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Roster dependency identity differs')
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
                raise AssertionError('Roster dependency bytes differ')
            result[address] = (row, bytes(code))
    if not wanted.issubset(result):
        raise AssertionError(('Accepted roster dependencies absent', sorted(wanted - set(result))))
    return result

def all_records(memory):
    return [read(memory, RECORDS + index * 132, 132) for index in range(100)]

def grouped(memory, records, base):
    result = []
    for slot in range(3):
        identity = u32(memory, base + slot * 4)
        if identity:
            found = next((record for record in records if struct.unpack_from('<I', record, 20)[0] == identity), None)
            if found is not None:
                result.append(found)
    return result

def species_count(records, species, variant):
    return sum(struct.unpack_from('<h', record, 24)[0] == species and (variant == 4 or record[26] == variant) for record in records)

def expected(memory, name, first, second):
    records = all_records(memory)
    party = grouped(memory, records, PARTY)
    reserve = grouped(memory, records, RESERVE)
    if name == 'saved_roster_species_count':
        return species_count([record for record in records if struct.unpack_from('<I', record, 20)[0]], first, second)
    if name == 'saved_reserve_species_count':
        return species_count(reserve, first, second)
    if name == 'native_main_02062bf0':
        return species_count(party, first, second)
    equipped = sum(record[49] == first for record in [*party, *reserve])
    if name == 'saved_equipped_item_count':
        return equipped
    if name == 'saved_inventory_unequipped_raw':
        quantity = 0 if first >= 255 else struct.unpack('<b', read(memory, COUNTS + first, 1))[0]
        return quantity - equipped
    raise AssertionError(('Unknown roster function', name))

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    tests = dict(matches)
    row, code = reused[0x02062bf0]
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
    rng = random.Random(20261027)
    cases = 0
    calls = 0
    fixtures = ['captured-primary', 'captured-backup', 'zero-identities', 'distinct', 'duplicate-identities', 'duplicate-references', 'missing-references', 'signed-species']
    for fixture in fixtures:
        memory = {0x021bd000: bytearray(rng.randbytes(0x5000))}
        bank = 0x7100 if fixture == 'captured-backup' else 0
        write(memory, MAIN, save[bank + 0x90:bank + 0x3a68])
        if not fixture.startswith('captured'):
            for index in range(100):
                data = bytearray(rng.randbytes(132))
                identity = 0 if fixture == 'zero-identities' else index + 1
                if fixture == 'duplicate-identities' and index in (0, 1, 2):
                    identity = 1
                struct.pack_into('<I', data, 20, identity)
                struct.pack_into('<H', data, 24, [0, 1, 139, 431, 511, 0xffff, 0x8000, 0x7fff][index % 8])
                data[26] = [0, 1, 2, 3, 4, 255][index % 6]
                data[49] = [0, 1, 2, 127, 128, 255][index % 6]
                write(memory, RECORDS + index * 132, bytes(data))
            party = [1, 2, 3]
            reserve = [4, 5, 6]
            if fixture == 'duplicate-references':
                party = reserve = [1, 1, 1]
            elif fixture == 'missing-references':
                party = reserve = [0, 9999, 0xffffffff]
            elif fixture == 'duplicate-identities':
                party = reserve = [1, 2, 3]
            write(memory, PARTY, struct.pack('<III', *party))
            write(memory, RESERVE, struct.pack('<III', *reserve))
            write(memory, COUNTS, bytes([0, 1, 127, 128, 255]) * 51)
        for machine in machines:
            for address, data in memory.items():
                machine.mem_write(address, bytes(data))
        for name, (row, code) in tests.items():
            if name in ('saved_roster_species_count', 'saved_reserve_species_count', 'native_main_02062bf0'):
                vectors = [(species, variant) for species in (-32768, -1, 0, 1, 2, 139, 176, 188, 350, 431, 511, 32767, 65535, -0x80000000) for variant in (-1, 0, 1, 2, 3, 4, 255, 256)]
            else:
                vectors = [(item, 0) for item in [-33, -1, *range(257)]]
            for first, second in vectors:
                result = expected(memory, name, first, second)
                for machine in machines:
                    machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
                    machine.reg_write(UC_ARM_REG_R1, second & 0xffffffff)
                    machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                    machine.reg_write(UC_ARM_REG_LR, STOP)
                    began = time.monotonic()
                    machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                    if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                        raise AssertionError(('Roster execution bounds', fixture, name, first, second))
                    if machine.reg_read(UC_ARM_REG_R0) != result & 0xffffffff:
                        raise AssertionError(('Roster count/raw quantity differs', fixture, name, first, second, machine.reg_read(UC_ARM_REG_R0), result))
                    for address, data in memory.items():
                        if bytes(machine.mem_read(address, len(data))) != data:
                            raise AssertionError(('Read-only roster/inventory/guard RAM changed', fixture, name))
                    calls += 1
                cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(tests), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedCountsAndUnchangedRam': True, 'platformStubs': {}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Roster counting requires nonzero saved identity, signed16-bit species equality and variant equality except for wildcard4.', 'Party/reserve references resolve the first matching nonzero identity, while raw full-roster counts can include multiple records with duplicate identities.', 'Repeated group references are counted per slot; the same identity referenced six times can contribute six equipment matches.', 'Raw unequipped quantity is signed inventory count minus equipment matches without clamping and can be negative.', 'Equipment byte0 and raw signed species/variant values are observed without imposing valid gameplay labels.'], 'limitations': ['No platform/gameplay function is substituted; all record lookup and inventory callees execute.', 'These counts do not establish owned-individual validity, uniqueness or resource availability for malformed saves.', 'Negative inventory indices are bounded pre-array ARM reads; the original getter lacks a lower-bound check, and no legal-index claim is made.', 'No new semantic partition promotion occurs.']}
