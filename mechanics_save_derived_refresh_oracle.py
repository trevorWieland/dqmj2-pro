import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from ndspy.rom import NintendoDSRom
from save_worker_oracle import read, write, put, u32
import mechanics_save_features_oracle as feature_model
import mechanics_save_feature_bonus_oracle as bonus_model
from mechanics_save_record_update_oracle import lookup
from verify_record_features import compiled

EKT = 0x02500000
SKILL = 0x02510000
FEAT = 0x02520000
ITEM = 0x02530000
RECORDS = 0x021bd674
PARTY = 0x021bd540
RESERVE = 0x021bd54c
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pointer_dependencies(root, arm):
    wanted = {0x02062a50, 0x02062a88, 0x0206342c, 0x0206347c}
    result = {}
    registry = json.loads((root / 'recovery.json').read_text(encoding='utf-8'))
    for batch in registry['batches']:
        document = json.loads((root / batch['report']).read_text(encoding='utf-8'))
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if row.get('module') not in ('main', 'arm9') or address not in wanted:
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Refresh group dependency hash differs')
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
                raise AssertionError('Refresh group native span differs')
            result[address] = (row, bytes(code))
    if not wanted.issubset(result):
        raise AssertionError(('Refresh group dependency absent', sorted(wanted - set(result))))
    return result

def refresh(memory, identity, blobs, present):
    record = lookup(memory, identity)
    if not record:
        return 0
    ekt, skills, feat, items = blobs
    species = struct.unpack('<h', read(memory, record + 24, 2))[0]
    variant = read(memory, record + 26, 1)[0]
    features, count = feature_model.collect(ekt, skills if present else None, feat, species, variant, read(memory, record + 122, 10), 256, 256)
    block = read(memory, record + 32, 32)
    item = block[17]
    for family, at in ((24, 36), (26, 38)):
        base = struct.unpack_from('<h', block, 0 if family == 24 else 2)[0]
        value = base + bonus_model.bonus(features, family)
        if read(memory, bonus_model.TOGGLE, 1)[0]:
            value += items[8 + item * 88 + (33 if family == 24 else 34)]
        write(memory, record + at, struct.pack('<H', min(value, 9999) & 65535))
    write(memory, record + 51, b'\0')
    return 1

def validate(arm, save, matches, root):
    reused = compiled(arm)
    reused.update(pointer_dependencies(root, arm))
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*reused.values(), *matches.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rom = NintendoDSRom((root / 'inputs/game.nds').read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'SkillTbl.bin', 'FeatTbl.bin', 'ItemTbl.bin')}
    blobs = (assets['EnmyKindTbl.bin'][8:], assets['SkillTbl.bin'], assets['FeatTbl.bin'], assets['ItemTbl.bin'])
    rng = random.Random(20261027)
    fixtures = [(species, species % 3, species & 1, True, species % 8) for species in range(512)]
    fixtures += [(species, variant, toggle, present, pattern) for species in (0, 139, 353, 511) for variant in (0, 1, 2) for toggle in (0, 255) for present in (False, True) for pattern in range(8)]
    cases = calls = 0
    for species, variant, toggle, present, pattern in fixtures:
        original = {0x020ddd00: bytearray(rng.randbytes(0x100)), 0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021bd000: bytearray(rng.randbytes(0x5000)), 0x021c2a00: bytearray(rng.randbytes(0x1000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), EKT: bytearray(blobs[0] + bytes(0x10000 - len(blobs[0]))), SKILL: bytearray(blobs[1] + bytes(0x4000 - len(blobs[1]))), FEAT: bytearray(blobs[2] + bytes(0x1000 - len(blobs[2]))), ITEM: bytearray(blobs[3][8:] + bytes(0x6000 - len(blobs[3][8:])))}
        write(original, 0x021bd51c, save[0x90:0x3a68])
        write(original, RECORDS, bytes(13200))
        for index in range(3):
            data = bytearray(rng.randbytes(132))
            struct.pack_into('<IhB', data, 20, index + 1, species, variant)
            data[122:132] = bytes([1, 0, 2, 255, 128, 100, 255, 255, 0, 0])
            write(original, RECORDS + index * 132, bytes(data))
        first = [1, 2, 3] if pattern == 0 else [1, 1, 1] if pattern == 1 else [0, 0, 0] if pattern == 2 else [1, 0xffffffff, 3] if pattern == 3 else [1, 0, 1] if pattern == 4 else [3, 2, 1] if pattern == 5 else [0xffffffff] * 3 if pattern == 6 else [2, 2, 0]
        write(original, PARTY, struct.pack('<III', *first))
        write(original, RESERVE, struct.pack('<III', *reversed(first)))
        put(original, 0x020f69f0, EKT)
        put(original, 0x021c673c, SKILL if present else 0)
        put(original, 0x021c6740, 256)
        put(original, 0x021c6750, FEAT)
        put(original, 0x021c6754, FEAT + 8)
        put(original, 0x021c2ab4, ITEM)
        write(original, bonus_model.TOGGLE, bytes([int(toggle)]))
        vectors = [(name, identity) for name in matches for identity in ((0, 1, 2, 3, 0xffffffff) if name == 'saved_record_derived_refresh' else (0,))]
        for name, identity in vectors:
            memory = {address: bytearray(data) for address, data in original.items()}
            if name == 'saved_record_derived_refresh':
                result = refresh(memory, identity, blobs, present)
            else:
                group = PARTY if name == 'saved_party_derived_refresh' else RESERVE
                result = sum(refresh(memory, u32(memory, group + index * 4), blobs, present) for index in range(3))
            row, code = matches[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                machine.reg_write(UC_ARM_REG_R0, identity)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Derived refresh bounds', name, species, pattern))
                if machine.reg_read(UC_ARM_REG_R0) != result:
                    raise AssertionError(('Derived refresh return', name, species, pattern))
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        raise AssertionError(('Derived refresh record/group/table/guard RAM', name, species, variant, pattern, hex(address)))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRecordFeaturesEquipmentAndGroups': True, 'platformStubs': {}, 'retainedNativeDependency': {'module': 'main', 'mode': 'ARM', 'address': '0x02008d78', 'bytes': 148, 'sha256': sha(arm[0x8d78:0x8e0c]), 'role': 'SDK fill'}, 'assetSha256': {name: sha(blob) for name, blob in assets.items()}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Refresh collects features from the current species/variant/five skills, replaces halfwords0x24/0x26 with derived values and clears byte0x33.', 'Missing IDs return0 without writes; group aggregates execute all three slots, sum successful refresh calls and preserve duplicate references as repeated operations.', 'All512 species, signed base fields, toggles, missing skill table, repeated/missing/null group references and guard memory are tested.'], 'limitations': ['The SDK fill body executes retained native ARM; all gameplay callees use existing verified source bodies without duplicate credit.', 'Raw fields and feature effects do not establish complete stat growth, legal game state or ownership semantics.', 'No semantic partition bytes or original assets are changed.']}
