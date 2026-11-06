import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control47/native_itcm_01ffc654.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01ffc654.json'
ADDRESS = 0x01FFC654
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def execute(code, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x200000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    context = 0x03008000
    ids = [(vector << 8) + index + 1 for index in range(6)]
    engine.mem_write(context + 28, struct.pack('<6I', *ids))
    engine.mem_write(0x01FFFAA4, rng.randbytes(0x100))
    expected = [(0x020633B0, []), (0x02008D78, [0x01FFFAB0, 0, 6]), (0x02008D78, [0x01FFFAE0, 0, 192])]
    for index in range(6):
        expected.append((0x02062A10, [ids[index]]))
        if vector & (1 << index):
            expected.append((0x02046AF4, [0, 0x03002000 + index * 0x100, 0, 0, 0x01FFFAE0 + index * 32, 255]))
    expected.append((0x020BB1B4, [6, 0x01FFFAC8, 0x01FFFAB0, 0x01FFFAA4]))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[-2:] = [0x0301FFF0, 0x05000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, initial in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, initial)
    calls, writes, visited = [], [], set()
    def store(uc, location, payload):
        uc.mem_write(location, payload)
        writes.append([location, len(payload), payload.hex()])
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        arguments = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        stack = list(struct.unpack('<2I', bytes(uc.mem_read(uc.reg_read(matcher.REGISTERS[-2]), 8))))
        required = expected[len(calls)] if len(calls) < len(expected) else None
        if required is None or address != required[0] or (arguments + stack)[:len(required[1])] != required[1]:
            raise ValueError('Six-record initialization called the wrong helper or arguments')
        result = context if address == 0x020633B0 else rng.getrandbits(32)
        if address == 0x02008D78:
            store(uc, arguments[0], bytes([arguments[1]]) * arguments[2])
        if address == 0x02062A10:
            index = ids.index(arguments[0])
            result = 0x03002000 + index * 0x100 if vector & (1 << index) else 0
        if address == 0x02046AF4:
            index = (arguments[1] - 0x03002000) // 0x100
            store(uc, stack[0], bytes([index + 1]) * 32)
        if address == 0x020BB1B4:
            pointers = list(struct.unpack('<6I', bytes(uc.mem_read(0x01FFFAC8, 24))))
            if pointers != [0x01FFFAE0 + index * 32 for index in range(6)] or bytes(uc.mem_read(0x01FFFAB0, 6)) != bytes(6):
                raise ValueError('Six-record registration did not receive the initialized pointer table and flags')
            for index in range(6):
                required_bytes = bytes([index + 1 if vector & (1 << index) else 0]) * 32
                if bytes(uc.mem_read(0x01FFFAE0 + index * 32, 32)) != required_bytes:
                    raise ValueError('Six-record output slice overlaps or an absent record was not left zero')
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': arguments, 'stackArguments': stack if address == 0x02046AF4 else []})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=3000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(expected):
        raise ValueError('Six-record initialization did not finish the expected protocol')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Six-record compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = report['matches'][0]
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen six-record C source changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Six-record source stopped matching the complete native span')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    cases = []
    external = 0
    for vector in range(64):
        expected, actual = execute(native, vector), execute(compiled, vector)
        if expected != actual:
            raise ValueError('Native and compiled six-record effects differ')
        external += len(expected['calls']) * 2
        cases.append({'recordPresenceMask': vector, 'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['sourceCallAliases'] = {'native_fn_first_02062a10': '0x02062a10', 'native_fn_second_02062a10': '0x02062a10'}
    entry['oracle'] = {'vectors': 64, 'nativeAndRecompiledCalls': 128, 'syntheticExternalCalls': external, 'nativeCalleeCalls': 0,
                       'verifiedReturn': True, 'independentPointerTableAndSliceAssertions': True, 'records': cases,
                       'limitations': ['Two separate C declarations bind to the same measured ARM target to preserve the native branch/call-site distinction; their historical source identities are unknown',
                                       'All 64 record-presence patterns and six source-ID arguments, destination slices, clearing and six-argument copy forwarding are checked',
                                       'External helper bodies use synthetic contracts, not native implementations; no callee gets source credit',
                                       'Registers/CPSR,ordered writes,call arguments,stack forwarding and initialized memory are compared']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': 64, 'nativeAndRecompiledCalls': 128, 'syntheticExternalCalls': external})


if __name__ == '__main__':
    main()
