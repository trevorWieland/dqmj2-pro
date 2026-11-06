import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
import mechanics_save_runtime_view_oracle as view_model
import mechanics_save_native_name_oracle as name_model
import mechanics_save_features_oracle as feature_model
import mechanics_save_feature_bonus_oracle as bonus_model
import mechanics_save_action_banks_oracle as action_model
import mechanics_save_projection_oracle as projection_model

EKT = 0x02500000
SKILL = 0x02510000
FEAT = 0x02520000
POINTERS = 0x02540000
BASE = 0x02550000
SUFFIX = 0x02560000
ITEM = 0x02570000
RECORDS = 0x021bd674
SAVED_GROUPS = 0x021bce0c
RUNTIME_GROUPS = 0x021c404c
ACTIVE_GROUP = 0x021c3730
RUNTIME = 0x021c0ef4
ENEMY = 0x021c1544
BATTLE_SKILLS = 0x02238d5c
MODE = 0x020f69e8
RNG = 0x020f6044
STOP = 0x027ff800
PARTS = ((0x90, 0x3a68, 0x021bd51c), (0x3a68, 0x3a9c, 0x021b9eb4), (0x3a9c, 0x5d40, 0x021bb278), (0x5d40, 0x70d0, 0x021b9ee8))
SAVED_REGISTERS = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
RETAINED = {0x02008c14: (20, 'SDK word fill'), 0x02008d78: (148, 'SDK byte fill'), 0x02008e0c: (304, 'SDK byte copy'), 0x02008c58: (76, 'SDK bulk word fill'), 0x02044ff4: (148, 'native name builder'), 0x02026350: (484, 'unsigned runtime division')}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, images, matches):
    paths = [root / batch['report'] for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']]
    paths.extend(root / ('evidence/matches/mechanics-save-' + suffix + '.json') for suffix in ('roster', 'features', 'feature-bonus', 'inventory', 'action-banks', 'projection', 'runtime-view', 'native-name', 'runtime-rng', 'battle-skill-pointer'))
    rows = {}
    for path in paths:
        document = json.loads(path.read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Initializer dependency ROM namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            module = 'main' if row.get('module') == 'arm9' else row.get('module')
            if module in images:
                rows[module, int(row['address'], 16)] = (row, document.get('nativeSymbolModules', {}))
    wanted = {('main', address) for address in (0x0205dc70, 0x0205dc88, 0x0205dcbc, 0x0205dcfc, 0x02044d84)}
    for row, code in matches.values():
        for relocation in row.get('relocations', []):
            if relocation['type'] in (1, 28, 29):
                wanted.add(('ov001' if relocation['symbol'] == 'native_battle_skills' else 'main', int(relocation['target'], 16)))
    result = {}
    while wanted:
        key = wanted.pop()
        module, address = key
        if key in result or module == 'main' and address in RETAINED:
            continue
        if key not in rows:
            raise AssertionError(('Initializer unresolved qualified call', key))
        row, qualifiers = rows[key]
        if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
            raise AssertionError('Initializer dependency source/object identity differs')
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
                target_module = qualifiers.get(relocation['symbol'], module)
                wanted.add(('main' if target_module == 'arm9' else target_module, int(relocation['target'], 16)))
        base, image = images[module]
        if code != image[address - base:address - base + row['bytes']]:
            raise AssertionError(('Initializer qualified native span differs', key))
        result[key] = (row, bytes(code))
    if ('ov001', 0x021e9164) not in result or ('main', 0x0203d294) not in result:
        raise AssertionError('Initializer qualified overlay/RNG source dependencies absent')
    return result

def constructor(memory, arm, blobs, destination, record, extra):
    previous = view_model.VIEW
    view_model.VIEW = destination
    try:
        view_model.expected(memory, arm, *blobs[:3], record, extra)
    finally:
        view_model.VIEW = previous

def random10(memory):
    state = (u32(memory, RNG) * 0x41c64e6d + 12345) & 0xffffffff
    put(memory, RNG, state)
    return (state >> 16) % 10 + 1

def derived(memory, items, destination):
    features = read(memory, destination + 74, 64)
    block = read(memory, destination + 284, 32)
    for family, offset in ((24, 4), (26, 6)):
        value = struct.unpack_from('<h', block, 0 if family == 24 else 2)[0] + bonus_model.bonus(features, family)
        if read(memory, bonus_model.TOGGLE, 1)[0]:
            value += items[8 + block[17] * 88 + (33 if family == 24 else 34)]
        write(memory, destination + 284 + offset, struct.pack('<H', min(value, 9999) & 65535))

def expected(memory, arm, blobs, mode, arguments):
    first, second, third = arguments
    if mode in (0, 2, 8):
        for index, value in enumerate(arguments):
            signed = (value & 65535) - (65536 if value & 32768 else 0)
            put(memory, ENEMY + index * 528, signed & 0xffffffff)
        write(memory, RUNTIME + 16, b'\0')
    elif mode in (4, 7):
        if mode == 4:
            write(memory, ENEMY, bytes(1584))
            source = RUNTIME_GROUPS + u32(memory, ACTIVE_GROUP) * 444 + 48
        else:
            source = SAVED_GROUPS + first * 444 + 48
        for index in range(3):
            write(memory, ENEMY + index * 528 + 46, b'\xff\xff')
        destination = ENEMY
        for index in range(3):
            record = source + index * 132
            if u32(memory, record + 20):
                constructor(memory, arm, blobs, destination, record, int(mode == 7))
                if mode == 7:
                    derived(memory, blobs[3], destination)
                destination += 528
        if mode == 4:
            write(memory, RUNTIME + 16, b'\0')
    elif mode == 1:
        for index, value in enumerate(arguments):
            at = ENEMY + index * 528
            write(memory, at + 46, struct.pack('<H', value & 65535))
            write(memory, at + 48, b'\0')
            put(memory, at + 4, 2000 + index)
        for index in range(3):
            at = RUNTIME + 32 + index * 528
            species = struct.unpack('<h', read(memory, at + 46, 2))[0]
            if species >= 0:
                previous = name_model.EKT
                name_model.EKT = EKT
                try:
                    name_model.expected(memory, 'native-builder', at + 182, species, read(memory, at + 48, 1)[0])
                finally:
                    name_model.EKT = previous
        write(memory, RUNTIME + 16, b'\0')
        for index, values in enumerate(((400, 100, 100, 100, 50, 100, 108, 54), (600, 100, 200, 100, 50, 100, 107, 53), (600, 100, 300, 100, 50, 100, 107, 53))):
            at = ENEMY + index * 528
            write(memory, at + 284, struct.pack('<8h', *values))
            write(memory, at + 50, struct.pack('<H', random10(memory)))
            write(memory, at + 170, bytes([random10(memory)]))
        for index in range(3):
            at = ENEMY + index * 528
            species = struct.unpack('<h', read(memory, at + 46, 2))[0]
            if species != -1:
                features, count = feature_model.collect(blobs[0], blobs[1], blobs[2], species, 0, read(memory, BATTLE_SKILLS + index * 10, 10), 256, 256)
                write(memory, at + 74, features)
                if action_model.expected(memory, blobs[1], 'saved_skill_action_filter', BATTLE_SKILLS + index * 10, at + 74, at + 12, 0, True):
                    raise AssertionError('Unexpected action fault in initializer fixture')
                projection_model.expected(memory, arm, 'saved_projection_with_features', species, 0, at + 74, at + 138)

def validate(arm, save, matches, root):
    rom = NintendoDSRom((root / 'inputs/game.nds').read_bytes())
    overlay = rom.loadArm9Overlays()[1]
    images = {'main': (0x02000000, arm), 'ov001': (overlay.ramAddress, bytes(overlay.data))}
    if overlay.ramAddress != 0x021d7240 or sha(overlay.data) != '39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92':
        raise AssertionError('Initializer ov001 image identity differs')
    reused = dependencies(root, images, matches)
    seen = {'native': set(), 'recompiled': set()}
    observed = {0x02067cc4, 0x02067bec, 0x02063f04, 0x020649fc, 0x0203d294, 0x021e9164}

    def entry(machine, address, size, user):
        seen[user].add(address)

    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        for base, image in images.values():
            machine.mem_write(base, image)
        if rebuilt:
            for row, code in [*reused.values(), *matches.values()]:
                machine.mem_write(int(row['address'], 16), code)
        for address in observed:
            machine.hook_add(UC_HOOK_CODE, entry, user_data='recompiled' if rebuilt else 'native', begin=address, end=address)
        machines.append(machine)
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'SkillTbl.bin', 'FeatTbl.bin', 'ItemTbl.bin')}
    blobs = assets['EnmyKindTbl.bin'][8:], assets['SkillTbl.bin'], assets['FeatTbl.bin'], assets['ItemTbl.bin']
    rng = random.Random(20261027)
    vectors = [(mode, pattern, (pattern % 4, 139, -1) if mode == 7 else (0, 139, -1), pattern, pattern & 1, 0) for mode in range(256) for pattern in range(8)]
    vectors += [(1, 7, (species, (species + 1) % 512, -1), species, 0, 0) for species in range(512)]
    vectors += [(7, 7, (species % 4, 0, 0), species, toggle, 0) for species in range(512) for toggle in (0, 255)]
    vectors += [(7, 8, (group, 0, 0), 0, 0, bank) for bank in (0, 0x7100) for group in range(4)]
    vectors += [(mode, 0, arguments, 139, 0, 0) for mode in (0, 2, 8) for arguments in ((-32768, -1, 32767), (0x7fffffff, -0x80000000, 65535), (65536, -65536, 0))]
    cases = calls = 0
    for mode, pattern, arguments, species, toggle, bank in vectors:
        original = {0x020da000: bytearray(arm[0xda000:0xdb000]), 0x020ddd00: bytearray(arm[0xddd00:0xded00]), 0x020f6000: bytearray(rng.randbytes(0x2000)), 0x021b9000: bytearray(rng.randbytes(0xa000)), 0x021c3000: bytearray(rng.randbytes(0x2000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), 0x02238000: bytearray(rng.randbytes(0x1000)), EKT: bytearray(blobs[0] + bytes(0x10000 - len(blobs[0]))), SKILL: bytearray(blobs[1] + bytes(0x4000 - len(blobs[1]))), FEAT: bytearray(blobs[2] + bytes(0x1000 - len(blobs[2]))), POINTERS: bytearray(0x6000), BASE: bytearray(0x4000), SUFFIX: bytearray(0x2000), ITEM: bytearray(blobs[3][8:] + bytes(0x6000 - len(blobs[3][8:])))}
        for begin, end, destination in PARTS:
            write(original, destination, save[bank + begin:bank + end])
        for index in range(100):
            data = bytearray(rng.randbytes(132))
            struct.pack_into('<IhB', data, 20, index + 1, (species + index) % 512, index % 3)
            data[122:132] = bytes([1, 0, 2, 255, 128, 100, 255, 255, 0, 0])
            write(original, RECORDS + index * 132, bytes(data))
        for group in range(4):
            for index in range(3):
                data = bytearray(read(original, RECORDS + index * 132, 132))
                struct.pack_into('<I', data, 20, index + 1 if pattern != 8 and pattern & (1 << index) else 0)
                if pattern != 8:
                    write(original, SAVED_GROUPS + group * 444 + 48 + index * 132, bytes(data))
                if group < 3:
                    write(original, RUNTIME_GROUPS + group * 444 + 48 + index * 132, bytes(data))
        for index in range(3):
            write(original, RUNTIME + 32 + index * 528 + 46, struct.pack('<hB', (species + index) % 512 if index != 2 else -1, index))
            write(original, BATTLE_SKILLS + index * 10, bytes([1, 0, 2, 255, 128, 100, 255, 255, 0, 0]))
        put(original, ACTIVE_GROUP, pattern % 3)
        write(original, MODE, bytes([mode]))
        write(original, bonus_model.TOGGLE, bytes([toggle]))
        put(original, 0x020f69f0, EKT)
        put(original, 0x021c673c, SKILL)
        put(original, 0x021c6740, 256)
        put(original, 0x021c6750, FEAT)
        put(original, 0x021c6754, FEAT + 8)
        put(original, 0x021c2ab4, ITEM)
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
        incoming = [rng.getrandbits(32) for register in SAVED_REGISTERS]
        stack = bytes(0x10000) if mode == 1 else rng.randbytes(0x10000)
        row, code = next(iter(matches.values()))
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED_REGISTERS, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                machine.reg_write(register, value & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=2000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000:
                raise AssertionError(('Initializer execution/stack bounds', mode, pattern, species))
            if [machine.reg_read(register) for register in SAVED_REGISTERS] != incoming:
                raise AssertionError(('Initializer callee-saved register ABI', mode, pattern))
            for address, data in memory.items():
                actual = bytes(machine.mem_read(address, len(data)))
                if actual != data:
                    at = next(index for index, (left, right) in enumerate(zip(actual, data)) if left != right)
                    raise AssertionError(('Initializer source/state/table/overlay-BSS/guard RAM', mode, pattern, species, hex(address + at), actual[at], data[at]))
            calls += 1
        cases += 1
    if any(not observed.issubset(values) for values in seen.values()):
        raise AssertionError(('Initializer source entry coverage absent', seen))
    models = ('mechanics_save_runtime_view_oracle.py', 'mechanics_save_native_name_oracle.py', 'mechanics_save_features_oracle.py', 'mechanics_save_feature_bonus_oracle.py', 'mechanics_save_action_banks_oracle.py', 'mechanics_save_projection_oracle.py')
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 2000000, 'elapsedSecondsLimit': 2, 'returnPcAndStackVerified': True, 'calleeSavedR4ThroughR11Verified': True, 'independentExpectedModeGroupsRngAndRuntimeViews': True, 'platformStubs': {}, 'transitiveQualifiedCallClosureChecked': True, 'patchedDependencyFunctions': len(reused), 'moduleImages': {name: {'base': hex(base), 'sha256': sha(image)} for name, (base, image) in images.items()}, 'explicitOv001Fixture': True, 'requiredSourceEntriesSeen': {key: [hex(address) for address in sorted(values)] for key, values in seen.items()}, 'retainedNativeDependencies': [{'module': 'main', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'role': role} for address, (size, role) in RETAINED.items()], 'stackFixtures': {'mode1': 'zeroed64KiB to bound native name-builder seed padding', 'otherModes': 'randomized64KiB'}, 'expectedModels': [{'source': name, 'sha256': sha((root / name).read_bytes())} for name in models], 'assetSha256': {name: sha(blob) for name, blob in assets.items()}, 'reusedAcceptedSources': [{**{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')}, 'module': module} for (module, address), (row, code) in reused.items()], 'observations': ['Modes0/2/8 sign-extend three supplied halfwords into raw32-bit view tags and clear runtime flag16; modes3/5/6/9..255 preserve state.', 'Mode4 clears the three views and compacts occupied records from the active runtime444-byte group, then clears flag16.', 'Mode7 compacts occupied saved records from section3 RAM021BCE0C+selector*444+48, copies their extra fields and recomputes two derived halfwords, while preserving flag16.', 'Mode1 writes species/variant/IDs2000..2002, updates party names, initializes raw blocks, performs six actual LCG calls and constructs features/actions/projection using qualified ov001 skill pointers.', 'Saved group fixtures cover bank-relative0x5630 plus48-byte prefixes and three132-byte records per444-byte group; captured groups from both banks have zero IDs and synthetic fixtures exercise populated/sparse layouts.'], 'limitations': ['Four SDK memory functions, the unsigned divider and the148-byte name builder remain native ARM; no platform/gameplay provider is substituted.', 'Mode1 fixtures explicitly load ov001 and zero inherited stack padding. Full overlay transitions, arbitrary name-builder stack contents and original text encoding remain unproved.', 'Four444-byte groups fit inside the copied section3 interval through bank0x5D20, but this is not a valid selector-count or group-purpose claim.', 'All categories/species/pointers used for populated projections are bounded fixtures. Complete runtime type definitions, legal game state and gameplay labels remain outstanding.', 'No save partition meaning is promoted and no original ROM/save/table is mutated.']}
