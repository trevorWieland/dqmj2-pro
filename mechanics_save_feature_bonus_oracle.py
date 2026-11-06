import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put

TABLE = 0x02500000
BLOCK = 0x02530080
FEATURES = 0x02540080
TOGGLE = 0x020ddd40
STOP = 0x027ff800
WEIGHTS = [5, 10, 15, 20, 22, 24, 26, 28, 30, 35]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x0206259c, 0x02065d88, 0x0207b674, 0x0207c2b8, 0x0207c3d8}
    reports = [root / batch['report'] for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']]
    reports.extend(root / 'evidence/matches' / name for name in ('mechanics-save-inventory.json', 'mechanics-save-features.json'))
    result = {}
    for path in reports:
        document = json.loads(path.read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Bonus dependency namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if address not in wanted or row.get('module') not in ('main', 'arm9'):
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Bonus dependency identity differs')
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
                raise AssertionError('Bonus dependency native span differs')
            result[address] = (row, bytes(code))
    if not wanted.issubset(result):
        raise AssertionError(('Required bonus dependencies absent', sorted(wanted - set(result))))
    return result

def bonus(values, family):
    if values is None:
        return 0
    total = 0
    for value in values[:64]:
        if not value:
            break
        index = value - (128 if family == 24 else 138)
        if 0 <= index < 10:
            total += WEIGHTS[index]
    return total

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    tests = dict(matches)
    for address in (0x0207c2b8, 0x0207c3d8):
        row, code = reused[address]
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
    table = bytes(NintendoDSRom((root / 'inputs/game.nds').read_bytes()).getFileByName('ItemTbl.bin'))
    if len(table) != 22536:
        raise AssertionError('Bonus ItemTbl length differs')
    items = table[8:]
    rng = random.Random(20261027)
    lists = [None, bytes(64), bytes([128]) * 64, bytes([137]) * 64, bytes([138]) * 64, bytes([147]) * 64, bytes([128, 0, 137]) + bytes(61)]
    lists += [bytes([identity]) * length + bytes(64 - length) for identity in range(128, 148) for length in (1, 2, 63, 64)]
    lists += [rng.randbytes(64) for _ in range(256)]
    cases = 0
    calls = 0
    for name, (row, code) in tests.items():
        family = 24 if name.endswith('24') or int(row['address'], 16) == 0x0207c2b8 else 26
        wrapper = name.startswith('native_main_')
        vectors = [(features, 0, 0, 0) for features in lists] if not wrapper else [(features, base, toggle, item) for features in lists[:7] for base in (-32768, -1, 0, 1, 9998, 9999, 10000, 32767) for toggle in (0, 1, 255) for item in (0, 1, 28, 127, 255)]
        if wrapper:
            vectors += [(lists[item % 7], 123, item & 1, item) for item in range(256)]
        for features, base, toggle, item in vectors:
            memory = {0x020ddd00: bytearray(rng.randbytes(0x1000)), 0x021c2a00: bytearray(rng.randbytes(0x1000)), TABLE: bytearray(items + bytes(0x6000 - len(items))), 0x02530000: bytearray(rng.randbytes(0x1000)), 0x02540000: bytearray(rng.randbytes(0x1000))}
            put(memory, 0x021c2ab4, TABLE)
            write(memory, TOGGLE, bytes([toggle]))
            if features is not None:
                write(memory, FEATURES, features)
            block = bytearray(rng.randbytes(32))
            struct.pack_into('<HH', block, 0, (base if family == 24 else base ^ 0x5555) & 65535, (base if family == 26 else base ^ 0xaaaa) & 65535)
            block[17] = item
            write(memory, BLOCK, bytes(block))
            result = bonus(features, family)
            if wrapper:
                result += base
                if toggle:
                    result += items[item * 88 + (33 if family == 24 else 34)]
                result = min(result, 9999)
            first = BLOCK if wrapper else FEATURES if features is not None else 0
            second = FEATURES if features is not None else 0
            for machine in machines:
                for address, data in memory.items():
                    machine.mem_write(address, bytes(data))
                machine.reg_write(UC_ARM_REG_R0, first)
                machine.reg_write(UC_ARM_REG_R1, second)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Bonus bounds', name, base, toggle, item))
                if machine.reg_read(UC_ARM_REG_R0) != result & 0xffffffff:
                    raise AssertionError(('Native weighted bonus/derived value differs', name, base, toggle, item, machine.reg_read(UC_ARM_REG_R0), result))
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        raise AssertionError(('Read-only bonus/block/ItemTbl/toggle/guard RAM changed', name))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(tests), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedWeightedFeaturesAndEquipment': True, 'platformStubs': {}, 'itemAssetSha256': sha(table), 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Native IDs128..137 and138..147 have weights5,10,15,20,22,24,26,28,30,35 in their respective accumulators.', 'Occurrences include duplicates before the first zero and stop at64 bytes; null lists contribute zero.', 'Existing derived wrappers add signed block halfword0/2 and, when the native toggle is nonzero, ItemTbl byte0x21/0x22 selected by block byte0x11.', 'Derived wrappers cap the result at9999 without a lower floor; negative signed base probes remain negative.', 'All feature-count, ItemTbl, toggle and wrapper callees execute from native or hash-verified accepted C.'], 'limitations': ['Native feature IDs and raw field projections do not establish all gameplay labels or effects.', 'Isolated signed-base/toggle probes do not establish legal battle state or full stat growth.', 'No platform/gameplay provider is substituted and no semantic partition bytes are promoted.']}
