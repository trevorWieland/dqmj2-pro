import hashlib
import json
import struct
import time

from project import ROOT
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
import mechanics_save_section3_identity_oracle as caller_model

PROVIDERS = {}
THUMB_RETAINED = {0x02096ed0: 18, 0x02096f50: 102, 0x02097198: 18, 0x02097330: 28, 0x0209734c: 36, 0x020973d8: 150, 0x0209cc88: 16, 0x0209ccf4: 88, 0x0209cd4c: 96}
RETAINED = {0x02008d78: 148, 0x02008e0c: 304, 0x02008c58: 76, 0x02008ca4: 56, **THUMB_RETAINED}
CALLER_REPORTS = ('evidence/matches/mechanics-save-section3-identity.json', 'evidence/matches/mechanics-save-pointer-controls.json', 'evidence/matches/mechanics-save-identity-profile-pointer.json')
CALLER_ADDRESSES = (0x02063eb0, 0x02063ebc, 0x02063ec8, 0x02068618, 0x020687dc, 0x02068830, 0x02068a0c, 0x02068a88)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(arm, rom_hash, matches):
    available = {}
    batches = list(json.loads((ROOT / 'recovery.json').read_text(encoding='utf-8'))['batches'])
    batches.extend({'report': path} for path in CALLER_REPORTS)
    for batch in batches:
        path = ROOT / batch['report']
        document = json.loads(path.read_text(encoding='utf-8'))
        for row in document.get('matches', document.get('functionMatches', [])):
            if row.get('module', 'main') in ('main', 'arm9') and row.get('exactAfterDeclaredRelocation', row.get('exactBytes', False)):
                available[int(row['address'], 16)] = (row, document, batch['report'])
    available.update({int(row['address'], 16): (row, {'romSha256': rom_hash, 'source': 'src/mechanics_save/identity_library.c', 'sourceSha256': sha((ROOT / 'src/mechanics_save/identity_library.c').read_bytes())}, None) for row, code in matches.values()})
    pending = [int(row['address'], 16) for row, code in matches.values()]
    pending.extend(CALLER_ADDRESSES)
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
                displacement = target - address - at
                if relocation.get('targetMode') == 'thumb':
                    value = 0xfa000000 | ((displacement & 2) << 23) | ((displacement >> 2) & 0xffffff)
                else:
                    value = (previous & 0xff000000) | ((displacement >> 2) & 0xffffff)
            else:
                raise AssertionError('Runtime serialization unsupported relocation')
            struct.pack_into('<I', code, at, value & 0xffffffff)
        size = row.get('bytes', row.get('size'))
        if code != arm[address - 0x02000000:address - 0x02000000 + size]:
            raise AssertionError(('Runtime serialization source span differs', row['name']))
        if row.get('isolatedCallerBinary'):
            linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
            if sha(linked) != row['isolatedCallerBinarySha256'] or linked != bytes(code):
                raise AssertionError('Actual MW caller bytes differ from ELF relocation hypothesis')
            code = bytearray(linked)
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
    own_addresses = {int(row['address'], 16) for row, code in matches.values()}
    caller_matches = {functions[address]['name']: (functions[address], functions[address]['code']) for address in CALLER_ADDRESSES}
    original_loader = caller_model.dependencies
    original_machine = caller_model.Uc
    contexts = []
    def tracked_machine(*args, **kwargs):
        machine = original_machine(*args, **kwargs)
        state = {'seen': set()}
        def hook(uc, address, size, current):
            if address in own_addresses:
                current['seen'].add(address)
        machine.hook_add(UC_HOOK_CODE, hook, state)
        contexts.append(state)
        return machine
    caller_model.dependencies = lambda *args: functions
    caller_model.Uc = tracked_machine
    try:
        report = caller_model.validate(arm, save, caller_matches, root)
    finally:
        caller_model.dependencies = original_loader
        caller_model.Uc = original_machine
    for state in contexts:
        if state['seen'] != own_addresses:
            raise AssertionError(('Connected library source entry missing', sorted(own_addresses - state['seen'])))
    additional = 0
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for address, function in functions.items():
                machine.mem_write(address, function['code'])
        state = {'role': None, 'result': 0, 'length': 0, 'seen': 0}
        def hook(uc, address, size, current):
            if address not in (0x0209cc88, 0x0209ccf4):
                return
            args = [uc.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
            if current['role'] == 'read':
                if address != 0x0209cc88 or args[0] != 0x021bb2b8 + current['index'] * 12 or args[1] != caller_model.OUTPUT:
                    raise AssertionError(('Typed Thumb query caller ABI', args))
                uc.mem_write(args[2], struct.pack('<I', current['length']))
                uc.mem_write(caller_model.OUTPUT, current['payload'])
            elif current['role'] == 'valid':
                if address != 0x0209ccf4 or args[:2] != [caller_model.NAME, 76]:
                    raise AssertionError(('Typed Thumb data-validation caller ABI', args))
            else:
                raise AssertionError('Unexpected typed Thumb contract entry')
            current['seen'] += 1
            destination = uc.reg_read(UC_ARM_REG_LR)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (current['result'], 0xdead0101, 0xdead0202, 0xdead0303)):
                uc.reg_write(register, value)
            uc.reg_write(UC_ARM_REG_CPSR, (uc.reg_read(UC_ARM_REG_CPSR) & ~0x20) | (0x20 if destination & 1 else 0))
            uc.reg_write(UC_ARM_REG_PC, destination & ~1)
        machine.hook_add(UC_HOOK_CODE, hook, state)
        incoming = [0x12340000 + index for index in range(8)]
        for index in (0, 1, 63):
            for success in (0, 1):
                for returned_length in (0, 75, 76, 77, 0xffffffff):
                    payload = bytes((index + offset * 7) & 255 for offset in range(76))
                    state.update({'role': 'read', 'result': success, 'length': returned_length, 'index': index, 'payload': payload, 'seen': 0})
                    machine.mem_write(caller_model.OUTPUT, bytes(76))
                    row = matches['saved_identity_record_data_read'][0]
                    actual = caller_model.invoke(machine, int(row['address'], 16), (index, 76, caller_model.OUTPUT), incoming)
                    if machine.reg_read(UC_ARM_REG_CPSR) & 0x20:
                        raise AssertionError('Typed Thumb query failed to return ARM state')
                    if actual != int(bool(success) and returned_length == 76) or state['seen'] != 1 or bytes(machine.mem_read(caller_model.OUTPUT, 76)) != payload:
                        raise AssertionError(('Typed Thumb query result/length contract', index, success, returned_length))
                    additional += 1
        for success in (0, 1, 0x80000000, 0xffffffff):
            state.update({'role': 'valid', 'result': success, 'seen': 0})
            row = matches['saved_identity_record_data_valid'][0]
            actual = caller_model.invoke(machine, int(row['address'], 16), (76, caller_model.NAME), incoming)
            if machine.reg_read(UC_ARM_REG_CPSR) & 0x20:
                raise AssertionError('Typed Thumb validation failed to return ARM state')
            if actual != int(bool(success)) or state['seen'] != 1:
                raise AssertionError(('Typed Thumb validation result contract', success))
            additional += 1
    report['sourcePatchedFunctions'] = len(functions)
    report['testedFunctions'] = list(matches)
    report['executedNewSourceEntries'] = [hex(address) for address in sorted(own_addresses)]
    report['additionalTypedThumbCallerContractCalls'] = additional
    report['thumbToArmReturnStateVerified'] = True
    report['actualMwLinkedCallerBytesPatched'] = all(row.get('isolatedCallerBinary') for row, code in matches.values())
    report['reusedAcceptedSources'] = [{key: value for key, value in function.items() if key != 'code'} for function in functions.values() if function['report']]
    report['retainedNativeEntries'] = [{'module': 'main', 'mode': 'Thumb' if address in THUMB_RETAINED else 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])} for address, size in RETAINED.items()]
    report['independentModelSources'] = [{'source': 'mechanics_save_section3_identity_oracle.py', 'sha256': sha((root / 'mechanics_save_section3_identity_oracle.py').read_bytes())}]
    report['observations'] += ['All nine new ARM library bodies execute in both native/source machines through the same520 actual-library protocols; insertion, lookup, free-slot search, parsing, writing, clearing and data wrappers retain effects across calls.', 'The68 additional typed Thumb caller contracts verify query-success/length matching, boolean normalization, ABI arguments and an explicit return-state transition from Thumb to ARM.']
    report['limitations'] = ['The nine ARM library wrappers receive source credit only after separate actual MW linker validation of their typed ARM/Thumb calls.', 'Thumb SDK identity/code/string/data routines and memory primitives remain native; their declared entry spans and complete ARM9 identity are pinned.', 'Positive online data-service behavior remains controlled caller contracts; the actual SDK offline protocols use zero initialization state.', 'Native-generated synthetic fixtures do not independently prove the retained SDK checksum/encoding algorithm or complete network/profile legality.', 'No original profile/input or semantic partition is changed.']
    return report

