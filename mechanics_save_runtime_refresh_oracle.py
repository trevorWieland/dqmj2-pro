import hashlib
import json
import random
import struct
import time
from pathlib import Path

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
from mechanics_save_record_update_oracle import lookup
import mechanics_save_runtime_view_oracle as view_model
import mechanics_save_native_name_oracle as name_model

EKT = 0x02500000
SKILL = 0x02510000
FEAT = 0x02520000
POINTERS = 0x02540000
BASE = 0x02550000
SUFFIX = 0x02560000
RECORDS = 0x021bd674
SIDE = 0x021c3880
RUNTIME = 0x021c0ef4
VIEWS = RUNTIME + 32
MODE = 0x020f69e8
STOP = 0x027ff800
RETAINED = {0x02008c14: (20, 'SDK word fill'), 0x02008d78: (148, 'SDK byte fill'), 0x02008e0c: (304, 'SDK byte copy'), 0x02008c58: (76, 'SDK bulk word fill'), 0x02044ff4: (148, 'native name builder')}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm, matches):
    paths = [root / batch['report'] for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']]
    paths.extend(root / ('evidence/matches/mechanics-save-' + suffix + '.json') for suffix in ('roster', 'features', 'action-banks', 'projection', 'runtime-view', 'native-name'))
    rows = {}
    for path in paths:
        document = json.loads(path.read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Runtime refresh ROM namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            if row.get('module') in ('main', 'arm9'):
                rows[int(row['address'], 16)] = row
    builder_calls = set()
    for offset in range(0x44ff4, 0x45084, 4):
        word = struct.unpack_from('<I', arm, offset)[0]
        if word & 0x0f000000 == 0x0b000000:
            displacement = (word & 0xffffff) * 4
            if displacement & 0x2000000:
                displacement -= 0x4000000
            builder_calls.add(0x02000000 + offset + 8 + displacement)
    if builder_calls != {0x0205dc70, 0x0205dcbc, 0x0205dcfc, 0x02044d84}:
        raise AssertionError('Retained name builder direct-call graph differs')
    wanted = builder_calls | {int(relocation['target'], 16) for row, code in matches.values() for relocation in row.get('relocations', []) if relocation['type'] in (1, 28, 29)}
    result = {}
    while wanted:
        address = wanted.pop()
        if address in result or address in RETAINED:
            continue
        if address not in rows:
            raise AssertionError(('Runtime refresh unresolved direct callee', hex(address)))
        row = rows[address]
        if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
            raise AssertionError('Runtime refresh source/object hash differs')
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
            if relocation['type'] in (1, 28, 29):
                wanted.add(int(relocation['target'], 16))
        if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
            raise AssertionError('Runtime refresh dependency native bytes differ')
        result[address] = (row, bytes(code))
    return result

def view_expected(memory, arm, blobs, destination, record):
    previous = view_model.VIEW
    view_model.VIEW = destination
    try:
        return view_model.expected(memory, arm, *blobs, record, 0)
    finally:
        view_model.VIEW = previous

def expected(memory, arm, blobs, mode, arguments):
    if mode in (0, 3, 5, 6, 7, 8):
        for index in range(3):
            identity = u32(memory, 0x021bd540 + index * 4)
            record = lookup(memory, identity)
            view_expected(memory, arm, blobs, VIEWS + index * 528, record or 0)
        put(memory, RUNTIME, u32(memory, 0x021bd538))
    elif mode == 4:
        count = sum(u32(memory, SIDE + index * 132 + 20) != 0 for index in range(3))
        write(memory, VIEWS, bytes(1584))
        for index in range(3):
            write(memory, VIEWS + index * 528 + 46, b'\xff\xff')
        for index in range(count):
            view_expected(memory, arm, blobs, VIEWS + index * 528, SIDE + index * 132)
        put(memory, RUNTIME, 0)
    elif mode == 1:
        for index, value in enumerate(arguments):
            write(memory, VIEWS + index * 528 + 46, struct.pack('<H', value & 65535))
        for index in range(3):
            at = VIEWS + index * 528
            species = struct.unpack('<h', read(memory, at + 46, 2))[0]
            if species >= 0:
                variant = read(memory, at + 48, 1)[0]
                previous = name_model.EKT
                name_model.EKT = EKT
                try:
                    name_model.expected(memory, 'native-builder', at + 182, species, variant)
                finally:
                    name_model.EKT = previous

def validate(arm, save, matches, root):
    reused = dependencies(root, arm, matches)
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
    blobs = assets['EnmyKindTbl.bin'][8:], assets['SkillTbl.bin'], assets['FeatTbl.bin']
    rng = random.Random(20261027)
    groups = ([1, 2, 3], [0, 0, 0], [1, 0, 3], [3, 1, 1], [0xffffffff, 2, 0], [0, 2, 3], [0, 0, 3], [3, 2, 1])
    vectors = [(mode, pattern, (0, 139, -1), pattern % 512) for mode in (*range(10), 255) for pattern in range(8)]
    vectors += [(mode, 0, (species, (species + 1) % 512, -1), species) for mode in (0, 1, 4) for species in range(512)]
    vectors += [(1, 0, arguments, 139) for arguments in ((-32768, -1, 0), (511, 139, 0), (65536, 65535, -65536))]
    cases = calls = 0
    for mode, pattern, arguments, species in vectors:
        original = {0x020da000: bytearray(arm[0xda000:0xdb000]), 0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021bd000: bytearray(rng.randbytes(0x5000)), 0x021c3000: bytearray(rng.randbytes(0x2000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), EKT: bytearray(blobs[0] + bytes(0x10000 - len(blobs[0]))), SKILL: bytearray(blobs[1] + bytes(0x4000 - len(blobs[1]))), FEAT: bytearray(blobs[2] + bytes(0x1000 - len(blobs[2]))), POINTERS: bytearray(0x6000), BASE: bytearray(0x4000), SUFFIX: bytearray(0x2000)}
        write(original, 0x021bd51c, save[0x90:0x3a68])
        for index in range(100):
            data = bytearray(rng.randbytes(132))
            struct.pack_into('<IhB', data, 20, index + 1, (species + index) % 512, index % 3)
            data[122:132] = bytes([1, 0, 2, 255, 128, 100, 255, 255, 0, 0])
            write(original, RECORDS + index * 132, bytes(data))
        write(original, 0x021bd540, struct.pack('<III', *groups[pattern]))
        for index in range(3):
            data = bytearray(read(original, RECORDS + index * 132, 132))
            struct.pack_into('<I', data, 20, groups[pattern][index])
            write(original, SIDE + index * 132, bytes(data))
            write(original, VIEWS + index * 528 + 48, bytes([index]))
        write(original, MODE, bytes([mode]))
        put(original, 0x020f69f0, EKT)
        put(original, 0x021c673c, SKILL)
        put(original, 0x021c6740, 256)
        put(original, 0x021c6750, FEAT)
        put(original, 0x021c6754, FEAT + 8)
        for group in range(4):
            put(original, name_model.ROOTS + group * 4, POINTERS + group * 8)
            for table in range(2):
                vector = POINTERS + 0x1000 + (group * 2 + table) * 0x800
                put(original, POINTERS + group * 8 + table * 4, vector)
                for identity in range(512):
                    put(original, vector + identity * 4, BASE + identity * 32 if table == 0 else SUFFIX + identity * 16)
        for identity in range(512):
            write(original, BASE + identity * 32, bytes([0x80 + identity % 64, 0x40 + identity // 64, 0x60 + identity % 16, 0xe3, 0x1b]))
            write(original, SUFFIX + identity * 16, bytes([0x50 + identity % 16, 0x70 + identity // 64, 0xe3, 0x1b]))
        memory = {address: bytearray(data) for address, data in original.items()}
        expected(memory, arm, blobs, mode, arguments)
        row, code = next(iter(matches.values()))
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            machine.mem_write(0x027f0000, bytes(0x10000))
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                machine.reg_write(register, value & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=2000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError(('Runtime refresh bounds', mode, pattern, species))
            for address, data in memory.items():
                observed = bytes(machine.mem_read(address, len(data)))
                if observed != data:
                    at = next(index for index, (left, right) in enumerate(zip(observed, data)) if left != right)
                    raise AssertionError(('Runtime refresh state/table/text/guard RAM', mode, pattern, species, hex(address + at), observed[at], data[at]))
            calls += 1
        cases += 1
    models = ('mechanics_save_runtime_view_oracle.py', 'mechanics_save_native_name_oracle.py', 'mechanics_save_features_oracle.py', 'mechanics_save_action_banks_oracle.py', 'mechanics_save_projection_oracle.py', 'mechanics_save_roster_oracle.py')
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 2000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedModeViewsTextAndGold': True, 'platformStubs': {}, 'transitiveDirectCallClosureChecked': True, 'patchedDependencyFunctions': len(reused), 'retainedNativeDependencies': [{'module': 'main', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'role': role} for address, (size, role) in RETAINED.items()], 'seededStack': {'address': '0x027f0000', 'bytes': 65536, 'valueHex': '00', 'reason': 'Bound retained native name-builder local padding, without assuming arbitrary inherited stack contents.'}, 'expectedModels': [{'source': name, 'sha256': sha((root / name).read_bytes())} for name in models], 'assetSha256': {name: sha(blob) for name, blob in assets.items()}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Modes0/3/5/6/7/8 refresh three party views and snapshot the raw purse word; null/missing party references change only each species marker.', 'Mode4 clears all three528-byte views, marks all species as-1, converts only the first N side records where N counts all three nonzero IDs, then sets the runtime purse snapshot to0.', 'Sparse side-record layouts therefore process a prefix rather than skipping holes to seek every occupied entry.', 'Mode1 truncates three input species halfwords and rebuilds names only for nonnegative markers, preserving other view state; mode2 and values outside0..8 make no changes.', 'All512 species in party/name/side modes, sparse and duplicate references, signed-halfword input truncation and complete source/table/runtime/text guards are tested.'], 'limitations': ['Four SDK memory primitives and the148-byte native name builder remain retained ARM dependencies; every declared direct call and retained builder call is explicitly resolved.', 'The stack starts zeroed to bound name-builder padding reads; text tables contain controlled raw strings rather than decoded original names.', 'Mode meanings and runtime fields stay technical; this is no full battle/scene, encoding or legal game-state model.', 'No new save-byte meanings or original game/save inputs are changed.']}
