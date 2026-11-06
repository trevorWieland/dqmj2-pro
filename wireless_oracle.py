import json
import random
import struct
import match_lowlevel as common
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

REGIONS = [(0x02380000, 0x30000), (0x027E0000, 0x20000), (0x037F8000, 0x18000),
           (0x03000000, 0x20000), (0x04000000, 0x2000), (0x04800000, 0x10000), (0x05000000, 0x1000)]
VALUES = [0, 1, 2, 3, 4, 5, 7, 8, 15, 16, 23, 24, 31, 32, 63, 64, 127, 128, 255, 256, 65535, 65536, 0x7fffffff, 0x80000000, 0xffffffff]


def execute(code, spec, vector):
    rng = random.Random(20261027 + vector)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for first, size in REGIONS:
        machine.mem_map(first, size)
        machine.mem_write(first, rng.randbytes(size))
    machine.mem_write(spec['address'], code)
    machine.mem_write(0x0380FFF4, struct.pack('<I', 0x03002000))
    for offset in (0x330, 0x334, 0x33a, 0x34c):
        machine.mem_write(0x03002000 + offset, struct.pack('<H', [0, 1, 2, 65535][vector % 4]))
    registers = [rng.getrandbits(32) for _ in common.REGISTERS]
    registers[0] = VALUES[vector] if vector < len(VALUES) else rng.getrandbits(32)
    registers[-2:] = [0x0301FFF0, 0x05000000]
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (0x20 if spec.get('mode') == 'thumb' else 0))
    for register, value in zip(common.REGISTERS, registers):
        machine.reg_write(register, value)
    contract = spec.get('wirelessContract')
    if contract:
        if contract.get('kind') == 'record-index':
            registers[0] = vector % 32
            machine.reg_write(common.REGISTERS[0], registers[0])
            machine.mem_write(0x0300231C, struct.pack('<I', 0x03006000))
            slot = 0x03006000 + registers[0] * 28
            machine.mem_write(slot, struct.pack('<H', [0, 1, 2, 32767, 32768, 65535, 0x1234, 0xabcd][(vector // 32) % 8]))
            old_value = bytes(machine.mem_read(slot, 2))
        elif contract.get('kind') == 'bit-query':
            registers[0] = vector % 32
            machine.reg_write(common.REGISTERS[0], registers[0])
            slot = 0x0300232C
            machine.mem_write(slot, struct.pack('<H', [0, 1, 2, 3, 32767, 32768, 65535, 0x1234][(vector // 32) % 8]))
            old_value = bytes(machine.mem_read(slot, 2))
        elif contract.get('kind') in ('shift-and-register-store', 'clear-state-register'):
            slot = 0x03002000 + contract['offset']
            old_value = bytes(machine.mem_read(slot, 2))
        else:
            slot = 0x03002000 + contract['offset']
            old_value = bytes(machine.mem_read(slot, 2))
    writes, visited = [], set()
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        if not spec['address'] <= address < spec['address'] + len(code):
            raise ValueError('Wireless caller reached a native callee outside this bounded source-only fixture')
        visited.add(address)
    machine.hook_add(UC_HOOK_CODE, trace)
    machine.emu_start(spec['address'] | int(spec.get('mode') == 'thumb'), 0x05000000, count=1000)
    if machine.reg_read(UC_ARM_REG_PC) != 0x05000000:
        raise ValueError('Wireless function did not return within the bounded instruction limit')
    if contract:
        if contract.get('kind') in ('record-index', 'bit-query'):
            required_result = struct.unpack('<H', old_value)[0]
            if contract['kind'] == 'bit-query':
                required_result &= 1 << registers[0]
            if machine.reg_read(common.REGISTERS[0]) != required_result or writes or bytes(machine.mem_read(slot, 2)) != old_value:
                raise ValueError('Bounded record index or bit-query result/absence of writes differs')
        elif contract.get('kind') in ('shift-and-register-store', 'clear-state-register'):
            if contract['kind'] == 'shift-and-register-store':
                field_value, hardware_value = (registers[0] >> 1) & 65535, registers[0] & 65535
                required = [[slot, 2, field_value], [contract['register'], 2, hardware_value]]
                if machine.reg_read(common.REGISTERS[0]) != 0:
                    raise ValueError('Shifted control setter did not return zero')
            else:
                field_value = hardware_value = 0
                required = [[contract['register'], 2, 0], [slot, 2, 0]]
            if writes != required or bytes(machine.mem_read(slot, 2)) != struct.pack('<H', field_value) or bytes(machine.mem_read(contract['register'], 2)) != struct.pack('<H', hardware_value):
                raise ValueError('Exact state/register halfword effects or write order differ')
        else:
            allowed = registers[0] <= contract['maximum']
            required = [[slot, 2, registers[0] & 65535]] if allowed else []
            stored = struct.pack('<H', registers[0] & 65535) if allowed else old_value
            if machine.reg_read(common.REGISTERS[0]) != (0 if allowed else 5) or writes != required or bytes(machine.mem_read(slot, 2)) != stored:
                raise ValueError('Unsigned range guard, exact halfword write or rejection preservation differs')
    return {'registers': [machine.reg_read(register) for register in common.REGISTERS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [common.sha(bytes(machine.mem_read(first, size))) for first, size in REGIONS]}


def verify(compiled, spec):
    if spec.get('program') is None and spec['module'] == 'arm7-main':
        contracts = {0x027E9090: {'maximum': 3, 'offset': 0x336}, 0x027E9344: {'maximum': 1, 'offset': 0x332},
                     0x027EBFEC: {'kind': 'record-index', 'vectors': 256},
                     0x027E9CC0: {'kind': 'shift-and-register-store', 'offset': 0x354, 'register': 0x0480803c}}
        if spec['address'] in contracts:
            spec = dict(spec, wirelessContract=contracts[spec['address']])
    if spec.get('program') == 'dwc/utility.bin/move/child.srl' and spec['module'] == 'utility-child-arm7-main' and spec['address'] == 0x027E9DF4:
        spec = dict(spec, wirelessContract={'kind': 'bit-query', 'vectors': 256})
    if spec.get('program') == 'dwc/utility.bin/move/child.srl' and spec['module'] == 'utility-child-arm7-main' and spec['address'] == 0x027F15BC:
        spec = dict(spec, wirelessContract={'kind': 'clear-state-register', 'offset': 0x4a4, 'register': 0x04808080})
    binary = (common.ROOT / spec['binary']).read_bytes()
    native = binary[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
    records, visited, results = [], set(), {}
    vectors = spec.get('wirelessContract', {}).get('vectors', 64)
    for vector in range(vectors):
        expected, actual = execute(native, spec, vector), execute(compiled, spec, vector)
        if expected != actual:
            raise ValueError('Wireless native and freshly compiled C effects differ')
        visited.update(expected['visited'])
        key = hex(expected['registers'][0])
        results[key] = results.get(key, 0) + 1
        records.append(common.sha(json.dumps(expected, sort_keys=True).encode()))
    return {'vectors': vectors, 'nativeAndRecompiledCalls': vectors * 2, 'nativeCalleeCalls': 0, 'verifiedReturn': True,
            'independentHalfwordRangeAssertions': bool(spec.get('wirelessContract')) and not spec['wirelessContract'].get('kind'),
            'independentRecordOrBitAssertions': spec.get('wirelessContract', {}).get('kind') in ('record-index', 'bit-query'),
            'independentControlWriteAssertions': spec.get('wirelessContract', {}).get('kind') in ('shift-and-register-store', 'clear-state-register'),
            'contract': spec.get('wirelessContract'),
            'stateSha256': records, 'observedReturnCounts': results, 'instructionAddressesVisited': [hex(value) for value in sorted(visited)],
            'limitations': ['The shared pointer at0380FFF4 is explicitly initialized to isolated aligned scratch RAM; hardware windows contain synthetic bytes',
                            'Argument boundaries and deterministic random words compare all registers/CPSR,ordered writes and initialized regions',
                            'This fixture compares measured CPU effects and does not assign wireless field meanings or claim physical hardware/controller behavior',
                            'No native callee body is loaded or executed; unsupported pointer/callback paths remain explicit']}
