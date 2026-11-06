import hashlib
import json
import random
import struct
import time

from project import ROOT
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
from verify_save_protocol import PARTS

PROVIDERS = {}
RETAINED = {0x02008d78: 148, 0x02008e0c: 304, 0x02008c58: 76, 0x02008ca4: 56, 0x020bb234: 64, 0x020bafe8: 68, 0x020bb02c: 32, 0x020bb04c: 32, 0x020bb0e8: 56, 0x020bb210: 36, 0x020baf40: 52, 0x020bb0a0: 72}
RECORDS76 = 0x021bb5b8
RECORDS12 = 0x021bc8b8
IDENTITIES = 0x021bb2b8
SCRATCH = 0x021bcbc0
PROFILE = 0x021bb278
INPUT = 0x02500040
NAME = 0x02500100
OUTPUT = 0x02500200
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
    available.update({int(row['address'], 16): (row, {'romSha256': rom_hash, 'source': 'src/mechanics_save/section3_identity.c', 'sourceSha256': sha((ROOT / 'src/mechanics_save/section3_identity.c').read_bytes())}, None) for row, code in matches.values()})
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

def invoke(machine, address, arguments, incoming):
    for register, value in zip(SAVED, incoming):
        machine.reg_write(register, value)
    for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
        machine.reg_write(register, value & 0xffffffff)
    machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    began = time.monotonic()
    machine.emu_start(address, STOP, count=1000000)
    if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming:
        raise AssertionError(('Identity data bounded return/ABI', hex(address), arguments))
    return machine.reg_read(UC_ARM_REG_R0)

def generate_codes(machine):
    result = {}
    for identity in range(1, 66):
        profile = bytearray(64)
        struct.pack_into('<I', profile, 28, identity)
        machine.mem_write(0x02501000, bytes(profile))
        low = invoke(machine, 0x02097331, (0x02501000,), [0] * 8)
        code = low | (machine.reg_read(UC_ARM_REG_R1) << 32)
        text = f'{code:012d}'.encode()
        if len(text) != 12 or not code:
            raise AssertionError('Identity native synthetic code fixture differs')
        result[identity] = (struct.pack('<III', 0x1000, code & 0xffffffff, code >> 32), text)
    return result

def locate(memory, identity):
    if identity is None:
        return -1
    for index in range(64):
        if read(memory, IDENTITIES + index * 12, 12) == identity:
            return index
    return -1

def add(memory, identity):
    index = locate(memory, identity)
    if index != -1:
        return index
    index = next((index for index in range(64) if not u32(memory, IDENTITIES + index * 12) & 0x1800), -1)
    if index == -1:
        return -1
    if identity is None:
        return -2
    write(memory, IDENTITIES + index * 12, identity)
    return index

def model(memory, name, arguments, identity=None, digits=None):
    if name.endswith('_pointer'):
        return RECORDS76 if 'records76' in name else RECORDS12 if 'records12' in name else SCRATCH
    if name == 'saved_identity_name_write':
        index = add(memory, identity)
        if index >= 0:
            write(memory, RECORDS76 + index * 76, read(memory, arguments[1], 20))
        return index & 0xffffffff
    if name == 'saved_identity_digits_write':
        found = locate(memory, identity)
        if found != -1:
            return found
        index = add(memory, identity)
        if index >= 0:
            output = bytearray()
            for offset, value in enumerate(digits):
                if offset in (4, 8):
                    output.extend(b'\xe1\x43')
                output.append((value - 0x2f) & 255)
            write(memory, RECORDS76 + index * 76, bytes(output) + bytes(20 - len(output)))
        return index & 0xffffffff
    if name == 'saved_identity_remove':
        index = arguments[0]
        if not 0 <= index < 64:
            return 0
        write(memory, RECORDS76 + index * 76, bytes(76))
        write(memory, RECORDS12 + index * 12, bytes(12))
        write(memory, IDENTITIES + index * 12, bytes(12))
        return 1
    if name == 'saved_identity_data_read':
        return 0
    if name == 'saved_identity_scratch_import':
        write(memory, SCRATCH, read(memory, arguments[0], 76))
        return 0
    raise AssertionError(('Unknown section3 identity function', name))

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
    codes = generate_codes(machines[0])
    rng = random.Random(202610277)
    cases = operations = calls = 0
    for bank in (0, 0x7100):
        for pattern in range(4):
            for identity_id in range(1, 66):
                original = {0x021b9000: bytearray(rng.randbytes(0xa000)), 0x021d1000: bytearray(rng.randbytes(0x1000)), 0x02500000: bytearray(rng.randbytes(0x2000))}
                for start, end, address in PARTS:
                    write(original, address, save[bank + start:bank + end])
                write(original, PROFILE, bytes(64))
                put(original, 0x021d1b80, 0)
                for index in range(64):
                    value = None if pattern == 0 else index + 1 if pattern == 1 else index + 1 if pattern == 2 and index % 3 == 0 else 1 if pattern == 3 and index % 2 == 0 else None
                    write(original, IDENTITIES + index * 12, codes[value][0] if value else bytes(12))
                identity, digits = codes[identity_id]
                write(original, INPUT, identity)
                write(original, 0x02500300, digits + b'\0')
                write(original, 0x02500340, b'000000000000\0')
                write(original, 0x02500380, codes[65][0])
                write(original, 0x025003c0, codes[65][1] + b'\0')
                expected = {address: bytearray(data) for address, data in original.items()}
                program = [('saved_identity_records76_pointer', (), None, None), ('saved_identity_records12_pointer', (), None, None), ('saved_identity_scratch76_pointer', (), None, None), ('saved_identity_name_write', (INPUT, NAME), identity, None), ('saved_identity_digits_write', (0x025003c0,), codes[65][0], codes[65][1]), ('saved_identity_digits_write', (0x02500300,), identity, digits), ('saved_identity_name_write', (0, NAME), None, None), ('saved_identity_digits_write', (0x02500340,), None, b'000000000000'), ('saved_identity_data_read', (identity_id - 1, OUTPUT), None, None), ('saved_identity_scratch_import', (NAME,), None, None), ('saved_identity_remove', (identity_id - 1,), None, None)]
                incoming = [rng.getrandbits(32) for register in SAVED]
                stack = rng.randbytes(0x10000)
                for machine in machines:
                    for address, data in original.items():
                        machine.mem_write(address, bytes(data))
                    machine.mem_write(0x027f0000, stack)
                for name, arguments, identity_data, text in program:
                    result = model(expected, name, arguments, identity_data, text)
                    row, code = matches[name]
                    for machine in machines:
                        actual_result = invoke(machine, int(row['address'], 16), arguments, incoming)
                        if actual_result != result:
                            raise AssertionError(('Identity library caller result', name, bank, pattern, identity_id, hex(result), hex(actual_result)))
                        for address, data in expected.items():
                            actual = bytes(machine.mem_read(address, len(data)))
                            if actual != data:
                                mismatch = next(index for index, (a, b) in enumerate(zip(actual, data)) if a != b)
                                raise AssertionError(('Identity library caller complete RAM/guard differs', name, bank, pattern, identity_id, hex(address + mismatch), actual[mismatch], data[mismatch]))
                        calls += 1
                    operations += 1
                cases += 1
    contracts = 0
    for machine in machines:
        state = {'kind': None, 'result': 0, 'seen': 0}
        def hook(uc, address, size, current):
            if address not in (0x020bb234, 0x020bb210) or current['kind'] is None:
                return
            args = [uc.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
            if address == 0x020bb234:
                if args != [current['index'], 76, OUTPUT]:
                    raise AssertionError(('Identity bounded read contract arguments', args))
                uc.mem_write(OUTPUT, current['payload'])
            elif args[:2] != [76, NAME]:
                raise AssertionError(('Identity bounded validation contract arguments', args))
            current['seen'] += 1
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (current['result'], 0xdead0101, 0xdead0202, 0xdead0303)):
                uc.reg_write(register, value)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        handle = machine.hook_add(UC_HOOK_CODE, hook, state)
        machine.ctl_remove_cache(0x02000000, 0x02100000)
        for index in (-2147483648, -1, 0, 1, 63, 64, 2147483647):
            for value in (0, 1):
                payload = rng.randbytes(76)
                machine.mem_write(OUTPUT, bytes([0x6b]) * 0x100)
                incoming = [rng.getrandbits(32) for register in SAVED]
                state.update({'kind': 'read', 'result': value, 'index': index, 'payload': payload, 'seen': 0})
                result = invoke(machine, int(matches['saved_identity_data_read'][0]['address'], 16), (index, OUTPUT), incoming)
                valid = 0 <= index < 64
                if result != (value if valid else 0) or state['seen'] != int(valid) or bytes(machine.mem_read(OUTPUT, 76)) != (payload if valid else bytes([0x6b]) * 76):
                    raise AssertionError(('Identity bounded data-read caller contract', index, value, result, state['seen'], bytes(machine.mem_read(OUTPUT, 76)).hex(), payload.hex()))
                contracts += 1
        for value in (0, 1):
            payload = rng.randbytes(76)
            machine.mem_write(NAME, payload)
            state.update({'kind': 'validate', 'result': value, 'seen': 0})
            result = invoke(machine, int(matches['saved_identity_scratch_import'][0]['address'], 16), (NAME,), [0] * 8)
            if result != value or state['seen'] != 1 or bytes(machine.mem_read(SCRATCH, 76)) != payload:
                raise AssertionError('Identity bounded scratch-import validation contract')
            contracts += 1
        machine.hook_del(handle)
    retained = [{'module': 'main', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])} for address, size in RETAINED.items()]
    thumb = [(0x02096ed0, 18), (0x02096f50, 102), (0x02097198, 18), (0x02097330, 28), (0x0209734c, 36), (0x020973d8, 150), (0x0209cc88, 16), (0x0209ccf4, 88), (0x0209cd4c, 96)]
    return {'engine': 'Unicorn', 'cases': cases, 'operations': operations, 'nativeAndRecompiledCalls': calls, 'additionalBoundedCallerContractCalls': contracts, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'randomizedInitialStack': True, 'independentSequentialLookupInsertionNameFormattingDeletionModel': True, 'sourcePatchedFunctions': len(functions), 'platformStubs': {}, 'actualLibraryProtocolProviders': {}, 'boundedLibraryContracts': {'0x020bb234': 'Additional caller-only query0/1 outcomes and76-byte writes; actual SDK success data service remains outside scope.', '0x020bb210': 'Additional caller-only validation0/1 outcomes after actual scratch copy; actual SDK online validation remains outside scope.'}, 'offlineSdkControl': {'module': 'main', 'address': '0x021d1b80', 'value': 0}, 'syntheticIdentityCodes': {'nativeGenerator': {'module': 'main', 'mode': 'Thumb', 'address': '0x02097330', 'bytes': 28}, 'count': len(codes), 'fixtureSha256': sha(b''.join(record + text for record, text in codes.values())), 'profile': '64 private bytes zero except word0x1C set1..65; no original profile changed'}, 'retainedNativeEntries': retained + [{'module': 'main', 'mode': 'Thumb', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])} for address, size in thumb], 'reusedAcceptedSources': [{key: value for key, value in function.items() if key != 'code'} for function in functions.values() if function['report']], 'observations': ['Raw12-byte identity lookup/insertion executes the retained ARM/Thumb library with valid synthetic native-generated decimal codes; empty/full/sparse/duplicate64-slot layouts and both copied banks are covered.', 'Name write replaces the first20 bytes of a found or newly inserted76-byte record; existing entries retain their indices, full arrays return-1 and rejected null/zero-code inputs return-2 when a free slot exists.', 'New12-digit strings format into20 bytes by subtracting0x2F from each signed input byte and inserting E143 before positions4/8; existing identities return before rewriting the name.', 'Removal validates0..63, calls the native library then clears the corresponding76-byte and12-byte saved records.', 'The scratch importer copies76 bytes before validating; data queries and validation return0 with the explicitly offline SDK word, with separate bounded0/1 caller contracts.'], 'limitations': ['SDK identity/string/data routines and listed memory primitives remain native; retained entry spans are qualified ARM/Thumb and transitive code is pinned by the complete ARM9 hash.', 'Synthetic code generation exercises native checksum/creation routines but is not an independent proof of the SDK checksum algorithm.', 'Positive data-query/online-validation outcomes are controlled caller contracts, not complete SDK service/network behavior.', 'Working identity/record names and formatting establish no decoded people, friend-code legality, online functionality or semantic-partition promotion.']}

