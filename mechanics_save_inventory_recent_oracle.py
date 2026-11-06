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
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
from verify_save_protocol import PARTS

PROVIDERS = {}
RETAINED = {0x02008d78: 148, 0x02008e0c: 304, 0x02063a0c: 104}
BITS = 0x021c0c44
QUEUES = 0x021c0c64
BUFFER = 0x021bd524
ITEM = 0x02500000
INPUT = 0x02570040
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
    available.update({int(row['address'], 16): (row, {'romSha256': rom_hash, 'source': 'src/mechanics_save/inventory_recent.c', 'sourceSha256': sha((ROOT / 'src/mechanics_save/inventory_recent.c').read_bytes())}, None) for row, code in matches.values()})
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

def compact(memory, family):
    address = QUEUES + family * 12
    original = read(memory, address, 10)
    values = bytes(value for value in original if value)
    write(memory, address, values)
    if len(values) < 10:
        write(memory, address + len(values), b'\0')
    return len(values)

def insert(memory, item):
    family = int(read(memory, ITEM + item * 88 + 44, 1)[0] == 7)
    if not item:
        return 0
    address = QUEUES + family * 12
    original = read(memory, address, 10)
    write(memory, address, bytes(10))
    values = bytes([item & 255]) + bytes(value for value in original[:9] if value)
    write(memory, address, values)
    return compact(memory, family)

def model(memory, name, argument):
    if name in ('saved_item_observed_get', 'saved_item_observed_set'):
        address = BITS + (argument >> 5) * 4
        word = u32(memory, address)
        previous = (word >> (argument & 31)) & 1
        if name.endswith('_set') and not previous:
            insert(memory, argument)
            put(memory, address, word | (1 << (argument & 31)))
        return previous
    if name == 'saved_item_recent_insert':
        return insert(memory, argument)
    if name == 'saved_item_recent_remove':
        if not argument:
            return 0
        family = int(read(memory, ITEM + argument * 88 + 44, 1)[0] == 7)
        address = QUEUES + family * 12
        index = next((index for index, value in enumerate(read(memory, address, 10)) if value == argument), None)
        if index is None:
            return 0
        write(memory, address + index, b'\0')
        return compact(memory, family)
    if name == 'saved_item_buffer_get':
        return BUFFER
    if name == 'saved_item_buffer_set':
        write(memory, BUFFER, bytes(20))
        write(memory, BUFFER, read(memory, argument, 20))
        return None
    raise AssertionError(('Unknown inventory recent operation', name))

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
    item_file = bytes(NintendoDSRom((root / 'inputs/game.nds').read_bytes()).getFileByName('ItemTbl.bin'))
    rng = random.Random(202610274)
    vectors = [(item, bank, pattern, None) for item in range(256) for bank in (0, 0x7100) for pattern in range(6)]
    vectors += [(128, bank, 5, family) for bank in (0, 0x7100) for family in range(256)]
    cases = operations = calls = 0
    for item, bank, pattern, kind in vectors:
        original = {0x021b9000: bytearray(rng.randbytes(0xa000)), ITEM: bytearray(item_file[8:] + bytes(0x6000 - len(item_file[8:]))), INPUT - 0x40: bytearray(rng.randbytes(0x100))}
        for start, end, address in PARTS:
            write(original, address, save[bank + start:bank + end])
        put(original, 0x021c2ab4, ITEM)
        if kind is not None:
            write(original, ITEM + item * 88 + 44, bytes([kind]))
        write(original, BITS, bytes([255 if pattern & 1 else 0]) * 32)
        queue = bytes(10) if pattern == 0 else bytes(range(1, 11)) if pattern == 1 else bytes([item]) * 10 if pattern == 2 else bytes([item, 0, 2, 0, 3, 0, 4, 0, item, 0]) if pattern == 3 else bytes([0] * 9 + [item]) if pattern == 4 else bytes(rng.randrange(256) if index % 3 else 0 for index in range(10))
        for family in range(2):
            write(original, QUEUES + family * 12, queue)
        program = [('saved_item_observed_get', item), ('saved_item_observed_set', item), ('saved_item_observed_set', item), ('saved_item_recent_insert', item), ('saved_item_recent_remove', item), ('saved_item_recent_remove', item), ('saved_item_buffer_set', INPUT), ('saved_item_buffer_get', 0), ('saved_item_buffer_set', BUFFER), ('saved_item_buffer_set', BUFFER + 20)]
        expected = {address: bytearray(data) for address, data in original.items()}
        stack = rng.randbytes(0x10000)
        incoming = [rng.getrandbits(32) for register in SAVED]
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            machine.mem_write(0x027f0000, stack)
        for name, argument in program:
            result = model(expected, name, argument)
            row, code = matches[name]
            for machine in machines:
                for register, value in zip(SAVED, incoming):
                    machine.reg_write(register, value)
                machine.reg_write(UC_ARM_REG_R0, argument)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=50000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming:
                    raise AssertionError(('Recent inventory bounded return/ABI', name, item, pattern, kind))
                if result is not None and machine.reg_read(UC_ARM_REG_R0) != result:
                    raise AssertionError(('Recent inventory result', name, item, pattern, kind, result, machine.reg_read(UC_ARM_REG_R0)))
                for address, data in expected.items():
                    actual = bytes(machine.mem_read(address, len(data)))
                    if actual != data:
                        mismatch = next(index for index, (a, b) in enumerate(zip(actual, data)) if a != b)
                        raise AssertionError(('Recent inventory complete state/table/guard differs', name, item, pattern, kind, hex(address + mismatch), actual[mismatch], data[mismatch]))
                calls += 1
            operations += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'operations': operations, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 50000, 'elapsedSecondsLimit': 2, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'randomizedInitialStack': True, 'independentSequentialFlagQueueAndBufferModel': True, 'platformStubs': {}, 'sourcePatchedFunctions': len(functions), 'assetSha256': {'ItemTbl.bin': sha(item_file)}, 'reusedAcceptedSources': [{key: value for key, value in function.items() if key != 'code'} for function in functions.values() if function['report']], 'retainedNative': [{'module': 'main', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])} for address, size in RETAINED.items()], 'observations': ['The observation bit setter returns its previous bit and prepends to a recent-ID queue only on the first transition; ID0 sets bit0 without queue insertion.', 'ItemTbl raw byte0x2C equal to7 selects the second queue; every other byte selects the first.', 'Each queue uses ten active bytes with a12-byte stride; direct insertion prepends a nonzero byte and retains nonzero bytes from the first nine prior positions without deduplicating.', 'Removal clears the first matching byte and compacts nonzero bytes, then clears only the first new terminator; stale bytes beyond it remain native observable state.', 'The20-byte saved buffer is cleared before source copying, so copying from itself leaves it zero.', 'All256 native item IDs, all256 synthetic metadata byte values, both copied banks, duplicates/sparse/full queues and ten sequential operations per fixture are covered.'], 'limitations': ['SDK fill148 B, byte copy304 B and the104-byte recent-ID finder remain native ARM; the finder draft is98/104 bytes and receives no source credit.', 'Raw observation bits and queues provide native ID/consumer evidence without legal inventory, ordering-purpose or semantic-partition claims.', 'No original bank/table/input changes or physical save writes occur.']}

