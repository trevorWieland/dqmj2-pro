import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control48/native_itcm_01ffc7a0.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ffc7a0.json'
ADDRESS = 0x01FFC7A0
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
VALUES = list(range(24)) + [0xffffffff, 0x7fffffff, 0x80000000]


def execute(code, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x500000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    selector = VALUES[vector // 4]
    configuration = vector % 4
    signed_field = [-1, 0, 1, -0x80000000][configuration]
    status = [0, 4, 5, 0xffffffff][configuration]
    flag = [-128, 0, 1, 127][configuration]
    record = 0x03004000
    engine.mem_write(record + 0x58, bytes([flag & 255]))
    engine.mem_write(0x02246720, rng.randbytes(32))
    engine.mem_write(0x02246728, struct.pack('<i', signed_field))
    expected = [(0x02223C54, []), (0x020642DC, [])]
    if selector == 1:
        menu = 20 if signed_field >= 0 else 27
    elif selector == 2:
        expected.append((0x01FFA8D8, []))
        menu = 23 if status == 4 else 24
    else:
        menu = 18 if flag == 0 else 22
    expected.append((0x02089804, []) if 8 <= selector <= 15 else (0x020620E8, [menu, 1]))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[-2:] = [0x0301FFF0, 0x05000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, initial in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, initial)
    calls, writes, visited = [], [], set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        required = expected[len(calls)] if len(calls) < len(expected) else None
        arguments = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        if required is None or address != required[0] or arguments[:len(required[1])] != required[1]:
            raise ValueError('Menu dispatch selected a different helper, menu or arguments')
        if calls and bytes(uc.mem_read(0x02246734, 4)) != b'\1\0\0\0':
            raise ValueError('Menu dispatch failed to initialize state before the selector call')
        result = {0x02223C54: record, 0x020642DC: selector, 0x01FFA8D8: status}.get(address, rng.getrandbits(32))
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': arguments})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=1000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(expected):
        raise ValueError('Menu dispatch failed to complete its protocol')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Menu compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = report['matches'][0]
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen menu C changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Menu source stopped matching the complete native span and table')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    cases = []
    external = 0
    for vector in range(len(VALUES) * 4):
        expected, actual = execute(native, vector), execute(compiled, vector)
        if expected != actual:
            raise ValueError('Native and compiled menu effects differ')
        external += len(expected['calls']) * 2
        cases.append({'selector': hex(VALUES[vector // 4]), 'configuration': vector % 4,
                      'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['oracle'] = {'vectors': len(cases), 'nativeAndRecompiledCalls': len(cases) * 2, 'syntheticExternalCalls': external,
                       'nativeCalleeCalls': 0, 'verifiedReturn': True, 'independentMenuSelectionAssertions': True, 'records': cases,
                       'limitations': ['All sixteen table entries, unsigned out-of-range, signed global extrema, record flag values and status comparisons are checked',
                                       'External callers and the overlay-qualified record accessor are synthetic contracts, with no callee or gameplay semantics credit',
                                       'Void-source results are not assigned a semantic meaning; all registers/CPSR,ordered writes,call arguments and initialized memory are compared']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': len(cases), 'nativeAndRecompiledCalls': len(cases) * 2, 'syntheticExternalCalls': external})


if __name__ == '__main__':
    main()
