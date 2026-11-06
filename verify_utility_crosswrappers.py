import argparse
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
VALUES = [0, 1, 2, 255, 65535, 0x7fffffff, 0x80000000, 0xffffffff]


def execute(code, spec, vector):
    rng = random.Random(20261027 + vector)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    regions = [(0x02000000, 0x23000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in regions:
        machine.mem_map(first, size)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(spec['address'], code)
    arguments = [VALUES[vector % 8], VALUES[(vector // 8) % 8], rng.getrandbits(32), rng.getrandbits(32)]
    if vector >= 64:
        arguments[:2] = [rng.getrandbits(32), rng.getrandbits(32)]
    address = spec['address']
    required_result = 0xA5700000 | vector
    returned_results = {}
    if address == 0x0200EE4C:
        expected = [(0x0200EC60, [arguments[0], arguments[1], 65535, 2, 1])]
    elif address == 0x020103D4:
        expected = [(0x020103F0, [int(arguments[0] == 1), 0, 0, 1])]
    elif address == 0x0200EED4:
        expected = [(0x0200F09C, [arguments[0], 1]), (0x02009240, [arguments[0]])]
    elif address in (0x0200E210, 0x0200E1E4, 0x0200E1B8):
        gate = VALUES[vector % 8]
        status = VALUES[(vector // 8) % 8]
        channel = {0x0200E210: 1, 0x0200E1E4: 2, 0x0200E1B8: 9}[address]
        probe = (0x0200DAD4, []) if address == 0x0200E210 else (0x0200DA80, [1, 2 if address == 0x0200E1E4 else 7])
        expected = [probe]
        returned_results[probe[0]] = gate
        required_result = gate
        if gate == 0:
            expected.extend([(0x0200DC5C, [channel, arguments[0]]), (0x0200DB84, [channel, 0])])
            returned_results[0x0200DB84] = status
            required_result = status or 2
    else:
        raise ValueError('Unrecognized frozen wrapper identity')
    registers = [rng.getrandbits(32) for _ in common.REGISTERS]
    registers[:4] = arguments
    registers[-2:] = [0x0301FFF0, 0x05000000]
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x30)
    for register, value in zip(common.REGISTERS, registers):
        machine.reg_write(register, value)
    calls, writes, visited = [], [], set()
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def trace(uc, location, size, user):
        if address <= location < address + len(code):
            visited.add(location)
            return
        required = expected[len(calls)] if len(calls) < len(expected) else None
        actual = [uc.reg_read(register) for register in common.REGISTERS[:4]]
        stack = list(struct.unpack('<I', bytes(uc.mem_read(uc.reg_read(common.REGISTERS[-2]), 4))))
        if required is None or location != required[0] or (actual + stack)[:len(required[1])] != required[1]:
            raise ValueError('Thumb wrapper failed its explicit call order/argument/stack contract')
        if not uc.reg_read(UC_ARM_REG_CPSR) & 0x20:
            raise ValueError('Measured Thumb callee entry lost its declared mode')
        returned = uc.reg_read(common.REGISTERS[-1])
        scratch = 0x03008000 + len(calls) * 4
        payload = rng.getrandbits(32)
        uc.mem_write(scratch, struct.pack('<I', payload))
        writes.append([scratch, 4, payload])
        calls.append({'address': hex(location), 'arguments': actual, 'stackArguments': stack if len(required[1]) > 4 else []})
        for register in common.REGISTERS[:4] + [common.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        result = returned_results.get(location, required_result if len(calls) == len(expected) else rng.getrandbits(32))
        uc.reg_write(common.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x30)
        uc.reg_write(UC_ARM_REG_PC, returned)
    machine.hook_add(UC_HOOK_CODE, trace)
    machine.emu_start(address | 1, 0x05000000, count=1000)
    if machine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(expected) or machine.reg_read(common.REGISTERS[0]) != required_result:
        raise ValueError('Thumb wrapper failed to preserve input or forward the final helper result')
    return {'registers': [machine.reg_read(register) for register in common.REGISTERS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [utility_runtime.sha(bytes(machine.mem_read(first, size))) for first, size in regions]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', choices=['crossreuse02', 'crossreuse03'], default='crossreuse02')
    args = parser.parse_args()
    path = ROOT / f'evidence/matches/utility-{args.batch}.json'
    report = json.loads(path.read_text())
    identities = {'crossreuse02': {0x0200EE4C, 0x020103D4, 0x0200EED4}, 'crossreuse03': {0x0200E210, 0x0200E1E4, 0x0200E1B8}}
    if {int(entry['address'], 0) for entry in report['matches']} != identities[args.batch]:
        raise ValueError('Frozen utility wrapper batch identities changed')
    results = []
    external = 0
    for old in report['matches']:
        provenance = old['sourceReuseProvenance']
        for filename, digest in [(old['source'], old['sourceSha256']), (provenance['source'], provenance['sourceSha256'])]:
            if utility_runtime.sha((ROOT / filename).read_bytes()) != digest:
                raise ValueError('Frozen wrapper C source or origin provenance changed')
        spec = utility_code.accepted_spec(old)
        flags = old['compilerFlags']
        entry, compiled = utility_code.compile_compare(ROOT / old['source'], dict(spec, compilerPath=ROOT / old['compiler']),
                                                       int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
        if compiled is None:
            raise ValueError('Wrapper source no longer matches all native bytes and relocations')
        binary = (ROOT / spec['binary']).read_bytes()
        native = binary[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
        records = []
        total = 0
        for vector in range(128):
            expected, actual = execute(native, spec, vector), execute(compiled, spec, vector)
            if expected != actual:
                raise ValueError('Native and freshly compiled Thumb wrapper effects differ')
            total += len(expected['calls']) * 2
            records.append({'vector': vector, 'stateSha256': utility_runtime.sha(json.dumps(expected, sort_keys=True).encode())})
        external += total
        entry['sourceReuseProvenance'] = provenance
        entry['oracle'] = {'vectors': 128, 'nativeAndRecompiledCalls': 256, 'syntheticExternalCalls': total, 'nativeCalleeCalls': 0,
                           'verifiedReturn': True, 'independentCallAndStackAssertions': True, 'records': records,
                           'independentFailureAndFallbackAssertions': args.batch == 'crossreuse03',
                           'limitations': ['All callees are explicit synthetic Thumb contracts; none of their native bodies execute or get source credit',
                                           ('Register/stack argument order, exact-one Boolean normalization, retained input and final return forwarding are checked' if args.batch == 'crossreuse02' else
                                            'Early probe failures, explicit channel and retained-input forwarding, nonzero status propagation and zero-status fallback to2 are checked'),
                                           'Registers R0-R12/SP/LR,CPSR,ordered writes,callee modes and initialized memory are compared',
                                           'Whole utility linking and nested container regeneration remain separately required']}
        results.append(entry)
    report.update(matches=results)
    path.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': len(results), 'bytes': sum(entry['bytes'] for entry in results), 'cases': len(results) * 128,
           'nativeAndRecompiledCalls': len(results) * 256, 'syntheticExternalCalls': external, 'nativeCalleeCalls': 0})


if __name__ == '__main__':
    main()
