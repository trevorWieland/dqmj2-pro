import hashlib
import json
import random
import struct
import time

from project import ROOT
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
from mechanics_save_runtime_commit_oracle import expected as commit, RUNTIME, PARTY, RESERVE, RECORDS
from mechanics_save_derived_refresh_oracle import refresh
from verify_save_protocol import PARTS

PROVIDERS = {}
RETAINED = {0x02008d78: 148}
CONTEXT = 0x02102dc0
STATE = 0x020f6054
STOP = 0x027ff800
OUTPUT = 0x02570040
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(arm, rom_hash, matches):
    available = {}
    for batch in json.loads((ROOT / 'recovery.json').read_text(encoding='utf-8'))['batches']:
        path = ROOT / batch['report']
        document = json.loads(path.read_text(encoding='utf-8'))
        for row in document.get('matches', document.get('functionMatches', [])):
            if row.get('module', 'main') in ('main', 'arm9') and row.get('exactAfterDeclaredRelocation', row.get('exactBytes', False)):
                available[int(row['address'], 16)] = (row, document, batch['report'])
    available.update({int(row['address'], 16): (row, {'romSha256': rom_hash, 'source': 'src/mechanics_save/world_transition.c', 'sourceSha256': sha((ROOT / 'src/mechanics_save/world_transition.c').read_bytes())}, None) for row, code in matches.values()})
    pending = [int(row['address'], 16) for row, code in matches.values()]
    result = {}
    missing = set()
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    while pending:
        address = pending.pop()
        if address in result or address in PROVIDERS or address in RETAINED:
            continue
        if address not in available:
            missing.add(address)
            continue
        row, document, report = available[address]
        if document['romSha256'] != rom_hash:
            raise AssertionError('Runtime serialization ROM namespace differs')
        source = row.get('source') or document['source']
        source_hash = row.get('sourceSha256') or document['sourceSha256']
        if sha((ROOT / source).read_bytes()) != source_hash or sha((ROOT / row['object']).read_bytes()) != row['objectSha256']:
            raise AssertionError(('Runtime serialization source/object identity differs', source))
        with (ROOT / row['object']).open('rb') as stream:
            elf = ELFFile(stream)
            symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
            code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
        for relocation in row.get('relocations', []):
            at = relocation['offset']
            target = int(relocation['target'], 16) + relocation['addend']
            previous = struct.unpack_from('<I', code, at)[0]
            if relocation['type'] == 2:
                value = target
            elif relocation['type'] in (1, 28, 29):
                value = (previous & 0xff000000) | (((target - address - at) >> 2) & 0xffffff)
            else:
                raise AssertionError('Runtime serialization unsupported relocation')
            struct.pack_into('<I', code, at, value & 0xffffffff)
        size = row.get('bytes', row.get('size'))
        if code != arm[address - 0x02000000:address - 0x02000000 + size]:
            raise AssertionError(('Runtime serialization source span differs', row['name']))
        result[address] = {'name': row['name'], 'address': hex(address), 'bytes': size, 'source': source, 'sourceSha256': source_hash, 'object': row['object'], 'objectSha256': row['objectSha256'], 'report': report, 'code': bytes(code)}
        for relocation in row.get('relocations', []):
            target = int(relocation['target'], 16) + relocation['addend']
            if target in available and target != address:
                pending.append(target)
        for instruction in decoder.disasm(code, address):
            if instruction.mnemonic in ('b', 'bl') and instruction.op_str.startswith('#0x'):
                target = int(instruction.op_str[1:], 16)
                if not address <= target < address + size:
                    pending.append(target)
    if missing:
        raise AssertionError(('Runtime serialization missing source dependencies', [hex(value) for value in sorted(missing)]))
    return result

def signed_byte(value):
    return value - 256 if value & 128 else value

def model(memory, name, argument, blobs, present):
    result = None
    if name in ('saved_world_marker_exchange', 'saved_world_route_exchange'):
        address = CONTEXT + (5 if 'marker' in name else 1)
        result = signed_byte(read(memory, address, 1)[0]) & 0xffffffff
        write(memory, address, bytes([argument & 255]))
    elif name in ('saved_world_marker_get', 'saved_world_route_get'):
        result = signed_byte(read(memory, CONTEXT + (5 if 'marker' in name else 1), 1)[0]) & 0xffffffff
    elif name == 'saved_world_kind_set':
        write(memory, CONTEXT, bytes([argument & 255]))
    elif name == 'saved_world_kind_get':
        result = read(memory, CONTEXT, 1)[0]
    elif name == 'saved_world_position_set':
        write(memory, CONTEXT + 36, read(memory, argument, 12))
    elif name == 'saved_world_position_get':
        if argument:
            write(memory, argument, read(memory, CONTEXT + 36, 12))
        result = CONTEXT + 36
    elif name in ('saved_world_heading_get', 'saved_world_clock_get'):
        address = CONTEXT + (12 if 'heading' in name else 24)
        if argument:
            put(memory, argument, u32(memory, address))
        result = u32(memory, address)
    elif name == 'saved_world_transition_apply':
        kind = read(memory, CONTEXT, 1)[0]
        previous = read(memory, CONTEXT + 2, 1)
        if kind in (1, 10, 11):
            write(memory, STATE + 12, previous)
            write(memory, STATE + 4, b'\0')
            write(memory, CONTEXT + 5, b'\xff')
            if kind == 11:
                write(memory, STATE + 1, b'\1')
            if kind == 1 and u32(memory, 0x020edce0) == 2:
                commit(memory, 'saved_runtime_blocks_commit', (), 0)
                count = struct.unpack('<H', read(memory, RUNTIME + 22, 2))[0]
                write(memory, CONTEXT + 90, struct.pack('<H', (count + 1) & 65535))
                if not read(memory, RUNTIME + 10, 1)[0]:
                    count = struct.unpack('<H', read(memory, 0x021bd668, 2))[0]
                    write(memory, 0x021bd668, struct.pack('<H', min((count + 1) & 65535, 9999)))
        elif kind == 3:
            if read(memory, CONTEXT + 0x5f, 1)[0] == 1:
                write(memory, STATE + 12, previous)
                write(memory, STATE + 4, b'\0')
                write(memory, CONTEXT + 5, b'\xff')
            else:
                write(memory, STATE + 12, read(memory, 0x021c0dc8 + 14, 1))
                write(memory, STATE + 4, b'\3')
                write(memory, CONTEXT + 5, b'\xfe')
            commit(memory, 'saved_runtime_blocks_commit', (), 0)
            for group in (0x021bd540, 0x021bd54c):
                for index in range(3):
                    refresh(memory, u32(memory, group + index * 4), blobs, present)
            if not read(memory, CONTEXT + 0x60, 1)[0]:
                gold = u32(memory, 0x021bd538)
                gold = gold - 0x100000000 if gold & 0x80000000 else gold
                put(memory, 0x021bd538, max(0, min(gold >> 1, 999999)))
        elif kind == 4:
            world = 0x021b9eb4
            write(memory, STATE + 12, read(memory, world, 1))
            write(memory, STATE + 4, b'\4')
            write(memory, CONTEXT + 5, b'\xff')
            write(memory, CONTEXT + 2, read(memory, world, 1))
            write(memory, CONTEXT + 36, read(memory, world + 8, 12))
            put(memory, CONTEXT + 12, u32(memory, world + 20))
            put(memory, CONTEXT + 24, (u32(memory, world + 20) + 0xb4000) & 0xffffffff)
        elif kind in (5, 7, 8):
            write(memory, STATE + 12, previous)
            write(memory, STATE + 4, b'\0')
        else:
            write(memory, STATE + 4, read(memory, CONTEXT + 1, 1))
    else:
        raise AssertionError(('Unknown world transition function', name))
    return result

def fixture(save, bank, kind, scenario, species, blobs, rng):
    ekt, skills, feat, items = blobs
    memory = {0x020ddd00: bytearray(rng.randbytes(0x100)), 0x020edc00: bytearray(rng.randbytes(0x1000)), 0x020f6000: bytearray(rng.randbytes(0x2000)), 0x02102d00: bytearray(rng.randbytes(0x1000)), 0x021b9000: bytearray(rng.randbytes(0xa000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), 0x02500000: bytearray(ekt + bytes(0x10000 - len(ekt))), 0x02510000: bytearray(skills + bytes(0x4000 - len(skills))), 0x02520000: bytearray(feat + bytes(0x1000 - len(feat))), 0x02530000: bytearray(items[8:] + bytes(0x6000 - len(items[8:]))), OUTPUT - 0x40: bytearray(rng.randbytes(0x100))}
    for start, end, address in PARTS:
        write(memory, address, save[bank + start:bank + end])
    write(memory, RECORDS, bytes(13200))
    for index in range(6):
        record = bytearray(rng.randbytes(132))
        struct.pack_into('<IhB', record, 20, index + 1, species, scenario % 3)
        record[122:132] = bytes([1, 0, 2, 255, 128, 100, 255, 255, 0, 0])
        write(memory, RECORDS + index * 132, bytes(record))
    ids = [1, 2, 3, 4, 5, 6] if scenario == 0 else [1] * 6 if scenario == 1 else [0] * 6 if scenario == 2 else [1, 0, 0xffffffff, 3, 1, 2]
    write(memory, 0x021bd540, struct.pack('<III', *ids[:3]))
    write(memory, 0x021bd54c, struct.pack('<III', *ids[3:]))
    for ordinal, identity in enumerate(ids):
        view = (PARTY if ordinal < 3 else RESERVE) + (ordinal % 3) * 528
        put(memory, view + 4, identity)
        write(memory, view + 284, rng.randbytes(32))
    put(memory, RUNTIME, (0, 1999999, 0x80000000, 0xffffffff)[scenario])
    write(memory, CONTEXT, bytes([kind]))
    write(memory, CONTEXT + 0x5f, bytes([scenario & 1]))
    write(memory, CONTEXT + 0x60, bytes([scenario >> 1]))
    put(memory, 0x020edce0, (2, 1, 2, 3)[scenario])
    put(memory, 0x020f69f0, 0x02500000)
    put(memory, 0x021c673c, 0 if scenario == 3 else 0x02510000)
    put(memory, 0x021c6740, 256)
    put(memory, 0x021c6750, 0x02520000)
    put(memory, 0x021c6754, 0x02520008)
    put(memory, 0x021c2ab4, 0x02530000)
    write(memory, 0x020ddd40, bytes([scenario & 1]))
    write(memory, RUNTIME + 10, bytes([scenario >> 1]))
    write(memory, RUNTIME + 22, struct.pack('<H', (0, 9999, 65535, 0x8000)[scenario]))
    write(memory, 0x021bd668, struct.pack('<H', (0, 9998, 9999, 65535)[scenario]))
    return memory

def validate(arm, save, matches, root):
    rom_hash = sha((root / 'inputs/game.nds').read_bytes())
    functions = dependencies(arm, rom_hash, matches)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for address, function in functions.items():
                machine.mem_write(address, function['code'])
        machines.append(machine)
    rom = NintendoDSRom((root / 'inputs/game.nds').read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'SkillTbl.bin', 'FeatTbl.bin', 'ItemTbl.bin')}
    blobs = (assets['EnmyKindTbl.bin'][8:], assets['SkillTbl.bin'], assets['FeatTbl.bin'], assets['ItemTbl.bin'])
    rng = random.Random(202610273)
    vectors = [('saved_world_transition_apply', 0, bank, kind, scenario, kind % 512) for bank in (0, 0x7100) for kind in range(256) for scenario in range(4)]
    vectors += [('saved_world_transition_apply', 0, 0, 3, scenario, species) for species in range(512) for scenario in (0, 3)]
    for name in matches:
        if name == 'saved_world_transition_apply':
            continue
        args = (OUTPUT, CONTEXT + 12, CONTEXT + 24, CONTEXT + 36, 0) if 'get' in name and ('position' in name or 'heading' in name or 'clock' in name) else (OUTPUT, CONTEXT + 12, CONTEXT + 24, CONTEXT + 36) if name == 'saved_world_position_set' else (0, 1, 127, 128, 255, 256, -1, -257, -2147483648, 2147483647)
        vectors.extend((name, argument, bank, old, old % 4, old) for argument in args for bank in (0, 0x7100) for old in (0, 1, 127, 128, 255))
    cases = calls = 0
    for name, argument, bank, kind, scenario, species in vectors:
        if name == 'saved_world_position_set' and not argument:
            continue
        original = fixture(save, bank, kind, scenario, species, blobs, rng)
        write(original, CONTEXT + 1, bytes([kind]))
        write(original, CONTEXT + 5, bytes([kind]))
        memory = {address: bytearray(data) for address, data in original.items()}
        result = model(memory, name, argument, blobs, scenario != 3)
        row, code = matches[name]
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_R0, argument & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming:
                raise AssertionError(('World transition bounded return/ABI', name, kind, scenario))
            if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('World context return', name, argument, kind, result, machine.reg_read(UC_ARM_REG_R0)))
            for address, data in memory.items():
                actual = bytes(machine.mem_read(address, len(data)))
                if actual != data:
                    mismatch = next(index for index, (a, b) in enumerate(zip(actual, data)) if a != b)
                    raise AssertionError(('World context/transition RAM/table/guard differs', name, argument, kind, scenario, species, hex(address + mismatch), actual[mismatch], data[mismatch]))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'randomizedInitialStack': True, 'independentCompleteStateModel': True, 'platformStubs': {}, 'sourcePatchedFunctions': len(functions), 'reusedAcceptedSources': [{key: value for key, value in function.items() if key != 'code'} for function in functions.values() if function['report']], 'retainedNative': [{'module': 'main', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])} for address, size in RETAINED.items()], 'assetSha256': {name: sha(data) for name, data in assets.items()}, 'observations': ['Kind1 commits runtime blocks and updates counters only when the native SDK type word is2; kind3 commits and recomputes party/reserve halfwords before conditionally halving the purse.', 'Kind4 restores map, previous map,12-byte position and heading from section2 and sets the runtime clock to heading+0xB4000 with32-bit wrap.', 'Kinds10/11 set mode0 and marker-1, with11 also setting raw state byte1; kinds5/7/8 preserve the marker, while other kinds copy the raw signed route byte into mode.', 'The ten context helpers preserve signed byte returns, truncate writes, copy12-byte positions and support optional or aliased outputs.', 'All256 kind bytes, every native species in kind3, both copied banks, duplicate/absent group IDs, item toggle/absent SkillTbl and full state/table guards are covered.'], 'limitations': ['The148-byte SDK fill remains retained native ARM; no gameplay or platform provider is substituted.', 'Kind values, raw state bytes, marker meaning and clock units are observations without complete scene or save semantics.', 'Aliased position/output fixtures establish bounded ARM effects rather than a portable overlapping-struct-assignment contract.', 'This transition does not itself write a physical save or establish bank chronology.']}

