import json
import random
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control46/native_itcm_01ffbb44.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ffbb44.json'
ADDRESS = 0x01FFBB44
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
VALUES = list(range(40)) + [0xffffffff, 0xfffffff0, 0x7fffffff, 0x80000000]


def execute(code, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x200000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    engine.mem_write(0x021D4100, rng.randbytes(32))
    value = VALUES[vector]
    expected = [0x020642DC] + ([0x02089804] if 16 <= value <= 24 else [0x020620E8] if 25 <= value <= 27 else [])
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
        arguments = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        if len(calls) >= len(expected) or address != expected[len(calls)]:
            raise ValueError('Switch selected an unexpected external target or call order')
        if address == 0x020620E8 and arguments[:2] != [20, 1]:
            raise ValueError('Switch did not forward the required explicit arguments')
        if bytes(uc.mem_read(0x021D4114, 4)) != b'\1\0\0\0':
            raise ValueError('Switch did not initialize the state word before calling helpers')
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': arguments})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], value if address == 0x020642DC else rng.getrandbits(32))
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=1000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(expected):
        raise ValueError('Switch failed to return after the expected dispatch')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Dispatch compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = report['matches'][0]
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen dispatch C changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Dispatch C stopped matching its full native span and branch table')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    cases = []
    external = 0
    for vector in range(len(VALUES)):
        expected, actual = execute(native, vector), execute(compiled, vector)
        if expected != actual:
            raise ValueError('Native and compiled switch dispatch effects differ')
        external += len(expected['calls']) * 2
        cases.append({'selector': hex(VALUES[vector]), 'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['oracle'] = {'vectors': len(VALUES), 'nativeAndRecompiledCalls': len(VALUES) * 2, 'syntheticExternalCalls': external,
                       'nativeCalleeCalls': 0, 'verifiedReturn': True, 'independentDispatchAssertions': True, 'records': cases,
                       'limitations': ['All twelve table entries, both call destinations, unsigned underflow and upper out-of-range selectors are checked',
                                       'External helpers are deterministic synthetic contracts; their native code does not execute or gain credit',
                                       'Void source has no semantic result; registers/CPSR,ordered writes,call arguments and initialized memory are compared']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': len(VALUES), 'nativeAndRecompiledCalls': len(VALUES) * 2, 'syntheticExternalCalls': external})


if __name__ == '__main__':
    main()
