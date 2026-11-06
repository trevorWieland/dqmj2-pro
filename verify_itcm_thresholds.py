import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control50/native_itcm_01ffbffc.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ffbffc.json'
ADDRESS = 0x01FFBFFC
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
VALUES = [-0x80000000, -10000001, -101, -10, -9, -1, 0, 1, 9, 10, 101, 0x7fffffff]
AGES = [(0, 0), (1800, 1800), (1801, 1801), (3600, 1800), (3600, 1801), (3601, 0), (0xffffffff, 0)]


def signed(value):
    return (value + 0x80000000) % 0x100000000 - 0x80000000


def quotient(value, divisor):
    return abs(value) // divisor * (-1 if value < 0 else 1)


def vectors():
    result = []
    for count in range(11):
        for ages in AGES:
            for tag_match in (False, True):
                result.append((VALUES[len(result) % len(VALUES)], count, ages, tag_match))
    for value in VALUES:
        for count in range(11):
            result.append((value, count, (3600, 1801), True))
    return result


def execute(code, case, vector, table):
    value, count, ages, tag_match = case
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x200000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    engine.mem_write(0x01FFBB04, struct.pack('<12i', *table))
    status, record, expected_pointer = 0x03002000, 0x03004000, 0x03007000
    bits = ((1 << count) - 1) | ((vector & 63) << 10)
    engine.mem_write(record + 0x1946, struct.pack('<H', bits))
    tag = rng.getrandbits(32)
    engine.mem_write(expected_pointer, struct.pack('<I', tag if tag_match else tag ^ 1))
    argument = rng.getrandbits(32)
    expected = [(0x01FFBB38, []), (0x02063F48, []),
                (0x020BA5A4, [argument, 0x020E2C68, 65535]),
                (0x020BA5A4, [argument, 0x020E2C74, 65535]), (0x020894C8, [])]
    result = 0
    if tag_match:
        expected.append((0x01FFBB38, []))
        if ages[0] > 3600:
            result = 0x7fffff
        else:
            expected.append((0x01FFBB38, []))
            lower = 5 - count // 2 if count < 8 else 1
            upper = lower + 5
            if ages[1] > 1800:
                lower -= 1
                upper += 1
            current = quotient(value, 10)
            lower_value = quotient(signed(current * table[lower]), 100)
            upper_value = quotient(signed(current * table[upper]), 100)
            result = 0x7fffff if upper_value < current < lower_value else 0
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[0], registers[-2], registers[-1] = argument, 0x0301FFF0, 0x05000000
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, initial in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, initial)
    calls, writes, visited = [], [], set()
    status_calls = 0
    parse_calls = 0
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, contents, user: writes.append([address, size, contents & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        nonlocal status_calls, parse_calls
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        required = expected[len(calls)] if len(calls) < len(expected) else None
        arguments = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        if required is None or address != required[0] or arguments[:len(required[1])] != required[1]:
            raise ValueError('Threshold routine called a different helper, label or arguments')
        returned_value = rng.getrandbits(32)
        if address == 0x01FFBB38:
            age = 0 if status_calls == 0 else ages[status_calls - 1]
            uc.mem_write(status, struct.pack('<iI', value, age))
            writes.append([status, 8, struct.pack('<iI', value, age).hex()])
            status_calls += 1
            returned_value = status
        elif address == 0x02063F48:
            returned_value = record
        elif address == 0x020894C8:
            returned_value = expected_pointer
        elif address == 0x020BA5A4:
            returned_value = tag if parse_calls == 0 else rng.getrandbits(32)
            parse_calls += 1
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': arguments})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], returned_value)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=2000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(expected) or engine.reg_read(matcher.REGISTERS[0]) != result:
        raise ValueError('Threshold result differs from independent signed division, wrapped product and bounded table selection')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Threshold function compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = report['matches'][0]
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen threshold function C source changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Threshold routine stopped matching its entire native span')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    table = list(struct.unpack('<12i', binary[0x3b04:0x3b34]))
    cases = []
    external = 0
    for vector, case in enumerate(vectors()):
        expected, actual = execute(native, case, vector, table), execute(compiled, case, vector, table)
        if expected != actual:
            raise ValueError('Native and compiled threshold function effects differ')
        external += len(expected['calls']) * 2
        cases.append({'value': case[0], 'setBits': case[1], 'ageReadings': list(case[2]), 'tagMatches': case[3],
                      'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['oracle'] = {'vectors': len(cases), 'nativeAndRecompiledCalls': len(cases) * 2, 'syntheticExternalCalls': external,
                       'nativeCalleeCalls': 0, 'verifiedReturn': True, 'independentSignedArithmeticAndIndexAssertions': True, 'records': cases,
                       'limitations': ['Signed division truncates toward zero; products wrap modulo 2^32 before signed interpretation, including extrema',
                                       'Only the lowest ten flags are counted; all eleven counts, threshold ages and mismatching tags are covered',
                                       'Status helper supplies two independent age readings to require a reload; all external native bodies remain unexecuted and uncredited',
                                       'The twelve-word numeric table is native input state and is reconstructed separately in evidence/data/itcm-thresholds.json',
                                       'Registers/CPSR,ordered writes,call arguments and initialized memory are compared']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': len(cases), 'nativeAndRecompiledCalls': len(cases) * 2, 'syntheticExternalCalls': external})


if __name__ == '__main__':
    main()
