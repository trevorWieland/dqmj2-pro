import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put
import mechanics_save_features_oracle as feature_model
import mechanics_save_action_banks_oracle as action_model
import mechanics_save_projection_oracle as projection_model
import mechanics_save_roster_oracle as roster_model

EKT = 0x02500000
SKILL = 0x02510000
FEAT = 0x02520000
VIEW = 0x02530080
RECORDS = 0x021bd674
STOP = 0x027ff800
RETAINED = {0x02008c14: (20, 'SDK word fill'), 0x02008d78: (148, 'SDK byte fill'), 0x02008e0c: (304, 'SDK byte copy')}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm, matches):
    registry = json.loads((root / 'recovery.json').read_text(encoding='utf-8'))
    paths = [root / batch['report'] for batch in registry['batches']]
    paths.extend(root / ('evidence/matches/mechanics-save-' + suffix + '.json') for suffix in ('roster', 'features', 'action-banks', 'projection'))
    rows = {}
    for path in paths:
        document = json.loads(path.read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Runtime view dependency ROM namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            if row.get('module') in ('main', 'arm9'):
                rows[int(row['address'], 16)] = row
    wanted = {int(relocation['target'], 16) for row, code in matches.values() for relocation in row.get('relocations', []) if relocation['type'] in (1, 28, 29)}
    result = {}
    while wanted:
        address = wanted.pop()
        if address in result or address in RETAINED:
            continue
        if address not in rows:
            raise AssertionError(('Runtime view unresolved direct callee', hex(address)))
        row = rows[address]
        if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
            raise AssertionError('Runtime view dependency source/object hash differs')
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
            raise AssertionError('Runtime view dependency native span differs')
        result[address] = (row, bytes(code))
    return result

def expected(memory, arm, ekt, skills, feat, record, extra):
    if not record:
        write(memory, VIEW + 46, b'\xff\xff')
        return 0
    data = read(memory, record, 132)
    identity, species, variant = struct.unpack_from('<IhB', data, 20)
    put(memory, VIEW + 4, identity)
    write(memory, VIEW + 46, struct.pack('<hB', species, variant))
    count = roster_model.expected(memory, 'saved_roster_species_count', species, variant)
    write(memory, VIEW + 171, bytes([count & 255]))
    count = sum(data[122 + index * 2] != 0 for index in range(5))
    write(memory, VIEW + 172, bytes([count]))
    write(memory, VIEW + 224, data[64:122])
    write(memory, VIEW + 284, data[32:64])
    features, count = feature_model.collect(ekt, skills, feat, species, variant, data[122:132], 256, 256)
    write(memory, VIEW + 74, features)
    fault = action_model.expected(memory, skills, 'saved_skill_action_filter', record + 122, VIEW + 74, VIEW + 12, 0, True)
    if fault:
        raise AssertionError('Runtime view fixture unexpectedly malformed')
    projection_model.expected(memory, arm, 'saved_projection_with_features', species, variant, VIEW + 74, VIEW + 138)
    write(memory, VIEW + 175, data[28:29])
    write(memory, VIEW + 182, data[:20])
    if extra:
        write(memory, VIEW + 214, data[122:132])
        write(memory, VIEW + 178, data[30:31])
        write(memory, VIEW + 177, data[27:28])
    return 1

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
    ekt, skills, feat = assets['EnmyKindTbl.bin'][8:], assets['SkillTbl.bin'], assets['FeatTbl.bin']
    synthetic_skills = bytearray(skills)
    synthetic_feat = bytearray(feat)
    for identity in range(201, 229):
        synthetic_feat[8 + identity * 8] |= 4
    for identity in range(1, 6):
        synthetic_skills[8 + identity * 60:18 + identity * 60] = bytes(10)
        synthetic_skills[58 + identity * 60:68 + identity * 60] = bytes(201 + ((identity - 1) * 10 + index) % 28 for index in range(10))
    rng = random.Random(20261027)
    fixtures = [('synthetic', species, variant, extra, 0) for species in range(512) for variant in (0, 1, 2) for extra in (0, 1)]
    fixtures += [('captured', index, 0, extra, bank) for bank in (0, 0x7100) for index in range(100) for extra in (0, 1)]
    fixtures += [('all-same', species, variant, extra, 0) for species in (0, 139, 353, 500, 511) for variant in (0, 2, 4) for extra in (0, -1)]
    fixtures += [('feature-caps', species, variant, extra, 0) for species in (0, 139, 353, 500, 511) for variant in (0, 1, 2) for extra in (0, 1)]
    fixtures += [('null', 0, 0, extra, 0) for extra in (0, 1, -1)]
    cases = calls = 0
    for label, species, variant, extra, bank in fixtures:
        skill_data = bytes(synthetic_skills) if label == 'feature-caps' else skills
        feat_data = bytes(synthetic_feat) if label == 'feature-caps' else feat
        original = {0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021bd000: bytearray(rng.randbytes(0x5000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), EKT: bytearray(ekt + bytes(0x10000 - len(ekt))), SKILL: bytearray(skill_data + bytes(0x4000 - len(skill_data))), FEAT: bytearray(feat_data + bytes(0x1000 - len(feat_data))), 0x02530000: bytearray(rng.randbytes(0x1000))}
        write(original, 0x021bd51c, save[bank + 0x90:bank + 0x3a68])
        record = RECORDS + species * 132 if label == 'captured' else RECORDS
        if label not in ('captured', 'null'):
            for index in range(100):
                data = bytearray(rng.randbytes(132))
                target_species = species if label == 'all-same' or index == 0 else (species + index) % 512
                struct.pack_into('<IhB', data, 20, 0 if index % 4 == 3 else index + 1, target_species, variant)
                data[122:132] = bytes([1, 255, 2, 255, 3, 255, 4, 255, 5, 255]) if label == 'feature-caps' else bytes([1, 0, 2, 255, 128, 100, 255, 255, 0, 0])
                write(original, RECORDS + index * 132, bytes(data))
        put(original, 0x020f69f0, EKT)
        put(original, 0x021c673c, SKILL)
        put(original, 0x021c6740, 256)
        put(original, 0x021c6750, FEAT)
        put(original, 0x021c6754, FEAT + 8)
        record = 0 if label == 'null' else record
        memory = {address: bytearray(data) for address, data in original.items()}
        result = expected(memory, arm, ekt, skill_data, feat_data, record, extra)
        row, code = next(iter(matches.values()))
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            machine.reg_write(UC_ARM_REG_R0, VIEW)
            machine.reg_write(UC_ARM_REG_R1, record)
            machine.reg_write(UC_ARM_REG_R2, extra & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError(('Runtime view bounds', label, species, variant, extra))
            if machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('Runtime view return', label, species, variant))
            for address, data in memory.items():
                observed = bytes(machine.mem_read(address, len(data)))
                if observed != data:
                    at = next(index for index, (left, right) in enumerate(zip(observed, data)) if left != right)
                    raise AssertionError(('Runtime view/record/table/guard RAM', label, species, variant, extra, hex(address + at), observed[at], data[at]))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedComposedRuntimeViewAndSourceGuards': True, 'platformStubs': {}, 'transitiveDirectCallClosureChecked': True, 'patchedDependencyFunctions': len(reused), 'retainedNativeDependencies': [{'module': 'main', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'role': role} for address, (size, role) in RETAINED.items()], 'assetSha256': {name: sha(blob) for name, blob in assets.items()}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['The constructor combines native ID/species/variant, roster and skill counts,58 raw bytes,32 block bytes, collected features, filtered action bits and adjusted packed-EKT projection into a runtime record.', 'Extra mode adds raw skill pairs and bytes1B/1E; normal mode preserves those destination bytes.', 'Null source returns0 and changes only the destination signed-halfword species marker to-1.', 'All512 species with three variants, every captured record from both banks, variant4 raw wildcard probes, repeated species, feature-cap fixtures, extra flags and whole source/table/destination guards are checked.', 'Every transitive declared direct-call target resolves to verified accepted C or one of three explicitly retained SDK memory primitives.'], 'limitations': ['The three SDK memory helpers execute native ARM; no platform or gameplay provider is substituted.', 'The runtime layout uses raw offsets and technical fields; feature/projection purposes, action legality and full battle/gameplay mechanics remain unresolved.', 'Variant4 projection row crossings are bounded ARM probes; native projection-table extent and legal variants are not asserted.', 'Source/destination overlap and invalid species/pointers are outside this constructor proof.', 'No additional save semantic bytes or original inputs are changed.']}
