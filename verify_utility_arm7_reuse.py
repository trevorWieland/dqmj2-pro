import hashlib
import json
import random
import struct
from pathlib import Path
import match_lowlevel as common
import utility_code
import utility_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/utility-crossreuse05.json'
RETURN = 0x05000000
REGIONS = [(0x027E0000, 0x20000), (0x037F8000, 0x18000), (0x03000000, 0x20000), (0x04800000, 0x10000), (RETURN, 0x1000)]


def setter_engine(code):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for address in (0x027EB000, 0x0380F000, 0x03002000, 0x0301F000, RETURN):
        machine.mem_map(address, 0x1000)
    machine.mem_write(0x027EB45C, code)
    machine.mem_write(0x0380FFF4, struct.pack('<I', 0x03002000))
    writes = []
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    return machine, writes


def setter(machine, writes, value):
    flags = (value * 0x9e3779b1) & 0xffffffff
    machine.mem_write(0x0300232C, b'\x5a\xa5')
    machine.mem_write(0x03002340, struct.pack('<I', flags))
    registers = [(value * 0x6a09e667 + index * 0x9e3779b1) & 0xffffffff for index in range(13)] + [0x0301FFF0, RETURN]
    registers[0] = value
    machine.reg_write(UC_ARM_REG_CPSR, ((value & 15) << 28) | 0x10)
    for register, initial in zip(common.REGISTERS, registers):
        machine.reg_write(register, initial)
    writes.clear()
    machine.emu_start(0x027EB45C, RETURN, count=100)
    valid = bool(value & 0x7ffe)
    expected_writes = [[0x0300232C, 2, value], [0x03002340, 4, flags | 4]] if valid else []
    actual = [machine.reg_read(register) for register in common.REGISTERS]
    if machine.reg_read(UC_ARM_REG_PC) != RETURN or actual[0] != (0 if valid else 5) or actual[4:] != registers[4:] or writes != expected_writes:
        raise ValueError('Halfword control setter disagrees with independent mask/field/dirty-bit expectations')
    required = struct.pack('<H', value if valid else 0xa55a) + struct.pack('<I', flags | 4 if valid else flags)
    stored = bytes(machine.mem_read(0x0300232C, 2)) + bytes(machine.mem_read(0x03002340, 4))
    if stored != required:
        raise ValueError('Control setter changed the wrong field or changed state on a rejected input')
    return struct.pack('<16I', *actual, machine.reg_read(UC_ARM_REG_CPSR)) + stored


def execute(code, spec, vector):
    rng = random.Random(20261027 + vector)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for first, size in REGIONS:
        machine.mem_map(first, size)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(spec['address'], code)
    control, source, message = 0x03002000, 0x03004000, 0x03006000
    machine.mem_write(0x0380FFF4, struct.pack('<I', control))
    arguments = [rng.getrandbits(32) for _ in range(4)]
    ring = spec['address'] == 0x027E95BC
    boundary = 0x04805F60
    current_span = [128, 256, 1024][vector % 3]
    new_span = current_span + 16 if vector & 1 else current_span
    if ring:
        lengths = [0, 1, 2, 3, 7, 8, 9, 63, 64, 65, 127, 128]
        count = lengths[vector % len(lengths)]
        destination = boundary - [0, 2, 4, 8, 64, 128][(vector // len(lengths)) % 6]
        rounded = (count + 1) & ~1
        first_count = min(rounded, boundary - destination)
        remainder = rounded - first_count
        arguments[:3] = [source, destination, count]
        expected = [(0x037FE6EC, [destination, source, first_count])]
        if remainder:
            expected.append((0x037FE6EC, [boundary - new_span, source + first_count, remainder]))
        machine.mem_write(control + 0x3de, struct.pack('<H', current_span))
        hardware = bytearray(rng.randbytes(0x10000))
        machine.mem_write(0x04800000, bytes(hardware))
        for _, args in expected:
            begin = args[0] - 0x04800000
            hardware[begin:begin + args[2]] = bytes(machine.mem_read(args[1], args[2]))
        required_message = None
    else:
        state = [0, 1, 2, 65535][vector % 4]
        guard = [0, 1, 2, 0xffffffff][(vector // 4) % 4]
        outputs = [(0x1234 + vector) & 65535, (0xabcd ^ vector) & 65535]
        machine.mem_write(0x027F9A40, struct.pack('<I', control))
        machine.mem_write(control, struct.pack('<H', state))
        required_message = bytearray(rng.randbytes(32))
        machine.mem_write(message, bytes(required_message))
        expected = []
        if state == 1:
            expected.append((0x027E8228, []))
        expected.extend([(0x0380576C, []), (0x038057C8, [message])])
        result_code = 3 if state != 1 else 1 if guard == 0 else 0
        struct.pack_into('<HH', required_message, 0, 5, result_code)
        if state == 1 and guard == 0:
            struct.pack_into('<HH', required_message, 4, *outputs)
    registers = [rng.getrandbits(32) for _ in common.REGISTERS]
    registers[:4] = arguments
    registers[-2:] = [0x0301FFF0, RETURN]
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, initial in zip(common.REGISTERS, registers):
        machine.reg_write(register, initial)
    calls, writes, visited = [], [], set()
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def store(uc, address, payload):
        uc.mem_write(address, payload)
        writes.append([address, len(payload), payload.hex()])
    def trace(uc, address, size, user):
        if spec['address'] <= address < spec['address'] + len(code):
            visited.add(address)
            return
        required = expected[len(calls)] if len(calls) < len(expected) else None
        actual = [uc.reg_read(register) for register in common.REGISTERS[:4]]
        if required is None or address != required[0] or actual[:len(required[1])] != required[1] or uc.reg_read(UC_ARM_REG_CPSR) & 0x20:
            raise ValueError('ARM7 source changed its explicit ARM callee/argument/order contract')
        returned_value = 0xc0200000 | vector
        if ring:
            store(uc, actual[0], bytes(uc.mem_read(actual[1], actual[2])))
            if not calls and remainder:
                store(uc, control + 0x3de, struct.pack('<H', new_span))
        elif address == 0x027E8228:
            if actual[0] == actual[1] or any(pointer & 1 or not 0x0301FFB0 <= pointer <= 0x0301FFEE for pointer in actual[:2]):
                raise ValueError('Protocol guard did not receive two separate stack halfword outputs')
            for pointer, value in zip(actual[:2], outputs):
                store(uc, pointer, struct.pack('<H', value))
            returned_value = guard
        elif address == 0x0380576C:
            returned_value = message
        elif address == 0x038057C8:
            if bytes(uc.mem_read(message, 32)) != bytes(required_message):
                raise ValueError('Protocol message header/code or guarded halfwords are wrong')
        returned = uc.reg_read(common.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': actual})
        for register in common.REGISTERS[:4] + [common.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(common.REGISTERS[0], returned_value)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, returned)
    machine.hook_add(UC_HOOK_CODE, trace)
    machine.emu_start(spec['address'], RETURN, count=2000)
    if machine.reg_read(UC_ARM_REG_PC) != RETURN or len(calls) != len(expected) or machine.reg_read(common.REGISTERS[0]) != 0xc0200000 | vector:
        raise ValueError('ARM7 source did not return its final helper result')
    if ring:
        if bytes(machine.mem_read(0x04800000, 0x10000)) != bytes(hardware):
            raise ValueError('Rounded copy/wrap destination bytes or untouched synthetic MMIO differ')
    elif struct.unpack('<H', bytes(machine.mem_read(control, 2)))[0] != (2 if state == 1 and guard else state):
        raise ValueError('Protocol state transition differs from the independent expectation')
    return {'registers': [machine.reg_read(register) for register in common.REGISTERS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [utility_runtime.sha(bytes(machine.mem_read(first, size))) for first, size in REGIONS]}


def main():
    report = json.loads(REPORT.read_text())
    if {int(entry['address'], 0) for entry in report['matches']} != {0x027EB45C, 0x027E95BC, 0x027E8418}:
        raise ValueError('Frozen ARM7 C reuse batch identities changed')
    results = []
    for old in report['matches']:
        provenance = old['sourceReuseProvenance']
        for path, digest in [(old['source'], old['sourceSha256']), (provenance['source'], provenance['sourceSha256'])]:
            if utility_runtime.sha((ROOT / path).read_bytes()) != digest:
                raise ValueError('Frozen ARM7 reused C or origin source changed')
        spec = utility_code.accepted_spec(old)
        if spec['processor'] != 'arm7' or spec['mode'] != 'arm':
            raise ValueError('Frozen ARM7 source CPU/mode changed')
        flags = old['compilerFlags']
        entry, compiled = utility_code.compile_compare(ROOT / old['source'], dict(spec, compilerPath=ROOT / old['compiler']),
                                                       int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
        if compiled is None:
            raise ValueError('ARM7 reused C stopped matching its full native span and relocations')
        binary = (ROOT / spec['binary']).read_bytes()
        native = binary[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
        digest = hashlib.sha256()
        external = 0
        vectors = 65536 if spec['address'] == 0x027EB45C else 128
        if vectors == 65536:
            first, first_writes = setter_engine(native)
            second, second_writes = setter_engine(compiled)
            for value in range(vectors):
                expected, actual = setter(first, first_writes, value), setter(second, second_writes, value)
                if expected != actual:
                    raise ValueError('Native and compiled halfword setter register/flag effects differ')
                digest.update(struct.pack('<H', value) + expected)
        else:
            for vector in range(vectors):
                expected, actual = execute(native, spec, vector), execute(compiled, spec, vector)
                if expected != actual:
                    raise ValueError('Native and compiled ARM7 protocol/copy effects differ')
                external += len(expected['calls']) * 2
                digest.update(json.dumps(expected, sort_keys=True).encode())
        entry['sourceReuseProvenance'] = provenance
        entry['oracle'] = {'vectors': vectors, 'nativeAndRecompiledCalls': vectors * 2, 'syntheticExternalCalls': external,
                           'nativeCalleeCalls': 0, 'verifiedReturn': True, 'exhaustiveHalfwordDomain': vectors == 65536,
                           'independentEffectsAndCallAssertions': True, 'stateSha256': digest.hexdigest(),
                           'limitations': ['The setter exhausts all16-bit inputs; mask rejects leave fields unchanged and valid values set the exact halfword/dirty bit',
                                           'The copy fixture models bounded nonnegative lengths, even-byte rounding, boundary splits, refreshed wrap span and exact synthetic-MMIO bytes',
                                           'The message fixture checks status guards, two stack halfword outputs, state transition and complete initialized message bytes',
                                           'External helpers are synthetic ARM contracts and physical MMIO is not modeled; no native callee or historical field meaning receives credit',
                                           'Registers R0-R12/SP/LR,CPSR,ordered writes,call mode/arguments and initialized memory effects are compared']}
        results.append(entry)
    report.update(matches=results)
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': len(results), 'bytes': sum(entry['bytes'] for entry in results),
           'cases': sum(entry['oracle']['vectors'] for entry in results),
           'nativeAndRecompiledCalls': sum(entry['oracle']['nativeAndRecompiledCalls'] for entry in results)})


if __name__ == '__main__':
    main()
