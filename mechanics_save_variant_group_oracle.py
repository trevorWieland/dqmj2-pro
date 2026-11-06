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
    available.update({int(row['address'], 16): (row, {'romSha256': rom_hash, 'source': 'src/mechanics_save/variant_group.c', 'sourceSha256': sha((ROOT / 'src/mechanics_save/variant_group.c').read_bytes())}, None) for row, code in matches.values()})
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
    table = kind_file[8:]
    if len(table) != 51200:
        raise AssertionError('Variant measured kind table extent differs')
    rng = random.Random(202610276)
    vectors = [('saved_variant_group', species, variant, None) for species in range(512) for variant in (-32768, -1, 0, 1, 2, 3, 4, 5, 127, 255, 256, 32767)]
    vectors += [('saved_variant_group', group, variant, group) for group in range(16) for variant in range(256)]
    vectors += [('saved_kind_byte0d', species, previous, None) for species in range(512) for previous in (-32768, -1, 0, 255, 32767)]
    cases = calls = 0
    for name, species, argument, synthetic_group in vectors:
        data = bytearray(table)
        if synthetic_group is not None:
            flags = struct.unpack_from('<H', data, species * 100 + 4)[0]
            struct.pack_into('<H', data, species * 100 + 4, (flags & 0xfff0) | synthetic_group)
        state = bytearray(rng.randbytes(0x1000))
        struct.pack_into('<I', state, 0xf0, TABLE)
        table_guard = b'\x43' * 0x100 + bytes(data) + b'\xa7' * 0x100
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        if name == 'saved_variant_group':
            group = struct.unpack_from('<H', data, species * 100 + 4)[0] & 15
            result = (group + argument * 3) & 255
            if argument > 0:
                quotient = int((result - 1) / 3)
                result = (quotient * 3 + 1) & 255
        else:
            result = data[species * 100 + 13]
        row, code = matches[name]
        for machine in machines:
            machine.mem_write(0x020f6900, bytes(state))
            machine.mem_write(TABLE - 0x100, table_guard)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_R0, species)
            machine.reg_write(UC_ARM_REG_R1, argument & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=10000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming:
                raise AssertionError(('Variant group bounded return/ABI', name, species, argument))
            if machine.reg_read(UC_ARM_REG_R0) != result:
                raise AssertionError(('Variant group/column result', name, species, argument, synthetic_group, result, machine.reg_read(UC_ARM_REG_R0)))
            if bytes(machine.mem_read(0x020f6900, 0x1000)) != state or bytes(machine.mem_read(TABLE - 0x100, len(table_guard))) != table_guard:
                raise AssertionError(('Variant group state/table/guards changed', name, species, argument))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 10000, 'elapsedSecondsLimit': 2, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'randomizedInitialStack': True, 'independentLowNibbleTruncationSignedDivisionAndColumnModel': True, 'platformStubs': {}, 'retainedNative': [], 'sourcePatchedFunctions': len(functions), 'assetSha256': {'EnmyKindTbl.bin': sha(kind_file)}, 'reusedAcceptedSources': [{key: value for key, value in function.items() if key != 'code'} for function in functions.values() if function['report']], 'observations': ['The group projection adds3*variant to the low4-bit native row field and truncates to a byte; nonpositive variants return that byte.', 'Positive variants map the truncated byte through signed truncating division: ((byte-1)/3)*3+1, then truncate again; byte0 consequently maps to1.', 'The second reader returns raw row byte0x0D after a cancelling ADD/SUB of its second argument.', 'All512 native rows, all16 synthetic low-nibble values with all256 variant bytes, negative/boundary variants and safe signed cancellation arguments are covered.'], 'limitations': ['These native table projections do not establish complete variant legality, grouping labels or stat meanings.', 'Variant inputs stay within-32768..32767 to avoid ordinary C signed multiplication overflow; species indices remain within the measured512 rows.', 'No native helper or provider is substituted, and no original assets or semantic partition are changed.']}

