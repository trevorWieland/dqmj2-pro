import hashlib
import json
from pathlib import Path
import struct
import sys
import time

from project import ROOT, configuration, native_dependencies, read_json, verify_inputs, write_json

CONFIG = configuration()
native_dependencies(CONFIG)
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

MAIN = 0x021bd51c
IO = 0x021c6bfc
CONTROL = 0x020edcf0
STATE = 0x021d4c3c
FLAGS = 0x021d4cd8
BUFFER = 0x02500000
BACKEND = 0x020e5500
DESCRIPTOR = 0x02530000
OUTPUT = 0x02600000
STOP = 0x027ff800
PARTS = [(0x90, 0x3a68, MAIN), (0x3a68, 0x3a9c, 0x021b9eb4), (0x3a9c, 0x5d40, 0x021bb278), (0x5d40, 0x70d0, 0x021b9ee8)]
DATE = bytes(range(16))
TIME = bytes(range(0x30, 0x3c))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def checksum(data, start, end):
    return sum(struct.unpack_from('<I', data, at)[0] for at in range(start, end, 4)) & 0xffffffff

def seal(bank):
    struct.pack_into('<I', bank, 0x88, checksum(bank, 0x90, 0x70d0))
    struct.pack_into('<I', bank, 0x8c, checksum(bank, 0, 0x8c))
    return bytes(bank)

def compiled_functions(arm, rom_hash):
    functions = {}
    reports = [ROOT / 'evidence/matches/checksum.json', *sorted((ROOT / 'evidence/matches').glob('save*.json'))]
    for path in reports:
        document = read_json(path)
        rows = document.get('matches', document.get('functionMatches', []))
        if not rows:
            continue
        if document['romSha256'] != rom_hash:
            raise ValueError(('Protocol report ROM mismatch', str(path)))
        for row in rows:
            if not row.get('exactAfterDeclaredRelocation', row.get('exactBytes', False)):
                continue
            source = ROOT / (row.get('source') or document['source'])
            if sha(source.read_bytes()) != (row.get('sourceSha256') or document['sourceSha256']):
                raise ValueError(('Protocol source hash mismatch', str(source)))
            obj = ROOT / row['object']
            if sha(obj.read_bytes()) != row['objectSha256']:
                raise ValueError(('Protocol object hash mismatch', str(obj)))
            with obj.open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
                code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
            address = int(row['address'], 16)
            for relocation in row.get('relocations', []):
                offset = relocation['offset']
                target = int(relocation['target'], 16) + relocation['addend']
                value = struct.unpack_from('<I', code, offset)[0]
                if relocation['type'] == 2:
                    value = target & 0xffffffff
                elif relocation['type'] in (1, 28, 29):
                    value = (value & 0xff000000) | (((target - address - offset) >> 2) & 0xffffff)
                else:
                    raise ValueError('Unsupported protocol relocation')
                struct.pack_into('<I', code, offset, value)
            size = row.get('bytes', row.get('size'))
            expected = arm[address - 0x02000000:address - 0x02000000 + size]
            if code != expected:
                raise ValueError(('Protocol compiled span differs', row['name']))
            functions[address] = {'name': row['name'], 'code': bytes(code), 'report': str(path.relative_to(ROOT))}
    return functions

def expected_summary(bank):
    summary = bytearray(bytes([0xa5]) * 0x60)
    summary[:4] = bank[0x90:0x94]
    summary[4:0x18] = bank[0x98:0xac]
    ids = [struct.unpack_from('<I', bank, 0xb4 + slot * 4)[0] for slot in range(3)]
    present = 0
    for slot, identity in enumerate(ids):
        found = None
        if identity:
            for index in range(100):
                at = 0x1e8 + index * 0x84
                if struct.unpack_from('<I', bank, at + 0x14)[0] == identity:
                    found = bank[at:at + 0x84]
                    break
        if found is None:
            summary[0x18 + slot * 0x14:0x1a + slot * 0x14] = b'\xe3\x1b'
            summary[0x54 + slot * 2:0x56 + slot * 2] = bytes(2)
            summary[0x5a + slot] = 0
        else:
            present += 1
            summary[0x18 + slot * 0x14:0x2c + slot * 0x14] = found[:0x14]
            summary[0x54 + slot * 2:0x56 + slot * 2] = found[0x18:0x1a]
            limit = 50 if found[0x1c] < 4 else 75 if found[0x1c] < 10 else 100
            summary[0x5a + slot] = found[0x30] | (0x80 if found[0x30] == limit else 0)
    summary[0x5d] = present
    summary[0x5e] = bank[0x3a68]
    indices = [0xac, 0xad, 0xae, 0xaf, 0xb2, 0xb1, 0x22f]
    summary[0x5f] = sum(((bank[0x3994 + (index >> 3)] >> (index & 7)) & 1) << bit for bit, index in enumerate(indices))
    return summary

def expected_written_device(original, bank):
    output = bytearray(original)
    built = bytearray(bytes([0xa5]) * 0xe200)
    struct.pack_into('<III', built, 0, 0x5a4953, 0x10000, 0x70d0)
    built[0xc:0x1c] = DATE
    built[0x1c:0x28] = TIME
    built[0x28:0x88] = expected_summary(bank)
    built[0x90:0x70d0] = bank[0x90:0x70d0]
    struct.pack_into('<I', built, 0x88, checksum(built, 0x90, 0x70d0))
    struct.pack_into('<I', built, 0x8c, checksum(built, 0, 0x8c))
    built[0x7100:0xe1d0] = built[:0x70d0]
    output[:0xe200] = built
    return bytes(output)

def run_case(arm, source_functions, device_bytes, scenario, rebuilt):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, arm)
    machine.mem_write(0x021b9000, bytes(0x25000))
    if rebuilt:
        for address, function in source_functions.items():
            machine.mem_write(address, function['code'])
    machine.mem_write(FLAGS, struct.pack('<I', 0xffffffff))
    machine.mem_write(OUTPUT, bytes([0x77]) * 16)
    machine.mem_write(BACKEND, struct.pack('<I', DESCRIPTOR))
    machine.mem_write(DESCRIPTOR, bytes(0x80))
    machine.mem_write(0x020e5480, struct.pack('<I', 1))
    context = {'device': bytearray(device_bytes), 'pending': None, 'trace': [], 'allocations': {}, 'seen': set(), 'frames': 0, 'request': None}
    platform = {0x0200ff98: 'schedule', 0x02000b64: 'validate', 0x02007ff4: 'irq-disable', 0x02008008: 'irq-restore', 0x020068d4: 'queue-wait', 0x0200ffd4: 'bus-lock', 0x02010058: 'bus-unlock', 0x02011194: 'wait', 0x020060e4: 'allocate-lock', 0x0202a37c: 'allocate-head', 0x0202a44c: 'allocate-tail', 0x0202a498: 'free', 0x0200f3e0: 'date', 0x0200f48c: 'time', 0x020c22c4: 'message-open', 0x020c2330: 'message-close', 0x0200a41c: 'fifo-ready', 0x0200a440: 'fifo-send', 0x02008064: 'pause', 0x020072d0: 'cache-invalidate', 0x02007308: 'cache-clean', 0x0200732c: 'cache-drain', 0x02006924: 'queue-wake', 0x0200698c: 'thread-wake'}

    def backend_field(offset):
        return struct.unpack('<I', machine.mem_read(BACKEND + offset, 4))[0]

    def hook(uc, address, size, user):
        if address in source_functions:
            context['seen'].add(address)
        if address == 0x020108a8:
            packet = [uc.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)] + list(struct.unpack('<IIIII', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 20)))
            reading = packet[6] == 6
            role = ('read' if reading else 'write') + ('-async' if packet[5] else '')
            offset = packet[0] if reading else packet[1]
            if offset + packet[2] > len(context['device']):
                raise AssertionError(('Out-of-device request', role, offset, packet[2]))
            context['request'] = {'role': role, 'offset': offset, 'bytes': packet[2], 'operation': packet[6], 'mode': packet[7], 'final': packet[8], 'frame': context['frames'], 'commands': 0, 'writes': 0, 'verifications': 0}
            context['trace'].append(context['request'])
        if address not in platform:
            return
        role = platform[address]
        arguments = [uc.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        result = 0
        if role == 'schedule':
            if arguments[0] != 0x020106b8 or context['pending'] is not None:
                raise AssertionError('Backend schedule argument or overlap differs')
            request = context['request']
            context['pending'] = {'role': request['role'], 'ready': context['frames'] + 1 + scenario.get('read-delay' if request['role'] == 'read-async' else 'write-delay', 0), 'request': request}
            result = 1
        elif role == 'fifo-ready':
            result = 1
        elif role == 'irq-disable' and backend_field(0x114) & 0x20:
            source, destination, count = struct.unpack('<III', uc.mem_read(DESCRIPTOR + 0xc, 12))
            request = context['request'] or {'role': 'configure', 'commands': 0, 'writes': 0, 'verifications': 0}
            operation = backend_field(4)
            if operation:
                request['commands'] += 1
            error = int(scenario.get('prefix-failure', False)) if request['role'] == 'read' else scenario.get('read-error' if request['role'] == 'read-async' else 'write-error', 0)
            if operation in (0, 2) or request['role'] == 'configure':
                error = 0
            elif operation == 8:
                request['writes'] += 1
                if request['writes'] == scenario.get('write-fail-chunk', -1):
                    error = 1
            elif operation == 9:
                request['verifications'] += 1
                if request['verifications'] == scenario.get('verify-fail-chunk', -1):
                    error = 1
            offset = source if operation == 6 else destination
            if operation in (6, 8, 9) and offset + count > len(context['device']):
                raise AssertionError('Chunk exceeds virtual device')
            if not error:
                if operation == 6:
                    uc.mem_write(destination, bytes(context['device'][source:source + count]))
                elif operation == 8:
                    context['device'][destination:destination + count] = bytes(uc.mem_read(source, count))
                elif operation == 9:
                    error = int(context['device'][destination:destination + count] != uc.mem_read(source, count))
                elif operation not in (0, 2):
                    raise AssertionError(('Unsupported virtual command', operation))
            uc.mem_write(DESCRIPTOR, struct.pack('<I', error))
            uc.reg_write(UC_ARM_REG_R0, 11)
            uc.reg_write(UC_ARM_REG_R1, operation)
            uc.reg_write(UC_ARM_REG_R2, 1)
            uc.reg_write(UC_ARM_REG_PC, 0x02011210)
            return
        elif role in ('allocate-head', 'allocate-tail'):
            fail = scenario.get('load-allocation-failure' if role == 'allocate-head' else 'write-allocation-failure', False)
            if not fail:
                if context['allocations']:
                    raise AssertionError('Unexpected overlapping allocation')
                context['allocations'][BUFFER] = {'heap': arguments[0], 'bytes': arguments[1]}
                uc.mem_write(BUFFER, bytes([0xa5]) * 0x20000)
                result = BUFFER
        elif role == 'free':
            context['allocations'].pop(arguments[1], None)
        elif role == 'queue-wait':
            if context['pending'] is not None:
                raise AssertionError('Unexpected blocking wait during cooperative asynchronous operation')
        elif role == 'allocate-lock':
            result = 0x1234
        elif role == 'date':
            uc.mem_write(arguments[0], DATE)
        elif role == 'time':
            uc.mem_write(arguments[0], TIME)
        elif role.startswith('message-'):
            context['trace'].append({'role': role, 'frame': context['frames']})
        uc.reg_write(UC_ARM_REG_R0, result & 0xffffffff)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    for address in set(source_functions) | set(platform) | {0x020108a8}:
        machine.hook_add(UC_HOOK_CODE, hook, begin=address, end=address)

    def call(address, first=0, second=0):
        machine.reg_write(UC_ARM_REG_R0, first)
        machine.reg_write(UC_ARM_REG_R1, second)
        machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        began = time.monotonic()
        machine.emu_start(address, STOP, count=1000000)
        if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
            raise AssertionError('Protocol call exceeded execution bounds')
        return machine.reg_read(UC_ARM_REG_R0)

    if call(0x02027a14) != 1:
        raise AssertionError('Native device initialization failed')
    call(0x0207db24)
    control = struct.unpack('<BBBBIIIIII', machine.mem_read(CONTROL, 28))
    if control[5:10] != (0x70d0, 2, 0x80, 0x7100, 0x10000):
        raise AssertionError(('Configured save geometry differs', control))
    done = 0
    for frame in range(1, 121):
        context['frames'] = frame
        pending = context['pending']
        if pending and not scenario.get('read-pending' if pending['role'] == 'read-async' else 'write-pending', False) and frame >= pending['ready']:
            context['request'] = pending['request']
            call(0x020106b8, BACKEND)
            context['pending'] = None
        done = call(0x020c3258, OUTPUT, OUTPUT + 4)
        if done:
            break
    payloads = [bytes(machine.mem_read(destination, end - begin)) for begin, end, destination in PARTS]
    result = {'done': bool(done), 'frames': context['frames'], 'state': machine.mem_read(STATE, 1)[0], 'ticks': struct.unpack('<H', machine.mem_read(STATE + 2, 2))[0], 'phase': machine.mem_read(OUTPUT, 1)[0], 'error': struct.unpack('<I', machine.mem_read(OUTPUT + 4, 4))[0], 'flags': struct.unpack('<I', machine.mem_read(FLAGS, 4))[0], 'deviceSha256': sha(context['device']), 'payloadSha256': [sha(data) for data in payloads], 'configuredPageBytes': control[7], 'configuredStrideBytes': control[8], 'trace': context['trace'], 'outstandingAllocations': len(context['allocations']), 'executedSourceFunctions': sorted(source_functions[address]['name'] for address in context['seen'])}
    return result, bytes(context['device']), payloads

def main():
    identities = verify_inputs(CONFIG)
    save = CONFIG['save'].read_bytes()
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    functions = compiled_functions(arm, identities['rom']['sha256'])
    primary = bytearray(save[:0x7100])
    backup = bytearray(save[0x7100:0xe200])
    struct.pack_into('<I', primary, 0xac, 123456)
    struct.pack_into('<I', backup, 0xac, 654321)
    backup[0x4000] ^= 0x5a
    primary, backup = seal(primary), seal(backup)
    scenarios = [('distinct-valid', {}), ('delayed-valid', {'read-delay': 2, 'write-delay': 3}), ('bad-primary-valid-backup', {'bad-primary': True}), ('torn-backup-payload', {'bad-backup': 'payload'}), ('bad-backup-header', {'bad-backup': 'header'}), ('bad-backup-length', {'bad-backup': 'length'}), ('prefix-read-failure', {'prefix-failure': True}), ('load-allocation-failure', {'load-allocation-failure': True}), ('write-allocation-failure', {'write-allocation-failure': True}), ('read-device-error', {'read-error': 1}), ('write-device-error', {'write-error': 1}), ('write-failure-before-primary-complete', {'write-fail-chunk': 10}), ('write-failure-after-primary-complete', {'write-fail-chunk': 114}), ('write-verification-failure', {'verify-fail-chunk': 1}), ('pending-read', {'read-pending': True}), ('pending-write', {'write-pending': True})]
    results = []
    for label, scenario in scenarios:
        first, second = bytearray(primary), bytearray(backup)
        if scenario.get('bad-primary'):
            first[0] ^= 1
        if scenario.get('bad-backup') == 'payload':
            second[0x90] ^= 1
        elif scenario.get('bad-backup') == 'header':
            second[0x8c] ^= 1
        elif scenario.get('bad-backup') == 'length':
            second[4] ^= 1
        device = bytes(first + second + save[0xe200:])
        native, actual_device, payloads = run_case(arm, functions, device, scenario, False)
        rebuilt, rebuilt_device, rebuilt_payloads = run_case(arm, functions, device, scenario, True)
        if native != rebuilt or actual_device != rebuilt_device or payloads != rebuilt_payloads:
            raise AssertionError(('Native/recompiled protocol differs', label))
        successful = label in ('distinct-valid', 'delayed-valid', 'bad-primary-valid-backup')
        required = {'save_backend_worker', 'save_backend_command', 'save_backend_fifo_callback', 'save_backend_configure', 'save_backend_descriptor_select'}
        if successful and not required.issubset(native['executedSourceFunctions']):
            raise AssertionError('Required recovered backend bodies were not executed')
        pending = label.startswith('pending-')
        expected_device = expected_written_device(device, backup) if successful else device
        changed_prefix = 0
        if scenario.get('write-fail-chunk') or scenario.get('verify-fail-chunk'):
            changed_prefix = (scenario['write-fail-chunk'] - 1) * 0x100 if scenario.get('write-fail-chunk') else 0x100
            expected_device = expected_written_device(device, backup)[:changed_prefix] + device[changed_prefix:]
        if actual_device != expected_device or native['done'] == pending:
            raise AssertionError(('Protocol outcome differs', label, native))
        loaded = successful or label.startswith('write-') or label == 'pending-write'
        expected_payloads = [backup[begin:end] if loaded else bytes(end - begin) for begin, end, destination in PARTS]
        if payloads != expected_payloads:
            raise AssertionError(('Backup RAM restoration differs', label))
        expected_phase = 0x77 if pending else 19 if successful else 16 if scenario.get('bad-backup') else 3
        expected_error = 0x77777777 if successful or pending or scenario.get('bad-backup') else 0x20000000 if label.startswith('write-') else 0x50000000
        if native['phase'] != expected_phase or native['error'] != expected_error:
            raise AssertionError(('Protocol output differs', label, native))
        if native['flags'] != (0xffffffff if pending else 0xfffffffd):
            raise AssertionError('Recovery flag completion effect differs')
        bank_validity = []
        for at in (0, 0x7100):
            bank = actual_device[at:at + 0x7100]
            bank_validity.append(struct.unpack_from('<I', bank)[0] == 0x5a4953 and struct.unpack_from('<I', bank, 0x88)[0] == checksum(bank, 0x90, 0x70d0) and struct.unpack_from('<I', bank, 0x8c)[0] == checksum(bank, 0, 0x8c))
        if changed_prefix and bank_validity != [changed_prefix >= 0x7100, True]:
            raise AssertionError(('Interrupted virtual bank validity differs', label, bank_validity))
        results.append({'scenario': label, **native, 'nativeAndRecompiledEqual': True, 'independentExpectedDeviceAndRam': True, 'changedDevicePrefixBytes': changed_prefix if changed_prefix else 0xe200 if successful else 0, 'finalChecksumValidBanks': bank_validity})
    report = {'schemaVersion': 1, 'romSha256': identities['rom']['sha256'], 'saveSha256': identities['save']['sha256'], 'source': 'verify_save_protocol.py', 'sourceSha256': sha(Path(__file__).read_bytes()), 'matches': [], 'nativeSymbols': {}, 'protocolOnly': True, 'oracle': {'cases': len(results), 'nativeAndRecompiledProtocols': len(results) * 2, 'patchedSourceFunctions': len(functions), 'fifoBoundaries': ['0x0200a41c', '0x0200a440'], 'results': results}, 'limitations': ['The software control/type/block/load/record/summary/write/recovery, SDK dispatch, request backend, configuration/descriptor selection, chunk worker, command retry and FIFO callback bodies execute; FIFO completion, scheduler/interrupt/queue/bus/cache primitives, allocation, clocks and presentation remain isolated stubs.', 'The backend initialized word and descriptor pointer are seeded explicitly; full SDK initialization remains a separate dependency.', 'Asynchronous workers execute cooperatively between recovery frames; the IRQ provider supplies descriptor status/data effects and redirects into the actual matched channel11 FIFO callback. Physical timing/ARM7 effects remain unverified.', 'Actual type0x1001 selection gives page0x80 and save stride0x7100. The earlier protocol boundary stub supplied synthetic page0x100; that older geometry was not a native configuration observation.', 'Initialization0x02027A14 and lock0x02027ABC remain native dependencies until their drafts match.', 'Pending scenarios are bounded observations of continued waiting rather than claims of hardware completion or failure.', 'No original game/save, device file or audible emulator was used or modified.']}
    verify_inputs(CONFIG)
    write_json(ROOT / 'evidence/matches/save-write-protocol.json', report)
    print(json.dumps({'cases': len(results), 'nativeAndRecompiledProtocols': len(results) * 2, 'patchedSourceFunctions': len(functions), 'passed': True}, indent=2))

if __name__ == '__main__':
    main()
