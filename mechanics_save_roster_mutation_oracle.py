import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
from mechanics_save_record_update_oracle import lookup
from verify_record_features import compiled
import mechanics_save_library_oracle as library
import mechanics_save_features_oracle as features

EKT = 0x02500000
SKILL = 0x02510000
FEAT = 0x02520000
RECORDS = 0x021bd674
PARTY = 0x021bd540
RESERVE = 0x021bd54c
COUNTER = 0x021bd520
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    result = compiled(arm)
    result.update(library.dependencies(root, arm))
    wanted = {0x02062638, 0x020626d0, 0x020627ec, 0x02062828}
    registry = json.loads((root / 'recovery.json').read_text(encoding='utf-8'))
    paths = [root / batch['report'] for batch in registry['batches']]
    paths.append(root / 'evidence/matches/mechanics-save-library.json')
    for path in paths:
        document = json.loads(path.read_text(encoding='utf-8'))
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if row.get('module') not in ('main', 'arm9') or (address not in wanted and path.name != 'mechanics-save-library.json'):
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Roster mutation dependency identity differs')
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
                raise AssertionError('Roster mutation dependency span differs')
            result[address] = (row, bytes(code))
    if not wanted.issubset(result):
        raise AssertionError('Roster mutation required source absent')
    return result

def feature_observe(memory, blobs, record):
    ekt, skills, feat = blobs
    species = struct.unpack('<h', read(memory, record + 24, 2))[0]
    variant = read(memory, record + 26, 1)[0]
    output, count = features.collect(ekt, skills, feat, species, variant, read(memory, record + 122, 10), 256, 256)
    for identity in output:
        library.set_bit(memory, 0x021c0b84, identity)

def secondary_set(memory, identity):
    previous = library.bit(memory, library.SECONDARY, identity)
    library.set_bit(memory, library.SECONDARY, identity)
    if not previous:
        library.set_bit(memory, library.SECONDARY, identity + 64)
        library.set_bit(memory, library.EVENT, 76)

def expected(memory, blobs, name, first, second):
    if name == 'saved_record_first_free':
        return next((RECORDS + index * 132 for index in range(100) if not u32(memory, RECORDS + index * 132 + 20)), 0)
    if name == 'saved_record_features_observe':
        feature_observe(memory, blobs, first)
        return None
    if name == 'saved_record_create':
        record = expected(memory, blobs, 'saved_record_first_free', 0, 0)
        if not record:
            return 0
        write(memory, record, bytes(132))
        write(memory, record + 24, struct.pack('<hB', first, second))
        identity = (u32(memory, COUNTER) + 1) & 0xffffffff
        put(memory, COUNTER, identity)
        put(memory, record + 20, identity)
        library.expected(memory, blobs[0], 'saved_library_obtained_set', first, second, 0)
        library.expected(memory, blobs[0], 'saved_library_seen_set', first, second, 0)
        category = ((struct.unpack_from('<H', blobs[0], first * 100 + 4)[0] >> 8) & 15) // 3
        if category != 2 or library.bit(memory, library.EVENT, 16):
            feature_observe(memory, blobs, record)
        records = [read(memory, RECORDS + index * 132, 132) for index in range(100)]
        records.sort(key=lambda value: (struct.unpack_from('<I', value, 20)[0] == 0, struct.unpack_from('<I', value, 20)[0]))
        write(memory, RECORDS, b''.join(records))
        return identity
    group = PARTY if 'party' in name else RESERVE
    values = [u32(memory, group + index * 4) for index in range(3)]
    if name.endswith('_has_id'):
        return int(first != 0 and first in values)
    if name.endswith('_insert_id'):
        if not lookup(memory, first) or first in values or 0 not in values:
            return 0
        put(memory, group + values.index(0) * 4, first)
        if group == RESERVE:
            secondary_set(memory, 14)
            secondary_set(memory, 15)
        return 1
    if name.endswith('_remove_index'):
        if not 0 <= first < 3 or not values[first]:
            return 0
        result = values[first]
        values.pop(first)
        values.append(0)
        write(memory, group, struct.pack('<III', *values))
        return result
    raise AssertionError('Unexpected roster mutation operation')

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
    rom = NintendoDSRom((root / 'inputs/game.nds').read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'SkillTbl.bin', 'FeatTbl.bin')}
    blobs = (assets['EnmyKindTbl.bin'][8:], assets['SkillTbl.bin'], assets['FeatTbl.bin'])
    rng = random.Random(20261027)
    cases = calls = 0
    vectors = []
    for name in matches:
        if name == 'saved_record_create':
            vectors.extend((name, species, species % 3, species % 4, species & 1) for species in range(512))
            vectors.extend((name, species, variant, pattern, gate) for species in (0, 139, 353, 452, 455, 500, 511) for variant in (0, 1, 2) for pattern in (0, 3, 4) for gate in (False, True))
        elif name == 'saved_record_features_observe':
            vectors.extend((name, RECORDS, 0, species, False) for species in range(512))
        elif name == 'saved_record_first_free':
            vectors.extend((name, 0, 0, pattern, False) for pattern in range(5))
        else:
            arguments = (-1, 0, 1, 2, 3, 4, 0x7fffffff, 0xffffffff) if name.endswith('_remove_index') else (0, 1, 2, 3, 4, 8, 0xffffffff)
            vectors.extend((name, first, 0, pattern, gate) for first in arguments for pattern in range(8) for gate in (False, True))
    for name, first, second, pattern, gate in vectors:
        original = {0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021b9000: bytearray(rng.randbytes(0x9000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), EKT: bytearray(blobs[0] + bytes(0x10000 - len(blobs[0]))), SKILL: bytearray(blobs[1] + bytes(0x4000 - len(blobs[1]))), FEAT: bytearray(blobs[2] + bytes(0x1000 - len(blobs[2])))}
        write(original, 0x021bd51c, save[0x90:0x3a68])
        write(original, RECORDS, bytes(13200))
        filled = 100 if pattern == 4 else 99 if pattern == 3 else 3
        for index in range(filled):
            data = bytearray(rng.randbytes(132))
            species = pattern if name == 'saved_record_features_observe' else index % 512
            struct.pack_into('<IhB', data, 20, index + 1, species, species % 3)
            data[122:132] = bytes([1, 0, 2, 255, 128, 100, 255, 255, 0, 0])
            write(original, RECORDS + index * 132, bytes(data))
        if name == 'saved_record_first_free':
            free_index = [0, 1, 50, 99, None][pattern]
            if free_index is not None:
                for index in range(100):
                    put(original, RECORDS + index * 132 + 20, index + 1)
                put(original, RECORDS + free_index * 132 + 20, 0)
        put(original, COUNTER, 200)
        groups = ([1, 2, 3], [0, 0, 0], [1, 0, 2], [0, 1, 2], [1, 1, 0], [0xffffffff, 0, 0], [0, 0, 3], [3, 2, 1])[pattern % 8]
        write(original, PARTY, struct.pack('<III', *groups))
        write(original, RESERVE, struct.pack('<III', *reversed(groups)))
        put(original, 0x020f69f0, EKT)
        put(original, 0x021c673c, SKILL)
        put(original, 0x021c6740, 256)
        put(original, 0x021c6750, FEAT)
        put(original, 0x021c6754, FEAT + 8)
        put(original, library.EVENT, u32(original, library.EVENT) | (1 << 16) if gate else u32(original, library.EVENT) & ~(1 << 16))
        if not gate:
            write(original, library.SECONDARY, bytes(0x14))
        memory = {address: bytearray(data) for address, data in original.items()}
        result = expected(memory, blobs, name, first, second)
        row, code = matches[name]
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            machine.reg_write(UC_ARM_REG_R0, first & 0xffffffff)
            machine.reg_write(UC_ARM_REG_R1, second)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=2000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError(('Roster mutation bounds', name, first, pattern))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('Roster mutation return', name, first, pattern, machine.reg_read(UC_ARM_REG_R0), result))
            for address, data in memory.items():
                observed = bytes(machine.mem_read(address, len(data)))
                if observed != data:
                    at = next(index for index, (left, right) in enumerate(zip(observed, data)) if left != right)
                    raise AssertionError(('Roster/library/group/guard RAM', name, first, pattern, hex(address + at), observed[at], data[at]))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 2000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRosterLibraryFeaturesGroupsAndSort': True, 'platformStubs': {}, 'retainedNativeDependencies': [{'module': 'main', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'role': role} for address, size, role in ((0x02008d78, 148, 'SDK fill'), (0x0201d470, 356, 'SDK heap sort; matched native comparator callback executes'))], 'assetSha256': {name: sha(blob) for name, blob in assets.items()}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Creation clears132 bytes at the first zero-ID record, stores species/variant, increments the raw ID counter, updates obtained/seen flags, conditionally observes features and sorts the roster by native ID.', 'Feature observation iterates all64 collector bytes, including cleared trailing zeros, so raw feature bit0 is set whenever observation runs.', 'Party/reserve insertion rejects missing IDs and duplicates, fills the first empty slot; reserve insertion also executes secondary flags14/15 and their history/event effects.', 'Removal compacts only when the selected slot is nonzero; a zero slot leaves later holes untouched.', 'Every native species, native library exception IDs, category2 event gating, full roster, missing references, duplicate group references and signed/unsigned removal boundaries are tested.'], 'limitations': ['SDK fill and heap sort remain retained native ARM rather than source-match credit; no provider is substituted.', 'Creation counter-overflow/collision sorting and indistinguishable zero-ID records with nonzero payloads are outside this bounded unique-ID proof.', 'All64-byte observation includes raw feature0; no feature name or complete gameplay consequence is inferred.', 'Native observer02064038 remains an unmatched draft due to register allocation and contributes no source credit.', 'No new semantic partition bytes or original assets are modified.']}
