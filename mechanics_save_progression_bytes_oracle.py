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

PROVIDERS = {}
RETAINED = {}
TABLE = 0x02500000
STOP = 0x027ff800
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
    available.update({int(row['address'], 16): (row, {'romSha256': rom_hash, 'source': 'src/mechanics_save/progression_bytes.c', 'sourceSha256': sha((ROOT / 'src/mechanics_save/progression_bytes.c').read_bytes())}, None) for row, code in matches.values()})
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

def validate(arm, save, matches, root):
    functions = dependencies(arm, sha((root / 'inputs/game.nds').read_bytes()), matches)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for address, function in functions.items():
                machine.mem_write(address, function['code'])
        machines.append(machine)
    kind_file = bytes(NintendoDSRom((root / 'inputs/game.nds').read_bytes()).getFileByName('EnmyKindTbl.bin'))
    actual = kind_file[8:]
    if len(actual) != 51200:
        raise AssertionError('Measured native kind table extent differs')
    rng = random.Random(202610275)
    synthetic = bytearray(actual)
    for species in (0, 139, 353, 511):
        for offset in (0x47, 0x4b, 0x4f, 0x53, 0x57, 0x5b):
            for bucket in range(4):
                synthetic[species * 100 + offset + bucket] = (species + offset * 17 + bucket * 31) & 255
    fixtures = [(species, level, previous, False) for species in range(512) for level in (10, 40, 50, 51) for previous in (0, 255)]
    boundaries = (-2147483648, -1, 0, 1, 9, 10, 11, 39, 40, 41, 49, 50, 51, 100, 2147483647)
    fixtures += [(species, level, previous, synthetic_case) for species in (0, 139, 353, 511) for level in boundaries for previous in (-32768, -255, -1, 1, 127, 32767) for synthetic_case in (False, True)]
    cases = calls = 0
    for species, level, previous, synthetic_case in fixtures:
        table = bytes(synthetic) if synthetic_case else actual
        state = bytearray(rng.randbytes(0x1000))
        struct.pack_into('<I', state, 0xf0, TABLE)
        table_guard = b'\x65' * 0x100 + table + b'\xc9' * 0x100
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        for machine in machines:
            machine.mem_write(0x020f6900, bytes(state))
            machine.mem_write(TABLE - 0x100, table_guard)
            machine.mem_write(0x027f0000, stack)
        bucket = 0 if level <= 10 else 1 if level <= 40 else 2 if level <= 50 else 3
        for name, (row, code) in matches.items():
            offset = int(name[-2:], 16)
            result = table[species * 100 + offset + bucket]
            for machine in machines:
                for register, value in zip(SAVED, incoming):
                    machine.reg_write(register, value)
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), (species, previous, level)):
                    machine.reg_write(register, value & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=10000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming:
                    raise AssertionError(('Progression byte bounded return/ABI', name, species, level))
                if machine.reg_read(UC_ARM_REG_R0) != result:
                    raise AssertionError(('Progression byte table/bucket/cancellation', name, species, previous, level, result, machine.reg_read(UC_ARM_REG_R0)))
                if bytes(machine.mem_read(0x020f6900, 0x1000)) != state or bytes(machine.mem_read(TABLE - 0x100, len(table_guard))) != table_guard:
                    raise AssertionError(('Progression byte state/table/guards changed', name, species, level))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 10000, 'elapsedSecondsLimit': 2, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'randomizedInitialStack': True, 'independentTableAndSignedBucketModel': True, 'platformStubs': {}, 'retainedNative': [], 'sourcePatchedFunctions': len(functions), 'assetSha256': {'EnmyKindTbl.bin': sha(kind_file)}, 'reusedAcceptedSources': [{key: value for key, value in function.items() if key != 'code'} for function in functions.values() if function['report']], 'observations': ['The signed third argument maps to four bucket offsets: <=10,11..40,41..50,>=51.', 'Six functions read one byte from native100-byte species rows at starts0x47/0x4B/0x4F/0x53/0x57/0x5B plus that bucket.', 'Native ADD then SUB of the second argument cancel before unsigned-byte return; bounded signed second arguments leave the table result unchanged.', 'Every512 native species, all bucket thresholds, signed-level extremes, synthetic distinct bytes, table guards and randomized incoming ABI state are checked.'], 'limitations': ['Raw column and bucket observations establish no complete stat growth, XP curve, progression formula or gameplay labels.', 'Species indices are restricted to0..511 in the measured table; unchecked native index arithmetic does not prove other values legal.', 'Second arguments stay within-32768..32767 so the tested ordinary C additions avoid signed overflow.']}

